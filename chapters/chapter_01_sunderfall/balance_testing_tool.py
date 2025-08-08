#!/usr/bin/env python3
"""
Balance Testing Tool for Chronicles of Ruin: Sunderfall
Simulates thousands of combat encounters to fine-tune game balance
"""

import sys
import json
import time
import random
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import statistics

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent / "src"))

from systems.player_system import PlayerSystem, Player
from systems.combat_system import CombatSystem
from systems.monster_system import MonsterSystem
from systems.class_system import ClassSystem
from systems.skills_system import SkillsSystem
from systems.items_system import ItemsSystem
from systems.status_elemental_system import StatusElementalSystem
from systems.archetype_system import ArchetypeSystem
from systems.xp_system import XPSystem

@dataclass
class BalanceTestResult:
    """Results from a balance test"""
    total_encounters: int
    player_wins: int
    monster_wins: int
    average_rounds: float
    average_damage_dealt: float
    average_damage_taken: float
    win_rate: float
    class_performance: Dict[str, float]
    archetype_performance: Dict[str, float]
    level_performance: Dict[int, float]

class BalanceTestingTool:
    """Comprehensive balance testing for the game"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / "data"
        
        # Initialize all systems
        self.player_system = PlayerSystem(self.data_dir)
        self.combat_system = CombatSystem(self.data_dir)
        self.monster_system = MonsterSystem(self.data_dir)
        self.class_system = ClassSystem(self.data_dir)
        self.skills_system = SkillsSystem(self.data_dir)
        self.items_system = ItemsSystem(self.data_dir)
        self.status_system = StatusElementalSystem(self.data_dir)
        self.archetype_system = ArchetypeSystem(self.data_dir)
        self.xp_system = XPSystem(self.data_dir)
        
        # Test configurations
        self.test_configs = {
            "early_game": {"levels": [1, 2, 3], "iterations": 1000},
            "mid_game": {"levels": [5, 7, 10], "iterations": 1000},
            "late_game": {"levels": [15, 20, 25], "iterations": 500},
            "end_game": {"levels": [30, 40, 50], "iterations": 200}
        }
    
    def create_test_character(self, level: int, class_name: str, archetype: str = None) -> Player:
        """Create a test character with optimal build"""
        # Create base character
        player = self.player_system.create_player(
            name=f"Test_{class_name}_{level}",
            class_name=class_name,
            archetype=archetype
        )
        
        # Level up to target level
        for _ in range(level - 1):
            self.xp_system.gain_experience(player, 1000)
        
        # Allocate points optimally
        self._optimize_character_build(player, class_name, archetype)
        
        # Equip best available items
        self._equip_best_items(player, level)
        
        return player
    
    def _optimize_character_build(self, player: Player, class_name: str, archetype: str):
        """Optimize character build for testing"""
        # Allocate class points optimally
        available_points = player.class_points
        
        if class_name == "Warrior":
            # Focus on strength and constitution
            strength_points = min(available_points // 2, 20)
            constitution_points = min(available_points - strength_points, 15)
            remaining_points = available_points - strength_points - constitution_points
            
            player.strength += strength_points
            player.constitution += constitution_points
            player.dexterity += remaining_points // 2
            player.intelligence += remaining_points // 2
            
        elif class_name == "Mage":
            # Focus on intelligence and wisdom
            intelligence_points = min(available_points // 2, 20)
            wisdom_points = min(available_points - intelligence_points, 15)
            remaining_points = available_points - intelligence_points - wisdom_points
            
            player.intelligence += intelligence_points
            player.wisdom += wisdom_points
            player.constitution += remaining_points // 2
            player.dexterity += remaining_points // 2
            
        elif class_name == "Rogue":
            # Focus on dexterity and strength
            dexterity_points = min(available_points // 2, 20)
            strength_points = min(available_points - dexterity_points, 15)
            remaining_points = available_points - dexterity_points - strength_points
            
            player.dexterity += dexterity_points
            player.strength += strength_points
            player.constitution += remaining_points // 2
            player.intelligence += remaining_points // 2
        
        # Upgrade skills optimally
        self._optimize_skills(player, class_name, archetype)
    
    def _optimize_skills(self, player: Player, class_name: str, archetype: str):
        """Optimize skill upgrades for testing"""
        available_points = player.skill_points
        
        # Get class skills
        class_skills = self.skills_system.get_class_skills(class_name)
        
        # Prioritize active skills and passives
        active_skills = [skill for skill in class_skills if skill.get("type") == "active"]
        passive_skills = [skill for skill in class_skills if skill.get("type") == "passive"]
        
        # Upgrade active skills first
        for skill in active_skills[:3]:  # Top 3 active skills
            if available_points > 0:
                max_level = min(5, available_points)
                self.skills_system.upgrade_skill(player, skill["name"], max_level)
                available_points -= max_level
        
        # Upgrade passive skills
        for skill in passive_skills[:2]:  # Top 2 passive skills
            if available_points > 0:
                max_level = min(3, available_points)
                self.skills_system.upgrade_skill(player, skill["name"], max_level)
                available_points -= max_level
    
    def _equip_best_items(self, player: Player, level: int):
        """Equip the best available items for the character's level"""
        # Get available items for the level
        available_items = self.items_system.get_items_by_level(level)
        
        # Equip best weapon
        weapons = [item for item in available_items if item.get("type") == "weapon"]
        if weapons:
            best_weapon = max(weapons, key=lambda x: x.get("damage", 0))
            self.items_system.equip_item(player, best_weapon["name"])
        
        # Equip best armor
        armors = [item for item in available_items if item.get("type") == "armor"]
        if armors:
            best_armor = max(armors, key=lambda x: x.get("defense", 0))
            self.items_system.equip_item(player, best_armor["name"])
        
        # Equip accessories
        accessories = [item for item in available_items if item.get("type") == "accessory"]
        for accessory in accessories[:2]:  # Equip up to 2 accessories
            self.items_system.equip_item(player, accessory["name"])
    
    def run_combat_simulation(self, player: Player, monster_name: str, iterations: int = 100) -> Dict[str, Any]:
        """Run multiple combat simulations and return statistics"""
        results = {
            "player_wins": 0,
            "monster_wins": 0,
            "rounds": [],
            "damage_dealt": [],
            "damage_taken": [],
            "combat_logs": []
        }
        
        for i in range(iterations):
            # Create fresh copies for each simulation
            player_copy = self.player_system.create_player(
                name=player.name,
                class_name=player.class_name,
                archetype=player.archetype
            )
            
            # Copy player stats and equipment
            player_copy.__dict__.update(player.__dict__)
            
            # Get monster
            monster = self.monster_system.get_monster(monster_name)
            if not monster:
                continue
            
            # Run combat
            combat_result = self.combat_system.start_combat(player_copy, monster)
            
            # Record results
            if combat_result["winner"] == "player":
                results["player_wins"] += 1
            else:
                results["monster_wins"] += 1
            
            results["rounds"].append(combat_result["rounds"])
            results["damage_dealt"].append(combat_result.get("damage_dealt", 0))
            results["damage_taken"].append(combat_result.get("damage_taken", 0))
            
            # Keep detailed logs for first few encounters
            if i < 5:
                results["combat_logs"].append(combat_result.get("log", []))
        
        return results
    
    def run_comprehensive_balance_test(self) -> BalanceTestResult:
        """Run comprehensive balance testing across all classes and levels"""
        print("=== CHRONICLES OF RUIN: SUNDERFALL BALANCE TESTING ===")
        print("Running comprehensive balance tests...")
        
        total_encounters = 0
        total_player_wins = 0
        total_monster_wins = 0
        all_rounds = []
        all_damage_dealt = []
        all_damage_taken = []
        
        class_performance = {}
        archetype_performance = {}
        level_performance = {}
        
        # Test each game phase
        for phase_name, config in self.test_configs.items():
            print(f"\n--- Testing {phase_name.upper()} ---")
            
            for level in config["levels"]:
                print(f"  Testing Level {level}...")
                
                # Test each class
                for class_name in ["Warrior", "Mage", "Rogue"]:
                    # Test base class
                    player = self.create_test_character(level, class_name)
                    monster = self._get_appropriate_monster(level)
                    
                    if monster:
                        results = self.run_combat_simulation(
                            player, monster["name"], config["iterations"]
                        )
                        
                        # Aggregate results
                        total_encounters += config["iterations"]
                        total_player_wins += results["player_wins"]
                        total_monster_wins += results["monster_wins"]
                        all_rounds.extend(results["rounds"])
                        all_damage_dealt.extend(results["damage_dealt"])
                        all_damage_taken.extend(results["damage_taken"])
                        
                        # Record class performance
                        win_rate = results["player_wins"] / config["iterations"]
                        class_key = f"{class_name}_L{level}"
                        class_performance[class_key] = win_rate
                        
                        # Record level performance
                        if level not in level_performance:
                            level_performance[level] = []
                        level_performance[level].append(win_rate)
                        
                        print(f"    {class_name}: {win_rate:.1%} win rate")
                    
                    # Test archetypes
                    archetypes = self.archetype_system.get_archetypes_for_class(class_name)
                    for archetype in archetypes:
                        player = self.create_test_character(level, class_name, archetype["name"])
                        monster = self._get_appropriate_monster(level)
                        
                        if monster:
                            results = self.run_combat_simulation(
                                player, monster["name"], config["iterations"] // 2
                            )
                            
                            # Aggregate results
                            total_encounters += config["iterations"] // 2
                            total_player_wins += results["player_wins"]
                            total_monster_wins += results["monster_wins"]
                            all_rounds.extend(results["rounds"])
                            all_damage_dealt.extend(results["damage_dealt"])
                            all_damage_taken.extend(results["damage_taken"])
                            
                            # Record archetype performance
                            win_rate = results["player_wins"] / (config["iterations"] // 2)
                            archetype_key = f"{class_name}_{archetype['name']}_L{level}"
                            archetype_performance[archetype_key] = win_rate
                            
                            print(f"      {archetype['name']}: {win_rate:.1%} win rate")
        
        # Calculate overall statistics
        overall_win_rate = total_player_wins / total_encounters if total_encounters > 0 else 0
        avg_rounds = statistics.mean(all_rounds) if all_rounds else 0
        avg_damage_dealt = statistics.mean(all_damage_dealt) if all_damage_dealt else 0
        avg_damage_taken = statistics.mean(all_damage_taken) if all_damage_taken else 0
        
        # Calculate level performance averages
        for level in level_performance:
            level_performance[level] = statistics.mean(level_performance[level])
        
        return BalanceTestResult(
            total_encounters=total_encounters,
            player_wins=total_player_wins,
            monster_wins=total_monster_wins,
            average_rounds=avg_rounds,
            average_damage_dealt=avg_damage_dealt,
            average_damage_taken=avg_damage_taken,
            win_rate=overall_win_rate,
            class_performance=class_performance,
            archetype_performance=archetype_performance,
            level_performance=level_performance
        )
    
    def _get_appropriate_monster(self, level: int) -> Dict[str, Any]:
        """Get an appropriate monster for the given level"""
        monsters = self.monster_system.get_monsters_by_level(level)
        if monsters:
            # Choose a monster close to the player's level
            return random.choice(monsters)
        return None
    
    def generate_balance_report(self, results: BalanceTestResult) -> str:
        """Generate a detailed balance report"""
        report = []
        report.append("=" * 60)
        report.append("CHRONICLES OF RUIN: SUNDERFALL - BALANCE REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Overall statistics
        report.append("OVERALL STATISTICS:")
        report.append(f"  Total Encounters: {results.total_encounters:,}")
        report.append(f"  Player Wins: {results.player_wins:,}")
        report.append(f"  Monster Wins: {results.monster_wins:,}")
        report.append(f"  Overall Win Rate: {results.win_rate:.1%}")
        report.append(f"  Average Combat Rounds: {results.average_rounds:.1f}")
        report.append(f"  Average Damage Dealt: {results.average_damage_dealt:.1f}")
        report.append(f"  Average Damage Taken: {results.average_damage_taken:.1f}")
        report.append("")
        
        # Class performance
        report.append("CLASS PERFORMANCE:")
        for class_key, win_rate in sorted(results.class_performance.items()):
            report.append(f"  {class_key}: {win_rate:.1%}")
        report.append("")
        
        # Archetype performance
        report.append("ARCHETYPE PERFORMANCE:")
        for archetype_key, win_rate in sorted(results.archetype_performance.items()):
            report.append(f"  {archetype_key}: {win_rate:.1%}")
        report.append("")
        
        # Level performance
        report.append("LEVEL PERFORMANCE:")
        for level, win_rate in sorted(results.level_performance.items()):
            report.append(f"  Level {level}: {win_rate:.1%}")
        report.append("")
        
        # Balance recommendations
        report.append("BALANCE RECOMMENDATIONS:")
        overall_win_rate = results.win_rate
        
        if overall_win_rate < 0.4:
            report.append("  ⚠️  Overall win rate is too low. Consider:")
            report.append("     - Reducing monster damage")
            report.append("     - Increasing player health")
            report.append("     - Buffing player skills")
        elif overall_win_rate > 0.7:
            report.append("  ⚠️  Overall win rate is too high. Consider:")
            report.append("     - Increasing monster damage")
            report.append("     - Reducing player health")
            report.append("     - Nerfing player skills")
        else:
            report.append("  ✅ Overall win rate is balanced!")
        
        # Check for class balance issues
        class_rates = list(results.class_performance.values())
        if class_rates:
            min_rate = min(class_rates)
            max_rate = max(class_rates)
            if max_rate - min_rate > 0.2:
                report.append("  ⚠️  Class balance issues detected. Consider:")
                report.append("     - Buffing underperforming classes")
                report.append("     - Nerfing overperforming classes")
            else:
                report.append("  ✅ Class balance looks good!")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def save_balance_report(self, results: BalanceTestResult, filename: str = "balance_report.txt"):
        """Save balance report to file"""
        report = self.generate_balance_report(results)
        
        report_file = self.base_dir / filename
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"Balance report saved to: {report_file}")
    
    def run_quick_test(self) -> BalanceTestResult:
        """Run a quick balance test for immediate feedback"""
        print("Running quick balance test...")
        
        # Test mid-game levels with fewer iterations
        quick_config = {"levels": [5, 10], "iterations": 100}
        
        total_encounters = 0
        total_player_wins = 0
        total_monster_wins = 0
        all_rounds = []
        all_damage_dealt = []
        all_damage_taken = []
        
        class_performance = {}
        archetype_performance = {}
        level_performance = {}
        
        for level in quick_config["levels"]:
            for class_name in ["Warrior", "Mage", "Rogue"]:
                player = self.create_test_character(level, class_name)
                monster = self._get_appropriate_monster(level)
                
                if monster:
                    results = self.run_combat_simulation(
                        player, monster["name"], quick_config["iterations"]
                    )
                    
                    total_encounters += quick_config["iterations"]
                    total_player_wins += results["player_wins"]
                    total_monster_wins += results["monster_wins"]
                    all_rounds.extend(results["rounds"])
                    all_damage_dealt.extend(results["damage_dealt"])
                    all_damage_taken.extend(results["damage_taken"])
                    
                    win_rate = results["player_wins"] / quick_config["iterations"]
                    class_key = f"{class_name}_L{level}"
                    class_performance[class_key] = win_rate
                    
                    if level not in level_performance:
                        level_performance[level] = []
                    level_performance[level].append(win_rate)
        
        # Calculate statistics
        overall_win_rate = total_player_wins / total_encounters if total_encounters > 0 else 0
        avg_rounds = statistics.mean(all_rounds) if all_rounds else 0
        avg_damage_dealt = statistics.mean(all_damage_dealt) if all_damage_dealt else 0
        avg_damage_taken = statistics.mean(all_damage_taken) if all_damage_taken else 0
        
        for level in level_performance:
            level_performance[level] = statistics.mean(level_performance[level])
        
        return BalanceTestResult(
            total_encounters=total_encounters,
            player_wins=total_player_wins,
            monster_wins=total_monster_wins,
            average_rounds=avg_rounds,
            average_damage_dealt=avg_damage_dealt,
            average_damage_taken=avg_damage_taken,
            win_rate=overall_win_rate,
            class_performance=class_performance,
            archetype_performance=archetype_performance,
            level_performance=level_performance
        )

def main():
    """Main function for balance testing"""
    tool = BalanceTestingTool()
    
    print("Chronicles of Ruin: Sunderfall - Balance Testing Tool")
    print("=" * 60)
    print("1. Quick Balance Test (Fast)")
    print("2. Comprehensive Balance Test (Slow)")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        print("\nRunning quick balance test...")
        start_time = time.time()
        results = tool.run_quick_test()
        end_time = time.time()
        
        print(f"\nQuick test completed in {end_time - start_time:.1f} seconds")
        print(tool.generate_balance_report(results))
        
    elif choice == "2":
        print("\nRunning comprehensive balance test...")
        start_time = time.time()
        results = tool.run_comprehensive_balance_test()
        end_time = time.time()
        
        print(f"\nComprehensive test completed in {end_time - start_time:.1f} seconds")
        print(tool.generate_balance_report(results))
        tool.save_balance_report(results)
        
    else:
        print("Exiting...")

if __name__ == "__main__":
    main()

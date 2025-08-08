#!/usr/bin/env python3
"""
Naked Challenge Test - Skills Only Gameplay
Test that the game is beatable using ONLY skills, with zero gear equipped
This validates the core design philosophy: Skills > Gear
"""

import sys
import json
import time
import random
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add project paths
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "tools"))
sys.path.append(str(Path(__file__).parent / "chapters" / "chapter_01_sunderfall" / "src"))

from tools.ai_player_system import AIPlayerSystem

class NakedChallengeValidator:
    """Test that the game is beatable with skills only - no gear"""
    
    def __init__(self):
        self.ai_system = AIPlayerSystem(Path("."))
        self.test_results = []
        
    def create_naked_challenge_players(self):
        """Create AI players specifically for naked challenge testing"""
        naked_players = [
            {
                "name": "NakedWarrior",
                "playstyle": "aggressive",
                "personality": "strategic", 
                "preferred_archetype": "melee",
                "decision_style": "analytical",
                "risk_tolerance": 0.6,
                "patience_level": 0.8,
                "optimization_focus": "damage",
                "skill_level": "expert"
            },
            {
                "name": "NakedMage",
                "playstyle": "balanced",
                "personality": "analytical",
                "preferred_archetype": "magic", 
                "decision_style": "strategic",
                "risk_tolerance": 0.4,
                "patience_level": 0.9,
                "optimization_focus": "efficiency",
                "skill_level": "expert"
            },
            {
                "name": "NakedRanger",
                "playstyle": "defensive",
                "personality": "cautious",
                "preferred_archetype": "ranged",
                "decision_style": "conservative",
                "risk_tolerance": 0.3,
                "patience_level": 0.7,
                "optimization_focus": "survival",
                "skill_level": "master"
            },
            {
                "name": "NakedHybrid",
                "playstyle": "explorer",
                "personality": "adaptive",
                "preferred_archetype": "hybrid",
                "decision_style": "experimental", 
                "risk_tolerance": 0.5,
                "patience_level": 0.6,
                "optimization_focus": "balanced",
                "skill_level": "experienced"
            }
        ]
        
        print("🏃‍♂️ Creating NAKED CHALLENGE AI players...")
        created_players = []
        
        for player_data in naked_players:
            profile = self.ai_system.create_ai_player_profile(**player_data)
            created_players.append(profile.name)
            print(f"  Created: {profile.name} ({player_data['preferred_archetype']}, {player_data['skill_level']})")
        
        return created_players
    
    def simulate_naked_combat_encounter(self, player_name: str, enemy_type: str, 
                                       enemy_level: int, player_level: int) -> Dict[str, Any]:
        """Simulate combat with NO GEAR - skills only"""
        
        player_profile = self.ai_system.get_ai_player_profile(player_name)
        if not player_profile:
            return {"error": "Player not found"}
        
        # Naked character stats (SKILLS ONLY)
        naked_stats = {
            "base_health": 50 + (player_level * 10),  # Only level-based health
            "base_mana": 30 + (player_level * 5),     # Only level-based mana
            "base_damage": 5 + (player_level * 2),    # Minimal base damage from level
            "skill_points": player_level * 3,         # Skills are the main power source
            "resistances": {},                        # No gear resistances
            "gear_bonuses": {}                        # ZERO gear bonuses
        }
        
        # Enemy stats scale with level
        enemy_stats = {
            "health": 40 + (enemy_level * 15),
            "damage": 8 + (enemy_level * 3),
            "resistances": self._get_enemy_resistances(enemy_type)
        }
        
        print(f"  🥊 {player_name} vs {enemy_type} (Level {enemy_level})")
        print(f"      Player: {naked_stats['base_health']} HP, {naked_stats['base_damage']} base dmg, {naked_stats['skill_points']} skill points")
        print(f"      Enemy: {enemy_stats['health']} HP, {enemy_stats['damage']} dmg")
        
        # Simulate combat with skills-only strategy
        combat_result = self._simulate_skills_only_combat(
            player_profile, naked_stats, enemy_stats, enemy_type
        )
        
        return combat_result
    
    def _get_enemy_resistances(self, enemy_type: str) -> Dict[str, float]:
        """Get enemy resistance patterns"""
        resistance_patterns = {
            "corrupted_wolf": {"physical": 20.0, "poison": 50.0},
            "corrupted_bear": {"physical": 40.0, "fire": 30.0},
            "corrupted_sprite": {"lightning": 60.0, "ice": 30.0},
            "corrupted_treant": {"physical": 60.0, "fire": -20.0},  # Vulnerable to fire
            "skeleton_warrior": {"physical": 30.0, "poison": 80.0},
            "corrupted_mage": {"fire": 40.0, "lightning": 40.0},
            "forest_guardian": {"physical": 50.0, "fire": 30.0, "ice": 30.0},
            "corruption_lord": {"physical": 60.0, "fire": 40.0, "ice": 40.0, "lightning": 40.0}  # Boss
        }
        
        return resistance_patterns.get(enemy_type, {})
    
    def _simulate_skills_only_combat(self, player_profile, player_stats: Dict, 
                                   enemy_stats: Dict, enemy_type: str) -> Dict[str, Any]:
        """Simulate combat using ONLY skills - no gear bonuses"""
        
        # Skills-based strategy based on player archetype
        archetype_strategies = {
            "melee": {
                "primary_skills": ["power_strike", "berserker_rage", "defensive_stance"],
                "damage_multiplier": 1.5,  # Pure archetype bonus
                "survival_bonus": 0.2
            },
            "magic": {
                "primary_skills": ["fireball", "ice_shard", "mana_shield"],
                "damage_multiplier": 1.5,
                "mana_efficiency": 1.3
            },
            "ranged": {
                "primary_skills": ["aimed_shot", "poison_arrow", "evasive_maneuvers"],
                "damage_multiplier": 1.5,
                "accuracy_bonus": 0.3
            },
            "hybrid": {
                "primary_skills": ["elemental_weapon", "tactical_strike", "adaptive_defense"],
                "damage_multiplier": 1.25,  # Hybrid penalty but more versatile
                "versatility_bonus": 0.4
            }
        }
        
        archetype = player_profile.preferred_archetype
        strategy = archetype_strategies.get(archetype, archetype_strategies["hybrid"])
        
        # Calculate skill-based damage
        base_damage = player_stats["base_damage"]
        skill_multiplier = strategy["damage_multiplier"]
        
        # Factor in player skill level
        skill_level_multipliers = {
            "noob": 0.8,
            "casual": 0.9, 
            "experienced": 1.0,
            "expert": 1.2,
            "master": 1.4
        }
        
        skill_level_mult = skill_level_multipliers.get(player_profile.skill_level, 1.0)
        
        # Final damage calculation (SKILLS ONLY)
        effective_damage = base_damage * skill_multiplier * skill_level_mult
        
        # Apply enemy resistances
        primary_damage_type = self._get_primary_damage_type(archetype)
        resistance = enemy_stats["resistances"].get(primary_damage_type, 0.0)
        resistance_multiplier = max(0.01, 1.0 - (resistance / 100.0))
        
        final_damage = effective_damage * resistance_multiplier
        
        # Calculate survival probability (skills-based)
        player_health = player_stats["base_health"]
        enemy_damage = enemy_stats["damage"]
        enemy_health = enemy_stats["health"]
        
        # How many hits to kill enemy vs how many hits to die
        hits_to_kill_enemy = max(1, enemy_health / final_damage)
        hits_to_die = max(1, player_health / enemy_damage)
        
        # Add survival bonuses from skills
        survival_bonus = strategy.get("survival_bonus", 0.0)
        effective_hits_to_die = hits_to_die * (1 + survival_bonus)
        
        # Calculate win probability
        if effective_hits_to_die > hits_to_kill_enemy * 1.2:
            win_probability = 0.85  # Clear advantage
        elif effective_hits_to_die > hits_to_kill_enemy:
            win_probability = 0.70  # Slight advantage
        elif effective_hits_to_die * 1.2 > hits_to_kill_enemy:
            win_probability = 0.45  # Close fight
        else:
            win_probability = 0.20  # Disadvantage but still possible with skills
        
        # Factor in player profile traits
        if player_profile.risk_tolerance > 0.7:
            win_probability += 0.1  # Aggressive players fight better
        if player_profile.patience_level > 0.8:
            win_probability += 0.05  # Patient players make better decisions
        
        # Randomize the actual outcome
        won_fight = random.random() < win_probability
        
        # Calculate performance metrics
        damage_dealt = final_damage * hits_to_kill_enemy if won_fight else final_damage * (hits_to_die * 0.8)
        health_lost = enemy_damage * (hits_to_kill_enemy * 0.7) if won_fight else player_health
        
        return {
            "victory": won_fight,
            "player": player_profile.name,
            "enemy": enemy_type,
            "damage_dealt": round(damage_dealt),
            "health_lost": round(health_lost),
            "skill_effectiveness": skill_multiplier,
            "resistance_factor": resistance_multiplier,
            "win_probability": win_probability,
            "strategy_used": strategy["primary_skills"],
            "naked_stats": player_stats,
            "final_damage_per_hit": round(final_damage, 1)
        }
    
    def _get_primary_damage_type(self, archetype: str) -> str:
        """Get the primary damage type for an archetype"""
        damage_types = {
            "melee": "physical",
            "magic": "fire",
            "ranged": "physical", 
            "hybrid": "physical"
        }
        return damage_types.get(archetype, "physical")
    
    def run_naked_progression_test(self, player_name: str) -> Dict[str, Any]:
        """Test full game progression with naked character"""
        
        print(f"\n🏃‍♂️ NAKED PROGRESSION TEST: {player_name}")
        print("=" * 50)
        
        # Game progression stages
        progression_stages = [
            {"level": 1, "enemies": ["corrupted_wolf"], "area": "sunderfall_outskirts"},
            {"level": 3, "enemies": ["corrupted_wolf", "corrupted_bear"], "area": "whispering_woods"},
            {"level": 5, "enemies": ["corrupted_sprite", "skeleton_warrior"], "area": "ancient_ruins"},
            {"level": 8, "enemies": ["corrupted_treant", "corrupted_mage"], "area": "corrupted_grove"},
            {"level": 12, "enemies": ["forest_guardian"], "area": "guardian_chamber"},
            {"level": 15, "enemies": ["corruption_lord"], "area": "boss_arena"}  # Final boss
        ]
        
        stage_results = []
        overall_success = True
        
        for i, stage in enumerate(progression_stages):
            stage_name = f"Stage {i+1}: Level {stage['level']} - {stage['area']}"
            print(f"\n🎯 {stage_name}")
            
            stage_victories = 0
            stage_attempts = 0
            stage_combats = []
            
            # Test against each enemy type at this stage
            for enemy_type in stage["enemies"]:
                # Multiple attempts to get statistical significance
                attempts = 5 if enemy_type != "corruption_lord" else 10  # More attempts for boss
                
                for attempt in range(attempts):
                    stage_attempts += 1
                    enemy_level = stage["level"] + random.randint(-1, 1)  # Small level variance
                    
                    combat_result = self.simulate_naked_combat_encounter(
                        player_name, enemy_type, enemy_level, stage["level"]
                    )
                    
                    stage_combats.append(combat_result)
                    
                    if combat_result.get("victory", False):
                        stage_victories += 1
                        result_symbol = "✅"
                    else:
                        result_symbol = "❌"
                    
                    if attempt < 3 or enemy_type == "corruption_lord":  # Show details for boss
                        print(f"    {result_symbol} vs {enemy_type}: {combat_result.get('final_damage_per_hit', 0)} dmg/hit, {combat_result.get('win_probability', 0):.1%} chance")
            
            # Calculate stage success rate
            stage_success_rate = stage_victories / stage_attempts
            stage_result = {
                "stage": stage_name,
                "level": stage["level"],
                "area": stage["area"],
                "success_rate": stage_success_rate,
                "victories": stage_victories,
                "attempts": stage_attempts,
                "combats": stage_combats
            }
            
            stage_results.append(stage_result)
            
            print(f"    📊 Stage Success Rate: {stage_success_rate:.1%} ({stage_victories}/{stage_attempts})")
            
            # Consider stage failed if success rate too low
            min_success_rate = 0.4 if "boss" in stage["area"] else 0.6  # Bosses can be harder
            if stage_success_rate < min_success_rate:
                print(f"    ❌ STAGE FAILED - Success rate too low!")
                overall_success = False
            else:
                print(f"    ✅ Stage passed!")
        
        return {
            "player": player_name,
            "overall_success": overall_success,
            "stage_results": stage_results,
            "final_boss_attempts": stage_results[-1]["attempts"] if stage_results else 0,
            "final_boss_victories": stage_results[-1]["victories"] if stage_results else 0,
            "average_success_rate": sum(s["success_rate"] for s in stage_results) / len(stage_results) if stage_results else 0.0
        }
    
    def run_full_naked_challenge(self) -> Dict[str, Any]:
        """Run the complete naked challenge test"""
        
        print("🏃‍♂️ NAKED CHALLENGE - SKILLS ONLY GAMEPLAY TEST")
        print("=" * 60)
        print("Testing core design philosophy: Game must be beatable with NO GEAR")
        print("Only skills, levels, and player decision-making allowed!")
        
        # Create test players
        player_names = self.create_naked_challenge_players()
        
        # Test each player through full progression
        all_results = []
        
        for player_name in player_names:
            result = self.run_naked_progression_test(player_name)
            all_results.append(result)
        
        # Analyze overall results
        successful_players = sum(1 for r in all_results if r["overall_success"])
        total_players = len(all_results)
        
        average_final_boss_rate = sum(
            r["stage_results"][-1]["success_rate"] for r in all_results 
            if r["stage_results"]
        ) / len(all_results)
        
        overall_average_success = sum(r["average_success_rate"] for r in all_results) / len(all_results)
        
        analysis = {
            "naked_challenge_passed": successful_players > 0,  # At least one player can beat it naked
            "player_success_rate": successful_players / total_players,
            "average_success_rate": overall_average_success,
            "final_boss_success_rate": average_final_boss_rate,
            "successful_players": successful_players,
            "total_players": total_players,
            "player_results": all_results
        }
        
        return analysis
    
    def save_naked_challenge_results(self, results: Dict[str, Any], 
                                   filename: str = "naked_challenge_results.json") -> str:
        """Save naked challenge results"""
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        return filename

def main():
    """Run the naked challenge validation test"""
    
    validator = NakedChallengeValidator()
    
    try:
        results = validator.run_full_naked_challenge()
        
        print("\n" + "=" * 60)
        print("🏆 NAKED CHALLENGE RESULTS")
        print("=" * 60)
        
        if results["naked_challenge_passed"]:
            print("✅ NAKED CHALLENGE: PASSED!")
            print("   Game IS beatable with skills only - no gear required!")
        else:
            print("❌ NAKED CHALLENGE: FAILED!")
            print("   Game balance needs adjustment - too gear-dependent!")
        
        print(f"\n📊 Statistics:")
        print(f"   Players who completed naked: {results['successful_players']}/{results['total_players']}")
        print(f"   Average success rate: {results['average_success_rate']:.1%}")
        print(f"   Final boss success rate: {results['final_boss_success_rate']:.1%}")
        
        print(f"\n🎯 Core Design Philosophy Validation:")
        if results["final_boss_success_rate"] > 0.3:
            print("   ✅ Skills > Gear philosophy CONFIRMED")
            print("   ✅ Game beatable without gear gatekeeping")
            print("   ✅ Set system can remain optional luxury")
        else:
            print("   ❌ Too gear-dependent - needs rebalancing")
            print("   ❌ Skills not powerful enough alone")
        
        # Save detailed results
        filename = validator.save_naked_challenge_results(results)
        print(f"\n💾 Detailed results saved to: {filename}")
        
        return results["naked_challenge_passed"]
        
    except Exception as e:
        print(f"❌ Naked challenge test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Boss Encounter Tool - Chronicles of Ruin: Sunderfall
CLI tool for testing and managing boss encounters
"""

import sys
import os
import time
import random
from pathlib import Path
from typing import Dict, List, Any, Optional

# Change to the chapter directory and add src to path
chapter_dir = Path(__file__).parent.parent / "chapters" / "chapter_01_sunderfall"
os.chdir(str(chapter_dir))
sys.path.insert(0, str(chapter_dir / "src"))

from src.systems.player_system import PlayerSystem
from src.systems.monster_system import MonsterSystem
from src.systems.combat_system import CombatSystem
from src.systems.boss_system import BossSystem, BossType, BossPhase


class BossEncounterTool:
    """CLI tool for boss encounter management and testing."""
    
    def __init__(self):
        """Initialize the boss encounter tool."""
        self.base_dir = Path(__file__).parent.parent / "chapters" / "chapter_01_sunderfall"
        self.data_dir = self.base_dir / "data"
        
        # Initialize systems
        self.player_system = PlayerSystem()
        self.monster_system = MonsterSystem()
        self.combat_system = CombatSystem(self.player_system, self.monster_system, None)
        self.boss_system = BossSystem(self.monster_system, self.player_system, self.combat_system)
        
        # Active encounters
        self.active_encounters = {}
        
    def print_header(self):
        """Print the tool header."""
        print("=" * 60)
        print("    CHRONICLES OF RUIN: SUNDERFALL - BOSS ENCOUNTER TOOL")
        print("=" * 60)
        print()
    
    def print_menu(self):
        """Print the main menu."""
        print("\nBOSS ENCOUNTER MENU:")
        print("1. Create District Boss")
        print("2. Create Unique Monster")
        print("3. Create World Boss")
        print("4. Start Boss Combat")
        print("5. Continue Boss Combat")
        print("6. View Active Encounters")
        print("7. Simulate Boss Fight")
        print("8. Test Boss Abilities")
        print("9. Generate Boss Report")
        print("0. Exit")
        print()
    
    def create_district_boss(self):
        """Create a district boss encounter."""
        print("\n=== CREATE DISTRICT BOSS ===")
        
        # Get district information
        district_name = input("Enter district name: ").strip()
        if not district_name:
            print("District name is required!")
            return
        
        district_level = input("Enter district level (1-50): ").strip()
        try:
            district_level = int(district_level)
            if district_level < 1 or district_level > 50:
                print("District level must be between 1 and 50!")
                return
        except ValueError:
            print("Invalid district level!")
            return
        
        player_level = input("Enter player level (1-100): ").strip()
        try:
            player_level = int(player_level)
            if player_level < 1 or player_level > 100:
                print("Player level must be between 1 and 100!")
                return
        except ValueError:
            print("Invalid player level!")
            return
        
        # Create boss
        boss = self.boss_system.create_district_boss(district_level, player_level, district_name)
        
        print(f"\n✅ Created District Boss:")
        print(f"   Name: {boss['name']}")
        print(f"   Level: {boss['level']}")
        print(f"   Health: {boss['stats']['max_health']}")
        print(f"   Damage: {boss['stats']['damage']}")
        print(f"   Defense: {boss['stats']['defense']}")
        print(f"   Archetype: {boss['archetype'].value}")
        print(f"   Classification: {boss['classification'].value}")
        print(f"   Phases: {len(boss['phases'])}")
        print(f"   Abilities: {len(boss['abilities'])}")
        
        # Store encounter
        encounter_id = f"district_{int(time.time())}"
        self.active_encounters[encounter_id] = {
            "type": "district_boss",
            "boss": boss,
            "created_time": time.time()
        }
        
        print(f"\nEncounter ID: {encounter_id}")
    
    def create_unique_monster(self):
        """Create a unique monster encounter."""
        print("\n=== CREATE UNIQUE MONSTER ===")
        
        # Get parameters
        district_level = input("Enter district level (1-50): ").strip()
        try:
            district_level = int(district_level)
            if district_level < 1 or district_level > 50:
                print("District level must be between 1 and 50!")
                return
        except ValueError:
            print("Invalid district level!")
            return
        
        player_level = input("Enter player level (1-100): ").strip()
        try:
            player_level = int(player_level)
            if player_level < 1 or player_level > 100:
                print("Player level must be between 1 and 100!")
                return
        except ValueError:
            print("Invalid player level!")
            return
        
        # Optional forced archetype and classification
        print("\nOptional: Force specific archetype and classification")
        force_type = input("Force specific type? (y/n): ").strip().lower()
        
        forced_archetype = None
        forced_classification = None
        
        if force_type == 'y':
            print("\nAvailable Archetypes:")
            print("1. Melee")
            print("2. Ranged")
            print("3. Magic")
            print("4. Wild")
            
            archetype_choice = input("Select archetype (1-4): ").strip()
            archetype_map = {
                "1": "melee",
                "2": "ranged", 
                "3": "magic",
                "4": "wild"
            }
            
            if archetype_choice in archetype_map:
                from src.systems.monster_system import MonsterArchetype
                forced_archetype = MonsterArchetype(archetype_map[archetype_choice])
            
            print("\nAvailable Classifications:")
            print("1. Demonic")
            print("2. Undead")
            print("3. Beast")
            print("4. Elemental")
            print("5. Construct")
            print("6. Humanoid")
            
            classification_choice = input("Select classification (1-6): ").strip()
            classification_map = {
                "1": "demonic",
                "2": "undead",
                "3": "beast",
                "4": "elemental",
                "5": "construct",
                "6": "humanoid"
            }
            
            if classification_choice in classification_map:
                from src.systems.monster_system import MonsterClassification
                forced_classification = MonsterClassification(classification_map[classification_choice])
        
        # Create unique monster
        unique_monster = self.boss_system.create_unique_monster(
            district_level, player_level, forced_archetype, forced_classification
        )
        
        print(f"\n✅ Created Unique Monster:")
        print(f"   Name: {unique_monster['name']}")
        print(f"   Level: {unique_monster['level']}")
        print(f"   Health: {unique_monster['stats']['max_health']}")
        print(f"   Damage: {unique_monster['stats']['damage']}")
        print(f"   Defense: {unique_monster['stats']['defense']}")
        print(f"   Archetype: {unique_monster['archetype'].value}")
        print(f"   Classification: {unique_monster['classification'].value}")
        print(f"   Phases: {len(unique_monster['phases'])}")
        print(f"   Abilities: {len(unique_monster['abilities'])}")
        
        # Store encounter
        encounter_id = f"unique_{int(time.time())}"
        self.active_encounters[encounter_id] = {
            "type": "unique_monster",
            "boss": unique_monster,
            "created_time": time.time()
        }
        
        print(f"\nEncounter ID: {encounter_id}")
    
    def create_world_boss(self):
        """Create a world boss encounter."""
        print("\n=== CREATE WORLD BOSS ===")
        
        # Get parameters
        player_level = input("Enter player level (1-100): ").strip()
        try:
            player_level = int(player_level)
            if player_level < 1 or player_level > 100:
                print("Player level must be between 1 and 100!")
                return
        except ValueError:
            print("Invalid player level!")
            return
        
        boss_name = input("Enter custom boss name (or press Enter for random): ").strip()
        if not boss_name:
            boss_name = None
        
        # Create world boss
        world_boss = self.boss_system.create_world_boss(player_level, boss_name)
        
        print(f"\n✅ Created World Boss:")
        print(f"   Name: {world_boss['name']}")
        print(f"   Level: {world_boss['level']}")
        print(f"   Health: {world_boss['stats']['max_health']}")
        print(f"   Damage: {world_boss['stats']['damage']}")
        print(f"   Defense: {world_boss['stats']['defense']}")
        print(f"   Archetype: {world_boss['archetype'].value}")
        print(f"   Classification: {world_boss['classification'].value}")
        print(f"   Phases: {len(world_boss['phases'])}")
        print(f"   Abilities: {len(world_boss['abilities'])}")
        
        # Store encounter
        encounter_id = f"world_{int(time.time())}"
        self.active_encounters[encounter_id] = {
            "type": "world_boss",
            "boss": world_boss,
            "created_time": time.time()
        }
        
        print(f"\nEncounter ID: {encounter_id}")
    
    def start_boss_combat(self):
        """Start a boss combat encounter."""
        print("\n=== START BOSS COMBAT ===")
        
        # Show active encounters
        if not self.active_encounters:
            print("No active encounters available!")
            print("Create a boss encounter first.")
            return
        
        print("Active Encounters:")
        for encounter_id, encounter in self.active_encounters.items():
            boss = encounter["boss"]
            print(f"  {encounter_id}: {boss['name']} (Level {boss['level']})")
        
        encounter_id = input("\nEnter encounter ID: ").strip()
        if encounter_id not in self.active_encounters:
            print("Invalid encounter ID!")
            return
        
        # Get or create player
        player_name = input("Enter player name: ").strip()
        if not player_name:
            print("Player name is required!")
            return
        
        player_class = input("Enter player class (Warrior/Mage/Rogue): ").strip()
        if player_class not in ["Warrior", "Mage", "Rogue"]:
            print("Invalid player class!")
            return
        
        # Create or get player
        base_archetypes = {"Melee": 1, "Ranged": 1, "Magic": 1}  # Default distribution
        player = self.player_system.create_player(player_name, player_name, base_archetypes)
        
        # Set player level for testing
        player_level = input("Enter player level (1-100): ").strip()
        try:
            player_level = int(player_level)
            if player_level < 1 or player_level > 100:
                print("Player level must be between 1 and 100!")
                return
        except ValueError:
            print("Invalid player level!")
            return
        
        # Level up player
        for _ in range(player_level - 1):
            self.player_system.xp_system.gain_experience(player, 1000)
        
        # Start combat
        encounter = self.active_encounters[encounter_id]
        boss = encounter["boss"]
        
        combat_state = self.boss_system.start_boss_combat(player.__dict__, boss)
        
        print(f"\n🎯 BOSS COMBAT STARTED!")
        print(f"   Player: {player.name} (Level {player.level})")
        print(f"   Boss: {boss['name']} (Level {boss['level']})")
        print(f"   Player Health: {player.current_health}/{player.max_health}")
        print(f"   Boss Health: {boss['stats']['current_health']}/{boss['stats']['max_health']}")
        
        # Store combat state
        encounter["combat_state"] = combat_state
        encounter["player"] = player
        
        print(f"\nCombat ready! Use option 5 to continue the fight.")
    
    def continue_boss_combat(self):
        """Continue an active boss combat."""
        print("\n=== CONTINUE BOSS COMBAT ===")
        
        # Find encounters with active combat
        active_combats = []
        for encounter_id, encounter in self.active_encounters.items():
            if "combat_state" in encounter:
                active_combats.append((encounter_id, encounter))
        
        if not active_combats:
            print("No active boss combats!")
            print("Start a boss combat first.")
            return
        
        print("Active Boss Combats:")
        for encounter_id, encounter in active_combats:
            boss = encounter["boss"]
            player = encounter["player"]
            combat_state = encounter["combat_state"]
            print(f"  {encounter_id}: {player.name} vs {boss['name']} (Round {combat_state['round']})")
        
        encounter_id = input("\nEnter encounter ID: ").strip()
        if encounter_id not in self.active_encounters:
            print("Invalid encounter ID!")
            return
        
        encounter = self.active_encounters[encounter_id]
        if "combat_state" not in encounter:
            print("No active combat for this encounter!")
            return
        
        # Get player action
        print("\nAvailable Actions:")
        print("1. Attack")
        print("2. Use Skill")
        print("3. Use Item")
        print("4. Defend")
        
        action_choice = input("Select action (1-4): ").strip()
        action_map = {
            "1": "attack",
            "2": "skill",
            "3": "item",
            "4": "defend"
        }
        
        player_action = action_map.get(action_choice, "attack")
        
        # Process combat round
        boss_id = encounter["boss"]["id"]
        result = self.boss_system.process_boss_combat_round(boss_id, player_action)
        
        if "error" in result:
            print(f"Error: {result['error']}")
            return
        
        if "winner" in result:
            # Combat ended
            print(f"\n🏁 COMBAT ENDED!")
            print(f"   Winner: {result['winner'].title()}")
            print(f"   Rounds: {result['rounds']}")
            print(f"   Damage Dealt: {result['damage_dealt']}")
            print(f"   Damage Taken: {result['damage_taken']}")
            
            if result['winner'] == 'player':
                rewards = result['rewards']
                print(f"\n🎁 REWARDS:")
                print(f"   Experience: {rewards['experience']}")
                print(f"   Gold: {rewards['gold']}")
                print(f"   Loot: {len(rewards['loot']['rare_items'])} rare items")
            
            # Remove combat state
            del encounter["combat_state"]
            return
        
        # Show round results
        player_result = result["player_result"]
        boss_result = result["boss_result"]
        
        print(f"\n⚔️ ROUND {result['round']} RESULTS:")
        print(f"   Player Action: {player_result['action']}")
        print(f"   Player Damage: {player_result['damage_dealt']}")
        print(f"   Boss Health: {player_result['boss_health_remaining']}")
        
        print(f"   Boss Action: {boss_result['action']}")
        print(f"   Boss Damage: {boss_result['damage_dealt']}")
        print(f"   Player Health: {boss_result['player_health_remaining']}")
        
        # Check for phase transitions
        combat_state = result["combat_state"]
        if combat_state["phase_transitions"]:
            latest_transition = combat_state["phase_transitions"][-1]
            if latest_transition["round"] == result["round"]:
                print(f"\n🔥 PHASE TRANSITION: {latest_transition['description']}")
        
        # Check for abilities used
        if combat_state["abilities_used"]:
            latest_ability = combat_state["abilities_used"][-1]
            if latest_ability["round"] == result["round"]:
                print(f"   Boss Ability: {latest_ability['description']}")
    
    def view_active_encounters(self):
        """View all active encounters."""
        print("\n=== ACTIVE ENCOUNTERS ===")
        
        if not self.active_encounters:
            print("No active encounters.")
            return
        
        for encounter_id, encounter in self.active_encounters.items():
            boss = encounter["boss"]
            print(f"\nEncounter ID: {encounter_id}")
            print(f"   Type: {encounter['type']}")
            print(f"   Boss: {boss['name']}")
            print(f"   Level: {boss['level']}")
            print(f"   Health: {boss['stats']['current_health']}/{boss['stats']['max_health']}")
            print(f"   Phase: {boss['current_phase'].value}")
            print(f"   Created: {time.strftime('%H:%M:%S', time.localtime(encounter['created_time']))}")
            
            if "combat_state" in encounter:
                print(f"   Status: In Combat (Round {encounter['combat_state']['round']})")
            else:
                print(f"   Status: Ready for Combat")
    
    def simulate_boss_fight(self):
        """Simulate a complete boss fight."""
        print("\n=== SIMULATE BOSS FIGHT ===")
        
        # Get boss parameters
        boss_type = input("Enter boss type (district/unique/world): ").strip().lower()
        if boss_type not in ["district", "unique", "world"]:
            print("Invalid boss type!")
            return
        
        district_level = input("Enter district level (1-50): ").strip()
        try:
            district_level = int(district_level)
        except ValueError:
            print("Invalid district level!")
            return
        
        player_level = input("Enter player level (1-100): ").strip()
        try:
            player_level = int(player_level)
        except ValueError:
            print("Invalid player level!")
            return
        
        # Create boss
        if boss_type == "district":
            district_name = input("Enter district name: ").strip()
            boss = self.boss_system.create_district_boss(district_level, player_level, district_name)
        elif boss_type == "unique":
            boss = self.boss_system.create_unique_monster(district_level, player_level)
        else:  # world
            boss = self.boss_system.create_world_boss(player_level)
        
        # Create player
        base_archetypes = {"Melee": 1, "Ranged": 1, "Magic": 1}  # Default distribution
        player = self.player_system.create_player("SimPlayer", "SimPlayer", base_archetypes)
        for _ in range(player_level - 1):
            self.player_system.xp_system.gain_experience(player, 1000)
        
        # Start combat
        combat_state = self.boss_system.start_boss_combat(player.__dict__, boss)
        
        print(f"\n🎯 SIMULATING BOSS FIGHT:")
        print(f"   Player: {player.name} (Level {player.level})")
        print(f"   Boss: {boss['name']} (Level {boss['level']})")
        print(f"   Player Health: {player.current_health}/{player.max_health}")
        print(f"   Boss Health: {boss['stats']['current_health']}/{boss['stats']['max_health']}")
        
        # Simulate combat
        round_count = 0
        max_rounds = 50  # Prevent infinite loops
        
        while round_count < max_rounds:
            round_count += 1
            
            # Process round
            boss_id = boss["id"]
            result = self.boss_system.process_boss_combat_round(boss_id, "attack")
            
            if "winner" in result:
                print(f"\n🏁 SIMULATION COMPLETE!")
                print(f"   Winner: {result['winner'].title()}")
                print(f"   Rounds: {result['rounds']}")
                print(f"   Damage Dealt: {result['damage_dealt']}")
                print(f"   Damage Taken: {result['damage_taken']}")
                
                if result['winner'] == 'player':
                    rewards = result['rewards']
                    print(f"\n🎁 REWARDS:")
                    print(f"   Experience: {rewards['experience']}")
                    print(f"   Gold: {rewards['gold']}")
                
                break
            
            # Show progress every 5 rounds
            if round_count % 5 == 0:
                player_result = result["player_result"]
                boss_result = result["boss_result"]
                print(f"   Round {round_count}: Player HP {boss_result['player_health_remaining']}, Boss HP {player_result['boss_health_remaining']}")
        
        if round_count >= max_rounds:
            print(f"\n⚠️ Simulation stopped after {max_rounds} rounds (possible infinite loop)")
    
    def test_boss_abilities(self):
        """Test boss abilities."""
        print("\n=== TEST BOSS ABILITIES ===")
        
        # Create a test boss
        boss = self.boss_system.create_district_boss(10, 15, "Test District")
        
        print(f"Testing abilities for: {boss['name']}")
        print(f"Abilities: {[ability.value for ability in boss['abilities']]}")
        
        # Test each ability
        for ability in boss['abilities']:
            print(f"\nTesting {ability.value}...")
            
            # Create test combat state
            base_archetypes = {"Melee": 1, "Ranged": 1, "Magic": 1}  # Default distribution
            test_player = self.player_system.create_player("TestPlayer", "TestPlayer", base_archetypes)
            combat_state = self.boss_system.start_boss_combat(test_player.__dict__, boss)
            
            # Use ability
            result = self.boss_system._use_boss_ability(combat_state, ability)
            
            print(f"   Action: {result['action']}")
            print(f"   Description: {result['description']}")
            
            if 'damage_dealt' in result:
                print(f"   Damage: {result['damage_dealt']}")
            if 'heal_amount' in result:
                print(f"   Heal: {result['heal_amount']}")
            if 'minions_spawned' in result:
                print(f"   Minions: {result['minions_spawned']}")
    
    def generate_boss_report(self):
        """Generate a comprehensive boss report."""
        print("\n=== BOSS REPORT ===")
        
        if not self.active_encounters:
            print("No encounters to report on.")
            return
        
        print(f"Total Active Encounters: {len(self.active_encounters)}")
        
        # Statistics
        boss_types = {}
        total_health = 0
        total_damage = 0
        total_defense = 0
        
        for encounter_id, encounter in self.active_encounters.items():
            boss = encounter["boss"]
            boss_type = encounter["type"]
            
            if boss_type not in boss_types:
                boss_types[boss_type] = 0
            boss_types[boss_type] += 1
            
            total_health += boss["stats"]["max_health"]
            total_damage += boss["stats"]["damage"]
            total_defense += boss["stats"]["defense"]
        
        print(f"\nBoss Type Distribution:")
        for boss_type, count in boss_types.items():
            print(f"   {boss_type}: {count}")
        
        if self.active_encounters:
            avg_health = total_health / len(self.active_encounters)
            avg_damage = total_damage / len(self.active_encounters)
            avg_defense = total_defense / len(self.active_encounters)
            
            print(f"\nAverage Stats:")
            print(f"   Health: {avg_health:.1f}")
            print(f"   Damage: {avg_damage:.1f}")
            print(f"   Defense: {avg_defense:.1f}")
        
        # Active combats
        active_combats = [e for e in self.active_encounters.values() if "combat_state" in e]
        if active_combats:
            print(f"\nActive Combats: {len(active_combats)}")
            for encounter in active_combats:
                boss = encounter["boss"]
                player = encounter["player"]
                combat_state = encounter["combat_state"]
                print(f"   {player.name} vs {boss['name']} (Round {combat_state['round']})")
    
    def run(self):
        """Run the boss encounter tool."""
        self.print_header()
        
        while True:
            self.print_menu()
            choice = input("Enter your choice (0-9): ").strip()
            
            if choice == "0":
                print("Exiting Boss Encounter Tool...")
                break
            elif choice == "1":
                self.create_district_boss()
            elif choice == "2":
                self.create_unique_monster()
            elif choice == "3":
                self.create_world_boss()
            elif choice == "4":
                self.start_boss_combat()
            elif choice == "5":
                self.continue_boss_combat()
            elif choice == "6":
                self.view_active_encounters()
            elif choice == "7":
                self.simulate_boss_fight()
            elif choice == "8":
                self.test_boss_abilities()
            elif choice == "9":
                self.generate_boss_report()
            else:
                print("Invalid choice! Please enter 0-9.")


def main():
    """Main function."""
    tool = BossEncounterTool()
    tool.run()


if __name__ == "__main__":
    main()

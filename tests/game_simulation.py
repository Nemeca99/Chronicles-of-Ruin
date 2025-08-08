#!/usr/bin/env python3
"""
GAME SIMULATION FOR CHRONICLES OF RUIN: SUNDERFALL
==================================================

This script simulates actual gameplay scenarios to demonstrate
the game's functionality without requiring manual input.

FEATURES:
- Automated character creation and progression
- Combat simulations with various scenarios
- Inventory management demonstrations
- Skill progression and learning
- Quest and exploration simulations
- Multiplayer feature demonstrations

USAGE:
    python game_simulation.py [--scenario SCENARIO] [--duration SECONDS]

SCENARIOS:
    new_player: Simulate a new player's first experience
    combat_focused: Focus on combat mechanics and battles
    exploration: Simulate exploration and discovery
    multiplayer: Demonstrate multiplayer features
    full_gameplay: Complete gameplay simulation
"""

import sys
import os
import time
import random
import json
from typing import Dict, Any, List, Optional
import argparse

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class GameSimulator:
    """Simulates actual gameplay scenarios"""
    
    def __init__(self):
        self.game_state = {
            'player': None,
            'location': 'Starting Village',
            'inventory': [],
            'experience': 0,
            'level': 1,
            'health': 100,
            'max_health': 100,
            'gold': 50,
            'quests': [],
            'combat_log': []
        }
        self.game_systems = {}
        self.simulation_log = []
        
    def setup_game_systems(self):
        """Initialize all game systems"""
        print("🎮 Initializing game systems...")
        
        try:
            from systems.class_system import ClassSystem
            from systems.archetype_system import ArchetypeSystem
            from systems.status_elemental_system import StatusElementalSystem
            from systems.combat_system import CombatSystem
            from systems.items_system import ItemsSystem
            from systems.player_system import PlayerSystem
            from systems.skills_system import SkillsSystem
            
            self.game_systems = {
                'class': ClassSystem(),
                'archetype': ArchetypeSystem(),
                'status': StatusElementalSystem(),
                'combat': CombatSystem(),
                'items': ItemsSystem(),
                'player': PlayerSystem(),
                'skills': SkillsSystem()
            }
            
            print("✅ Game systems initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize game systems: {e}")
            return False
    
    def create_player(self, name="SimulatedHero", character_class="Warrior"):
        """Create a simulated player character"""
        print(f"\n👤 Creating character: {name}")
        print("=" * 40)
        
        # Create player with basic stats
        self.game_state['player'] = {
            'name': name,
            'class': character_class,
            'level': 1,
            'experience': 0,
            'stats': {
                'strength': 15,
                'dexterity': 12,
                'constitution': 14,
                'intelligence': 8,
                'wisdom': 10,
                'charisma': 12
            },
            'health': 100,
            'max_health': 100,
            'equipment': {
                'weapon': 'Rusty Sword',
                'armor': 'Leather Armor',
                'accessory': None
            },
            'skills': ['Basic Attack'],
            'archetype': 'Guardian'
        }
        
        print(f"✅ Created {name} - Level {self.game_state['player']['level']} {character_class}")
        print(f"🛡️ Health: {self.game_state['player']['health']}/{self.game_state['player']['max_health']}")
        print(f"⚔️ Weapon: {self.game_state['player']['equipment']['weapon']}")
        
        self.log_event(f"Character {name} created successfully")
    
    def simulate_combat_encounter(self, enemy_type="Goblin"):
        """Simulate a combat encounter"""
        print(f"\n⚔️ Combat Encounter: {enemy_type}")
        print("=" * 35)
        
        # Create enemy
        enemy = self.create_enemy(enemy_type)
        print(f"👹 Enemy: {enemy['name']} (Level {enemy['level']})")
        print(f"🩸 Enemy Health: {enemy['health']}/{enemy['max_health']}")
        
        round_num = 1
        while enemy['health'] > 0 and self.game_state['player']['health'] > 0:
            print(f"\n🔥 Round {round_num}")
            
            # Player attacks
            damage = self.calculate_player_damage()
            enemy['health'] = max(0, enemy['health'] - damage)
            print(f"⚔️ {self.game_state['player']['name']} deals {damage} damage!")
            print(f"👹 {enemy['name']} health: {enemy['health']}/{enemy['max_health']}")
            
            if enemy['health'] <= 0:
                print(f"💀 {enemy['name']} defeated!")
                break
            
            # Enemy attacks
            enemy_damage = self.calculate_enemy_damage(enemy)
            self.game_state['player']['health'] = max(0, self.game_state['player']['health'] - enemy_damage)
            print(f"👹 {enemy['name']} deals {enemy_damage} damage!")
            print(f"👤 {self.game_state['player']['name']} health: {self.game_state['player']['health']}/{self.game_state['player']['max_health']}")
            
            if self.game_state['player']['health'] <= 0:
                print(f"💀 {self.game_state['player']['name']} has fallen!")
                break
            
            round_num += 1
            time.sleep(0.5)  # Add some delay for dramatic effect
        
        # Combat results
        if enemy['health'] <= 0:
            experience_gained = enemy['experience_reward']
            gold_gained = enemy['gold_reward']
            self.game_state['experience'] += experience_gained
            self.game_state['gold'] += gold_gained
            
            print(f"\n🎉 Victory!")
            print(f"📈 Experience gained: {experience_gained}")
            print(f"💰 Gold gained: {gold_gained}")
            
            # Check for level up
            self.check_level_up()
            
            self.log_event(f"Defeated {enemy['name']} - Gained {experience_gained} XP, {gold_gained} gold")
        else:
            print(f"\n💀 Defeat! {self.game_state['player']['name']} has fallen in battle.")
            self.log_event(f"Defeated by {enemy['name']}")
    
    def create_enemy(self, enemy_type):
        """Create an enemy for combat"""
        enemies = {
            'Goblin': {
                'name': 'Goblin',
                'level': 2,
                'health': 25,
                'max_health': 25,
                'stats': {'strength': 10, 'dexterity': 14, 'constitution': 8},
                'equipment': {'weapon': 'Rusty Dagger'},
                'experience_reward': 15,
                'gold_reward': 5
            },
            'Orc': {
                'name': 'Orc Warrior',
                'level': 4,
                'health': 45,
                'max_health': 45,
                'stats': {'strength': 16, 'dexterity': 10, 'constitution': 12},
                'equipment': {'weapon': 'Battle Axe'},
                'experience_reward': 30,
                'gold_reward': 12
            },
            'Troll': {
                'name': 'Cave Troll',
                'level': 6,
                'health': 80,
                'max_health': 80,
                'stats': {'strength': 18, 'dexterity': 8, 'constitution': 16},
                'equipment': {'weapon': 'Stone Club'},
                'experience_reward': 50,
                'gold_reward': 25
            }
        }
        
        return enemies.get(enemy_type, enemies['Goblin'])
    
    def calculate_player_damage(self):
        """Calculate player damage"""
        base_damage = self.game_state['player']['stats']['strength']
        weapon_bonus = 5  # Basic weapon damage
        critical_chance = 0.1  # 10% critical chance
        
        if random.random() < critical_chance:
            damage = (base_damage + weapon_bonus) * 2
            print("💥 Critical hit!")
        else:
            damage = base_damage + weapon_bonus
        
        return max(1, damage)
    
    def calculate_enemy_damage(self, enemy):
        """Calculate enemy damage"""
        base_damage = enemy['stats']['strength']
        weapon_bonus = 3  # Basic enemy weapon damage
        return max(1, base_damage + weapon_bonus)
    
    def check_level_up(self):
        """Check if player should level up"""
        experience_needed = self.game_state['player']['level'] * 100
        
        if self.game_state['experience'] >= experience_needed:
            self.game_state['player']['level'] += 1
            self.game_state['player']['max_health'] += 10
            self.game_state['player']['health'] = self.game_state['player']['max_health']
            
            # Increase stats
            for stat in self.game_state['player']['stats']:
                self.game_state['player']['stats'][stat] += 1
            
            print(f"\n🌟 LEVEL UP! {self.game_state['player']['name']} is now level {self.game_state['player']['level']}!")
            print(f"🩸 Health increased to {self.game_state['player']['max_health']}")
            print(f"📊 All stats increased!")
            
            self.log_event(f"Leveled up to {self.game_state['player']['level']}")
    
    def simulate_exploration(self):
        """Simulate exploration and discovery"""
        print(f"\n🗺️ Exploring {self.game_state['location']}")
        print("=" * 35)
        
        # Random exploration events
        events = [
            "You discover an ancient ruin...",
            "A mysterious cave entrance appears...",
            "You find a hidden treasure chest!",
            "A friendly merchant approaches...",
            "You encounter a wandering spirit...",
            "A magical portal shimmers in the distance..."
        ]
        
        event = random.choice(events)
        print(f"🔍 {event}")
        
        # Random outcomes
        outcomes = [
            ("You find some gold!", 10),
            ("You discover a healing potion!", 0),
            ("You gain experience from your exploration!", 5),
            ("You find nothing of interest.", 0),
            ("You discover a rare gem!", 25)
        ]
        
        outcome, reward = random.choice(outcomes)
        print(f"📦 {outcome}")
        
        if reward > 0:
            if "gold" in outcome.lower():
                self.game_state['gold'] += reward
                print(f"💰 Gained {reward} gold!")
            elif "experience" in outcome.lower():
                self.game_state['experience'] += reward
                print(f"📈 Gained {reward} experience!")
                self.check_level_up()
        
        self.log_event(f"Explored {self.game_state['location']} - {outcome}")
    
    def simulate_inventory_management(self):
        """Simulate inventory management"""
        print(f"\n🎒 Inventory Management")
        print("=" * 25)
        
        # Create some items
        items = [
            {'name': 'Health Potion', 'type': 'consumable', 'value': 15},
            {'name': 'Steel Sword', 'type': 'weapon', 'value': 50},
            {'name': 'Magic Ring', 'type': 'accessory', 'value': 100},
            {'name': 'Leather Armor', 'type': 'armor', 'value': 30}
        ]
        
        # Add items to inventory
        for item in items:
            if random.random() < 0.7:  # 70% chance to find each item
                self.game_state['inventory'].append(item)
                print(f"📦 Found: {item['name']} ({item['type']})")
        
        # Display inventory
        print(f"\n📋 Inventory ({len(self.game_state['inventory'])} items):")
        for item in self.game_state['inventory']:
            print(f"  • {item['name']} ({item['type']}) - Value: {item['value']} gold")
        
        # Use a health potion if available
        health_potions = [item for item in self.game_state['inventory'] if item['name'] == 'Health Potion']
        if health_potions and self.game_state['player']['health'] < self.game_state['player']['max_health']:
            potion = health_potions[0]
            self.game_state['inventory'].remove(potion)
            self.game_state['player']['health'] = min(self.game_state['player']['max_health'], 
                                                    self.game_state['player']['health'] + 30)
            print(f"💊 Used Health Potion! Health: {self.game_state['player']['health']}/{self.game_state['player']['max_health']}")
        
        self.log_event(f"Managed inventory - {len(self.game_state['inventory'])} items")
    
    def simulate_quest_completion(self):
        """Simulate quest completion"""
        print(f"\n📜 Quest Completion")
        print("=" * 20)
        
        quests = [
            {"name": "Defeat the Goblin Raiders", "reward": {"experience": 50, "gold": 25}},
            {"name": "Find the Lost Artifact", "reward": {"experience": 75, "gold": 40}},
            {"name": "Clear the Cave of Shadows", "reward": {"experience": 100, "gold": 60}},
            {"name": "Rescue the Village Elder", "reward": {"experience": 150, "gold": 80}}
        ]
        
        quest = random.choice(quests)
        print(f"🎯 Completed: {quest['name']}")
        
        # Apply rewards
        self.game_state['experience'] += quest['reward']['experience']
        self.game_state['gold'] += quest['reward']['gold']
        
        print(f"📈 Experience gained: {quest['reward']['experience']}")
        print(f"💰 Gold gained: {quest['reward']['gold']}")
        
        self.check_level_up()
        self.log_event(f"Completed quest: {quest['name']}")
    
    def simulate_multiplayer_features(self):
        """Simulate multiplayer features"""
        print(f"\n👥 Multiplayer Features")
        print("=" * 25)
        
        # Simulate guild creation
        print("🏰 Creating a guild...")
        guild_name = "The Dragon Slayers"
        print(f"✅ Guild '{guild_name}' created successfully!")
        
        # Simulate party formation
        party_members = ["SimulatedHero", "MagePlayer", "RoguePlayer", "HealerPlayer"]
        print(f"👥 Formed party with {len(party_members)} members:")
        for member in party_members:
            print(f"  • {member}")
        
        # Simulate group combat
        print(f"\n⚔️ Group Combat Simulation")
        print("=" * 30)
        
        group_enemy = {
            'name': 'Ancient Dragon',
            'level': 10,
            'health': 200,
            'max_health': 200
        }
        
        print(f"🐉 Fighting: {group_enemy['name']} (Level {group_enemy['level']})")
        print(f"🩸 Enemy Health: {group_enemy['health']}/{group_enemy['max_health']}")
        
        # Simulate group combat rounds
        for round_num in range(1, 6):
            total_damage = 0
            for member in party_members:
                damage = random.randint(15, 25)
                total_damage += damage
                print(f"⚔️ {member} deals {damage} damage")
            
            group_enemy['health'] = max(0, group_enemy['health'] - total_damage)
            print(f"🐉 Dragon health: {group_enemy['health']}/{group_enemy['max_health']}")
            
            if group_enemy['health'] <= 0:
                print(f"💀 {group_enemy['name']} defeated!")
                break
            
            # Dragon counter-attack
            dragon_damage = random.randint(20, 35)
            print(f"🐉 Dragon deals {dragon_damage} damage to the party!")
            
            time.sleep(0.5)
        
        if group_enemy['health'] <= 0:
            print(f"\n🎉 Group victory! All party members gain experience!")
            self.game_state['experience'] += 200
            self.game_state['gold'] += 150
            self.check_level_up()
        
        self.log_event(f"Participated in group combat against {group_enemy['name']}")
    
    def log_event(self, event):
        """Log a game event"""
        self.simulation_log.append({
            'timestamp': time.time(),
            'event': event,
            'player_level': self.game_state['player']['level'],
            'location': self.game_state['location']
        })
    
    def print_game_status(self):
        """Print current game status"""
        player = self.game_state['player']
        print(f"\n📊 GAME STATUS")
        print("=" * 15)
        print(f"👤 Player: {player['name']} (Level {player['level']})")
        print(f"🩸 Health: {player['health']}/{player['max_health']}")
        print(f"📈 Experience: {self.game_state['experience']}")
        print(f"💰 Gold: {self.game_state['gold']}")
        print(f"🗺️ Location: {self.game_state['location']}")
        print(f"🎒 Inventory: {len(self.game_state['inventory'])} items")
        print(f"📜 Quests: {len(self.game_state['quests'])} active")
    
    def run_new_player_scenario(self):
        """Simulate a new player's first experience"""
        print("\n🎮 NEW PLAYER SCENARIO")
        print("=" * 30)
        
        if not self.setup_game_systems():
            return
        
        # Create character
        self.create_player("NewHero", "Warrior")
        
        # Initial exploration
        self.simulate_exploration()
        
        # First combat encounter
        self.simulate_combat_encounter("Goblin")
        
        # Inventory management
        self.simulate_inventory_management()
        
        # First quest
        self.simulate_quest_completion()
        
        # Level up
        self.check_level_up()
        
        self.print_game_status()
    
    def run_combat_focused_scenario(self):
        """Focus on combat mechanics"""
        print("\n⚔️ COMBAT FOCUSED SCENARIO")
        print("=" * 30)
        
        if not self.setup_game_systems():
            return
        
        self.create_player("CombatHero", "Warrior")
        
        # Multiple combat encounters
        enemies = ["Goblin", "Orc", "Troll"]
        for enemy in enemies:
            self.simulate_combat_encounter(enemy)
            time.sleep(1)
        
        self.print_game_status()
    
    def run_exploration_scenario(self):
        """Focus on exploration and discovery"""
        print("\n🗺️ EXPLORATION SCENARIO")
        print("=" * 30)
        
        if not self.setup_game_systems():
            return
        
        self.create_player("Explorer", "Rogue")
        
        # Multiple exploration events
        for i in range(5):
            self.simulate_exploration()
            time.sleep(0.5)
        
        # Inventory management
        self.simulate_inventory_management()
        
        self.print_game_status()
    
    def run_multiplayer_scenario(self):
        """Demonstrate multiplayer features"""
        print("\n👥 MULTIPLAYER SCENARIO")
        print("=" * 30)
        
        if not self.setup_game_systems():
            return
        
        self.create_player("MultiplayerHero", "Warrior")
        
        # Multiplayer features
        self.simulate_multiplayer_features()
        
        self.print_game_status()
    
    def run_full_gameplay_scenario(self):
        """Complete gameplay simulation"""
        print("\n🎮 FULL GAMEPLAY SCENARIO")
        print("=" * 35)
        
        if not self.setup_game_systems():
            return
        
        self.create_player("FullGameHero", "Warrior")
        
        # Complete gameplay loop
        for i in range(3):
            self.simulate_exploration()
            self.simulate_combat_encounter(random.choice(["Goblin", "Orc"]))
            self.simulate_inventory_management()
            time.sleep(0.5)
        
        self.simulate_quest_completion()
        self.simulate_multiplayer_features()
        
        self.print_game_status()
    
    def run(self, scenario="new_player", duration=None):
        """Main execution method"""
        print("🚀 Starting Sunderfall Game Simulation")
        print("=" * 45)
        
        scenarios = {
            'new_player': self.run_new_player_scenario,
            'combat_focused': self.run_combat_focused_scenario,
            'exploration': self.run_exploration_scenario,
            'multiplayer': self.run_multiplayer_scenario,
            'full_gameplay': self.run_full_gameplay_scenario
        }
        
        if scenario in scenarios:
            scenarios[scenario]()
        else:
            print(f"❌ Unknown scenario: {scenario}")
            print(f"Available scenarios: {', '.join(scenarios.keys())}")
        
        print(f"\n📝 Simulation Log ({len(self.simulation_log)} events):")
        for event in self.simulation_log[-5:]:  # Show last 5 events
            print(f"  • {event['event']}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Game simulation for Sunderfall")
    parser.add_argument('--scenario', default='new_player', 
                       choices=['new_player', 'combat_focused', 'exploration', 'multiplayer', 'full_gameplay'],
                       help='Scenario to simulate')
    parser.add_argument('--duration', type=int, help='Simulation duration in seconds')
    
    args = parser.parse_args()
    
    simulator = GameSimulator()
    simulator.run(args.scenario, args.duration)


if __name__ == "__main__":
    main()

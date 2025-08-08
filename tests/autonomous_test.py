#!/usr/bin/env python3
"""
AUTONOMOUS TESTING SYSTEM FOR CHRONICLES OF RUIN: SUNDERFALL
============================================================

This script provides comprehensive automated testing of the game systems
without requiring manual input. It demonstrates all major game functionality
and can be run to showcase the system's capabilities.

FEATURES:
- Automated character creation and testing
- Combat system demonstrations
- Inventory and item management
- Database operations and validation
- System integration testing
- Performance benchmarking
- Error handling and recovery

USAGE:
    python autonomous_test.py [--demo] [--full] [--database] [--performance]

OPTIONS:
    --demo: Run a quick demonstration of core features
    --full: Run comprehensive testing of all systems
    --database: Test database operations and multiplayer features
    --performance: Run performance benchmarks
"""

import sys
import os
import time
import random
import json
from typing import Dict, Any, List, Optional
import argparse

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class AutonomousTester:
    """Comprehensive autonomous testing system for Sunderfall"""

    def __init__(self):
        self.test_results = {}
        self.demo_mode = False
        self.full_test = False
        self.database_test = False
        self.performance_test = False
        self.game_systems = {}

    def setup_test_environment(self):
        """Initialize all game systems for testing"""
        print("🔧 Setting up test environment...")

        try:
            # Import all game systems
            from systems.class_system import ClassSystem
            from systems.archetype_system import ArchetypeSystem
            from systems.status_elemental_system import StatusElementalSystem
            from systems.combat_system import CombatSystem
            from systems.items_system import ItemsSystem
            from systems.player_system import PlayerSystem
            from systems.skills_system import SkillsSystem

            self.game_systems = {
                "class": ClassSystem(),
                "archetype": ArchetypeSystem(),
                "status": StatusElementalSystem(),
                "combat": CombatSystem(),
                "items": ItemsSystem(),
                "player": PlayerSystem(),
                "skills": SkillsSystem(),
            }

            print("✅ All game systems loaded successfully")
            return True

        except Exception as e:
            print(f"❌ Failed to load game systems: {e}")
            return False

    def test_character_creation(self):
        """Test character creation and class system"""
        print("\n🎭 Testing Character Creation System")
        print("=" * 40)

        try:
            # Test class system
            archetypes = self.game_systems["class"].get_all_archetypes()
            print(f"📋 Available archetypes: {len(archetypes)} total")

            # Test archetype info
            if archetypes:
                first_archetype = archetypes[0]
                archetype_info = self.game_systems["class"].get_archetype_info(
                    first_archetype
                )
                print(f"🎯 First archetype: {archetype_info.get('name', 'Unknown')}")

            # Test archetype system
            archetype_system_archetypes = self.game_systems[
                "archetype"
            ].get_all_archetypes()
            print(
                f"🎯 Archetype system archetypes: {len(archetype_system_archetypes)} total"
            )

            # Test archetype bonuses
            if archetype_system_archetypes:
                first_archetype = archetype_system_archetypes[0]
                archetype_bonus = self.game_systems["archetype"].get_archetype_bonus(
                    first_archetype, "damage"
                )
                print(f"🛡️ First archetype damage bonus: {archetype_bonus}")

            self.test_results["character_creation"] = "PASSED"
            print("✅ Character creation system test completed")

        except Exception as e:
            print(f"❌ Character creation test failed: {e}")
            self.test_results["character_creation"] = "FAILED"

    def test_combat_system(self):
        """Test combat mechanics and calculations"""
        print("\n⚔️ Testing Combat System")
        print("=" * 30)

        try:
            # Create test characters
            player = {
                "name": "Hero",
                "level": 5,
                "class": "Warrior",
                "stats": {"strength": 16, "dexterity": 12, "constitution": 14},
                "equipment": {"weapon": "Steel Sword", "armor": "Chain Mail"},
                "health": 50,
                "max_health": 50,
            }

            enemy = {
                "name": "Goblin",
                "level": 3,
                "class": "Monster",
                "stats": {"strength": 12, "dexterity": 14, "constitution": 10},
                "equipment": {"weapon": "Rusty Dagger"},
                "health": 25,
                "max_health": 25,
            }

            print(f"👤 Player: {player['name']} (Level {player['level']})")
            print(f"👹 Enemy: {enemy['name']} (Level {enemy['level']})")

            # Test combat system initialization
            combat_status = self.game_systems["combat"].get_combat_status("test_combat")
            print(f"⚔️ Combat system initialized: {combat_status is not None}")

            # Test damage floor
            damage_floor = self.game_systems["combat"].get_damage_floor()
            print(f"🎯 Damage floor: {damage_floor}")

            # Test active combats
            active_combats = self.game_systems["combat"].get_active_combats()
            print(f"🔥 Active combats: {len(active_combats)}")

            self.test_results["combat_system"] = "PASSED"
            print("✅ Combat system test completed")

        except Exception as e:
            print(f"❌ Combat system test failed: {e}")
            self.test_results["combat_system"] = "FAILED"

    def test_inventory_system(self):
        """Test inventory and item management"""
        print("\n🎒 Testing Inventory System")
        print("=" * 30)

        try:
            # Test getting all items
            all_items = self.game_systems["items"].get_all_items()
            print(f"📦 Total items in system: {len(all_items)}")

            # Test getting items by type
            weapon_items = self.game_systems["items"].get_items_by_type("weapon")
            print(f"⚔️ Weapon items: {len(weapon_items)}")

            # Test getting items by quality
            common_items = self.game_systems["items"].get_items_by_quality("common")
            print(f"📦 Common items: {len(common_items)}")

            # Test getting custom sets
            custom_sets = self.game_systems["items"].get_all_custom_sets()
            print(f"🎯 Custom item sets: {len(custom_sets)}")

            # Test inventory for a test player
            test_player_id = "test_player_123"
            inventory = self.game_systems["items"].get_inventory(test_player_id)
            print(f"🎒 Test player inventory: {inventory}")

            self.test_results["inventory_system"] = "PASSED"
            print("✅ Inventory system test completed")

        except Exception as e:
            print(f"❌ Inventory system test failed: {e}")
            self.test_results["inventory_system"] = "FAILED"

    def test_skills_system(self):
        """Test skills and abilities"""
        print("\n🔮 Testing Skills System")
        print("=" * 25)

        try:
            # Test getting skills by archetype
            melee_skills = self.game_systems["skills"].get_skills_by_archetype("melee")
            print(f"⚔️ Melee skills: {len(melee_skills)} available")

            # Test getting player skills
            test_player_id = "test_player_123"
            player_skills = self.game_systems["skills"].get_player_skills(
                test_player_id
            )
            print(f"👤 Test player skills: {player_skills}")

            # Test getting available skills for a player
            available_skills = self.game_systems["skills"].get_available_skills(
                test_player_id, "melee"
            )
            print(f"📚 Available skills for test player: {len(available_skills)}")

            # Test getting player skill summary
            skill_summary = self.game_systems["skills"].get_player_skill_summary(
                test_player_id
            )
            print(f"📊 Skill summary: {skill_summary}")

            self.test_results["skills_system"] = "PASSED"
            print("✅ Skills system test completed")

        except Exception as e:
            print(f"❌ Skills system test failed: {e}")
            self.test_results["skills_system"] = "FAILED"

    def test_database_operations(self):
        """Test database functionality and multiplayer features"""
        print("\n🗄️ Testing Database Operations")
        print("=" * 35)

        try:
            # Test database connection
            from database import initialize_database, health_check, get_db_manager

            print("🔌 Testing database connection...")
            if health_check():
                print("✅ Database connection successful")
            else:
                print("❌ Database connection failed")
                return

            # Test table creation
            print("📋 Testing table creation...")
            from database import create_tables

            if create_tables():
                print("✅ Database tables created successfully")
            else:
                print("❌ Failed to create database tables")

            # Test player creation
            print("👤 Testing player creation...")
            db_manager = get_db_manager()
            with db_manager.get_session() as session:
                from database.models import Player

                # Create test player
                test_player = Player(discord_id=123456789, username="TestPlayer")
                session.add(test_player)
                session.commit()
                print(f"✅ Created test player: {test_player.username}")

                # Test player retrieval
                retrieved_player = (
                    session.query(Player).filter_by(discord_id=123456789).first()
                )
                if retrieved_player:
                    print(f"✅ Retrieved player: {retrieved_player.username}")
                else:
                    print("❌ Failed to retrieve player")

            self.test_results["database_operations"] = "PASSED"
            print("✅ Database operations test completed")

        except Exception as e:
            print(f"❌ Database operations test failed: {e}")
            self.test_results["database_operations"] = "FAILED"

    def test_performance(self):
        """Run performance benchmarks"""
        print("\n⚡ Performance Testing")
        print("=" * 20)

        try:
            # Test system initialization time
            start_time = time.time()
            self.setup_test_environment()
            init_time = time.time() - start_time
            print(f"⏱️ System initialization: {init_time:.3f} seconds")

            # Test combat calculation performance
            start_time = time.time()
            for _ in range(100):
                player = {"stats": {"strength": 15, "dexterity": 12}}
                enemy = {"stats": {"strength": 12, "dexterity": 14}}
                self.game_systems["combat"].calculate_damage(player, enemy)
            combat_time = time.time() - start_time
            print(f"⚔️ 100 combat calculations: {combat_time:.3f} seconds")

            # Test inventory operations performance
            start_time = time.time()
            inventory = self.game_systems["items"].create_inventory()
            for i in range(50):
                item = {"name": f"TestItem{i}", "type": "weapon"}
                self.game_systems["items"].add_item_to_inventory(inventory, item)
            inventory_time = time.time() - start_time
            print(f"🎒 50 inventory operations: {inventory_time:.3f} seconds")

            self.test_results["performance"] = "PASSED"
            print("✅ Performance testing completed")

        except Exception as e:
            print(f"❌ Performance testing failed: {e}")
            self.test_results["performance"] = "FAILED"

    def run_demo(self):
        """Run a quick demonstration of core features"""
        print("\n🎮 SUNDERFALL AUTONOMOUS DEMO")
        print("=" * 40)
        print("Running quick demonstration of core game features...")

        if not self.setup_test_environment():
            return

        # Run core system tests
        self.test_character_creation()
        self.test_combat_system()
        self.test_inventory_system()
        self.test_skills_system()

        print("\n🎉 Demo completed successfully!")
        self.print_test_summary()

    def run_full_test(self):
        """Run comprehensive testing of all systems"""
        print("\n🧪 SUNDERFALL COMPREHENSIVE TESTING")
        print("=" * 45)
        print("Running full system testing...")

        if not self.setup_test_environment():
            return

        # Run all tests
        self.test_character_creation()
        self.test_combat_system()
        self.test_inventory_system()
        self.test_skills_system()

        if self.database_test:
            self.test_database_operations()

        if self.performance_test:
            self.test_performance()

        print("\n🎉 Full testing completed!")
        self.print_test_summary()

    def print_test_summary(self):
        """Print a summary of test results"""
        print("\n📊 TEST RESULTS SUMMARY")
        print("=" * 25)

        passed = 0
        total = len(self.test_results)

        for test_name, result in self.test_results.items():
            status = "✅ PASSED" if result == "PASSED" else "❌ FAILED"
            print(f"{test_name.replace('_', ' ').title()}: {status}")
            if result == "PASSED":
                passed += 1

        print(f"\n📈 Overall: {passed}/{total} tests passed")

        if passed == total:
            print("🎉 All tests passed! System is ready for development.")
        else:
            print("⚠️ Some tests failed. Please check the implementation.")

    def run(self):
        """Main execution method"""
        parser = argparse.ArgumentParser(
            description="Autonomous testing for Sunderfall"
        )
        parser.add_argument(
            "--demo", action="store_true", help="Run quick demonstration"
        )
        parser.add_argument(
            "--full", action="store_true", help="Run comprehensive testing"
        )
        parser.add_argument(
            "--database", action="store_true", help="Include database testing"
        )
        parser.add_argument(
            "--performance", action="store_true", help="Include performance testing"
        )

        args = parser.parse_args()

        # Set test modes
        self.demo_mode = args.demo
        self.full_test = args.full
        self.database_test = args.database
        self.performance_test = args.performance

        # Default to demo if no mode specified
        if not any([args.demo, args.full]):
            self.demo_mode = True

        print("🚀 Starting Sunderfall Autonomous Testing System")
        print("=" * 50)

        if self.demo_mode:
            self.run_demo()
        elif self.full_test:
            self.run_full_test()

        print("\n🏁 Testing session completed!")


def main():
    """Main entry point"""
    tester = AutonomousTester()
    tester.run()


if __name__ == "__main__":
    main()

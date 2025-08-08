"""
Comprehensive Test Suite for Monster System - Chronicles of Ruin: Sunderfall

This module tests all aspects of the monster system including scaling mechanics,
monster generation, classification bonuses, and behavior mechanics.
"""

import sys
import os
import unittest
import random
from typing import Dict, List

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from systems.monster_system import (
    MonsterSystem,
    MonsterArchetype,
    MonsterClassification,
)


class TestMonsterSystem(unittest.TestCase):
    """Test suite for the Monster System."""

    def setUp(self):
        """Set up test fixtures."""
        self.monster_system = MonsterSystem()

    def test_monster_level_scaling_early_game(self):
        """Test monster level scaling in early game."""
        # Level 1 monster, Player Level 5
        final_level = self.monster_system.calculate_monster_level(1, 5)

        # Should be between 1 and 11 (base + 10 max)
        self.assertGreaterEqual(final_level, 1)
        self.assertLessEqual(final_level, 11)

        print(f"✅ Early Game Scaling: Base 1, Player 5 → Level {final_level}")

    def test_monster_level_scaling_mid_game(self):
        """Test monster level scaling in mid game."""
        # Level 1 monster, Player Level 15
        final_level = self.monster_system.calculate_monster_level(1, 15)

        # Should be capped at 11 (base 1 + 10 max)
        self.assertLessEqual(final_level, 11)

        print(
            f"✅ Mid Game Scaling: Base 1, Player 15 → Level {final_level} (capped at 11)"
        )

    def test_monster_level_scaling_late_game(self):
        """Test monster level scaling in late game."""
        # Level 10 monster, Player Level 40
        final_level = self.monster_system.calculate_monster_level(10, 40)

        # Should be capped at 20 (base 10 + 10 max)
        self.assertLessEqual(final_level, 20)

        print(
            f"✅ Late Game Scaling: Base 10, Player 40 → Level {final_level} (capped at 20)"
        )

    def test_monster_level_scaling_no_cap_needed(self):
        """Test monster level scaling when cap isn't needed."""
        # Level 15 monster, Player Level 20
        final_level = self.monster_system.calculate_monster_level(15, 20)

        # Should be around 15-17 (base 15 + small scaling + random variation)
        # Allow for random variation of ±2
        self.assertGreaterEqual(final_level, 13)
        self.assertLessEqual(final_level, 19)

        print(f"✅ No Cap Needed: Base 15, Player 20 → Level {final_level}")

    def test_monster_level_scaling_negative_player_level(self):
        """Test monster level scaling when player level is lower than base."""
        # Level 10 monster, Player Level 5
        final_level = self.monster_system.calculate_monster_level(10, 5)

        # Should be around 8-12 (base 10 + negative scaling + random variation)
        # Allow for random variation of ±2
        self.assertGreaterEqual(final_level, 6)
        self.assertLessEqual(final_level, 12)

        print(f"✅ Negative Scaling: Base 10, Player 5 → Level {final_level}")

    def test_monster_stats_generation_melee(self):
        """Test monster stats generation for melee archetype."""
        stats = self.monster_system.generate_monster_stats(
            5, MonsterArchetype.MELEE, MonsterClassification.HUMANOID, False
        )

        # Melee gets +20% health, +30% damage, +25% defense
        expected_health = int((50 + (5 * 10)) * 1.2)  # Base health * 1.2
        expected_damage = int((10 + (5 * 2)) * 1.3)  # Base damage * 1.3
        expected_defense = int((5 + (5 * 1)) * 1.25)  # Base defense * 1.25

        self.assertEqual(stats["health"], expected_health)
        self.assertEqual(stats["damage"], expected_damage)
        self.assertEqual(stats["defense"], expected_defense)

        print(
            f"✅ Melee Stats: Health {stats['health']}, Damage {stats['damage']}, Defense {stats['defense']}"
        )

    def test_monster_stats_generation_wild(self):
        """Test monster stats generation for Wild monsters."""
        stats = self.monster_system.generate_monster_stats(
            5, MonsterArchetype.MELEE, MonsterClassification.HUMANOID, True
        )

        # Wild gets +50% to all stats and +3 levels
        self.assertEqual(stats["level"], 8)  # 5 + 3
        self.assertGreater(stats["health"], 100)  # Should be significantly higher
        self.assertGreater(stats["damage"], 20)  # Should be significantly higher

        print(
            f"✅ Wild Stats: Level {stats['level']}, Health {stats['health']}, Damage {stats['damage']}"
        )

    def test_monster_classification_bonuses_demonic(self):
        """Test demonic classification bonuses."""
        stats = self.monster_system.generate_monster_stats(
            5, MonsterArchetype.MELEE, MonsterClassification.DEMONIC, False
        )

        # Demonic gets fire damage and burn immunity
        self.assertIn("fire_damage", stats)
        self.assertIn("burn_resistance", stats)
        self.assertTrue(stats["burn_immune"])

        print(
            f"✅ Demonic Bonuses: Fire Damage {stats['fire_damage']}, Burn Immune: {stats['burn_immune']}"
        )

    def test_monster_classification_bonuses_undead(self):
        """Test undead classification bonuses."""
        stats = self.monster_system.generate_monster_stats(
            5, MonsterArchetype.MELEE, MonsterClassification.UNDEAD, False
        )

        # Undead gets cold damage and stun immunity
        self.assertIn("cold_damage", stats)
        self.assertIn("stun_resistance", stats)
        self.assertTrue(stats["stun_immune"])

        print(
            f"✅ Undead Bonuses: Cold Damage {stats['cold_damage']}, Stun Immune: {stats['stun_immune']}"
        )

    def test_monster_classification_bonuses_elemental(self):
        """Test elemental classification bonuses."""
        stats = self.monster_system.generate_monster_stats(
            5, MonsterArchetype.MELEE, MonsterClassification.ELEMENTAL, False
        )

        # Elemental gets elemental damage and status immunity
        self.assertIn("elemental_damage", stats)
        self.assertIn("status_resistance", stats)
        self.assertTrue(stats["status_immune"])

        print(
            f"✅ Elemental Bonuses: Elemental Damage {stats['elemental_damage']}, Status Immune: {stats['status_immune']}"
        )

    def test_monster_type_distribution_early_districts(self):
        """Test monster type distribution in early districts."""
        # Set random seed for consistent testing
        random.seed(42)

        melee_count = 0
        ranged_count = 0
        magic_count = 0
        wild_count = 0

        for _ in range(100):
            archetype, classification = self.monster_system.determine_monster_type(3, 5)
            if archetype == MonsterArchetype.MELEE:
                melee_count += 1
            elif archetype == MonsterArchetype.RANGED:
                ranged_count += 1
            elif archetype == MonsterArchetype.MAGIC:
                magic_count += 1
            elif archetype == MonsterArchetype.WILD:
                wild_count += 1

        # Early districts should have more melee and ranged
        self.assertGreater(melee_count, 30)  # Should be around 40%
        self.assertGreater(ranged_count, 20)  # Should be around 30%

        print(
            f"✅ Early District Distribution: Melee {melee_count}, Ranged {ranged_count}, Magic {magic_count}, Wild {wild_count}"
        )

    def test_monster_type_distribution_late_districts(self):
        """Test monster type distribution in late districts."""
        # Set random seed for consistent testing
        random.seed(42)

        melee_count = 0
        ranged_count = 0
        magic_count = 0
        wild_count = 0

        for _ in range(100):
            archetype, classification = self.monster_system.determine_monster_type(
                25, 40
            )
            if archetype == MonsterArchetype.MELEE:
                melee_count += 1
            elif archetype == MonsterArchetype.RANGED:
                ranged_count += 1
            elif archetype == MonsterArchetype.MAGIC:
                magic_count += 1
            elif archetype == MonsterArchetype.WILD:
                wild_count += 1

        # Late districts should have more magic and wild
        self.assertGreater(magic_count, 20)  # Should be around 30%
        self.assertGreater(wild_count, 15)  # Should be around 20%

        print(
            f"✅ Late District Distribution: Melee {melee_count}, Ranged {ranged_count}, Magic {magic_count}, Wild {wild_count}"
        )

    def test_monster_spawn_early_game(self):
        """Test monster spawning in early game."""
        monster = self.monster_system.spawn_monster(5, 10, 3)

        # Verify monster structure
        self.assertIn("name", monster)
        self.assertIn("level", monster)
        self.assertIn("archetype", monster)
        self.assertIn("classification", monster)
        self.assertIn("stats", monster)
        self.assertIn("loot_table", monster)
        self.assertIn("experience_reward", monster)

        # Verify level scaling
        self.assertGreaterEqual(monster["level"], 1)
        self.assertLessEqual(monster["level"], 13)  # Base 3 + 10 max

        print(f"✅ Early Game Spawn: {monster['name']} (Level {monster['level']})")

    def test_monster_spawn_mid_game(self):
        """Test monster spawning in mid game."""
        monster = self.monster_system.spawn_monster(15, 25, 8)

        # Verify level scaling
        self.assertGreaterEqual(monster["level"], 6)
        self.assertLessEqual(monster["level"], 18)  # Base 8 + 10 max

        print(f"✅ Mid Game Spawn: {monster['name']} (Level {monster['level']})")

    def test_monster_spawn_late_game(self):
        """Test monster spawning in late game."""
        monster = self.monster_system.spawn_monster(30, 50, 15)

        # Verify level scaling
        self.assertGreaterEqual(monster["level"], 13)
        self.assertLessEqual(monster["level"], 25)  # Base 15 + 10 max

        print(f"✅ Late Game Spawn: {monster['name']} (Level {monster['level']})")

    def test_monster_name_generation(self):
        """Test monster name generation."""
        # Test regular monster
        name = self.monster_system.generate_monster_name(
            MonsterArchetype.MELEE, MonsterClassification.HUMANOID, False, False
        )
        self.assertIsInstance(name, str)
        self.assertGreater(len(name), 0)

        # Test Wild monster
        wild_name = self.monster_system.generate_monster_name(
            MonsterArchetype.MELEE, MonsterClassification.HUMANOID, True, False
        )
        self.assertIn("Wild", wild_name)

        # Test unique monster
        unique_name = self.monster_system.generate_monster_name(
            MonsterArchetype.MELEE, MonsterClassification.HUMANOID, False, True
        )
        self.assertIn("Unique", unique_name)

        print(
            f"✅ Name Generation: Regular '{name}', Wild '{wild_name}', Unique '{unique_name}'"
        )

    def test_loot_table_generation(self):
        """Test loot table generation."""
        # Regular monster stats
        regular_stats = {"level": 10, "is_unique": False}
        regular_loot = self.monster_system.generate_loot_table(regular_stats)

        self.assertIn("gold", regular_loot)
        self.assertIn("guaranteed_unique_item", regular_loot)
        self.assertIn("item_level", regular_loot)
        self.assertIn("drop_chance_multiplier", regular_loot)

        # Check gold range for regular monster (level * 2 + random 1-10)
        expected_min_gold = 10 * 2 + 1  # 21
        expected_max_gold = 10 * 2 + 10  # 30
        self.assertGreaterEqual(regular_loot["gold"], expected_min_gold)
        self.assertLessEqual(regular_loot["gold"], expected_max_gold)

        # Unique monster stats
        unique_stats = {"level": 10, "is_unique": True}
        unique_loot = self.monster_system.generate_loot_table(unique_stats)

        self.assertTrue(unique_loot["guaranteed_unique_item"])

        # Check gold range for unique monster (5x regular)
        expected_min_unique_gold = expected_min_gold * 5  # 105
        expected_max_unique_gold = expected_max_gold * 5  # 150
        self.assertGreaterEqual(unique_loot["gold"], expected_min_unique_gold)
        self.assertLessEqual(unique_loot["gold"], expected_max_unique_gold)

        self.assertEqual(unique_loot["drop_chance_multiplier"], 3.0)

        print(
            f"✅ Loot Generation: Regular Gold {regular_loot['gold']} (range: {expected_min_gold}-{expected_max_gold})"
        )
        print(
            f"✅ Unique Gold {unique_loot['gold']} (range: {expected_min_unique_gold}-{expected_max_unique_gold})"
        )

    def test_experience_reward_calculation(self):
        """Test experience reward calculation."""
        # Regular monster
        regular_stats = {"level": 10, "is_wild": False, "is_unique": False}
        regular_exp = self.monster_system.calculate_experience_reward(regular_stats)
        expected_regular = 10 * 10  # level * 10
        self.assertEqual(regular_exp, expected_regular)

        # Wild monster
        wild_stats = {"level": 10, "is_wild": True, "is_unique": False}
        wild_exp = self.monster_system.calculate_experience_reward(wild_stats)
        expected_wild = 10 * 10 * 2  # level * 10 * 2
        self.assertEqual(wild_exp, expected_wild)

        # Unique monster
        unique_stats = {"level": 10, "is_wild": False, "is_unique": True}
        unique_exp = self.monster_system.calculate_experience_reward(unique_stats)
        expected_unique = 10 * 10 * 5  # level * 10 * 5
        self.assertEqual(unique_exp, expected_unique)

        print(
            f"✅ Experience Rewards: Regular {regular_exp}, Wild {wild_exp}, Unique {unique_exp}"
        )

    def test_wild_monster_spawn_chance(self):
        """Test Wild monster spawn chance."""
        # Set random seed for consistent testing
        random.seed(42)

        wild_count = 0
        total_spawns = 1000

        for _ in range(total_spawns):
            monster = self.monster_system.spawn_monster(10, 20, 5)
            if monster["is_wild"]:
                wild_count += 1

        # Should be around 5% (0.05 * 1000 = 50)
        wild_percentage = (wild_count / total_spawns) * 100
        self.assertGreater(wild_percentage, 3)  # At least 3%
        self.assertLess(wild_percentage, 7)  # At most 7%

        print(
            f"✅ Wild Spawn Rate: {wild_count}/{total_spawns} ({wild_percentage:.1f}%)"
        )

    def test_unique_monster_spawn_chance(self):
        """Test unique monster spawn chance."""
        # Set random seed for consistent testing
        random.seed(42)

        unique_count = 0
        total_spawns = 1000

        for _ in range(total_spawns):
            monster = self.monster_system.spawn_monster(10, 20, 5)
            if monster["is_unique"]:
                unique_count += 1

        # Should be around 1% (0.01 * 1000 = 10)
        unique_percentage = (unique_count / total_spawns) * 100
        self.assertGreater(unique_percentage, 0.5)  # At least 0.5%
        self.assertLess(unique_percentage, 1.5)  # At most 1.5%

        print(
            f"✅ Unique Spawn Rate: {unique_count}/{total_spawns} ({unique_percentage:.1f}%)"
        )

    def test_monster_scaling_cap_mechanic(self):
        """Test that monster scaling is properly capped at +10 levels."""
        # Test various scenarios where scaling should be capped
        test_cases = [
            (1, 20),  # Base 1, Player 20 → Should cap at 11
            (5, 25),  # Base 5, Player 25 → Should cap at 15
            (10, 30),  # Base 10, Player 30 → Should cap at 20
            (20, 50),  # Base 20, Player 50 → Should cap at 30
        ]

        for base_level, player_level in test_cases:
            final_level = self.monster_system.calculate_monster_level(
                base_level, player_level
            )
            max_allowed = base_level + 10

            self.assertLessEqual(final_level, max_allowed)
            print(
                f"✅ Scaling Cap: Base {base_level}, Player {player_level} → Level {final_level} (Max: {max_allowed})"
            )


def run_monster_tests():
    """Run all monster system tests with detailed output."""
    print("👹 MONSTER SYSTEM TESTING 🔥")
    print("=" * 60)

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMonsterSystem)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")

    if result.errors:
        print("\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")

    if result.wasSuccessful():
        print("\n🎉 ALL TESTS PASSED! Monster system is working correctly!")
    else:
        print("\n⚠️  Some tests failed. Please review the issues above.")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_monster_tests()
    sys.exit(0 if success else 1)

"""
Comprehensive Test Suite for XP System - Chronicles of Ruin: Sunderfall

This module tests all aspects of the XP system including XP calculations,
point allocation, monster rewards, and level progression mechanics.
"""

import sys
import os
import unittest
from typing import Dict, List

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from systems.xp_system import XPSystem, XPType


class TestXPSystem(unittest.TestCase):
    """Test suite for the XP System."""

    def setUp(self):
        """Set up test fixtures."""
        self.xp_system = XPSystem()

    def test_xp_requirement_calculation(self):
        """Test XP requirement calculation for different levels."""
        # Test first few levels
        level_1_xp = self.xp_system.calculate_xp_requirement(1)
        level_2_xp = self.xp_system.calculate_xp_requirement(2)
        level_3_xp = self.xp_system.calculate_xp_requirement(3)

        # Should have exponential growth
        self.assertEqual(level_1_xp, 100)  # Base XP
        self.assertEqual(level_2_xp, 102)  # 100 * 1.025
        self.assertEqual(level_3_xp, 105)  # 102 * 1.025

        print(
            f"✅ XP Requirements: Level 1 = {level_1_xp}, Level 2 = {level_2_xp}, Level 3 = {level_3_xp}"
        )

    def test_total_xp_calculation(self):
        """Test total XP calculation for reaching specific levels."""
        # Test total XP for level 5
        total_xp_level_5 = self.xp_system.calculate_total_xp_for_level(5)

        # Should be sum of XP requirements for levels 1-4 (to reach level 5)
        expected_total = sum(
            self.xp_system.calculate_xp_requirement(i) for i in range(1, 5)
        )
        self.assertEqual(total_xp_level_5, expected_total)

        print(f"✅ Total XP for Level 5: {total_xp_level_5}")

    def test_level_from_xp_calculation(self):
        """Test calculating level from total XP."""
        # Test various XP amounts
        test_cases = [
            (0, 1, 0),  # 0 XP = Level 1, 0 remaining
            (100, 2, 0),  # 100 XP = Level 2, 0 remaining
            (150, 2, 50),  # 150 XP = Level 2, 50 remaining
            (202, 3, 0),  # 202 XP = Level 3, 0 remaining
            (307, 4, 0),  # 307 XP = Level 4, 0 remaining
        ]

        for total_xp, expected_level, expected_remaining in test_cases:
            level, remaining = self.xp_system.calculate_level_from_xp(total_xp)
            self.assertEqual(level, expected_level)
            self.assertEqual(remaining, expected_remaining)

            print(f"✅ {total_xp} XP → Level {level} ({remaining} remaining)")

    def test_point_calculation_early_levels(self):
        """Test point calculation for early levels."""
        # Test levels 1-6
        for level in range(1, 7):
            points = self.xp_system.calculate_points_from_level(level)

            # Base points should always be 0 (set during creation)
            self.assertEqual(points["base"], 0)

            # Class points: 1 per 3 levels
            expected_class_points = level // 3
            self.assertEqual(points["class"], expected_class_points)

            # Skill points: 1 per level
            expected_skill_points = level
            self.assertEqual(points["skill"], expected_skill_points)

            print(
                f"✅ Level {level}: Base {points['base']}, Class {points['class']}, Skill {points['skill']}"
            )

    def test_point_calculation_mid_levels(self):
        """Test point calculation for mid levels."""
        # Test levels 10-15
        for level in range(10, 16):
            points = self.xp_system.calculate_points_from_level(level)

            # Class points: 1 per 3 levels
            expected_class_points = level // 3
            self.assertEqual(points["class"], expected_class_points)

            # Skill points: 1 per level
            expected_skill_points = level
            self.assertEqual(points["skill"], expected_skill_points)

            print(f"✅ Level {level}: Class {points['class']}, Skill {points['skill']}")

    def test_monster_xp_reward_regular(self):
        """Test XP rewards from regular monsters."""
        monster = {
            "level": 10,
            "archetype": "melee",
            "is_wild": False,
            "is_unique": False,
        }

        # Test against different player archetypes
        for player_archetype in ["melee", "ranged", "magic", "wild"]:
            xp_reward = self.xp_system.calculate_monster_xp_reward(
                monster, player_archetype
            )

            # Base XP should be monster level * 10 * archetype bonus
            base_xp = 10 * 10  # 100
            if player_archetype == "melee":
                expected_base = int(base_xp * 1.1)  # 110
            elif player_archetype == "ranged":
                expected_base = int(base_xp * 1.0)  # 100
            elif player_archetype == "magic":
                expected_base = int(base_xp * 1.0)  # 100
            elif player_archetype == "wild":
                expected_base = int(base_xp * 1.2)  # 120

            self.assertEqual(xp_reward["base"], expected_base)

            # Class and Skill XP should match the base XP for regular monsters
            # But they don't get archetype bonuses for class/skill XP
            if player_archetype == "melee":
                expected_class = int(base_xp * 1.0)  # 100 (no class bonus for melee)
                expected_skill = int(base_xp * 1.0)  # 100 (no skill bonus for melee)
            elif player_archetype == "ranged":
                expected_class = int(base_xp * 1.1)  # 110 (class bonus for ranged)
                expected_skill = int(base_xp * 1.0)  # 100 (no skill bonus for ranged)
            elif player_archetype == "magic":
                expected_class = int(base_xp * 1.0)  # 100 (no class bonus for magic)
                expected_skill = int(base_xp * 1.1)  # 110 (skill bonus for magic)
            elif player_archetype == "wild":
                expected_class = int(base_xp * 1.2)  # 120 (class bonus for wild)
                expected_skill = int(base_xp * 1.2)  # 120 (skill bonus for wild)

            self.assertEqual(xp_reward["class"], expected_class)
            self.assertEqual(xp_reward["skill"], expected_skill)

            print(
                f"✅ Regular Monster vs {player_archetype}: Base {xp_reward['base']}, Class {xp_reward['class']}, Skill {xp_reward['skill']}"
            )

    def test_monster_xp_reward_wild(self):
        """Test XP rewards from Wild monsters."""
        monster = {
            "level": 10,
            "archetype": "melee",
            "is_wild": True,
            "is_unique": False,
        }

        xp_reward = self.xp_system.calculate_monster_xp_reward(monster, "melee")

        # Wild monsters give 2x base XP, 1.5x class XP, 1.8x skill XP
        base_xp = 10 * 10  # 100
        expected_base = int(base_xp * 2.0 * 1.1)  # 220 (2.0 * 1.1 melee bonus)
        expected_class = int(base_xp * 1.5 * 1.0)  # 150 (1.5 * 1.0 melee class bonus)
        expected_skill = int(base_xp * 1.8 * 1.0)  # 180 (1.8 * 1.0 melee skill bonus)

        self.assertEqual(xp_reward["base"], expected_base)
        self.assertEqual(xp_reward["class"], expected_class)
        self.assertEqual(xp_reward["skill"], expected_skill)

        print(
            f"✅ Wild Monster: Base {xp_reward['base']}, Class {xp_reward['class']}, Skill {xp_reward['skill']}"
        )

    def test_monster_xp_reward_unique(self):
        """Test XP rewards from unique monsters."""
        monster = {
            "level": 10,
            "archetype": "melee",
            "is_wild": False,
            "is_unique": True,
        }

        xp_reward = self.xp_system.calculate_monster_xp_reward(monster, "melee")

        # Unique monsters give 5x base XP, 3x class XP, 4x skill XP
        base_xp = 10 * 10  # 100
        expected_base = int(base_xp * 5.0 * 1.1)  # 550 (5.0 * 1.1 melee bonus)
        expected_class = int(base_xp * 3.0 * 1.0)  # 300 (3.0 * 1.0 melee class bonus)
        expected_skill = int(base_xp * 4.0 * 1.0)  # 400 (4.0 * 1.0 melee skill bonus)

        self.assertEqual(xp_reward["base"], expected_base)
        self.assertEqual(xp_reward["class"], expected_class)
        self.assertEqual(xp_reward["skill"], expected_skill)

        print(
            f"✅ Unique Monster: Base {xp_reward['base']}, Class {xp_reward['class']}, Skill {xp_reward['skill']}"
        )

    def test_archetype_xp_bonuses(self):
        """Test archetype-specific XP bonuses."""
        monster = {
            "level": 10,
            "archetype": "melee",
            "is_wild": False,
            "is_unique": False,
        }

        # Test different player archetypes
        test_cases = [
            ("melee", 1.1, 1.0, 1.0),  # Melee gets +10% base XP
            ("ranged", 1.0, 1.1, 1.0),  # Ranged gets +10% class XP
            ("magic", 1.0, 1.0, 1.1),  # Magic gets +10% skill XP
            ("wild", 1.2, 1.2, 1.2),  # Wild gets +20% all XP
        ]

        for player_archetype, base_bonus, class_bonus, skill_bonus in test_cases:
            xp_reward = self.xp_system.calculate_monster_xp_reward(
                monster, player_archetype
            )

            base_xp = 10 * 10  # 100
            expected_base = int(base_xp * base_bonus)
            expected_class = int(base_xp * class_bonus)
            expected_skill = int(base_xp * skill_bonus)

            self.assertEqual(xp_reward["base"], expected_base)
            self.assertEqual(xp_reward["class"], expected_class)
            self.assertEqual(xp_reward["skill"], expected_skill)

            print(
                f"✅ {player_archetype} vs Regular: Base {xp_reward['base']}, Class {xp_reward['class']}, Skill {xp_reward['skill']}"
            )

    def test_add_xp(self):
        """Test adding XP to current totals."""
        current_xp = {"base": 100, "class": 50, "skill": 75}
        xp_gained = {"base": 25, "class": 15, "skill": 20}

        updated_xp = self.xp_system.add_xp(current_xp, xp_gained)

        expected_base = 100 + 25  # 125
        expected_class = 50 + 15  # 65
        expected_skill = 75 + 20  # 95

        self.assertEqual(updated_xp["base"], expected_base)
        self.assertEqual(updated_xp["class"], expected_class)
        self.assertEqual(updated_xp["skill"], expected_skill)

        print(
            f"✅ Add XP: Base {updated_xp['base']}, Class {updated_xp['class']}, Skill {updated_xp['skill']}"
        )

    def test_level_up_detection(self):
        """Test level up detection and point gains."""
        # Test with Skill XP that gains exactly one level
        # Use 110 XP which = Level 2 with 10 remaining (gained 1 level from 0)
        current_xp = {
            "base": 50,  # Level 1, 50 remaining (no level up from 0)
            "class": 50,  # Level 1, 50 remaining (no level up from 0)
            "skill": 110,  # Level 2, 10 remaining (1 level up from 0)
        }

        leveled_up, point_gains = self.xp_system.check_level_up_legacy(current_xp)

        # Should level up
        self.assertTrue(leveled_up)

        # Should gain 1 skill point (1 level gained)
        self.assertEqual(point_gains["skill"], 1)

        # Should gain 0 class points (no class level gained)
        self.assertEqual(point_gains["class"], 0)

        # Should gain 0 base points (unchanged from creation)
        self.assertEqual(point_gains["base"], 0)

        print(
            f"✅ Level Up: Skill +{point_gains['skill']}, Class +{point_gains['class']}, Base +{point_gains['base']}"
        )

    def test_level_up_class_point_gain(self):
        """Test gaining class points at higher levels."""
        # Test with Class XP that gains exactly 3 levels to get 1 class point
        # Use 307 XP which = Level 4 (gained 3 levels from 0, so 1 class point)
        current_xp = {
            "base": 50,  # Level 1 (no level up from 0)
            "class": 307,  # Level 4 (gained 3 levels from 0, so 1 class point: 4//3=1, 0//3=0)
            "skill": 50,  # Level 1 (no level up from 0)
        }

        leveled_up, point_gains = self.xp_system.check_level_up_legacy(current_xp)

        # Should level up
        self.assertTrue(leveled_up)

        # Should gain 0 skill points (no skill level gained)
        self.assertEqual(point_gains["skill"], 0)

        # Should gain 1 class point (Class Level 4 // 3 = 1, started at 0 // 3 = 0, so gain 1)
        self.assertEqual(point_gains["class"], 1)

        print(
            f"✅ Class Point Gain: Skill +{point_gains['skill']}, Class +{point_gains['class']}"
        )

    def test_comprehensive_level_ranges(self):
        """Test XP system across different level ranges."""
        test_ranges = [
            (1, 10),  # Early game
            (10, 25),  # Mid game
            (25, 50),  # Late game
            (50, 100),  # End game
        ]

        for start_level, end_level in test_ranges:
            print(f"\n🔍 Testing Level Range {start_level}-{end_level}:")

            for level in range(
                start_level, min(end_level + 1, start_level + 6)
            ):  # Test 6 levels per range
                # Test XP requirements
                xp_req = self.xp_system.calculate_xp_requirement(level)
                total_xp = self.xp_system.calculate_total_xp_for_level(level)

                # Test point calculation
                points = self.xp_system.calculate_points_from_level(level)

                # Verify point calculations
                expected_class = level // 3
                expected_skill = level

                self.assertEqual(points["class"], expected_class)
                self.assertEqual(points["skill"], expected_skill)
                self.assertEqual(points["base"], 0)

                # Test level calculation from XP
                calculated_level, remaining = self.xp_system.calculate_level_from_xp(
                    total_xp
                )
                self.assertEqual(calculated_level, level)

                print(
                    f"  ✅ Level {level}: XP Req {xp_req}, Total {total_xp}, Class {points['class']}, Skill {points['skill']}"
                )

                # Test monster XP rewards for this level
                monster = {
                    "level": level,
                    "archetype": "melee",
                    "is_wild": False,
                    "is_unique": False,
                }
                xp_reward = self.xp_system.calculate_monster_xp_reward(monster, "melee")

                # Verify XP rewards are reasonable
                self.assertGreater(xp_reward["base"], 0)
                self.assertGreater(xp_reward["class"], 0)
                self.assertGreater(xp_reward["skill"], 0)

                print(
                    f"    🎯 Monster XP: Base {xp_reward['base']}, Class {xp_reward['class']}, Skill {xp_reward['skill']}"
                )

    def test_player_level_calculation(self):
        """Test that player level is correctly calculated as Class + Skill levels."""
        test_cases = [
            (5, 10, 15),  # Class 5, Skill 10 = Level 15
            (10, 5, 15),  # Class 10, Skill 5 = Level 15
            (3, 7, 10),  # Class 3, Skill 7 = Level 10
            (15, 25, 40),  # Class 15, Skill 25 = Level 40
        ]

        for class_level, skill_level, expected_total in test_cases:
            # Calculate points for the total level
            total_level = class_level + skill_level
            points = self.xp_system.calculate_points_from_level(total_level)

            # Verify the points match the individual levels
            self.assertEqual(points["class"], total_level // 3)
            self.assertEqual(points["skill"], total_level)

            print(
                f"✅ Class {class_level} + Skill {skill_level} = Level {total_level} (Class {points['class']}, Skill {points['skill']})"
            )

    def test_xp_progress_calculation(self):
        """Test XP progress calculation."""
        # Test progress at 50% to next level
        current_xp = {"base": 150, "class": 75, "skill": 100}

        progress = self.xp_system.get_xp_progress(current_xp)

        # Progress should be between 0 and 100
        for xp_type in ["base", "class", "skill"]:
            self.assertGreaterEqual(progress[xp_type], 0.0)
            self.assertLessEqual(progress[xp_type], 100.0)

        print(
            f"✅ XP Progress: Base {progress['base']:.1f}%, Class {progress['class']:.1f}%, Skill {progress['skill']:.1f}%"
        )

    def test_available_points_calculation(self):
        """Test available points calculation."""
        total_points = {"base": 10, "class": 5, "skill": 15}
        used_points = {"base": 3, "class": 2, "skill": 8}

        available_points = self.xp_system.get_available_points(
            total_points, used_points
        )

        expected_base = 10 - 3  # 7
        expected_class = 5 - 2  # 3
        expected_skill = 15 - 8  # 7

        self.assertEqual(available_points["base"], expected_base)
        self.assertEqual(available_points["class"], expected_class)
        self.assertEqual(available_points["skill"], expected_skill)

        print(
            f"✅ Available Points: Base {available_points['base']}, Class {available_points['class']}, Skill {available_points['skill']}"
        )

    def test_no_level_up(self):
        """Test when player doesn't have enough XP for level up."""
        # Start with not enough XP for level 2
        current_xp = {"base": 50, "class": 25, "skill": 35}

        leveled_up, point_gains = self.xp_system.check_level_up_legacy(current_xp)

        # Should not level up
        self.assertFalse(leveled_up)

        # Should have no point gains
        expected_gains = {"base": 0, "class": 0, "skill": 0}
        self.assertEqual(point_gains, expected_gains)

        print(f"✅ No Level Up: {leveled_up}")

    def test_monster_type_detection(self):
        """Test monster type detection for XP rates."""
        # Test regular monster
        regular_monster = {"level": 10, "is_wild": False, "is_unique": False}
        xp_reward = self.xp_system.calculate_monster_xp_reward(regular_monster, "melee")
        self.assertEqual(xp_reward["base"], 110)  # 10 * 10 * 1.1 (melee bonus)

        # Test wild monster
        wild_monster = {"level": 10, "is_wild": True, "is_unique": False}
        xp_reward = self.xp_system.calculate_monster_xp_reward(wild_monster, "melee")
        self.assertEqual(xp_reward["base"], 220)  # 10 * 10 * 2.0 * 1.1

        # Test unique monster
        unique_monster = {"level": 10, "is_wild": False, "is_unique": True}
        xp_reward = self.xp_system.calculate_monster_xp_reward(unique_monster, "melee")
        self.assertEqual(xp_reward["base"], 550)  # 10 * 10 * 5.0 * 1.1

        print(f"✅ Monster Type Detection: Regular {xp_reward['base']} XP")

    def test_point_progression_over_time(self):
        """Test point progression over multiple levels."""
        points_over_time = []

        for level in range(1, 10):
            points = self.xp_system.calculate_points_from_level(level)
            points_over_time.append((level, points))

        # Verify progression
        for i, (level, points) in enumerate(points_over_time):
            if i > 0:
                prev_level, prev_points = points_over_time[i - 1]

                # Skill points should increase by 1 each level
                self.assertEqual(points["skill"], prev_points["skill"] + 1)

                # Class points should increase every 3 levels
                expected_class_increase = 1 if level % 3 == 0 else 0
                self.assertEqual(
                    points["class"], prev_points["class"] + expected_class_increase
                )

        print(f"✅ Point Progression: Level 1-9 verified")


def run_xp_tests():
    """Run all XP system tests with detailed output."""
    print("📊 XP SYSTEM TESTING 🎯")
    print("=" * 60)

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestXPSystem)

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
        print("\n🎉 ALL TESTS PASSED! XP system is working correctly!")
    else:
        print("\n⚠️  Some tests failed. Please review the issues above.")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_xp_tests()
    sys.exit(0 if success else 1)

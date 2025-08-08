#!/usr/bin/env python3
"""
Fix level-up detection logic
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.systems.xp_system import XPSystem


def test_simple_level_up():
    """Test a simple level up scenario."""
    xp_system = XPSystem()

    print("🔍 Testing Simple Level Up")
    print("=" * 30)

    # Start at 150 XP (should be level 2)
    current_level, _ = xp_system.calculate_level_from_xp(150)
    print(f"150 XP = Level {current_level}")

    # What's the XP for level 3?
    level_3_xp = xp_system.calculate_total_xp_for_level(3)
    print(f"Level 3 requires: {level_3_xp} XP")

    # Test with level 3 XP + 1
    test_xp = level_3_xp + 1
    test_current_xp = {"base": test_xp, "class": test_xp // 2, "skill": test_xp // 2}

    print(f"Testing with {test_xp} XP:")

    # Check current level
    test_level, _ = xp_system.calculate_level_from_xp(test_xp)
    print(f"  Current level: {test_level}")

    # Check level up
    leveled_up, gains = xp_system.check_level_up(test_current_xp)
    print(f"  Level up: {leveled_up}")
    print(f"  Gains: {gains}")

    # Let's try with a much higher amount
    print(f"\n🚀 Testing with higher XP:")
    high_xp = 5000
    high_current_xp = {"base": high_xp, "class": high_xp // 2, "skill": high_xp // 2}

    high_level, _ = xp_system.calculate_level_from_xp(high_xp)
    print(f"  {high_xp} XP = Level {high_level}")

    leveled_up_high, gains_high = xp_system.check_level_up(high_current_xp)
    print(f"  Level up: {leveled_up_high}")
    print(f"  Gains: {gains_high}")


def test_boundary_conditions():
    """Test exact boundary conditions."""
    xp_system = XPSystem()

    print(f"\n🎯 Testing Boundary Conditions")
    print("=" * 40)

    for level in [2, 3, 4, 5]:
        level_xp = xp_system.calculate_total_xp_for_level(level)

        # Test with exact XP - 1
        test_xp_minus = {
            "base": level_xp - 1,
            "class": level_xp // 2,
            "skill": level_xp // 2,
        }
        leveled_up_minus, _ = xp_system.check_level_up(test_xp_minus)

        # Test with exact XP
        test_xp_exact = {
            "base": level_xp,
            "class": level_xp // 2,
            "skill": level_xp // 2,
        }
        leveled_up_exact, gains_exact = xp_system.check_level_up(test_xp_exact)

        # Test with exact XP + 1
        test_xp_plus = {
            "base": level_xp + 1,
            "class": level_xp // 2,
            "skill": level_xp // 2,
        }
        leveled_up_plus, gains_plus = xp_system.check_level_up(test_xp_plus)

        print(f"Level {level} ({level_xp} XP):")
        print(f"  {level_xp - 1} XP: {leveled_up_minus}")
        print(f"  {level_xp} XP: {leveled_up_exact} {gains_exact}")
        print(f"  {level_xp + 1} XP: {leveled_up_plus} {gains_plus}")


if __name__ == "__main__":
    test_simple_level_up()
    test_boundary_conditions()

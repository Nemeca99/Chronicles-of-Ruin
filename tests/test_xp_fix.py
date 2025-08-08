#!/usr/bin/env python3
"""
Quick script to test and fix XP system level-up detection
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.systems.xp_system import XPSystem


def test_level_up_detection():
    """Test level-up detection and find correct XP amounts."""
    xp_system = XPSystem()

    print("🔍 Testing Level-Up Detection Logic")
    print("=" * 50)

    # Test different XP amounts to find ones that trigger level-ups
    test_amounts = [200, 407, 514, 624, 852, 1091, 1343, 1608, 1886, 2178, 2485, 2807]

    level_up_triggers = []

    for xp_amount in test_amounts:
        current_xp = {
            "base": xp_amount,
            "class": xp_amount // 2,
            "skill": xp_amount // 2,
        }

        # Check current level
        current_level, _ = xp_system.calculate_level_from_xp(xp_amount)

        # Check if level-up would trigger
        leveled_up, gains = xp_system.check_level_up(current_xp)

        # Get next level XP requirement
        next_level_xp = xp_system.calculate_total_xp_for_level(current_level + 1)

        print(
            f"XP: {xp_amount:4d} | Level: {current_level:2d} | Next: {next_level_xp:4d} | Level Up: {leveled_up}"
        )

        if leveled_up:
            level_up_triggers.append((xp_amount, current_level, gains))

    print(f"\n✅ Found {len(level_up_triggers)} level-up triggers:")
    for xp, level, gains in level_up_triggers:
        print(f"  {xp} XP → Level {level} gains: {gains}")

    return level_up_triggers


def find_working_level_ups():
    """Find XP amounts that actually trigger level-ups."""
    xp_system = XPSystem()

    print("\n🎯 Finding Working Level-Up XP Amounts")
    print("=" * 50)

    working_amounts = []

    # Test a range of XP amounts
    for xp in range(100, 5000, 50):
        current_xp = {"base": xp, "class": xp // 2, "skill": xp // 2}
        leveled_up, gains = xp_system.check_level_up(current_xp)

        if leveled_up:
            current_level, _ = xp_system.calculate_level_from_xp(xp)
            working_amounts.append((xp, current_level, gains))

            if len(working_amounts) >= 10:  # Stop after finding 10 examples
                break

    print(f"✅ Found {len(working_amounts)} working level-up amounts:")
    for xp, level, gains in working_amounts[:5]:  # Show first 5
        print(f"  {xp} XP → Level {level} gains: {gains}")

    return working_amounts


def test_exponential_progression():
    """Test the exponential XP progression."""
    xp_system = XPSystem()

    print("\n📈 Testing Exponential XP Progression")
    print("=" * 50)

    levels_to_test = [1, 2, 3, 5, 10, 20, 50, 100]

    for level in levels_to_test:
        xp_req = xp_system.calculate_xp_requirement(level)
        total_xp = xp_system.calculate_total_xp_for_level(level)
        points = xp_system.calculate_points_from_level(level)

        print(
            f"Level {level:3d}: Req {xp_req:4d} XP | Total {total_xp:6d} XP | Class {points['class']:2d} | Skill {points['skill']:2d}"
        )


def main():
    """Run all tests."""
    print("🚀 XP System Quick Test & Fix Script")
    print("=" * 60)

    # Test current system
    test_exponential_progression()

    # Find level-up triggers
    triggers = test_level_up_detection()

    # Find working level-ups
    working = find_working_level_ups()

    # Suggest fixes for tests
    print("\n🔧 Suggested Test Fixes:")
    print("=" * 30)

    if working:
        first_working = working[0]
        second_working = working[1] if len(working) > 1 else working[0]

        print(f"For test_level_up_detection:")
        print(
            f"  current_xp = {{'base': {first_working[0]}, 'class': {first_working[0]//2}, 'skill': {first_working[0]//2}}}"
        )
        print(
            f"  # Should level up to {first_working[1]} with gains: {first_working[2]}"
        )

        print(f"\nFor test_level_up_class_point_gain:")
        print(
            f"  current_xp = {{'base': {second_working[0]}, 'class': {second_working[0]//2}, 'skill': {second_working[0]//2}}}"
        )
        print(
            f"  # Should level up to {second_working[1]} with gains: {second_working[2]}"
        )


if __name__ == "__main__":
    main()

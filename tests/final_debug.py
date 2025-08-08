#!/usr/bin/env python3
"""
Final debug of level-up detection
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.systems.xp_system import XPSystem


def debug_exact_scenario():
    """Debug the exact level-up scenario."""
    xp_system = XPSystem()

    print("🔍 Final Debug of Level-Up Detection")
    print("=" * 50)

    # Test scenario: Player has 200 XP (level 2), should level up to level 3
    test_xp = {"base": 200, "class": 100, "skill": 100}

    print(f"Testing scenario: {test_xp}")

    # Step by step debug
    current_level, remaining = xp_system.calculate_level_from_xp(test_xp["base"])
    print(
        f"1. Current level from {test_xp['base']} XP: {current_level} (remaining: {remaining})"
    )

    current_points = xp_system.calculate_points_from_level(current_level)
    print(f"2. Current points at level {current_level}: {current_points}")

    next_level_xp = xp_system.calculate_total_xp_for_level(current_level + 1)
    print(f"3. XP needed for level {current_level + 1}: {next_level_xp}")

    has_enough = test_xp["base"] >= next_level_xp
    print(f"4. Has enough XP? {test_xp['base']} >= {next_level_xp} = {has_enough}")

    if has_enough:
        new_level = current_level + 1
        new_points = xp_system.calculate_points_from_level(new_level)
        print(f"5. New level: {new_level}, New points: {new_points}")

        point_gains = {}
        for point_type in ["base", "class", "skill"]:
            point_gains[point_type] = (
                new_points[point_type] - current_points[point_type]
            )
        print(f"6. Point gains: {point_gains}")

    # Call the actual function
    leveled_up, gains = xp_system.check_level_up(test_xp)
    print(f"7. Actual function result: leveled_up={leveled_up}, gains={gains}")

    print(f"\n🎯 Let's test level progression:")
    for xp in [100, 200, 302, 407, 514]:
        level, rem = xp_system.calculate_level_from_xp(xp)
        total_for_level = xp_system.calculate_total_xp_for_level(level)
        print(f"  {xp} XP → Level {level} (total for level {level}: {total_for_level})")


if __name__ == "__main__":
    debug_exact_scenario()

#!/usr/bin/env python3
"""
Debug level-up detection logic
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.systems.xp_system import XPSystem


def debug_level_up_logic():
    """Debug the level-up detection step by step."""
    xp_system = XPSystem()

    print("🔍 Debugging Level-Up Detection Logic")
    print("=" * 50)

    # Test with 1343 XP (should be Level 13)
    test_xp = {"base": 1343, "class": 671, "skill": 672}

    print(f"Testing with XP: {test_xp}")

    # Step 1: Calculate current level from base XP
    current_level, remaining = xp_system.calculate_level_from_xp(test_xp.get("base", 0))
    print(f"Current level from base XP: {current_level} (remaining: {remaining})")

    # Step 2: Calculate points at current level
    current_points = xp_system.calculate_points_from_level(current_level)
    print(f"Current points: {current_points}")

    # Step 3: Check XP for next level
    next_level_xp = xp_system.calculate_total_xp_for_level(current_level + 1)
    print(f"XP needed for level {current_level + 1}: {next_level_xp}")

    # Step 4: Check if we have enough XP
    has_enough = test_xp.get("base", 0) >= next_level_xp
    print(f"Current base XP: {test_xp.get('base', 0)}")
    print(f"Has enough XP for next level: {has_enough}")

    # Step 5: Call the actual function
    leveled_up, point_gains = xp_system.check_level_up(test_xp)
    print(f"Level up result: {leveled_up}")
    print(f"Point gains: {point_gains}")

    # Let's also test what happens at the exact boundary
    print(f"\n🎯 Testing at exact boundary:")
    exact_xp = {
        "base": next_level_xp,
        "class": next_level_xp // 2,
        "skill": next_level_xp // 2,
    }
    print(f"Testing with XP: {exact_xp}")

    leveled_up_exact, gains_exact = xp_system.check_level_up(exact_xp)
    print(f"Level up result: {leveled_up_exact}")
    print(f"Point gains: {gains_exact}")


def test_multiple_boundaries():
    """Test level-up detection at multiple level boundaries."""
    xp_system = XPSystem()

    print(f"\n📊 Testing Multiple Level Boundaries")
    print("=" * 50)

    for level in range(2, 11):  # Test levels 2-10
        # Get exact XP needed for this level
        level_xp = xp_system.calculate_total_xp_for_level(level)

        # Test with exact XP
        test_xp = {"base": level_xp, "class": level_xp // 2, "skill": level_xp // 2}
        leveled_up, gains = xp_system.check_level_up(test_xp)

        print(
            f"Level {level} ({level_xp} XP): Level up = {leveled_up}, Gains = {gains}"
        )


if __name__ == "__main__":
    debug_level_up_logic()
    test_multiple_boundaries()

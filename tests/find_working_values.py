#!/usr/bin/env python3
"""
Find working XP values for level-up tests
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.systems.xp_system import XPSystem


def find_working_levelups():
    """Find XP amounts that actually trigger level-ups."""
    xp_system = XPSystem()

    print("🔍 Finding Working Level-Up Values")
    print("=" * 50)

    working_values = []

    # Test different XP amounts
    for test_xp in range(300, 1000, 10):
        current_level, _ = xp_system.calculate_level_from_xp(test_xp)
        next_level_xp = xp_system.calculate_total_xp_for_level(current_level + 1)

        test_current_xp = {
            "base": test_xp,
            "class": test_xp // 2,
            "skill": test_xp // 2,
        }
        leveled_up, gains = xp_system.check_level_up(test_current_xp)

        if leveled_up:
            working_values.append((test_xp, current_level, gains))
            print(
                f"✅ {test_xp} XP: Level {current_level} → Level {current_level + 1}, Gains: {gains}"
            )

            if len(working_values) >= 5:  # Find 5 working examples
                break

    if not working_values:
        print("❌ No working level-ups found!")
        print("Let me check a specific example:")

        # Check a specific case: Player at level 2 with enough XP for level 3
        level_2_xp = xp_system.calculate_total_xp_for_level(2)  # 200 XP
        level_3_xp = xp_system.calculate_total_xp_for_level(3)  # 302 XP

        print(f"Level 2 requires: {level_2_xp} XP")
        print(f"Level 3 requires: {level_3_xp} XP")

        # Test with a player who has level 2 XP but needs to level up to 3
        test_cases = [
            level_2_xp + 1,  # Just over level 2
            level_3_xp - 1,  # Just under level 3
            level_3_xp,  # Exactly level 3
            level_3_xp + 1,  # Just over level 3
        ]

        for test_xp in test_cases:
            current_level, remaining = xp_system.calculate_level_from_xp(test_xp)
            test_current_xp = {
                "base": test_xp,
                "class": test_xp // 2,
                "skill": test_xp // 2,
            }
            leveled_up, gains = xp_system.check_level_up(test_current_xp)

            print(
                f"  {test_xp} XP: Level {current_level} (remaining: {remaining}), Level up: {leveled_up}"
            )

    return working_values


if __name__ == "__main__":
    working = find_working_levelups()

    if working:
        print(f"\n🎯 Use these values in tests:")
        for i, (xp, level, gains) in enumerate(working[:2]):
            test_name = (
                "test_level_up_detection"
                if i == 0
                else "test_level_up_class_point_gain"
            )
            print(f"{test_name}:")
            print(
                f"  current_xp = {{'base': {xp}, 'class': {xp//2}, 'skill': {xp//2}}}"
            )
            print(f"  # Gains: {gains}")

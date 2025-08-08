"""
XP System - Chronicles of Ruin: Sunderfall

This module implements the experience point system including Base Points (unchanged),
Class Points (1 per 3 levels), Skill Points (1 per level), and monster XP rates.
"""

import math
from typing import Dict, List, Tuple, Optional
from enum import Enum


class XPType(Enum):
    """Types of experience points."""

    BASE = "base"  # Unchanged from creation
    CLASS = "class"  # 1 per 3 levels
    SKILL = "skill"  # 1 per level


class XPSystem:
    """
    XP System for Chronicles of Ruin: Sunderfall

    Handles all XP calculations, point allocation, and level progression.
    Uses exponential growth: 100 XP base, 1.025x multiplier per level.
    """

    def __init__(self):
        """Initialize the XP system."""
        self.base_xp_per_level = 100  # Starting XP requirement
        self.xp_multiplier = 1.025  # Multiplier per level
        self.max_level = 100  # Maximum player level

        # Archetype XP bonuses
        self.archetype_bonuses = {
            "melee": {"base": 1.1, "class": 1.0, "skill": 1.0},  # +10% base XP
            "ranged": {"base": 1.0, "class": 1.1, "skill": 1.0},  # +10% class XP
            "magic": {"base": 1.0, "class": 1.0, "skill": 1.1},  # +10% skill XP
            "wild": {"base": 1.2, "class": 1.2, "skill": 1.2},  # +20% all XP
        }

        # Monster type XP multipliers
        self.monster_type_multipliers = {
            "regular": {"base": 1.0, "class": 1.0, "skill": 1.0},
            "wild": {"base": 2.0, "class": 1.5, "skill": 1.8},  # Wild monsters
            "unique": {"base": 5.0, "class": 3.0, "skill": 4.0},  # Unique monsters
        }

    def calculate_xp_requirement(self, level: int) -> int:
        """
        Calculate XP required to level up from the given level.

        Args:
            level: Current level (1-based)

        Returns:
            XP required to reach next level
        """
        if level <= 0:
            return self.base_xp_per_level

        # Level 1 needs base_xp_per_level (100) to reach Level 2
        # Each subsequent level needs 1.025x more than the previous
        # Level 1→2: 100 XP
        # Level 2→3: 100 * 1.025 = 102 XP
        # Level 3→4: 102 * 1.025 = 105 XP (rounded)
        xp_required = int(self.base_xp_per_level * (self.xp_multiplier ** (level - 1)))
        return xp_required

    def calculate_total_xp_for_level(self, level: int) -> int:
        """
        Calculate total XP required to reach a specific level.

        Args:
            level: Target level

        Returns:
            Total XP required
        """
        if level <= 1:
            return 0

        total_xp = 0
        for current_level in range(1, level):
            # XP needed to go from current_level to current_level + 1
            xp_needed = self.calculate_xp_requirement(current_level)
            total_xp += xp_needed
        return total_xp

    def calculate_level_from_xp(self, total_xp: int) -> Tuple[int, int]:
        """
        Calculate current level and remaining XP from total XP.

        Args:
            total_xp: Total experience points (resets to 0 each level)

        Returns:
            Tuple of (current_level, remaining_xp_toward_next_level)
        """
        if total_xp <= 0:
            return 1, 0

        # Start at level 1
        current_level = 1
        remaining_xp = total_xp

        # Keep leveling up while we have enough XP
        while True:
            xp_needed_for_next_level = self.calculate_xp_requirement(current_level)

            # If we don't have enough XP to level up, we're at current level
            if remaining_xp < xp_needed_for_next_level:
                break

            # Level up! Subtract the XP cost and increase level
            remaining_xp -= xp_needed_for_next_level
            current_level += 1

        return current_level, remaining_xp

    def calculate_points_from_level(self, level: int) -> Dict[str, int]:
        """
        Calculate points available at a given level.

        Args:
            level: Player level (sum of Class + Skill levels)

        Returns:
            Dictionary with point counts
        """
        # Base points are set during character creation and don't change
        base_points = 0

        # Class points: 1 per 3 levels
        class_points = level // 3

        # Skill points: 1 per level
        skill_points = level

        return {"base": base_points, "class": class_points, "skill": skill_points}

    def calculate_points_from_xp(self, current_xp: Dict[str, int]) -> Dict[str, int]:
        """
        Calculate points available from current XP totals.

        Args:
            current_xp: Current XP totals for base, class, and skill

        Returns:
            Dictionary with point counts
        """
        # Calculate levels from each XP pool
        class_xp = current_xp.get("class", 0)
        skill_xp = current_xp.get("skill", 0)

        class_level, _ = self.calculate_level_from_xp(class_xp)
        skill_level, _ = self.calculate_level_from_xp(skill_xp)

        # Base points are set during character creation and don't change
        base_points = 0

        # Class points: 1 per 3 class levels
        class_points = class_level // 3

        # Skill points: 1 per skill level
        skill_points = skill_level

        return {"base": base_points, "class": class_points, "skill": skill_points}

    def calculate_monster_xp_reward(
        self, monster_data: Dict, player_archetype: str
    ) -> Dict[str, int]:
        """
        Calculate XP reward from defeating a monster.

        Args:
            monster_data: Monster information
            player_archetype: Player's archetype

        Returns:
            Dictionary with XP rewards for each type
        """
        monster_level = monster_data.get("level", 1)
        base_xp = monster_level * 10

        # Determine monster type for multipliers
        monster_type = self._determine_monster_type(monster_data)
        type_multipliers = self.monster_type_multipliers[monster_type]

        # Get archetype bonuses
        archetype_bonuses = self.archetype_bonuses.get(
            player_archetype, {"base": 1.0, "class": 1.0, "skill": 1.0}
        )

        # Calculate XP rewards
        xp_reward = {}
        for xp_type in ["base", "class", "skill"]:
            # Apply monster type multiplier and archetype bonus
            multiplier = type_multipliers[xp_type] * archetype_bonuses[xp_type]
            xp_reward[xp_type] = int(base_xp * multiplier)

        return xp_reward

    def _determine_monster_type(self, monster_data: Dict) -> str:
        """Determine monster type for XP rate calculation."""
        if monster_data.get("is_unique", False):
            return "unique"
        elif monster_data.get("is_wild", False):
            return "wild"
        elif monster_data.get("classification") == "boss":
            return "boss"
        else:
            return "regular"

    def add_xp(
        self, current_xp: Dict[str, int], xp_gained: Dict[str, int]
    ) -> Dict[str, int]:
        """
        Add XP to current totals.

        Args:
            current_xp: Current XP totals
            xp_gained: XP gained from monster defeat

        Returns:
            Updated XP totals
        """
        updated_xp = current_xp.copy()

        for xp_type in XPType:
            xp_type_str = xp_type.value
            updated_xp[xp_type_str] = updated_xp.get(xp_type_str, 0) + xp_gained.get(
                xp_type_str, 0
            )

        return updated_xp

    def check_level_up(
        self, old_xp: Dict[str, int], new_xp: Dict[str, int]
    ) -> Tuple[bool, Dict[str, int]]:
        """
        Check if player should level up when gaining XP.

        Args:
            old_xp: XP totals before gaining XP
            new_xp: XP totals after gaining XP

        Returns:
            Tuple of (leveled_up, point_gains)
        """
        # Calculate levels before and after XP gain
        old_base_level, _ = self.calculate_level_from_xp(old_xp.get("base", 0))
        old_class_level, _ = self.calculate_level_from_xp(old_xp.get("class", 0))
        old_skill_level, _ = self.calculate_level_from_xp(old_xp.get("skill", 0))

        new_base_level, _ = self.calculate_level_from_xp(new_xp.get("base", 0))
        new_class_level, _ = self.calculate_level_from_xp(new_xp.get("class", 0))
        new_skill_level, _ = self.calculate_level_from_xp(new_xp.get("skill", 0))

        # Check if any levels increased
        leveled_up = (
            new_base_level > old_base_level
            or new_class_level > old_class_level
            or new_skill_level > old_skill_level
        )

        # Calculate point gains
        point_gains = {"base": 0, "class": 0, "skill": 0}

        # Base points don't change (set during character creation)
        point_gains["base"] = 0

        # Class points: 1 per 3 class levels
        old_class_points = old_class_level // 3
        new_class_points = new_class_level // 3
        point_gains["class"] = new_class_points - old_class_points

        # Skill points: 1 per skill level
        point_gains["skill"] = new_skill_level - old_skill_level

        return leveled_up, point_gains

    def check_level_up_legacy(
        self, current_xp: Dict[str, int]
    ) -> Tuple[bool, Dict[str, int]]:
        """
        Legacy level-up check for backward compatibility with tests.

        Args:
            current_xp: Current XP totals

        Returns:
            Tuple of (leveled_up, point_gains)
        """
        # For legacy tests, assume they had 0 XP before and gained current_xp
        old_xp = {"base": 0, "class": 0, "skill": 0}
        return self.check_level_up(old_xp, current_xp)

    def get_xp_progress(self, current_xp: Dict[str, int]) -> Dict[str, float]:
        """
        Calculate XP progress to next level for each type.

        Args:
            current_xp: Current XP totals

        Returns:
            Dictionary with progress percentages
        """
        progress = {}

        for xp_type in XPType:
            xp_type_str = xp_type.value
            current_xp_amount = current_xp.get(xp_type_str, 0)

            # Calculate current level and XP needed for next level
            current_level, _ = self.calculate_level_from_xp(current_xp_amount)
            xp_for_current_level = self.calculate_total_xp_for_level(current_level)
            xp_for_next_level = self.calculate_total_xp_for_level(current_level + 1)

            # Calculate progress
            xp_in_current_level = current_xp_amount - xp_for_current_level
            xp_needed_for_next = xp_for_next_level - xp_for_current_level

            if xp_needed_for_next > 0:
                progress_percentage = (xp_in_current_level / xp_needed_for_next) * 100
                # Ensure progress is between 0 and 100
                progress[xp_type_str] = max(0.0, min(100.0, progress_percentage))
            else:
                progress[xp_type_str] = 100.0

        return progress

    def get_available_points(
        self, total_points: Dict[str, int], used_points: Dict[str, int]
    ) -> Dict[str, int]:
        """
        Calculate available points for allocation.

        Args:
            total_points: Total points earned
            used_points: Points already used

        Returns:
            Dictionary with available points
        """
        available_points = {}

        for point_type in ["base", "class", "skill"]:
            total = total_points.get(point_type, 0)
            used = used_points.get(point_type, 0)
            available_points[point_type] = max(0, total - used)

        return available_points


# Example usage and testing
def test_xp_system():
    """Test the XP system with various scenarios."""
    xp_system = XPSystem()

    # Test XP requirements
    print("📊 XP REQUIREMENTS TEST:")
    print("=" * 50)

    for level in range(1, 11):
        xp_needed = xp_system.calculate_xp_requirement(level)
        total_xp = xp_system.calculate_total_xp_for_level(level)
        print(f"Level {level}: {xp_needed} XP needed, {total_xp} total XP")

    # Test point calculation
    print("\n🎯 POINT CALCULATION TEST:")
    print("=" * 50)

    for level in range(1, 16):
        points = xp_system.calculate_points_from_level(level)
        print(
            f"Level {level}: Base {points['base']}, Class {points['class']}, Skill {points['skill']}"
        )

    # Test monster XP rewards
    print("\n👹 MONSTER XP REWARDS TEST:")
    print("=" * 50)

    test_monsters = [
        {"level": 5, "archetype": "melee", "is_wild": False, "is_unique": False},
        {"level": 10, "archetype": "ranged", "is_wild": True, "is_unique": False},
        {"level": 15, "archetype": "magic", "is_wild": False, "is_unique": True},
        {"level": 20, "archetype": "wild", "is_wild": False, "is_unique": False},
    ]

    player_archetypes = ["melee", "ranged", "magic", "wild"]

    for monster in test_monsters:
        print(f"\nMonster Level {monster['level']} ({monster['archetype']}):")
        for player_archetype in player_archetypes:
            xp_reward = xp_system.calculate_monster_xp_reward(monster, player_archetype)
            print(
                f"  vs {player_archetype}: Base {xp_reward['base']}, Class {xp_reward['class']}, Skill {xp_reward['skill']}"
            )

    # Test level up mechanics
    print("\n🚀 LEVEL UP TEST:")
    print("=" * 50)

    # Simulate gaining XP
    current_xp = {"base": 0, "class": 0, "skill": 0}

    for i in range(5):
        # Gain XP from a monster
        monster = {
            "level": 5,
            "archetype": "melee",
            "is_wild": False,
            "is_unique": False,
        }
        xp_gained = xp_system.calculate_monster_xp_reward(monster, "melee")
        current_xp = xp_system.add_xp(current_xp, xp_gained)

        # Check for level up
        leveled_up, point_gains = xp_system.check_level_up(current_xp)

        current_level, remaining_xp = xp_system.calculate_level_from_xp(
            current_xp["base"]
        )
        progress = xp_system.get_xp_progress(current_xp)

        print(
            f"Step {i+1}: Level {current_level}, Base XP {current_xp['base']} ({progress['base']:.1f}%)"
        )

        if leveled_up:
            print(
                f"  🎉 LEVEL UP! Gained: Base {point_gains.get('base', 0)}, Class {point_gains.get('class', 0)}, Skill {point_gains.get('skill', 0)}"
            )


if __name__ == "__main__":
    test_xp_system()

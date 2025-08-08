"""
CHRONICLES OF RUIN: PLAYER SYSTEM
=================================

This module handles all player-related functionality for Chronicles of Ruin.
It manages player progression, stats, experience, and character data.

PURPOSE:
- Manages player character data and stats
- Handles experience and level progression
- Manages Class Points and Skill Points
- Provides player save/load functionality
- Handles player achievements and milestones

ARCHITECTURE:
- PlayerManager: Manages all player data and state
- ProgressionSystem: Handles experience and leveling
- StatsCalculator: Calculates player stats and bonuses
- SaveSystem: Handles player data persistence
- AchievementTracker: Tracks player achievements

PROGRESSION SYSTEM:
- Player Levels: Provide Skill Points for skill allocation
- Class Points: Permanent measure of character power
- Experience: Gained through combat and exploration
- Skill Points: Can be reset, used for skill progression
- Class Points: Permanent, cannot be reset

PLAYER STATS:
- Core Stats: Strength, Dexterity, Intelligence, etc.
- Combat Stats: Damage, Defense, Critical Chance, etc.
- Derived Stats: Calculated from core stats and equipment
- Status Resistances: Protection against status effects

This system provides the foundation for character progression
and ensures meaningful player advancement over time.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import json
import time
from .xp_system import XPSystem


class StatType(Enum):
    """Enumeration of player stat types."""

    # Archetype Attributes (Class Points)
    POWER = "power"           # Melee Offense
    TOUGHNESS = "toughness"   # Melee Defense vs Magic
    AGILITY = "agility"       # Ranged Offense  
    FINESSE = "finesse"       # Ranged Defense vs Melee
    KNOWLEDGE = "knowledge"   # Magic Offense
    WISDOM = "wisdom"         # Magic Defense vs Ranged
    CHAOS = "chaos"           # Wild Utility

    # Combat stats
    DAMAGE = "damage"
    DEFENSE = "defense"
    CRITICAL_CHANCE = "critical_chance"
    CRITICAL_DAMAGE = "critical_damage"
    ACCURACY = "accuracy"
    DODGE = "dodge"

    # Resource stats
    HEALTH = "health"
    MANA = "mana"
    STAMINA = "stamina"


class PlayerSystem:
    """
    Main player system that handles all player-related functionality.
    Manages character data, progression, and stats.
    """

    def __init__(self):
        """Initialize the player system."""
        self.players = {}  # player_id -> player_data
        self.xp_system = XPSystem()
        # Keep old experience table for backward compatibility
        self.experience_table = self._initialize_experience_table()
        self.stat_calculations = self._initialize_stat_calculations()

    def _initialize_experience_table(self) -> Dict[int, int]:
        """Initialize the experience required for each level."""
        table = {}
        base_exp = 100

        for level in range(1, 101):  # Levels 1-100
            if level == 1:
                table[level] = 0
            else:
                # Exponential growth: each level requires 1.5x more exp
                table[level] = int(base_exp * (1.5 ** (level - 2)))

        return table

    def _initialize_stat_calculations(self) -> Dict[StatType, Dict]:
        """Initialize how stats are calculated from archetype attributes."""
        return {
            StatType.DAMAGE: {
                "base": 10,
                "power_multiplier": 2.0,      # Melee offense
                "agility_multiplier": 1.5,     # Ranged offense
                "knowledge_multiplier": 1.0,   # Magic offense
            },
            StatType.DEFENSE: {
                "base": 5,
                "toughness_multiplier": 2.0,   # Melee defense vs Magic
                "finesse_multiplier": 1.5,     # Ranged defense vs Melee
                "wisdom_multiplier": 1.0,      # Magic defense vs Ranged
            },
            StatType.CRITICAL_CHANCE: {
                "base": 0.05,
                "agility_bonus": 0.01,         # Ranged precision
                "chaos_bonus": 0.02,           # Wild unpredictability
                "max": 0.50,
            },
            StatType.HEALTH: {
                "base": 100,
                "toughness_multiplier": 10.0,  # Melee survivability
                "level_multiplier": 5.0,
            },
            StatType.MANA: {
                "base": 50,
                "knowledge_multiplier": 8.0,   # Magic offense
                "wisdom_multiplier": 5.0,      # Magic defense
                "level_multiplier": 3.0,
            },
        }

    def create_player(
        self, player_id: str, name: str, base_archetypes: Dict[str, int]
    ) -> bool:
        """
        Create a new player character with base archetype point distribution.

        Args:
            player_id: Unique identifier for the player
            name: Character name
            base_archetypes: Dictionary of archetype -> base points (must total 3)
                           e.g., {"melee": 3} for pure, {"melee": 2, "magic": 1} for hybrid

        Returns:
            True if successful, False otherwise
        """
        if player_id in self.players:
            return False

        # Validate base archetype points (must total exactly 3)
        total_base_points = sum(base_archetypes.values())
        if total_base_points != 3:
            raise ValueError(
                f"Base archetype points must total 3, got {total_base_points}"
            )

        # Start at level 5 (3 from creation + 2 free levels)
        starting_class_level = 5
        starting_skill_level = 0

        # Calculate initial Class Points (1 per 3 class levels + 2 free)
        initial_class_points = (
            starting_class_level // 3
        ) + 2  # 1 + 2 = 3 points to start

        player_data = {
            "id": player_id,
            "name": name,
            "base_archetypes": base_archetypes.copy(),  # Permanent, determines ultimate access
            "archetypes": base_archetypes.copy(),  # Current archetype levels (same as base for now)
            # Starting at level 5 with XP system
            "xp": {
                "base": 0,
                "class": self.xp_system.calculate_total_xp_for_level(
                    starting_class_level
                ),
                "skill": 0,
            },
            "levels": {
                "base": 1,
                "class": starting_class_level,
                "skill": starting_skill_level,
            },
            "player_level": starting_class_level + starting_skill_level,  # 5 + 0 = 5
            # Point allocation
            "points": {
                "base": 3,  # The 3 base points distributed at creation
                "class": initial_class_points,  # 3 points to start with
                "skill": 0,  # No skill points yet
            },
            "unused_points": {
                "class": initial_class_points,
                "skill": 0,
            },  # All 3 class points available
            # Legacy fields for backward compatibility
            "level": 1,
            "experience": 0,
            "class_points": 0,
            "skill_points": 0,
            "unused_skill_points": 0,
            # Archetype Attributes (Class Points)
            "attributes": {
                StatType.POWER: 0,        # Melee Offense
                StatType.TOUGHNESS: 0,    # Melee Defense vs Magic
                StatType.AGILITY: 0,      # Ranged Offense
                StatType.FINESSE: 0,      # Ranged Defense vs Melee
                StatType.KNOWLEDGE: 0,    # Magic Offense
                StatType.WISDOM: 0,       # Magic Defense vs Ranged
                StatType.CHAOS: 0,        # Wild Utility
            },
            # Combat stats
            "combat_stats": {
                StatType.DAMAGE: 10,
                StatType.DEFENSE: 5,
                StatType.CRITICAL_CHANCE: 0.05,
                StatType.CRITICAL_DAMAGE: 1.5,
                StatType.ACCURACY: 0.8,
                StatType.DODGE: 0.05,
            },
            # Resources
            "resources": {
                StatType.HEALTH: 100,
                StatType.MANA: 50,
                StatType.STAMINA: 100,
            },
            # Resistances
            "resistances": {
                "physical": 0,
                "burn": 0,
                "freeze": 0,
                "stun": 0,
                "poison": 0,
                "bleed": 0,
                "chaos": 0,
            },
            # Progression tracking
            "total_experience_gained": 0,
            "enemies_defeated": 0,
            "items_found": 0,
            "skills_learned": 0,
            # Timestamps
            "created_at": time.time(),
            "last_login": time.time(),
            "play_time": 0,
        }

        self.players[player_id] = player_data

        # Initialize levels and points from starting XP
        self._update_levels_from_xp(player_id)

        return True

    def get_player(self, player_id: str) -> Optional[Dict]:
        """Get player data by ID."""
        return self.players.get(player_id)

    def get_all_players(self) -> List[Dict]:
        """Get all players."""
        return list(self.players.values())

    def _update_levels_from_xp(self, player_id: str):
        """Update all levels and points based on current XP totals."""
        if player_id not in self.players:
            return

        player = self.players[player_id]

        # Calculate levels from XP pools
        for xp_type in ["base", "class", "skill"]:
            xp_amount = player["xp"][xp_type]
            level, _ = self.xp_system.calculate_level_from_xp(xp_amount)
            player["levels"][xp_type] = level

        # Calculate player level (class + skill)
        player["player_level"] = player["levels"]["class"] + player["levels"]["skill"]

        # Update legacy level for backward compatibility
        player["level"] = player["player_level"]

        # Calculate points from levels
        points = self.xp_system.calculate_points_from_xp(player["xp"])

        # Update point totals
        for point_type in ["base", "class", "skill"]:
            old_points = player["points"][point_type]
            new_points = points[point_type]

            # Add newly gained points to unused points
            if new_points > old_points:
                points_gained = new_points - old_points
                if point_type in player["unused_points"]:
                    player["unused_points"][point_type] += points_gained

            player["points"][point_type] = new_points

        # Update legacy fields
        player["class_points"] = player["points"]["class"]
        player["skill_points"] = player["points"]["skill"]
        player["unused_skill_points"] = player["unused_points"].get("skill", 0)

    def add_xp(self, player_id: str, xp_gained: Dict[str, int]) -> Dict:
        """
        Add XP to a player and handle leveling.

        Args:
            player_id: ID of the player
            xp_gained: Dictionary with XP amounts for each type

        Returns:
            Dictionary with leveling results
        """
        if player_id not in self.players:
            return {"success": False, "error": "Player not found"}

        player = self.players[player_id]

        # Store old XP for level-up detection
        old_xp = player["xp"].copy()

        # Add XP using the XP system
        new_xp = self.xp_system.add_xp(old_xp, xp_gained)
        player["xp"] = new_xp

        # Update legacy total experience
        total_gained = sum(xp_gained.values())
        player["experience"] += total_gained
        player["total_experience_gained"] += total_gained

        # Update levels and points
        old_player_level = player["player_level"]
        self._update_levels_from_xp(player_id)
        new_player_level = player["player_level"]

        # Check for level-ups
        leveled_up, point_gains = self.xp_system.check_level_up(old_xp, new_xp)

        # Recalculate stats if player level changed
        if new_player_level != old_player_level:
            self._recalculate_player_stats(player_id)

        return {
            "success": True,
            "leveled_up": leveled_up,
            "point_gains": point_gains,
            "old_player_level": old_player_level,
            "new_player_level": new_player_level,
            "levels": player["levels"].copy(),
            "xp": player["xp"].copy(),
            "unused_points": player["unused_points"].copy(),
        }

    def add_experience(self, player_id: str, experience: int) -> Dict:
        """
        Add experience to a player and handle leveling.

        Args:
            player_id: ID of the player
            experience: Experience to add

        Returns:
            Dictionary with leveling results
        """
        if player_id not in self.players:
            return {"success": False, "error": "Player not found"}

        player = self.players[player_id]
        player["experience"] += experience
        player["total_experience_gained"] += experience

        # Check for level up
        level_gained = 0
        skill_points_gained = 0

        while True:
            next_level = player["level"] + 1
            if next_level in self.experience_table:
                required_exp = self.experience_table[next_level]
                if player["experience"] >= required_exp:
                    player["level"] = next_level
                    level_gained += 1
                    skill_points_gained += 2  # 2 skill points per level
                    player["unused_skill_points"] += 2
                else:
                    break
            else:
                break

        # Recalculate stats after leveling
        if level_gained > 0:
            self._recalculate_player_stats(player_id)

        return {
            "success": True,
            "level_gained": level_gained,
            "skill_points_gained": skill_points_gained,
            "current_level": player["level"],
            "current_experience": player["experience"],
            "next_level_exp": self.experience_table.get(player["level"] + 1, 0),
        }

    def add_class_points(self, player_id: str, points: int) -> bool:
        """
        Add Class Points to a player.

        Args:
            player_id: ID of the player
            points: Class Points to add

        Returns:
            True if successful, False otherwise
        """
        if player_id not in self.players:
            return False

        self.players[player_id]["class_points"] += points
        return True

    def use_skill_points(self, player_id: str, points: int) -> bool:
        """
        Use Skill Points for a player.

        Args:
            player_id: ID of the player
            points: Skill Points to use

        Returns:
            True if successful, False otherwise
        """
        if player_id not in self.players:
            return False

        player = self.players[player_id]
        if player["unused_skill_points"] >= points:
            player["unused_skill_points"] -= points
            player["skill_points"] += points
            return True

        return False

    def reset_skill_points(self, player_id: str) -> bool:
        """
        Reset Skill Points for a player (Class Points remain unchanged).

        Args:
            player_id: ID of the player

        Returns:
            True if successful, False otherwise
        """
        if player_id not in self.players:
            return False

        player = self.players[player_id]
        player["unused_skill_points"] += player["skill_points"]
        player["skill_points"] = 0
        return True

    def allocate_class_points_to_attribute(self, player_id: str, attribute: StatType, points: int) -> Dict:
        """
        Allocate Class Points to a specific attribute.

        Args:
            player_id: ID of the player
            attribute: The attribute to allocate points to (POWER, TOUGHNESS, etc.)
            points: Number of Class Points to allocate

        Returns:
            Dictionary with success status and details
        """
        if player_id not in self.players:
            return {"success": False, "error": "Player not found"}

        player = self.players[player_id]
        available_class_points = player["unused_points"]["class"]

        if available_class_points < points:
            return {
                "success": False, 
                "error": f"Not enough Class Points (need {points}, have {available_class_points})"
            }

        # Validate attribute type
        valid_attributes = [
            StatType.POWER, StatType.TOUGHNESS, StatType.AGILITY, 
            StatType.FINESSE, StatType.KNOWLEDGE, StatType.WISDOM, StatType.CHAOS
        ]
        
        if attribute not in valid_attributes:
            return {"success": False, "error": f"Invalid attribute: {attribute.value}"}

        # Allocate points
        player["attributes"][attribute] += points
        player["unused_points"]["class"] -= points

        # Recalculate stats after attribute change
        self._recalculate_player_stats(player_id)

        return {
            "success": True,
            "attribute": attribute.value,
            "points_allocated": points,
            "total_in_attribute": player["attributes"][attribute],
            "remaining_class_points": player["unused_points"]["class"]
        }

    def get_attribute_info(self, player_id: str) -> Dict:
        """
        Get detailed information about a player's attributes and Class Points.

        Args:
            player_id: ID of the player

        Returns:
            Dictionary with attribute information
        """
        if player_id not in self.players:
            return {"error": "Player not found"}

        player = self.players[player_id]
        attributes = player["attributes"]
        
        # Map attributes to their archetype associations
        archetype_mapping = {
            StatType.POWER: "Melee (Offense)",
            StatType.TOUGHNESS: "Melee (Defense vs Magic)",
            StatType.AGILITY: "Ranged (Offense)",
            StatType.FINESSE: "Ranged (Defense vs Melee)",
            StatType.KNOWLEDGE: "Magic (Offense)",
            StatType.WISDOM: "Magic (Defense vs Ranged)",
            StatType.CHAOS: "Wild (Utility)"
        }

        result = {
            "player_id": player_id,
            "class_points_available": player["unused_points"]["class"],
            "attributes": {}
        }

        for attribute, value in attributes.items():
            result["attributes"][attribute.value] = {
                "value": value,
                "archetype": archetype_mapping.get(attribute, "Unknown"),
                "description": self._get_attribute_description(attribute)
            }

        return result

    def _get_attribute_description(self, attribute: StatType) -> str:
        """Get a description of what an attribute does."""
        descriptions = {
            StatType.POWER: "Increases damage for Melee archetypes",
            StatType.TOUGHNESS: "Increases defense and health, especially against Magic",
            StatType.AGILITY: "Increases damage and critical chance for Ranged archetypes",
            StatType.FINESSE: "Increases defense and accuracy, especially against Melee",
            StatType.KNOWLEDGE: "Increases damage and mana for Magic archetypes",
            StatType.WISDOM: "Increases defense and mana regeneration, especially against Ranged",
            StatType.CHAOS: "Increases critical chance and unpredictable effects for Wild archetypes"
        }
        return descriptions.get(attribute, "Unknown attribute")

    def _recalculate_player_stats(self, player_id: str):
        """Recalculate all player stats based on level and archetype attributes."""
        if player_id not in self.players:
            return

        player = self.players[player_id]
        attributes = player["attributes"]
        level = player["player_level"]  # Use the new player_level

        # Calculate derived stats
        for stat_type, calculation in self.stat_calculations.items():
            value = calculation.get("base", 0)

            # Add attribute-based bonuses
            for stat_name, multiplier in calculation.items():
                if stat_name.endswith("_multiplier") or stat_name.endswith("_bonus"):
                    # Extract the attribute name from the calculation key
                    attribute_name = stat_name.replace("_multiplier", "").replace("_bonus", "")
                    
                    # Map the calculation key to the actual StatType enum
                    attribute_mapping = {
                        "power": StatType.POWER,
                        "toughness": StatType.TOUGHNESS,
                        "agility": StatType.AGILITY,
                        "finesse": StatType.FINESSE,
                        "knowledge": StatType.KNOWLEDGE,
                        "wisdom": StatType.WISDOM,
                        "chaos": StatType.CHAOS
                    }
                    
                    attribute_type = attribute_mapping.get(attribute_name)
                    if attribute_type and attribute_type in attributes:
                        if stat_name.endswith("_multiplier"):
                            value += attributes[attribute_type] * multiplier
                        else:
                            value += multiplier

            # Add level-based bonuses
            if "level_multiplier" in calculation:
                value += level * calculation["level_multiplier"]

            # Apply maximum limits
            if "max" in calculation:
                value = min(value, calculation["max"])

            # Update the appropriate stat category
            if stat_type in [StatType.HEALTH, StatType.MANA, StatType.STAMINA]:
                player["resources"][stat_type] = int(value)
            elif stat_type in [
                StatType.DAMAGE,
                StatType.DEFENSE,
                StatType.CRITICAL_CHANCE,
                StatType.CRITICAL_DAMAGE,
                StatType.ACCURACY,
                StatType.DODGE,
            ]:
                player["combat_stats"][stat_type] = value
            else:
                player["stats"][stat_type] = int(value)

    def get_player_stats(self, player_id: str) -> Dict:
        """Get comprehensive player stats."""
        if player_id not in self.players:
            return {"error": "Player not found"}

        player = self.players[player_id]

        return {
            "id": player["id"],
            "name": player["name"],
            "level": player["level"],
            "experience": player["experience"],
            "class_points": player["class_points"],
            "skill_points": player["skill_points"],
            "unused_skill_points": player["unused_skill_points"],
            "stats": player["stats"],
            "combat_stats": player["combat_stats"],
            "resources": player["resources"],
            "resistances": player["resistances"],
            "progression": {
                "total_experience_gained": player["total_experience_gained"],
                "enemies_defeated": player["enemies_defeated"],
                "items_found": player["items_found"],
                "skills_learned": player["skills_learned"],
            },
        }

    def update_player_stat(
        self, player_id: str, stat_type: StatType, value: int
    ) -> bool:
        """
        Update a player's core stat.

        Args:
            player_id: ID of the player
            stat_type: Type of stat to update
            value: New value for the stat

        Returns:
            True if successful, False otherwise
        """
        if player_id not in self.players:
            return False

        player = self.players[player_id]
        player["stats"][stat_type] = value

        # Recalculate derived stats
        self._recalculate_player_stats(player_id)
        return True

    def add_resistance(self, player_id: str, resistance_type: str, value: int) -> bool:
        """
        Add resistance to a player.

        Args:
            player_id: ID of the player
            resistance_type: Type of resistance
            value: Resistance value to add

        Returns:
            True if successful, False otherwise
        """
        if player_id not in self.players:
            return False

        player = self.players[player_id]
        if resistance_type in player["resistances"]:
            player["resistances"][resistance_type] += value
            return True

        return False

    def track_achievement(
        self, player_id: str, achievement_type: str, value: int = 1
    ) -> bool:
        """
        Track an achievement for a player.

        Args:
            player_id: ID of the player
            achievement_type: Type of achievement
            value: Value to add

        Returns:
            True if successful, False otherwise
        """
        if player_id not in self.players:
            return False

        player = self.players[player_id]

        if achievement_type == "enemies_defeated":
            player["enemies_defeated"] += value
        elif achievement_type == "items_found":
            player["items_found"] += value
        elif achievement_type == "skills_learned":
            player["skills_learned"] += value
        else:
            return False

        return True

    def save_player_data(self, player_id: str, file_path: str) -> bool:
        """
        Save player data to a file.

        Args:
            player_id: ID of the player
            file_path: Path to save file

        Returns:
            True if successful, False otherwise
        """
        if player_id not in self.players:
            return False

        try:
            with open(file_path, "w") as f:
                json.dump(self.players[player_id], f, indent=2)
            return True
        except Exception:
            return False

    def load_player_data(self, player_id: str, file_path: str) -> bool:
        """
        Load player data from a file.

        Args:
            player_id: ID of the player
            file_path: Path to load file from

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(file_path, "r") as f:
                player_data = json.load(f)

            self.players[player_id] = player_data
            return True
        except Exception:
            return False

    def get_player_summary(self, player_id: str) -> Dict:
        """Get a summary of player progress and achievements."""
        if player_id not in self.players:
            return {"error": "Player not found"}

        player = self.players[player_id]

        return {
            "name": player["name"],
            "level": player["level"],
            "class_points": player["class_points"],
            "skill_points": player["skill_points"],
            "total_experience": player["total_experience_gained"],
            "achievements": {
                "enemies_defeated": player["enemies_defeated"],
                "items_found": player["items_found"],
                "skills_learned": player["skills_learned"],
            },
            "play_time": player["play_time"],
            "created_at": player["created_at"],
        }


# Example usage and testing
if __name__ == "__main__":
    player_system = PlayerSystem()

    # Test creating a player
    success = player_system.create_player("player1", "Hero", ["melee", "ranged"])
    print(f"Player created: {success}")

    # Test adding experience
    result = player_system.add_experience("player1", 150)
    print(f"Experience result: {result}")

    # Test using skill points
    success = player_system.use_skill_points("player1", 2)
    print(f"Used skill points: {success}")

    # Test getting player stats
    stats = player_system.get_player_stats("player1")
    print(
        f"Player stats: Level {stats['level']}, Class Points: {stats['class_points']}"
    )

    # Test tracking achievements
    player_system.track_achievement("player1", "enemies_defeated", 5)
    summary = player_system.get_player_summary("player1")
    print(f"Player summary: {summary['achievements']}")

"""
CHRONICLES OF RUIN: CLASS SYSTEM
================================

This module handles the character class and archetype system for Chronicles of Ruin.
It implements the flexible class combination system where players can mix and match
abilities from different archetypes to create custom builds.

PURPOSE:
- Manages the 4 main archetypes (Melee, Ranged, Magic, Wild)
- Handles the 3 subtypes within each archetype
- Implements the class combination rules and restrictions
- Manages skill point allocation and class progression
- Provides character creation and class selection interface

ARCHITECTURE:
- ArchetypeSystem: Manages the 4 main archetypes and their subtypes
- ClassCombination: Handles rules for combining different archetypes
- SkillAllocation: Manages skill points and class progression
- CharacterCreation: Handles the character creation process

CLASS SYSTEM RULES:
- Players can choose from 4 main archetypes: Melee, Ranged, Magic, Wild
- Each archetype has 3 subtypes/specializations
- Players can combine archetypes with restrictions:
  * 2 archetypes: Can pick 2 subtypes from each
  * 3 archetypes: Can pick 1 subtype from each
  * 4 archetypes: Can pick 1 subtype from each (maximum flexibility)
- Class Points are permanent, Skill Points can be reset
- Unlockable classes provide additional options later in the game

ARCHETYPE STRUCTURE:
1. MELEE: Juggernaut, Duelist, Berserker
2. RANGED: Archer, Gunslinger, Trapper
3. MAGIC: Elementalist, Arcanist, Necromancer
4. WILD: Alchemist, Chaos Mage, Beastmaster

This system provides deep customization while maintaining balance and
preventing overpowered combinations through strategic restrictions.
"""

from typing import Dict, List, Optional, Tuple
from enum import Enum
from .player_system import PlayerSystem, StatType


class ArchetypeType(Enum):
    """Enumeration of the four main archetypes."""

    MELEE = "melee"
    RANGED = "ranged"
    MAGIC = "magic"
    WILD = "wild"


class SubtypeType(Enum):
    """Enumeration of all subtypes across all archetypes."""

    # Melee subtypes
    JUGGERNAUT = "juggernaut"
    DUELIST = "duelist"
    BERSERKER = "berserker"

    # Ranged subtypes
    ARCHER = "archer"
    GUNSLINGER = "gunslinger"
    TRAPPER = "trapper"

    # Magic subtypes
    ELEMENTALIST = "elementalist"
    ARCANIST = "arcanist"
    NECROMANCER = "necromancer"

    # Wild subtypes
    ALCHEMIST = "alchemist"
    CHAOS_MAGE = "chaos_mage"
    BEASTMASTER = "beastmaster"


class ClassSystem:
    """
    Main class system that manages character classes, archetypes, and combinations.
    Handles the flexible class system where players can mix archetypes.
    """

    def __init__(self, player_system: PlayerSystem = None):
        """Initialize the class system with all archetypes and subtypes."""
        self.archetypes = self._initialize_archetypes()
        self.class_combinations = self._initialize_combinations()
        self.unlocked_classes = set()  # Classes unlocked through gameplay

        # Integrate with player system
        self.player_system = player_system or PlayerSystem()

        # Initialize class feature trees
        self.class_features = self._initialize_class_features()

    def _initialize_archetypes(self) -> Dict[ArchetypeType, Dict]:
        """Initialize all archetypes with their subtypes and basic information."""
        return {
            ArchetypeType.MELEE: {
                "name": "Melee",
                "description": "Close combat specialists who excel in physical combat",
                "subtypes": {
                    SubtypeType.JUGGERNAUT: {
                        "name": "Juggernaut",
                        "description": "Heavy armor and two-handed weapons",
                        "focus": "defense_and_raw_power",
                        "base_skills": ["Bash", "Heavy Strike", "Defensive Stance"],
                    },
                    SubtypeType.DUELIST: {
                        "name": "Duelist",
                        "description": "Dual-wielding and precise strikes",
                        "focus": "speed_and_precision",
                        "base_skills": ["Quick Strike", "Dual Slash", "Parry"],
                    },
                    SubtypeType.BERSERKER: {
                        "name": "Berserker",
                        "description": "Rage-fueled combat with high risk/reward",
                        "focus": "damage_and_rage",
                        "base_skills": [
                            "Rage Strike",
                            "Blood Frenzy",
                            "Berserker Rage",
                        ],
                    },
                },
            },
            ArchetypeType.RANGED: {
                "name": "Ranged",
                "description": "Distance fighters who attack from afar",
                "subtypes": {
                    SubtypeType.ARCHER: {
                        "name": "Archer",
                        "description": "Traditional bow and arrow combat",
                        "focus": "precision_and_versatility",
                        "base_skills": ["Precise Shot", "Multi-Shot", "Aimed Shot"],
                    },
                    SubtypeType.GUNSLINGER: {
                        "name": "Gunslinger",
                        "description": "Magical firearms and quick-draw techniques",
                        "focus": "speed_and_style",
                        "base_skills": [
                            "Quick Draw",
                            "Ricochet Shot",
                            "Fan the Hammer",
                        ],
                    },
                    SubtypeType.TRAPPER: {
                        "name": "Trapper",
                        "description": "Traps and survivalist techniques",
                        "focus": "control_and_preparation",
                        "base_skills": ["Bear Trap", "Poison Dart", "Camouflage"],
                    },
                },
            },
            ArchetypeType.MAGIC: {
                "name": "Magic",
                "description": "Spellcasters who wield arcane and elemental power",
                "subtypes": {
                    SubtypeType.ELEMENTALIST: {
                        "name": "Elementalist",
                        "description": "Master of fire, ice, and lightning",
                        "focus": "elemental_combos",
                        "base_skills": ["Fireball", "Ice Bolt", "Lightning Strike"],
                    },
                    SubtypeType.ARCANIST: {
                        "name": "Arcanist",
                        "description": "Pure magical energy and arcane manipulation",
                        "focus": "raw_magical_power",
                        "base_skills": ["Arcane Bolt", "Teleport", "Time Slow"],
                    },
                    SubtypeType.NECROMANCER: {
                        "name": "Necromancer",
                        "description": "Dark magic and undead minions",
                        "focus": "minions_and_life_drain",
                        "base_skills": ["Raise Dead", "Life Drain", "Death Touch"],
                    },
                },
            },
            ArchetypeType.WILD: {
                "name": "Wild",
                "description": "Unpredictable and chaotic combat styles",
                "subtypes": {
                    SubtypeType.ALCHEMIST: {
                        "name": "Alchemist",
                        "description": "Potions, bombs, and chemical warfare",
                        "focus": "utility_and_explosions",
                        "base_skills": ["Acid Vial", "Healing Potion", "Smoke Bomb"],
                    },
                    SubtypeType.CHAOS_MAGE: {
                        "name": "Chaos Mage",
                        "description": "Unpredictable magic with high risk/reward",
                        "focus": "random_effects_and_chaos",
                        "base_skills": ["Chaos Bolt", "Random Teleport", "Wild Surge"],
                    },
                    SubtypeType.BEASTMASTER: {
                        "name": "Beastmaster",
                        "description": "Animal companions and primal instincts",
                        "focus": "companions_and_primal_power",
                        "base_skills": ["Summon Wolf", "Primal Roar", "Pack Tactics"],
                    },
                },
            },
        }

    def _initialize_combinations(self) -> Dict[str, Dict]:
        """Initialize the rules for combining different archetypes."""
        return {
            "two_archetypes": {
                "description": "Choose 2 archetypes, pick 2 subtypes from each",
                "restrictions": "Maximum 2 archetypes, 2 subtypes per archetype",
            },
            "three_archetypes": {
                "description": "Choose 3 archetypes, pick 1 subtype from each",
                "restrictions": "Maximum 3 archetypes, 1 subtype per archetype",
            },
            "four_archetypes": {
                "description": "Choose all 4 archetypes, pick 1 subtype from each",
                "restrictions": "All 4 archetypes, 1 subtype per archetype",
            },
        }

    def get_archetype_info(self, archetype: ArchetypeType) -> Dict:
        """Get information about a specific archetype."""
        return self.archetypes.get(archetype, {})

    def get_subtype_info(self, archetype: ArchetypeType, subtype: SubtypeType) -> Dict:
        """Get information about a specific subtype."""
        archetype_data = self.archetypes.get(archetype, {})
        subtypes = archetype_data.get("subtypes", {})
        return subtypes.get(subtype, {})

    def get_all_archetypes(self) -> List[ArchetypeType]:
        """Get a list of all available archetypes."""
        return list(self.archetypes.keys())

    def get_subtypes_for_archetype(self, archetype: ArchetypeType) -> List[SubtypeType]:
        """Get all subtypes for a specific archetype."""
        archetype_data = self.archetypes.get(archetype, {})
        subtypes = archetype_data.get("subtypes", {})
        return list(subtypes.keys())

    def validate_class_combination(
        self,
        selected_archetypes: List[ArchetypeType],
        selected_subtypes: Dict[ArchetypeType, List[SubtypeType]],
    ) -> Tuple[bool, str]:
        """
        Validate if a class combination is legal according to the rules.

        Args:
            selected_archetypes: List of chosen archetypes
            selected_subtypes: Dict mapping archetype to list of chosen subtypes

        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(selected_archetypes) < 1:
            return False, "Must select at least one archetype"

        if len(selected_archetypes) > 4:
            return False, "Cannot select more than 4 archetypes"

        # Check that all selected archetypes have subtypes
        for archetype in selected_archetypes:
            if archetype not in selected_subtypes:
                return False, f"Must select subtypes for {archetype.value}"

        # Check subtype limits based on number of archetypes
        if len(selected_archetypes) == 1:
            # Single archetype: can pick all 3 subtypes
            for archetype, subtypes in selected_subtypes.items():
                if len(subtypes) > 3:
                    return (
                        False,
                        f"Cannot select more than 3 subtypes for {archetype.value}",
                    )

        elif len(selected_archetypes) == 2:
            # Two archetypes: can pick 2 subtypes from each
            for archetype, subtypes in selected_subtypes.items():
                if len(subtypes) > 2:
                    return (
                        False,
                        f"Cannot select more than 2 subtypes for {archetype.value} in 2-archetype build",
                    )

        elif len(selected_archetypes) >= 3:
            # Three or four archetypes: can pick 1 subtype from each
            for archetype, subtypes in selected_subtypes.items():
                if len(subtypes) > 1:
                    return (
                        False,
                        f"Cannot select more than 1 subtype for {archetype.value} in multi-archetype build",
                    )

        return True, "Valid class combination"

    def create_character_class(
        self,
        selected_archetypes: List[ArchetypeType],
        selected_subtypes: Dict[ArchetypeType, List[SubtypeType]],
    ) -> Dict:
        """
        Create a character class based on the selected archetypes and subtypes.

        Args:
            selected_archetypes: List of chosen archetypes
            selected_subtypes: Dict mapping archetype to list of chosen subtypes

        Returns:
            Character class data structure
        """
        is_valid, error_msg = self.validate_class_combination(
            selected_archetypes, selected_subtypes
        )
        if not is_valid:
            raise ValueError(f"Invalid class combination: {error_msg}")

        # Build the character class
        character_class = {
            "archetypes": selected_archetypes,
            "subtypes": selected_subtypes,
            "skills": [],
            "class_points": 0,
            "skill_points": 0,
            "unlocked_abilities": set(),
        }

        # Collect all base skills from selected subtypes
        for archetype in selected_archetypes:
            for subtype in selected_subtypes[archetype]:
                subtype_info = self.get_subtype_info(archetype, subtype)
                base_skills = subtype_info.get("base_skills", [])
                character_class["skills"].extend(base_skills)

        return character_class

    def get_class_description(self, character_class: Dict) -> str:
        """Generate a description for a character class based on its components."""
        archetypes = character_class["archetypes"]
        subtypes = character_class["subtypes"]

        if len(archetypes) == 1:
            archetype = archetypes[0]
            subtype_list = subtypes[archetype]
            return f"Pure {archetype.value.title()} specializing in {', '.join([s.value.title() for s in subtype_list])}"

        elif len(archetypes) == 2:
            return f"Hybrid {archetypes[0].value.title()}/{archetypes[1].value.title()} build"

        elif len(archetypes) == 3:
            archetype_names = [a.value.title() for a in archetypes]
            return f"Triple archetype: {'/'.join(archetype_names)}"

        else:  # 4 archetypes
            return "Master of all archetypes - ultimate flexibility"

    def unlock_class(self, class_name: str):
        """Unlock a new class through gameplay."""
        self.unlocked_classes.add(class_name)

    def get_unlocked_classes(self) -> List[str]:
        """Get list of unlocked classes."""
        return list(self.unlocked_classes)

    def _initialize_class_features(self) -> Dict[ArchetypeType, Dict]:
        """Initialize class features that can be unlocked with Class Points."""
        return {
            ArchetypeType.MELEE: {
                "features": {
                    1: {
                        "name": "Combat Training",
                        "description": "+2 Damage, +1 Defense",
                        "bonuses": {StatType.DAMAGE: 2, StatType.DEFENSE: 1},
                    },
                    2: {
                        "name": "Weapon Mastery",
                        "description": "+5% Critical Chance, +0.2 Critical Damage",
                        "bonuses": {
                            StatType.CRITICAL_CHANCE: 0.05,
                            StatType.CRITICAL_DAMAGE: 0.2,
                        },
                    },
                    3: {
                        "name": "Battle Hardened",
                        "description": "+15 Health, +3 Defense",
                        "bonuses": {StatType.HEALTH: 15, StatType.DEFENSE: 3},
                    },
                    4: {
                        "name": "Berserker Rage",
                        "description": "+4 Damage, +10% Critical Chance",
                        "bonuses": {StatType.DAMAGE: 4, StatType.CRITICAL_CHANCE: 0.10},
                    },
                    5: {
                        "name": "Legendary Warrior",
                        "description": "+5 All Combat Stats",
                        "bonuses": {
                            StatType.DAMAGE: 5,
                            StatType.DEFENSE: 5,
                            StatType.CRITICAL_CHANCE: 0.05,
                        },
                    },
                }
            },
            ArchetypeType.RANGED: {
                "features": {
                    1: {
                        "name": "Precision Training",
                        "description": "+10% Accuracy, +1 Damage",
                        "bonuses": {StatType.ACCURACY: 0.10, StatType.DAMAGE: 1},
                    },
                    2: {
                        "name": "Eagle Eye",
                        "description": "+10% Critical Chance, +5% Accuracy",
                        "bonuses": {
                            StatType.CRITICAL_CHANCE: 0.10,
                            StatType.ACCURACY: 0.05,
                        },
                    },
                    3: {
                        "name": "Fleet Footed",
                        "description": "+10% Dodge, +2 Dexterity",
                        "bonuses": {StatType.DODGE: 0.10, StatType.AGILITY: 2},
                    },
                    4: {
                        "name": "Master Archer",
                        "description": "+3 Damage, +0.3 Critical Damage",
                        "bonuses": {StatType.DAMAGE: 3, StatType.CRITICAL_DAMAGE: 0.3},
                    },
                    5: {
                        "name": "Legendary Marksman",
                        "description": "+15% Critical Chance, +2 All Stats",
                        "bonuses": {
                            StatType.CRITICAL_CHANCE: 0.15,
                            StatType.DAMAGE: 2,
                            StatType.ACCURACY: 0.10,
                        },
                    },
                }
            },
            ArchetypeType.MAGIC: {
                "features": {
                    1: {
                        "name": "Arcane Knowledge",
                        "description": "+10 Mana, +1 Intelligence",
                        "bonuses": {StatType.MANA: 10, StatType.KNOWLEDGE: 1},
                    },
                    2: {
                        "name": "Spell Focus",
                        "description": "+2 Magic Damage, +5 Mana",
                        "bonuses": {StatType.DAMAGE: 2, StatType.MANA: 5},
                    },
                    3: {
                        "name": "Elemental Mastery",
                        "description": "+2 Intelligence, +1 Wisdom",
                        "bonuses": {StatType.KNOWLEDGE: 2, StatType.WISDOM: 1},
                    },
                    4: {
                        "name": "Arcane Power",
                        "description": "+3 Magic Damage, +10 Mana",
                        "bonuses": {StatType.DAMAGE: 3, StatType.MANA: 10},
                    },
                    5: {
                        "name": "Legendary Mage",
                        "description": "+4 All Mental Stats, +15 Mana",
                        "bonuses": {
                            StatType.KNOWLEDGE: 4,
                            StatType.WISDOM: 4,
                            StatType.MANA: 15,
                        },
                    },
                }
            },
            ArchetypeType.WILD: {
                "features": {
                    1: {
                        "name": "Chaos Touch",
                        "description": "+1 Chaos, +5% Wild Damage Bonus",
                        "bonuses": {StatType.CHAOS: 1, "wild_damage_bonus": 0.05},
                    },
                    2: {
                        "name": "Unpredictable",
                        "description": "+2 Chaos, +5% Dodge",
                        "bonuses": {StatType.CHAOS: 2, StatType.DODGE: 0.05},
                    },
                    3: {
                        "name": "Chaotic Energy",
                        "description": "+3 Chaos, +10% Critical Chance",
                        "bonuses": {StatType.CHAOS: 3, StatType.CRITICAL_CHANCE: 0.10},
                    },
                    4: {
                        "name": "Wild Surge",
                        "description": "+2 All Stats, +15% Wild Effects",
                        "bonuses": {
                            StatType.CHAOS: 2,
                            "wild_damage_bonus": 0.15,
                            "wild_effect_chance": 0.15,
                        },
                    },
                    5: {
                        "name": "Legendary Chaos",
                        "description": "+5 Chaos, +25% Wild Power",
                        "bonuses": {
                            StatType.CHAOS: 5,
                            "wild_damage_bonus": 0.25,
                            "wild_effect_chance": 0.25,
                        },
                    },
                }
            },
        }

    def unlock_class_feature(
        self, player_id: str, archetype: ArchetypeType, feature_level: int
    ) -> Dict:
        """
        Unlock a class feature for a player using Class Points.

        Args:
            player_id: Player ID
            archetype: Archetype to unlock feature for
            feature_level: Level of feature to unlock (1-5)

        Returns:
            Result of the unlock attempt
        """
        # Get player data
        player_data = self.player_system.get_player(player_id)
        if not player_data:
            return {"success": False, "error": "Player not found"}

        # Check if player has this archetype
        player_archetypes = player_data.get("archetypes", {})
        # Check both enum objects and string values
        has_archetype = False
        for player_archetype in player_archetypes.keys():
            if hasattr(player_archetype, "value"):
                if player_archetype.value == archetype.value:
                    has_archetype = True
                    break
            elif player_archetype == archetype.value:
                has_archetype = True
                break

        if not has_archetype:
            return {
                "success": False,
                "error": f"Player does not have {archetype.value} archetype",
            }

        # Check if player has enough class points
        unused_class_points = player_data["unused_points"]["class"]
        if unused_class_points < 1:
            return {"success": False, "error": "Not enough Class Points (need 1)"}

        # Check if feature exists
        if archetype not in self.class_features:
            return {
                "success": False,
                "error": f"No features for archetype {archetype.value}",
            }

        features = self.class_features[archetype]["features"]
        if feature_level not in features:
            return {
                "success": False,
                "error": f"Feature level {feature_level} does not exist",
            }

        # Check prerequisites (must unlock features in order)
        if "class_features_unlocked" not in player_data:
            player_data["class_features_unlocked"] = {}
        if archetype.value not in player_data["class_features_unlocked"]:
            player_data["class_features_unlocked"][archetype.value] = []

        unlocked_features = player_data["class_features_unlocked"][archetype.value]
        if feature_level > 1 and (feature_level - 1) not in unlocked_features:
            return {
                "success": False,
                "error": f"Must unlock feature {feature_level - 1} first",
            }

        if feature_level in unlocked_features:
            return {
                "success": False,
                "error": f"Feature {feature_level} already unlocked",
            }

        # Unlock the feature
        feature = features[feature_level]
        unlocked_features.append(feature_level)

        # Deduct class point
        player_data["unused_points"]["class"] -= 1

        # Apply feature bonuses
        self._apply_class_feature_bonuses(player_data, feature)

        # Recalculate player stats
        self.player_system._recalculate_player_stats(player_id)

        return {
            "success": True,
            "feature_unlocked": feature,
            "remaining_class_points": player_data["unused_points"]["class"],
        }

    def _apply_class_feature_bonuses(self, player_data: Dict, feature: Dict):
        """Apply the stat bonuses from a class feature to player data."""
        bonuses = feature.get("bonuses", {})

        for stat_type, bonus_value in bonuses.items():
            if isinstance(stat_type, StatType):
                # Handle StatType enums
                if stat_type in [StatType.HEALTH, StatType.MANA, StatType.STAMINA]:
                    player_data["resources"][stat_type] += bonus_value
                elif stat_type in [
                    StatType.DAMAGE,
                    StatType.DEFENSE,
                    StatType.CRITICAL_CHANCE,
                    StatType.CRITICAL_DAMAGE,
                    StatType.ACCURACY,
                    StatType.DODGE,
                ]:
                    player_data["combat_stats"][stat_type] += bonus_value
                else:
                    player_data["stats"][stat_type] += bonus_value
            else:
                # Handle special bonuses (wild effects, etc.)
                if "special_bonuses" not in player_data:
                    player_data["special_bonuses"] = {}
                if stat_type not in player_data["special_bonuses"]:
                    player_data["special_bonuses"][stat_type] = 0
                player_data["special_bonuses"][stat_type] += bonus_value

    def get_available_class_features(
        self, player_id: str, archetype: ArchetypeType
    ) -> Dict:
        """
        Get available class features for a player and archetype.

        Args:
            player_id: Player ID
            archetype: Archetype to check features for

        Returns:
            Dictionary with available, unlocked, and next features
        """
        player_data = self.player_system.get_player(player_id)
        if not player_data:
            return {"error": "Player not found"}

        # Check if player has this archetype
        player_archetypes = player_data.get("archetypes", {})
        # Check both enum objects and string values
        has_archetype = False
        for player_archetype in player_archetypes.keys():
            if hasattr(player_archetype, "value"):
                if player_archetype.value == archetype.value:
                    has_archetype = True
                    break
            elif player_archetype == archetype.value:
                has_archetype = True
                break

        if not has_archetype:
            return {"error": f"Player does not have {archetype.value} archetype"}

        if "class_features_unlocked" not in player_data:
            player_data["class_features_unlocked"] = {}
        if archetype.value not in player_data["class_features_unlocked"]:
            player_data["class_features_unlocked"][archetype.value] = []

        unlocked_features = player_data["class_features_unlocked"][archetype.value]
        features = self.class_features[archetype]["features"]
        class_points = player_data["unused_points"]["class"]

        result = {
            "archetype": archetype.value,
            "class_points_available": class_points,
            "unlocked_features": [],
            "next_available": None,
            "all_features": [],
        }

        # Build feature info
        for level in sorted(features.keys()):
            feature_info = features[level].copy()
            feature_info["level"] = level
            feature_info["unlocked"] = level in unlocked_features
            feature_info["can_unlock"] = (
                level not in unlocked_features
                and class_points >= 1
                and (level == 1 or (level - 1) in unlocked_features)
            )

            result["all_features"].append(feature_info)

            if feature_info["unlocked"]:
                result["unlocked_features"].append(feature_info)
            elif feature_info["can_unlock"] and result["next_available"] is None:
                result["next_available"] = feature_info

        return result


# Example usage and testing
if __name__ == "__main__":
    class_system = ClassSystem()

    # Test getting archetype info
    melee_info = class_system.get_archetype_info(ArchetypeType.MELEE)
    print(f"Melee archetype: {melee_info['name']}")

    # Test getting subtypes
    melee_subtypes = class_system.get_subtypes_for_archetype(ArchetypeType.MELEE)
    print(f"Melee subtypes: {[s.value for s in melee_subtypes]}")

    # Test class combination validation
    test_archetypes = [ArchetypeType.MELEE, ArchetypeType.RANGED]
    test_subtypes = {
        ArchetypeType.MELEE: [SubtypeType.JUGGERNAUT, SubtypeType.DUELIST],
        ArchetypeType.RANGED: [SubtypeType.ARCHER],
    }

    is_valid, msg = class_system.validate_class_combination(
        test_archetypes, test_subtypes
    )
    print(f"Test combination valid: {is_valid}, Message: {msg}")

    # Test character creation
    if is_valid:
        character = class_system.create_character_class(test_archetypes, test_subtypes)
        description = class_system.get_class_description(character)
        print(f"Created character: {description}")
        print(f"Skills: {character['skills']}")

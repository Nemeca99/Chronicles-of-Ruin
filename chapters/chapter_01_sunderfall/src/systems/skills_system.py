"""
CHRONICLES OF RUIN: SKILLS SYSTEM
=================================

This module handles all skill-related functionality for Chronicles of Ruin.
It manages skill trees, abilities, skill progression, and skill interactions.

PURPOSE:
- Manages skill trees and ability progression
- Handles skill point allocation and skill levels
- Provides skill effects and interactions
- Manages skill cooldowns and resource costs
- Implements skill synergies and combinations

ARCHITECTURE:
- SkillManager: Manages all skill data and progression
- SkillTree: Handles skill tree structure and requirements
- SkillEffects: Implements skill effects and interactions
- SkillCooldowns: Manages skill cooldowns and timing
- SkillSynergies: Handles skill combinations and synergies

SKILL SYSTEM:
- Skills have base damage that increases with skill points
- Each skill point increases min/max damage by 1
- Skills can have status effects and elemental properties
- Skills have cooldowns and resource costs
- Skills can synergize with other skills and archetypes

SKILL TREES:
- Each archetype has its own skill tree
- Skills have prerequisites and unlock requirements
- Skills can be upgraded with skill points
- Skills provide both active and passive effects

This system provides deep skill customization while maintaining
the simple damage progression system.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import time
import random
from .player_system import PlayerSystem, StatType
from .class_system import ClassSystem, ArchetypeType


class SkillType(Enum):
    """Enumeration of skill types."""

    ACTIVE = "active"
    PASSIVE = "passive"
    ULTIMATE = "ultimate"
    UTILITY = "utility"


class ElementalType(Enum):
    """Enumeration of elemental types for skills."""

    PHYSICAL = "physical"
    FIRE = "fire"
    ICE = "ice"
    LIGHTNING = "lightning"
    NATURE = "nature"
    CHAOS = "chaos"


class SkillsSystem:
    """
    Main skills system that handles all skill-related functionality.
    Manages skill trees, progression, and effects.
    """

    def __init__(
        self, player_system: PlayerSystem = None, class_system: ClassSystem = None
    ):
        """Initialize the skills system."""
        self.skills_database = self._initialize_skills_database()
        self.player_skills = {}  # player_id -> skill_data
        self.skill_cooldowns = {}  # player_id -> skill_cooldowns
        self.skill_synergies = self._initialize_skill_synergies()

        # Integrate with other systems
        self.player_system = player_system or PlayerSystem()
        self.class_system = class_system or ClassSystem()

    def get_max_skill_level(self, player_id: str, skill_id: str) -> int:
        """
        Calculate the maximum level a skill can reach based on Class Points invested in its subtype.

        Args:
            player_id: ID of the player
            skill_id: ID of the skill

        Returns:
            Maximum skill level (equal to Class Points invested in that subtype)
        """
        # Get skill data to determine subtype
        skill_data = self.get_skill(skill_id)
        if not skill_data:
            return 0

        skill_subtype = skill_data.get("subtype", "juggernaut")  # Default subtype
        skill_archetype = skill_data.get("archetype", "melee")

        # Get player data
        player_data = self.player_system.get_player(player_id)
        if not player_data:
            return 0

        # Check if player has this archetype
        player_archetypes = player_data.get("archetypes", {})
        if skill_archetype not in player_archetypes:
            return 0  # Can't level skills for archetypes you don't have

        # Get subtype point distribution for this archetype
        subtype_points = player_data.get("subtype_points", {}).get(skill_archetype, {})
        points_in_subtype = subtype_points.get(skill_subtype, 0)

        # Max skill level = Class Points invested in that specific subtype
        return points_in_subtype

    def can_access_ultimate(self, player_id: str, skill_id: str) -> Tuple[bool, str]:
        """
        Check if a player can access an ultimate skill (requires pure build).

        Args:
            player_id: ID of the player
            skill_id: ID of the ultimate skill

        Returns:
            Tuple of (can_access, error_message)
        """
        # Get skill data
        skill_data = self.get_skill(skill_id)
        if not skill_data:
            return False, "Skill not found"

        # Check if it's an ultimate skill
        if not skill_data.get("is_ultimate", False):
            return True, "Not an ultimate skill"  # Non-ultimates don't need pure build

        if not skill_data.get("requires_pure_build", False):
            return True, "Ultimate doesn't require pure build"

        skill_archetype = skill_data.get("archetype", "melee")
        skill_subtype = skill_data.get("subtype", "juggernaut")

        # Get player data
        player_data = self.player_system.get_player(player_id)
        if not player_data:
            return False, "Player not found"

        # Check if player has this archetype
        player_archetypes = player_data.get("archetypes", {})
        if skill_archetype not in player_archetypes:
            return False, f"Player does not have {skill_archetype} archetype"

        # For ultimate access, check BASE ARCHETYPE POINTS:
        # 1. Must have 3 base points in this archetype (pure build)
        # 2. Wild always gets ultimate access (chaos exception)

        # Get base archetype points (set at character creation)
        base_archetypes = player_data.get("base_archetypes", {})
        base_points_in_archetype = base_archetypes.get(skill_archetype, 0)

        # Wild exception: Wild always gets ultimate access
        if skill_archetype == "wild":
            if base_points_in_archetype > 0:
                return True, "Wild archetype always gets ultimate access"
            else:
                return False, "Player does not have Wild archetype"

        # For all other archetypes: must have exactly 3 base points (pure build)
        if base_points_in_archetype < 3:
            return (
                False,
                f"Ultimate requires pure {skill_archetype.title()} build (3 base points). You have {base_points_in_archetype} base points in {skill_archetype.title()}",
            )

        return True, "Pure build requirement met"

    def allocate_subtype_points(
        self, player_id: str, archetype: str, subtype: str, points: int
    ) -> Dict:
        """
        Allocate Class Points to a specific subtype within an archetype.

        Args:
            player_id: ID of the player
            archetype: Base archetype (melee, ranged, magic, wild)
            subtype: Specific subtype within archetype
            points: Number of points to allocate

        Returns:
            Result of the allocation attempt
        """
        player_data = self.player_system.get_player(player_id)
        if not player_data:
            return {"success": False, "error": "Player not found"}

        # Check if player has this archetype
        player_archetypes = player_data.get("archetypes", {})
        if archetype not in player_archetypes:
            return {
                "success": False,
                "error": f"Player does not have {archetype} archetype",
            }

        # Initialize subtype_points if not exists
        if "subtype_points" not in player_data:
            player_data["subtype_points"] = {}
        if archetype not in player_data["subtype_points"]:
            player_data["subtype_points"][archetype] = {}

        # Check available Class Points
        available_class_points = player_data["unused_points"]["class"]
        if available_class_points < points:
            return {
                "success": False,
                "error": f"Not enough Class Points (need {points}, have {available_class_points})",
            }

        # Check total point limits for archetype (max 3 points per archetype)
        current_total = sum(player_data["subtype_points"][archetype].values())
        if current_total + points > 3:
            return {
                "success": False,
                "error": f"Cannot exceed 3 points per archetype (current: {current_total}, adding: {points})",
            }

        # Allocate points
        if subtype not in player_data["subtype_points"][archetype]:
            player_data["subtype_points"][archetype][subtype] = 0

        player_data["subtype_points"][archetype][subtype] += points
        player_data["unused_points"]["class"] -= points

        return {
            "success": True,
            "archetype": archetype,
            "subtype": subtype,
            "points_allocated": points,
            "total_in_subtype": player_data["subtype_points"][archetype][subtype],
            "remaining_class_points": player_data["unused_points"]["class"],
        }

    def can_upgrade_skill(
        self, player_id: str, skill_id: str, points_to_spend: int = 1
    ) -> Tuple[bool, str]:
        """
        Check if a skill can be upgraded, considering archetype class point limits.

        Args:
            player_id: ID of the player
            skill_id: ID of the skill
            points_to_spend: Number of skill points to spend

        Returns:
            Tuple of (can_upgrade, error_message)
        """
        # Get skill data
        skill_data = self.get_skill(skill_id)
        if not skill_data:
            return False, "Skill not found"

        # Get player skills
        player_skills = self.get_player_skills(player_id)
        if skill_id not in player_skills["learned_skills"]:
            return False, "Skill not learned"

        # Get player data for skill points
        player_data = self.player_system.get_player(player_id)
        if not player_data:
            return False, "Player not found"

        # Check if player has enough skill points
        available_skill_points = player_data["unused_points"]["skill"]
        if available_skill_points < points_to_spend:
            return (
                False,
                f"Not enough Skill Points (need {points_to_spend}, have {available_skill_points})",
            )

        # Check current skill level and max allowed
        current_level = player_skills["learned_skills"][skill_id]["level"]
        max_allowed_level = self.get_max_skill_level(player_id, skill_id)

        if current_level + points_to_spend > max_allowed_level:
            skill_subtype = skill_data.get("subtype", "juggernaut")
            skill_archetype = skill_data.get("archetype", "melee")
            return (
                False,
                f"Skill level capped at {max_allowed_level} (spend more Class Points in {skill_subtype.title()} subtype of {skill_archetype.title()} archetype to increase cap)",
            )

        # Check ultimate access if this is an ultimate skill
        if skill_data.get("is_ultimate", False):
            can_access, access_error = self.can_access_ultimate(player_id, skill_id)
            if not can_access:
                return False, f"Cannot upgrade ultimate skill: {access_error}"

        return True, "Can upgrade"

    def _initialize_skills_database(self) -> Dict[str, Dict]:
        """Initialize the skills database organized by subtypes with 10 skills each."""
        return {
            # MELEE ARCHETYPE - JUGGERNAUT SUBTYPE (Tank/Defense Focus)
            "juggernaut_shield_slam": {
                "id": "juggernaut_shield_slam",
                "name": "Shield Slam",
                "type": SkillType.ACTIVE,
                "archetype": "melee",
                "subtype": "juggernaut",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 2, "max": 4},
                "cooldown": 2,
                "mana_cost": 5,
                "description": "Slam with shield, dealing damage and stunning",
                "status_effect": {"type": "stun", "chance": 0.3, "duration": 1.0},
                "prerequisites": [],
                "max_level": 10,
            },
            "juggernaut_iron_will": {
                "id": "juggernaut_iron_will",
                "name": "Iron Will",
                "type": SkillType.PASSIVE,
                "archetype": "melee",
                "subtype": "juggernaut",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Increased resistance to status effects",
                "status_effect": None,
                "prerequisites": [],
                "max_level": 10,
            },
            "juggernaut_heavy_armor": {
                "id": "juggernaut_heavy_armor",
                "name": "Heavy Armor Mastery",
                "type": SkillType.PASSIVE,
                "archetype": "melee",
                "subtype": "juggernaut",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Increased defense from heavy armor",
                "status_effect": None,
                "prerequisites": ["juggernaut_iron_will"],
                "max_level": 10,
            },
            "juggernaut_taunt": {
                "id": "juggernaut_taunt",
                "name": "Taunt",
                "type": SkillType.ACTIVE,
                "archetype": "melee",
                "subtype": "juggernaut",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 3,
                "mana_cost": 8,
                "description": "Force enemies to attack you",
                "status_effect": {"type": "taunt", "chance": 1.0, "duration": 3.0},
                "prerequisites": ["juggernaut_shield_slam"],
                "max_level": 10,
            },
            "juggernaut_crushing_blow": {
                "id": "juggernaut_crushing_blow",
                "name": "Crushing Blow",
                "type": SkillType.ACTIVE,
                "archetype": "melee",
                "subtype": "juggernaut",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 5, "max": 8},
                "cooldown": 4,
                "mana_cost": 12,
                "description": "Powerful two-handed weapon attack",
                "status_effect": {"type": "knockdown", "chance": 0.25, "duration": 1.5},
                "prerequisites": ["juggernaut_heavy_armor"],
                "max_level": 10,
            },
            "juggernaut_fortress": {
                "id": "juggernaut_fortress",
                "name": "Fortress Stance",
                "type": SkillType.ACTIVE,
                "archetype": "melee",
                "subtype": "juggernaut",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 10,
                "mana_cost": 15,
                "description": "Become immobile but nearly invulnerable",
                "status_effect": {"type": "fortress", "chance": 1.0, "duration": 5.0},
                "prerequisites": ["juggernaut_taunt"],
                "max_level": 10,
            },
            "juggernaut_shield_wall": {
                "id": "juggernaut_shield_wall",
                "name": "Shield Wall",
                "type": SkillType.ACTIVE,
                "archetype": "melee",
                "subtype": "juggernaut",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 8,
                "mana_cost": 20,
                "description": "Create protective barrier for allies",
                "status_effect": {
                    "type": "shield_wall",
                    "chance": 1.0,
                    "duration": 6.0,
                },
                "prerequisites": ["juggernaut_crushing_blow"],
                "max_level": 10,
            },
            "juggernaut_retribution": {
                "id": "juggernaut_retribution",
                "name": "Retribution",
                "type": SkillType.PASSIVE,
                "archetype": "melee",
                "subtype": "juggernaut",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Reflect damage back to attackers",
                "status_effect": None,
                "prerequisites": ["juggernaut_fortress"],
                "max_level": 10,
            },
            "juggernaut_unbreakable": {
                "id": "juggernaut_unbreakable",
                "name": "Unbreakable",
                "type": SkillType.PASSIVE,
                "archetype": "melee",
                "subtype": "juggernaut",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Become immune to crowd control at low health",
                "status_effect": None,
                "prerequisites": ["juggernaut_shield_wall", "juggernaut_retribution"],
                "max_level": 10,
            },
            "juggernaut_world_breaker": {
                "id": "juggernaut_world_breaker",
                "name": "World Breaker",
                "type": SkillType.ULTIMATE,
                "archetype": "melee",
                "subtype": "juggernaut",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 25, "max": 40},
                "cooldown": 30,
                "mana_cost": 50,
                "description": "ULTIMATE: Devastating area attack that shakes the earth",
                "status_effect": {"type": "earthquake", "chance": 1.0, "duration": 3.0},
                "prerequisites": ["juggernaut_unbreakable"],
                "max_level": 10,
                "is_ultimate": True,
                "requires_pure_build": True,
            },
            # MELEE ARCHETYPE - DUELIST SUBTYPE (Speed/Precision Focus)
            "duelist_quick_strike": {
                "id": "duelist_quick_strike",
                "name": "Quick Strike",
                "type": SkillType.ACTIVE,
                "archetype": "melee",
                "subtype": "duelist",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 3, "max": 5},
                "cooldown": 1,
                "mana_cost": 3,
                "description": "Fast attack with high crit chance",
                "status_effect": None,
                "prerequisites": [],
                "max_level": 10,
            },
            "duelist_parry": {
                "id": "duelist_parry",
                "name": "Parry",
                "type": SkillType.ACTIVE,
                "archetype": "melee",
                "subtype": "duelist",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 3,
                "mana_cost": 5,
                "description": "Block and counter-attack",
                "status_effect": {"type": "counter", "chance": 1.0, "duration": 2.0},
                "prerequisites": [],
                "max_level": 10,
            },
            "duelist_dual_wield": {
                "id": "duelist_dual_wield",
                "name": "Dual Wield Mastery",
                "type": SkillType.PASSIVE,
                "archetype": "melee",
                "subtype": "duelist",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Increased attack speed with two weapons",
                "status_effect": None,
                "prerequisites": ["duelist_quick_strike"],
                "max_level": 10,
            },
            "duelist_riposte": {
                "id": "duelist_riposte",
                "name": "Riposte",
                "type": SkillType.ACTIVE,
                "archetype": "melee",
                "subtype": "duelist",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 6, "max": 10},
                "cooldown": 4,
                "mana_cost": 8,
                "description": "Counter-attack after successful parry",
                "status_effect": None,
                "prerequisites": ["duelist_parry"],
                "max_level": 10,
            },
            "duelist_flurry": {
                "id": "duelist_flurry",
                "name": "Flurry",
                "type": SkillType.ACTIVE,
                "archetype": "melee",
                "subtype": "duelist",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 2, "max": 4},
                "cooldown": 5,
                "mana_cost": 12,
                "description": "Multiple rapid attacks",
                "status_effect": None,
                "prerequisites": ["duelist_dual_wield"],
                "max_level": 10,
            },
            "duelist_precision": {
                "id": "duelist_precision",
                "name": "Precision",
                "type": SkillType.PASSIVE,
                "archetype": "melee",
                "subtype": "duelist",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Increased critical hit chance and damage",
                "status_effect": None,
                "prerequisites": ["duelist_riposte"],
                "max_level": 10,
            },
            "duelist_dance_of_blades": {
                "id": "duelist_dance_of_blades",
                "name": "Dance of Blades",
                "type": SkillType.ACTIVE,
                "archetype": "melee",
                "subtype": "duelist",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 4, "max": 7},
                "cooldown": 6,
                "mana_cost": 15,
                "description": "Graceful combo that hits multiple times",
                "status_effect": None,
                "prerequisites": ["duelist_flurry"],
                "max_level": 10,
            },
            "duelist_perfect_balance": {
                "id": "duelist_perfect_balance",
                "name": "Perfect Balance",
                "type": SkillType.PASSIVE,
                "archetype": "melee",
                "subtype": "duelist",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Immune to knockdown, increased dodge",
                "status_effect": None,
                "prerequisites": ["duelist_precision"],
                "max_level": 10,
            },
            "duelist_masterwork": {
                "id": "duelist_masterwork",
                "name": "Masterwork Technique",
                "type": SkillType.PASSIVE,
                "archetype": "melee",
                "subtype": "duelist",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "All attacks have perfect form",
                "status_effect": None,
                "prerequisites": ["duelist_dance_of_blades", "duelist_perfect_balance"],
                "max_level": 10,
            },
            "duelist_thousand_cuts": {
                "id": "duelist_thousand_cuts",
                "name": "Thousand Cuts",
                "type": SkillType.ULTIMATE,
                "archetype": "melee",
                "subtype": "duelist",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 20, "max": 35},
                "cooldown": 25,
                "mana_cost": 40,
                "description": "ULTIMATE: Unleash a storm of precise strikes",
                "status_effect": {
                    "type": "bleeding_storm",
                    "chance": 1.0,
                    "duration": 5.0,
                },
                "prerequisites": ["duelist_masterwork"],
                "max_level": 10,
                "is_ultimate": True,
                "requires_pure_build": True,
            },
            # MELEE ARCHETYPE - BERSERKER SUBTYPE (Rage/Damage Focus)
            "berserker_rage": {
                "id": "berserker_rage",
                "name": "Berserker Rage",
                "type": SkillType.ACTIVE,
                "archetype": "melee",
                "subtype": "berserker",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 8,
                "mana_cost": 10,
                "description": "Enter rage state, increased damage but reduced defense",
                "status_effect": {"type": "rage", "chance": 1.0, "duration": 6.0},
                "prerequisites": [],
                "max_level": 10,
            },
            "berserker_wild_swing": {
                "id": "berserker_wild_swing",
                "name": "Wild Swing",
                "type": SkillType.ACTIVE,
                "archetype": "melee",
                "subtype": "berserker",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 4, "max": 8},
                "cooldown": 2,
                "mana_cost": 6,
                "description": "Reckless attack with high damage variance",
                "status_effect": None,
                "prerequisites": [],
                "max_level": 10,
            },
            "berserker_bloodlust": {
                "id": "berserker_bloodlust",
                "name": "Bloodlust",
                "type": SkillType.PASSIVE,
                "archetype": "melee",
                "subtype": "berserker",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Heal when defeating enemies",
                "status_effect": None,
                "prerequisites": ["berserker_rage"],
                "max_level": 10,
            },
            "berserker_rampage": {
                "id": "berserker_rampage",
                "name": "Rampage",
                "type": SkillType.ACTIVE,
                "archetype": "melee",
                "subtype": "berserker",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 6, "max": 12},
                "cooldown": 5,
                "mana_cost": 15,
                "description": "Area attack that grows stronger with each kill",
                "status_effect": None,
                "prerequisites": ["berserker_wild_swing"],
                "max_level": 10,
            },
            "berserker_intimidate": {
                "id": "berserker_intimidate",
                "name": "Intimidate",
                "type": SkillType.ACTIVE,
                "archetype": "melee",
                "subtype": "berserker",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 6,
                "mana_cost": 8,
                "description": "Frighten enemies, reducing their damage",
                "status_effect": {"type": "fear", "chance": 0.8, "duration": 4.0},
                "prerequisites": ["berserker_bloodlust"],
                "max_level": 10,
            },
            "berserker_frenzy": {
                "id": "berserker_frenzy",
                "name": "Frenzy",
                "type": SkillType.ACTIVE,
                "archetype": "melee",
                "subtype": "berserker",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 8, "max": 15},
                "cooldown": 7,
                "mana_cost": 20,
                "description": "Attack speed and damage increase dramatically",
                "status_effect": {"type": "frenzy", "chance": 1.0, "duration": 5.0},
                "prerequisites": ["berserker_rampage"],
                "max_level": 10,
            },
            "berserker_unstoppable": {
                "id": "berserker_unstoppable",
                "name": "Unstoppable Force",
                "type": SkillType.PASSIVE,
                "archetype": "melee",
                "subtype": "berserker",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Cannot be slowed or stopped while raging",
                "status_effect": None,
                "prerequisites": ["berserker_intimidate"],
                "max_level": 10,
            },
            "berserker_blood_for_blood": {
                "id": "berserker_blood_for_blood",
                "name": "Blood for Blood",
                "type": SkillType.ACTIVE,
                "archetype": "melee",
                "subtype": "berserker",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 10,
                "mana_cost": 0,
                "description": "Sacrifice health for massive damage boost",
                "status_effect": {
                    "type": "blood_sacrifice",
                    "chance": 1.0,
                    "duration": 3.0,
                },
                "prerequisites": ["berserker_frenzy"],
                "max_level": 10,
            },
            "berserker_endless_rage": {
                "id": "berserker_endless_rage",
                "name": "Endless Rage",
                "type": SkillType.PASSIVE,
                "archetype": "melee",
                "subtype": "berserker",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Rage duration extended with each kill",
                "status_effect": None,
                "prerequisites": ["berserker_unstoppable", "berserker_blood_for_blood"],
                "max_level": 10,
            },
            "berserker_world_ender": {
                "id": "berserker_world_ender",
                "name": "World Ender",
                "type": SkillType.ULTIMATE,
                "archetype": "melee",
                "subtype": "berserker",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 30, "max": 50},
                "cooldown": 35,
                "mana_cost": 0,
                "description": "ULTIMATE: Become an unstoppable force of destruction",
                "status_effect": {"type": "apocalypse", "chance": 1.0, "duration": 8.0},
                "prerequisites": ["berserker_endless_rage"],
                "max_level": 10,
                "is_ultimate": True,
                "requires_pure_build": True,
            },
            # RANGED ARCHETYPE - MARKSMAN SUBTYPE (Precision/Damage Focus)
            "marksman_precise_shot": {
                "id": "marksman_precise_shot",
                "name": "Precise Shot",
                "type": SkillType.ACTIVE,
                "archetype": "ranged",
                "subtype": "marksman",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 3, "max": 6},
                "cooldown": 1,
                "mana_cost": 3,
                "description": "High accuracy shot with increased critical chance",
                "status_effect": {
                    "type": "vulnerability",
                    "chance": 0.2,
                    "duration": 2.0,
                },
                "prerequisites": [],
                "max_level": 10,
            },
            "marksman_quick_draw": {
                "id": "marksman_quick_draw",
                "name": "Quick Draw",
                "type": SkillType.PASSIVE,
                "archetype": "ranged",
                "subtype": "marksman",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Increased attack speed and reload time",
                "status_effect": None,
                "prerequisites": [],
                "max_level": 10,
            },
            "marksman_dead_eye": {
                "id": "marksman_dead_eye",
                "name": "Dead Eye",
                "type": SkillType.PASSIVE,
                "archetype": "ranged",
                "subtype": "marksman",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Increased critical chance and critical damage",
                "status_effect": None,
                "prerequisites": ["marksman_quick_draw"],
                "max_level": 10,
            },
            "marksman_piercing_shot": {
                "id": "marksman_piercing_shot",
                "name": "Piercing Shot",
                "type": SkillType.ACTIVE,
                "archetype": "ranged",
                "subtype": "marksman",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 6, "max": 12},
                "cooldown": 3,
                "mana_cost": 8,
                "description": "Shot that penetrates armor and hits multiple targets",
                "status_effect": {
                    "type": "armor_break",
                    "chance": 0.4,
                    "duration": 3.0,
                },
                "prerequisites": ["marksman_precise_shot"],
                "max_level": 10,
            },
            "marksman_head_hunter": {
                "id": "marksman_head_hunter",
                "name": "Head Hunter",
                "type": SkillType.ACTIVE,
                "archetype": "ranged",
                "subtype": "marksman",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 8, "max": 15},
                "cooldown": 5,
                "mana_cost": 12,
                "description": "High damage shot with guaranteed critical on weak enemies",
                "status_effect": {"type": "execution", "chance": 0.6, "duration": 1.0},
                "prerequisites": ["marksman_dead_eye"],
                "max_level": 10,
            },
            "marksman_steady_aim": {
                "id": "marksman_steady_aim",
                "name": "Steady Aim",
                "type": SkillType.ACTIVE,
                "archetype": "ranged",
                "subtype": "marksman",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 8,
                "mana_cost": 10,
                "description": "Take time to aim for massive damage increase",
                "status_effect": {"type": "steady_aim", "chance": 1.0, "duration": 4.0},
                "prerequisites": ["marksman_piercing_shot"],
                "max_level": 10,
            },
            "marksman_rapid_fire": {
                "id": "marksman_rapid_fire",
                "name": "Rapid Fire",
                "type": SkillType.ACTIVE,
                "archetype": "ranged",
                "subtype": "marksman",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 2, "max": 4},
                "cooldown": 6,
                "mana_cost": 15,
                "description": "Fire multiple shots in quick succession",
                "status_effect": {"type": "barrage", "chance": 1.0, "duration": 3.0},
                "prerequisites": ["marksman_head_hunter"],
                "max_level": 10,
            },
            "marksman_sniper_mastery": {
                "id": "marksman_sniper_mastery",
                "name": "Sniper Mastery",
                "type": SkillType.PASSIVE,
                "archetype": "ranged",
                "subtype": "marksman",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Increased damage at long range",
                "status_effect": None,
                "prerequisites": ["marksman_steady_aim"],
                "max_level": 10,
            },
            "marksman_perfect_shot": {
                "id": "marksman_perfect_shot",
                "name": "Perfect Shot",
                "type": SkillType.ACTIVE,
                "archetype": "ranged",
                "subtype": "marksman",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 15, "max": 25},
                "cooldown": 12,
                "mana_cost": 20,
                "description": "Ultimate precision shot with massive damage",
                "status_effect": {
                    "type": "perfect_hit",
                    "chance": 1.0,
                    "duration": 2.0,
                },
                "prerequisites": ["marksman_sniper_mastery", "marksman_rapid_fire"],
                "max_level": 10,
            },
            "marksman_death_mark": {
                "id": "marksman_death_mark",
                "name": "Death Mark",
                "type": SkillType.ULTIMATE,
                "archetype": "ranged",
                "subtype": "marksman",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 25, "max": 40},
                "cooldown": 30,
                "mana_cost": 40,
                "description": "ULTIMATE: Mark target for instant death on next hit",
                "status_effect": {"type": "death_mark", "chance": 1.0, "duration": 5.0},
                "prerequisites": ["marksman_perfect_shot"],
                "max_level": 10,
                "is_ultimate": True,
                "requires_pure_build": True,
            },
            # RANGED ARCHETYPE - TRAPPER SUBTYPE (Control/Defense Focus)
            "trapper_bear_trap": {
                "id": "trapper_bear_trap",
                "name": "Bear Trap",
                "type": SkillType.ACTIVE,
                "archetype": "ranged",
                "subtype": "trapper",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 1, "max": 3},
                "cooldown": 2,
                "mana_cost": 5,
                "description": "Place a trap that roots enemies",
                "status_effect": {"type": "root", "chance": 0.8, "duration": 3.0},
                "prerequisites": [],
                "max_level": 10,
            },
            "trapper_net_throw": {
                "id": "trapper_net_throw",
                "name": "Net Throw",
                "type": SkillType.ACTIVE,
                "archetype": "ranged",
                "subtype": "trapper",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 3,
                "mana_cost": 6,
                "description": "Throw a net to slow and entangle enemies",
                "status_effect": {"type": "entangle", "chance": 0.7, "duration": 4.0},
                "prerequisites": ["trapper_bear_trap"],
                "max_level": 10,
            },
            "trapper_caltrops": {
                "id": "trapper_caltrops",
                "name": "Caltrops",
                "type": SkillType.ACTIVE,
                "archetype": "ranged",
                "subtype": "trapper",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 1, "max": 2},
                "cooldown": 4,
                "mana_cost": 8,
                "description": "Scatter caltrops that slow and damage enemies",
                "status_effect": {"type": "bleed", "chance": 0.5, "duration": 5.0},
                "prerequisites": ["trapper_net_throw"],
                "max_level": 10,
            },
            "trapper_smoke_bomb": {
                "id": "trapper_smoke_bomb",
                "name": "Smoke Bomb",
                "type": SkillType.ACTIVE,
                "archetype": "ranged",
                "subtype": "trapper",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 6,
                "mana_cost": 10,
                "description": "Create smoke screen for stealth and evasion",
                "status_effect": {
                    "type": "smoke_screen",
                    "chance": 1.0,
                    "duration": 6.0,
                },
                "prerequisites": ["trapper_caltrops"],
                "max_level": 10,
            },
            "trapper_poison_trap": {
                "id": "trapper_poison_trap",
                "name": "Poison Trap",
                "type": SkillType.ACTIVE,
                "archetype": "ranged",
                "subtype": "trapper",
                "elemental_type": ElementalType.NATURE,
                "base_damage": {"min": 2, "max": 4},
                "cooldown": 5,
                "mana_cost": 12,
                "description": "Place a trap that poisons enemies over time",
                "status_effect": {"type": "poison", "chance": 0.9, "duration": 8.0},
                "prerequisites": ["trapper_smoke_bomb"],
                "max_level": 10,
            },
            "trapper_ice_trap": {
                "id": "trapper_ice_trap",
                "name": "Ice Trap",
                "type": SkillType.ACTIVE,
                "archetype": "ranged",
                "subtype": "trapper",
                "elemental_type": ElementalType.ICE,
                "base_damage": {"min": 3, "max": 6},
                "cooldown": 7,
                "mana_cost": 15,
                "description": "Place a trap that freezes enemies",
                "status_effect": {"type": "freeze", "chance": 0.6, "duration": 4.0},
                "prerequisites": ["trapper_poison_trap"],
                "max_level": 10,
            },
            "trapper_chain_trap": {
                "id": "trapper_chain_trap",
                "name": "Chain Trap",
                "type": SkillType.ACTIVE,
                "archetype": "ranged",
                "subtype": "trapper",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 4, "max": 8},
                "cooldown": 8,
                "mana_cost": 18,
                "description": "Create multiple linked traps",
                "status_effect": {
                    "type": "chain_reaction",
                    "chance": 1.0,
                    "duration": 5.0,
                },
                "prerequisites": ["trapper_ice_trap"],
                "max_level": 10,
            },
            "trapper_master_trapper": {
                "id": "trapper_master_trapper",
                "name": "Master Trapper",
                "type": SkillType.PASSIVE,
                "archetype": "ranged",
                "subtype": "trapper",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Increased trap effectiveness and duration",
                "status_effect": None,
                "prerequisites": ["trapper_chain_trap"],
                "max_level": 10,
            },
            "trapper_death_trap": {
                "id": "trapper_death_trap",
                "name": "Death Trap",
                "type": SkillType.ULTIMATE,
                "archetype": "ranged",
                "subtype": "trapper",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 20, "max": 35},
                "cooldown": 25,
                "mana_cost": 30,
                "description": "ULTIMATE: Create a deadly trap field",
                "status_effect": {
                    "type": "death_field",
                    "chance": 1.0,
                    "duration": 10.0,
                },
                "prerequisites": ["trapper_master_trapper"],
                "max_level": 10,
                "is_ultimate": True,
                "requires_pure_build": True,
            },
            # RANGED ARCHETYPE - GUNSLINGER SUBTYPE (High-Risk/High-Reward)
            "gunslinger_quick_draw": {
                "id": "gunslinger_quick_draw",
                "name": "Quick Draw",
                "type": SkillType.ACTIVE,
                "archetype": "ranged",
                "subtype": "gunslinger",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 4, "max": 8},
                "cooldown": 1,
                "mana_cost": 4,
                "description": "Fast draw with high critical chance",
                "status_effect": {"type": "quick_draw", "chance": 0.3, "duration": 1.0},
                "prerequisites": [],
                "max_level": 10,
            },
            "gunslinger_fan_the_hammer": {
                "id": "gunslinger_fan_the_hammer",
                "name": "Fan the Hammer",
                "type": SkillType.ACTIVE,
                "archetype": "ranged",
                "subtype": "gunslinger",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 2, "max": 5},
                "cooldown": 3,
                "mana_cost": 8,
                "description": "Rapid fire multiple shots",
                "status_effect": {"type": "barrage", "chance": 1.0, "duration": 2.0},
                "prerequisites": ["gunslinger_quick_draw"],
                "max_level": 10,
            },
            "gunslinger_duel": {
                "id": "gunslinger_duel",
                "name": "Duel",
                "type": SkillType.ACTIVE,
                "archetype": "ranged",
                "subtype": "gunslinger",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 8, "max": 16},
                "cooldown": 5,
                "mana_cost": 12,
                "description": "High-risk, high-reward single shot",
                "status_effect": {"type": "duel", "chance": 0.5, "duration": 3.0},
                "prerequisites": ["gunslinger_fan_the_hammer"],
                "max_level": 10,
            },
            "gunslinger_ricochet": {
                "id": "gunslinger_ricochet",
                "name": "Ricochet",
                "type": SkillType.ACTIVE,
                "archetype": "ranged",
                "subtype": "gunslinger",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 3, "max": 7},
                "cooldown": 4,
                "mana_cost": 10,
                "description": "Shot that bounces between enemies",
                "status_effect": {"type": "ricochet", "chance": 0.7, "duration": 2.0},
                "prerequisites": ["gunslinger_duel"],
                "max_level": 10,
            },
            "gunslinger_dead_man_hand": {
                "id": "gunslinger_dead_man_hand",
                "name": "Dead Man's Hand",
                "type": SkillType.ACTIVE,
                "archetype": "ranged",
                "subtype": "gunslinger",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 6, "max": 12},
                "cooldown": 6,
                "mana_cost": 15,
                "description": "Desperate attack with unpredictable results",
                "status_effect": {"type": "chaos_shot", "chance": 0.4, "duration": 3.0},
                "prerequisites": ["gunslinger_ricochet"],
                "max_level": 10,
            },
            "gunslinger_lucky_shot": {
                "id": "gunslinger_lucky_shot",
                "name": "Lucky Shot",
                "type": SkillType.PASSIVE,
                "archetype": "ranged",
                "subtype": "gunslinger",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Chance for shots to have unexpected effects",
                "status_effect": None,
                "prerequisites": ["gunslinger_dead_man_hand"],
                "max_level": 10,
            },
            "gunslinger_high_noon": {
                "id": "gunslinger_high_noon",
                "name": "High Noon",
                "type": SkillType.ACTIVE,
                "archetype": "ranged",
                "subtype": "gunslinger",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 10, "max": 20},
                "cooldown": 10,
                "mana_cost": 25,
                "description": "Dramatic showdown with massive damage potential",
                "status_effect": {"type": "high_noon", "chance": 1.0, "duration": 5.0},
                "prerequisites": ["gunslinger_lucky_shot"],
                "max_level": 10,
            },
            "gunslinger_ace_up_sleeve": {
                "id": "gunslinger_ace_up_sleeve",
                "name": "Ace Up Sleeve",
                "type": SkillType.PASSIVE,
                "archetype": "ranged",
                "subtype": "gunslinger",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Hidden advantage in critical situations",
                "status_effect": None,
                "prerequisites": ["gunslinger_high_noon"],
                "max_level": 10,
            },
            "gunslinger_last_stand": {
                "id": "gunslinger_last_stand",
                "name": "Last Stand",
                "type": SkillType.ULTIMATE,
                "archetype": "ranged",
                "subtype": "gunslinger",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 30, "max": 60},
                "cooldown": 40,
                "mana_cost": 0,
                "description": "ULTIMATE: Final desperate attack with everything",
                "status_effect": {"type": "last_stand", "chance": 1.0, "duration": 8.0},
                "prerequisites": ["gunslinger_ace_up_sleeve"],
                "max_level": 10,
                "is_ultimate": True,
                "requires_pure_build": True,
            },
            # MAGIC ARCHETYPE - ELEMENTALIST SUBTYPE (Burn/Power Focus)
            "elementalist_fireball": {
                "id": "elementalist_fireball",
                "name": "Fireball",
                "type": SkillType.ACTIVE,
                "archetype": "magic",
                "subtype": "elementalist",
                "elemental_type": ElementalType.FIRE,
                "base_damage": {"min": 4, "max": 8},
                "cooldown": 2,
                "mana_cost": 6,
                "description": "Launch a ball of fire that burns enemies",
                "status_effect": {"type": "burn", "chance": 0.6, "duration": 3.0},
                "prerequisites": [],
                "max_level": 10,
            },
            "elementalist_flame_burst": {
                "id": "elementalist_flame_burst",
                "name": "Flame Burst",
                "type": SkillType.ACTIVE,
                "archetype": "magic",
                "subtype": "elementalist",
                "elemental_type": ElementalType.FIRE,
                "base_damage": {"min": 6, "max": 12},
                "cooldown": 4,
                "mana_cost": 10,
                "description": "Explosive burst of flames",
                "status_effect": {"type": "burn", "chance": 0.8, "duration": 4.0},
                "prerequisites": ["elementalist_fireball"],
                "max_level": 10,
            },
            "elementalist_heat_wave": {
                "id": "elementalist_heat_wave",
                "name": "Heat Wave",
                "type": SkillType.ACTIVE,
                "archetype": "magic",
                "subtype": "elementalist",
                "elemental_type": ElementalType.FIRE,
                "base_damage": {"min": 3, "max": 6},
                "cooldown": 3,
                "mana_cost": 8,
                "description": "Wave of heat that damages over time",
                "status_effect": {"type": "burn", "chance": 0.7, "duration": 5.0},
                "prerequisites": ["elementalist_flame_burst"],
                "max_level": 10,
            },
            "elementalist_inferno": {
                "id": "elementalist_inferno",
                "name": "Inferno",
                "type": SkillType.ACTIVE,
                "archetype": "magic",
                "subtype": "elementalist",
                "elemental_type": ElementalType.FIRE,
                "base_damage": {"min": 8, "max": 15},
                "cooldown": 6,
                "mana_cost": 15,
                "description": "Create a raging inferno",
                "status_effect": {"type": "burn", "chance": 0.9, "duration": 6.0},
                "prerequisites": ["elementalist_heat_wave"],
                "max_level": 10,
            },
            "elementalist_phoenix_flame": {
                "id": "elementalist_phoenix_flame",
                "name": "Phoenix Flame",
                "type": SkillType.ACTIVE,
                "archetype": "magic",
                "subtype": "elementalist",
                "elemental_type": ElementalType.FIRE,
                "base_damage": {"min": 10, "max": 18},
                "cooldown": 8,
                "mana_cost": 20,
                "description": "Mystical flame that resurrects on death",
                "status_effect": {
                    "type": "phoenix_rebirth",
                    "chance": 0.3,
                    "duration": 2.0,
                },
                "prerequisites": ["elementalist_inferno"],
                "max_level": 10,
            },
            "elementalist_molten_armor": {
                "id": "elementalist_molten_armor",
                "name": "Molten Armor",
                "type": SkillType.PASSIVE,
                "archetype": "magic",
                "subtype": "elementalist",
                "elemental_type": ElementalType.FIRE,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Burning armor that damages attackers",
                "status_effect": None,
                "prerequisites": ["elementalist_phoenix_flame"],
                "max_level": 10,
            },
            "elementalist_volcanic_eruption": {
                "id": "elementalist_volcanic_eruption",
                "name": "Volcanic Eruption",
                "type": SkillType.ACTIVE,
                "archetype": "magic",
                "subtype": "elementalist",
                "elemental_type": ElementalType.FIRE,
                "base_damage": {"min": 12, "max": 22},
                "cooldown": 10,
                "mana_cost": 25,
                "description": "Erupt the ground with molten lava",
                "status_effect": {"type": "burn", "chance": 1.0, "duration": 8.0},
                "prerequisites": ["elementalist_molten_armor"],
                "max_level": 10,
            },
            "elementalist_fire_mastery": {
                "id": "elementalist_fire_mastery",
                "name": "Fire Mastery",
                "type": SkillType.PASSIVE,
                "archetype": "magic",
                "subtype": "elementalist",
                "elemental_type": ElementalType.FIRE,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Mastery of fire magic increases all fire damage",
                "status_effect": None,
                "prerequisites": ["elementalist_volcanic_eruption"],
                "max_level": 10,
            },
            "elementalist_solar_flare": {
                "id": "elementalist_solar_flare",
                "name": "Solar Flare",
                "type": SkillType.ULTIMATE,
                "archetype": "magic",
                "subtype": "elementalist",
                "elemental_type": ElementalType.FIRE,
                "base_damage": {"min": 25, "max": 45},
                "cooldown": 30,
                "mana_cost": 50,
                "description": "ULTIMATE: Channel the power of the sun",
                "status_effect": {
                    "type": "solar_burn",
                    "chance": 1.0,
                    "duration": 10.0,
                },
                "prerequisites": ["elementalist_fire_mastery"],
                "max_level": 10,
                "is_ultimate": True,
                "requires_pure_build": True,
            },
            # MAGIC ARCHETYPE - ARCANIST SUBTYPE (Frost/Defense Focus)
            "arcanist_frost_bolt": {
                "id": "arcanist_frost_bolt",
                "name": "Frost Bolt",
                "type": SkillType.ACTIVE,
                "archetype": "magic",
                "subtype": "arcanist",
                "elemental_type": ElementalType.ICE,
                "base_damage": {"min": 3, "max": 6},
                "cooldown": 2,
                "mana_cost": 5,
                "description": "Launch a bolt of ice that slows enemies",
                "status_effect": {"type": "slow", "chance": 0.5, "duration": 3.0},
                "prerequisites": [],
                "max_level": 10,
            },
            "arcanist_ice_shield": {
                "id": "arcanist_ice_shield",
                "name": "Ice Shield",
                "type": SkillType.ACTIVE,
                "archetype": "magic",
                "subtype": "arcanist",
                "elemental_type": ElementalType.ICE,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 4,
                "mana_cost": 8,
                "description": "Create a protective ice barrier",
                "status_effect": {"type": "ice_shield", "chance": 1.0, "duration": 5.0},
                "prerequisites": ["arcanist_frost_bolt"],
                "max_level": 10,
            },
            "arcanist_blizzard": {
                "id": "arcanist_blizzard",
                "name": "Blizzard",
                "type": SkillType.ACTIVE,
                "archetype": "magic",
                "subtype": "arcanist",
                "elemental_type": ElementalType.ICE,
                "base_damage": {"min": 5, "max": 10},
                "cooldown": 6,
                "mana_cost": 12,
                "description": "Create a blizzard that freezes enemies",
                "status_effect": {"type": "freeze", "chance": 0.4, "duration": 4.0},
                "prerequisites": ["arcanist_ice_shield"],
                "max_level": 10,
            },
            "arcanist_frost_nova": {
                "id": "arcanist_frost_nova",
                "name": "Frost Nova",
                "type": SkillType.ACTIVE,
                "archetype": "magic",
                "subtype": "arcanist",
                "elemental_type": ElementalType.ICE,
                "base_damage": {"min": 4, "max": 8},
                "cooldown": 5,
                "mana_cost": 10,
                "description": "Explosive burst of ice energy",
                "status_effect": {"type": "freeze", "chance": 0.6, "duration": 3.0},
                "prerequisites": ["arcanist_blizzard"],
                "max_level": 10,
            },
            "arcanist_ice_prison": {
                "id": "arcanist_ice_prison",
                "name": "Ice Prison",
                "type": SkillType.ACTIVE,
                "archetype": "magic",
                "subtype": "arcanist",
                "elemental_type": ElementalType.ICE,
                "base_damage": {"min": 2, "max": 4},
                "cooldown": 8,
                "mana_cost": 15,
                "description": "Trap enemies in ice",
                "status_effect": {"type": "freeze", "chance": 0.8, "duration": 6.0},
                "prerequisites": ["arcanist_frost_nova"],
                "max_level": 10,
            },
            "arcanist_glacial_armor": {
                "id": "arcanist_glacial_armor",
                "name": "Glacial Armor",
                "type": SkillType.PASSIVE,
                "archetype": "magic",
                "subtype": "arcanist",
                "elemental_type": ElementalType.ICE,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Armor of ice that freezes attackers",
                "status_effect": None,
                "prerequisites": ["arcanist_ice_prison"],
                "max_level": 10,
            },
            "arcanist_ice_storm": {
                "id": "arcanist_ice_storm",
                "name": "Ice Storm",
                "type": SkillType.ACTIVE,
                "archetype": "magic",
                "subtype": "arcanist",
                "elemental_type": ElementalType.ICE,
                "base_damage": {"min": 8, "max": 15},
                "cooldown": 10,
                "mana_cost": 20,
                "description": "Summon a devastating ice storm",
                "status_effect": {"type": "freeze", "chance": 0.7, "duration": 5.0},
                "prerequisites": ["arcanist_glacial_armor"],
                "max_level": 10,
            },
            "arcanist_frost_mastery": {
                "id": "arcanist_frost_mastery",
                "name": "Frost Mastery",
                "type": SkillType.PASSIVE,
                "archetype": "magic",
                "subtype": "arcanist",
                "elemental_type": ElementalType.ICE,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Mastery of ice magic increases all ice effects",
                "status_effect": None,
                "prerequisites": ["arcanist_ice_storm"],
                "max_level": 10,
            },
            "arcanist_eternal_winter": {
                "id": "arcanist_eternal_winter",
                "name": "Eternal Winter",
                "type": SkillType.ULTIMATE,
                "archetype": "magic",
                "subtype": "arcanist",
                "elemental_type": ElementalType.ICE,
                "base_damage": {"min": 20, "max": 35},
                "cooldown": 25,
                "mana_cost": 40,
                "description": "ULTIMATE: Bring eternal winter to the battlefield",
                "status_effect": {
                    "type": "eternal_freeze",
                    "chance": 1.0,
                    "duration": 8.0,
                },
                "prerequisites": ["arcanist_frost_mastery"],
                "max_level": 10,
                "is_ultimate": True,
                "requires_pure_build": True,
            },
            # MAGIC ARCHETYPE - OCCULTIST SUBTYPE (Lightning/Chaos Focus)
            "occultist_lightning_bolt": {
                "id": "occultist_lightning_bolt",
                "name": "Lightning Bolt",
                "type": SkillType.ACTIVE,
                "archetype": "magic",
                "subtype": "occultist",
                "elemental_type": ElementalType.LIGHTNING,
                "base_damage": {"min": 5, "max": 10},
                "cooldown": 2,
                "mana_cost": 6,
                "description": "Cast a bolt of lightning with high stun chance",
                "status_effect": {"type": "stun", "chance": 0.3, "duration": 2.0},
                "prerequisites": [],
                "max_level": 10,
            },
            "occultist_chain_lightning": {
                "id": "occultist_chain_lightning",
                "name": "Chain Lightning",
                "type": SkillType.ACTIVE,
                "archetype": "magic",
                "subtype": "occultist",
                "elemental_type": ElementalType.LIGHTNING,
                "base_damage": {"min": 4, "max": 8},
                "cooldown": 3,
                "mana_cost": 8,
                "description": "Lightning that chains between enemies",
                "status_effect": {"type": "stun", "chance": 0.2, "duration": 1.5},
                "prerequisites": ["occultist_lightning_bolt"],
                "max_level": 10,
            },
            "occultist_thunder_clap": {
                "id": "occultist_thunder_clap",
                "name": "Thunder Clap",
                "type": SkillType.ACTIVE,
                "archetype": "magic",
                "subtype": "occultist",
                "elemental_type": ElementalType.LIGHTNING,
                "base_damage": {"min": 6, "max": 12},
                "cooldown": 4,
                "mana_cost": 10,
                "description": "Thunderous clap that stuns and damages",
                "status_effect": {"type": "stun", "chance": 0.5, "duration": 2.5},
                "prerequisites": ["occultist_chain_lightning"],
                "max_level": 10,
            },
            "occultist_static_field": {
                "id": "occultist_static_field",
                "name": "Static Field",
                "type": SkillType.ACTIVE,
                "archetype": "magic",
                "subtype": "occultist",
                "elemental_type": ElementalType.LIGHTNING,
                "base_damage": {"min": 2, "max": 5},
                "cooldown": 5,
                "mana_cost": 12,
                "description": "Create a field of static electricity",
                "status_effect": {"type": "shock", "chance": 0.6, "duration": 4.0},
                "prerequisites": ["occultist_thunder_clap"],
                "max_level": 10,
            },
            "occultist_lightning_storm": {
                "id": "occultist_lightning_storm",
                "name": "Lightning Storm",
                "type": SkillType.ACTIVE,
                "archetype": "magic",
                "subtype": "occultist",
                "elemental_type": ElementalType.LIGHTNING,
                "base_damage": {"min": 8, "max": 16},
                "cooldown": 8,
                "mana_cost": 18,
                "description": "Summon a storm of lightning",
                "status_effect": {"type": "stun", "chance": 0.4, "duration": 3.0},
                "prerequisites": ["occultist_static_field"],
                "max_level": 10,
            },
            "occultist_chaos_bolt": {
                "id": "occultist_chaos_bolt",
                "name": "Chaos Bolt",
                "type": SkillType.ACTIVE,
                "archetype": "magic",
                "subtype": "occultist",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 10, "max": 20},
                "cooldown": 6,
                "mana_cost": 15,
                "description": "Unpredictable bolt with random effects",
                "status_effect": {"type": "chaos", "chance": 0.7, "duration": 3.0},
                "prerequisites": ["occultist_lightning_storm"],
                "max_level": 10,
            },
            "occultist_void_magic": {
                "id": "occultist_void_magic",
                "name": "Void Magic",
                "type": SkillType.PASSIVE,
                "archetype": "magic",
                "subtype": "occultist",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Mastery of chaotic void magic",
                "status_effect": None,
                "prerequisites": ["occultist_chaos_bolt"],
                "max_level": 10,
            },
            "occultist_reality_tear": {
                "id": "occultist_reality_tear",
                "name": "Reality Tear",
                "type": SkillType.ACTIVE,
                "archetype": "magic",
                "subtype": "occultist",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 15, "max": 30},
                "cooldown": 12,
                "mana_cost": 25,
                "description": "Tear reality itself with chaotic magic",
                "status_effect": {
                    "type": "reality_distortion",
                    "chance": 1.0,
                    "duration": 5.0,
                },
                "prerequisites": ["occultist_void_magic"],
                "max_level": 10,
            },
            "occultist_apocalypse": {
                "id": "occultist_apocalypse",
                "name": "Apocalypse",
                "type": SkillType.ULTIMATE,
                "archetype": "magic",
                "subtype": "occultist",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 30, "max": 50},
                "cooldown": 35,
                "mana_cost": 60,
                "description": "ULTIMATE: Unleash the apocalypse",
                "status_effect": {
                    "type": "apocalypse",
                    "chance": 1.0,
                    "duration": 10.0,
                },
                "prerequisites": ["occultist_reality_tear"],
                "max_level": 10,
                "is_ultimate": True,
                "requires_pure_build": True,
            },
            # WILD ARCHETYPE - BEASTMASTER SUBTYPE (Nature/Summoning Focus)
            "beastmaster_summon_wolf": {
                "id": "beastmaster_summon_wolf",
                "name": "Summon Wolf",
                "type": SkillType.ACTIVE,
                "archetype": "wild",
                "subtype": "beastmaster",
                "elemental_type": ElementalType.NATURE,
                "base_damage": {"min": 2, "max": 4},
                "cooldown": 3,
                "mana_cost": 8,
                "description": "Summon a loyal wolf companion",
                "status_effect": {"type": "summon", "chance": 1.0, "duration": 10.0},
                "prerequisites": [],
                "max_level": 10,
            },
            "beastmaster_animal_bond": {
                "id": "beastmaster_animal_bond",
                "name": "Animal Bond",
                "type": SkillType.PASSIVE,
                "archetype": "wild",
                "subtype": "beastmaster",
                "elemental_type": ElementalType.NATURE,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Increased effectiveness of summoned creatures",
                "status_effect": None,
                "prerequisites": ["beastmaster_summon_wolf"],
                "max_level": 10,
            },
            "beastmaster_summon_bear": {
                "id": "beastmaster_summon_bear",
                "name": "Summon Bear",
                "type": SkillType.ACTIVE,
                "archetype": "wild",
                "subtype": "beastmaster",
                "elemental_type": ElementalType.NATURE,
                "base_damage": {"min": 4, "max": 8},
                "cooldown": 5,
                "mana_cost": 12,
                "description": "Summon a powerful bear companion",
                "status_effect": {"type": "summon", "chance": 1.0, "duration": 12.0},
                "prerequisites": ["beastmaster_animal_bond"],
                "max_level": 10,
            },
            "beastmaster_pack_tactics": {
                "id": "beastmaster_pack_tactics",
                "name": "Pack Tactics",
                "type": SkillType.PASSIVE,
                "archetype": "wild",
                "subtype": "beastmaster",
                "elemental_type": ElementalType.NATURE,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Summoned creatures work together",
                "status_effect": None,
                "prerequisites": ["beastmaster_summon_bear"],
                "max_level": 10,
            },
            "beastmaster_summon_eagle": {
                "id": "beastmaster_summon_eagle",
                "name": "Summon Eagle",
                "type": SkillType.ACTIVE,
                "archetype": "wild",
                "subtype": "beastmaster",
                "elemental_type": ElementalType.NATURE,
                "base_damage": {"min": 3, "max": 6},
                "cooldown": 4,
                "mana_cost": 10,
                "description": "Summon a swift eagle companion",
                "status_effect": {"type": "summon", "chance": 1.0, "duration": 8.0},
                "prerequisites": ["beastmaster_pack_tactics"],
                "max_level": 10,
            },
            "beastmaster_nature_magic": {
                "id": "beastmaster_nature_magic",
                "name": "Nature Magic",
                "type": SkillType.PASSIVE,
                "archetype": "wild",
                "subtype": "beastmaster",
                "elemental_type": ElementalType.NATURE,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Mastery of nature magic",
                "status_effect": None,
                "prerequisites": ["beastmaster_summon_eagle"],
                "max_level": 10,
            },
            "beastmaster_summon_dragon": {
                "id": "beastmaster_summon_dragon",
                "name": "Summon Dragon",
                "type": SkillType.ACTIVE,
                "archetype": "wild",
                "subtype": "beastmaster",
                "elemental_type": ElementalType.NATURE,
                "base_damage": {"min": 8, "max": 16},
                "cooldown": 15,
                "mana_cost": 30,
                "description": "Summon a mighty dragon companion",
                "status_effect": {"type": "summon", "chance": 1.0, "duration": 15.0},
                "prerequisites": ["beastmaster_nature_magic"],
                "max_level": 10,
            },
            "beastmaster_wild_call": {
                "id": "beastmaster_wild_call",
                "name": "Wild Call",
                "type": SkillType.ULTIMATE,
                "archetype": "wild",
                "subtype": "beastmaster",
                "elemental_type": ElementalType.NATURE,
                "base_damage": {"min": 20, "max": 35},
                "cooldown": 30,
                "mana_cost": 50,
                "description": "ULTIMATE: Call forth all wild creatures",
                "status_effect": {"type": "wild_army", "chance": 1.0, "duration": 20.0},
                "prerequisites": ["beastmaster_summon_dragon"],
                "max_level": 10,
                "is_ultimate": True,
                "requires_pure_build": True,
            },
            # WILD ARCHETYPE - SHADOWHUNTER SUBTYPE (Stealth/Assassination Focus)
            "shadowhunter_shadow_step": {
                "id": "shadowhunter_shadow_step",
                "name": "Shadow Step",
                "type": SkillType.ACTIVE,
                "archetype": "wild",
                "subtype": "shadowhunter",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 2,
                "mana_cost": 5,
                "description": "Teleport through shadows",
                "status_effect": {"type": "stealth", "chance": 1.0, "duration": 3.0},
                "prerequisites": [],
                "max_level": 10,
            },
            "shadowhunter_backstab": {
                "id": "shadowhunter_backstab",
                "name": "Backstab",
                "type": SkillType.ACTIVE,
                "archetype": "wild",
                "subtype": "shadowhunter",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 6, "max": 12},
                "cooldown": 3,
                "mana_cost": 8,
                "description": "Stealth attack from behind",
                "status_effect": {"type": "critical", "chance": 0.8, "duration": 1.0},
                "prerequisites": ["shadowhunter_shadow_step"],
                "max_level": 10,
            },
            "shadowhunter_poison_dagger": {
                "id": "shadowhunter_poison_dagger",
                "name": "Poison Dagger",
                "type": SkillType.ACTIVE,
                "archetype": "wild",
                "subtype": "shadowhunter",
                "elemental_type": ElementalType.NATURE,
                "base_damage": {"min": 3, "max": 6},
                "cooldown": 2,
                "mana_cost": 6,
                "description": "Dagger coated with deadly poison",
                "status_effect": {"type": "poison", "chance": 0.7, "duration": 5.0},
                "prerequisites": ["shadowhunter_backstab"],
                "max_level": 10,
            },
            "shadowhunter_shadow_clone": {
                "id": "shadowhunter_shadow_clone",
                "name": "Shadow Clone",
                "type": SkillType.ACTIVE,
                "archetype": "wild",
                "subtype": "shadowhunter",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 2, "max": 4},
                "cooldown": 5,
                "mana_cost": 12,
                "description": "Create a shadow clone to fight",
                "status_effect": {"type": "clone", "chance": 1.0, "duration": 8.0},
                "prerequisites": ["shadowhunter_poison_dagger"],
                "max_level": 10,
            },
            "shadowhunter_death_mark": {
                "id": "shadowhunter_death_mark",
                "name": "Death Mark",
                "type": SkillType.ACTIVE,
                "archetype": "wild",
                "subtype": "shadowhunter",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 8,
                "mana_cost": 15,
                "description": "Mark target for instant death",
                "status_effect": {
                    "type": "death_mark",
                    "chance": 1.0,
                    "duration": 10.0,
                },
                "prerequisites": ["shadowhunter_shadow_clone"],
                "max_level": 10,
            },
            "shadowhunter_stealth_mastery": {
                "id": "shadowhunter_stealth_mastery",
                "name": "Stealth Mastery",
                "type": SkillType.PASSIVE,
                "archetype": "wild",
                "subtype": "shadowhunter",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Mastery of stealth and assassination",
                "status_effect": None,
                "prerequisites": ["shadowhunter_death_mark"],
                "max_level": 10,
            },
            "shadowhunter_shadow_assassin": {
                "id": "shadowhunter_shadow_assassin",
                "name": "Shadow Assassin",
                "type": SkillType.ACTIVE,
                "archetype": "wild",
                "subtype": "shadowhunter",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 10, "max": 20},
                "cooldown": 10,
                "mana_cost": 20,
                "description": "Become a shadow assassin",
                "status_effect": {
                    "type": "assassin_mode",
                    "chance": 1.0,
                    "duration": 8.0,
                },
                "prerequisites": ["shadowhunter_stealth_mastery"],
                "max_level": 10,
            },
            "shadowhunter_shadow_realm": {
                "id": "shadowhunter_shadow_realm",
                "name": "Shadow Realm",
                "type": SkillType.ULTIMATE,
                "archetype": "wild",
                "subtype": "shadowhunter",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 25, "max": 40},
                "cooldown": 35,
                "mana_cost": 45,
                "description": "ULTIMATE: Enter the shadow realm",
                "status_effect": {
                    "type": "shadow_realm",
                    "chance": 1.0,
                    "duration": 12.0,
                },
                "prerequisites": ["shadowhunter_shadow_assassin"],
                "max_level": 10,
                "is_ultimate": True,
                "requires_pure_build": True,
            },
            # WILD ARCHETYPE - ALCHEMIST SUBTYPE (Chaos/Transmutation Focus)
            "alchemist_potion_throw": {
                "id": "alchemist_potion_throw",
                "name": "Potion Throw",
                "type": SkillType.ACTIVE,
                "archetype": "wild",
                "subtype": "alchemist",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 2, "max": 5},
                "cooldown": 2,
                "mana_cost": 4,
                "description": "Throw a random potion with chaotic effects",
                "status_effect": {
                    "type": "random_potion",
                    "chance": 1.0,
                    "duration": 3.0,
                },
                "prerequisites": [],
                "max_level": 10,
            },
            "alchemist_transmute": {
                "id": "alchemist_transmute",
                "name": "Transmute",
                "type": SkillType.ACTIVE,
                "archetype": "wild",
                "subtype": "alchemist",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 4,
                "mana_cost": 8,
                "description": "Transform enemies into harmless creatures",
                "status_effect": {"type": "transmute", "chance": 0.5, "duration": 5.0},
                "prerequisites": ["alchemist_potion_throw"],
                "max_level": 10,
            },
            "alchemist_chaos_bomb": {
                "id": "alchemist_chaos_bomb",
                "name": "Chaos Bomb",
                "type": SkillType.ACTIVE,
                "archetype": "wild",
                "subtype": "alchemist",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 4, "max": 8},
                "cooldown": 5,
                "mana_cost": 10,
                "description": "Explosive bomb with random effects",
                "status_effect": {
                    "type": "chaos_explosion",
                    "chance": 1.0,
                    "duration": 4.0,
                },
                "prerequisites": ["alchemist_transmute"],
                "max_level": 10,
            },
            "alchemist_elixir_mastery": {
                "id": "alchemist_elixir_mastery",
                "name": "Elixir Mastery",
                "type": SkillType.PASSIVE,
                "archetype": "wild",
                "subtype": "alchemist",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Mastery of alchemical elixirs",
                "status_effect": None,
                "prerequisites": ["alchemist_chaos_bomb"],
                "max_level": 10,
            },
            "alchemist_philosophers_stone": {
                "id": "alchemist_philosophers_stone",
                "name": "Philosopher's Stone",
                "type": SkillType.ACTIVE,
                "archetype": "wild",
                "subtype": "alchemist",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 6, "max": 12},
                "cooldown": 8,
                "mana_cost": 15,
                "description": "Create the legendary philosopher's stone",
                "status_effect": {
                    "type": "transmutation",
                    "chance": 0.8,
                    "duration": 6.0,
                },
                "prerequisites": ["alchemist_elixir_mastery"],
                "max_level": 10,
            },
            "alchemist_chaos_brewing": {
                "id": "alchemist_chaos_brewing",
                "name": "Chaos Brewing",
                "type": SkillType.ACTIVE,
                "archetype": "wild",
                "subtype": "alchemist",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 3, "max": 7},
                "cooldown": 6,
                "mana_cost": 12,
                "description": "Brew chaotic potions with random effects",
                "status_effect": {
                    "type": "chaos_potion",
                    "chance": 1.0,
                    "duration": 5.0,
                },
                "prerequisites": ["alchemist_philosophers_stone"],
                "max_level": 10,
            },
            "alchemist_reality_warper": {
                "id": "alchemist_reality_warper",
                "name": "Reality Warper",
                "type": SkillType.PASSIVE,
                "archetype": "wild",
                "subtype": "alchemist",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Mastery of reality-warping alchemy",
                "status_effect": None,
                "prerequisites": ["alchemist_chaos_brewing"],
                "max_level": 10,
            },
            "alchemist_chaos_apotheosis": {
                "id": "alchemist_chaos_apotheosis",
                "name": "Chaos Apotheosis",
                "type": SkillType.ULTIMATE,
                "archetype": "wild",
                "subtype": "alchemist",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 20, "max": 35},
                "cooldown": 30,
                "mana_cost": 50,
                "description": "ULTIMATE: Achieve chaos apotheosis",
                "status_effect": {
                    "type": "chaos_ascension",
                    "chance": 1.0,
                    "duration": 15.0,
                },
                "prerequisites": ["alchemist_reality_warper"],
                "max_level": 10,
                "is_ultimate": True,
                "requires_pure_build": True,
            },
            # MISSING SKILLS TO COMPLETE ALL SUBTYPES TO 10 SKILLS EACH
            # RANGED ARCHETYPE - TRAPPER SUBTYPE (Missing 1 skill)
            "trapper_ambush": {
                "id": "trapper_ambush",
                "name": "Ambush",
                "type": SkillType.ACTIVE,
                "archetype": "ranged",
                "subtype": "trapper",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 5, "max": 10},
                "cooldown": 6,
                "mana_cost": 12,
                "description": "Set up an ambush for massive damage",
                "status_effect": {"type": "ambush", "chance": 0.8, "duration": 3.0},
                "prerequisites": ["trapper_master_trapper"],
                "max_level": 10,
            },
            # RANGED ARCHETYPE - GUNSLINGER SUBTYPE (Missing 1 skill)
            "gunslinger_showdown": {
                "id": "gunslinger_showdown",
                "name": "Showdown",
                "type": SkillType.ACTIVE,
                "archetype": "ranged",
                "subtype": "gunslinger",
                "elemental_type": ElementalType.PHYSICAL,
                "base_damage": {"min": 8, "max": 15},
                "cooldown": 8,
                "mana_cost": 20,
                "description": "Face-to-face gunfight with high stakes",
                "status_effect": {"type": "showdown", "chance": 0.6, "duration": 4.0},
                "prerequisites": ["gunslinger_ace_up_sleeve"],
                "max_level": 10,
            },
            # MAGIC ARCHETYPE - ELEMENTALIST SUBTYPE (Missing 1 skill)
            "elementalist_storm_caller": {
                "id": "elementalist_storm_caller",
                "name": "Storm Caller",
                "type": SkillType.ACTIVE,
                "archetype": "magic",
                "subtype": "elementalist",
                "elemental_type": ElementalType.LIGHTNING,
                "base_damage": {"min": 6, "max": 12},
                "cooldown": 7,
                "mana_cost": 18,
                "description": "Summon lightning storms to devastate enemies",
                "status_effect": {
                    "type": "lightning_storm",
                    "chance": 0.7,
                    "duration": 5.0,
                },
                "prerequisites": ["elementalist_master_elementalist"],
                "max_level": 10,
            },
            # MAGIC ARCHETYPE - ARCANIST SUBTYPE (Missing 1 skill)
            "arcanist_spell_weaver": {
                "id": "arcanist_spell_weaver",
                "name": "Spell Weaver",
                "type": SkillType.PASSIVE,
                "archetype": "magic",
                "subtype": "arcanist",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Weave multiple spells together for enhanced effects",
                "status_effect": None,
                "prerequisites": ["arcanist_master_arcanist"],
                "max_level": 10,
            },
            # MAGIC ARCHETYPE - OCCULTIST SUBTYPE (Missing 1 skill)
            "occultist_void_walker": {
                "id": "occultist_void_walker",
                "name": "Void Walker",
                "type": SkillType.ACTIVE,
                "archetype": "magic",
                "subtype": "occultist",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 4, "max": 8},
                "cooldown": 5,
                "mana_cost": 15,
                "description": "Walk through the void to avoid damage and teleport",
                "status_effect": {"type": "void_walk", "chance": 1.0, "duration": 2.0},
                "prerequisites": ["occultist_master_occultist"],
                "max_level": 10,
            },
            # WILD ARCHETYPE - BEASTMASTER SUBTYPE (Missing 2 skills)
            "beastmaster_pack_leader": {
                "id": "beastmaster_pack_leader",
                "name": "Pack Leader",
                "type": SkillType.PASSIVE,
                "archetype": "wild",
                "subtype": "beastmaster",
                "elemental_type": ElementalType.NATURE,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Lead your beasts with enhanced coordination",
                "status_effect": None,
                "prerequisites": ["beastmaster_master_beastmaster"],
                "max_level": 10,
            },
            "beastmaster_alpha_strike": {
                "id": "beastmaster_alpha_strike",
                "name": "Alpha Strike",
                "type": SkillType.ACTIVE,
                "archetype": "wild",
                "subtype": "beastmaster",
                "elemental_type": ElementalType.NATURE,
                "base_damage": {"min": 7, "max": 14},
                "cooldown": 6,
                "mana_cost": 20,
                "description": "Coordinate all beasts for a devastating attack",
                "status_effect": {
                    "type": "alpha_strike",
                    "chance": 0.9,
                    "duration": 3.0,
                },
                "prerequisites": ["beastmaster_pack_leader"],
                "max_level": 10,
            },
            # WILD ARCHETYPE - SHADOWHUNTER SUBTYPE (Missing 1 skill)
            "shadowhunter_master_shadowhunter": {
                "id": "shadowhunter_master_shadowhunter",
                "name": "Master Shadowhunter",
                "type": SkillType.PASSIVE,
                "archetype": "wild",
                "subtype": "shadowhunter",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Master the arts of shadow and assassination",
                "status_effect": None,
                "prerequisites": ["shadowhunter_shadow_assassin"],
                "max_level": 10,
            },
            "shadowhunter_shadow_veil": {
                "id": "shadowhunter_shadow_veil",
                "name": "Shadow Veil",
                "type": SkillType.ACTIVE,
                "archetype": "wild",
                "subtype": "shadowhunter",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 6,
                "mana_cost": 15,
                "description": "Create a veil of shadows to hide and protect",
                "status_effect": {
                    "type": "shadow_veil",
                    "chance": 1.0,
                    "duration": 4.0,
                },
                "prerequisites": ["shadowhunter_master_shadowhunter"],
                "max_level": 10,
            },
            # WILD ARCHETYPE - ALCHEMIST SUBTYPE (Missing 2 skills)
            "alchemist_essence_extractor": {
                "id": "alchemist_essence_extractor",
                "name": "Essence Extractor",
                "type": SkillType.ACTIVE,
                "archetype": "wild",
                "subtype": "alchemist",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 2, "max": 4},
                "cooldown": 3,
                "mana_cost": 8,
                "description": "Extract essence from enemies for alchemical use",
                "status_effect": {
                    "type": "essence_extraction",
                    "chance": 0.7,
                    "duration": 2.0,
                },
                "prerequisites": ["alchemist_master_alchemist"],
                "max_level": 10,
            },
            "alchemist_potion_master": {
                "id": "alchemist_potion_master",
                "name": "Potion Master",
                "type": SkillType.PASSIVE,
                "archetype": "wild",
                "subtype": "alchemist",
                "elemental_type": ElementalType.CHAOS,
                "base_damage": {"min": 0, "max": 0},
                "cooldown": 0,
                "mana_cost": 0,
                "description": "Master the art of potion brewing and enhancement",
                "status_effect": None,
                "prerequisites": ["alchemist_essence_extractor"],
                "max_level": 10,
            },
        }

    def _initialize_skill_synergies(self) -> Dict[Tuple[str, str], Dict]:
        """Initialize skill synergy combinations."""
        return {
            ("fireball", "ice_bolt"): {
                "name": "Elemental Combo",
                "description": "Fire and ice create a powerful explosion",
                "bonus_damage": 0.5,
                "additional_effect": "shatter",
            },
            ("bash", "heavy_strike"): {
                "name": "Melee Chain",
                "description": "Chain melee attacks for bonus damage",
                "bonus_damage": 0.3,
                "additional_effect": "chain",
            },
            ("precise_shot", "multi_shot"): {
                "name": "Ranged Barrage",
                "description": "Combine precision with multiple shots",
                "bonus_damage": 0.4,
                "additional_effect": "barrage",
            },
        }

    def get_skill(self, skill_id: str) -> Optional[Dict]:
        """Get skill data by ID."""
        return self.skills_database.get(skill_id)

    def get_skills_by_archetype(self, archetype: str) -> List[Dict]:
        """Get all skills for a specific archetype."""
        return [
            skill
            for skill in self.skills_database.values()
            if skill["archetype"] == archetype
        ]

    def get_player_skills(self, player_id: str) -> Dict:
        """Get all skills for a player."""
        if player_id not in self.player_skills:
            self.player_skills[player_id] = {
                "learned_skills": {},
                "skill_points_spent": 0,
                "total_skills": 0,
            }
        return self.player_skills[player_id]

    def learn_skill(self, player_id: str, skill_id: str) -> bool:
        """
        Learn a skill for a player.

        Args:
            player_id: ID of the player
            skill_id: ID of the skill to learn

        Returns:
            True if successful, False otherwise
        """
        skill_data = self.get_skill(skill_id)
        if not skill_data:
            return False

        player_skills = self.get_player_skills(player_id)

        # Check if already learned
        if skill_id in player_skills["learned_skills"]:
            return False

        # Check prerequisites
        for prereq in skill_data["prerequisites"]:
            if prereq not in player_skills["learned_skills"]:
                return False

        # Learn the skill
        player_skills["learned_skills"][skill_id] = {
            "level": 0,
            "learned_at": time.time(),
            "times_used": 0,
        }

        player_skills["total_skills"] += 1
        return True

    def upgrade_skill(
        self, player_id: str, skill_id: str, skill_points: int = 1
    ) -> Dict:
        """
        Upgrade a skill with skill points, respecting archetype class point limits.

        Args:
            player_id: ID of the player
            skill_id: ID of the skill to upgrade
            skill_points: Number of skill points to spend

        Returns:
            Dictionary with upgrade result
        """
        # Check if upgrade is allowed
        can_upgrade, error_message = self.can_upgrade_skill(
            player_id, skill_id, skill_points
        )
        if not can_upgrade:
            return {"success": False, "error": error_message}

        # Get data
        skill_data = self.get_skill(skill_id)
        player_skills = self.get_player_skills(player_id)
        player_data = self.player_system.get_player(player_id)

        # Perform the upgrade
        skill_info = player_skills["learned_skills"][skill_id]
        old_level = skill_info["level"]
        skill_info["level"] += skill_points
        new_level = skill_info["level"]

        # Deduct skill points from player
        player_data["unused_points"]["skill"] -= skill_points

        # Update skill usage tracking
        skill_info["times_upgraded"] = skill_info.get("times_upgraded", 0) + 1

        return {
            "success": True,
            "skill_name": skill_data["name"],
            "old_level": old_level,
            "new_level": new_level,
            "points_spent": skill_points,
            "remaining_skill_points": player_data["unused_points"]["skill"],
            "max_level_for_archetype": self.get_max_skill_level(player_id, skill_id),
        }

    def get_available_skills_for_player(self, player_id: str) -> Dict:
        """
        Get all skills available to a player based on their archetypes.

        Args:
            player_id: ID of the player

        Returns:
            Dictionary with available skills organized by archetype
        """
        player_data = self.player_system.get_player(player_id)
        if not player_data:
            return {"error": "Player not found"}

        player_archetypes = player_data.get("archetypes", {})
        player_skills = self.get_player_skills(player_id)

        result = {
            "player_id": player_id,
            "skill_points_available": player_data["unused_points"]["skill"],
            "class_points_available": player_data["unused_points"]["class"],
            "archetypes": {},
        }

        # Organize skills by archetype and subtype
        for skill_id, skill_data in self.skills_database.items():
            skill_archetype = skill_data.get("archetype", "melee")
            skill_subtype = skill_data.get("subtype", "juggernaut")

            # Skip skills for archetypes the player doesn't have
            if skill_archetype not in player_archetypes:
                continue

            if skill_archetype not in result["archetypes"]:
                result["archetypes"][skill_archetype] = {"subtypes": {}}

            if skill_subtype not in result["archetypes"][skill_archetype]["subtypes"]:
                # Get points allocated to this subtype
                subtype_points = player_data.get("subtype_points", {}).get(
                    skill_archetype, {}
                )
                points_in_subtype = subtype_points.get(skill_subtype, 0)

                result["archetypes"][skill_archetype]["subtypes"][skill_subtype] = {
                    "skills": [],
                    "points_allocated": points_in_subtype,
                    "max_skill_level": points_in_subtype,
                }

            # Determine skill status
            is_learned = skill_id in player_skills["learned_skills"]
            current_level = 0
            if is_learned:
                current_level = player_skills["learned_skills"][skill_id]["level"]

            max_level = self.get_max_skill_level(player_id, skill_id)
            can_learn = not is_learned and len(skill_data.get("prerequisites", [])) == 0
            can_upgrade = False
            can_access_ultimate = True
            ultimate_error = ""

            if is_learned:
                can_upgrade, _ = self.can_upgrade_skill(player_id, skill_id, 1)

            # Check ultimate access
            if skill_data.get("is_ultimate", False):
                can_access_ultimate, ultimate_error = self.can_access_ultimate(
                    player_id, skill_id
                )

            skill_info = {
                "id": skill_id,
                "name": skill_data["name"],
                "type": skill_data["type"].value,
                "subtype": skill_subtype,
                "description": skill_data["description"],
                "is_learned": is_learned,
                "current_level": current_level,
                "max_level_for_subtype": max_level,
                "can_learn": can_learn,
                "can_upgrade": can_upgrade,
                "is_ultimate": skill_data.get("is_ultimate", False),
                "can_access_ultimate": can_access_ultimate,
                "ultimate_restriction": (
                    ultimate_error if not can_access_ultimate else ""
                ),
                "base_damage": skill_data.get("base_damage", {"min": 0, "max": 0}),
                "cooldown": skill_data.get("cooldown", 0),
                "mana_cost": skill_data.get("mana_cost", 0),
                "prerequisites": skill_data.get("prerequisites", []),
            }

            result["archetypes"][skill_archetype]["subtypes"][skill_subtype][
                "skills"
            ].append(skill_info)

        return result

    def calculate_skill_damage(
        self, skill_id: str, skill_level: int, weapon_damage: int = 0
    ) -> Dict:
        """
        Calculate damage for a skill at a specific level.

        Args:
            skill_id: ID of the skill
            skill_level: Level of the skill
            weapon_damage: Additional weapon damage

        Returns:
            Damage calculation result
        """
        skill_data = self.get_skill(skill_id)
        if not skill_data:
            return {"error": "Skill not found"}

        base_damage = skill_data["base_damage"]

        # Calculate damage range with skill level
        min_damage = base_damage["min"] + skill_level + weapon_damage
        max_damage = base_damage["max"] + skill_level + weapon_damage

        return {
            "skill_id": skill_id,
            "skill_level": skill_level,
            "min_damage": min_damage,
            "max_damage": max_damage,
            "elemental_type": skill_data["elemental_type"].value,
            "status_effect": skill_data.get("status_effect"),
        }

    def can_use_skill(self, player_id: str, skill_id: str) -> bool:
        """
        Check if a player can use a skill (cooldown, mana, etc.).

        Args:
            player_id: ID of the player
            skill_id: ID of the skill

        Returns:
            True if skill can be used, False otherwise
        """
        skill_data = self.get_skill(skill_id)
        if not skill_data:
            return False

        player_skills = self.get_player_skills(player_id)

        # Check if skill is learned
        if skill_id not in player_skills["learned_skills"]:
            return False

        # Check cooldown
        if player_id not in self.skill_cooldowns:
            self.skill_cooldowns[player_id] = {}

        cooldown_data = self.skill_cooldowns[player_id]
        if skill_id in cooldown_data:
            last_used = cooldown_data[skill_id]
            cooldown = skill_data["cooldown"]
            if time.time() - last_used < cooldown:
                return False

        return True

    def use_skill(self, player_id: str, skill_id: str) -> bool:
        """
        Use a skill (mark as used, update cooldown).

        Args:
            player_id: ID of the player
            skill_id: ID of the skill

        Returns:
            True if successful, False otherwise
        """
        if not self.can_use_skill(player_id, skill_id):
            return False

        # Update cooldown
        if player_id not in self.skill_cooldowns:
            self.skill_cooldowns[player_id] = {}

        self.skill_cooldowns[player_id][skill_id] = time.time()

        # Update usage count
        player_skills = self.get_player_skills(player_id)
        if skill_id in player_skills["learned_skills"]:
            player_skills["learned_skills"][skill_id]["times_used"] += 1

        return True

    def get_skill_synergy(self, skill1_id: str, skill2_id: str) -> Optional[Dict]:
        """
        Get synergy information between two skills.

        Args:
            skill1_id: ID of the first skill
            skill2_id: ID of the second skill

        Returns:
            Synergy data if exists, None otherwise
        """
        # Check both combinations
        synergy_key1 = (skill1_id, skill2_id)
        synergy_key2 = (skill2_id, skill1_id)

        if synergy_key1 in self.skill_synergies:
            return self.skill_synergies[synergy_key1]
        elif synergy_key2 in self.skill_synergies:
            return self.skill_synergies[synergy_key2]
        else:
            return None

    def get_player_skill_summary(self, player_id: str) -> Dict:
        """Get a comprehensive summary of a player's skills."""
        player_skills = self.get_player_skills(player_id)

        summary = {
            "total_skills": player_skills["total_skills"],
            "skill_points_spent": player_skills["skill_points_spent"],
            "learned_skills": [],
        }

        for skill_id, skill_info in player_skills["learned_skills"].items():
            skill_data = self.get_skill(skill_id)
            if skill_data:
                summary["learned_skills"].append(
                    {
                        "id": skill_id,
                        "name": skill_data["name"],
                        "level": skill_info["level"],
                        "max_level": skill_data["max_level"],
                        "times_used": skill_info["times_used"],
                        "archetype": skill_data["archetype"],
                        "elemental_type": skill_data["elemental_type"].value,
                    }
                )

        return summary

    def get_available_skills(self, player_id: str, archetype: str) -> List[Dict]:
        """
        Get skills available for learning by a player.

        Args:
            player_id: ID of the player
            archetype: Archetype to get skills for

        Returns:
            List of available skills
        """
        player_skills = self.get_player_skills(player_id)
        learned_skills = set(player_skills["learned_skills"].keys())

        available_skills = []

        for skill_id, skill_data in self.skills_database.items():
            if skill_data["archetype"] == archetype:
                # Check if already learned
                if skill_id in learned_skills:
                    continue

                # Check prerequisites
                prerequisites_met = True
                for prereq in skill_data["prerequisites"]:
                    if prereq not in learned_skills:
                        prerequisites_met = False
                        break

                if prerequisites_met:
                    available_skills.append(
                        {
                            "id": skill_id,
                            "name": skill_data["name"],
                            "description": skill_data["description"],
                            "prerequisites": skill_data["prerequisites"],
                            "max_level": skill_data["max_level"],
                        }
                    )

        return available_skills

    def reset_player_skills(self, player_id: str) -> bool:
        """
        Reset all skills for a player (refund skill points).

        Args:
            player_id: ID of the player

        Returns:
            True if successful, False otherwise
        """
        if player_id not in self.player_skills:
            return False

        # Calculate total skill points to refund
        total_points = 0
        for skill_info in self.player_skills[player_id]["learned_skills"].values():
            total_points += skill_info["level"]

        # Reset skills
        self.player_skills[player_id] = {
            "learned_skills": {},
            "skill_points_spent": 0,
            "total_skills": 0,
        }

        # Clear cooldowns
        if player_id in self.skill_cooldowns:
            del self.skill_cooldowns[player_id]

        return True


# Example usage and testing
if __name__ == "__main__":
    skills_system = SkillsSystem()

    # Test getting skills
    bash_skill = skills_system.get_skill("bash")
    print(f"Bash skill: {bash_skill['name']}")

    # Test learning a skill
    success = skills_system.learn_skill("player1", "bash")
    print(f"Learned bash: {success}")

    # Test upgrading a skill
    success = skills_system.upgrade_skill("player1", "bash", 2)
    print(f"Upgraded bash: {success}")

    # Test skill damage calculation
    damage_info = skills_system.calculate_skill_damage("bash", 2, 3)
    print(f"Bash damage: {damage_info['min']}-{damage_info['max']}")

    # Test skill synergy
    synergy = skills_system.get_skill_synergy("fireball", "ice_bolt")
    if synergy:
        print(f"Synergy found: {synergy['name']}")

    # Test player skill summary
    summary = skills_system.get_player_skill_summary("player1")
    print(f"Player skills: {summary['total_skills']} learned")

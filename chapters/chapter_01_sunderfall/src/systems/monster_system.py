"""
Monster System - Chronicles of Ruin: Sunderfall

This module implements monster generation, scaling, classification, and behavior
including the scaling mechanic where monsters scale with player level but cap at +10.
"""

import random
import math
from typing import Dict, List, Tuple, Optional
from enum import Enum
from .xp_system import XPSystem


class MonsterArchetype(Enum):
    """Monster archetypes with their characteristics."""

    MELEE = "melee"
    RANGED = "ranged"
    MAGIC = "magic"
    WILD = "wild"


class MonsterClassification(Enum):
    """Monster classifications that affect behavior and loot."""

    DEMONIC = "demonic"
    UNDEAD = "undead"
    BEAST = "beast"
    ELEMENTAL = "elemental"
    CONSTRUCT = "construct"
    HUMANOID = "humanoid"


class MonsterSystem:
    """
    Core monster system implementing generation, scaling, classification,
    and behavior mechanics.
    """

    def __init__(self):
        """Initialize the monster system with default configurations."""
        self.max_scaling_bonus = 10  # Maximum +10 levels above base
        self.wild_spawn_chance = 0.05  # 5% chance for Wild monster
        self.unique_spawn_chance = 0.01  # 1% chance for unique monster

        # Initialize XP system for calculating rewards
        self.xp_system = XPSystem()

        # Base stats per level
        self.base_health_per_level = 10
        self.base_damage_per_level = 2
        self.base_defense_per_level = 1

        # Archetype bonuses
        self.archetype_bonuses = {
            MonsterArchetype.MELEE: {"health": 0.20, "damage": 0.30, "defense": 0.25},
            MonsterArchetype.RANGED: {
                "health": 0.10,
                "damage": 0.25,
                "defense": 0.15,
                "accuracy": 0.20,
            },
            MonsterArchetype.MAGIC: {
                "health": 0.15,
                "damage": 0.20,
                "defense": 0.10,
                "status_power": 0.30,
            },
            MonsterArchetype.WILD: {
                "health": 0.25,
                "damage": 0.35,
                "defense": 0.20,
                "chaos_power": 0.50,
            },
        }

        # Classification bonuses
        self.classification_bonuses = {
            MonsterClassification.DEMONIC: {
                "fire_damage": 1.5,
                "burn_resistance": 50,
                "burn_immune": True,
            },
            MonsterClassification.UNDEAD: {
                "cold_damage": 1.3,
                "stun_resistance": 75,
                "stun_immune": True,
            },
            MonsterClassification.BEAST: {
                "physical_damage": 1.4,
                "bleed_resistance": 60,
                "bleed_immune": True,
            },
            MonsterClassification.ELEMENTAL: {
                "elemental_damage": 1.6,
                "status_resistance": 80,
                "status_immune": True,
            },
            MonsterClassification.CONSTRUCT: {
                "defense": 1.5,
                "poison_resistance": 70,
                "poison_immune": True,
            },
            MonsterClassification.HUMANOID: {
                "balanced": True,
                "no_special_immunities": True,
            },
        }

    def calculate_monster_level(self, base_level: int, player_level: int) -> int:
        """
        Calculate monster level based on player level with scaling cap.
        """
        # Early-game smoothing: if player is <= 8, dampen scaling
        if player_level <= 8:
            effective_player = base_level + max(0, (player_level - base_level) * 0.6)
        else:
            effective_player = player_level

        scaling_bonus = min(int(effective_player - base_level), self.max_scaling_bonus)

        # Apply smaller random variation at low levels
        if player_level <= 8:
            random_variation = random.randint(-1, 1)
        else:
            random_variation = random.randint(-2, 2)

        final_level = base_level + scaling_bonus + random_variation
        final_level = max(final_level, 1)
        final_level = min(final_level, base_level + self.max_scaling_bonus)
        return final_level

    def calculate_monster_level_from_player_data(
        self, base_level: int, player_data: Dict
    ) -> int:
        """
        Calculate monster level using full player data structure.

        Args:
            base_level: Base level of the monster
            player_data: Player data with levels dict

        Returns:
            Final monster level based on player's Class + Skill levels
        """
        # Extract player level (Class + Skill) from new data structure
        if "player_level" in player_data:
            player_level = player_data["player_level"]
        elif "levels" in player_data:
            # Calculate from levels dict
            player_level = player_data["levels"].get("class", 1) + player_data[
                "levels"
            ].get("skill", 1)
        else:
            # Fallback to legacy level
            player_level = player_data.get("level", 1)

        return self.calculate_monster_level(base_level, player_level)

    def generate_monster_stats(
        self,
        monster_level: int,
        archetype: MonsterArchetype,
        classification: MonsterClassification,
        is_wild: bool = False,
    ) -> Dict:
        """Generate complete monster stats based on level, archetype, and classification."""
        # Base stats
        base_health = 40 + (monster_level * self.base_health_per_level)
        base_damage = 8 + (monster_level * self.base_damage_per_level)
        base_defense = 4 + (monster_level * self.base_defense_per_level)

        # Early-game nerf (levels <= 8)
        if monster_level <= 8:
            base_health *= 0.60
            base_damage *= 0.45
            base_defense *= 0.65

        # Apply archetype bonuses
        archetype_bonus = self.archetype_bonuses[archetype]
        health = base_health * (1 + archetype_bonus.get("health", 0))
        damage = base_damage * (1 + archetype_bonus.get("damage", 0))
        defense = base_defense * (1 + archetype_bonus.get("defense", 0))

        # Apply classification bonuses
        classification_bonus = self.classification_bonuses[classification]

        # Apply Wild monster bonuses
        if is_wild:
            health *= 1.5  # +50% health
            damage *= 1.5  # +50% damage
            defense *= 1.5  # +50% defense
            monster_level += 3  # +3 levels

        # Build stats dictionary
        stats = {
            "level": monster_level,
            "health": int(health),
            "max_health": int(health),
            "damage": int(damage),
            "defense": int(defense),
            "archetype": archetype.value,
            "classification": classification.value,
            "is_wild": is_wild,
            "is_unique": False,
            "status_immune": False,
            "accuracy": 0.8 + archetype_bonus.get("accuracy", 0),
            "critical_chance": 0.05,
            "critical_multiplier": 1.5,
        }

        # Apply classification-specific bonuses
        if classification == MonsterClassification.DEMONIC:
            stats["fire_damage"] = damage * classification_bonus["fire_damage"]
            stats["burn_resistance"] = classification_bonus["burn_resistance"] + (
                monster_level * 2
            )
            stats["burn_immune"] = classification_bonus["burn_immune"]
        elif classification == MonsterClassification.UNDEAD:
            stats["cold_damage"] = damage * classification_bonus["cold_damage"]
            stats["stun_resistance"] = classification_bonus["stun_resistance"] + (
                monster_level * 3
            )
            stats["stun_immune"] = classification_bonus["stun_immune"]
        elif classification == MonsterClassification.BEAST:
            stats["physical_damage"] = damage * classification_bonus["physical_damage"]
            stats["bleed_resistance"] = classification_bonus["bleed_resistance"] + (
                monster_level * 2
            )
            stats["bleed_immune"] = classification_bonus["bleed_immune"]
        elif classification == MonsterClassification.ELEMENTAL:
            stats["elemental_damage"] = (
                damage * classification_bonus["elemental_damage"]
            )
            stats["status_resistance"] = classification_bonus["status_resistance"] + (
                monster_level * 3
            )
            stats["status_immune"] = classification_bonus["status_immune"]
        elif classification == MonsterClassification.CONSTRUCT:
            stats["defense"] *= classification_bonus["defense"]
            stats["poison_resistance"] = classification_bonus["poison_resistance"] + (
                monster_level * 2
            )
            stats["poison_immune"] = classification_bonus["poison_immune"]

        return stats

    def determine_monster_type(
        self, district_level: int, player_level: int
    ) -> Tuple[MonsterArchetype, MonsterClassification]:
        """
        Determine monster archetype and classification based on district and player level.

        Args:
            district_level: Level of the current district
            player_level: Current player level

        Returns:
            Tuple of (archetype, classification)
        """
        # Archetype distribution based on district level
        if district_level <= 5:
            # Early districts: More melee and ranged
            archetype_weights = {
                MonsterArchetype.MELEE: 0.4,
                MonsterArchetype.RANGED: 0.3,
                MonsterArchetype.MAGIC: 0.2,
                MonsterArchetype.WILD: 0.1,
            }
        elif district_level <= 15:
            # Mid districts: Balanced distribution
            archetype_weights = {
                MonsterArchetype.MELEE: 0.3,
                MonsterArchetype.RANGED: 0.3,
                MonsterArchetype.MAGIC: 0.25,
                MonsterArchetype.WILD: 0.15,
            }
        else:
            # Late districts: More magic and wild
            archetype_weights = {
                MonsterArchetype.MELEE: 0.25,
                MonsterArchetype.RANGED: 0.25,
                MonsterArchetype.MAGIC: 0.3,
                MonsterArchetype.WILD: 0.2,
            }

        # Classification distribution
        classification_weights = {
            MonsterClassification.HUMANOID: 0.3,
            MonsterClassification.BEAST: 0.25,
            MonsterClassification.UNDEAD: 0.2,
            MonsterClassification.DEMONIC: 0.15,
            MonsterClassification.ELEMENTAL: 0.07,
            MonsterClassification.CONSTRUCT: 0.03,
        }

        # Select archetype
        archetype = random.choices(
            list(archetype_weights.keys()), weights=list(archetype_weights.values())
        )[0]

        # Select classification
        classification = random.choices(
            list(classification_weights.keys()),
            weights=list(classification_weights.values()),
        )[0]

        return archetype, classification

    def spawn_monster(
        self, district_level: int, player_level: int, base_monster_level: int
    ) -> Dict:
        """
        Spawn a monster with appropriate scaling and characteristics.

        Args:
            district_level: Level of the current district
            player_level: Current player level
            base_monster_level: Base level of the monster

        Returns:
            Dictionary containing complete monster data
        """
        # Calculate final monster level with scaling
        final_level = self.calculate_monster_level(base_monster_level, player_level)

        # Determine monster type
        archetype, classification = self.determine_monster_type(
            district_level, player_level
        )

        # Check for Wild monster
        is_wild = random.random() < self.wild_spawn_chance

        # Check for unique monster (rare)
        is_unique = random.random() < self.unique_spawn_chance

        # Generate monster stats
        stats = self.generate_monster_stats(
            final_level, archetype, classification, is_wild
        )

        # Set unique flag
        stats["is_unique"] = is_unique

        # Generate monster name
        monster_name = self.generate_monster_name(
            archetype, classification, is_wild, is_unique
        )

        # Build complete monster data
        monster_data = {
            "name": monster_name,
            "level": stats["level"],
            "archetype": stats["archetype"],
            "classification": stats["classification"],
            "is_wild": stats["is_wild"],
            "is_unique": stats["is_unique"],
            "stats": stats,
            "loot_table": self.generate_loot_table(stats),
            "experience_reward": self.calculate_experience_reward(stats),
        }

        return monster_data

    def generate_monster_name(
        self,
        archetype: MonsterArchetype,
        classification: MonsterClassification,
        is_wild: bool,
        is_unique: bool,
    ) -> str:
        """Generate a monster name based on its characteristics."""
        base_names = {
            MonsterArchetype.MELEE: ["Warrior", "Berserker", "Guardian", "Champion"],
            MonsterArchetype.RANGED: ["Archer", "Sniper", "Ranger", "Hunter"],
            MonsterArchetype.MAGIC: ["Mage", "Sorcerer", "Warlock", "Enchanter"],
            MonsterArchetype.WILD: ["Beast", "Savage", "Feral", "Primal"],
        }

        classification_prefixes = {
            MonsterClassification.DEMONIC: ["Infernal", "Hellish", "Demonic", "Fiery"],
            MonsterClassification.UNDEAD: [
                "Undead",
                "Skeletal",
                "Necrotic",
                "Corrupted",
            ],
            MonsterClassification.BEAST: ["Feral", "Wild", "Savage", "Untamed"],
            MonsterClassification.ELEMENTAL: [
                "Elemental",
                "Primal",
                "Ancient",
                "Ethereal",
            ],
            MonsterClassification.CONSTRUCT: [
                "Mechanical",
                "Constructed",
                "Artificial",
                "Forged",
            ],
            MonsterClassification.HUMANOID: ["", "Veteran", "Elite", "Master"],
        }

        # Select base name
        base_name = random.choice(base_names[archetype])

        # Select prefix
        prefix = random.choice(classification_prefixes[classification])

        # Build name
        if is_unique:
            name = f"Unique {prefix} {base_name}" if prefix else f"Unique {base_name}"
        elif is_wild:
            name = f"Wild {prefix} {base_name}" if prefix else f"Wild {base_name}"
        else:
            name = f"{prefix} {base_name}" if prefix else base_name

        return name

    def generate_loot_table(self, monster_stats: Dict) -> Dict:
        """Generate loot table for the monster."""
        # Calculate base gold based on monster level
        base_gold = monster_stats["level"] * 2 + random.randint(
            1, monster_stats["level"]
        )

        # Unique monsters have guaranteed unique drops
        if monster_stats["is_unique"]:
            loot_table = {
                "gold": base_gold * 5,  # 5x gold for unique
                "guaranteed_unique_item": True,
                "item_level": monster_stats["level"],
                "drop_chance_multiplier": 3.0,
            }
        else:
            loot_table = {
                "gold": base_gold,
                "guaranteed_unique_item": False,
                "item_level": monster_stats["level"],
                "drop_chance_multiplier": 1.0,
            }

        return loot_table

    def generate_encounter_monster(
        self,
        base_level: int,
        player_data: Dict,
        forced_archetype: MonsterArchetype = None,
        forced_classification: MonsterClassification = None,
    ) -> Dict:
        """Generate a complete monster for an encounter, scaled to player level."""
        monster_level = self.calculate_monster_level_from_player_data(
            base_level, player_data
        )

        player_level = player_data.get("player_level", 1)

        # Determine archetype (random if not forced), avoid Wild early
        if forced_archetype:
            archetype = forced_archetype
        else:
            if player_level <= 8:
                archetypes = [
                    MonsterArchetype.MELEE,
                    MonsterArchetype.RANGED,
                    MonsterArchetype.MAGIC,
                ]
                archetype = random.choice(archetypes)
            else:
                if random.random() < self.wild_spawn_chance:
                    archetype = MonsterArchetype.WILD
                else:
                    archetypes = [
                        MonsterArchetype.MELEE,
                        MonsterArchetype.RANGED,
                        MonsterArchetype.MAGIC,
                    ]
                    archetype = random.choice(archetypes)

        # Determine classification (random if not forced) favor HUMANOID early
        if forced_classification:
            classification = forced_classification
        else:
            if player_level <= 8:
                classification = MonsterClassification.HUMANOID
            else:
                classification = random.choice(list(MonsterClassification))

        # Unique and Wild gating at low level
        if player_level <= 8:
            is_unique = False
            is_wild = False
        else:
            is_unique = random.random() < self.unique_spawn_chance
            is_wild = archetype == MonsterArchetype.WILD

        monster_stats = self.generate_monster_stats(
            monster_level, archetype, classification, is_wild
        )

        if is_unique:
            monster_stats["is_unique"] = True
            monster_stats["level"] += 5
            monster_stats["health"] = int(monster_stats["health"] * 2.5)
            monster_stats["max_health"] = monster_stats["health"]
            monster_stats["damage"] = int(monster_stats["damage"] * 2.0)
            monster_stats["defense"] = int(monster_stats["defense"] * 1.5)

        monster_stats["name"] = self.generate_monster_name(
            archetype, classification, is_wild, is_unique
        )
        monster_stats["loot"] = self.generate_loot_table(monster_stats)

        return monster_stats

    def calculate_experience_reward(
        self, monster_stats: Dict, player_archetype: str = "melee"
    ) -> Dict[str, int]:
        """
        Calculate specialized XP reward for defeating the monster.

        Args:
            monster_stats: Monster statistics including level, type, etc.
            player_archetype: Player's primary archetype for archetype bonuses

        Returns:
            Dictionary with base/class/skill XP rewards
        """
        # Use the XP system's monster reward calculation
        return self.xp_system.calculate_monster_xp_reward(
            monster_stats, player_archetype
        )

    def calculate_experience_reward_legacy(self, monster_stats: Dict) -> int:
        """Legacy single-value experience calculation for backward compatibility."""
        base_exp = monster_stats["level"] * 10

        # Apply bonuses
        if monster_stats["is_wild"]:
            base_exp *= 2  # Double XP for Wild monsters

        if monster_stats["is_unique"]:
            base_exp *= 5  # 5x XP for unique monsters

        return int(base_exp)


# Example usage and testing
def test_monster_system():
    """Test the monster system with various scenarios."""
    monster_system = MonsterSystem()

    # Test monster level scaling
    print("🎯 MONSTER LEVEL SCALING TEST:")
    print("=" * 50)

    test_cases = [
        (1, 5, "Early game - Level 1 monster, Player Level 5"),
        (1, 15, "Mid game - Level 1 monster, Player Level 15"),
        (1, 25, "Late game - Level 1 monster, Player Level 25"),
        (10, 20, "Mid game - Level 10 monster, Player Level 20"),
        (20, 40, "Late game - Level 20 monster, Player Level 40"),
    ]

    for base_level, player_level, description in test_cases:
        final_level = monster_system.calculate_monster_level(base_level, player_level)
        max_possible = base_level + 10
        print(f"{description}:")
        print(f"  Base Level: {base_level}, Player Level: {player_level}")
        print(f"  Final Level: {final_level} (Max: {max_possible})")
        print()

    # Test monster generation
    print("👹 MONSTER GENERATION TEST:")
    print("=" * 50)

    test_scenarios = [
        (5, 10, 3, "Early Game Monster"),
        (15, 25, 8, "Mid Game Monster"),
        (30, 50, 15, "Late Game Monster"),
    ]

    for district_level, player_level, base_monster_level, description in test_scenarios:
        monster = monster_system.spawn_monster(
            district_level, player_level, base_monster_level
        )

        print(f"{description}:")
        print(f"  Name: {monster['name']}")
        print(f"  Level: {monster['level']} (Base: {base_monster_level})")
        print(f"  Archetype: {monster['archetype']}")
        print(f"  Classification: {monster['classification']}")
        print(f"  Health: {monster['stats']['health']}")
        print(f"  Damage: {monster['stats']['damage']}")
        print(f"  Wild: {monster['is_wild']}")
        print(f"  Unique: {monster['is_unique']}")
        print(f"  Experience: {monster['experience_reward']}")
        print(f"  Gold: {monster['loot_table']['gold']}")
        print()


if __name__ == "__main__":
    test_monster_system()

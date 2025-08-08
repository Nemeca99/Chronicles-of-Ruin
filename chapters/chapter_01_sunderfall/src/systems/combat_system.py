"""
Combat System - Chronicles of Ruin: Sunderfall

This module implements the core combat mechanics including damage calculation,
combat triangle system, Wild monster mechanics, status effect integration,
and AI learning integration.
"""

import random
import math
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum
from .player_system import PlayerSystem, StatType
from .monster_system import MonsterSystem, MonsterArchetype
from .xp_system import XPSystem
from .resistance_system import ResistanceSystem, EntityType, ResistanceType


class Archetype(Enum):
    """Combat archetypes with their relationships in the combat triangle."""

    MELEE = "melee"
    RANGED = "ranged"
    MAGIC = "magic"
    WILD = "wild"


class StatusEffect(Enum):
    """Status effects that can be applied during combat."""

    BURN = "burn"
    FREEZE = "freeze"
    STUN = "stun"
    POISON = "poison"
    BLEED = "bleed"
    CHAOS = "chaos"
    SLOW = "slow"
    WEAKEN = "weaken"
    VULNERABLE = "vulnerable"


class CombatSystem:
    """
    Core combat system implementing damage calculation, combat triangle,
    Wild monster mechanics, status effect integration, and AI learning.
    """

    def __init__(
        self,
        player_system: PlayerSystem = None,
        monster_system: MonsterSystem = None,
        items_system=None,
        resistance_system: ResistanceSystem = None,
    ):
        """Initialize the combat system with default configurations."""
        self.combat_triangle_bonus = 0.20  # 20% damage bonus/penalty (tuned)
        self.wild_same_archetype_bonus = 0.35  # 35% damage to same archetype (tuned)
        self.damage_floor = 1.0  # Minimum damage
        self.max_damage_reduction = 0.90  # Maximum 90% damage reduction

        # Integrate with other systems
        self.player_system = player_system or PlayerSystem()
        self.monster_system = monster_system or MonsterSystem()
        self.items_system = items_system
        self.xp_system = XPSystem()
        self.resistance_system = resistance_system or ResistanceSystem()

        # AI learning integration
        self.combat_patterns = {}
        self.boss_encounters = {}
        self.skill_effectiveness = {}

    def calculate_damage(
        self,
        attacker_stats: Dict,
        target_stats: Dict,
        skill_data: Dict,
        weapon_data: Dict,
        resistance_profile: Dict = None,
    ) -> Tuple[float, List[StatusEffect], Dict[str, Any]]:
        """
        Calculate final damage using the complete calculation system with resistance.

        Args:
            attacker_stats: Dictionary containing attacker's current attributes
            target_stats: Dictionary containing target's current attributes
            skill_data: Dictionary containing skill information and modifiers
            weapon_data: Dictionary containing weapon statistics and bonuses
            resistance_profile: Resistance profile for the target

        Returns:
            Tuple of (final_damage, applied_status_effects, combat_analysis)
        """
        # Step 1: Calculate base stats
        base_damage = self._calculate_base_damage(
            attacker_stats, skill_data, weapon_data
        )

        # Step 2: Apply item percentages
        modified_damage = self._apply_item_percentages(base_damage, weapon_data)

        # Step 3: Apply combat triangle
        triangle_damage = self._apply_combat_triangle(
            modified_damage, attacker_stats, target_stats
        )

        # Step 4: Apply resistance system
        resistance_damage = self._apply_resistance_system(
            triangle_damage, target_stats, resistance_profile, skill_data
        )

        # Step 5: Apply damage floor
        final_damage = max(resistance_damage, self.damage_floor)

        # Step 6: Apply status effects with resistance consideration
        applied_effects = self._apply_status_effects_with_resistance(
            attacker_stats, target_stats, skill_data, resistance_profile
        )

        # Step 7: Generate combat analysis for AI learning
        combat_analysis = self._generate_combat_analysis(
            attacker_stats, target_stats, skill_data, weapon_data,
            base_damage, final_damage, applied_effects, resistance_profile
        )

        return final_damage, applied_effects, combat_analysis

    def _calculate_base_damage(
        self, attacker_stats: Dict, skill_data: Dict, weapon_data: Dict
    ) -> float:
        """Calculate base damage from stats, skills, and weapon."""
        # Scaled for early/mid/late progression
        power_damage = (
            attacker_stats.get("power", 0) * 0.4
        )  # Slightly higher contribution (tuned)
        weapon_damage = weapon_data.get("damage", 0)
        skill_damage = skill_data.get("base_damage", 0)

        return power_damage + weapon_damage + skill_damage

    def _apply_item_percentages(self, base_damage: float, weapon_data: Dict) -> float:
        """Apply percentage bonuses from equipment."""
        # Get equipment bonuses from ItemsSystem if available
        if self.items_system and "player_id" in weapon_data:
            equipment_bonuses = self.items_system.get_equipment_bonuses(
                weapon_data["player_id"]
            )

            # Apply equipment bonuses
            for bonus_type, bonus_value in equipment_bonuses.items():
                if bonus_type in [
                    "physical_damage",
                    "fire_damage",
                    "ice_damage",
                    "lightning_damage",
                ]:
                    base_damage *= 1 + bonus_value

        # Apply weapon-specific bonuses
        percentage_bonuses = weapon_data.get("percentage_bonuses", [])
        total_percentage = sum(percentage_bonuses)

        return base_damage * (1 + total_percentage)

    def _apply_combat_triangle(
        self, damage: float, attacker_stats: Dict, target_stats: Dict
    ) -> float:
        """Apply combat triangle multipliers."""
        attacker_archetype = Archetype(attacker_stats.get("archetype", "melee"))
        target_archetype = Archetype(target_stats.get("archetype", "melee"))

        # Get combat triangle multiplier
        triangle_multiplier = self._get_combat_triangle_multiplier(
            attacker_archetype, target_archetype
        )

        # Apply Wild monster bonus if applicable
        if (
            self._is_wild_monster(target_stats)
            and attacker_archetype == target_archetype
        ):
            triangle_multiplier += self.wild_same_archetype_bonus

        return damage * triangle_multiplier

    def _get_combat_triangle_multiplier(
        self, attacker: Archetype, target: Archetype
    ) -> float:
        """Get combat triangle multiplier based on archetype relationships."""
        if attacker == target:
            return 1.0  # No bonus/penalty for same archetype

        # Combat triangle: Melee > Ranged > Magic > Melee
        triangle_relationships = {
            (Archetype.MELEE, Archetype.RANGED): 1
            + self.combat_triangle_bonus,  # Melee > Ranged
            (Archetype.RANGED, Archetype.MAGIC): 1
            + self.combat_triangle_bonus,  # Ranged > Magic
            (Archetype.MAGIC, Archetype.MELEE): 1
            + self.combat_triangle_bonus,  # Magic > Melee
            (Archetype.RANGED, Archetype.MELEE): 1
            - self.combat_triangle_bonus,  # Ranged < Melee
            (Archetype.MAGIC, Archetype.RANGED): 1
            - self.combat_triangle_bonus,  # Magic < Ranged
            (Archetype.MELEE, Archetype.MAGIC): 1
            - self.combat_triangle_bonus,  # Melee < Magic
        }

        return triangle_relationships.get((attacker, target), 1.0)

    def _is_wild_monster(self, target_stats: Dict) -> bool:
        """Check if target is a Wild monster."""
        return target_stats.get("is_wild", False)

    def _apply_resistance_system(
        self, 
        damage: float, 
        target_stats: Dict, 
        resistance_profile: Dict = None,
        skill_data: Dict = None
    ) -> float:
        """Apply resistance system to damage calculation"""
        if not resistance_profile:
            return damage

        # Get damage type from skill
        damage_type = skill_data.get("damage_type", "physical")
        
        # Calculate resistance
        resistance_value = self.resistance_system.calculate_damage_with_resistance(
            damage, damage_type, resistance_profile
        )

        return resistance_value

    def _apply_status_effects_with_resistance(
        self, 
        attacker_stats: Dict, 
        target_stats: Dict, 
        skill_data: Dict,
        resistance_profile: Dict = None
    ) -> List[StatusEffect]:
        """Apply status effects considering resistance and immunities"""
        applied_effects = []
        
        # Check if target is a boss
        is_boss = target_stats.get("entity_type") == EntityType.BOSS
        
        # Get status effects from skill
        skill_effects = skill_data.get("status_effects", [])
        
        for effect in skill_effects:
            effect_enum = StatusEffect(effect)
            
            # Check if boss is immune to this effect
            if is_boss:
                if effect_enum in [StatusEffect.STUN, StatusEffect.FREEZE]:
                    continue  # Bosses are immune to stun and freeze
                elif effect_enum == StatusEffect.SLOW:
                    # Bosses can be slowed but with reduced chance
                    if random.random() < 0.3:  # 30% chance for bosses
                        applied_effects.append(effect_enum)
                    continue
            
            # Check resistance system for status effect application
            if resistance_profile and self.resistance_system.can_apply_status_effect(
                effect_enum.value, resistance_profile
            ):
                # Calculate application chance based on resistance
                chance = self.resistance_system.calculate_status_effect_chance(
                    effect_enum.value, resistance_profile
                )
                
                if random.random() < chance:
                    applied_effects.append(effect_enum)
            else:
                # Default application chance
                if random.random() < 0.7:  # 70% default chance
                    applied_effects.append(effect_enum)
        
        return applied_effects

    def _generate_combat_analysis(
        self, 
        attacker_stats: Dict, 
        target_stats: Dict, 
        skill_data: Dict, 
        weapon_data: Dict,
        base_damage: float, 
        final_damage: float, 
        applied_effects: List[StatusEffect],
        resistance_profile: Dict = None
    ) -> Dict[str, Any]:
        """Generate detailed combat analysis for AI learning"""
        
        # Calculate effectiveness metrics
        damage_effectiveness = final_damage / max(base_damage, 1)
        damage_reduction = (base_damage - final_damage) / max(base_damage, 1)
        
        # Analyze skill effectiveness
        skill_name = skill_data.get("name", "unknown")
        skill_type = skill_data.get("skill_type", "unknown")
        
        # Store for AI learning
        if skill_name not in self.skill_effectiveness:
            self.skill_effectiveness[skill_name] = {
                "usage_count": 0,
                "total_damage": 0,
                "effectiveness_ratios": [],
                "status_effect_success": 0,
                "status_effect_attempts": 0
            }
        
        skill_stats = self.skill_effectiveness[skill_name]
        skill_stats["usage_count"] += 1
        skill_stats["total_damage"] += final_damage
        skill_stats["effectiveness_ratios"].append(damage_effectiveness)
        
        # Track status effect success
        skill_stats["status_effect_attempts"] += len(skill_data.get("status_effects", []))
        skill_stats["status_effect_success"] += len(applied_effects)
        
        # Generate analysis
        analysis = {
            "skill_used": skill_name,
            "skill_type": skill_type,
            "base_damage": base_damage,
            "final_damage": final_damage,
            "damage_effectiveness": damage_effectiveness,
            "damage_reduction": damage_reduction,
            "status_effects_applied": [effect.value for effect in applied_effects],
            "status_effect_success_rate": len(applied_effects) / max(len(skill_data.get("status_effects", [])), 1),
            "target_type": target_stats.get("entity_type", "unknown"),
            "is_boss_encounter": target_stats.get("entity_type") == EntityType.BOSS,
            "resistance_applied": resistance_profile is not None,
            "combat_triangle_bonus": self._get_combat_triangle_multiplier(
                Archetype(attacker_stats.get("archetype", "melee")),
                Archetype(target_stats.get("archetype", "melee"))
            ),
            "skill_effectiveness_trend": self._calculate_skill_effectiveness_trend(skill_name)
        }
        
        return analysis

    def _calculate_skill_effectiveness_trend(self, skill_name: str) -> Dict[str, Any]:
        """Calculate effectiveness trend for a skill"""
        if skill_name not in self.skill_effectiveness:
            return {"trend": "unknown", "average_effectiveness": 0.0}
        
        skill_stats = self.skill_effectiveness[skill_name]
        if not skill_stats["effectiveness_ratios"]:
            return {"trend": "unknown", "average_effectiveness": 0.0}
        
        recent_ratios = skill_stats["effectiveness_ratios"][-5:]  # Last 5 uses
        average_effectiveness = sum(recent_ratios) / len(recent_ratios)
        
        if len(recent_ratios) >= 2:
            trend = "improving" if recent_ratios[-1] > recent_ratios[0] else "declining"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "average_effectiveness": average_effectiveness,
            "usage_count": skill_stats["usage_count"]
        }

    def record_boss_encounter(self, boss_name: str, encounter_data: Dict[str, Any]):
        """Record boss encounter data for AI learning"""
        if boss_name not in self.boss_encounters:
            self.boss_encounters[boss_name] = {
                "encounters": 0,
                "successful_strategies": [],
                "failed_strategies": [],
                "effective_skills": [],
                "ineffective_skills": [],
                "average_damage_taken": 0,
                "average_damage_dealt": 0
            }
        
        boss_stats = self.boss_encounters[boss_name]
        boss_stats["encounters"] += 1
        
        # Record strategy effectiveness
        strategy = encounter_data.get("strategy", "unknown")
        success = encounter_data.get("success", False)
        
        if success:
            boss_stats["successful_strategies"].append(strategy)
        else:
            boss_stats["failed_strategies"].append(strategy)
        
        # Record skill effectiveness
        skills_used = encounter_data.get("skills_used", [])
        for skill in skills_used:
            if skill.get("effective", False):
                boss_stats["effective_skills"].append(skill["name"])
            else:
                boss_stats["ineffective_skills"].append(skill["name"])
        
        # Update damage averages
        damage_taken = encounter_data.get("damage_taken", 0)
        damage_dealt = encounter_data.get("damage_dealt", 0)
        
        boss_stats["average_damage_taken"] = (
            (boss_stats["average_damage_taken"] * (boss_stats["encounters"] - 1) + damage_taken) 
            / boss_stats["encounters"]
        )
        boss_stats["average_damage_dealt"] = (
            (boss_stats["average_damage_dealt"] * (boss_stats["encounters"] - 1) + damage_dealt) 
            / boss_stats["encounters"]
        )

    def get_combat_learning_data(self) -> Dict[str, Any]:
        """Get combat learning data for AI system"""
        return {
            "skill_effectiveness": self.skill_effectiveness,
            "boss_encounters": self.boss_encounters,
            "combat_patterns": self.combat_patterns,
            "learning_insights": self._generate_combat_insights()
        }

    def _generate_combat_insights(self) -> List[str]:
        """Generate insights from combat data"""
        insights = []
        
        # Analyze skill effectiveness
        for skill_name, stats in self.skill_effectiveness.items():
            if stats["usage_count"] >= 3:  # Only analyze skills used multiple times
                avg_effectiveness = sum(stats["effectiveness_ratios"]) / len(stats["effectiveness_ratios"])
                if avg_effectiveness > 1.2:
                    insights.append(f"{skill_name} is highly effective (avg: {avg_effectiveness:.2f})")
                elif avg_effectiveness < 0.8:
                    insights.append(f"{skill_name} is underperforming (avg: {avg_effectiveness:.2f})")
        
        # Analyze boss encounters
        for boss_name, stats in self.boss_encounters.items():
            if stats["encounters"] >= 2:
                success_rate = len(stats["successful_strategies"]) / stats["encounters"]
                if success_rate > 0.7:
                    insights.append(f"Effective strategies found for {boss_name}")
                elif success_rate < 0.3:
                    insights.append(f"Struggling with {boss_name} - need new strategies")
        
        return insights

    def calculate_defense(self, target_stats: Dict, damage_type: str) -> float:
        """
        Calculate damage reduction based on target's defense stats.

        Args:
            target_stats: Dictionary containing target's defense attributes
            damage_type: Type of damage ('physical', 'magical', 'status')

        Returns:
            Damage reduction multiplier (0.0 to max_damage_reduction)
        """
        if damage_type == "physical":
            defense = target_stats.get("toughness", 0)
        elif damage_type == "magical":
            defense = target_stats.get("wisdom", 0)
        elif damage_type == "status":
            defense = target_stats.get("status_resistance", 0)
        else:
            defense = 0

        # Calculate damage reduction (capped at max_damage_reduction)
        damage_reduction = min(defense / 100, self.max_damage_reduction)

        return 1 - damage_reduction

    def apply_status_effect_damage(
        self,
        status_effect: StatusEffect,
        base_damage: float,
        duration: float,
        target_resistance: float,
    ) -> float:
        """
        Calculate status effect damage over time.

        Args:
            status_effect: Type of status effect
            base_damage: Base damage that caused the status effect
            duration: Duration of the status effect
            target_resistance: Target's resistance to the status effect

        Returns:
            Total damage from status effect
        """
        status_damage_multipliers = {
            StatusEffect.BURN: 0.2,  # 20% of base damage over duration
            StatusEffect.POISON: 0.15,  # 15% of base damage over duration
            StatusEffect.BLEED: 0.1,  # 10% of base damage over duration
            StatusEffect.CHAOS: 0.15,  # 15% of base damage over duration
        }

        multiplier = status_damage_multipliers.get(status_effect, 0.0)
        base_status_damage = base_damage * multiplier

        # Apply resistance
        final_status_damage = max(base_status_damage - target_resistance, 0.5)

        return final_status_damage * duration

    def is_critical_hit(self, attacker_stats: Dict, weapon_data: Dict) -> bool:
        """Determine if an attack is a critical hit."""
        base_crit_chance = attacker_stats.get("critical_chance", 0.05)  # 5% base
        weapon_crit_bonus = weapon_data.get("critical_chance", 0.0)
        total_crit_chance = base_crit_chance + weapon_crit_bonus

        return random.random() < total_crit_chance

    def calculate_critical_damage(
        self, base_damage: float, attacker_stats: Dict, weapon_data: Dict
    ) -> float:
        """Calculate critical hit damage."""
        base_crit_multiplier = 1.5  # 50% bonus damage
        weapon_crit_bonus = weapon_data.get("critical_multiplier", 0.0)
        total_crit_multiplier = base_crit_multiplier + weapon_crit_bonus

        return base_damage * total_crit_multiplier

    def create_encounter(
        self,
        player_id: str,
        area_level: int,
        forced_archetype: MonsterArchetype = None,
        forced_classification=None,
    ) -> Dict:
        """
        Create a complete combat encounter with a player and generated monster.

        Args:
            player_id: ID of the player
            area_level: Base level of the area for monster generation
            forced_archetype: Optional specific monster archetype
        """
        # Get player data
        player_data = self.player_system.get_player(player_id)
        if not player_data:
            return {"error": "Player not found"}

        # Generate monster for this encounter
        monster_data = self.monster_system.generate_encounter_monster(
            area_level, player_data, forced_archetype, forced_classification
        )

        # Create encounter state
        encounter = {
            "player": {
                "id": player_id,
                "name": player_data["name"],
                "current_health": player_data["resources"][StatType.HEALTH],
                "max_health": player_data["resources"][StatType.HEALTH],
                "level": player_data["player_level"],
                "stats": player_data["combat_stats"].copy(),
                "archetype": self._get_player_primary_archetype(player_data),
                "status_effects": [],
            },
            "monster": {
                "name": monster_data["name"],
                "current_health": monster_data["health"],
                "max_health": monster_data["health"],
                "level": monster_data["level"],
                "damage": monster_data["damage"],
                "defense": monster_data["defense"],
                "archetype": monster_data["archetype"],
                "classification": monster_data["classification"],
                "is_wild": monster_data["is_wild"],
                "is_unique": monster_data["is_unique"],
                "status_effects": [],
            },
            "state": {
                "turn": "player",  # Who goes first
                "round": 1,
                "combat_active": True,
            },
            "log": [f"You encounter a {monster_data['name']}!"],
        }

        return encounter

    def player_attack(
        self, encounter: Dict, skill_data: Dict = None, weapon_data: Dict = None
    ) -> Dict:
        """
        Execute a player attack against the monster.

        Args:
            encounter: Current encounter state
            skill_data: Optional skill being used
            weapon_data: Optional weapon data

        Returns:
            Updated encounter state with attack results
        """
        if not encounter["state"]["combat_active"]:
            return encounter

        # Default basic attack if no skill/weapon provided
        if skill_data is None:
            skill_data = {"base_damage": 10, "status_chances": {}}
        if weapon_data is None:
            weapon_data = {"damage": 5, "percentage_bonuses": []}

        # Add player_id to weapon_data for ItemsSystem integration
        weapon_data["player_id"] = encounter["player"]["id"]

        player = encounter["player"]
        monster = encounter["monster"]

        # Convert player stats for damage calculation
        attacker_stats = {
            "power": player["stats"][StatType.DAMAGE],
            "archetype": player["archetype"],
            "critical_chance": player["stats"][StatType.CRITICAL_CHANCE],
        }

        # Convert monster stats for damage calculation
        target_stats = {
            "archetype": monster["archetype"],
            "toughness": monster["defense"],
            "is_wild": monster["is_wild"],
        }

        # Calculate damage
        damage, status_effects = self.calculate_damage(
            attacker_stats, target_stats, skill_data, weapon_data
        )

        # Check for critical hit
        is_crit = self.is_critical_hit(attacker_stats, weapon_data)
        if is_crit:
            damage = self.calculate_critical_damage(damage, attacker_stats, weapon_data)
            encounter["log"].append(f"CRITICAL HIT!")

        # Apply damage to monster
        monster["current_health"] = max(0, monster["current_health"] - damage)

        # Log the attack
        damage_text = f"You deal {damage:.1f} damage"
        if is_crit:
            damage_text += " (CRITICAL!)"
        encounter["log"].append(damage_text)

        # Apply status effects
        for effect in status_effects:
            monster["status_effects"].append(effect.value)
            encounter["log"].append(f"Monster is afflicted with {effect.value}!")

        # Check if monster is defeated
        if monster["current_health"] <= 0:
            encounter["state"]["combat_active"] = False
            encounter["log"].append(f"You defeated the {monster['name']}!")

            # Calculate and award XP
            xp_reward = self._award_victory_xp(encounter)
            encounter["xp_reward"] = xp_reward
        else:
            # Monster's turn
            encounter["state"]["turn"] = "monster"

        return encounter

    def monster_attack(self, encounter: Dict) -> Dict:
        """
        Execute a monster attack against the player.

        Args:
            encounter: Current encounter state

        Returns:
            Updated encounter state with attack results
        """
        if not encounter["state"]["combat_active"]:
            return encounter

        player = encounter["player"]
        monster = encounter["monster"]

        # Convert monster stats for damage calculation
        attacker_stats = {
            "power": monster["damage"],
            "archetype": monster["archetype"],
            "critical_chance": 0.05,  # 5% base crit for monsters
        }

        # Convert player stats for damage calculation
        target_stats = {
            "archetype": player["archetype"],
            "toughness": player["stats"][StatType.DEFENSE],
            "is_wild": False,  # Players are never Wild
        }

        # Basic monster attack
        skill_data = {"base_damage": monster["damage"] * 0.5, "status_chances": {}}
        weapon_data = {"damage": 0, "percentage_bonuses": []}

        # Calculate damage
        damage, status_effects = self.calculate_damage(
            attacker_stats, target_stats, skill_data, weapon_data
        )

        # Apply damage to player
        player["current_health"] = max(0, player["current_health"] - damage)

        # Log the attack
        encounter["log"].append(
            f"The {monster['name']} attacks for {damage:.1f} damage!"
        )

        # Apply status effects to player
        for effect in status_effects:
            player["status_effects"].append(effect.value)
            encounter["log"].append(f"You are afflicted with {effect.value}!")

        # Check if player is defeated
        if player["current_health"] <= 0:
            encounter["state"]["combat_active"] = False
            encounter["log"].append("You have been defeated!")
        else:
            # Player's turn
            encounter["state"]["turn"] = "player"
            encounter["state"]["round"] += 1

        return encounter

    def _get_player_primary_archetype(self, player_data: Dict) -> str:
        """Determine player's primary archetype from their archetype distribution."""
        # Check both archetypes and base_archetypes fields
        archetypes = player_data.get("archetypes", {})
        base_archetypes = player_data.get("base_archetypes", {})

        # Use archetypes if available, otherwise fall back to base_archetypes
        if archetypes:
            # Find the archetype with the highest value
            primary = max(archetypes.items(), key=lambda x: x[1])
            key = primary[0]
        elif base_archetypes:
            # Find the archetype with the highest value
            primary = max(base_archetypes.items(), key=lambda x: x[1])
            key = primary[0]
        else:
            return "melee"  # Default

        # Normalize to string value
        try:
            return key.value if hasattr(key, "value") else str(key)
        except Exception:
            return str(key)

    def _award_victory_xp(self, encounter: Dict) -> Dict[str, int]:
        """
        Award XP to the player for defeating the monster.

        Args:
            encounter: Combat encounter with monster data

        Returns:
            XP reward breakdown
        """
        player = encounter["player"]
        monster = encounter["monster"]

        # Reconstruct monster stats for XP calculation
        monster_stats = {
            "level": monster["level"],
            "is_wild": monster["is_wild"],
            "is_unique": monster["is_unique"],
            "classification": monster["classification"],
        }

        # Calculate XP reward
        xp_reward = self.monster_system.calculate_experience_reward(
            monster_stats, player["archetype"]
        )

        # Award XP to player
        result = self.player_system.add_xp(player["id"], xp_reward)

        return {"xp_gained": xp_reward, "level_up_result": result}


# Example usage and testing
def test_combat_system():
    """Test the combat system with various scenarios."""
    combat = CombatSystem()

    # Test scenario 1: Early game (Level 1-10) - Monster HP: 5, Player HP: 20
    early_attacker_stats = {"power": 2, "archetype": "melee", "critical_chance": 0.05}

    early_target_stats = {"archetype": "ranged", "toughness": 2, "is_wild": False}

    early_skill_data = {
        "base_damage": 1,
        "status_chances": {"burn": 0.05, "stun": 0.02},
    }

    early_weapon_data = {
        "damage": 1,
        "percentage_bonuses": [0.1],  # +10% damage
        "critical_chance": 0.02,
        "critical_multiplier": 0.2,
    }

    # Test scenario 2: Mid game (Level 20-40) - Monster HP: 15-25, Player HP: 40-60
    mid_attacker_stats = {"power": 4, "archetype": "melee", "critical_chance": 0.08}

    mid_target_stats = {"archetype": "ranged", "toughness": 5, "is_wild": False}

    mid_skill_data = {"base_damage": 2, "status_chances": {"burn": 0.08, "stun": 0.04}}

    mid_weapon_data = {
        "damage": 2,
        "percentage_bonuses": [0.15],  # +15% damage
        "critical_chance": 0.03,
        "critical_multiplier": 0.3,
    }

    # Test scenario 3: Late game (Level 60-80) - Monster HP: 40-60, Player HP: 80-120
    late_attacker_stats = {"power": 7, "archetype": "melee", "critical_chance": 0.12}

    late_target_stats = {"archetype": "ranged", "toughness": 8, "is_wild": False}

    late_skill_data = {"base_damage": 3, "status_chances": {"burn": 0.12, "stun": 0.06}}

    late_weapon_data = {
        "damage": 3,
        "percentage_bonuses": [0.2],  # +20% damage
        "critical_chance": 0.05,
        "critical_multiplier": 0.4,
    }

    # Test Early Game
    print("🌱 EARLY GAME TEST (Level 1-10) - Monster HP: 5, Player HP: 20:")
    early_damage, early_effects = combat.calculate_damage(
        early_attacker_stats, early_target_stats, early_skill_data, early_weapon_data
    )
    print(
        f"  Base Damage: {combat._calculate_base_damage(early_attacker_stats, early_skill_data, early_weapon_data):.1f}"
    )
    print(f"  Final Damage: {early_damage:.1f}")
    print(f"  Status Effects: {[effect.value for effect in early_effects]}")

    # Test Mid Game
    print("\n⚔️ MID GAME TEST (Level 20-40) - Monster HP: 15-25, Player HP: 40-60:")
    mid_damage, mid_effects = combat.calculate_damage(
        mid_attacker_stats, mid_target_stats, mid_skill_data, mid_weapon_data
    )
    print(
        f"  Base Damage: {combat._calculate_base_damage(mid_attacker_stats, mid_skill_data, mid_weapon_data):.1f}"
    )
    print(f"  Final Damage: {mid_damage:.1f}")
    print(f"  Status Effects: {[effect.value for effect in mid_effects]}")

    # Test Late Game
    print("\n🔥 LATE GAME TEST (Level 60-80) - Monster HP: 40-60, Player HP: 80-120:")
    late_damage, late_effects = combat.calculate_damage(
        late_attacker_stats, late_target_stats, late_skill_data, late_weapon_data
    )
    print(
        f"  Base Damage: {combat._calculate_base_damage(late_attacker_stats, late_skill_data, late_weapon_data):.1f}"
    )
    print(f"  Final Damage: {late_damage:.1f}")
    print(f"  Status Effects: {[effect.value for effect in late_effects]}")

    # Test Wild Monster (Late Game)
    print("\n🌪️ WILD MONSTER TEST (Late Game):")
    wild_target_stats = late_target_stats.copy()
    wild_target_stats["is_wild"] = True
    wild_target_stats["archetype"] = "melee"  # Same archetype as attacker

    wild_damage, wild_effects = combat.calculate_damage(
        late_attacker_stats, wild_target_stats, late_skill_data, late_weapon_data
    )
    print(f"  Damage vs Wild Monster: {wild_damage:.1f}")
    print(f"  Status Effects: {[effect.value for effect in wild_effects]}")


if __name__ == "__main__":
    test_combat_system()

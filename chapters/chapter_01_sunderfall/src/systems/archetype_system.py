"""
CHRONICLES OF RUIN: ARCHETYPE SYSTEM
====================================

This module handles the archetype system for Chronicles of Ruin.
It manages the 4 main archetypes (Melee, Ranged, Magic, Wild) and their
interactions, bonuses, and special abilities.

PURPOSE:
- Manages the 4 main archetypes and their core mechanics
- Handles archetype-specific bonuses and abilities
- Implements archetype interactions and synergies
- Provides archetype progression and unlocking
- Manages archetype-specific game mechanics

ARCHITECTURE:
- ArchetypeManager: Manages all archetype data and interactions
- ArchetypeBonus: Handles archetype-specific bonuses
- ArchetypeSynergy: Manages archetype combinations and synergies
- ArchetypeProgression: Handles archetype unlocking and progression
- ArchetypeMechanics: Implements archetype-specific game mechanics

ARCHETYPE OVERVIEW:
1. MELEE: Close combat specialists with high physical damage and defense
2. RANGED: Distance fighters with precision and tactical advantages
3. MAGIC: Spellcasters with elemental power and status effects
4. WILD: Unpredictable and chaotic combat with high risk/reward

Each archetype has unique mechanics, bonuses, and playstyles that
contribute to the game's strategic depth and player choice.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import random

class ArchetypeType(Enum):
    """Enumeration of the four main archetypes."""
    MELEE = "melee"
    RANGED = "ranged"
    MAGIC = "magic"
    WILD = "wild"

class ArchetypeBonus(Enum):
    """Enumeration of archetype-specific bonuses."""
    # Melee bonuses
    MELEE_DAMAGE_BONUS = "melee_damage_bonus"
    MELEE_DEFENSE_BONUS = "melee_defense_bonus"
    MELEE_CRITICAL_BONUS = "melee_critical_bonus"
    
    # Ranged bonuses
    RANGED_PRECISION_BONUS = "ranged_precision_bonus"
    RANGED_DISTANCE_BONUS = "ranged_distance_bonus"
    RANGED_CRITICAL_BONUS = "ranged_critical_bonus"
    
    # Magic bonuses
    MAGIC_ELEMENTAL_BONUS = "magic_elemental_bonus"
    MAGIC_STATUS_BONUS = "magic_status_bonus"
    MAGIC_MANA_BONUS = "magic_mana_bonus"
    
    # Wild bonuses
    WILD_CHAOS_BONUS = "wild_chaos_bonus"
    WILD_RANDOM_BONUS = "wild_random_bonus"
    WILD_RISK_BONUS = "wild_risk_bonus"

class ArchetypeSystem:
    """
    Main archetype system that manages all archetype-related functionality.
    Handles archetype bonuses, synergies, and interactions.
    """
    
    def __init__(self):
        """Initialize the archetype system."""
        self.archetypes = self._initialize_archetypes()
        self.bonuses = self._initialize_bonuses()
        self.synergies = self._initialize_synergies()
        self.unlocked_archetypes = set([ArchetypeType.MELEE, ArchetypeType.RANGED, 
                                       ArchetypeType.MAGIC, ArchetypeType.WILD])
    
    def _initialize_archetypes(self) -> Dict[ArchetypeType, Dict]:
        """Initialize all archetypes with their core information."""
        return {
            ArchetypeType.MELEE: {
                'name': 'Melee',
                'description': 'Close combat specialists who excel in physical combat',
                'primary_stat': 'strength',
                'secondary_stat': 'constitution',
                'base_damage_bonus': 1.2,
                'base_defense_bonus': 1.3,
                'critical_chance': 0.15,
                'special_ability': 'Close Combat Mastery',
                'unlock_requirement': None
            },
            ArchetypeType.RANGED: {
                'name': 'Ranged',
                'description': 'Distance fighters who attack from afar',
                'primary_stat': 'dexterity',
                'secondary_stat': 'perception',
                'base_damage_bonus': 1.1,
                'base_defense_bonus': 0.9,
                'critical_chance': 0.20,
                'special_ability': 'Precision Shot',
                'unlock_requirement': None
            },
            ArchetypeType.MAGIC: {
                'name': 'Magic',
                'description': 'Spellcasters who wield arcane and elemental power',
                'primary_stat': 'intelligence',
                'secondary_stat': 'wisdom',
                'base_damage_bonus': 1.3,
                'base_defense_bonus': 0.8,
                'critical_chance': 0.10,
                'special_ability': 'Elemental Mastery',
                'unlock_requirement': None
            },
            ArchetypeType.WILD: {
                'name': 'Wild',
                'description': 'Unpredictable and chaotic combat styles',
                'primary_stat': 'chaos',
                'secondary_stat': 'luck',
                'base_damage_bonus': 1.5,
                'base_defense_bonus': 0.7,
                'critical_chance': 0.25,
                'special_ability': 'Chaos Surge',
                'unlock_requirement': 'Complete tutorial'
            }
        }
    
    def _initialize_bonuses(self) -> Dict[ArchetypeBonus, Dict]:
        """Initialize archetype-specific bonuses."""
        return {
            ArchetypeBonus.MELEE_DAMAGE_BONUS: {
                'archetype': ArchetypeType.MELEE,
                'description': 'Increases physical damage by 20%',
                'value': 0.2,
                'type': 'damage_multiplier'
            },
            ArchetypeBonus.MELEE_DEFENSE_BONUS: {
                'archetype': ArchetypeType.MELEE,
                'description': 'Increases physical defense by 30%',
                'value': 0.3,
                'type': 'defense_multiplier'
            },
            ArchetypeBonus.MELEE_CRITICAL_BONUS: {
                'archetype': ArchetypeType.MELEE,
                'description': 'Increases critical hit chance by 15%',
                'value': 0.15,
                'type': 'critical_chance'
            },
            ArchetypeBonus.RANGED_PRECISION_BONUS: {
                'archetype': ArchetypeType.RANGED,
                'description': 'Increases accuracy and reduces miss chance',
                'value': 0.25,
                'type': 'accuracy_bonus'
            },
            ArchetypeBonus.RANGED_DISTANCE_BONUS: {
                'archetype': ArchetypeType.RANGED,
                'description': 'Increases effective range and damage at distance',
                'value': 0.3,
                'type': 'range_bonus'
            },
            ArchetypeBonus.RANGED_CRITICAL_BONUS: {
                'archetype': ArchetypeType.RANGED,
                'description': 'Increases critical hit chance by 20%',
                'value': 0.20,
                'type': 'critical_chance'
            },
            ArchetypeBonus.MAGIC_ELEMENTAL_BONUS: {
                'archetype': ArchetypeType.MAGIC,
                'description': 'Increases elemental damage by 30%',
                'value': 0.3,
                'type': 'elemental_damage'
            },
            ArchetypeBonus.MAGIC_STATUS_BONUS: {
                'archetype': ArchetypeType.MAGIC,
                'description': 'Increases status effect chance and duration',
                'value': 0.25,
                'type': 'status_effect_bonus'
            },
            ArchetypeBonus.MAGIC_MANA_BONUS: {
                'archetype': ArchetypeType.MAGIC,
                'description': 'Increases mana pool and regeneration',
                'value': 0.4,
                'type': 'mana_bonus'
            },
            ArchetypeBonus.WILD_CHAOS_BONUS: {
                'archetype': ArchetypeType.WILD,
                'description': 'Increases chaos damage and random effects',
                'value': 0.5,
                'type': 'chaos_damage'
            },
            ArchetypeBonus.WILD_RANDOM_BONUS: {
                'archetype': ArchetypeType.WILD,
                'description': 'Random chance for bonus effects',
                'value': 0.3,
                'type': 'random_bonus'
            },
            ArchetypeBonus.WILD_RISK_BONUS: {
                'archetype': ArchetypeType.WILD,
                'description': 'High risk, high reward damage bonus',
                'value': 0.4,
                'type': 'risk_reward'
            }
        }
    
    def _initialize_synergies(self) -> Dict[Tuple[ArchetypeType, ArchetypeType], Dict]:
        """Initialize archetype synergy combinations."""
        return {
            (ArchetypeType.MELEE, ArchetypeType.RANGED): {
                'name': 'Hybrid Combat',
                'description': 'Combines melee and ranged tactics',
                'bonus': 'Gain both melee and ranged bonuses at 50% effectiveness',
                'effect': 'hybrid_combat'
            },
            (ArchetypeType.MELEE, ArchetypeType.MAGIC): {
                'name': 'Battle Mage',
                'description': 'Combines physical combat with magical enhancement',
                'bonus': 'Physical attacks gain elemental properties',
                'effect': 'battle_mage'
            },
            (ArchetypeType.RANGED, ArchetypeType.MAGIC): {
                'name': 'Arcane Archer',
                'description': 'Combines precision with magical arrows',
                'bonus': 'Ranged attacks can apply status effects',
                'effect': 'arcane_archer'
            },
            (ArchetypeType.WILD, ArchetypeType.MELEE): {
                'name': 'Berserker',
                'description': 'Combines chaos with raw physical power',
                'bonus': 'Random critical hits and damage spikes',
                'effect': 'berserker'
            },
            (ArchetypeType.WILD, ArchetypeType.MAGIC): {
                'name': 'Chaos Mage',
                'description': 'Combines chaos with magical power',
                'bonus': 'Random spell effects and amplified chaos',
                'effect': 'chaos_mage'
            }
        }
    
    def get_archetype_info(self, archetype: ArchetypeType) -> Dict:
        """Get information about a specific archetype."""
        return self.archetypes.get(archetype, {})
    
    def get_archetype_bonus(self, archetype: ArchetypeType, bonus_type: str) -> float:
        """Get a specific bonus value for an archetype."""
        for bonus_enum, bonus_data in self.bonuses.items():
            if bonus_data['archetype'] == archetype and bonus_type in bonus_enum.value:
                return bonus_data['value']
        return 0.0
    
    def get_all_archetypes(self) -> List[ArchetypeType]:
        """Get a list of all available archetypes."""
        return list(self.archetypes.keys())
    
    def get_unlocked_archetypes(self) -> List[ArchetypeType]:
        """Get a list of unlocked archetypes."""
        return list(self.unlocked_archetypes)
    
    def unlock_archetype(self, archetype: ArchetypeType) -> bool:
        """
        Unlock an archetype for use.
        
        Args:
            archetype: Archetype to unlock
            
        Returns:
            True if unlocked successfully, False otherwise
        """
        if archetype in self.unlocked_archetypes:
            return True
        
        # Check unlock requirements
        archetype_info = self.get_archetype_info(archetype)
        requirement = archetype_info.get('unlock_requirement')
        
        if requirement is None or self._check_unlock_requirement(requirement):
            self.unlocked_archetypes.add(archetype)
            print(f"✓ Unlocked archetype: {archetype.value.title()}")
            return True
        else:
            print(f"✗ Cannot unlock {archetype.value.title()}: {requirement}")
            return False
    
    def _check_unlock_requirement(self, requirement: str) -> bool:
        """Check if an unlock requirement is met."""
        # This would be implemented based on game state
        # For now, assume all requirements are met
        return True
    
    def get_archetype_synergy(self, archetype1: ArchetypeType, archetype2: ArchetypeType) -> Optional[Dict]:
        """
        Get synergy information between two archetypes.
        
        Args:
            archetype1: First archetype
            archetype2: Second archetype
            
        Returns:
            Synergy data if exists, None otherwise
        """
        # Check both combinations
        synergy_key1 = (archetype1, archetype2)
        synergy_key2 = (archetype2, archetype1)
        
        if synergy_key1 in self.synergies:
            return self.synergies[synergy_key1]
        elif synergy_key2 in self.synergies:
            return self.synergies[synergy_key2]
        else:
            return None
    
    def calculate_archetype_bonus(self, archetype: ArchetypeType, base_value: float, 
                                 bonus_type: str) -> float:
        """
        Calculate the bonus value for an archetype.
        
        Args:
            archetype: Archetype to calculate bonus for
            base_value: Base value to apply bonus to
            bonus_type: Type of bonus to calculate
            
        Returns:
            Modified value with archetype bonus applied
        """
        bonus = self.get_archetype_bonus(archetype, bonus_type)
        return base_value * (1 + bonus)
    
    def get_archetype_special_ability(self, archetype: ArchetypeType) -> str:
        """Get the special ability name for an archetype."""
        archetype_info = self.get_archetype_info(archetype)
        return archetype_info.get('special_ability', 'None')
    
    def apply_archetype_effects(self, archetype: ArchetypeType, damage: float, 
                               defense: float, critical_chance: float) -> Tuple[float, float, float]:
        """
        Apply archetype effects to combat stats.
        
        Args:
            archetype: Archetype to apply effects for
            damage: Base damage value
            defense: Base defense value
            critical_chance: Base critical chance
            
        Returns:
            Tuple of (modified_damage, modified_defense, modified_critical_chance)
        """
        archetype_info = self.get_archetype_info(archetype)
        
        # Apply damage bonus
        damage_bonus = archetype_info.get('base_damage_bonus', 1.0)
        modified_damage = damage * damage_bonus
        
        # Apply defense bonus
        defense_bonus = archetype_info.get('base_defense_bonus', 1.0)
        modified_defense = defense * defense_bonus
        
        # Apply critical chance bonus
        crit_bonus = archetype_info.get('critical_chance', 0.0)
        modified_critical = critical_chance + crit_bonus
        
        return modified_damage, modified_defense, modified_critical
    
    def get_archetype_summary(self, archetype: ArchetypeType) -> Dict:
        """Get a comprehensive summary of an archetype."""
        archetype_info = self.get_archetype_info(archetype)
        
        summary = {
            'name': archetype_info.get('name', archetype.value.title()),
            'description': archetype_info.get('description', ''),
            'primary_stat': archetype_info.get('primary_stat', ''),
            'secondary_stat': archetype_info.get('secondary_stat', ''),
            'special_ability': archetype_info.get('special_ability', ''),
            'is_unlocked': archetype in self.unlocked_archetypes,
            'bonuses': []
        }
        
        # Add applicable bonuses
        for bonus_enum, bonus_data in self.bonuses.items():
            if bonus_data['archetype'] == archetype:
                summary['bonuses'].append({
                    'name': bonus_enum.value,
                    'description': bonus_data['description'],
                    'value': bonus_data['value'],
                    'type': bonus_data['type']
                })
        
        return summary

# Example usage and testing
if __name__ == "__main__":
    archetype_system = ArchetypeSystem()
    
    # Test getting archetype info
    melee_info = archetype_system.get_archetype_info(ArchetypeType.MELEE)
    print(f"Melee archetype: {melee_info['name']}")
    
    # Test archetype bonus calculation
    base_damage = 100.0
    modified_damage = archetype_system.calculate_archetype_bonus(
        ArchetypeType.MELEE, base_damage, "damage"
    )
    print(f"Base damage: {base_damage}, Modified: {modified_damage}")
    
    # Test synergy
    synergy = archetype_system.get_archetype_synergy(ArchetypeType.MELEE, ArchetypeType.RANGED)
    if synergy:
        print(f"Synergy found: {synergy['name']}")
    
    # Test archetype summary
    summary = archetype_system.get_archetype_summary(ArchetypeType.MAGIC)
    print(f"Magic archetype summary: {summary['name']}")
    print(f"Special ability: {summary['special_ability']}")

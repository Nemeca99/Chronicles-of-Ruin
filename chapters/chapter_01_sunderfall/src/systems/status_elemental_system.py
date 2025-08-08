"""
CHRONICLES OF RUIN: STATUS AND ELEMENTAL SYSTEM
===============================================

This module handles all status effects, elemental mechanics, and the resistance system
for Chronicles of Ruin. It implements the clean damage system where all damage is
either physical or status-based, with status effects having their own resistance types.

PURPOSE:
- Manages status effects (burn, freeze, stun, etc.)
- Handles elemental damage calculations
- Implements the resistance system (physical vs status)
- Provides status effect application and duration tracking
- Manages elemental skill interactions and combos

ARCHITECTURE:
- StatusEffect: Base class for all status effects
- ElementalSystem: Handles fire, ice, lightning interactions
- ResistanceSystem: Manages physical and status resistances
- StatusTracker: Tracks active status effects on entities
- DamageCalculator: Calculates damage with status effects

DAMAGE SYSTEM RULES:
- All damage is either Physical or Status
- Physical: Basic attacks, weapon damage, non-elemental skills
- Status: Elemental effects (burn, freeze, stun, etc.)
- Status effects have a chance to apply and deal damage over time
- Status damage is calculated as percentage of initial damage
- Each status type has its own resistance (burn resistance, stun resistance, etc.)

STATUS EFFECT TYPES:
- BURN: Fire-based, deals damage over time (50% of initial damage over 2 seconds)
- FREEZE: Ice-based, slows and may freeze enemies
- STUN: Lightning-based, prevents actions for duration
- POISON: Nature-based, deals damage over time
- BLEED: Physical-based, deals damage over time
- CHAOS: Wild-based, random effects

ELEMENTAL INTERACTIONS:
- Fire + Ice: Shatter effect (bonus damage)
- Lightning + Water: Chain lightning effect
- Fire + Poison: Explosive poison
- Chaos + Any: Random amplification

This system provides tactical depth while maintaining simplicity and clarity
for players to understand and strategize around.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import random
import time

class StatusType(Enum):
    """Enumeration of all status effect types."""
    BURN = "burn"
    FREEZE = "freeze"
    STUN = "stun"
    POISON = "poison"
    BLEED = "bleed"
    CHAOS = "chaos"

class ElementalType(Enum):
    """Enumeration of elemental types for skills."""
    FIRE = "fire"
    ICE = "ice"
    LIGHTNING = "lightning"
    NATURE = "nature"
    PHYSICAL = "physical"
    CHAOS = "chaos"

class StatusEffect:
    """
    Base class for all status effects.
    Handles application, duration, damage calculation, and removal.
    """
    
    def __init__(self, status_type: StatusType, duration: float, 
                 damage_per_tick: float, tick_interval: float = 1.0):
        """
        Initialize a status effect.
        
        Args:
            status_type: Type of status effect
            duration: How long the effect lasts (seconds)
            damage_per_tick: Damage dealt each tick
            tick_interval: Time between damage ticks (seconds)
        """
        self.status_type = status_type
        self.duration = duration
        self.damage_per_tick = damage_per_tick
        self.tick_interval = tick_interval
        self.time_applied = time.time()
        self.last_tick_time = time.time()
        self.is_active = True
    
    def get_remaining_duration(self) -> float:
        """Get remaining duration of the status effect."""
        elapsed = time.time() - self.time_applied
        return max(0, self.duration - elapsed)
    
    def should_tick(self) -> bool:
        """Check if the status effect should deal damage this tick."""
        if not self.is_active:
            return False
        
        current_time = time.time()
        if current_time - self.last_tick_time >= self.tick_interval:
            self.last_tick_time = current_time
            return True
        return False
    
    def tick(self) -> float:
        """Process one tick of the status effect and return damage dealt."""
        if self.should_tick():
            return self.damage_per_tick
        return 0.0
    
    def check_expired(self) -> bool:
        """Check if the status effect has expired and should be removed."""
        if time.time() - self.time_applied >= self.duration:
            self.is_active = False
            return True
        return False
    
    def get_description(self) -> str:
        """Get a description of the status effect."""
        return f"{self.status_type.value.title()}: {self.damage_per_tick} damage per {self.tick_interval}s for {self.duration}s"

class StatusElementalSystem:
    """
    Main system for managing status effects and elemental interactions.
    Handles application, tracking, and removal of status effects.
    """
    
    def __init__(self):
        """Initialize the status and elemental system."""
        self.status_effects = {}  # entity_id -> list of active status effects
        self.resistance_data = {}  # entity_id -> resistance values
        self.elemental_combos = self._initialize_elemental_combos()
        self.status_definitions = self._initialize_status_definitions()
    
    def _initialize_status_definitions(self) -> Dict[StatusType, Dict]:
        """Initialize the definitions for all status effects."""
        return {
            StatusType.BURN: {
                'elemental_type': ElementalType.FIRE,
                'base_duration': 2.0,
                'damage_percentage': 0.5,  # 50% of initial damage
                'tick_interval': 0.5,
                'description': 'Burns the target, dealing fire damage over time'
            },
            StatusType.FREEZE: {
                'elemental_type': ElementalType.ICE,
                'base_duration': 1.5,
                'damage_percentage': 0.3,
                'tick_interval': 0.5,
                'description': 'Freezes the target, dealing ice damage and slowing'
            },
            StatusType.STUN: {
                'elemental_type': ElementalType.LIGHTNING,
                'base_duration': 1.0,
                'damage_percentage': 0.0,  # Stun doesn't deal damage
                'tick_interval': 1.0,
                'description': 'Stuns the target, preventing actions'
            },
            StatusType.POISON: {
                'elemental_type': ElementalType.NATURE,
                'base_duration': 3.0,
                'damage_percentage': 0.4,
                'tick_interval': 0.5,
                'description': 'Poisons the target, dealing nature damage over time'
            },
            StatusType.BLEED: {
                'elemental_type': ElementalType.PHYSICAL,
                'base_duration': 2.5,
                'damage_percentage': 0.35,
                'tick_interval': 0.5,
                'description': 'Causes bleeding, dealing physical damage over time'
            },
            StatusType.CHAOS: {
                'elemental_type': ElementalType.CHAOS,
                'base_duration': 2.0,
                'damage_percentage': 0.6,
                'tick_interval': 0.3,
                'description': 'Chaos effect with random damage and effects'
            }
        }
    
    def _initialize_elemental_combos(self) -> Dict[Tuple[ElementalType, ElementalType], Dict]:
        """Initialize elemental interaction combinations."""
        return {
            (ElementalType.FIRE, ElementalType.ICE): {
                'name': 'Shatter',
                'effect': 'Fire shatters frozen enemies for bonus damage',
                'damage_multiplier': 1.5,
                'description': 'Fire attacks deal 50% bonus damage to frozen enemies'
            },
            (ElementalType.LIGHTNING, ElementalType.ICE): {
                'name': 'Conduct',
                'effect': 'Lightning conducts through frozen enemies',
                'damage_multiplier': 1.3,
                'description': 'Lightning attacks deal 30% bonus damage to frozen enemies'
            },
            (ElementalType.FIRE, ElementalType.NATURE): {
                'name': 'Explosive',
                'effect': 'Fire ignites poison for explosive damage',
                'damage_multiplier': 2.0,
                'description': 'Fire attacks on poisoned enemies cause explosions'
            },
            (ElementalType.CHAOS, ElementalType.FIRE): {
                'name': 'Chaos Flame',
                'effect': 'Chaos amplifies fire effects randomly',
                'damage_multiplier': 1.2,
                'description': 'Chaos randomly amplifies fire damage'
            }
        }
    
    def apply_status_effect(self, target_id: str, status_type: StatusType, 
                          initial_damage: float, chance: float = 1.0) -> bool:
        """
        Apply a status effect to a target.
        
        Args:
            target_id: ID of the target entity
            status_type: Type of status effect to apply
            initial_damage: Initial damage that caused the status effect
            chance: Chance of applying the status effect (0.0 to 1.0)
            
        Returns:
            True if status effect was applied, False otherwise
        """
        # Check if status effect should be applied
        if random.random() > chance:
            return False
        
        # Get status effect definition
        status_def = self.status_definitions.get(status_type)
        if not status_def:
            return False
        
        # Calculate status effect damage
        damage_per_tick = initial_damage * status_def['damage_percentage']
        
        # Apply resistance
        resistance = self.get_status_resistance(target_id, status_type)
        damage_per_tick = max(0, damage_per_tick - resistance)
        
        # Create status effect
        status_effect = StatusEffect(
            status_type=status_type,
            duration=status_def['base_duration'],
            damage_per_tick=damage_per_tick,
            tick_interval=status_def['tick_interval']
        )
        
        # Add to target's status effects
        if target_id not in self.status_effects:
            self.status_effects[target_id] = []
        
        self.status_effects[target_id].append(status_effect)
        return True
    
    def get_status_resistance(self, entity_id: str, status_type: StatusType) -> float:
        """Get the resistance value for a specific status type on an entity."""
        if entity_id not in self.resistance_data:
            return 0.0
        
        resistance_key = f"{status_type.value}_resistance"
        return self.resistance_data[entity_id].get(resistance_key, 0.0)
    
    def set_status_resistance(self, entity_id: str, status_type: StatusType, resistance: float):
        """Set the resistance value for a specific status type on an entity."""
        if entity_id not in self.resistance_data:
            self.resistance_data[entity_id] = {}
        
        resistance_key = f"{status_type.value}_resistance"
        self.resistance_data[entity_id][resistance_key] = resistance
    
    def process_status_effects(self, entity_id: str) -> Dict[StatusType, float]:
        """
        Process all status effects for an entity and return damage dealt.
        
        Args:
            entity_id: ID of the entity to process
            
        Returns:
            Dict mapping status type to damage dealt
        """
        if entity_id not in self.status_effects:
            return {}
        
        damage_dealt = {}
        active_effects = []
        
        for effect in self.status_effects[entity_id]:
            # Check if effect has expired
            if effect.check_expired():
                continue
            
            # Process tick
            damage = effect.tick()
            if damage > 0:
                damage_dealt[effect.status_type] = damage
            
            active_effects.append(effect)
        
        # Update active effects list
        self.status_effects[entity_id] = active_effects
        
        return damage_dealt
    
    def get_active_status_effects(self, entity_id: str) -> List[StatusEffect]:
        """Get all active status effects for an entity."""
        if entity_id not in self.status_effects:
            return []
        
        # Remove expired effects
        active_effects = []
        for effect in self.status_effects[entity_id]:
            if not effect.check_expired():
                active_effects.append(effect)
        
        self.status_effects[entity_id] = active_effects
        return active_effects
    
    def clear_status_effects(self, entity_id: str, status_type: Optional[StatusType] = None):
        """
        Clear status effects from an entity.
        
        Args:
            entity_id: ID of the entity
            status_type: Specific status type to clear (None for all)
        """
        if entity_id not in self.status_effects:
            return
        
        if status_type is None:
            # Clear all status effects
            self.status_effects[entity_id] = []
        else:
            # Clear specific status type
            active_effects = []
            for effect in self.status_effects[entity_id]:
                if effect.status_type != status_type:
                    active_effects.append(effect)
            self.status_effects[entity_id] = active_effects
    
    def check_elemental_combo(self, attacker_element: ElementalType, 
                            target_id: str) -> Optional[Dict]:
        """
        Check for elemental combo effects when attacking.
        
        Args:
            attacker_element: Elemental type of the attack
            target_id: ID of the target entity
            
        Returns:
            Combo effect data if applicable, None otherwise
        """
        active_effects = self.get_active_status_effects(target_id)
        
        for effect in active_effects:
            effect_element = self.status_definitions[effect.status_type]['elemental_type']
            combo_key = (attacker_element, effect_element)
            
            if combo_key in self.elemental_combos:
                return self.elemental_combos[combo_key]
        
        return None
    
    def calculate_damage_with_status(self, base_damage: float, skill_element: ElementalType,
                                   target_id: str, status_chance: float = 0.3) -> Tuple[float, List[StatusType]]:
        """
        Calculate damage including potential status effects.
        
        Args:
            base_damage: Base damage of the attack
            skill_element: Elemental type of the skill
            target_id: ID of the target
            status_chance: Chance to apply status effect
            
        Returns:
            Tuple of (total_damage, applied_status_effects)
        """
        total_damage = base_damage
        applied_statuses = []
        
        # Check for elemental combos
        combo_effect = self.check_elemental_combo(skill_element, target_id)
        if combo_effect:
            total_damage *= combo_effect['damage_multiplier']
        
        # Determine status effect type based on elemental type
        status_type = self._get_status_type_for_element(skill_element)
        if status_type:
            if self.apply_status_effect(target_id, status_type, base_damage, status_chance):
                applied_statuses.append(status_type)
        
        return total_damage, applied_statuses
    
    def _get_status_type_for_element(self, element: ElementalType) -> Optional[StatusType]:
        """Get the status type associated with an elemental type."""
        element_status_map = {
            ElementalType.FIRE: StatusType.BURN,
            ElementalType.ICE: StatusType.FREEZE,
            ElementalType.LIGHTNING: StatusType.STUN,
            ElementalType.NATURE: StatusType.POISON,
            ElementalType.PHYSICAL: StatusType.BLEED,
            ElementalType.CHAOS: StatusType.CHAOS
        }
        return element_status_map.get(element)
    
    def get_status_summary(self, entity_id: str) -> Dict:
        """Get a summary of all active status effects for an entity."""
        active_effects = self.get_active_status_effects(entity_id)
        
        summary = {
            'active_effects': [],
            'total_damage_per_tick': 0.0,
            'effect_count': len(active_effects)
        }
        
        for effect in active_effects:
            summary['active_effects'].append({
                'type': effect.status_type.value,
                'remaining_duration': effect.get_remaining_duration(),
                'damage_per_tick': effect.damage_per_tick,
                'description': effect.get_description()
            })
            summary['total_damage_per_tick'] += effect.damage_per_tick
        
        return summary

# Example usage and testing
if __name__ == "__main__":
    status_system = StatusElementalSystem()
    
    # Test status effect application
    target_id = "test_enemy"
    initial_damage = 20.0
    
    # Apply burn effect
    applied = status_system.apply_status_effect(target_id, StatusType.BURN, initial_damage, 0.8)
    print(f"Burn applied: {applied}")
    
    # Set some resistance
    status_system.set_status_resistance(target_id, StatusType.BURN, 2.0)
    
    # Process status effects
    damage_dealt = status_system.process_status_effects(target_id)
    print(f"Damage dealt: {damage_dealt}")
    
    # Get status summary
    summary = status_system.get_status_summary(target_id)
    print(f"Status summary: {summary}")
    
    # Test elemental combo
    combo = status_system.check_elemental_combo(ElementalType.FIRE, target_id)
    print(f"Elemental combo: {combo}")

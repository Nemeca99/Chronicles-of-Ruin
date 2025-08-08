#!/usr/bin/env python3
"""
Resistance System for Chronicles of Ruin
Implements resistance mechanics with boss immunities and damage calculations
"""

import random
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass

class ResistanceType(Enum):
    """Types of resistances in the game"""
    PHYSICAL = "physical"
    FIRE = "fire"
    ICE = "ice"
    LIGHTNING = "lightning"
    POISON = "poison"
    BLEED = "bleed"
    STUN = "stun"
    FREEZE = "freeze"
    SLOW = "slow"
    CHAOS = "chaos"

class EntityType(Enum):
    """Types of entities for immunity purposes"""
    REGULAR_MONSTER = "regular_monster"
    BOSS = "boss"
    PLAYER = "player"
    NPC = "npc"

@dataclass
class ResistanceProfile:
    """Complete resistance profile for an entity"""
    entity_type: EntityType
    resistances: Dict[ResistanceType, float]  # -99 to +99 for regular, -99 to +100 for bosses
    immunities: List[ResistanceType]  # Bosses only
    vulnerabilities: List[ResistanceType]  # Takes extra damage
    
    def __post_init__(self):
        if self.resistances is None:
            self.resistances = {}
        if self.immunities is None:
            self.immunities = []
        if self.vulnerabilities is None:
            self.vulnerabilities = []

class ResistanceSystem:
    """Manages resistance calculations and boss immunities"""
    
    def __init__(self):
        self.max_regular_resistance = 99.0  # Max for regular entities
        self.max_boss_resistance = 100.0    # Max for bosses (only for immunities)
        self.min_resistance = -99.0         # Minimum resistance (negative = vulnerability)
        
        # Boss immunities (cannot be stunned or frozen, but can be slowed)
        self.boss_immunities = [ResistanceType.STUN, ResistanceType.FREEZE]
        
        # Initialize default resistance profiles
        self._initialize_default_profiles()
    
    def _initialize_default_profiles(self):
        """Initialize default resistance profiles for different entity types"""
        self.default_profiles = {
            EntityType.REGULAR_MONSTER: ResistanceProfile(
                entity_type=EntityType.REGULAR_MONSTER,
                resistances={
                    ResistanceType.PHYSICAL: 0.0,
                    ResistanceType.FIRE: 0.0,
                    ResistanceType.ICE: 0.0,
                    ResistanceType.LIGHTNING: 0.0,
                    ResistanceType.POISON: 0.0,
                    ResistanceType.BLEED: 0.0,
                    ResistanceType.STUN: 0.0,
                    ResistanceType.FREEZE: 0.0,
                    ResistanceType.SLOW: 0.0,
                    ResistanceType.CHAOS: 0.0
                },
                immunities=[],
                vulnerabilities=[]
            ),
            EntityType.BOSS: ResistanceProfile(
                entity_type=EntityType.BOSS,
                resistances={
                    ResistanceType.PHYSICAL: 0.0,
                    ResistanceType.FIRE: 0.0,
                    ResistanceType.ICE: 0.0,
                    ResistanceType.LIGHTNING: 0.0,
                    ResistanceType.POISON: 0.0,
                    ResistanceType.BLEED: 0.0,
                    ResistanceType.STUN: 100.0,  # Immune to stun
                    ResistanceType.FREEZE: 100.0, # Immune to freeze
                    ResistanceType.SLOW: 0.0,     # Can be slowed
                    ResistanceType.CHAOS: 0.0
                },
                immunities=[ResistanceType.STUN, ResistanceType.FREEZE],
                vulnerabilities=[]
            ),
            EntityType.PLAYER: ResistanceProfile(
                entity_type=EntityType.PLAYER,
                resistances={
                    ResistanceType.PHYSICAL: 0.0,
                    ResistanceType.FIRE: 0.0,
                    ResistanceType.ICE: 0.0,
                    ResistanceType.LIGHTNING: 0.0,
                    ResistanceType.POISON: 0.0,
                    ResistanceType.BLEED: 0.0,
                    ResistanceType.STUN: 0.0,
                    ResistanceType.FREEZE: 0.0,
                    ResistanceType.SLOW: 0.0,
                    ResistanceType.CHAOS: 0.0
                },
                immunities=[],
                vulnerabilities=[]
            )
        }
    
    def create_resistance_profile(self, entity_type: EntityType, 
                                custom_resistances: Dict[ResistanceType, float] = None,
                                immunities: List[ResistanceType] = None,
                                vulnerabilities: List[ResistanceType] = None) -> ResistanceProfile:
        """Create a resistance profile for an entity"""
        base_profile = self.default_profiles[entity_type].resistances.copy()
        
        if custom_resistances:
            base_profile.update(custom_resistances)
        
        # Validate resistances
        for resistance_type, value in base_profile.items():
            if entity_type == EntityType.BOSS and resistance_type in self.boss_immunities:
                # Bosses can have 100% resistance for immunities
                base_profile[resistance_type] = max(self.min_resistance, min(value, self.max_boss_resistance))
            else:
                # Regular entities max at 99%
                base_profile[resistance_type] = max(self.min_resistance, min(value, self.max_regular_resistance))
        
        return ResistanceProfile(
            entity_type=entity_type,
            resistances=base_profile,
            immunities=immunities or [],
            vulnerabilities=vulnerabilities or []
        )
    
    def calculate_damage_with_resistance(self, base_damage: float, 
                                       damage_type: ResistanceType,
                                       target_profile: ResistanceProfile) -> float:
        """
        Calculate damage after applying resistance.
        Resistance is applied to BASE damage, not modified damage.
        """
        resistance = target_profile.resistances.get(damage_type, 0.0)
        
        # Apply resistance (positive = damage reduction, negative = damage increase)
        resistance_multiplier = (100.0 - resistance) / 100.0
        
        # Ensure minimum damage
        final_damage = max(1.0, base_damage * resistance_multiplier)
        
        return final_damage
    
    def can_apply_status_effect(self, status_type: ResistanceType, 
                               target_profile: ResistanceProfile) -> bool:
        """Check if a status effect can be applied to the target"""
        # Bosses are immune to certain status effects
        if target_profile.entity_type == EntityType.BOSS:
            if status_type in target_profile.immunities:
                return False
        
        # Check resistance
        resistance = target_profile.resistances.get(status_type, 0.0)
        if resistance >= 100.0:
            return False
        
        return True
    
    def calculate_status_effect_chance(self, status_type: ResistanceType,
                                     target_profile: ResistanceProfile,
                                     base_chance: float = 1.0) -> float:
        """Calculate the chance of applying a status effect"""
        if not self.can_apply_status_effect(status_type, target_profile):
            return 0.0
        
        resistance = target_profile.resistances.get(status_type, 0.0)
        
        # Resistance reduces chance of application
        chance_multiplier = (100.0 - resistance) / 100.0
        final_chance = base_chance * chance_multiplier
        
        return max(0.0, min(1.0, final_chance))
    
    def get_resistance_summary(self, profile: ResistanceProfile) -> Dict:
        """Get a summary of resistances and immunities"""
        summary = {
            "entity_type": profile.entity_type.value,
            "resistances": {},
            "immunities": [immunity.value for immunity in profile.immunities],
            "vulnerabilities": [vuln.value for vuln in profile.vulnerabilities]
        }
        
        for resistance_type, value in profile.resistances.items():
            summary["resistances"][resistance_type.value] = value
        
        return summary
    
    def create_boss_profile(self, boss_name: str, 
                          custom_resistances: Dict[ResistanceType, float] = None,
                          vulnerabilities: List[ResistanceType] = None) -> Tuple[str, ResistanceProfile]:
        """Create a boss resistance profile with immunities"""
        profile = self.create_resistance_profile(
            EntityType.BOSS,
            custom_resistances=custom_resistances,
            immunities=self.boss_immunities,
            vulnerabilities=vulnerabilities
        )
        
        return boss_name, profile
    
    def create_monster_profile(self, monster_name: str,
                             custom_resistances: Dict[ResistanceType, float] = None,
                             immunities: List[ResistanceType] = None,
                             vulnerabilities: List[ResistanceType] = None) -> Tuple[str, ResistanceProfile]:
        """Create a regular monster resistance profile"""
        profile = self.create_resistance_profile(
            EntityType.REGULAR_MONSTER,
            custom_resistances=custom_resistances,
            immunities=immunities,
            vulnerabilities=vulnerabilities
        )
        
        return monster_name, profile
    
    def create_player_profile(self, player_name: str,
                            custom_resistances: Dict[ResistanceType, float] = None,
                            immunities: List[ResistanceType] = None,
                            vulnerabilities: List[ResistanceType] = None) -> Tuple[str, ResistanceProfile]:
        """Create a player resistance profile"""
        profile = self.create_resistance_profile(
            EntityType.PLAYER,
            custom_resistances=custom_resistances,
            immunities=immunities,
            vulnerabilities=vulnerabilities
        )
        
        return player_name, profile

def main():
    """Test the resistance system"""
    resistance_system = ResistanceSystem()
    
    print("🛡️ RESISTANCE SYSTEM TEST")
    print("=" * 50)
    
    # Test regular monster
    monster_name, monster_profile = resistance_system.create_monster_profile(
        "Goblin Warrior",
        custom_resistances={
            ResistanceType.FIRE: 25.0,
            ResistanceType.PHYSICAL: -10.0  # Takes 10% more physical damage
        }
    )
    
    print(f"\n📊 {monster_name} Resistance Profile:")
    summary = resistance_system.get_resistance_summary(monster_profile)
    for resistance_type, value in summary["resistances"].items():
        print(f"  {resistance_type}: {value}%")
    
    # Test boss
    boss_name, boss_profile = resistance_system.create_boss_profile(
        "Ancient Dragon",
        custom_resistances={
            ResistanceType.FIRE: 75.0,
            ResistanceType.ICE: -25.0,  # Vulnerable to ice
            ResistanceType.PHYSICAL: 50.0
        },
        vulnerabilities=[ResistanceType.ICE]
    )
    
    print(f"\n🐉 {boss_name} Resistance Profile:")
    summary = resistance_system.get_resistance_summary(boss_profile)
    print(f"  Immunities: {summary['immunities']}")
    print(f"  Vulnerabilities: {summary['vulnerabilities']}")
    for resistance_type, value in summary["resistances"].items():
        print(f"  {resistance_type}: {value}%")
    
    # Test damage calculations
    base_damage = 100.0
    
    print(f"\n⚔️ DAMAGE CALCULATIONS:")
    print(f"Base Damage: {base_damage}")
    
    # Fire damage vs goblin (25% resistance)
    fire_damage = resistance_system.calculate_damage_with_resistance(
        base_damage, ResistanceType.FIRE, monster_profile
    )
    print(f"Fire vs Goblin: {fire_damage:.1f} (25% resistance)")
    
    # Physical damage vs goblin (-10% resistance = takes more damage)
    phys_damage = resistance_system.calculate_damage_with_resistance(
        base_damage, ResistanceType.PHYSICAL, monster_profile
    )
    print(f"Physical vs Goblin: {phys_damage:.1f} (-10% resistance)")
    
    # Ice damage vs dragon (-25% resistance = takes more damage)
    ice_damage = resistance_system.calculate_damage_with_resistance(
        base_damage, ResistanceType.ICE, boss_profile
    )
    print(f"Ice vs Dragon: {ice_damage:.1f} (-25% resistance)")
    
    # Test status effect application
    print(f"\n🎯 STATUS EFFECT TESTS:")
    
    # Can stun goblin?
    can_stun_goblin = resistance_system.can_apply_status_effect(
        ResistanceType.STUN, monster_profile
    )
    print(f"Can stun Goblin: {can_stun_goblin}")
    
    # Can stun dragon?
    can_stun_dragon = resistance_system.can_apply_status_effect(
        ResistanceType.STUN, boss_profile
    )
    print(f"Can stun Dragon: {can_stun_dragon}")
    
    # Can slow dragon?
    can_slow_dragon = resistance_system.can_apply_status_effect(
        ResistanceType.SLOW, boss_profile
    )
    print(f"Can slow Dragon: {can_slow_dragon}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Boss Encounter Designer for Chronicles of Ruin - Phase 2
Enhanced boss creation with mechanics, AI testing, and balance validation
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from chapters.chapter_01_sunderfall.src.systems.resistance_system import ResistanceSystem, ResistanceType, EntityType

class BossPhase(Enum):
    """Boss encounter phases"""
    PHASE_1 = "phase_1"    # 100-75% HP
    PHASE_2 = "phase_2"    # 75-50% HP  
    PHASE_3 = "phase_3"    # 50-25% HP
    PHASE_4 = "phase_4"    # 25-0% HP

class MechanicType(Enum):
    """Types of boss mechanics"""
    DAMAGE_OVER_TIME = "damage_over_time"
    AREA_DENIAL = "area_denial"
    BUFF_DISPEL = "buff_dispel"
    HEALING_REDUCTION = "healing_reduction"
    DAMAGE_REFLECTION = "damage_reflection"
    SUMMON_ADDS = "summon_adds"
    ENRAGE = "enrage"
    SHIELD = "shield"
    TELEPORT = "teleport"
    STATUS_IMMUNITY = "status_immunity"

class BossEncounterDesigner:
    """Enhanced boss encounter design tool with AI testing"""
    
    def __init__(self):
        self.resistance_system = ResistanceSystem()
        self.bosses_file = Path("chapters/chapter_01_sunderfall/data/enhanced_bosses.json")
        self.boss_encounters = self._load_boss_encounters()
        
    def _load_boss_encounters(self) -> Dict:
        """Load boss encounters from file"""
        if self.bosses_file.exists():
            try:
                with open(self.bosses_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading bosses: {e}")
        return {}
    
    def _save_boss_encounters(self):
        """Save boss encounters to file"""
        self.bosses_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.bosses_file, 'w') as f:
            json.dump(self.boss_encounters, f, indent=2)
    
    def create_boss_interactive(self, designer_id: str) -> Optional[str]:
        """Interactive boss creation"""
        print("=== Enhanced Boss Encounter Designer ===\n")
        
        # Basic boss information
        name = input("Boss name: ").strip()
        if not name:
            print("Name required!")
            return None
            
        description = input("Boss description: ").strip()
        if not description:
            print("Description required!")
            return None
        
        # Boss tier/difficulty
        print("\nBoss tiers:")
        tiers = ["Elite", "Champion", "Boss", "Raid Boss", "World Boss"]
        for i, tier in enumerate(tiers, 1):
            print(f"  {i}. {tier}")
        
        try:
            tier_choice = int(input("Choose tier (1-5): ")) - 1
            boss_tier = tiers[tier_choice]
        except (ValueError, IndexError):
            print("Invalid choice!")
            return None
        
        # Base stats based on tier
        base_stats = self._get_tier_stats(boss_tier)
        print(f"\nBase stats for {boss_tier}:")
        print(f"  Health: {base_stats['health']}")
        print(f"  Damage: {base_stats['damage']}")
        print(f"  Defense: {base_stats['defense']}")
        
        # Level range
        try:
            min_level = int(input("Minimum recommended level: "))
            max_level = int(input("Maximum recommended level: "))
            if min_level > max_level:
                min_level, max_level = max_level, min_level
        except ValueError:
            print("Invalid level range!")
            return None
        
        # Resistances and immunities
        print("\nConfigure resistances (bosses are immune to stun/freeze by default):")
        resistances = {}
        immunities = [ResistanceType.STUN, ResistanceType.FREEZE]  # Default boss immunities
        
        # Physical resistance
        try:
            phys_res = float(input("Physical resistance % (0-99, default 30): ") or "30")
            resistances[ResistanceType.PHYSICAL] = min(99, max(0, phys_res))
        except ValueError:
            resistances[ResistanceType.PHYSICAL] = 30.0
        
        # Elemental resistances
        elements = [ResistanceType.FIRE, ResistanceType.ICE, ResistanceType.LIGHTNING, ResistanceType.POISON]
        for element in elements:
            try:
                res = float(input(f"{element.value.title()} resistance % (-99 to 99, default 0): ") or "0")
                resistances[element] = min(99, max(-99, res))
            except ValueError:
                resistances[element] = 0.0
        
        # Additional immunities
        print("\nAdditional immunities (beyond stun/freeze):")
        print("1. Poison  2. Bleed  3. Slow  4. None")
        try:
            immune_choice = input("Choose additional immunity (1-4, default 4): ") or "4"
            if immune_choice == "1":
                immunities.append(ResistanceType.POISON)
            elif immune_choice == "2":
                immunities.append(ResistanceType.BLEED)
            elif immune_choice == "3":
                immunities.append(ResistanceType.SLOW)
        except:
            pass
        
        # Boss mechanics by phase
        print("\nDesign boss mechanics by phase:")
        phases = {}
        
        for phase in [BossPhase.PHASE_1, BossPhase.PHASE_2, BossPhase.PHASE_3, BossPhase.PHASE_4]:
            hp_ranges = {
                BossPhase.PHASE_1: "100-75%",
                BossPhase.PHASE_2: "75-50%", 
                BossPhase.PHASE_3: "50-25%",
                BossPhase.PHASE_4: "25-0%"
            }
            
            print(f"\n{phase.value.upper()} ({hp_ranges[phase]} HP):")
            
            # Choose mechanics for this phase
            print("Available mechanics:")
            mechanics = list(MechanicType)
            for i, mech in enumerate(mechanics, 1):
                print(f"  {i}. {mech.value}")
            
            phase_mechanics = []
            while len(phase_mechanics) < 3:  # Max 3 mechanics per phase
                try:
                    choice = input(f"Add mechanic {len(phase_mechanics)+1} (1-{len(mechanics)}, 0 to finish): ")
                    if choice == "0":
                        break
                    
                    mech_idx = int(choice) - 1
                    if 0 <= mech_idx < len(mechanics):
                        mechanic = mechanics[mech_idx]
                        if mechanic not in phase_mechanics:
                            # Create mechanic with values
                            mechanic_data = self._create_mechanic(mechanic, boss_tier)
                            phase_mechanics.append(mechanic_data)
                            print(f"Added: {mechanic_data['name']}")
                        else:
                            print("Mechanic already added!")
                    else:
                        print("Invalid choice!")
                except ValueError:
                    print("Invalid input!")
            
            phases[phase.value] = {
                'hp_range': hp_ranges[phase],
                'mechanics': phase_mechanics
            }
        
        # Create resistance profile
        resistance_profile = self.resistance_system.create_resistance_profile(
            EntityType.BOSS,
            custom_resistances=resistances,
            immunities=immunities,
            vulnerabilities=[]
        )
        
        # Create boss encounter
        boss_id = f"boss_{designer_id}_{int(time.time())}"
        
        boss_encounter = {
            'id': boss_id,
            'name': name,
            'description': description,
            'designer_id': designer_id,
            'creation_time': time.time(),
            'tier': boss_tier,
            'level_range': [min_level, max_level],
            'base_stats': base_stats,
            'resistance_data': {
                'resistances': {rt.value: val for rt, val in resistances.items()},
                'immunities': [rt.value for rt in immunities],
                'vulnerabilities': []
            },
            'phases': phases,
            'ai_test_results': {},
            'balance_rating': None,
            'difficulty_rating': self._calculate_difficulty(boss_tier, phases)
        }
        
        self.boss_encounters[boss_id] = boss_encounter
        self._save_boss_encounters()
        
        print(f"\n✅ Boss encounter '{name}' created!")
        print(f"Boss ID: {boss_id}")
        print(f"Tier: {boss_tier}")
        print(f"Level Range: {min_level}-{max_level}")
        print(f"Difficulty: {boss_encounter['difficulty_rating']:.1f}/10")
        print(f"Total Phases: {len([p for p in phases.values() if p['mechanics']])}")
        
        return boss_id
    
    def _get_tier_stats(self, tier: str) -> Dict[str, int]:
        """Get base stats for boss tier"""
        tier_stats = {
            "Elite": {"health": 500, "damage": 25, "defense": 15},
            "Champion": {"health": 1000, "damage": 40, "defense": 25},
            "Boss": {"health": 2500, "damage": 60, "defense": 40},
            "Raid Boss": {"health": 5000, "damage": 80, "defense": 60},
            "World Boss": {"health": 10000, "damage": 100, "defense": 80}
        }
        return tier_stats.get(tier, tier_stats["Elite"])
    
    def _create_mechanic(self, mechanic_type: MechanicType, boss_tier: str) -> Dict:
        """Create a specific mechanic with appropriate values"""
        tier_multipliers = {
            "Elite": 1.0,
            "Champion": 1.2,
            "Boss": 1.5,
            "Raid Boss": 2.0,
            "World Boss": 2.5
        }
        
        multiplier = tier_multipliers.get(boss_tier, 1.0)
        
        mechanic_templates = {
            MechanicType.DAMAGE_OVER_TIME: {
                'name': 'Corruption Aura',
                'description': 'Deals damage over time to all players',
                'damage_per_second': int(10 * multiplier),
                'duration': 8,
                'activation': 'continuous'
            },
            MechanicType.AREA_DENIAL: {
                'name': 'Flame Zones',
                'description': 'Creates dangerous areas that deal damage',
                'zone_damage': int(25 * multiplier),
                'zone_count': min(4, int(2 * multiplier)),
                'duration': 15
            },
            MechanicType.SUMMON_ADDS: {
                'name': 'Call Minions',
                'description': 'Summons additional enemies',
                'add_count': min(6, int(3 * multiplier)),
                'add_health': int(100 * multiplier),
                'cooldown': 30
            },
            MechanicType.ENRAGE: {
                'name': 'Berserker Rage',
                'description': 'Increases damage as health decreases',
                'damage_increase': int(20 * multiplier),
                'trigger_hp': 25,
                'duration': 'permanent'
            },
            MechanicType.SHIELD: {
                'name': 'Barrier',
                'description': 'Absorbs damage until broken',
                'shield_strength': int(300 * multiplier),
                'cooldown': 45,
                'duration': 20
            },
            MechanicType.HEALING_REDUCTION: {
                'name': 'Wound Curse',
                'description': 'Reduces healing effectiveness',
                'healing_reduction': min(80, int(50 * multiplier)),
                'duration': 12,
                'cooldown': 25
            },
            MechanicType.DAMAGE_REFLECTION: {
                'name': 'Thorns',
                'description': 'Reflects damage back to attackers',
                'reflection_percent': min(50, int(25 * multiplier)),
                'duration': 10,
                'cooldown': 35
            },
            MechanicType.TELEPORT: {
                'name': 'Phase Shift',
                'description': 'Teleports around the battlefield',
                'teleport_frequency': max(5, int(10 / multiplier)),
                'duration': 3,
                'phase_trigger': 'low_health'
            },
            MechanicType.BUFF_DISPEL: {
                'name': 'Nullify',
                'description': 'Removes player buffs',
                'dispel_count': min(5, int(3 * multiplier)),
                'cooldown': 20,
                'range': 'all_players'
            },
            MechanicType.STATUS_IMMUNITY: {
                'name': 'Cleanse',
                'description': 'Removes debuffs and gains temporary immunity',
                'immunity_duration': min(15, int(8 * multiplier)),
                'cooldown': 40,
                'trigger': 'debuff_count'
            }
        }
        
        return mechanic_templates.get(mechanic_type, {
            'name': 'Unknown Mechanic',
            'description': 'Unknown mechanic type',
            'effect': 'none'
        })
    
    def _calculate_difficulty(self, tier: str, phases: Dict) -> float:
        """Calculate boss difficulty rating (1-10)"""
        base_difficulty = {
            "Elite": 2.0,
            "Champion": 4.0,
            "Boss": 6.0,
            "Raid Boss": 8.0,
            "World Boss": 9.0
        }.get(tier, 2.0)
        
        # Add difficulty for mechanics
        total_mechanics = sum(len(phase_data['mechanics']) for phase_data in phases.values())
        mechanic_difficulty = min(2.0, total_mechanics * 0.3)
        
        return min(10.0, base_difficulty + mechanic_difficulty)
    
    def test_boss_with_ai(self, boss_id: str) -> Dict[str, Any]:
        """Test boss encounter using AI players"""
        if boss_id not in self.boss_encounters:
            return {'error': 'Boss not found'}
        
        boss = self.boss_encounters[boss_id]
        print(f"\n=== AI Testing Boss: {boss['name']} ===")
        
        # Simulate AI testing
        import random
        
        test_sessions = []
        for party_size in [1, 3, 5]:  # Solo, small group, full party
            for player_skill in ['noob', 'expert']:
                # Simulate encounter
                difficulty = boss['difficulty_rating']
                party_bonus = (party_size - 1) * 0.3  # Group makes it easier
                skill_bonus = 2.0 if player_skill == 'expert' else -1.0
                
                success_chance = max(0.1, min(0.9, (5.0 + party_bonus + skill_bonus - difficulty) / 8.0))
                victory = random.random() < success_chance
                
                # Calculate performance metrics
                attempt_time = random.uniform(60, 300)  # 1-5 minutes
                damage_dealt = random.randint(1000, 5000) * party_size
                damage_taken = random.randint(500, 2000) * party_size
                
                session = {
                    'party_size': party_size,
                    'player_skill': player_skill,
                    'victory': victory,
                    'attempt_time': round(attempt_time, 1),
                    'damage_dealt': damage_dealt,
                    'damage_taken': damage_taken,
                    'success_chance': round(success_chance * 100, 1)
                }
                test_sessions.append(session)
        
        # Analyze results
        victories = sum(1 for s in test_sessions if s['victory'])
        avg_time = sum(s['attempt_time'] for s in test_sessions) / len(test_sessions)
        
        balance_rating = self._assess_boss_balance(test_sessions, boss)
        
        test_results = {
            'test_time': time.time(),
            'sessions': test_sessions,
            'victory_rate': victories / len(test_sessions),
            'average_time': avg_time,
            'balance_rating': balance_rating,
            'recommendations': self._generate_boss_recommendations(test_sessions, boss)
        }
        
        # Save results
        self.boss_encounters[boss_id]['ai_test_results'] = test_results
        self.boss_encounters[boss_id]['balance_rating'] = balance_rating
        self._save_boss_encounters()
        
        print(f"Victory Rate: {test_results['victory_rate']:.1%}")
        print(f"Average Time: {avg_time:.1f}s")
        print(f"Balance Rating: {balance_rating:.2f}")
        print("Recommendations:")
        for rec in test_results['recommendations']:
            print(f"  - {rec}")
        
        return test_results
    
    def _assess_boss_balance(self, sessions: List[Dict], boss: Dict) -> float:
        """Assess boss balance (0.0 to 1.0)"""
        victory_rate = sum(1 for s in sessions if s['victory']) / len(sessions)
        
        # Target victory rates by difficulty
        target_rates = {
            "Elite": 0.8,      # 80% victory rate
            "Champion": 0.65,  # 65% victory rate  
            "Boss": 0.5,       # 50% victory rate
            "Raid Boss": 0.3,  # 30% victory rate
            "World Boss": 0.15 # 15% victory rate
        }
        
        target = target_rates.get(boss['tier'], 0.5)
        difference = abs(victory_rate - target)
        
        # Perfect balance = 1.0, completely off = 0.0
        return max(0.0, 1.0 - (difference / target))
    
    def _generate_boss_recommendations(self, sessions: List[Dict], boss: Dict) -> List[str]:
        """Generate recommendations for boss balance"""
        recommendations = []
        victory_rate = sum(1 for s in sessions if s['victory']) / len(sessions)
        
        if victory_rate > 0.8:
            recommendations.append("Boss may be too easy - consider increasing health or damage")
        elif victory_rate < 0.2:
            recommendations.append("Boss may be too difficult - consider reducing health or damage")
        
        # Check party size impact
        solo_victories = sum(1 for s in sessions if s['party_size'] == 1 and s['victory'])
        party_victories = sum(1 for s in sessions if s['party_size'] > 1 and s['victory'])
        
        if solo_victories == 0:
            recommendations.append("Boss requires group play - ensure this is intended")
        elif party_victories / max(1, solo_victories) < 1.5:
            recommendations.append("Consider adding mechanics that reward group coordination")
        
        # Check skill impact
        noob_victories = sum(1 for s in sessions if s['player_skill'] == 'noob' and s['victory'])
        expert_victories = sum(1 for s in sessions if s['player_skill'] == 'expert' and s['victory'])
        
        if expert_victories == noob_victories:
            recommendations.append("Boss doesn't sufficiently reward player skill")
        
        return recommendations
    
    def list_bosses(self, designer_id: Optional[str] = None) -> List[Dict]:
        """List all boss encounters"""
        bosses_list = []
        
        for boss_id, boss in self.boss_encounters.items():
            if designer_id and boss['designer_id'] != designer_id:
                continue
            
            boss_info = {
                'id': boss['id'],
                'name': boss['name'],
                'designer_id': boss['designer_id'],
                'tier': boss['tier'],
                'level_range': boss['level_range'],
                'difficulty': boss['difficulty_rating'],
                'balance_rating': boss.get('balance_rating'),
                'tested': bool(boss.get('ai_test_results'))
            }
            bosses_list.append(boss_info)
        
        return sorted(bosses_list, key=lambda x: x['difficulty'], reverse=True)
    
    def get_boss_details(self, boss_id: str) -> Optional[Dict]:
        """Get detailed boss information"""
        return self.boss_encounters.get(boss_id)
    
    def delete_boss(self, boss_id: str, designer_id: str) -> bool:
        """Delete a boss encounter (designer only)"""
        if boss_id not in self.boss_encounters:
            return False
        
        if self.boss_encounters[boss_id]['designer_id'] != designer_id:
            return False
        
        del self.boss_encounters[boss_id]
        self._save_boss_encounters()
        return True

def main():
    """Main CLI interface"""
    designer = BossEncounterDesigner()
    
    while True:
        print("\n=== Boss Encounter Designer ===")
        print("1. Create new boss")
        print("2. List bosses")
        print("3. View boss details")
        print("4. Test boss with AI")
        print("5. Delete boss")
        print("0. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            designer_id = input("Designer ID: ").strip()
            if designer_id:
                designer.create_boss_interactive(designer_id)
        
        elif choice == "2":
            bosses = designer.list_bosses()
            if bosses:
                print(f"\n{'ID':<25} {'Name':<20} {'Tier':<10} {'Levels':<8} {'Diff':<5} {'Tested'}")
                print("-" * 75)
                for b in bosses:
                    levels = f"{b['level_range'][0]}-{b['level_range'][1]}"
                    tested = "Yes" if b['tested'] else "No"
                    print(f"{b['id']:<25} {b['name']:<20} {b['tier']:<10} {levels:<8} {b['difficulty']:<5.1f} {tested}")
            else:
                print("No bosses found.")
        
        elif choice == "3":
            boss_id = input("Boss ID: ").strip()
            details = designer.get_boss_details(boss_id)
            if details:
                print(f"\n=== {details['name']} ===")
                print(f"Tier: {details['tier']}")
                print(f"Level Range: {details['level_range'][0]}-{details['level_range'][1]}")
                print(f"Difficulty: {details['difficulty_rating']:.1f}/10")
                
                if details.get('balance_rating'):
                    print(f"Balance: {details['balance_rating']:.2f}")
                
                print("\nPhases:")
                for phase_name, phase_data in details['phases'].items():
                    if phase_data['mechanics']:
                        print(f"  {phase_name.upper()} ({phase_data['hp_range']}):")
                        for mechanic in phase_data['mechanics']:
                            print(f"    - {mechanic['name']}: {mechanic['description']}")
                
                if details.get('ai_test_results'):
                    results = details['ai_test_results']
                    print(f"\nAI Test Results:")
                    print(f"  Victory Rate: {results['victory_rate']:.1%}")
                    print(f"  Average Time: {results['average_time']:.1f}s")
            else:
                print("Boss not found.")
        
        elif choice == "4":
            boss_id = input("Boss ID to test: ").strip()
            if boss_id in designer.boss_encounters:
                designer.test_boss_with_ai(boss_id)
            else:
                print("Boss not found.")
        
        elif choice == "5":
            boss_id = input("Boss ID to delete: ").strip()
            designer_id = input("Designer ID: ").strip()
            if designer.delete_boss(boss_id, designer_id):
                print("Boss deleted.")
            else:
                print("Delete failed (not found or not designer).")
        
        elif choice == "0":
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()

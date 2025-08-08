#!/usr/bin/env python3
"""
Set Item Manager for Chronicles of Ruin - Phase 2
Enhanced custom set creation with AI testing and balance validation
"""

import sys
import json
import time
import random
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from chapters.chapter_01_sunderfall.src.systems.items_system import ItemsSystem, ItemType, ItemQuality, EquipmentSlot

class SetManager:
    """Enhanced set item manager with AI testing capabilities"""
    
    def __init__(self):
        self.items_system = ItemsSystem()
        self.sets_file = Path("chapters/chapter_01_sunderfall/data/enhanced_sets.json")
        self.enhanced_sets = self._load_enhanced_sets()
        
    def _load_enhanced_sets(self) -> Dict:
        """Load enhanced sets from file"""
        if self.sets_file.exists():
            try:
                with open(self.sets_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading sets: {e}")
        return {}
    
    def _save_enhanced_sets(self):
        """Save enhanced sets to file"""
        self.sets_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.sets_file, 'w') as f:
            json.dump(self.enhanced_sets, f, indent=2)
    
    def create_set_interactive(self, creator_id: str) -> Optional[str]:
        """Interactive set creation with enhanced features"""
        print("=== Enhanced Set Creation Tool ===\n")
        
        # Basic information
        name = input("Set name: ").strip()
        if not name:
            print("Name required!")
            return None
            
        description = input("Set description: ").strip()
        if not description:
            print("Description required!")
            return None
        
        # Choose set type
        print("\nSet types:")
        set_types = ["Combat", "Defense", "Magic", "Utility", "Hybrid"]
        for i, stype in enumerate(set_types, 1):
            print(f"  {i}. {stype}")
        
        try:
            type_choice = int(input("Choose type (1-5): ")) - 1
            set_type = set_types[type_choice]
        except (ValueError, IndexError):
            print("Invalid choice!")
            return None
        
        # Select pieces (2-6 pieces for balance)
        print(f"\nSelect 2-6 equipment pieces:")
        slots = [
            ("Main Hand", "weapon_main"),
            ("Off Hand", "weapon_off"), 
            ("Head", "armor_head"),
            ("Chest", "armor_chest"),
            ("Legs", "armor_legs"),
            ("Feet", "armor_feet"),
            ("Ring 1", "accessory_1"),
            ("Ring 2", "accessory_2")
        ]
        
        for i, (name, slot) in enumerate(slots, 1):
            print(f"  {i}. {name}")
        
        selected_slots = []
        while len(selected_slots) < 6:
            try:
                choice = input(f"Select slot {len(selected_slots)+1} (1-8, 0 to finish): ")
                if choice == "0":
                    break
                    
                slot_idx = int(choice) - 1
                if 0 <= slot_idx < len(slots):
                    slot_name, slot_id = slots[slot_idx]
                    if slot_id not in selected_slots:
                        selected_slots.append(slot_id)
                        print(f"Added: {slot_name}")
                    else:
                        print("Already selected!")
                else:
                    print("Invalid slot!")
                    
            except ValueError:
                print("Invalid input!")
        
        if len(selected_slots) < 2:
            print("Need at least 2 pieces!")
            return None
        
        # Create set bonuses based on type and pieces
        bonuses = self._generate_bonuses(set_type, len(selected_slots))
        
        # Create the set
        set_id = f"enhanced_{creator_id}_{int(time.time())}"
        
        enhanced_set = {
            'id': set_id,
            'name': name,
            'description': description,
            'creator_id': creator_id,
            'creation_time': time.time(),
            'set_type': set_type,
            'slots': selected_slots,
            'bonuses': bonuses,
            'usage_count': 0,
            'balance_rating': None,
            'ai_test_results': {},
            'reroll_count': 0,
            'gambling_tax_per_piece': {slot: 0.0 for slot in selected_slots},
            'base_reroll_cost': self._calculate_base_reroll_cost(len(selected_slots))
        }
        
        self.enhanced_sets[set_id] = enhanced_set
        self._save_enhanced_sets()
        
        print(f"\n✅ Enhanced set '{name}' created!")
        print(f"Set ID: {set_id}")
        print(f"Type: {set_type}")
        print(f"Pieces: {len(selected_slots)}")
        print("Bonuses:")
        for bonus in bonuses:
            print(f"  {bonus['pieces']}pc: {bonus['name']} - {bonus['effect']}")
        
        return set_id
    
    def _generate_bonuses(self, set_type: str, piece_count: int) -> List[Dict]:
        """Generate balanced bonuses based on set type and piece count"""
        bonus_templates = {
            "Combat": [
                {"pieces": 2, "name": "Combat Prowess", "effect": "+10% damage", "values": {"damage": 0.10}},
                {"pieces": 4, "name": "Battle Fury", "effect": "+15% crit chance", "values": {"crit_chance": 0.15}},
                {"pieces": 6, "name": "Warrior's Might", "effect": "+25% damage, +10% crit", "values": {"damage": 0.25, "crit_chance": 0.10}}
            ],
            "Defense": [
                {"pieces": 2, "name": "Guardian's Will", "effect": "+15% health", "values": {"health": 0.15}},
                {"pieces": 4, "name": "Stalwart Defense", "effect": "+20% damage reduction", "values": {"damage_reduction": 0.20}},
                {"pieces": 6, "name": "Fortress", "effect": "+30% health, +15% reduction", "values": {"health": 0.30, "damage_reduction": 0.15}}
            ],
            "Magic": [
                {"pieces": 2, "name": "Arcane Focus", "effect": "+15% mana", "values": {"mana": 0.15}},
                {"pieces": 4, "name": "Spell Mastery", "effect": "+20% spell damage", "values": {"spell_damage": 0.20}},
                {"pieces": 6, "name": "Archmage", "effect": "+25% spell damage, +30% mana", "values": {"spell_damage": 0.25, "mana": 0.30}}
            ],
            "Utility": [
                {"pieces": 2, "name": "Explorer", "effect": "+10% movement speed", "values": {"movement_speed": 0.10}},
                {"pieces": 4, "name": "Efficient", "effect": "+15% experience gain", "values": {"experience": 0.15}},
                {"pieces": 6, "name": "Master Explorer", "effect": "+20% speed, +25% exp", "values": {"movement_speed": 0.20, "experience": 0.25}}
            ],
            "Hybrid": [
                {"pieces": 2, "name": "Balanced", "effect": "+8% damage, +8% health", "values": {"damage": 0.08, "health": 0.08}},
                {"pieces": 4, "name": "Versatile", "effect": "+12% all stats", "values": {"all_stats": 0.12}},
                {"pieces": 6, "name": "Master of All", "effect": "+15% all stats, +10% efficiency", "values": {"all_stats": 0.15, "efficiency": 0.10}}
            ]
        }
        
        template_bonuses = bonus_templates.get(set_type, bonus_templates["Hybrid"])
        return [bonus for bonus in template_bonuses if bonus["pieces"] <= piece_count]
    
    def test_set_with_ai(self, set_id: str) -> Dict[str, Any]:
        """Test a set using AI players"""
        if set_id not in self.enhanced_sets:
            return {'error': 'Set not found'}
        
        enhanced_set = self.enhanced_sets[set_id]
        print(f"\n=== AI Testing: {enhanced_set['name']} ===")
        
        # Simulate AI testing (in real implementation, would use actual AI system)
        import random
        
        # Mock test results
        test_sessions = []
        for player_type in ['noob', 'expert', 'balanced']:
            # Simulate performance based on set bonuses
            base_performance = 45 if player_type == 'noob' else (65 if player_type == 'expert' else 55)
            
            # Calculate bonus impact
            bonus_impact = 0
            for bonus in enhanced_set['bonuses']:
                for value in bonus['values'].values():
                    bonus_impact += value * 20  # Convert to performance points
            
            performance = base_performance + bonus_impact + random.uniform(-5, 5)
            
            session = {
                'player_type': player_type,
                'performance_score': round(performance, 1),
                'experience_gained': int(100 + bonus_impact * 10),
                'quests_completed': random.randint(2, 5),
                'feedback': self._generate_ai_feedback(enhanced_set, performance)
            }
            test_sessions.append(session)
        
        # Calculate overall results
        avg_performance = sum(s['performance_score'] for s in test_sessions) / len(test_sessions)
        balance_rating = self._calculate_balance_rating(avg_performance, enhanced_set)
        
        test_results = {
            'test_time': time.time(),
            'sessions': test_sessions,
            'average_performance': avg_performance,
            'balance_rating': balance_rating,
            'recommendations': self._generate_recommendations(avg_performance, enhanced_set)
        }
        
        # Save results
        self.enhanced_sets[set_id]['ai_test_results'] = test_results
        self.enhanced_sets[set_id]['balance_rating'] = balance_rating
        self._save_enhanced_sets()
        
        print(f"Average Performance: {avg_performance:.1f}")
        print(f"Balance Rating: {balance_rating:.2f}")
        print("Recommendations:")
        for rec in test_results['recommendations']:
            print(f"  - {rec}")
        
        return test_results
    
    def _generate_ai_feedback(self, enhanced_set: Dict, performance: float) -> str:
        """Generate AI feedback based on performance"""
        if performance > 70:
            return "Set feels very powerful, good synergy between bonuses"
        elif performance > 50:
            return "Set provides noticeable benefits, well-balanced"
        else:
            return "Set bonuses feel underwhelming, could use improvement"
    
    def _calculate_balance_rating(self, avg_performance: float, enhanced_set: Dict) -> float:
        """Calculate balance rating (0.0 to 1.0)"""
        # Ideal performance range is 45-65
        if 45 <= avg_performance <= 65:
            return 1.0  # Perfect balance
        elif avg_performance > 65:
            # Overpowered
            excess = avg_performance - 65
            return max(0.3, 1.0 - (excess / 20))
        else:
            # Underpowered
            deficit = 45 - avg_performance
            return max(0.5, 1.0 - (deficit / 30))
    
    def _generate_recommendations(self, avg_performance: float, enhanced_set: Dict) -> List[str]:
        """Generate balance recommendations"""
        recommendations = []
        
        if avg_performance > 70:
            recommendations.append("Set may be overpowered - consider reducing bonus values")
        elif avg_performance > 65:
            recommendations.append("Set is strong but balanced for high-end content")
        elif avg_performance < 40:
            recommendations.append("Set needs stronger bonuses to be viable")
        elif avg_performance < 45:
            recommendations.append("Consider small increases to bonus values")
        else:
            recommendations.append("Set appears well-balanced for its tier")
        
        # Type-specific recommendations
        if enhanced_set['set_type'] == 'Combat' and avg_performance < 50:
            recommendations.append("Combat sets should provide strong offensive bonuses")
        elif enhanced_set['set_type'] == 'Defense' and avg_performance > 60:
            recommendations.append("Defense sets should focus on survivability over damage")
        
        return recommendations
    
    def list_sets(self, creator_id: Optional[str] = None) -> List[Dict]:
        """List all enhanced sets"""
        sets_list = []
        
        for set_id, enhanced_set in self.enhanced_sets.items():
            if creator_id and enhanced_set['creator_id'] != creator_id:
                continue
            
            set_info = {
                'id': enhanced_set['id'],
                'name': enhanced_set['name'],
                'creator_id': enhanced_set['creator_id'],
                'set_type': enhanced_set['set_type'],
                'pieces': len(enhanced_set['slots']),
                'usage_count': enhanced_set['usage_count'],
                'balance_rating': enhanced_set.get('balance_rating'),
                'tested': bool(enhanced_set.get('ai_test_results'))
            }
            sets_list.append(set_info)
        
        return sorted(sets_list, key=lambda x: x['usage_count'], reverse=True)
    
    def get_set_details(self, set_id: str) -> Optional[Dict]:
        """Get detailed set information"""
        return self.enhanced_sets.get(set_id)
    
    def delete_set(self, set_id: str, creator_id: str) -> bool:
        """Delete a set (creator only)"""
        if set_id not in self.enhanced_sets:
            return False
        
        if self.enhanced_sets[set_id]['creator_id'] != creator_id:
            return False
        
        del self.enhanced_sets[set_id]
        self._save_enhanced_sets()
        return True
    
    def _calculate_base_reroll_cost(self, piece_count: int) -> int:
        """Calculate base cost for rerolling a set"""
        # Base cost scales with number of pieces
        return 100 * piece_count
    
    def calculate_reroll_cost(self, set_id: str) -> int:
        """Calculate current reroll cost including gambling tax"""
        if set_id not in self.enhanced_sets:
            return 0
        
        set_data = self.enhanced_sets[set_id]
        base_cost = set_data['base_reroll_cost']
        reroll_count = set_data['reroll_count']
        
        # Exponential base cost increase
        escalation_cost = base_cost * (2 ** reroll_count)
        
        # Calculate total gambling tax from all pieces
        total_tax = sum(set_data['gambling_tax_per_piece'].values())
        tax_multiplier = 1 + total_tax
        
        return int(escalation_cost * tax_multiplier)
    
    def reroll_set_bonuses(self, set_id: str, player_gold: int) -> Dict:
        """Reroll set bonuses with gambling tax system"""
        if set_id not in self.enhanced_sets:
            return {"success": False, "error": "Set not found"}
        
        set_data = self.enhanced_sets[set_id]
        reroll_cost = self.calculate_reroll_cost(set_id)
        
        if player_gold < reroll_cost:
            return {
                "success": False, 
                "error": f"Not enough gold! Need {reroll_cost}, have {player_gold}"
            }
        
        # Apply gambling tax to each piece (0.001% to 0.01% per piece)
        for slot in set_data['slots']:
            tax_increase = random.uniform(0.00001, 0.0001)  # 0.001% to 0.01% as decimal
            set_data['gambling_tax_per_piece'][slot] += tax_increase
        
        # Increment reroll count
        set_data['reroll_count'] += 1
        
        # Generate new bonuses
        new_bonuses = self._generate_bonuses(set_data['set_type'], len(set_data['slots']))
        set_data['bonuses'] = new_bonuses
        
        # Save changes
        self._save_enhanced_sets()
        
        return {
            "success": True,
            "cost_paid": reroll_cost,
            "new_bonuses": new_bonuses,
            "reroll_count": set_data['reroll_count'],
            "next_reroll_cost": self.calculate_reroll_cost(set_id),
            "gambling_taxes": {slot: f"{tax*100:.4f}%" for slot, tax in set_data['gambling_tax_per_piece'].items()}
        }

def main():
    """Main CLI interface"""
    manager = SetManager()
    
    while True:
        print("\n=== Enhanced Set Item Manager ===")
        print("1. Create new set")
        print("2. List sets")
        print("3. View set details")
        print("4. Test set with AI")
        print("5. Reroll set bonuses (GAMBLING)")
        print("6. Delete set")
        print("0. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            creator_id = input("Creator ID: ").strip()
            if creator_id:
                manager.create_set_interactive(creator_id)
        
        elif choice == "2":
            sets = manager.list_sets()
            if sets:
                print(f"\n{'ID':<25} {'Name':<20} {'Type':<10} {'Pieces':<7} {'Rating':<7} {'Tested'}")
                print("-" * 80)
                for s in sets:
                    rating = f"{s['balance_rating']:.2f}" if s['balance_rating'] else "N/A"
                    tested = "Yes" if s['tested'] else "No"
                    print(f"{s['id']:<25} {s['name']:<20} {s['set_type']:<10} {s['pieces']:<7} {rating:<7} {tested}")
            else:
                print("No sets found.")
        
        elif choice == "3":
            set_id = input("Set ID: ").strip()
            details = manager.get_set_details(set_id)
            if details:
                print(f"\n=== {details['name']} ===")
                print(f"Type: {details['set_type']}")
                print(f"Creator: {details['creator_id']}")
                print(f"Pieces: {len(details['slots'])}")
                print(f"Usage: {details['usage_count']}")
                if details.get('balance_rating'):
                    print(f"Balance: {details['balance_rating']:.2f}")
                
                print("\nBonuses:")
                for bonus in details['bonuses']:
                    print(f"  {bonus['pieces']}pc: {bonus['name']} - {bonus['effect']}")
                
                if details.get('ai_test_results'):
                    results = details['ai_test_results']
                    print(f"\nAI Test Results:")
                    print(f"  Average Performance: {results['average_performance']:.1f}")
                    print("  Recommendations:")
                    for rec in results['recommendations']:
                        print(f"    - {rec}")
            else:
                print("Set not found.")
        
        elif choice == "4":
            set_id = input("Set ID to test: ").strip()
            if set_id in manager.enhanced_sets:
                manager.test_set_with_ai(set_id)
            else:
                print("Set not found.")
        
        elif choice == "5":
            set_id = input("Set ID to reroll: ").strip()
            if set_id not in manager.enhanced_sets:
                print("Set not found.")
                continue
            
            # Show current cost and gambling taxes
            current_cost = manager.calculate_reroll_cost(set_id)
            set_data = manager.enhanced_sets[set_id]
            
            print(f"\n=== GAMBLING REROLL ===")
            print(f"Set: {set_data['name']}")
            print(f"Reroll Count: {set_data['reroll_count']}")
            print(f"Current Cost: {current_cost} gold")
            
            if set_data['reroll_count'] > 0:
                print("\nGambling Taxes per piece:")
                for slot, tax in set_data['gambling_tax_per_piece'].items():
                    print(f"  {slot}: +{tax*100:.4f}% cost")
            
            print(f"\n⚠️  WARNING: Each reroll adds 0.001%-0.01% permanent tax per piece!")
            player_gold = int(input(f"Your gold amount: ") or "0")
            
            if player_gold < current_cost:
                print(f"❌ Not enough gold! Need {current_cost}, have {player_gold}")
                continue
            
            confirm = input("Confirm reroll? (y/N): ").lower().strip()
            if confirm == 'y':
                result = manager.reroll_set_bonuses(set_id, player_gold)
                if result['success']:
                    print(f"\n✅ Reroll successful!")
                    print(f"💰 Cost: {result['cost_paid']} gold")
                    print(f"🎲 Reroll #{result['reroll_count']}")
                    print(f"💸 Next reroll cost: {result['next_reroll_cost']} gold")
                    
                    print("\n🎁 New bonuses:")
                    for bonus in result['new_bonuses']:
                        print(f"  {bonus['pieces']}pc: {bonus['name']} - {bonus['effect']}")
                    
                    print("\n📊 Updated gambling taxes:")
                    for slot, tax in result['gambling_taxes'].items():
                        print(f"  {slot}: +{tax}")
                else:
                    print(f"❌ {result['error']}")
        
        elif choice == "6":
            set_id = input("Set ID to delete: ").strip()
            creator_id = input("Creator ID: ").strip()
            if manager.delete_set(set_id, creator_id):
                print("Set deleted.")
            else:
                print("Delete failed (not found or not creator).")
        
        elif choice == "0":
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()

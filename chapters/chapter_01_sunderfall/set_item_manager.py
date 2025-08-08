#!/usr/bin/env python3
"""
Set Item Manager for Chronicles of Ruin: Sunderfall
Advanced tool for creating and managing custom set items
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent / "src"))

from systems.items_system import ItemsSystem, ItemType, ItemQuality, EquipmentSlot
from systems.player_system import PlayerSystem, Player

class SetBonusType(Enum):
    """Types of set bonuses available"""
    DAMAGE_BOOST = "damage_boost"
    DEFENSE_BOOST = "defense_boost"
    HEALTH_BOOST = "health_boost"
    MANA_BOOST = "mana_boost"
    CRITICAL_CHANCE = "critical_chance"
    CRITICAL_DAMAGE = "critical_damage"
    STATUS_RESISTANCE = "status_resistance"
    ELEMENTAL_RESISTANCE = "elemental_resistance"
    SKILL_BOOST = "skill_boost"
    EXPERIENCE_BOOST = "experience_boost"
    GOLD_BOOST = "gold_boost"
    CUSTOM_EFFECT = "custom_effect"

@dataclass
class SetItem:
    """Represents a custom set item"""
    id: str
    name: str
    description: str
    creator_id: str
    creation_time: float
    quality: ItemQuality
    set_bonuses: Dict[str, Any]
    set_items: List[str]
    usage_count: int
    is_permanent: bool
    rarity: str
    level_requirement: int
    class_restriction: Optional[str]

class SetItemManager:
    """Advanced set item management system"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / "data"
        
        # Initialize systems
        self.items_system = ItemsSystem()
        self.player_system = PlayerSystem(self.data_dir)
        
        # Set bonus templates
        self.bonus_templates = self._initialize_bonus_templates()
        
        # Set item categories
        self.set_categories = {
            "combat": ["damage_boost", "defense_boost", "critical_chance", "critical_damage"],
            "survival": ["health_boost", "mana_boost", "status_resistance", "elemental_resistance"],
            "utility": ["skill_boost", "experience_boost", "gold_boost"],
            "custom": ["custom_effect"]
        }
    
    def _initialize_bonus_templates(self) -> Dict[str, Dict]:
        """Initialize bonus templates for set creation"""
        return {
            "warrior_set": {
                "name": "Warrior's Valor",
                "description": "A set designed for frontline combat",
                "bonuses": {
                    "damage_boost": 0.25,
                    "defense_boost": 0.20,
                    "health_boost": 0.30,
                    "critical_chance": 0.10
                },
                "items": ["iron_sword", "iron_armor", "warrior_ring"],
                "level_requirement": 5,
                "class_restriction": "Warrior"
            },
            "mage_set": {
                "name": "Mage's Wisdom",
                "description": "A set designed for spellcasting",
                "bonuses": {
                    "mana_boost": 0.40,
                    "skill_boost": 0.25,
                    "elemental_resistance": 0.20,
                    "critical_damage": 0.15
                },
                "items": ["staff_of_wisdom", "mage_robes", "wisdom_amulet"],
                "level_requirement": 5,
                "class_restriction": "Mage"
            },
            "rogue_set": {
                "name": "Rogue's Shadow",
                "description": "A set designed for stealth and precision",
                "bonuses": {
                    "critical_chance": 0.20,
                    "critical_damage": 0.30,
                    "dexterity_boost": 0.25,
                    "status_resistance": 0.15
                },
                "items": ["shadow_blade", "leather_armor", "stealth_ring"],
                "level_requirement": 5,
                "class_restriction": "Rogue"
            },
            "balanced_set": {
                "name": "Adventurer's Kit",
                "description": "A balanced set for all-around performance",
                "bonuses": {
                    "damage_boost": 0.15,
                    "defense_boost": 0.15,
                    "health_boost": 0.20,
                    "experience_boost": 0.10
                },
                "items": ["balanced_sword", "balanced_armor", "lucky_charm"],
                "level_requirement": 1,
                "class_restriction": None
            }
        }
    
    def create_set_from_template(self, creator_id: str, template_name: str, 
                                custom_name: str = None, custom_description: str = None) -> Optional[str]:
        """Create a set using a predefined template"""
        if template_name not in self.bonus_templates:
            return None
        
        template = self.bonus_templates[template_name]
        
        set_name = custom_name or template["name"]
        set_description = custom_description or template["description"]
        
        return self.items_system.create_custom_set(
            creator_id=creator_id,
            set_name=set_name,
            set_description=set_description,
            set_bonuses=template["bonuses"],
            set_items=template["items"]
        )
    
    def create_custom_set(self, creator_id: str, set_name: str, set_description: str,
                         set_bonuses: Dict[str, Any], set_items: List[str],
                         level_requirement: int = 1, class_restriction: str = None,
                         rarity: str = "rare") -> str:
        """Create a fully custom set with advanced options"""
        
        # Validate set items
        valid_items = []
        for item_id in set_items:
            if self.items_system.get_item(item_id):
                valid_items.append(item_id)
        
        if not valid_items:
            raise ValueError("No valid items provided for set")
        
        # Create the set
        set_id = self.items_system.create_custom_set(
            creator_id=creator_id,
            set_name=set_name,
            set_description=set_description,
            set_bonuses=set_bonuses,
            set_items=valid_items
        )
        
        # Add additional metadata
        custom_set = self.items_system.get_custom_set(set_id)
        if custom_set:
            custom_set["level_requirement"] = level_requirement
            custom_set["class_restriction"] = class_restriction
            custom_set["rarity"] = rarity
        
        return set_id
    
    def get_set_info(self, set_id: str) -> Optional[SetItem]:
        """Get detailed set information"""
        set_data = self.items_system.get_custom_set(set_id)
        if not set_data:
            return None
        
        return SetItem(
            id=set_data["id"],
            name=set_data["name"],
            description=set_data["description"],
            creator_id=set_data["creator_id"],
            creation_time=set_data["creation_time"],
            quality=set_data["quality"],
            set_bonuses=set_data["set_bonuses"],
            set_items=set_data["set_items"],
            usage_count=set_data["usage_count"],
            is_permanent=set_data["is_permanent"],
            rarity=set_data.get("rarity", "rare"),
            level_requirement=set_data.get("level_requirement", 1),
            class_restriction=set_data.get("class_restriction")
        )
    
    def get_sets_by_category(self, category: str) -> List[SetItem]:
        """Get sets filtered by category"""
        all_sets = self.items_system.get_all_custom_sets()
        category_sets = []
        
        for set_data in all_sets:
            set_info = self.get_set_info(set_data["id"])
            if set_info:
                # Check if set matches category
                if category == "combat" and any(bonus in set_info.set_bonuses 
                                               for bonus in ["damage_boost", "defense_boost", "critical_chance"]):
                    category_sets.append(set_info)
                elif category == "survival" and any(bonus in set_info.set_bonuses 
                                                  for bonus in ["health_boost", "mana_boost", "status_resistance"]):
                    category_sets.append(set_info)
                elif category == "utility" and any(bonus in set_info.set_bonuses 
                                                 for bonus in ["skill_boost", "experience_boost", "gold_boost"]):
                    category_sets.append(set_info)
                elif category == "custom":
                    category_sets.append(set_info)
        
        return category_sets
    
    def get_sets_by_creator(self, creator_id: str) -> List[SetItem]:
        """Get all sets created by a specific player"""
        sets_data = self.items_system.get_custom_sets_by_creator(creator_id)
        return [self.get_set_info(set_data["id"]) for set_data in sets_data 
                if self.get_set_info(set_data["id"])]
    
    def get_popular_sets(self, limit: int = 10) -> List[SetItem]:
        """Get the most popular sets by usage count"""
        all_sets = self.items_system.get_all_custom_sets()
        
        # Sort by usage count
        sorted_sets = sorted(all_sets, key=lambda x: x.get("usage_count", 0), reverse=True)
        
        popular_sets = []
        for set_data in sorted_sets[:limit]:
            set_info = self.get_set_info(set_data["id"])
            if set_info:
                popular_sets.append(set_info)
        
        return popular_sets
    
    def can_use_set(self, player: Player, set_id: str) -> Dict[str, Any]:
        """Check if a player can use a specific set"""
        set_info = self.get_set_info(set_id)
        if not set_info:
            return {"can_use": False, "reason": "Set not found"}
        
        # Check level requirement
        if player.level < set_info.level_requirement:
            return {"can_use": False, "reason": f"Level {set_info.level_requirement} required"}
        
        # Check class restriction
        if set_info.class_restriction and player.class_name != set_info.class_restriction:
            return {"can_use": False, "reason": f"Class {set_info.class_restriction} required"}
        
        # Check if player has required items
        inventory = self.items_system.get_inventory(player.id)
        player_items = inventory.get("items", [])
        
        missing_items = []
        for item_id in set_info.set_items:
            if item_id not in player_items:
                missing_items.append(item_id)
        
        if missing_items:
            return {"can_use": False, "reason": f"Missing items: {', '.join(missing_items)}"}
        
        return {"can_use": True, "reason": "All requirements met"}
    
    def apply_set_bonuses(self, player: Player, set_id: str) -> Dict[str, Any]:
        """Apply set bonuses to a player"""
        can_use = self.can_use_set(player, set_id)
        if not can_use["can_use"]:
            return {"success": False, "reason": can_use["reason"]}
        
        set_info = self.get_set_info(set_id)
        if not set_info:
            return {"success": False, "reason": "Set not found"}
        
        # Apply bonuses
        bonuses_applied = {}
        for bonus_type, bonus_value in set_info.set_bonuses.items():
            if bonus_type == "damage_boost":
                player.damage_multiplier = player.damage_multiplier * (1 + bonus_value)
                bonuses_applied["damage_boost"] = bonus_value
            elif bonus_type == "defense_boost":
                player.defense_multiplier = player.defense_multiplier * (1 + bonus_value)
                bonuses_applied["defense_boost"] = bonus_value
            elif bonus_type == "health_boost":
                player.max_health = int(player.max_health * (1 + bonus_value))
                player.current_health = player.max_health
                bonuses_applied["health_boost"] = bonus_value
            elif bonus_type == "mana_boost":
                player.max_mana = int(player.max_mana * (1 + bonus_value))
                player.current_mana = player.max_mana
                bonuses_applied["mana_boost"] = bonus_value
            elif bonus_type == "critical_chance":
                player.critical_chance = min(1.0, player.critical_chance + bonus_value)
                bonuses_applied["critical_chance"] = bonus_value
            elif bonus_type == "critical_damage":
                player.critical_damage_multiplier = player.critical_damage_multiplier * (1 + bonus_value)
                bonuses_applied["critical_damage"] = bonus_value
        
        # Increment usage count
        self.items_system.use_custom_set(set_id, player.id)
        
        return {
            "success": True,
            "set_name": set_info.name,
            "bonuses_applied": bonuses_applied,
            "usage_count": set_info.usage_count + 1
        }
    
    def remove_set_bonuses(self, player: Player, set_id: str) -> Dict[str, Any]:
        """Remove set bonuses from a player"""
        set_info = self.get_set_info(set_id)
        if not set_info:
            return {"success": False, "reason": "Set not found"}
        
        # Remove bonuses (reverse the application)
        bonuses_removed = {}
        for bonus_type, bonus_value in set_info.set_bonuses.items():
            if bonus_type == "damage_boost":
                player.damage_multiplier = player.damage_multiplier / (1 + bonus_value)
                bonuses_removed["damage_boost"] = bonus_value
            elif bonus_type == "defense_boost":
                player.defense_multiplier = player.defense_multiplier / (1 + bonus_value)
                bonuses_removed["defense_boost"] = bonus_value
            elif bonus_type == "health_boost":
                player.max_health = int(player.max_health / (1 + bonus_value))
                player.current_health = min(player.current_health, player.max_health)
                bonuses_removed["health_boost"] = bonus_value
            elif bonus_type == "mana_boost":
                player.max_mana = int(player.max_mana / (1 + bonus_value))
                player.current_mana = min(player.current_mana, player.max_mana)
                bonuses_removed["mana_boost"] = bonus_value
            elif bonus_type == "critical_chance":
                player.critical_chance = max(0.0, player.critical_chance - bonus_value)
                bonuses_removed["critical_chance"] = bonus_value
            elif bonus_type == "critical_damage":
                player.critical_damage_multiplier = player.critical_damage_multiplier / (1 + bonus_value)
                bonuses_removed["critical_damage"] = bonus_value
        
        return {
            "success": True,
            "set_name": set_info.name,
            "bonuses_removed": bonuses_removed
        }
    
    def generate_set_suggestions(self, player: Player) -> List[Dict[str, Any]]:
        """Generate set suggestions based on player's current items and class"""
        inventory = self.items_system.get_inventory(player.id)
        player_items = inventory.get("items", [])
        
        suggestions = []
        
        # Check template sets
        for template_name, template in self.bonus_templates.items():
            if template["class_restriction"] and template["class_restriction"] != player.class_name:
                continue
            
            if player.level < template["level_requirement"]:
                continue
            
            # Check how many template items the player has
            owned_items = [item for item in template["items"] if item in player_items]
            completion_rate = len(owned_items) / len(template["items"])
            
            if completion_rate > 0.3:  # At least 30% complete
                suggestions.append({
                    "template": template_name,
                    "name": template["name"],
                    "description": template["description"],
                    "completion_rate": completion_rate,
                    "owned_items": owned_items,
                    "missing_items": [item for item in template["items"] if item not in player_items],
                    "bonuses": template["bonuses"]
                })
        
        # Sort by completion rate
        suggestions.sort(key=lambda x: x["completion_rate"], reverse=True)
        return suggestions
    
    def export_set_data(self, set_id: str) -> Optional[Dict[str, Any]]:
        """Export set data for sharing"""
        set_info = self.get_set_info(set_id)
        if not set_info:
            return None
        
        return {
            "id": set_info.id,
            "name": set_info.name,
            "description": set_info.description,
            "creator_id": set_info.creator_id,
            "creation_time": set_info.creation_time,
            "set_bonuses": set_info.set_bonuses,
            "set_items": set_info.set_items,
            "level_requirement": set_info.level_requirement,
            "class_restriction": set_info.class_restriction,
            "rarity": set_info.rarity,
            "usage_count": set_info.usage_count
        }
    
    def import_set_data(self, set_data: Dict[str, Any], new_creator_id: str) -> Optional[str]:
        """Import set data from another player"""
        try:
            return self.create_custom_set(
                creator_id=new_creator_id,
                set_name=set_data["name"],
                set_description=set_data["description"],
                set_bonuses=set_data["set_bonuses"],
                set_items=set_data["set_items"],
                level_requirement=set_data.get("level_requirement", 1),
                class_restriction=set_data.get("class_restriction"),
                rarity=set_data.get("rarity", "rare")
            )
        except Exception as e:
            print(f"Error importing set: {e}")
            return None

def main():
    """Main function for set item management"""
    manager = SetItemManager()
    
    print("Chronicles of Ruin: Sunderfall - Set Item Manager")
    print("=" * 60)
    print("1. Create Set from Template")
    print("2. Create Custom Set")
    print("3. View Set Information")
    print("4. List Popular Sets")
    print("5. Generate Set Suggestions")
    print("6. Export/Import Set Data")
    print("7. Exit")
    
    choice = input("\nEnter your choice (1-7): ").strip()
    
    if choice == "1":
        print("\nAvailable Templates:")
        for template_name in manager.bonus_templates.keys():
            template = manager.bonus_templates[template_name]
            print(f"  {template_name}: {template['name']} - {template['description']}")
        
        template_name = input("\nEnter template name: ").strip()
        custom_name = input("Enter custom name (or press Enter for default): ").strip()
        custom_description = input("Enter custom description (or press Enter for default): ").strip()
        
        set_id = manager.create_set_from_template(
            creator_id="test_player",
            template_name=template_name,
            custom_name=custom_name if custom_name else None,
            custom_description=custom_description if custom_description else None
        )
        
        if set_id:
            print(f"Set created successfully! ID: {set_id}")
        else:
            print("Failed to create set.")
    
    elif choice == "2":
        print("\nCreate Custom Set")
        set_name = input("Enter set name: ").strip()
        set_description = input("Enter set description: ").strip()
        
        print("\nAvailable bonus types:")
        for bonus_type in SetBonusType:
            print(f"  {bonus_type.value}")
        
        bonuses = {}
        while True:
            bonus_type = input("\nEnter bonus type (or 'done' to finish): ").strip()
            if bonus_type == "done":
                break
            
            try:
                bonus_value = float(input(f"Enter {bonus_type} value (0.0-1.0): "))
                bonuses[bonus_type] = bonus_value
            except ValueError:
                print("Invalid value. Please enter a number.")
        
        set_items = []
        print("\nEnter item IDs for the set (one per line, 'done' to finish):")
        while True:
            item_id = input("Item ID: ").strip()
            if item_id == "done":
                break
            set_items.append(item_id)
        
        try:
            set_id = manager.create_custom_set(
                creator_id="test_player",
                set_name=set_name,
                set_description=set_description,
                set_bonuses=bonuses,
                set_items=set_items
            )
            print(f"Custom set created successfully! ID: {set_id}")
        except Exception as e:
            print(f"Failed to create set: {e}")
    
    elif choice == "3":
        set_id = input("\nEnter set ID: ").strip()
        set_info = manager.get_set_info(set_id)
        
        if set_info:
            print(f"\nSet Information:")
            print(f"  Name: {set_info.name}")
            print(f"  Description: {set_info.description}")
            print(f"  Creator: {set_info.creator_id}")
            print(f"  Usage Count: {set_info.usage_count}")
            print(f"  Level Requirement: {set_info.level_requirement}")
            print(f"  Class Restriction: {set_info.class_restriction or 'None'}")
            print(f"  Rarity: {set_info.rarity}")
            print(f"  Bonuses: {set_info.set_bonuses}")
            print(f"  Items: {set_info.set_items}")
        else:
            print("Set not found.")
    
    elif choice == "4":
        print("\nPopular Sets:")
        popular_sets = manager.get_popular_sets(limit=10)
        
        for i, set_info in enumerate(popular_sets, 1):
            print(f"{i}. {set_info.name} - {set_info.usage_count} uses")
            print(f"   {set_info.description}")
            print()
    
    elif choice == "5":
        # Create a test player for suggestions
        test_player = manager.player_system.create_player("test_player", "Warrior")
        test_player.level = 10
        
        # Add some items to inventory
        inventory = manager.items_system.get_inventory(test_player.id)
        inventory["items"].extend(["iron_sword", "iron_armor"])
        
        suggestions = manager.generate_set_suggestions(test_player)
        
        print(f"\nSet Suggestions for {test_player.name} (Level {test_player.level} {test_player.class_name}):")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion['name']} - {suggestion['completion_rate']:.1%} complete")
            print(f"   {suggestion['description']}")
            print(f"   Missing: {', '.join(suggestion['missing_items'])}")
            print()
    
    elif choice == "6":
        print("\nExport/Import Set Data")
        print("1. Export set data")
        print("2. Import set data")
        
        sub_choice = input("Enter choice (1-2): ").strip()
        
        if sub_choice == "1":
            set_id = input("Enter set ID to export: ").strip()
            set_data = manager.export_set_data(set_id)
            
            if set_data:
                filename = f"set_export_{set_id}.json"
                with open(filename, 'w') as f:
                    json.dump(set_data, f, indent=2)
                print(f"Set data exported to {filename}")
            else:
                print("Set not found.")
        
        elif sub_choice == "2":
            filename = input("Enter import filename: ").strip()
            try:
                with open(filename, 'r') as f:
                    set_data = json.load(f)
                
                set_id = manager.import_set_data(set_data, "test_player")
                if set_id:
                    print(f"Set imported successfully! New ID: {set_id}")
                else:
                    print("Failed to import set.")
            except Exception as e:
                print(f"Error importing set: {e}")
    
    else:
        print("Exiting...")

if __name__ == "__main__":
    main()

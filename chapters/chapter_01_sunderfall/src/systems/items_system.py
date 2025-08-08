"""
CHRONICLES OF RUIN: ITEMS SYSTEM
================================

This module handles all item-related functionality for Chronicles of Ruin.
It manages equipment, custom set creation, item properties, and inventory.

PURPOSE:
- Manages equipment and item data
- Handles custom set item creation
- Provides item bonuses and modifiers
- Manages inventory and item storage
- Implements item rarity and quality systems

ARCHITECTURE:
- ItemManager: Manages all item data and properties
- EquipmentSystem: Handles equipment slots and bonuses
- CustomSetCreator: Manages custom set item creation
- InventoryManager: Handles inventory and item storage
- ItemQuality: Manages item rarity and quality levels

ITEM TYPES:
- Weapons: Primary damage sources with various types
- Armor: Defensive equipment for different slots
- Accessories: Rings, amulets, etc. with special bonuses
- Consumables: Potions, scrolls, etc. for temporary effects
- Custom Sets: Player-created sets with unique bonuses

CUSTOM SET SYSTEM:
- Players can create permanent custom set items
- Sets provide unique bonuses and effects
- Sets are permanent and cannot be modified once created
- Sets can be shared and used by other players

This system provides deep itemization while allowing players to
create their own unique equipment through the custom set system.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import random
import json
import time

class ItemType(Enum):
    """Enumeration of item types."""
    WEAPON = "weapon"
    ARMOR = "armor"
    ACCESSORY = "accessory"
    CONSUMABLE = "consumable"
    CUSTOM_SET = "custom_set"

class EquipmentSlot(Enum):
    """Enumeration of equipment slots."""
    WEAPON_MAIN = "weapon_main"
    WEAPON_OFF = "weapon_off"
    ARMOR_HEAD = "armor_head"
    ARMOR_CHEST = "armor_chest"
    ARMOR_LEGS = "armor_legs"
    ARMOR_FEET = "armor_feet"
    ACCESSORY_1 = "accessory_1"
    ACCESSORY_2 = "accessory_2"

class ItemQuality(Enum):
    """Enumeration of item quality levels."""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"
    CUSTOM = "custom"

class ItemsSystem:
    """
    Main items system that handles all item-related functionality.
    Manages equipment, custom sets, and inventory.
    """
    
    def __init__(self):
        """Initialize the items system."""
        self.items_database = self._initialize_items_database()
        self.custom_sets = {}
        self.equipment_slots = self._initialize_equipment_slots()
        self.inventories = {}  # player_id -> inventory
        
    def _initialize_items_database(self) -> Dict[str, Dict]:
        """Initialize the items database with base items."""
        return {
            # Weapons
            "iron_sword": {
                'id': 'iron_sword',
                'name': 'Iron Sword',
                'type': ItemType.WEAPON,
                'slot': EquipmentSlot.WEAPON_MAIN,
                'quality': ItemQuality.COMMON,
                'damage': 5,
                'damage_modifier': 1.0,
                'description': 'A basic iron sword',
                'bonuses': {'physical_damage': 0.1}
            },
            "steel_sword": {
                'id': 'steel_sword',
                'name': 'Steel Sword',
                'type': ItemType.WEAPON,
                'slot': EquipmentSlot.WEAPON_MAIN,
                'quality': ItemQuality.UNCOMMON,
                'damage': 8,
                'damage_modifier': 1.1,
                'description': 'A well-crafted steel sword',
                'bonuses': {'physical_damage': 0.15}
            },
            "fire_staff": {
                'id': 'fire_staff',
                'name': 'Fire Staff',
                'type': ItemType.WEAPON,
                'slot': EquipmentSlot.WEAPON_MAIN,
                'quality': ItemQuality.RARE,
                'damage': 6,
                'damage_modifier': 1.2,
                'description': 'A staff that channels fire magic',
                'bonuses': {'fire_damage': 0.25, 'mana_bonus': 0.2}
            },
            
            # Armor
            "leather_armor": {
                'id': 'leather_armor',
                'name': 'Leather Armor',
                'type': ItemType.ARMOR,
                'slot': EquipmentSlot.ARMOR_CHEST,
                'quality': ItemQuality.COMMON,
                'defense': 3,
                'description': 'Basic leather armor',
                'bonuses': {'physical_defense': 0.1}
            },
            "chain_mail": {
                'id': 'chain_mail',
                'name': 'Chain Mail',
                'type': ItemType.ARMOR,
                'slot': EquipmentSlot.ARMOR_CHEST,
                'quality': ItemQuality.UNCOMMON,
                'defense': 6,
                'description': 'Protective chain mail armor',
                'bonuses': {'physical_defense': 0.2}
            },
            
            # Accessories
            "ring_of_strength": {
                'id': 'ring_of_strength',
                'name': 'Ring of Strength',
                'type': ItemType.ACCESSORY,
                'slot': EquipmentSlot.ACCESSORY_1,
                'quality': ItemQuality.RARE,
                'description': 'A ring that increases strength',
                'bonuses': {'physical_damage': 0.1, 'strength': 2}
            },
            "amulet_of_protection": {
                'id': 'amulet_of_protection',
                'name': 'Amulet of Protection',
                'type': ItemType.ACCESSORY,
                'slot': EquipmentSlot.ACCESSORY_2,
                'quality': ItemQuality.EPIC,
                'description': 'An amulet that provides protection',
                'bonuses': {'all_defense': 0.15, 'status_resistance': 0.2}
            }
        }
    
    def _initialize_equipment_slots(self) -> Dict[EquipmentSlot, Dict]:
        """Initialize equipment slot definitions."""
        return {
            EquipmentSlot.WEAPON_MAIN: {
                'name': 'Main Hand',
                'allowed_types': [ItemType.WEAPON],
                'required': False
            },
            EquipmentSlot.WEAPON_OFF: {
                'name': 'Off Hand',
                'allowed_types': [ItemType.WEAPON],
                'required': False
            },
            EquipmentSlot.ARMOR_HEAD: {
                'name': 'Head',
                'allowed_types': [ItemType.ARMOR],
                'required': False
            },
            EquipmentSlot.ARMOR_CHEST: {
                'name': 'Chest',
                'allowed_types': [ItemType.ARMOR],
                'required': False
            },
            EquipmentSlot.ARMOR_LEGS: {
                'name': 'Legs',
                'allowed_types': [ItemType.ARMOR],
                'required': False
            },
            EquipmentSlot.ARMOR_FEET: {
                'name': 'Feet',
                'allowed_types': [ItemType.ARMOR],
                'required': False
            },
            EquipmentSlot.ACCESSORY_1: {
                'name': 'Accessory 1',
                'allowed_types': [ItemType.ACCESSORY],
                'required': False
            },
            EquipmentSlot.ACCESSORY_2: {
                'name': 'Accessory 2',
                'allowed_types': [ItemType.ACCESSORY],
                'required': False
            }
        }
    
    def get_item(self, item_id: str) -> Optional[Dict]:
        """Get item data by ID."""
        return self.items_database.get(item_id)
    
    def get_all_items(self) -> List[Dict]:
        """Get all items in the database."""
        return list(self.items_database.values())
    
    def get_items_by_type(self, item_type: ItemType) -> List[Dict]:
        """Get all items of a specific type."""
        return [item for item in self.items_database.values() if item['type'] == item_type]
    
    def get_items_by_quality(self, quality: ItemQuality) -> List[Dict]:
        """Get all items of a specific quality."""
        return [item for item in self.items_database.values() if item['quality'] == quality]
    
    def create_custom_set(self, creator_id: str, set_name: str, set_description: str,
                         set_bonuses: Dict, set_items: List[str]) -> str:
        """
        Create a custom set item.
        
        Args:
            creator_id: ID of the player creating the set
            set_name: Name of the custom set
            set_description: Description of the set
            set_bonuses: Dictionary of bonuses the set provides
            set_items: List of item IDs that make up the set
            
        Returns:
            Custom set ID
        """
        set_id = f"custom_set_{creator_id}_{int(time.time())}"
        
        custom_set = {
            'id': set_id,
            'name': set_name,
            'description': set_description,
            'creator_id': creator_id,
            'creation_time': time.time(),
            'type': ItemType.CUSTOM_SET,
            'quality': ItemQuality.CUSTOM,
            'set_bonuses': set_bonuses,
            'set_items': set_items,
            'usage_count': 0,
            'is_permanent': True
        }
        
        self.custom_sets[set_id] = custom_set
        return set_id
    
    def get_custom_set(self, set_id: str) -> Optional[Dict]:
        """Get custom set data by ID."""
        return self.custom_sets.get(set_id)
    
    def get_all_custom_sets(self) -> List[Dict]:
        """Get all custom sets."""
        return list(self.custom_sets.values())
    
    def get_custom_sets_by_creator(self, creator_id: str) -> List[Dict]:
        """Get all custom sets created by a specific player."""
        return [set_data for set_data in self.custom_sets.values() 
                if set_data['creator_id'] == creator_id]
    
    def use_custom_set(self, set_id: str, user_id: str) -> bool:
        """
        Use a custom set (increment usage count).
        
        Args:
            set_id: ID of the custom set
            user_id: ID of the player using the set
            
        Returns:
            True if successful, False otherwise
        """
        if set_id not in self.custom_sets:
            return False
        
        self.custom_sets[set_id]['usage_count'] += 1
        return True
    
    def get_inventory(self, player_id: str) -> Dict:
        """Get a player's inventory."""
        if player_id not in self.inventories:
            self.inventories[player_id] = {
                'items': [],
                'equipment': {},
                'gold': 0,
                'capacity': 50
            }
        return self.inventories[player_id]
    
    def add_item_to_inventory(self, player_id: str, item_id: str, quantity: int = 1) -> bool:
        """
        Add an item to a player's inventory.
        
        Args:
            player_id: ID of the player
            item_id: ID of the item to add
            quantity: Quantity to add
            
        Returns:
            True if successful, False otherwise
        """
        inventory = self.get_inventory(player_id)
        
        # Check if item exists
        if item_id not in self.items_database and item_id not in self.custom_sets:
            return False
        
        # Check inventory capacity
        if len(inventory['items']) + quantity > inventory['capacity']:
            return False
        
        # Add item
        for _ in range(quantity):
            inventory['items'].append(item_id)
        
        return True
    
    def remove_item_from_inventory(self, player_id: str, item_id: str, quantity: int = 1) -> bool:
        """
        Remove an item from a player's inventory.
        
        Args:
            player_id: ID of the player
            item_id: ID of the item to remove
            quantity: Quantity to remove
            
        Returns:
            True if successful, False otherwise
        """
        inventory = self.get_inventory(player_id)
        
        # Count available items
        available = inventory['items'].count(item_id)
        
        if available < quantity:
            return False
        
        # Remove items
        for _ in range(quantity):
            inventory['items'].remove(item_id)
        
        return True
    
    def equip_item(self, player_id: str, item_id: str, slot: EquipmentSlot) -> bool:
        """
        Equip an item to a specific slot.
        
        Args:
            player_id: ID of the player
            item_id: ID of the item to equip
            slot: Equipment slot to equip to
            
        Returns:
            True if successful, False otherwise
        """
        inventory = self.get_inventory(player_id)
        
        # Check if item is in inventory
        if item_id not in inventory['items']:
            return False
        
        # Get item data
        item_data = self.get_item(item_id)
        if not item_data:
            return False
        
        # Check if slot is valid for item type
        slot_data = self.equipment_slots.get(slot)
        if not slot_data or item_data['type'] not in slot_data['allowed_types']:
            return False
        
        # Unequip current item in slot
        if slot in inventory['equipment']:
            old_item = inventory['equipment'][slot]
            inventory['items'].append(old_item)
        
        # Equip new item
        inventory['equipment'][slot] = item_id
        inventory['items'].remove(item_id)
        
        return True
    
    def unequip_item(self, player_id: str, slot: EquipmentSlot) -> bool:
        """
        Unequip an item from a specific slot.
        
        Args:
            player_id: ID of the player
            slot: Equipment slot to unequip from
            
        Returns:
            True if successful, False otherwise
        """
        inventory = self.get_inventory(player_id)
        
        if slot not in inventory['equipment']:
            return False
        
        # Move item back to inventory
        item_id = inventory['equipment'][slot]
        inventory['items'].append(item_id)
        del inventory['equipment'][slot]
        
        return True
    
    def get_equipment_bonuses(self, player_id: str) -> Dict:
        """
        Get all bonuses from equipped items.
        
        Args:
            player_id: ID of the player
            
        Returns:
            Dictionary of bonuses
        """
        inventory = self.get_inventory(player_id)
        bonuses = {}
        
        # Check equipped items
        for slot, item_id in inventory['equipment'].items():
            item_data = self.get_item(item_id)
            if item_data and 'bonuses' in item_data:
                for bonus_type, bonus_value in item_data['bonuses'].items():
                    if bonus_type in bonuses:
                        bonuses[bonus_type] += bonus_value
                    else:
                        bonuses[bonus_type] = bonus_value
        
        return bonuses
    
    def get_item_summary(self, item_id: str) -> Dict:
        """Get a comprehensive summary of an item."""
        # Check regular items
        if item_id in self.items_database:
            item_data = self.items_database[item_id]
            return {
                'id': item_data['id'],
                'name': item_data['name'],
                'type': item_data['type'].value,
                'quality': item_data['quality'].value,
                'description': item_data['description'],
                'bonuses': item_data.get('bonuses', {}),
                'is_custom': False
            }
        
        # Check custom sets
        elif item_id in self.custom_sets:
            set_data = self.custom_sets[item_id]
            return {
                'id': set_data['id'],
                'name': set_data['name'],
                'type': set_data['type'].value,
                'quality': set_data['quality'].value,
                'description': set_data['description'],
                'creator_id': set_data['creator_id'],
                'usage_count': set_data['usage_count'],
                'set_bonuses': set_data['set_bonuses'],
                'set_items': set_data['set_items'],
                'is_custom': True
            }
        
        return {'error': 'Item not found'}

# Example usage and testing
if __name__ == "__main__":
    items_system = ItemsSystem()
    
    # Test getting items
    iron_sword = items_system.get_item("iron_sword")
    print(f"Iron sword: {iron_sword['name']}")
    
    # Test creating custom set
    set_id = items_system.create_custom_set(
        creator_id="player1",
        set_name="Fire Warrior Set",
        set_description="A custom set for fire-based warriors",
        set_bonuses={'fire_damage': 0.3, 'physical_damage': 0.2},
        set_items=["fire_staff", "ring_of_strength"]
    )
    print(f"Created custom set: {set_id}")
    
    # Test inventory management
    items_system.add_item_to_inventory("player1", "iron_sword", 2)
    inventory = items_system.get_inventory("player1")
    print(f"Player inventory: {inventory['items']}")
    
    # Test equipment
    items_system.equip_item("player1", "iron_sword", EquipmentSlot.WEAPON_MAIN)
    bonuses = items_system.get_equipment_bonuses("player1")
    print(f"Equipment bonuses: {bonuses}")
    
    # Test custom set summary
    set_summary = items_system.get_item_summary(set_id)
    print(f"Custom set summary: {set_summary['name']}")
    print(f"Usage count: {set_summary['usage_count']}")

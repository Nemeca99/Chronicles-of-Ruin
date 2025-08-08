#!/usr/bin/env python3
"""
World System for Chronicles of Ruin: Sunderfall
Manages areas, districts, and exploration mechanics
"""

import json
import os
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime, timedelta
import random


class AreaType(Enum):
    """Types of areas"""

    DISTRICT = "district"
    BUILDING = "building"
    DUNGEON = "dungeon"
    WILDERNESS = "wilderness"
    TOWN = "town"


class AreaDifficulty(Enum):
    """Area difficulty levels"""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"
    MASTER = "master"


class Area:
    """Represents a game area"""

    def __init__(
        self,
        area_id: str,
        name: str,
        description: str,
        area_type: AreaType,
        difficulty: AreaDifficulty,
        level_requirement: int,
        monster_types: List[str],
        loot_table: List[str],
        connections: List[str] = None,
    ):
        self.area_id = area_id
        self.name = name
        self.description = description
        self.area_type = area_type
        self.difficulty = difficulty
        self.level_requirement = level_requirement
        self.monster_types = monster_types
        self.loot_table = loot_table
        self.connections = connections or []
        self.created_at = datetime.now()


class WorldSystem:
    """Manages world areas and exploration"""

    def __init__(self, player_system=None, monster_system=None):
        self.player_system = player_system
        self.monster_system = monster_system
        self.areas = {}
        self.player_exploration = {}
        self._load_areas()

    def _load_areas(self):
        """Load all game areas"""
        # Starting District
        self._add_area(
            Area(
                "village_square",
                "Village Square",
                "The heart of the village, where villagers gather and trade",
                AreaType.DISTRICT,
                AreaDifficulty.EASY,
                1,
                ["bandit", "thief"],
                ["health_potion", "leather_armor", "iron_sword"],
                ["market_district", "residential_district"],
            )
        )

        # Market District
        self._add_area(
            Area(
                "market_district",
                "Market District",
                "A bustling marketplace filled with merchants and goods",
                AreaType.DISTRICT,
                AreaDifficulty.EASY,
                2,
                ["merchant_guard", "pickpocket"],
                ["mana_potion", "chain_armor", "steel_sword"],
                ["village_square", "warehouse_district"],
            )
        )

        # Residential District
        self._add_area(
            Area(
                "residential_district",
                "Residential District",
                "Quiet streets lined with homes and gardens",
                AreaType.DISTRICT,
                AreaDifficulty.MEDIUM,
                3,
                ["guard", "watchman"],
                ["strength_potion", "plate_armor", "magic_sword"],
                ["village_square", "noble_district"],
            )
        )

        # Warehouse District
        self._add_area(
            Area(
                "warehouse_district",
                "Warehouse District",
                "Large warehouses storing goods and supplies",
                AreaType.DISTRICT,
                AreaDifficulty.MEDIUM,
                4,
                ["warehouse_guard", "smuggler"],
                ["rare_gem", "gold_coin", "silver_coin"],
                ["market_district", "docks"],
            )
        )

        # Noble District
        self._add_area(
            Area(
                "noble_district",
                "Noble District",
                "Elegant mansions and estates of the wealthy",
                AreaType.DISTRICT,
                AreaDifficulty.HARD,
                5,
                ["noble_guard", "assassin"],
                ["magic_sword", "plate_armor", "rare_gem"],
                ["residential_district", "castle_gates"],
            )
        )

        # Docks
        self._add_area(
            Area(
                "docks",
                "The Docks",
                "Busy port area with ships and sailors",
                AreaType.DISTRICT,
                AreaDifficulty.MEDIUM,
                4,
                ["sailor", "dock_worker"],
                ["fishing_rod", "sailor_hat", "gold_coin"],
                ["warehouse_district", "harbor"],
            )
        )

        # Castle Gates
        self._add_area(
            Area(
                "castle_gates",
                "Castle Gates",
                "Heavily guarded entrance to the royal castle",
                AreaType.DISTRICT,
                AreaDifficulty.EXPERT,
                6,
                ["royal_guard", "knight"],
                ["royal_sword", "royal_armor", "crown_jewel"],
                ["noble_district", "castle_interior"],
            )
        )

        # Castle Interior
        self._add_area(
            Area(
                "castle_interior",
                "Castle Interior",
                "The grand halls and chambers of the royal castle",
                AreaType.DISTRICT,
                AreaDifficulty.MASTER,
                7,
                ["royal_knight", "castle_mage"],
                ["royal_crown", "magic_staff", "ancient_tome"],
                ["castle_gates"],
            )
        )

        # Wilderness Areas
        self._add_area(
            Area(
                "forest_path",
                "Forest Path",
                "A winding path through dense woods",
                AreaType.WILDERNESS,
                AreaDifficulty.MEDIUM,
                3,
                ["wolf", "bandit"],
                ["healing_herb", "mana_herb", "wooden_staff"],
                ["village_square", "forest_clearing"],
            )
        )

        self._add_area(
            Area(
                "forest_clearing",
                "Forest Clearing",
                "A peaceful clearing in the heart of the forest",
                AreaType.WILDERNESS,
                AreaDifficulty.HARD,
                4,
                ["bear", "hunter"],
                ["bear_claw", "hunting_bow", "leather_armor"],
                ["forest_path", "mountain_path"],
            )
        )

        # Dungeon Areas
        self._add_area(
            Area(
                "ancient_crypt",
                "Ancient Crypt",
                "A dark and foreboding underground tomb",
                AreaType.DUNGEON,
                AreaDifficulty.HARD,
                5,
                ["skeleton", "zombie"],
                ["bone_sword", "necrotic_armor", "soul_gem"],
                ["forest_clearing"],
            )
        )

        # Training Grounds (new easy area)
        self._add_area(
            Area(
                "training_grounds",
                "Training Grounds",
                "A safe place for new adventurers to practice against weak foes.",
                AreaType.DISTRICT,
                AreaDifficulty.EASY,
                1,
                ["guard", "watchman"],
                ["health_potion", "healing_herb", "wooden_staff"],
                ["village_square", "market_district"],
            )
        )

        # Ensure connections include training grounds
        self.areas["village_square"].connections.append("training_grounds")
        self.areas["market_district"].connections.append("training_grounds")

    def _add_area(self, area: Area):
        """Add an area to the world"""
        self.areas[area.area_id] = area

    def get_player_exploration(self, player_id: str) -> Dict[str, Any]:
        """Get exploration data for a player"""
        if player_id not in self.player_exploration:
            self.player_exploration[player_id] = {
                "current_area": "village_square",
                "visited_areas": {"village_square"},
                "area_progress": {},
                "exploration_stats": {
                    "areas_visited": 1,
                    "total_exploration_time": 0,
                    "secrets_found": 0,
                    "treasures_discovered": 0,
                },
                "last_updated": datetime.now(),
            }
        return self.player_exploration[player_id]

    def get_available_areas(self, player_id: str) -> List[Dict[str, Any]]:
        """Get areas available to a player"""
        player_data = (
            self.player_system.get_player(player_id) if self.player_system else {}
        )
        exploration = self.get_player_exploration(player_id)
        current_area = exploration["current_area"]

        available_areas = []

        if current_area in self.areas:
            current_area_obj = self.areas[current_area]

            for connection_id in current_area_obj.connections:
                if connection_id in self.areas:
                    area = self.areas[connection_id]

                    # Check level requirement
                    if player_data.get("player_level", 0) < area.level_requirement:
                        continue

                    area_info = {
                        "id": area.area_id,
                        "name": area.name,
                        "description": area.description,
                        "type": area.area_type.value,
                        "difficulty": area.difficulty.value,
                        "level_requirement": area.level_requirement,
                        "visited": area.area_id in exploration["visited_areas"],
                        "monster_types": area.monster_types,
                        "loot_table": area.loot_table,
                    }

                    available_areas.append(area_info)

        return available_areas

    def travel_to_area(self, player_id: str, area_id: str) -> Dict[str, Any]:
        """Travel to a new area"""
        if area_id not in self.areas:
            return {"success": False, "error": "Area not found"}

        exploration = self.get_player_exploration(player_id)
        current_area = exploration["current_area"]

        # Check if area is connected to current area
        if current_area in self.areas:
            current_area_obj = self.areas[current_area]
            if area_id not in current_area_obj.connections:
                return {"success": False, "error": "Area not connected"}

        # Check level requirement
        area = self.areas[area_id]
        player_data = (
            self.player_system.get_player(player_id) if self.player_system else {}
        )

        if player_data.get("player_level", 0) < area.level_requirement:
            return {
                "success": False,
                "error": f"Level {area.level_requirement} required",
            }

        # Travel to area
        exploration["current_area"] = area_id
        exploration["visited_areas"].add(area_id)
        exploration["exploration_stats"]["areas_visited"] = len(
            exploration["visited_areas"]
        )
        exploration["last_updated"] = datetime.now()

        print(f"🗺️  Traveled to: {area.name}")
        print(f"   {area.description}")

        return {
            "success": True,
            "area_name": area.name,
            "area_description": area.description,
            "area_type": area.area_type.value,
            "difficulty": area.difficulty.value,
        }

    def get_current_area(self, player_id: str) -> Dict[str, Any]:
        """Get player's current area"""
        exploration = self.get_player_exploration(player_id)
        current_area_id = exploration["current_area"]

        if current_area_id in self.areas:
            area = self.areas[current_area_id]
            return {
                "id": area.area_id,
                "name": area.name,
                "description": area.description,
                "type": area.area_type.value,
                "difficulty": area.difficulty.value,
                "level_requirement": area.level_requirement,
                "monster_types": area.monster_types,
                "loot_table": area.loot_table,
                "connections": area.connections,
            }

        return None

    def generate_random_encounter(self, player_id: str) -> Dict[str, Any]:
        """Generate a random encounter in the current area"""
        exploration = self.get_player_exploration(player_id)
        current_area_id = exploration["current_area"]

        if current_area_id not in self.areas:
            return {"success": False, "error": "Invalid area"}

        area = self.areas[current_area_id]

        # Random chance for encounter
        if random.random() < 0.7:  # 70% chance
            if self.monster_system and self.player_system:
                player_data = self.player_system.get_player(player_id) or {}

                # Map local monster_types to archetypes/classifications
                def map_monster_type(mon_type: str):
                    mon_type = mon_type.lower()
                    if "guard" in mon_type or "warrior" in mon_type:
                        return ("melee", "humanoid")
                    if (
                        "watchman" in mon_type
                        or "archer" in mon_type
                        or "ranger" in mon_type
                    ):
                        return ("ranged", "humanoid")
                    if (
                        "mage" in mon_type
                        or "sorcer" in mon_type
                        or "wizard" in mon_type
                    ):
                        return ("magic", "humanoid")
                    return ("melee", "humanoid")

                # Pick a local type and map
                local_type = (
                    random.choice(area.monster_types) if area.monster_types else "guard"
                )
                arch_s, cls_s = map_monster_type(local_type)

                # Build forced enums safely
                from .monster_system import MonsterArchetype, MonsterClassification

                forced_archetype = MonsterArchetype(arch_s)
                forced_classification = MonsterClassification(cls_s)

                base_level = area.level_requirement
                monster = self.monster_system.generate_encounter_monster(
                    base_level=base_level,
                    player_data=player_data,
                    forced_archetype=forced_archetype,
                    forced_classification=forced_classification,
                )

                return {
                    "success": True,
                    "encounter_type": "monster",
                    "monster": monster,
                    "area": area.name,
                }

        # No encounter
        return {
            "success": True,
            "encounter_type": "none",
            "message": f"You explore {area.name} but find nothing of interest.",
        }

    def search_area(self, player_id: str) -> Dict[str, Any]:
        """Search the current area for items"""
        exploration = self.get_player_exploration(player_id)
        current_area_id = exploration["current_area"]

        if current_area_id not in self.areas:
            return {"success": False, "error": "Invalid area"}

        area = self.areas[current_area_id]

        # Random chance to find items
        found_items = []
        if random.random() < 0.4:  # 40% chance to find something
            num_items = random.randint(1, 2)
            for _ in range(num_items):
                item = random.choice(area.loot_table)
                found_items.append(item)

        if found_items:
            # Add items to player inventory
            if self.player_system and hasattr(self.player_system, "items_system"):
                items_system = self.player_system.items_system
                for item in found_items:
                    items_system.add_item_to_inventory(player_id, item, 1)

            exploration["exploration_stats"]["treasures_discovered"] += len(found_items)
            exploration["last_updated"] = datetime.now()

            return {
                "success": True,
                "found_items": found_items,
                "message": f"You found {len(found_items)} item(s) in {area.name}!",
            }
        else:
            return {
                "success": True,
                "found_items": [],
                "message": f"You search {area.name} but find nothing.",
            }

    def get_exploration_stats(self, player_id: str) -> Dict[str, Any]:
        """Get exploration statistics for a player"""
        exploration = self.get_player_exploration(player_id)

        return {
            "current_area": exploration["current_area"],
            "areas_visited": exploration["exploration_stats"]["areas_visited"],
            "total_areas": len(self.areas),
            "exploration_percentage": (
                exploration["exploration_stats"]["areas_visited"] / len(self.areas)
            )
            * 100,
            "secrets_found": exploration["exploration_stats"]["secrets_found"],
            "treasures_discovered": exploration["exploration_stats"][
                "treasures_discovered"
            ],
            "visited_areas": list(exploration["visited_areas"]),
        }

    def get_area_info(self, area_id: str) -> Dict[str, Any]:
        """Get detailed information about an area"""
        if area_id not in self.areas:
            return None

        area = self.areas[area_id]
        return {
            "id": area.area_id,
            "name": area.name,
            "description": area.description,
            "type": area.area_type.value,
            "difficulty": area.difficulty.value,
            "level_requirement": area.level_requirement,
            "monster_types": area.monster_types,
            "loot_table": area.loot_table,
            "connections": area.connections,
        }

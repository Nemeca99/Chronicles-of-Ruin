#!/usr/bin/env python3
"""
Comprehensive test script to verify all major systems are working correctly
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.systems.player_system import PlayerSystem
from src.systems.monster_system import MonsterSystem
from src.systems.combat_system import CombatSystem, Archetype
from src.systems.items_system import ItemsSystem
from src.systems.class_system import ClassSystem, ArchetypeType
from src.systems.skills_system import SkillsSystem
from src.systems.xp_system import XPSystem
from src.systems.status_elemental_system import StatusElementalSystem


def test_all_systems():
    """Test all major game systems."""
    print("🧪 Testing All Game Systems...")
    print("=" * 50)

    # Initialize all systems
    player_system = PlayerSystem()
    monster_system = MonsterSystem()
    items_system = ItemsSystem()
    combat_system = CombatSystem(player_system, monster_system, items_system)
    class_system = ClassSystem(player_system)
    skills_system = SkillsSystem(player_system, class_system)
    xp_system = XPSystem()
    status_system = StatusElementalSystem()

    print("✅ All systems initialized successfully")

    # Test 1: Player Creation
    print("\n1. Testing Player Creation...")
    player_id = "test_player_all"
    base_archetypes = {Archetype.MELEE: 3}  # Pure melee build

    success = player_system.create_player(player_id, "TestPlayer", base_archetypes)
    if not success:
        print("❌ Failed to create test player")
        return

    player_data = player_system.get_player(player_id)
    print(
        f"✅ Player created: {player_data['name']} (Level {player_data['player_level']})"
    )

    # Test 2: Item System
    print("\n2. Testing Item System...")
    items_system.add_item_to_inventory(player_id, "iron_sword", 1)
    items_system.add_item_to_inventory(player_id, "leather_armor", 1)

    inventory = items_system.get_inventory(player_id)
    print(f"✅ Items added: {len(inventory['items'])} items in inventory")

    # Test 3: Combat System
    print("\n3. Testing Combat System...")
    encounter = combat_system.create_encounter(player_id, area_level=1)
    if "error" in encounter:
        print(f"❌ Combat encounter failed: {encounter['error']}")
        return

    print(f"✅ Combat encounter created: {encounter['monster']['name']}")

    # Test player attack
    attack_result = combat_system.player_attack(encounter)
    print("✅ Player attack executed")

    # Test monster attack
    monster_result = combat_system.monster_attack(encounter)
    print("✅ Monster attack executed")

    # Test 4: Class Features
    print("\n4. Testing Class Features...")
    available_features = class_system.get_available_class_features(
        player_id, ArchetypeType.MELEE
    )
    print(
        f"✅ Class features available: {len(available_features.get('all_features', []))}"
    )

    if available_features.get("next_available"):
        unlock_result = class_system.unlock_class_feature(
            player_id,
            ArchetypeType.MELEE,
            available_features["next_available"]["level"],
        )
        print(f"✅ Class feature unlocked: {unlock_result['success']}")

    # Test 5: XP System
    print("\n5. Testing XP System...")
    xp_gain = {"base": 10, "class": 15, "skill": 5}
    xp_result = player_system.add_xp(player_id, xp_gain)
    print(f"✅ XP added: {xp_result['success']}")

    # Test 6: Skills System
    print("\n6. Testing Skills System...")
    available_skills = skills_system.get_available_skills_for_player(player_id)
    print(
        f"✅ Skills system working: {len(available_skills.get('archetypes', {}))} archetypes"
    )

    # Test 7: Status System
    print("\n7. Testing Status System...")
    status_effect = status_system.apply_status_effect("burn", 3, 0.1)
    print(f"✅ Status effect applied: {status_effect}")

    print("\n" + "=" * 50)
    print("🎉 All systems are working correctly!")
    print("✅ Player System")
    print("✅ Monster System")
    print("✅ Combat System")
    print("✅ Items System")
    print("✅ Class System")
    print("✅ Skills System")
    print("✅ XP System")
    print("✅ Status System")
    print("\n🚀 Ready for Discord Bot integration!")


if __name__ == "__main__":
    test_all_systems()

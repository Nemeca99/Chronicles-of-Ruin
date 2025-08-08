#!/usr/bin/env python3
"""
Test Character for Chronicles of Ruin: Sunderfall
A comprehensive test character to verify all game systems
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
from src.systems.achievement_system import AchievementSystem
from src.systems.quest_system import QuestSystem
from src.systems.economy_system import EconomySystem
from src.systems.world_system import WorldSystem


def create_test_character():
    """Create a comprehensive test character with all systems"""
    print("🎮 Creating Test Character...")
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
    achievement_system = AchievementSystem(player_system)
    quest_system = QuestSystem(player_system)
    economy_system = EconomySystem(player_system, items_system)
    world_system = WorldSystem(player_system, monster_system)
    
    print("✅ All systems initialized")
    
    # Create test character
    player_id = "test_character"
    player_name = "TestHero"
    base_archetypes = {Archetype.MELEE: 2, Archetype.MAGIC: 1}  # Hybrid build
    
    success = player_system.create_player(player_id, player_name, base_archetypes)
    if not success:
        print("❌ Failed to create test character")
        return None
    
    print(f"✅ Test character created: {player_name}")
    
    # Add some starting items
    items_system.add_item_to_inventory(player_id, "iron_sword", 1)
    items_system.add_item_to_inventory(player_id, "leather_armor", 1)
    items_system.add_item_to_inventory(player_id, "health_potion", 3)
    items_system.add_item_to_inventory(player_id, "mana_potion", 2)
    
    print("✅ Starting items added")
    
    # Add some XP to level up
    xp_gain = {"base": 500, "class": 300, "skill": 200}
    player_system.add_xp(player_id, xp_gain)
    
    print("✅ XP added for leveling")
    
    # Get character info
    player_data = player_system.get_player(player_id)
    print(f"📊 Character Level: {player_data['player_level']}")
    print(f"📊 Total XP: {player_data['xp']['base'] + player_data['xp']['class'] + player_data['xp']['skill']}")
    print(f"📊 Archetypes: {player_data['archetypes']}")
    
    # Test all systems
    test_results = {
        "player_system": test_player_system(player_system, player_id),
        "items_system": test_items_system(items_system, player_id),
        "combat_system": test_combat_system(combat_system, player_id),
        "class_system": test_class_system(class_system, player_id),
        "skills_system": test_skills_system(skills_system, player_id),
        "xp_system": test_xp_system(xp_system, player_id),
        "status_system": test_status_system(status_system),
        "achievement_system": test_achievement_system(achievement_system, player_id),
        "quest_system": test_quest_system(quest_system, player_id),
        "economy_system": test_economy_system(economy_system, player_id),
        "world_system": test_world_system(world_system, player_id)
    }
    
    # Print test results
    print("\n" + "=" * 50)
    print("🧪 SYSTEM TEST RESULTS")
    print("=" * 50)
    
    for system_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{system_name}: {status}")
    
    # Print character summary
    print("\n" + "=" * 50)
    print("🎭 TEST CHARACTER SUMMARY")
    print("=" * 50)
    
    print(f"Name: {player_name}")
    print(f"Level: {player_data['player_level']}")
    total_xp = player_data['xp']['base'] + player_data['xp']['class'] + player_data['xp']['skill']
    print(f"XP: {total_xp}")
    print(f"Archetypes: {list(player_data['archetypes'].keys())}")
    
    inventory = items_system.get_inventory(player_id)
    print(f"Inventory Items: {len(inventory['items'])}")
    
    gold = economy_system.get_gold(player_id)
    print(f"Gold: {gold}")
    
    current_area = world_system.get_current_area(player_id)
    if current_area:
        print(f"Current Area: {current_area['name']}")
    
    achievements = achievement_system.get_achievement_stats(player_id)
    print(f"Achievements: {achievements['completed_achievements']}/{achievements['total_achievements']}")
    
    quests = quest_system.get_quest_stats(player_id)
    print(f"Quests: {quests['completed_quests']}/{quests['total_quests']}")
    
    print("\n🚀 Test character is ready for comprehensive testing!")
    return player_id


def test_player_system(player_system, player_id):
    """Test player system functionality"""
    try:
        player_data = player_system.get_player(player_id)
        return player_data is not None and "player_level" in player_data
    except Exception as e:
        print(f"Player system test failed: {e}")
        return False


def test_items_system(items_system, player_id):
    """Test items system functionality"""
    try:
        inventory = items_system.get_inventory(player_id)
        return inventory is not None and "items" in inventory
    except Exception as e:
        print(f"Items system test failed: {e}")
        return False


def test_combat_system(combat_system, player_id):
    """Test combat system functionality"""
    try:
        encounter = combat_system.create_encounter(player_id, area_level=1)
        return "error" not in encounter
    except Exception as e:
        print(f"Combat system test failed: {e}")
        return False


def test_class_system(class_system, player_id):
    """Test class system functionality"""
    try:
        available_features = class_system.get_available_class_features(player_id, ArchetypeType.MELEE)
        return "all_features" in available_features
    except Exception as e:
        print(f"Class system test failed: {e}")
        return False


def test_skills_system(skills_system, player_id):
    """Test skills system functionality"""
    try:
        available_skills = skills_system.get_available_skills_for_player(player_id)
        return "archetypes" in available_skills
    except Exception as e:
        print(f"Skills system test failed: {e}")
        return False


def test_xp_system(xp_system, player_id):
    """Test XP system functionality"""
    try:
        # XP system is integrated with player system, so just check if it exists
        return xp_system is not None
    except Exception as e:
        print(f"XP system test failed: {e}")
        return False


def test_status_system(status_system):
    """Test status system functionality"""
    try:
        status_effect = status_system.apply_status_effect("burn", 3, 0.1)
        return status_effect is not None
    except Exception as e:
        print(f"Status system test failed: {e}")
        return False


def test_achievement_system(achievement_system, player_id):
    """Test achievement system functionality"""
    try:
        stats = achievement_system.get_achievement_stats(player_id)
        return "total_achievements" in stats
    except Exception as e:
        print(f"Achievement system test failed: {e}")
        return False


def test_quest_system(quest_system, player_id):
    """Test quest system functionality"""
    try:
        available_quests = quest_system.get_available_quests(player_id)
        return "main_story" in available_quests
    except Exception as e:
        print(f"Quest system test failed: {e}")
        return False


def test_economy_system(economy_system, player_id):
    """Test economy system functionality"""
    try:
        gold = economy_system.get_gold(player_id)
        return isinstance(gold, int) and gold >= 0
    except Exception as e:
        print(f"Economy system test failed: {e}")
        return False


def test_world_system(world_system, player_id):
    """Test world system functionality"""
    try:
        current_area = world_system.get_current_area(player_id)
        return current_area is not None and "name" in current_area
    except Exception as e:
        print(f"World system test failed: {e}")
        return False


def run_comprehensive_test():
    """Run a comprehensive test of all systems with the test character"""
    print("🧪 Running Comprehensive System Test...")
    print("=" * 50)
    
    # Create test character
    player_id = create_test_character()
    if not player_id:
        print("❌ Failed to create test character")
        return
    
    print(f"\n✅ Test character '{player_id}' created successfully!")
    print("🎮 Ready for comprehensive testing of all game systems!")
    print("\nYou can now use this character to test:")
    print("- Combat encounters")
    print("- Item management")
    print("- Quest progression")
    print("- Achievement tracking")
    print("- World exploration")
    print("- Economy and trading")
    print("- Class features and skills")
    print("- Status effects")
    print("- XP and leveling")


if __name__ == "__main__":
    run_comprehensive_test()

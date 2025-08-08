#!/usr/bin/env python3
"""
Test script for expanded Chapter 1 content
"""

import json
from pathlib import Path

def test_expanded_content():
    """Test the expanded quest and area content"""
    data_dir = Path("chapters/chapter_01_sunderfall/data")
    
    print("Testing expanded Chapter 1 content...")
    print("=" * 50)
    
    # Test quests
    quests_file = data_dir / "quests.json"
    if quests_file.exists():
        with open(quests_file, 'r') as f:
            quests = json.load(f)
        
        print(f"Loaded {len(quests)} quests:")
        
        # Count quests by type
        quest_types = {}
        for quest in quests:
            quest_type = quest.get('quest_type', 'unknown')
            quest_types[quest_type] = quest_types.get(quest_type, 0) + 1
        
        for quest_type, count in quest_types.items():
            print(f"  {quest_type}: {count} quests")
        
        # Show story quest progression
        story_quests = [q for q in quests if q.get('quest_type') == 'QuestType.STORY']
        print(f"\nStory quest progression ({len(story_quests)} quests):")
        for quest in story_quests:
            print(f"  {quest['id']}: {quest['name']} (Level {quest['level_requirement']})")
    
    # Test areas
    areas_file = data_dir / "areas.json"
    if areas_file.exists():
        with open(areas_file, 'r') as f:
            areas = json.load(f)
        
        print(f"\nLoaded {len(areas)} areas:")
        
        # Count areas by type
        area_types = {}
        for area in areas:
            area_type = area.get('area_type', 'unknown')
            area_types[area_type] = area_types.get(area_type, 0) + 1
        
        for area_type, count in area_types.items():
            print(f"  {area_type}: {count} areas")
        
        # Show area connections
        print(f"\nArea connections:")
        for area in areas:
            connections = area.get('connections', [])
            print(f"  {area['id']} -> {connections}")
    
    # Test progression system loading
    print(f"\nTesting progression system...")
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'chapters/chapter_01_sunderfall/src/systems'))
        
        from progression_system import ProgressionSystem
        
        progression = ProgressionSystem(data_dir)
        print(f"  Successfully loaded progression system")
        print(f"  Quests loaded: {len(progression.quests)}")
        print(f"  Areas loaded: {len(progression.areas)}")
        
        # Test quest availability
        test_player_id = "test_player"
        # Initialize a new player
        progress = progression.initialize_player_progress(test_player_id, "pure_dps")
        print(f"  Created player {test_player_id} at level {progress.level}")
        
        available_quests = progression.get_available_quests(test_player_id)
        print(f"  Available quests for new player: {len(available_quests)}")
        for quest in available_quests[:3]:  # Show first 3 quests
            print(f"    - {quest.name} (Level {quest.level_requirement})")
        
        # Test area availability
        available_areas = progression.get_available_areas(test_player_id)
        print(f"  Available areas for new player: {len(available_areas)}")
        for area in available_areas[:3]:  # Show first 3 areas
            print(f"    - {area.name} (Level {area.level_range[0]}-{area.level_range[1]})")
        
    except Exception as e:
        print(f"  Error testing progression system: {e}")
    
    print("\n" + "=" * 50)
    print("Expanded content test completed!")

if __name__ == "__main__":
    test_expanded_content()

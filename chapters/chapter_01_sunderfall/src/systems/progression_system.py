#!/usr/bin/env python3
"""
Progression System for Chronicles of Ruin
Manages AI player progression through Chapter 1 with story-driven content
"""

import json
import random
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from datetime import datetime

class QuestType(Enum):
    """Types of quests in the game"""
    STORY = "story"
    SIDE_QUEST = "side_quest"
    EXPLORATION = "exploration"
    COMBAT = "combat"
    CRAFTING = "crafting"
    SOCIAL = "social"

class QuestStatus(Enum):
    """Quest status tracking"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class AreaType(Enum):
    """Types of areas in the game"""
    TOWN = "town"
    FOREST = "forest"
    CAVE = "cave"
    RUINS = "ruins"
    BOSS_ARENA = "boss_arena"
    WILDERNESS = "wilderness"

@dataclass
class Quest:
    """Individual quest definition"""
    id: str
    name: str
    description: str
    quest_type: QuestType
    level_requirement: int
    objectives: List[Dict[str, Any]]
    rewards: Dict[str, Any]
    story_flags: List[str]
    prerequisites: List[str]
    
    def __post_init__(self):
        if self.objectives is None:
            self.objectives = []
        if self.rewards is None:
            self.rewards = {}
        if self.story_flags is None:
            self.story_flags = []
        if self.prerequisites is None:
            self.prerequisites = []

@dataclass
class Area:
    """Game area definition"""
    id: str
    name: str
    description: str
    area_type: AreaType
    level_range: Tuple[int, int]
    monsters: List[str]
    quests: List[str]
    connections: List[str]
    story_flags_required: List[str]
    
    def __post_init__(self):
        if self.monsters is None:
            self.monsters = []
        if self.quests is None:
            self.quests = []
        if self.connections is None:
            self.connections = []
        if self.story_flags_required is None:
            self.story_flags_required = []

@dataclass
class PlayerProgress:
    """Player progression tracking"""
    player_id: str
    level: int
    experience: int
    story_flags: List[str]
    completed_quests: List[str]
    current_quests: List[str]
    discovered_areas: List[str]
    current_area: str
    inventory: Dict[str, Any]
    skills_learned: List[str]
    achievements: List[str]
    playtime_hours: float
    last_session: datetime
    
    def __post_init__(self):
        if self.story_flags is None:
            self.story_flags = []
        if self.completed_quests is None:
            self.completed_quests = []
        if self.current_quests is None:
            self.current_quests = []
        if self.discovered_areas is None:
            self.discovered_areas = []
        if self.inventory is None:
            self.inventory = {}
        if self.skills_learned is None:
            self.skills_learned = []
        if self.achievements is None:
            self.achievements = []

class ProgressionSystem:
    """Manages AI player progression through Chapter 1"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.quests_file = self.data_dir / "quests.json"
        self.areas_file = self.data_dir / "areas.json"
        self.progress_file = self.data_dir / "player_progress.json"
        
        self.quests: Dict[str, Quest] = {}
        self.areas: Dict[str, Area] = {}
        self.player_progress: Dict[str, PlayerProgress] = {}
        
        # Chapter 1 story progression
        self.chapter_1_story = {
            "intro": "The village of Sunderfall has been plagued by mysterious disappearances...",
            "act_1": "Investigate the forest and discover the source of the corruption",
            "act_2": "Venture into the ancient ruins to find the artifact",
            "act_3": "Confront the corrupted guardian and restore balance",
            "epilogue": "The village is saved, but greater threats loom on the horizon..."
        }
        
        self._load_content()
        self._create_chapter_1_content()
    
    def _load_content(self):
        """Load quests, areas, and player progress"""
        # Load quests
        if self.quests_file.exists():
            try:
                with open(self.quests_file, 'r') as f:
                    quests_data = json.load(f)
                    for quest_data in quests_data:
                        quest = Quest(
                            id=quest_data['id'],
                            name=quest_data['name'],
                            description=quest_data['description'],
                            quest_type=QuestType(quest_data['quest_type']),
                            level_requirement=quest_data['level_requirement'],
                            objectives=quest_data.get('objectives', []),
                            rewards=quest_data.get('rewards', {}),
                            story_flags=quest_data.get('story_flags', []),
                            prerequisites=quest_data.get('prerequisites', [])
                        )
                        self.quests[quest.id] = quest
            except Exception as e:
                print(f"Error loading quests: {e}")
        
        # Load areas
        if self.areas_file.exists():
            try:
                with open(self.areas_file, 'r') as f:
                    areas_data = json.load(f)
                    for area_data in areas_data:
                        area = Area(
                            id=area_data['id'],
                            name=area_data['name'],
                            description=area_data['description'],
                            area_type=AreaType(area_data['area_type']),
                            level_range=tuple(area_data['level_range']),
                            monsters=area_data.get('monsters', []),
                            quests=area_data.get('quests', []),
                            connections=area_data.get('connections', []),
                            story_flags_required=area_data.get('story_flags_required', [])
                        )
                        self.areas[area.id] = area
            except Exception as e:
                print(f"Error loading areas: {e}")
        
        # Load player progress
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r') as f:
                    progress_data = json.load(f)
                    for player_id, player_data in progress_data.items():
                        progress = PlayerProgress(
                            player_id=player_id,
                            level=player_data['level'],
                            experience=player_data['experience'],
                            story_flags=player_data.get('story_flags', []),
                            completed_quests=player_data.get('completed_quests', []),
                            current_quests=player_data.get('current_quests', []),
                            discovered_areas=player_data.get('discovered_areas', []),
                            current_area=player_data.get('current_area', 'sunderfall_village'),
                            inventory=player_data.get('inventory', {}),
                            skills_learned=player_data.get('skills_learned', []),
                            achievements=player_data.get('achievements', []),
                            playtime_hours=player_data.get('playtime_hours', 0.0),
                            last_session=datetime.fromisoformat(player_data.get('last_session', datetime.now().isoformat()))
                        )
                        self.player_progress[player_id] = progress
            except Exception as e:
                print(f"Error loading player progress: {e}")
    
    def _create_chapter_1_content(self):
        """Create Chapter 1 quests and areas if they don't exist"""
        if not self.quests:
            self._create_chapter_1_quests()
        if not self.areas:
            self._create_chapter_1_areas()
    
    def _create_chapter_1_quests(self):
        """Create the main quests for Chapter 1"""
        
        # Act 1: Introduction and Forest Investigation
        self.quests["quest_001"] = Quest(
            id="quest_001",
            name="The Disappearances",
            description="Villagers have been disappearing from Sunderfall. Investigate the recent disappearances and speak with the village elder.",
            quest_type=QuestType.STORY,
            level_requirement=1,
            objectives=[
                {"type": "talk", "target": "village_elder", "description": "Speak with the village elder"},
                {"type": "explore", "target": "sunderfall_village", "description": "Explore the village for clues"},
                {"type": "collect", "target": "disappearance_reports", "count": 3, "description": "Collect reports of disappearances"}
            ],
            rewards={"experience": 100, "gold": 50, "items": ["basic_healing_potion"]},
            story_flags=["met_elder", "discovered_disappearances"],
            prerequisites=[]
        )
        
        self.quests["quest_002"] = Quest(
            id="quest_002",
            name="Into the Forest",
            description="The elder believes the disappearances are linked to the corrupted forest. Venture into the Whispering Woods to investigate.",
            quest_type=QuestType.STORY,
            level_requirement=2,
            objectives=[
                {"type": "explore", "target": "whispering_woods", "description": "Explore the Whispering Woods"},
                {"type": "defeat", "target": "corrupted_wolf", "count": 3, "description": "Defeat corrupted wolves"},
                {"type": "collect", "target": "corruption_sample", "count": 1, "description": "Collect a sample of the corruption"}
            ],
            rewards={"experience": 200, "gold": 100, "items": ["forest_map"]},
            story_flags=["discovered_corruption", "cleared_forest_path"],
            prerequisites=["quest_001"]
        )
        
        # Act 2: Ancient Ruins
        self.quests["quest_003"] = Quest(
            id="quest_003",
            name="The Ancient Ruins",
            description="The corruption leads to ancient ruins beneath the forest. Find the source of the corruption and the missing villagers.",
            quest_type=QuestType.STORY,
            level_requirement=5,
            objectives=[
                {"type": "explore", "target": "ancient_ruins", "description": "Explore the ancient ruins"},
                {"type": "defeat", "target": "corrupted_guardian", "count": 1, "description": "Defeat the corrupted guardian"},
                {"type": "rescue", "target": "missing_villagers", "count": 5, "description": "Rescue the missing villagers"}
            ],
            rewards={"experience": 500, "gold": 250, "items": ["ancient_artifact"]},
            story_flags=["found_villagers", "defeated_guardian"],
            prerequisites=["quest_002"]
        )
        
        # Act 3: Final Confrontation
        self.quests["quest_004"] = Quest(
            id="quest_004",
            name="The Corrupted Heart",
            description="The ancient artifact has been corrupted. Confront the source of corruption and restore balance to Sunderfall.",
            quest_type=QuestType.STORY,
            level_requirement=8,
            objectives=[
                {"type": "explore", "target": "corruption_heart", "description": "Reach the heart of corruption"},
                {"type": "defeat", "target": "corruption_lord", "count": 1, "description": "Defeat the Corruption Lord"},
                {"type": "ritual", "target": "purify_artifact", "description": "Purify the ancient artifact"}
            ],
            rewards={"experience": 1000, "gold": 500, "items": ["purified_artifact", "hero_badge"]},
            story_flags=["defeated_corruption_lord", "purified_artifact", "chapter_1_complete"],
            prerequisites=["quest_003"]
        )
        
        # Side Quests
        self.quests["quest_101"] = Quest(
            id="quest_101",
            name="Herb Gathering",
            description="The village healer needs rare herbs from the forest. Help gather healing herbs.",
            quest_type=QuestType.SIDE_QUEST,
            level_requirement=1,
            objectives=[
                {"type": "collect", "target": "healing_herb", "count": 10, "description": "Gather healing herbs"}
            ],
            rewards={"experience": 50, "gold": 25, "items": ["healing_potion"]},
            story_flags=["helped_healer"],
            prerequisites=[]
        )
        
        self.quests["quest_102"] = Quest(
            id="quest_102",
            name="Lost Equipment",
            description="A merchant lost his equipment in the forest. Help him recover his goods.",
            quest_type=QuestType.SIDE_QUEST,
            level_requirement=3,
            objectives=[
                {"type": "collect", "target": "merchant_goods", "count": 5, "description": "Recover merchant goods"},
                {"type": "return", "target": "merchant", "description": "Return goods to merchant"}
            ],
            rewards={"experience": 150, "gold": 75, "items": ["discount_voucher"]},
            story_flags=["helped_merchant"],
            prerequisites=[]
        )
    
    def _create_chapter_1_areas(self):
        """Create the areas for Chapter 1"""
        
        # Starting Area
        self.areas["sunderfall_village"] = Area(
            id="sunderfall_village",
            name="Sunderfall Village",
            description="A peaceful village nestled in the valley. Recently plagued by mysterious disappearances.",
            area_type=AreaType.TOWN,
            level_range=(1, 10),
            monsters=[],
            quests=["quest_001", "quest_101"],
            connections=["whispering_woods"],
            story_flags_required=[]
        )
        
        # Forest Area
        self.areas["whispering_woods"] = Area(
            id="whispering_woods",
            name="Whispering Woods",
            description="A dense forest with ancient trees. The air feels heavy with corruption.",
            area_type=AreaType.FOREST,
            level_range=(2, 6),
            monsters=["corrupted_wolf", "corrupted_bear", "corrupted_sprite"],
            quests=["quest_002", "quest_102"],
            connections=["sunderfall_village", "ancient_ruins"],
            story_flags_required=["met_elder"]
        )
        
        # Ruins Area
        self.areas["ancient_ruins"] = Area(
            id="ancient_ruins",
            name="Ancient Ruins",
            description="Crumbling ruins of an ancient civilization. The source of the corruption lies within.",
            area_type=AreaType.RUINS,
            level_range=(5, 10),
            monsters=["corrupted_guardian", "corrupted_skeleton", "corrupted_mage"],
            quests=["quest_003"],
            connections=["whispering_woods", "corruption_heart"],
            story_flags_required=["discovered_corruption"]
        )
        
        # Boss Area
        self.areas["corruption_heart"] = Area(
            id="corruption_heart",
            name="Heart of Corruption",
            description="The epicenter of corruption. A massive chamber where the Corruption Lord awaits.",
            area_type=AreaType.BOSS_ARENA,
            level_range=(8, 10),
            monsters=["corruption_lord"],
            quests=["quest_004"],
            connections=["ancient_ruins"],
            story_flags_required=["defeated_guardian"]
        )
    
    def initialize_player_progress(self, player_id: str, archetype: str) -> PlayerProgress:
        """Initialize a new player's progress starting at level 1"""
        progress = PlayerProgress(
            player_id=player_id,
            level=1,
            experience=0,
            story_flags=[],
            completed_quests=[],
            current_quests=["quest_001"],  # Start with the first quest
            discovered_areas=["sunderfall_village"],
            current_area="sunderfall_village",
            inventory={
                "gold": 50,
                "basic_healing_potion": 2,
                "basic_weapon": 1
            },
            skills_learned=["fireball", "healing_light", "stone_skin"],  # Basic skills
            achievements=[],
            playtime_hours=0.0,
            last_session=datetime.now()
        )
        
        self.player_progress[player_id] = progress
        return progress
    
    def get_available_quests(self, player_id: str) -> List[Quest]:
        """Get quests available to a player based on their progress"""
        if player_id not in self.player_progress:
            return []
        
        progress = self.player_progress[player_id]
        available_quests = []
        
        for quest in self.quests.values():
            # Check level requirement
            if quest.level_requirement > progress.level:
                continue
            
            # Check prerequisites
            if quest.prerequisites and not all(prereq in progress.completed_quests for prereq in quest.prerequisites):
                continue
            
            # Check if already completed
            if quest.id in progress.completed_quests:
                continue
            
            available_quests.append(quest)
        
        return available_quests
    
    def get_available_areas(self, player_id: str) -> List[Area]:
        """Get areas available to a player based on their progress"""
        if player_id not in self.player_progress:
            return []
        
        progress = self.player_progress[player_id]
        available_areas = []
        
        for area in self.areas.values():
            # Check level requirement
            if progress.level < area.level_range[0] or progress.level > area.level_range[1]:
                continue
            
            # Check story flags
            if area.story_flags_required and not all(flag in progress.story_flags for flag in area.story_flags_required):
                continue
            
            available_areas.append(area)
        
        return available_areas
    
    def complete_quest(self, player_id: str, quest_id: str) -> Dict[str, Any]:
        """Complete a quest and award rewards"""
        if player_id not in self.player_progress or quest_id not in self.quests:
            return {"success": False, "error": "Invalid player or quest"}
        
        progress = self.player_progress[player_id]
        quest = self.quests[quest_id]
        
        # Check if quest is in progress
        if quest_id not in progress.current_quests:
            return {"success": False, "error": "Quest not in progress"}
        
        # Award rewards
        progress.experience += quest.rewards.get("experience", 0)
        progress.gold = progress.inventory.get("gold", 0) + quest.rewards.get("gold", 0)
        
        # Add items to inventory
        for item in quest.rewards.get("items", []):
            progress.inventory[item] = progress.inventory.get(item, 0) + 1
        
        # Update progress
        progress.completed_quests.append(quest_id)
        progress.current_quests.remove(quest_id)
        progress.story_flags.extend(quest.story_flags)
        
        # Check for level up
        level_up_info = self._check_level_up(progress)
        
        return {
            "success": True,
            "rewards": quest.rewards,
            "story_flags": quest.story_flags,
            "level_up": level_up_info
        }
    
    def _check_level_up(self, progress: PlayerProgress) -> Optional[Dict[str, Any]]:
        """Check if player should level up and return level up info"""
        # Simple level up formula: 100 * level^2 experience per level
        required_exp = progress.level * progress.level * 100
        
        if progress.experience >= required_exp:
            old_level = progress.level
            progress.level += 1
            progress.experience -= required_exp
            
            # Award new skills based on level
            new_skills = self._get_skills_for_level(progress.level)
            progress.skills_learned.extend(new_skills)
            
            return {
                "old_level": old_level,
                "new_level": progress.level,
                "new_skills": new_skills
            }
        
        return None
    
    def _get_skills_for_level(self, level: int) -> List[str]:
        """Get new skills available at a given level"""
        skill_progression = {
            2: ["lightning_strike"],
            3: ["mirror_shield"],
            4: ["group_heal"],
            5: ["shadow_daggers"],
            6: ["evasion"],
            7: ["haste"],
            8: ["apocalypse"],  # Ultimate for pure DPS
            9: ["immortality"], # Ultimate for pure Support
            10: []  # No new skills at level 10
        }
        
        return skill_progression.get(level, [])
    
    def save_progress(self):
        """Save all progress data"""
        try:
            # Save quests
            quests_data = [asdict(quest) for quest in self.quests.values()]
            with open(self.quests_file, 'w') as f:
                json.dump(quests_data, f, indent=2, default=str)
            
            # Save areas
            areas_data = [asdict(area) for area in self.areas.values()]
            with open(self.areas_file, 'w') as f:
                json.dump(areas_data, f, indent=2, default=str)
            
            # Save player progress
            progress_data = {}
            for player_id, progress in self.player_progress.items():
                progress_data[player_id] = asdict(progress)
                progress_data[player_id]['last_session'] = progress.last_session.isoformat()
            
            with open(self.progress_file, 'w') as f:
                json.dump(progress_data, f, indent=2, default=str)
                
        except Exception as e:
            print(f"Error saving progress: {e}")

def main():
    """Test the progression system"""
    progression_system = ProgressionSystem(Path("data"))
    
    print("📚 CHAPTER 1 PROGRESSION SYSTEM")
    print("=" * 50)
    
    # Test player initialization
    player_id = "ai_player_001"
    progress = progression_system.initialize_player_progress(player_id, "pure_dps")
    
    print(f"\n🎮 Player Progress:")
    print(f"  Level: {progress.level}")
    print(f"  Experience: {progress.experience}")
    print(f"  Current Area: {progress.current_area}")
    print(f"  Skills Learned: {len(progress.skills_learned)}")
    print(f"  Current Quests: {len(progress.current_quests)}")
    
    # Test available quests
    available_quests = progression_system.get_available_quests(player_id)
    print(f"\n📋 Available Quests ({len(available_quests)}):")
    for quest in available_quests:
        print(f"  - {quest.name} (Level {quest.level_requirement})")
    
    # Test available areas
    available_areas = progression_system.get_available_areas(player_id)
    print(f"\n🗺️ Available Areas ({len(available_areas)}):")
    for area in available_areas:
        print(f"  - {area.name} (Level {area.level_range[0]}-{area.level_range[1]})")
    
    # Test quest completion
    if available_quests:
        quest = available_quests[0]
        result = progression_system.complete_quest(player_id, quest.id)
        print(f"\n✅ Completed Quest: {quest.name}")
        print(f"  Rewards: {result['rewards']}")
        if result.get('level_up'):
            print(f"  Level Up: {result['level_up']['old_level']} → {result['level_up']['new_level']}")
    
    # Save progress
    progression_system.save_progress()
    print(f"\n💾 Progress saved successfully!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Quest System for Chronicles of Ruin: Sunderfall
Manages story progression, side quests, and repeatable bounties
"""

import json
import os
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime, timedelta


class QuestType(Enum):
    """Types of quests"""
    MAIN_STORY = "main_story"
    SIDE_QUEST = "side_quest"
    BOUNTY = "bounty"
    ACHIEVEMENT = "achievement"


class QuestState(Enum):
    """Quest states"""
    AVAILABLE = "available"
    ACTIVE = "active"
    COMPLETED = "completed"
    TURNED_IN = "turned_in"
    FAILED = "failed"


class QuestObjective:
    """Represents a quest objective"""
    
    def __init__(self, 
                 objective_id: str,
                 description: str,
                 required_count: int,
                 current_count: int = 0,
                 is_optional: bool = False):
        self.objective_id = objective_id
        self.description = description
        self.required_count = required_count
        self.current_count = current_count
        self.is_optional = is_optional
    
    def update_progress(self, amount: int = 1):
        """Update objective progress"""
        self.current_count = min(self.current_count + amount, self.required_count)
    
    def is_complete(self) -> bool:
        """Check if objective is complete"""
        return self.current_count >= self.required_count


class Quest:
    """Represents a single quest"""
    
    def __init__(self,
                 quest_id: str,
                 name: str,
                 description: str,
                 quest_type: QuestType,
                 level_requirement: int,
                 objectives: List[QuestObjective],
                 rewards: Dict[str, Any],
                 time_limit: Optional[timedelta] = None,
                 prerequisites: List[str] = None):
        self.quest_id = quest_id
        self.name = name
        self.description = description
        self.quest_type = quest_type
        self.level_requirement = level_requirement
        self.objectives = objectives
        self.rewards = rewards
        self.time_limit = time_limit
        self.prerequisites = prerequisites or []
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None


class QuestSystem:
    """Manages player quests and progression"""
    
    def __init__(self, player_system=None):
        self.player_system = player_system
        self.quests = {}
        self.player_quests = {}
        self._load_quests()
    
    def _load_quests(self):
        """Load all available quests"""
        # Main Story Quests
        self._add_quest(Quest(
            "the_letter",
            "The Letter",
            "Meet the disguised king and learn about the plague",
            QuestType.MAIN_STORY,
            1,
            [QuestObjective("meet_king", "Meet the disguised king", 1)],
            {"xp": 100, "gold": 50, "item": "letter_from_king"}
        ))
        
        self._add_quest(Quest(
            "first_steps",
            "First Steps", 
            "Clear the first district and prove your worth",
            QuestType.MAIN_STORY,
            1,
            [QuestObjective("clear_district", "Clear the first district", 1)],
            {"xp": 200, "gold": 100, "item": "district_medal"}
        ))
        
        self._add_quest(Quest(
            "the_truth",
            "The Truth",
            "Discover the nature of the plague affecting the village",
            QuestType.MAIN_STORY,
            5,
            [QuestObjective("investigate_plague", "Investigate the plague source", 1)],
            {"xp": 500, "gold": 250, "skill_points": 2}
        ))
        
        # Side Quests
        self._add_quest(Quest(
            "help_villagers",
            "Help the Villagers",
            "Help villagers in distress by defeating monsters",
            QuestType.SIDE_QUEST,
            2,
            [QuestObjective("defeat_monsters", "Defeat 10 monsters", 10)],
            {"xp": 150, "gold": 75}
        ))
        
        self._add_quest(Quest(
            "collect_herbs",
            "Collect Herbs",
            "Gather healing herbs for the village healer",
            QuestType.SIDE_QUEST,
            3,
            [QuestObjective("gather_herbs", "Collect 20 healing herbs", 20)],
            {"xp": 200, "gold": 100, "item": "healing_potion"}
        ))
        
        # Bounty Quests (Repeatable)
        self._add_quest(Quest(
            "monster_bounty",
            "Monster Bounty",
            "Defeat monsters for the local bounty board",
            QuestType.BOUNTY,
            1,
            [QuestObjective("defeat_bounty_monsters", "Defeat 5 monsters", 5)],
            {"xp": 100, "gold": 50},
            time_limit=timedelta(hours=24)
        ))
        
        self._add_quest(Quest(
            "elite_bounty",
            "Elite Bounty",
            "Defeat elite monsters for higher rewards",
            QuestType.BOUNTY,
            5,
            [QuestObjective("defeat_elite_monsters", "Defeat 3 elite monsters", 3)],
            {"xp": 300, "gold": 150},
            time_limit=timedelta(hours=12)
        ))
    
    def _add_quest(self, quest: Quest):
        """Add a quest to the system"""
        self.quests[quest.quest_id] = quest
    
    def get_player_quests(self, player_id: str) -> Dict[str, Any]:
        """Get quest data for a player"""
        if player_id not in self.player_quests:
            self.player_quests[player_id] = {
                "active_quests": {},
                "completed_quests": set(),
                "failed_quests": set(),
                "quest_progress": {},
                "last_updated": datetime.now()
            }
        return self.player_quests[player_id]
    
    def get_available_quests(self, player_id: str) -> Dict[str, Any]:
        """Get all quests available to a player"""
        player_data = self.player_system.get_player(player_id) if self.player_system else {}
        player_quests = self.get_player_quests(player_id)
        
        available = {
            "main_story": [],
            "side_quests": [],
            "bounties": [],
            "achievements": []
        }
        
        for quest_id, quest in self.quests.items():
            # Skip if already completed or failed
            if quest_id in player_quests["completed_quests"]:
                continue
            if quest_id in player_quests["failed_quests"]:
                continue
            
            # Check level requirement
            if player_data.get("player_level", 0) < quest.level_requirement:
                continue
            
            # Check prerequisites
            if not self._check_prerequisites(player_id, quest):
                continue
            
            # Check if quest is active
            if quest_id in player_quests["active_quests"]:
                continue
            
            # Check time limits for bounties
            if quest.quest_type == QuestType.BOUNTY:
                if not self._can_accept_bounty(player_id, quest_id):
                    continue
            
            quest_info = {
                "id": quest_id,
                "name": quest.name,
                "description": quest.description,
                "type": quest.quest_type.value,
                "level_requirement": quest.level_requirement,
                "rewards": quest.rewards,
                "objectives": [obj.description for obj in quest.objectives]
            }
            
            if quest.quest_type == QuestType.MAIN_STORY:
                available["main_story"].append(quest_info)
            elif quest.quest_type == QuestType.SIDE_QUEST:
                available["side_quests"].append(quest_info)
            elif quest.quest_type == QuestType.BOUNTY:
                available["bounties"].append(quest_info)
            elif quest.quest_type == QuestType.ACHIEVEMENT:
                available["achievements"].append(quest_info)
        
        return available
    
    def _check_prerequisites(self, player_id: str, quest: Quest) -> bool:
        """Check if player meets quest prerequisites"""
        player_quests = self.get_player_quests(player_id)
        
        for prereq in quest.prerequisites:
            if prereq not in player_quests["completed_quests"]:
                return False
        
        return True
    
    def _can_accept_bounty(self, player_id: str, quest_id: str) -> bool:
        """Check if player can accept a bounty quest"""
        player_quests = self.get_player_quests(player_id)
        
        # Check if bounty is on cooldown
        if quest_id in player_quests.get("bounty_cooldowns", {}):
            cooldown_time = player_quests["bounty_cooldowns"][quest_id]
            if datetime.now() < cooldown_time:
                return False
        
        return True
    
    def accept_quest(self, player_id: str, quest_id: str) -> Dict[str, Any]:
        """Accept a quest"""
        if quest_id not in self.quests:
            return {"success": False, "error": "Quest not found"}
        
        quest = self.quests[quest_id]
        player_quests = self.get_player_quests(player_id)
        player_data = self.player_system.get_player(player_id) if self.player_system else {}
        
        # Check if already active or completed
        if quest_id in player_quests["active_quests"]:
            return {"success": False, "error": "Quest already active"}
        if quest_id in player_quests["completed_quests"]:
            return {"success": False, "error": "Quest already completed"}
        
        # Check level requirement
        if player_data.get("player_level", 0) < quest.level_requirement:
            return {"success": False, "error": f"Level {quest.level_requirement} required"}
        
        # Check prerequisites
        if not self._check_prerequisites(player_id, quest):
            return {"success": False, "error": "Prerequisites not met"}
        
        # Accept the quest
        player_quests["active_quests"][quest_id] = {
            "quest": quest,
            "objectives": [obj.__dict__.copy() for obj in quest.objectives],
            "started_at": datetime.now(),
            "time_limit": quest.time_limit
        }
        
        print(f"📜 Quest Accepted: {quest.name}")
        print(f"   {quest.description}")
        
        return {"success": True, "quest": quest.name}
    
    def update_quest_progress(self, player_id: str, objective_type: str, amount: int = 1):
        """Update progress for quest objectives"""
        player_quests = self.get_player_quests(player_id)
        
        for quest_id, quest_data in player_quests["active_quests"].items():
            quest = quest_data["quest"]
            
            for objective in quest_data["objectives"]:
                if objective["objective_id"] == objective_type:
                    objective["current_count"] = min(
                        objective["current_count"] + amount, 
                        objective["required_count"]
                    )
                    
                    # Check if quest is complete
                    if self._is_quest_complete(quest_data["objectives"]):
                        self._complete_quest(player_id, quest_id)
    
    def _is_quest_complete(self, objectives: List[Dict]) -> bool:
        """Check if all required objectives are complete"""
        for objective in objectives:
            if not objective["is_optional"] and objective["current_count"] < objective["required_count"]:
                return False
        return True
    
    def _complete_quest(self, player_id: str, quest_id: str):
        """Complete a quest and award rewards"""
        player_quests = self.get_player_quests(player_id)
        quest_data = player_quests["active_quests"][quest_id]
        quest = quest_data["quest"]
        
        # Remove from active quests
        del player_quests["active_quests"][quest_id]
        
        # Add to completed quests
        player_quests["completed_quests"].add(quest_id)
        
        # Apply rewards
        if self.player_system:
            if "xp" in quest.rewards:
                xp_gain = {"base": quest.rewards["xp"]}
                self.player_system.add_xp(player_id, xp_gain)
            
            if "gold" in quest.rewards:
                # Add gold to player (would need gold system integration)
                pass
            
            if "skill_points" in quest.rewards:
                # Add skill points (would need skill system integration)
                pass
        
        # Handle bounty cooldowns
        if quest.quest_type == QuestType.BOUNTY:
            if "bounty_cooldowns" not in player_quests:
                player_quests["bounty_cooldowns"] = {}
            player_quests["bounty_cooldowns"][quest_id] = datetime.now() + quest.time_limit
        
        print(f"🎉 Quest Completed: {quest.name}")
        print(f"   Rewards: {quest.rewards}")
    
    def get_active_quests(self, player_id: str) -> List[Dict[str, Any]]:
        """Get player's active quests"""
        player_quests = self.get_player_quests(player_id)
        active_quests = []
        
        for quest_id, quest_data in player_quests["active_quests"].items():
            quest = quest_data["quest"]
            objectives = quest_data["objectives"]
            
            quest_info = {
                "id": quest_id,
                "name": quest.name,
                "description": quest.description,
                "type": quest.quest_type.value,
                "objectives": []
            }
            
            for objective in objectives:
                quest_info["objectives"].append({
                    "description": objective["description"],
                    "current": objective["current_count"],
                    "required": objective["required_count"],
                    "is_optional": objective["is_optional"],
                    "percentage": min(100, (objective["current_count"] / objective["required_count"]) * 100)
                })
            
            active_quests.append(quest_info)
        
        return active_quests
    
    def get_quest_stats(self, player_id: str) -> Dict[str, Any]:
        """Get quest statistics for a player"""
        player_quests = self.get_player_quests(player_id)
        
        total_quests = len(self.quests)
        completed_quests = len(player_quests["completed_quests"])
        active_quests = len(player_quests["active_quests"])
        failed_quests = len(player_quests["failed_quests"])
        
        type_counts = {quest_type.value: 0 for quest_type in QuestType}
        
        for quest_id in player_quests["completed_quests"]:
            if quest_id in self.quests:
                quest = self.quests[quest_id]
                type_counts[quest.quest_type.value] += 1
        
        return {
            "total_quests": total_quests,
            "completed_quests": completed_quests,
            "active_quests": active_quests,
            "failed_quests": failed_quests,
            "completion_percentage": (completed_quests / total_quests) * 100 if total_quests > 0 else 0,
            "type_breakdown": type_counts
        }

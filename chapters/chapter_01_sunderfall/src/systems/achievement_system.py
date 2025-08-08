#!/usr/bin/env python3
"""
Achievement System for Chronicles of Ruin: Sunderfall
Tracks player accomplishments and provides meaningful rewards
"""

import json
import os
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime, timedelta


class AchievementTier(Enum):
    """Achievement difficulty tiers"""
    BRONZE = "bronze"
    SILVER = "silver" 
    GOLD = "gold"
    PLATINUM = "platinum"


class AchievementCategory(Enum):
    """Categories of achievements"""
    COMBAT = "combat"
    EXPLORATION = "exploration"
    SOCIAL = "social"
    PROGRESSION = "progression"
    COLLECTION = "collection"
    CRAFTING = "crafting"


class Achievement:
    """Represents a single achievement"""
    
    def __init__(self, 
                 achievement_id: str,
                 name: str,
                 description: str,
                 category: AchievementCategory,
                 tier: AchievementTier,
                 requirements: Dict[str, Any],
                 rewards: Dict[str, Any],
                 is_hidden: bool = False):
        self.achievement_id = achievement_id
        self.name = name
        self.description = description
        self.category = category
        self.tier = tier
        self.requirements = requirements
        self.rewards = rewards
        self.is_hidden = is_hidden
        self.created_at = datetime.now()


class AchievementSystem:
    """Manages player achievements and progress tracking"""
    
    def __init__(self, player_system=None):
        self.player_system = player_system
        self.achievements = {}
        self.player_progress = {}
        self._load_achievements()
    
    def _load_achievements(self):
        """Load all available achievements"""
        # Combat Achievements
        self._add_achievement(Achievement(
            "basic_slayer",
            "Basic Slayer",
            "Defeat 100 monsters of any type",
            AchievementCategory.COMBAT,
            AchievementTier.BRONZE,
            {"monsters_defeated": 100},
            {"xp": 500, "gold": 1000}
        ))
        
        self._add_achievement(Achievement(
            "elite_slayer", 
            "Elite Slayer",
            "Defeat 50 elite monsters",
            AchievementCategory.COMBAT,
            AchievementTier.SILVER,
            {"elite_monsters_defeated": 50},
            {"xp": 1000, "gold": 2500, "unique_item": "elite_hunter_badge"}
        ))
        
        self._add_achievement(Achievement(
            "boss_slayer",
            "Boss Slayer", 
            "Defeat 10 unique bosses",
            AchievementCategory.COMBAT,
            AchievementTier.GOLD,
            {"bosses_defeated": 10},
            {"xp": 2500, "gold": 5000, "unique_item": "boss_slayer_crown"}
        ))
        
        # Progression Achievements
        self._add_achievement(Achievement(
            "level_50",
            "Level 50",
            "Reach level 50",
            AchievementCategory.PROGRESSION,
            AchievementTier.SILVER,
            {"player_level": 50},
            {"xp": 1000, "gold": 2000, "skill_points": 5}
        ))
        
        self._add_achievement(Achievement(
            "level_100",
            "Level 100",
            "Reach level 100", 
            AchievementCategory.PROGRESSION,
            AchievementTier.GOLD,
            {"player_level": 100},
            {"xp": 2500, "gold": 5000, "skill_points": 10, "unique_item": "century_mark"}
        ))
        
        # Collection Achievements
        self._add_achievement(Achievement(
            "item_collector",
            "Item Collector",
            "Own 100 different items",
            AchievementCategory.COLLECTION,
            AchievementTier.SILVER,
            {"unique_items_owned": 100},
            {"xp": 1000, "gold": 2000, "unique_item": "collector_satchel"}
        ))
        
        # Hidden Achievements
        self._add_achievement(Achievement(
            "first_blood",
            "First Blood",
            "Defeat your first monster",
            AchievementCategory.COMBAT,
            AchievementTier.BRONZE,
            {"monsters_defeated": 1},
            {"xp": 100, "gold": 50},
            is_hidden=True
        ))
    
    def _add_achievement(self, achievement: Achievement):
        """Add an achievement to the system"""
        self.achievements[achievement.achievement_id] = achievement
    
    def get_player_progress(self, player_id: str) -> Dict[str, Any]:
        """Get achievement progress for a player"""
        if player_id not in self.player_progress:
            self.player_progress[player_id] = {
                "achievements": {},
                "stats": {
                    "monsters_defeated": 0,
                    "elite_monsters_defeated": 0,
                    "bosses_defeated": 0,
                    "unique_items_owned": 0,
                    "total_damage_dealt": 0,
                    "critical_hits": 0,
                    "status_effects_applied": 0,
                    "districts_visited": 0,
                    "guild_level": 0,
                    "trades_completed": 0
                },
                "completed_achievements": set(),
                "last_updated": datetime.now()
            }
        return self.player_progress[player_id]
    
    def update_player_stat(self, player_id: str, stat_name: str, value: int):
        """Update a player's achievement-related stat"""
        progress = self.get_player_progress(player_id)
        progress["stats"][stat_name] = progress["stats"].get(stat_name, 0) + value
        progress["last_updated"] = datetime.now()
        
        # Check for new achievements
        self._check_achievements(player_id)
    
    def _check_achievements(self, player_id: str):
        """Check if player has earned any new achievements"""
        progress = self.get_player_progress(player_id)
        player_data = self.player_system.get_player(player_id) if self.player_system else {}
        
        for achievement_id, achievement in self.achievements.items():
            if achievement_id in progress["completed_achievements"]:
                continue  # Already completed
                
            if self._check_achievement_requirements(achievement, progress, player_data):
                self._award_achievement(player_id, achievement)
    
    def _check_achievement_requirements(self, achievement: Achievement, 
                                     progress: Dict[str, Any], 
                                     player_data: Dict[str, Any]) -> bool:
        """Check if player meets achievement requirements"""
        for req_key, req_value in achievement.requirements.items():
            if req_key == "player_level":
                if player_data.get("player_level", 0) < req_value:
                    return False
            elif req_key in progress["stats"]:
                if progress["stats"][req_key] < req_value:
                    return False
            else:
                return False  # Unknown requirement
        return True
    
    def _award_achievement(self, player_id: str, achievement: Achievement):
        """Award an achievement to a player"""
        progress = self.get_player_progress(player_id)
        progress["completed_achievements"].add(achievement.achievement_id)
        
        # Apply rewards
        if self.player_system:
            if "xp" in achievement.rewards:
                xp_gain = {"base": achievement.rewards["xp"]}
                self.player_system.add_xp(player_id, xp_gain)
            
            if "gold" in achievement.rewards:
                # Add gold to player (would need gold system integration)
                pass
            
            if "skill_points" in achievement.rewards:
                # Add skill points (would need skill system integration)
                pass
        
        # Log achievement completion
        print(f"🎉 Achievement Unlocked: {achievement.name} ({achievement.tier.value})")
        print(f"   {achievement.description}")
    
    def get_available_achievements(self, player_id: str) -> Dict[str, Any]:
        """Get all achievements available to a player"""
        progress = self.get_player_progress(player_id)
        player_data = self.player_system.get_player(player_id) if self.player_system else {}
        
        available = {
            "completed": [],
            "in_progress": [],
            "available": [],
            "hidden": []
        }
        
        for achievement_id, achievement in self.achievements.items():
            if achievement_id in progress["completed_achievements"]:
                available["completed"].append({
                    "id": achievement_id,
                    "name": achievement.name,
                    "description": achievement.description,
                    "category": achievement.category.value,
                    "tier": achievement.tier.value,
                    "rewards": achievement.rewards
                })
            elif self._check_achievement_requirements(achievement, progress, player_data):
                available["available"].append({
                    "id": achievement_id,
                    "name": achievement.name,
                    "description": achievement.description,
                    "category": achievement.category.value,
                    "tier": achievement.tier.value,
                    "rewards": achievement.rewards
                })
            elif achievement.is_hidden:
                available["hidden"].append({
                    "id": achievement_id,
                    "name": "???",
                    "description": "Hidden achievement",
                    "category": achievement.category.value,
                    "tier": achievement.tier.value
                })
            else:
                # Calculate progress
                progress_info = self._calculate_progress(achievement, progress, player_data)
                available["in_progress"].append({
                    "id": achievement_id,
                    "name": achievement.name,
                    "description": achievement.description,
                    "category": achievement.category.value,
                    "tier": achievement.tier.value,
                    "progress": progress_info
                })
        
        return available
    
    def _calculate_progress(self, achievement: Achievement, 
                          progress: Dict[str, Any], 
                          player_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate progress towards an achievement"""
        progress_info = {}
        
        for req_key, req_value in achievement.requirements.items():
            if req_key == "player_level":
                current = player_data.get("player_level", 0)
                progress_info[req_key] = {
                    "current": current,
                    "required": req_value,
                    "percentage": min(100, (current / req_value) * 100)
                }
            elif req_key in progress["stats"]:
                current = progress["stats"][req_key]
                progress_info[req_key] = {
                    "current": current,
                    "required": req_value,
                    "percentage": min(100, (current / req_value) * 100)
                }
        
        return progress_info
    
    def get_achievement_stats(self, player_id: str) -> Dict[str, Any]:
        """Get achievement statistics for a player"""
        progress = self.get_player_progress(player_id)
        
        total_achievements = len(self.achievements)
        completed_achievements = len(progress["completed_achievements"])
        
        tier_counts = {tier.value: 0 for tier in AchievementTier}
        category_counts = {cat.value: 0 for cat in AchievementCategory}
        
        for achievement_id in progress["completed_achievements"]:
            if achievement_id in self.achievements:
                achievement = self.achievements[achievement_id]
                tier_counts[achievement.tier.value] += 1
                category_counts[achievement.category.value] += 1
        
        return {
            "total_achievements": total_achievements,
            "completed_achievements": completed_achievements,
            "completion_percentage": (completed_achievements / total_achievements) * 100 if total_achievements > 0 else 0,
            "tier_breakdown": tier_counts,
            "category_breakdown": category_counts,
            "stats": progress["stats"]
        }

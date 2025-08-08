#!/usr/bin/env python3
"""
Procedural Quest Generation System
Dynamically creates quests based on player progress and AI performance data
"""

import sys
import json
import time
import random
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass

# Add project paths
sys.path.append(str(Path(__file__).parent.parent))

class QuestType(Enum):
    STORY = "story"
    SIDE_QUEST = "side_quest"
    EXPLORATION = "exploration"
    COMBAT = "combat"
    CRAFTING = "crafting"
    SOCIAL = "social"
    GAMBLING = "gambling"  # New type for gambling-related quests
    COLLECTION = "collection"
    ESCORT = "escort"
    SURVIVAL = "survival"

class QuestDifficulty(Enum):
    TRIVIAL = "trivial"
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"
    EXTREME = "extreme"

@dataclass
class QuestTemplate:
    """Template for generating procedural quests"""
    name_pattern: str
    description_pattern: str
    quest_type: QuestType
    base_difficulty: QuestDifficulty
    objectives: List[Dict[str, Any]]
    rewards: Dict[str, Any]
    prerequisites: List[str]
    area_requirements: List[str]
    min_level: int
    max_level: int
    variables: Dict[str, List[str]]  # Randomizable elements

@dataclass
class GeneratedQuest:
    """A dynamically generated quest"""
    id: str
    name: str
    description: str
    quest_type: QuestType
    difficulty: QuestDifficulty
    objectives: List[Dict[str, Any]]
    rewards: Dict[str, Any]
    prerequisites: List[str]
    area_requirements: List[str]
    level_requirement: int
    estimated_duration: int  # minutes
    generation_timestamp: float
    ai_tested: bool = False
    success_rate: float = 0.0
    player_feedback: List[str] = None

class ProceduralQuestGenerator:
    """Main class for generating procedural quests"""
    
    def __init__(self):
        self.templates = self._load_quest_templates()
        self.generated_quests = {}
        self.quest_history = []
        self.player_preferences = {}
        self.ai_performance_data = {}
        
    def _load_quest_templates(self) -> Dict[str, QuestTemplate]:
        """Load quest templates from configuration"""
        templates = {
            "gambling_addiction": QuestTemplate(
                name_pattern="The {adjective} Gambler's {noun}",
                description_pattern="Help {npc_name} who has become addicted to rerolling their {item_type}. They've spent {gold_amount} gold and need assistance breaking the cycle.",
                quest_type=QuestType.GAMBLING,
                base_difficulty=QuestDifficulty.NORMAL,
                objectives=[
                    {"type": "talk_to_npc", "target": "{npc_name}", "count": 1},
                    {"type": "witness_gambling", "target": "set_reroll", "count": 3},
                    {"type": "intervention", "target": "gambling_intervention", "count": 1},
                    {"type": "provide_counseling", "target": "{npc_name}", "count": 1}
                ],
                rewards={"gold": 500, "experience": 200, "reputation": 10},
                prerequisites=["unlocked_gambling", "met_npc_{npc_name}"],
                area_requirements=["sunderfall_village", "gambling_district"],
                min_level=5,
                max_level=15,
                variables={
                    "adjective": ["Desperate", "Compulsive", "Unlucky", "Obsessed"],
                    "noun": ["Downfall", "Curse", "Addiction", "Problem"],
                    "npc_name": ["Marcus", "Elena", "Viktor", "Sarah"],
                    "item_type": ["Fire Lord's Regalia", "Mystic Wisdom Set", "Battle Gear"],
                    "gold_amount": ["50,000", "100,000", "200,000", "500,000"]
                }
            ),
            
            "set_creation_mentor": QuestTemplate(
                name_pattern="Master of {craft_type}",
                description_pattern="Learn the art of creating custom item sets from {master_name}, a legendary {profession}. Create your first {set_type} set with at least {piece_count} pieces.",
                quest_type=QuestType.CRAFTING,
                base_difficulty=QuestDifficulty.EASY,
                objectives=[
                    {"type": "talk_to_npc", "target": "{master_name}", "count": 1},
                    {"type": "gather_items", "target": "any_equipment", "count": "{piece_count}"},
                    {"type": "create_set", "target": "custom_set", "count": 1},
                    {"type": "demonstrate_set", "target": "{master_name}", "count": 1}
                ],
                rewards={"gold": 1000, "experience": 500, "set_creation_bonus": 0.1},
                prerequisites=["reached_level_3"],
                area_requirements=["sunderfall_village"],
                min_level=3,
                max_level=10,
                variables={
                    "craft_type": ["Set Creation", "Item Bonding", "Equipment Mastery"],
                    "master_name": ["Forge Master Torin", "Enchanter Lyra", "Artificer Grix"],
                    "profession": ["blacksmith", "enchanter", "artificer"],
                    "set_type": ["Combat", "Magic", "Defense", "Utility"],
                    "piece_count": ["4", "5", "6"]
                }
            ),
            
            "resistance_research": QuestTemplate(
                name_pattern="Understanding {damage_type} Resistance",
                description_pattern="Study the resistance patterns of {monster_type} creatures in {area_name}. Discover their weaknesses and document your findings for future adventurers.",
                quest_type=QuestType.EXPLORATION,
                base_difficulty=QuestDifficulty.NORMAL,
                objectives=[
                    {"type": "defeat_monsters", "target": "{monster_type}", "count": 10},
                    {"type": "test_damage_types", "target": "various_elements", "count": 5},
                    {"type": "document_findings", "target": "resistance_journal", "count": 1},
                    {"type": "report_to_scholar", "target": "Scholar Miren", "count": 1}
                ],
                rewards={"gold": 750, "experience": 400, "resistance_knowledge": True},
                prerequisites=["unlocked_area_{area_name}"],
                area_requirements=["{area_name}"],
                min_level=6,
                max_level=20,
                variables={
                    "damage_type": ["Fire", "Ice", "Lightning", "Poison", "Physical"],
                    "monster_type": ["corrupted_wolves", "forest_sprites", "ancient_guardians"],
                    "area_name": ["whispering_woods", "corrupted_grove", "ancient_ruins"]
                }
            ),
            
            "ai_learning_challenge": QuestTemplate(
                name_pattern="The {skill_type} Challenge",
                description_pattern="Test your skills against AI-controlled opponents in {challenge_area}. Adapt your strategy as they learn from your tactics and become more challenging.",
                quest_type=QuestType.COMBAT,
                base_difficulty=QuestDifficulty.HARD,
                objectives=[
                    {"type": "defeat_ai_opponents", "target": "ai_party", "count": 5},
                    {"type": "survive_adaptive_combat", "target": "learning_ai", "duration": 300},
                    {"type": "demonstrate_mastery", "target": "combat_skills", "count": 1}
                ],
                rewards={"gold": 2000, "experience": 1000, "ai_knowledge": True},
                prerequisites=["completed_basic_training"],
                area_requirements=["training_grounds", "{challenge_area}"],
                min_level=10,
                max_level=25,
                variables={
                    "skill_type": ["Combat", "Strategy", "Adaptation"],
                    "challenge_area": ["arena_district", "training_grounds", "combat_hall"]
                }
            ),
            
            "dynamic_difficulty_test": QuestTemplate(
                name_pattern="Proving Grounds: {trial_name}",
                description_pattern="Enter the adaptive proving grounds where the difficulty scales with your performance. Maintain a {success_rate}% success rate for {trial_duration} minutes.",
                quest_type=QuestType.SURVIVAL,
                base_difficulty=QuestDifficulty.EXTREME,
                objectives=[
                    {"type": "enter_proving_grounds", "target": "adaptive_arena", "count": 1},
                    {"type": "maintain_performance", "target": "success_rate_{success_rate}", "duration": "{trial_duration}"},
                    {"type": "survive_escalation", "target": "final_wave", "count": 1}
                ],
                rewards={"gold": 5000, "experience": 2500, "mastery_token": 1},
                prerequisites=["reached_level_15", "completed_ai_challenge"],
                area_requirements=["proving_grounds"],
                min_level=15,
                max_level=30,
                variables={
                    "trial_name": ["Endurance", "Mastery", "Adaptation"],
                    "success_rate": ["70", "80", "90"],
                    "trial_duration": ["10", "15", "20"]
                }
            )
        }
        
        return templates
    
    def generate_quest(self, player_level: int, player_preferences: Dict[str, Any] = None, 
                      ai_performance_data: Dict[str, Any] = None) -> GeneratedQuest:
        """Generate a new quest based on player data and AI performance"""
        
        # Filter templates by level and preferences
        suitable_templates = self._filter_templates_by_level(player_level)
        
        if player_preferences:
            suitable_templates = self._filter_by_preferences(suitable_templates, player_preferences)
        
        if ai_performance_data:
            suitable_templates = self._adjust_for_ai_performance(suitable_templates, ai_performance_data)
        
        # Select template
        template_name = random.choice(list(suitable_templates.keys()))
        template = suitable_templates[template_name]
        
        # Generate quest from template
        quest = self._generate_from_template(template, player_level)
        
        # Store and return
        self.generated_quests[quest.id] = quest
        self.quest_history.append(quest.id)
        
        return quest
    
    def _filter_templates_by_level(self, player_level: int) -> Dict[str, QuestTemplate]:
        """Filter templates that are appropriate for player level"""
        suitable = {}
        for name, template in self.templates.items():
            if template.min_level <= player_level <= template.max_level:
                suitable[name] = template
        return suitable
    
    def _filter_by_preferences(self, templates: Dict[str, QuestTemplate], 
                             preferences: Dict[str, Any]) -> Dict[str, QuestTemplate]:
        """Filter templates based on player preferences"""
        if "preferred_quest_types" in preferences:
            preferred_types = preferences["preferred_quest_types"]
            filtered = {}
            for name, template in templates.items():
                if template.quest_type.value in preferred_types:
                    filtered[name] = template
            return filtered if filtered else templates
        
        return templates
    
    def _adjust_for_ai_performance(self, templates: Dict[str, QuestTemplate], 
                                 ai_data: Dict[str, Any]) -> Dict[str, QuestTemplate]:
        """Adjust quest difficulty based on AI performance metrics"""
        player_success_rate = ai_data.get("success_rate", 0.5)
        
        # If player is performing well, include harder quests
        if player_success_rate > 0.8:
            # Prioritize hard and extreme quests
            hard_quests = {name: t for name, t in templates.items() 
                          if t.base_difficulty in [QuestDifficulty.HARD, QuestDifficulty.EXTREME]}
            if hard_quests:
                return hard_quests
        
        # If player is struggling, prioritize easier quests
        elif player_success_rate < 0.4:
            easy_quests = {name: t for name, t in templates.items() 
                          if t.base_difficulty in [QuestDifficulty.TRIVIAL, QuestDifficulty.EASY]}
            if easy_quests:
                return easy_quests
        
        return templates
    
    def _generate_from_template(self, template: QuestTemplate, player_level: int) -> GeneratedQuest:
        """Generate a specific quest from a template"""
        
        # Substitute variables
        variables = {}
        for var_name, options in template.variables.items():
            variables[var_name] = random.choice(options)
        
        # Generate quest details
        quest_id = f"proc_{template.quest_type.value}_{int(time.time())}_{random.randint(1000, 9999)}"
        
        name = self._substitute_variables(template.name_pattern, variables)
        description = self._substitute_variables(template.description_pattern, variables)
        
        # Process objectives
        objectives = []
        for obj_template in template.objectives:
            obj = {}
            for key, value in obj_template.items():
                if isinstance(value, str):
                    obj[key] = self._substitute_variables(value, variables)
                else:
                    obj[key] = value
            objectives.append(obj)
        
        # Adjust difficulty based on level
        difficulty = self._calculate_difficulty(template.base_difficulty, player_level, 
                                              template.min_level, template.max_level)
        
        # Calculate rewards based on difficulty and level
        rewards = self._calculate_rewards(template.rewards, difficulty, player_level)
        
        # Process prerequisites and area requirements
        prerequisites = [self._substitute_variables(pre, variables) for pre in template.prerequisites]
        area_requirements = [self._substitute_variables(area, variables) for area in template.area_requirements]
        
        # Estimate duration
        duration = self._estimate_duration(template.quest_type, difficulty, len(objectives))
        
        return GeneratedQuest(
            id=quest_id,
            name=name,
            description=description,
            quest_type=template.quest_type,
            difficulty=difficulty,
            objectives=objectives,
            rewards=rewards,
            prerequisites=prerequisites,
            area_requirements=area_requirements,
            level_requirement=max(template.min_level, player_level - 3),
            estimated_duration=duration,
            generation_timestamp=time.time(),
            player_feedback=[]
        )
    
    def _substitute_variables(self, text: str, variables: Dict[str, str]) -> str:
        """Substitute variables in text patterns"""
        result = text
        for var_name, value in variables.items():
            result = result.replace(f"{{{var_name}}}", value)
        return result
    
    def _calculate_difficulty(self, base_difficulty: QuestDifficulty, player_level: int,
                            min_level: int, max_level: int) -> QuestDifficulty:
        """Calculate actual difficulty based on player level relative to quest range"""
        
        level_progress = (player_level - min_level) / (max_level - min_level)
        level_progress = max(0.0, min(1.0, level_progress))
        
        difficulties = list(QuestDifficulty)
        base_index = difficulties.index(base_difficulty)
        
        # Adjust difficulty based on where player is in the level range
        if level_progress < 0.3:  # Player is at low end of range
            adjustment = -1
        elif level_progress > 0.7:  # Player is at high end of range
            adjustment = 1
        else:
            adjustment = 0
        
        new_index = max(0, min(len(difficulties) - 1, base_index + adjustment))
        return difficulties[new_index]
    
    def _calculate_rewards(self, base_rewards: Dict[str, Any], difficulty: QuestDifficulty, 
                         player_level: int) -> Dict[str, Any]:
        """Calculate actual rewards based on difficulty and level"""
        
        # Difficulty multipliers
        difficulty_multipliers = {
            QuestDifficulty.TRIVIAL: 0.5,
            QuestDifficulty.EASY: 0.8,
            QuestDifficulty.NORMAL: 1.0,
            QuestDifficulty.HARD: 1.5,
            QuestDifficulty.EXTREME: 2.5
        }
        
        multiplier = difficulty_multipliers[difficulty]
        level_multiplier = 1 + (player_level - 1) * 0.1  # 10% increase per level
        
        rewards = {}
        for reward_type, base_value in base_rewards.items():
            if isinstance(base_value, (int, float)):
                rewards[reward_type] = int(base_value * multiplier * level_multiplier)
            else:
                rewards[reward_type] = base_value
        
        return rewards
    
    def _estimate_duration(self, quest_type: QuestType, difficulty: QuestDifficulty, 
                         objective_count: int) -> int:
        """Estimate quest completion time in minutes"""
        
        base_times = {
            QuestType.STORY: 20,
            QuestType.SIDE_QUEST: 15,
            QuestType.EXPLORATION: 25,
            QuestType.COMBAT: 10,
            QuestType.CRAFTING: 12,
            QuestType.SOCIAL: 8,
            QuestType.GAMBLING: 5,
            QuestType.COLLECTION: 18,
            QuestType.ESCORT: 22,
            QuestType.SURVIVAL: 30
        }
        
        difficulty_multipliers = {
            QuestDifficulty.TRIVIAL: 0.5,
            QuestDifficulty.EASY: 0.8,
            QuestDifficulty.NORMAL: 1.0,
            QuestDifficulty.HARD: 1.5,
            QuestDifficulty.EXTREME: 2.0
        }
        
        base_time = base_times[quest_type]
        difficulty_mult = difficulty_multipliers[difficulty]
        objective_mult = 1 + (objective_count - 1) * 0.2
        
        return int(base_time * difficulty_mult * objective_mult)
    
    def test_quest_with_ai(self, quest_id: str, ai_player_name: str) -> Dict[str, Any]:
        """Test a generated quest with an AI player"""
        
        if quest_id not in self.generated_quests:
            return {"error": "Quest not found"}
        
        quest = self.generated_quests[quest_id]
        
        # Simulate AI testing the quest
        test_results = {
            "quest_id": quest_id,
            "ai_player": ai_player_name,
            "test_timestamp": time.time(),
            "objectives_completed": 0,
            "completion_time": 0,
            "difficulty_rating": "unknown",
            "enjoyment_score": 0.0,
            "issues_found": [],
            "suggestions": []
        }
        
        # Simulate objective completion based on quest difficulty
        success_probability = {
            QuestDifficulty.TRIVIAL: 0.95,
            QuestDifficulty.EASY: 0.85,
            QuestDifficulty.NORMAL: 0.70,
            QuestDifficulty.HARD: 0.55,
            QuestDifficulty.EXTREME: 0.40
        }[quest.difficulty]
        
        objectives_completed = 0
        for i, objective in enumerate(quest.objectives):
            if random.random() < success_probability:
                objectives_completed += 1
            else:
                test_results["issues_found"].append(f"Objective {i+1} too difficult: {objective}")
                break
        
        test_results["objectives_completed"] = objectives_completed
        test_results["completion_time"] = random.randint(
            int(quest.estimated_duration * 0.8), 
            int(quest.estimated_duration * 1.5)
        )
        
        # Calculate success rate and update quest
        success_rate = objectives_completed / len(quest.objectives)
        quest.success_rate = success_rate
        quest.ai_tested = True
        
        # Generate AI feedback
        if success_rate > 0.8:
            test_results["difficulty_rating"] = "appropriate"
            test_results["enjoyment_score"] = random.uniform(0.7, 1.0)
        elif success_rate > 0.5:
            test_results["difficulty_rating"] = "challenging"
            test_results["enjoyment_score"] = random.uniform(0.5, 0.8)
        else:
            test_results["difficulty_rating"] = "too_hard"
            test_results["enjoyment_score"] = random.uniform(0.2, 0.5)
            test_results["suggestions"].append("Reduce objective difficulty or provide better hints")
        
        return test_results
    
    def generate_quest_batch(self, count: int, player_level: int, 
                           preferences: Dict[str, Any] = None) -> List[GeneratedQuest]:
        """Generate multiple quests for variety"""
        
        quests = []
        for _ in range(count):
            quest = self.generate_quest(player_level, preferences)
            quests.append(quest)
        
        return quests
    
    def save_quests(self, filename: str = "procedural_quests.json"):
        """Save generated quests to file"""
        
        quest_data = {
            "generation_timestamp": time.time(),
            "quests": {},
            "statistics": {
                "total_generated": len(self.generated_quests),
                "by_type": {},
                "by_difficulty": {},
                "average_success_rate": 0.0
            }
        }
        
        # Convert quests to JSON-serializable format
        for quest_id, quest in self.generated_quests.items():
            quest_data["quests"][quest_id] = {
                "id": quest.id,
                "name": quest.name,
                "description": quest.description,
                "quest_type": quest.quest_type.value,
                "difficulty": quest.difficulty.value,
                "objectives": quest.objectives,
                "rewards": quest.rewards,
                "prerequisites": quest.prerequisites,
                "area_requirements": quest.area_requirements,
                "level_requirement": quest.level_requirement,
                "estimated_duration": quest.estimated_duration,
                "generation_timestamp": quest.generation_timestamp,
                "ai_tested": quest.ai_tested,
                "success_rate": quest.success_rate,
                "player_feedback": quest.player_feedback or []
            }
        
        # Calculate statistics
        quest_types = {}
        difficulties = {}
        success_rates = []
        
        for quest in self.generated_quests.values():
            # Count by type
            quest_type = quest.quest_type.value
            quest_types[quest_type] = quest_types.get(quest_type, 0) + 1
            
            # Count by difficulty
            difficulty = quest.difficulty.value
            difficulties[difficulty] = difficulties.get(difficulty, 0) + 1
            
            # Track success rates
            if quest.ai_tested:
                success_rates.append(quest.success_rate)
        
        quest_data["statistics"]["by_type"] = quest_types
        quest_data["statistics"]["by_difficulty"] = difficulties
        quest_data["statistics"]["average_success_rate"] = sum(success_rates) / len(success_rates) if success_rates else 0.0
        
        # Save to file
        with open(filename, 'w') as f:
            json.dump(quest_data, f, indent=2)
        
        return filename

def main():
    """Test the procedural quest generation system"""
    print("🎯 PROCEDURAL QUEST GENERATION TEST")
    print("=" * 50)
    
    generator = ProceduralQuestGenerator()
    
    # Test quest generation for different player levels
    test_levels = [3, 8, 15, 22]
    all_quests = []
    
    for level in test_levels:
        print(f"\n🎲 Generating quests for level {level} player...")
        
        # Generate a variety of quests
        quests = generator.generate_quest_batch(3, level)
        all_quests.extend(quests)
        
        for quest in quests:
            print(f"  📝 {quest.name}")
            print(f"     Type: {quest.quest_type.value} | Difficulty: {quest.difficulty.value}")
            print(f"     Level: {quest.level_requirement} | Duration: {quest.estimated_duration}m")
            print(f"     Rewards: {quest.rewards}")
            
            # Test quest with AI
            print(f"     🤖 Testing with AI...")
            test_result = generator.test_quest_with_ai(quest.id, "TestAI")
            success_rate = test_result["objectives_completed"] / len(quest.objectives)
            print(f"     Success: {success_rate:.0%} | Rating: {test_result['difficulty_rating']}")
    
    # Save all generated quests
    filename = generator.save_quests()
    print(f"\n💾 Saved {len(all_quests)} quests to {filename}")
    
    # Generate summary
    quest_types = {}
    difficulties = {}
    for quest in all_quests:
        quest_types[quest.quest_type.value] = quest_types.get(quest.quest_type.value, 0) + 1
        difficulties[quest.difficulty.value] = difficulties.get(quest.difficulty.value, 0) + 1
    
    print("\n📊 GENERATION SUMMARY:")
    print(f"Total Quests: {len(all_quests)}")
    print(f"By Type: {dict(quest_types)}")
    print(f"By Difficulty: {dict(difficulties)}")
    
    tested_quests = [q for q in all_quests if q.ai_tested]
    if tested_quests:
        avg_success = sum(q.success_rate for q in tested_quests) / len(tested_quests)
        print(f"Average AI Success Rate: {avg_success:.2%}")
    
    print("\n🎉 Procedural quest generation test completed!")
    
    return True

if __name__ == "__main__":
    main()

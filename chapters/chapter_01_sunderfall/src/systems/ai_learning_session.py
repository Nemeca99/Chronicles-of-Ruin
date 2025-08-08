#!/usr/bin/env python3
"""
AI Learning Session System for Chronicles of Ruin
Orchestrates comprehensive AI learning sessions with expanded Chapter 1 content
"""

import json
import random
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime, timedelta

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from chapters.chapter_01_sunderfall.src.systems.progression_system import ProgressionSystem, PlayerProgress, Quest, Area
from chapters.chapter_01_sunderfall.src.systems.resistance_system import ResistanceSystem, ResistanceProfile, EntityType, ResistanceType
from tools.ai_player_system import AIPlayerSystem

@dataclass
class GameSession:
    """Comprehensive game session data for AI learning"""
    player_id: str
    session_start: datetime
    session_end: datetime
    player_level: int
    current_area: str
    quests_completed: List[str]
    quests_failed: List[str]
    areas_explored: List[str]
    encounters_fought: List[Dict[str, Any]]
    boss_encounters: List[Dict[str, Any]]
    skills_used: List[str]
    damage_dealt: float
    damage_taken: float
    healing_done: float
    experience_gained: int
    items_collected: List[str]
    story_flags_earned: List[str]
    performance_score: float
    learning_insights: List[str]
    decisions_made: List[Dict[str, Any]]
    adaptation_notes: List[str]

class AILearningSession:
    """Orchestrates AI learning sessions with expanded Chapter 1 content"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.ai_system = AIPlayerSystem(Path(__file__).parent.parent.parent.parent.parent)
        self.progression_system = ProgressionSystem(data_dir)
        self.resistance_system = ResistanceSystem()
        
        # Session parameters
        self.session_duration_minutes = 30
        self.encounters_per_session = 8
        self.quest_completion_chance = 0.7
        self.boss_encounter_chance = 0.2
        self.exploration_chance = 0.6
        
        # Initialize game content
        self._initialize_game_content()
    
    def _initialize_game_content(self):
        """Initialize resistance profiles for expanded content"""
        # Regular monsters
        self.monster_profiles = {
            "corrupted_wolf": self.resistance_system.create_resistance_profile(
                EntityType.REGULAR_MONSTER,
                custom_resistances={ResistanceType.PHYSICAL: 20.0, ResistanceType.POISON: 50.0}
            ),
            "corrupted_bear": self.resistance_system.create_resistance_profile(
                EntityType.REGULAR_MONSTER,
                custom_resistances={ResistanceType.PHYSICAL: 40.0, ResistanceType.FIRE: 30.0}
            ),
            "corrupted_sprite": self.resistance_system.create_resistance_profile(
                EntityType.REGULAR_MONSTER,
                custom_resistances={ResistanceType.LIGHTNING: 60.0, ResistanceType.ICE: 30.0}
            ),
            "corrupted_treant": self.resistance_system.create_resistance_profile(
                EntityType.REGULAR_MONSTER,
                custom_resistances={ResistanceType.PHYSICAL: 60.0, ResistanceType.FIRE: -20.0}
            ),
            "corrupted_skeleton": self.resistance_system.create_resistance_profile(
                EntityType.REGULAR_MONSTER,
                custom_resistances={ResistanceType.PHYSICAL: 30.0, ResistanceType.POISON: 80.0}
            ),
            "corrupted_mage": self.resistance_system.create_resistance_profile(
                EntityType.REGULAR_MONSTER,
                custom_resistances={ResistanceType.FIRE: 40.0, ResistanceType.LIGHTNING: 40.0}
            ),
            "corrupted_guardian": self.resistance_system.create_resistance_profile(
                EntityType.REGULAR_MONSTER,
                custom_resistances={ResistanceType.PHYSICAL: 50.0, ResistanceType.FIRE: 30.0, ResistanceType.ICE: 30.0}
            ),
            "giant_rat": self.resistance_system.create_resistance_profile(
                EntityType.REGULAR_MONSTER,
                custom_resistances={ResistanceType.PHYSICAL: 10.0}
            ),
            "crop_pest": self.resistance_system.create_resistance_profile(
                EntityType.REGULAR_MONSTER,
                custom_resistances={ResistanceType.PHYSICAL: 5.0, ResistanceType.POISON: 70.0}
            ),
            "forest_threat": self.resistance_system.create_resistance_profile(
                EntityType.REGULAR_MONSTER,
                custom_resistances={ResistanceType.PHYSICAL: 25.0, ResistanceType.POISON: 40.0}
            )
        }
        
        # Boss monsters
        self.boss_profiles = {
            "corruption_lord": self.resistance_system.create_resistance_profile(
                EntityType.BOSS,
                custom_resistances={ResistanceType.PHYSICAL: 60.0, ResistanceType.FIRE: 40.0, ResistanceType.ICE: 40.0, ResistanceType.LIGHTNING: 40.0},
                immunities=[ResistanceType.STUN, ResistanceType.FREEZE, ResistanceType.POISON],
                vulnerabilities=[]
            ),
            "ancient_guardian": self.resistance_system.create_resistance_profile(
                EntityType.BOSS,
                custom_resistances={ResistanceType.PHYSICAL: 80.0, ResistanceType.FIRE: 20.0, ResistanceType.ICE: 60.0},
                immunities=[ResistanceType.STUN, ResistanceType.FREEZE],
                vulnerabilities=[ResistanceType.FIRE]
            ),
            "corrupted_heart": self.resistance_system.create_resistance_profile(
                EntityType.BOSS,
                custom_resistances={ResistanceType.PHYSICAL: 50.0, ResistanceType.FIRE: 30.0, ResistanceType.ICE: 30.0, ResistanceType.LIGHTNING: 30.0, ResistanceType.POISON: 90.0},
                immunities=[ResistanceType.STUN, ResistanceType.FREEZE, ResistanceType.POISON],
                vulnerabilities=[]
            )
        }
    
    def start_learning_session(self, player_id: str, archetype: str = "pure_dps") -> GameSession:
        """Start a new learning session for an AI player"""
        # Initialize or load player progress
        if player_id not in self.progression_system.player_progress:
            progress = self.progression_system.initialize_player_progress(player_id, archetype)
        else:
            progress = self.progression_system.player_progress[player_id]
        
        session_start = datetime.now()
        
        # Create session
        session = GameSession(
            player_id=player_id,
            session_start=session_start,
            session_end=session_start,
            player_level=progress.level,
            current_area=progress.current_area,
            quests_completed=[],
            quests_failed=[],
            areas_explored=[],
            encounters_fought=[],
            boss_encounters=[],
            skills_used=[],
            damage_dealt=0.0,
            damage_taken=0.0,
            healing_done=0.0,
            experience_gained=0,
            items_collected=[],
            story_flags_earned=[],
            performance_score=0.0,
            learning_insights=[],
            decisions_made=[],
            adaptation_notes=[]
        )
        
        return session
    
    def simulate_game_session(self, player_id: str, session_minutes: int = 30) -> Dict[str, Any]:
        """Simulate a comprehensive game session for AI learning"""
        session = self.start_learning_session(player_id)
        progress = self.progression_system.player_progress[player_id]
        
        # Simulate session activities
        for _ in range(self.encounters_per_session):
            # Randomly choose activity type
            activity_type = random.choices(
                ['combat', 'quest', 'exploration', 'boss'],
                weights=[0.4, 0.3, 0.2, 0.1]
            )[0]
            
            if activity_type == 'combat':
                encounter_data = self._simulate_encounter(session, progress)
                session.encounters_fought.append(encounter_data)
                
            elif activity_type == 'quest':
                quest_data = self._simulate_quest_activity(session, progress)
                if quest_data:
                    if quest_data['completed']:
                        session.quests_completed.append(quest_data['quest_id'])
                    else:
                        session.quests_failed.append(quest_data['quest_id'])
                        
            elif activity_type == 'exploration':
                exploration_data = self._simulate_exploration(session, progress)
                session.areas_explored.extend(exploration_data['areas'])
                session.story_flags_earned.extend(exploration_data['flags'])
                
            elif activity_type == 'boss':
                boss_data = self._simulate_boss_encounter(session, progress)
                session.boss_encounters.append(boss_data)
        
        # Calculate session performance
        session.performance_score = self._calculate_session_performance(session)
        session.learning_insights = self._generate_learning_insights(session)
        session.session_end = datetime.now()
        
        # Update AI player learning
        self._update_ai_player_learning(player_id, session)
        
        return asdict(session)
    
    def _simulate_encounter(self, session: GameSession, progress: PlayerProgress) -> Dict[str, Any]:
        """Simulate a regular combat encounter"""
        # Get available monsters for current area
        current_area = self.progression_system.areas.get(progress.current_area)
        if not current_area or not current_area.monsters:
            return {"type": "no_encounter", "result": "no_monsters"}
        
        monster_type = random.choice(current_area.monsters)
        monster_profile = self.monster_profiles.get(monster_type)
        
        if not monster_profile:
            return {"type": "no_encounter", "result": "no_profile"}
        
        # Simulate combat
        base_damage = random.uniform(10, 30) + (progress.level * 2)
        damage_dealt = self.resistance_system.calculate_damage_with_resistance(
            base_damage, ResistanceType.PHYSICAL, monster_profile
        )
        
        # AI decision making
        ai_decision = self._simulate_ai_decision("combat", {
            "monster_type": monster_type,
            "monster_resistances": monster_profile.resistances,
            "player_level": progress.level,
            "available_skills": progress.skills_learned
        })
        
        # Update session metrics
        session.damage_dealt += damage_dealt
        session.damage_taken += random.uniform(5, 15)
        session.skills_used.extend(ai_decision.get('skills_used', []))
        session.decisions_made.append(ai_decision)
        
        return {
            "type": "combat",
            "monster_type": monster_type,
            "damage_dealt": damage_dealt,
            "damage_taken": session.damage_taken,
            "ai_decision": ai_decision,
            "result": "victory" if damage_dealt > 15 else "defeat"
        }
    
    def _simulate_boss_encounter(self, session: GameSession, progress: PlayerProgress) -> Dict[str, Any]:
        """Simulate a boss encounter with special mechanics"""
        boss_type = "corruption_lord"
        boss_profile = self.boss_profiles.get(boss_type)
        
        if not boss_profile:
            return {"type": "no_boss", "result": "no_profile"}
        
        # Boss-specific mechanics
        base_damage = random.uniform(20, 50) + (progress.level * 3)
        damage_dealt = self.resistance_system.calculate_damage_with_resistance(
            base_damage, ResistanceType.PHYSICAL, boss_profile
        )
        
        # Check status effect immunities
        can_stun = self.resistance_system.can_apply_status_effect(ResistanceType.STUN, boss_profile)
        can_freeze = self.resistance_system.can_apply_status_effect(ResistanceType.FREEZE, boss_profile)
        can_slow = self.resistance_system.can_apply_status_effect(ResistanceType.SLOW, boss_profile)
        
        # AI decision making for boss
        ai_decision = self._simulate_ai_decision("boss_combat", {
            "boss_type": boss_type,
            "boss_immunities": boss_profile.immunities,
            "can_stun": can_stun,
            "can_freeze": can_freeze,
            "can_slow": can_slow,
            "player_level": progress.level,
            "available_skills": progress.skills_learned
        })
        
        # Update session metrics
        session.damage_dealt += damage_dealt
        session.damage_taken += random.uniform(15, 35)
        session.skills_used.extend(ai_decision.get('skills_used', []))
        session.decisions_made.append(ai_decision)
        
        return {
            "type": "boss_combat",
            "boss_type": boss_type,
            "damage_dealt": damage_dealt,
            "damage_taken": session.damage_taken,
            "ai_decision": ai_decision,
            "boss_immunities": boss_profile.immunities,
            "result": "victory" if damage_dealt > 30 else "defeat"
        }
    
    def _simulate_quest_activity(self, session: GameSession, progress: PlayerProgress) -> Optional[Dict[str, Any]]:
        """Simulate quest completion or failure"""
        available_quests = self.progression_system.get_available_quests(progress.player_id)
        
        if not available_quests:
            return None
        
        quest = random.choice(available_quests)
        completion_chance = self.quest_completion_chance
        
        # Adjust based on quest type and player level
        if quest.quest_type.value == "story":
            completion_chance += 0.1
        elif quest.quest_type.value == "side_quest":
            completion_chance -= 0.1
        
        if progress.level >= quest.level_requirement:
            completion_chance += 0.2
        else:
            completion_chance -= 0.3
        
        completed = random.random() < completion_chance
        
        # AI decision making for quest
        ai_decision = self._simulate_ai_decision("quest", {
            "quest_type": quest.quest_type.value,
            "quest_level": quest.level_requirement,
            "player_level": progress.level,
            "objectives": quest.objectives
        })
        
        session.decisions_made.append(ai_decision)
        
        if completed:
            # Complete quest
            quest_result = self.progression_system.complete_quest(progress.player_id, quest.id)
            session.experience_gained += quest.rewards.get('experience', 0)
            session.items_collected.extend(quest.rewards.get('items', []))
            session.story_flags_earned.extend(quest.story_flags)
            
            return {
                "quest_id": quest.id,
                "quest_type": quest.quest_type.value,
                "completed": True,
                "rewards": quest.rewards,
                "ai_decision": ai_decision
            }
        else:
            return {
                "quest_id": quest.id,
                "quest_type": quest.quest_type.value,
                "completed": False,
                "ai_decision": ai_decision
            }
    
    def _simulate_exploration(self, session: GameSession, progress: PlayerProgress) -> Dict[str, Any]:
        """Simulate area exploration"""
        available_areas = self.progression_system.get_available_areas(progress.player_id)
        
        if not available_areas:
            return {"areas": [], "flags": []}
        
        # Choose areas to explore
        areas_to_explore = random.sample(
            available_areas, 
            min(2, len(available_areas))
        )
        
        explored_areas = []
        story_flags = []
        
        for area in areas_to_explore:
            if area.id not in progress.discovered_areas:
                progress.discovered_areas.append(area.id)
                explored_areas.append(area.id)
                
                # Generate exploration-based story flags
                if area.area_type.value == "forest":
                    story_flags.append(f"explored_{area.id}")
                elif area.area_type.value == "ruins":
                    story_flags.append(f"discovered_{area.id}")
                elif area.area_type.value == "boss_arena":
                    story_flags.append(f"found_{area.id}")
        
        # AI decision making for exploration
        ai_decision = self._simulate_ai_decision("exploration", {
            "areas_available": [area.id for area in available_areas],
            "areas_explored": explored_areas,
            "player_level": progress.level
        })
        
        session.decisions_made.append(ai_decision)
        
        return {
            "areas": explored_areas,
            "flags": story_flags,
            "ai_decision": ai_decision
        }
    
    def _simulate_ai_decision(self, context: str, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate AI decision making for various contexts"""
        # This would integrate with the actual AI player system
        # For now, simulate basic decision making
        
        decision = {
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "game_state": game_state,
            "decision_type": "simulated",
            "confidence": random.uniform(0.5, 0.9),
            "reasoning": f"AI made decision in {context} context",
            "skills_used": [],
            "adaptation_notes": []
        }
        
        # Add context-specific logic
        if context == "combat":
            decision["skills_used"] = random.sample(["fireball", "lightning_strike", "healing_light"], 2)
            decision["reasoning"] = "Chose offensive skills for combat efficiency"
            
        elif context == "boss_combat":
            decision["skills_used"] = ["apocalypse", "stone_skin", "healing_light"]
            decision["reasoning"] = "Used ultimate skill and defensive abilities for boss fight"
            
        elif context == "quest":
            decision["reasoning"] = f"Attempted quest with {game_state.get('quest_type', 'unknown')} type"
            
        elif context == "exploration":
            decision["reasoning"] = f"Explored {len(game_state.get('areas_explored', []))} new areas"
        
        return decision
    
    def _calculate_session_performance(self, session: GameSession) -> float:
        """Calculate overall session performance score"""
        score = 0.0
        
        # Combat performance
        if session.damage_dealt > 0:
            combat_ratio = session.damage_dealt / (session.damage_taken + 1)
            score += min(combat_ratio * 20, 40)
        
        # Quest completion
        quest_success_rate = len(session.quests_completed) / (len(session.quests_completed) + len(session.quests_failed) + 1)
        score += quest_success_rate * 25
        
        # Exploration
        score += len(session.areas_explored) * 5
        
        # Boss encounters
        boss_success_rate = sum(1 for boss in session.boss_encounters if boss.get('result') == 'victory') / max(len(session.boss_encounters), 1)
        score += boss_success_rate * 20
        
        # Experience gained
        score += min(session.experience_gained / 100, 15)
        
        return min(score, 100.0)
    
    def _generate_learning_insights(self, session: GameSession) -> List[str]:
        """Generate learning insights from session data"""
        insights = []
        
        # Combat insights
        if session.damage_dealt > session.damage_taken:
            insights.append("Effective damage dealing strategy")
        else:
            insights.append("Need to improve defensive tactics")
        
        # Quest insights
        if len(session.quests_completed) > len(session.quests_failed):
            insights.append("Good quest completion rate")
        else:
            insights.append("Need to focus on quest objectives")
        
        # Boss insights
        if session.boss_encounters:
            boss_victories = sum(1 for boss in session.boss_encounters if boss.get('result') == 'victory')
            if boss_victories > 0:
                insights.append("Successfully adapted to boss mechanics")
            else:
                insights.append("Need to improve boss fight strategies")
        
        # Exploration insights
        if session.areas_explored:
            insights.append("Good exploration and discovery")
        
        # Skill usage insights
        if session.skills_used:
            unique_skills = len(set(session.skills_used))
            if unique_skills >= 3:
                insights.append("Good skill variety and adaptation")
            else:
                insights.append("Could use more skill variety")
        
        return insights
    
    def _update_ai_player_learning(self, player_id: str, session: GameSession) -> None:
        """Update AI player's learning data from session"""
        # Convert session data to format expected by AI player system
        session_data = {
            "damage_dealt": session.damage_dealt,
            "damage_taken": session.damage_taken,
            "healing_done": session.healing_done,
            "experience_gained": session.experience_gained,
            "quests_completed": len(session.quests_completed),
            "quests_failed": len(session.quests_failed),
            "areas_explored": len(session.areas_explored),
            "boss_encounters": len(session.boss_encounters),
            "boss_victories": sum(1 for boss in session.boss_encounters if boss.get('result') == 'victory'),
            "performance_score": session.performance_score,
            "skills_used": session.skills_used,
            "decisions_made": session.decisions_made,
            "learning_insights": session.learning_insights
        }
        
        # Update AI player learning
        if hasattr(self.ai_system, 'learn_from_game_session'):
            self.ai_system.learn_from_game_session(player_id, session_data)
    
    def run_learning_campaign(self, player_id: str, sessions: int = 5) -> Dict[str, Any]:
        """Run multiple learning sessions to simulate a campaign"""
        campaign_results = {
            "player_id": player_id,
            "total_sessions": sessions,
            "sessions": [],
            "overall_performance": 0.0,
            "learning_progress": [],
            "campaign_insights": []
        }
        
        for session_num in range(sessions):
            print(f"Running learning session {session_num + 1}/{sessions} for player {player_id}")
            
            session_result = self.simulate_game_session(player_id)
            campaign_results["sessions"].append(session_result)
            
            # Track learning progress
            campaign_results["learning_progress"].append({
                "session": session_num + 1,
                "performance": session_result["performance_score"],
                "experience_gained": session_result["experience_gained"],
                "quests_completed": len(session_result["quests_completed"])
            })
        
        # Calculate overall campaign performance
        if campaign_results["sessions"]:
            campaign_results["overall_performance"] = sum(
                session["performance_score"] for session in campaign_results["sessions"]
            ) / len(campaign_results["sessions"])
        
        # Generate campaign insights
        campaign_results["campaign_insights"] = self._generate_campaign_insights(campaign_results)
        
        return campaign_results
    
    def _generate_campaign_insights(self, campaign_results: Dict[str, Any]) -> List[str]:
        """Generate high-level insights from the entire campaign"""
        insights = []
        
        # Performance trends
        performances = [session["performance_score"] for session in campaign_results["sessions"]]
        if len(performances) > 1:
            if performances[-1] > performances[0]:
                insights.append("Player showed improvement over campaign")
            else:
                insights.append("Player performance remained consistent")
        
        # Quest completion analysis
        total_quests = sum(len(session["quests_completed"]) for session in campaign_results["sessions"])
        if total_quests > 0:
            insights.append(f"Completed {total_quests} quests during campaign")
        
        # Boss encounter analysis
        total_boss_encounters = sum(len(session["boss_encounters"]) for session in campaign_results["sessions"])
        if total_boss_encounters > 0:
            insights.append(f"Fought {total_boss_encounters} boss encounters")
        
        # Exploration analysis
        total_exploration = sum(len(session["areas_explored"]) for session in campaign_results["sessions"])
        if total_exploration > 0:
            insights.append(f"Explored {total_exploration} new areas")
        
        return insights

def main():
    """Test the AI learning session system"""
    data_dir = Path("chapters/chapter_01_sunderfall/data")
    learning_system = AILearningSession(data_dir)
    
    # Test a single session
    print("Testing AI learning session...")
    session_result = learning_system.simulate_game_session("test_player_001")
    
    print(f"Session completed for player {session_result['player_id']}")
    print(f"Performance score: {session_result['performance_score']:.2f}")
    print(f"Experience gained: {session_result['experience_gained']}")
    print(f"Quests completed: {len(session_result['quests_completed'])}")
    print(f"Areas explored: {len(session_result['areas_explored'])}")
    print(f"Boss encounters: {len(session_result['boss_encounters'])}")
    print(f"Learning insights: {session_result['learning_insights']}")
    
    # Test a learning campaign
    print("\nTesting learning campaign...")
    campaign_result = learning_system.run_learning_campaign("test_player_002", sessions=3)
    
    print(f"Campaign completed for player {campaign_result['player_id']}")
    print(f"Overall performance: {campaign_result['overall_performance']:.2f}")
    print(f"Campaign insights: {campaign_result['campaign_insights']}")

if __name__ == "__main__":
    main()

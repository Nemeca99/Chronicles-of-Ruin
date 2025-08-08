#!/usr/bin/env python3
"""
AI Learning Session System
Integrates progression, resistance, and skills systems for realistic AI learning
"""

import json
import random
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime

from ai_player_system import AIPLAYERSystem, PlayerProfile
from progression_system import ProgressionSystem
from resistance_system import ResistanceSystem, EntityType, ResistanceType

@dataclass
class GameSession:
    """Complete game session data for AI learning"""
    session_id: str
    player_id: str
    start_time: datetime
    end_time: Optional[datetime]
    player_level: int
    current_area: str
    quests_completed: List[str]
    areas_explored: List[str]
    encounters_fought: List[Dict[str, Any]]
    boss_encounters: List[Dict[str, Any]]
    skills_used: List[str]
    damage_dealt: float
    damage_taken: float
    healing_done: float
    status_effects_applied: int
    experience_gained: int
    decisions_made: int
    successful_decisions: int
    performance_score: float
    learning_insights: List[str]
    
    def __post_init__(self):
        if self.quests_completed is None:
            self.quests_completed = []
        if self.areas_explored is None:
            self.areas_explored = []
        if self.encounters_fought is None:
            self.encounters_fought = []
        if self.boss_encounters is None:
            self.boss_encounters = []
        if self.skills_used is None:
            self.skills_used = []
        if self.learning_insights is None:
            self.learning_insights = []

class AILearningSession:
    """Manages comprehensive AI learning sessions with full game integration"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.ai_system = AIPLAYERSystem(self.base_dir)
        self.progression_system = ProgressionSystem(self.base_dir / "chapters" / "chapter_01_sunderfall" / "data")
        self.resistance_system = ResistanceSystem()
        
        # Session tracking
        self.active_sessions: Dict[str, GameSession] = {}
        self.session_history: List[GameSession] = []
        
        # Learning configuration
        self.session_duration_minutes = 30
        self.encounters_per_session = 5
        self.quest_completion_chance = 0.3
        self.boss_encounter_chance = 0.1
        
        # Initialize content
        self._initialize_game_content()
    
    def _initialize_game_content(self):
        """Initialize game content for AI learning"""
        # Create sample monsters and bosses
        self.monsters = {
            "corrupted_wolf": self.resistance_system.create_monster_profile(
                "Corrupted Wolf",
                custom_resistances={
                    ResistanceType.PHYSICAL: -10.0,
                    ResistanceType.FIRE: 25.0
                }
            )[1],
            "corrupted_bear": self.resistance_system.create_monster_profile(
                "Corrupted Bear",
                custom_resistances={
                    ResistanceType.PHYSICAL: 30.0,
                    ResistanceType.ICE: -15.0
                }
            )[1],
            "corrupted_guardian": self.resistance_system.create_boss_profile(
                "Corrupted Guardian",
                custom_resistances={
                    ResistanceType.PHYSICAL: 50.0,
                    ResistanceType.LIGHTNING: -25.0
                },
                vulnerabilities=[ResistanceType.LIGHTNING]
            )[1],
            "corruption_lord": self.resistance_system.create_boss_profile(
                "Corruption Lord",
                custom_resistances={
                    ResistanceType.FIRE: 75.0,
                    ResistanceType.ICE: -25.0,
                    ResistanceType.PHYSICAL: 60.0
                },
                vulnerabilities=[ResistanceType.ICE]
            )[1]
        }
    
    def start_learning_session(self, player_id: str, archetype: str = "pure_dps") -> GameSession:
        """Start a new learning session for an AI player"""
        # Initialize or get player progress
        if player_id not in self.progression_system.player_progress:
            self.progression_system.initialize_player_progress(player_id, archetype)
        
        progress = self.progression_system.player_progress[player_id]
        
        # Create session
        session = GameSession(
            session_id=f"session_{int(time.time())}",
            player_id=player_id,
            start_time=datetime.now(),
            end_time=None,
            player_level=progress.level,
            current_area=progress.current_area,
            quests_completed=[],
            areas_explored=[],
            encounters_fought=[],
            boss_encounters=[],
            skills_used=progress.skills_learned.copy(),
            damage_dealt=0.0,
            damage_taken=0.0,
            healing_done=0.0,
            status_effects_applied=0,
            experience_gained=0,
            decisions_made=0,
            successful_decisions=0,
            performance_score=0.0,
            learning_insights=[]
        )
        
        self.active_sessions[player_id] = session
        return session
    
    def simulate_game_session(self, player_id: str, session_minutes: int = 30) -> Dict[str, Any]:
        """Simulate a complete game session for AI learning"""
        session = self.start_learning_session(player_id)
        progress = self.progression_system.player_progress[player_id]
        
        print(f"🎮 Starting AI Learning Session for {player_id}")
        print(f"   Level: {progress.level}")
        print(f"   Current Area: {progress.current_area}")
        print(f"   Skills Available: {len(progress.skills_learned)}")
        
        # Simulate encounters
        for encounter_num in range(self.encounters_per_session):
            encounter_result = self._simulate_encounter(session, progress)
            session.encounters_fought.append(encounter_result)
            
            # Update session metrics
            session.damage_dealt += encounter_result.get("damage_dealt", 0)
            session.damage_taken += encounter_result.get("damage_taken", 0)
            session.healing_done += encounter_result.get("healing_done", 0)
            session.status_effects_applied += encounter_result.get("status_effects_applied", 0)
            session.decisions_made += encounter_result.get("decisions_made", 0)
            session.successful_decisions += encounter_result.get("successful_decisions", 0)
            
            # Check for boss encounter
            if random.random() < self.boss_encounter_chance:
                boss_result = self._simulate_boss_encounter(session, progress)
                session.boss_encounters.append(boss_result)
        
        # Simulate quest completion
        available_quests = self.progression_system.get_available_quests(player_id)
        for quest in available_quests:
            if random.random() < self.quest_completion_chance:
                quest_result = self._simulate_quest_completion(session, progress, quest)
                session.quests_completed.append(quest.id)
                session.experience_gained += quest.rewards.get("experience", 0)
        
        # Simulate area exploration
        available_areas = self.progression_system.get_available_areas(player_id)
        for area in available_areas:
            if random.random() < 0.4:  # 40% chance to explore new area
                session.areas_explored.append(area.id)
        
        # Calculate performance score
        session.performance_score = self._calculate_session_performance(session)
        
        # Generate learning insights
        session.learning_insights = self._generate_learning_insights(session)
        
        # End session
        session.end_time = datetime.now()
        self.active_sessions.pop(player_id, None)
        self.session_history.append(session)
        
        # Update AI player learning
        self._update_ai_player_learning(player_id, session)
        
        return asdict(session)
    
    def _simulate_encounter(self, session: GameSession, progress: Any) -> Dict[str, Any]:
        """Simulate a combat encounter"""
        # Select random monster based on current area
        monster_name = random.choice(list(self.monsters.keys()))
        monster_profile = self.monsters[monster_name]
        
        # Determine if it's a boss encounter
        is_boss = monster_profile.entity_type == EntityType.BOSS
        
        # Simulate combat
        base_damage = random.uniform(50, 150)
        monster_damage = random.uniform(30, 100)
        
        # Apply resistance calculations
        damage_dealt = self.resistance_system.calculate_damage_with_resistance(
            base_damage, ResistanceType.PHYSICAL, monster_profile
        )
        
        damage_taken = self.resistance_system.calculate_damage_with_resistance(
            monster_damage, ResistanceType.PHYSICAL, 
            self.resistance_system.default_profiles[EntityType.PLAYER]
        )
        
        # Simulate skill usage
        skills_used = random.sample(progress.skills_learned, min(3, len(progress.skills_learned)))
        healing_done = sum(random.uniform(20, 80) for _ in range(len([s for s in skills_used if "heal" in s])))
        
        # Simulate status effects
        status_effects_applied = 0
        if not is_boss:  # Regular monsters can be affected by status effects
            status_effects_applied = random.randint(0, 2)
        
        # Determine success
        success = damage_dealt > damage_taken
        decisions_made = random.randint(3, 8)
        successful_decisions = decisions_made if success else random.randint(1, decisions_made - 1)
        
        return {
            "monster_name": monster_name,
            "is_boss": is_boss,
            "damage_dealt": damage_dealt,
            "damage_taken": damage_taken,
            "healing_done": healing_done,
            "status_effects_applied": status_effects_applied,
            "skills_used": skills_used,
            "success": success,
            "decisions_made": decisions_made,
            "successful_decisions": successful_decisions
        }
    
    def _simulate_boss_encounter(self, session: GameSession, progress: Any) -> Dict[str, Any]:
        """Simulate a boss encounter with special mechanics"""
        # Select boss monster
        boss_name = random.choice([name for name, profile in self.monsters.items() 
                                 if profile.entity_type == EntityType.BOSS])
        boss_profile = self.monsters[boss_name]
        
        # Boss encounters are more challenging
        base_damage = random.uniform(80, 200)
        boss_damage = random.uniform(60, 150)
        
        # Apply boss resistance calculations
        damage_dealt = self.resistance_system.calculate_damage_with_resistance(
            base_damage, ResistanceType.PHYSICAL, boss_profile
        )
        
        damage_taken = self.resistance_system.calculate_damage_with_resistance(
            boss_damage, ResistanceType.PHYSICAL,
            self.resistance_system.default_profiles[EntityType.PLAYER]
        )
        
        # Bosses are immune to certain status effects
        status_effects_applied = 0  # Bosses are immune to stun/freeze
        if boss_profile.resistances.get(ResistanceType.SLOW, 0) < 100:
            status_effects_applied = random.randint(0, 1)  # Can be slowed
        
        # More skill usage in boss fights
        skills_used = random.sample(progress.skills_learned, min(5, len(progress.skills_learned)))
        healing_done = sum(random.uniform(40, 120) for _ in range(len([s for s in skills_used if "heal" in s])))
        
        # Boss fights require more decisions
        decisions_made = random.randint(8, 15)
        success = damage_dealt > damage_taken * 1.2  # Bosses are harder to defeat
        successful_decisions = decisions_made if success else random.randint(3, decisions_made - 2)
        
        return {
            "boss_name": boss_name,
            "damage_dealt": damage_dealt,
            "damage_taken": damage_taken,
            "healing_done": healing_done,
            "status_effects_applied": status_effects_applied,
            "skills_used": skills_used,
            "success": success,
            "decisions_made": decisions_made,
            "successful_decisions": successful_decisions,
            "boss_immunities": [immunity.value for immunity in boss_profile.immunities],
            "boss_vulnerabilities": [vuln.value for vuln in boss_profile.vulnerabilities]
        }
    
    def _simulate_quest_completion(self, session: GameSession, progress: Any, quest: Any) -> Dict[str, Any]:
        """Simulate quest completion"""
        return {
            "quest_id": quest.id,
            "quest_name": quest.name,
            "completion_time": random.randint(5, 15),  # minutes
            "areas_visited": random.sample(session.areas_explored, min(2, len(session.areas_explored))),
            "rewards": quest.rewards,
            "story_flags": quest.story_flags
        }
    
    def _calculate_session_performance(self, session: GameSession) -> float:
        """Calculate overall session performance score"""
        if session.damage_taken == 0:
            damage_ratio = 1.0
        else:
            damage_ratio = session.damage_dealt / session.damage_taken
        
        healing_efficiency = session.healing_done / max(session.damage_taken, 1)
        quest_completion_rate = len(session.quests_completed) / max(len(session.quests_completed) + 1, 1)
        exploration_rate = len(session.areas_explored) / max(len(session.areas_explored) + 1, 1)
        decision_success_rate = session.successful_decisions / max(session.decisions_made, 1)
        
        # Weighted performance score
        performance_score = (
            damage_ratio * 0.3 +
            healing_efficiency * 0.2 +
            quest_completion_rate * 0.25 +
            exploration_rate * 0.15 +
            decision_success_rate * 0.1
        )
        
        return min(1.0, max(0.0, performance_score))
    
    def _generate_learning_insights(self, session: GameSession) -> List[str]:
        """Generate learning insights from the session"""
        insights = []
        
        # Combat insights
        if session.damage_dealt > session.damage_taken:
            insights.append("Effective damage dealing strategy")
        else:
            insights.append("Need to improve damage mitigation")
        
        if session.healing_done > 0:
            insights.append("Successfully utilized healing abilities")
        
        if session.status_effects_applied > 0:
            insights.append("Effectively applied status effects")
        
        # Boss encounter insights
        if session.boss_encounters:
            boss_successes = sum(1 for boss in session.boss_encounters if boss["success"])
            if boss_successes > 0:
                insights.append("Successfully adapted to boss mechanics")
            else:
                insights.append("Need to improve boss fight strategies")
        
        # Quest progression insights
        if session.quests_completed:
            insights.append("Made good quest progression")
        
        # Exploration insights
        if session.areas_explored:
            insights.append("Explored new areas effectively")
        
        return insights
    
    def _update_ai_player_learning(self, player_id: str, session: GameSession) -> None:
        """Update AI player learning based on session results"""
        if player_id in self.ai_system.ai_player_profiles:
            player_profile = self.ai_system.ai_player_profiles[player_id]
            
            # Convert session to learning data
            session_data = {
                "damage_dealt": session.damage_dealt,
                "damage_taken": session.damage_taken,
                "healing_done": session.healing_done,
                "status_effects_applied": session.status_effects_applied,
                "boss_encounters": len(session.boss_encounters),
                "bosses_defeated": sum(1 for boss in session.boss_encounters if boss["success"]),
                "quests_completed": len(session.quests_completed),
                "areas_explored": len(session.areas_explored),
                "experience_gained": session.experience_gained,
                "decisions_made": session.decisions_made,
                "successful_decisions": session.successful_decisions,
                "performance_score": session.performance_score,
                "boss_data": {boss["boss_name"]: boss for boss in session.boss_encounters},
                "quest_data": {quest: {"completion_time": 10} for quest in session.quests_completed}
            }
            
            # Update AI player learning
            player_profile.learn_from_game_session(session_data)
    
    def run_learning_campaign(self, player_id: str, sessions: int = 5) -> Dict[str, Any]:
        """Run multiple learning sessions for comprehensive AI development"""
        campaign_results = {
            "player_id": player_id,
            "total_sessions": sessions,
            "sessions": [],
            "overall_performance": 0.0,
            "learning_progress": {},
            "final_insights": []
        }
        
        print(f"🚀 Starting Learning Campaign for {player_id}")
        print(f"   Sessions: {sessions}")
        print("=" * 50)
        
        for session_num in range(sessions):
            print(f"\n📊 Session {session_num + 1}/{sessions}")
            session_result = self.simulate_game_session(player_id)
            campaign_results["sessions"].append(session_result)
            
            print(f"   Performance Score: {session_result['performance_score']:.2f}")
            print(f"   Damage Dealt: {session_result['damage_dealt']:.1f}")
            print(f"   Damage Taken: {session_result['damage_taken']:.1f}")
            print(f"   Healing Done: {session_result['healing_done']:.1f}")
            print(f"   Quests Completed: {len(session_result['quests_completed'])}")
            print(f"   Boss Encounters: {len(session_result['boss_encounters'])}")
        
        # Calculate overall performance
        performance_scores = [s["performance_score"] for s in campaign_results["sessions"]]
        campaign_results["overall_performance"] = sum(performance_scores) / len(performance_scores)
        
        # Analyze learning progress
        if player_id in self.ai_system.ai_player_profiles:
            player_profile = self.ai_system.ai_player_profiles[player_id]
            campaign_results["learning_progress"] = {
                "success_rate": player_profile.get_success_rate(),
                "games_played": player_profile.games_played,
                "experience_points": player_profile.experience_points,
                "strategy_memory_size": len(player_profile.strategy_memory),
                "failure_patterns_size": len(player_profile.failure_patterns)
            }
        
        # Generate final insights
        campaign_results["final_insights"] = self._generate_campaign_insights(campaign_results)
        
        print(f"\n🎯 Campaign Complete!")
        print(f"   Overall Performance: {campaign_results['overall_performance']:.2f}")
        print(f"   Learning Progress: {campaign_results['learning_progress']}")
        
        return campaign_results
    
    def _generate_campaign_insights(self, campaign_results: Dict[str, Any]) -> List[str]:
        """Generate insights from the entire campaign"""
        insights = []
        
        # Performance analysis
        avg_performance = campaign_results["overall_performance"]
        if avg_performance > 0.8:
            insights.append("Excellent overall performance")
        elif avg_performance > 0.6:
            insights.append("Good performance with room for improvement")
        else:
            insights.append("Needs significant improvement")
        
        # Learning progress analysis
        learning_progress = campaign_results["learning_progress"]
        if learning_progress.get("success_rate", 0) > 0.7:
            insights.append("High success rate in decision making")
        
        if learning_progress.get("strategy_memory_size", 0) > 5:
            insights.append("Successfully learned multiple strategies")
        
        return insights

def main():
    """Test the AI learning session system"""
    learning_system = AILearningSession(Path("."))
    
    print("🧠 AI LEARNING SESSION SYSTEM")
    print("=" * 50)
    
    # Test single session
    player_id = "ai_learner_001"
    session_result = learning_system.simulate_game_session(player_id)
    
    print(f"\n📊 Session Results:")
    print(f"  Performance Score: {session_result['performance_score']:.2f}")
    print(f"  Damage Dealt: {session_result['damage_dealt']:.1f}")
    print(f"  Damage Taken: {session_result['damage_taken']:.1f}")
    print(f"  Healing Done: {session_result['healing_done']:.1f}")
    print(f"  Quests Completed: {len(session_result['quests_completed'])}")
    print(f"  Boss Encounters: {len(session_result['boss_encounters'])}")
    print(f"  Learning Insights: {session_result['learning_insights']}")
    
    # Test learning campaign
    campaign_result = learning_system.run_learning_campaign(player_id, sessions=3)
    
    print(f"\n🎯 Campaign Results:")
    print(f"  Overall Performance: {campaign_result['overall_performance']:.2f}")
    print(f"  Learning Progress: {campaign_result['learning_progress']}")
    print(f"  Final Insights: {campaign_result['final_insights']}")

if __name__ == "__main__":
    main()

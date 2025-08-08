#!/usr/bin/env python3
"""
AI Player System for Chronicles of Ruin
Simulates human player behavior using Ollama for testing and development
"""

import os
import sys
import json
import requests
import time
import random
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any, Union
from enum import Enum
import logging

# Add the tools directory to the path
sys.path.append(str(Path(__file__).parent))

class PlayerActionType(Enum):
    """Types of player actions"""
    CHARACTER_CREATION = "character_creation"
    COMBAT_DECISION = "combat_decision"
    SKILL_ALLOCATION = "skill_allocation"
    EXPLORATION_CHOICE = "exploration_choice"
    INVENTORY_MANAGEMENT = "inventory_management"
    QUEST_DECISION = "quest_decision"
    GENERAL_CHOICE = "general_choice"

@dataclass
class PlayerProfile:
    """AI Player character profile with learning capabilities"""
    name: str
    playstyle: str  # "aggressive", "defensive", "balanced", "explorer", "minmaxer"
    personality: str  # "risk_taker", "cautious", "strategic", "impulsive"
    preferred_archetype: str  # "melee", "ranged", "magic", "hybrid"
    decision_style: str  # "analytical", "intuitive", "conservative", "experimental"
    risk_tolerance: float  # 0.0 to 1.0
    patience_level: float  # 0.0 to 1.0
    optimization_focus: str  # "damage", "survival", "utility", "balanced"
    
    # Learning and progression
    skill_level: str  # "noob", "casual", "experienced", "expert", "master"
    experience_points: int = 0
    games_played: int = 0
    successful_decisions: int = 0
    total_decisions: int = 0
    learning_rate: float = 0.1  # How quickly they adapt
    adaptation_threshold: float = 0.7  # When to change strategies
    
    # Team dynamics
    team_role: str = "solo"  # "tank", "dps", "support", "healer", "utility"
    team_coordination: float = 0.5  # How well they work with others
    communication_style: str = "direct"  # "direct", "supportive", "strategic"
    
    # Adaptive behavior
    strategy_memory: Dict[str, Any] = None  # Remember successful strategies
    failure_patterns: List[str] = None  # Track what doesn't work
    adaptation_history: List[Dict[str, Any]] = None  # Track changes over time
    
    def __post_init__(self):
        # Validate risk_tolerance and patience_level
        self.risk_tolerance = max(0.0, min(1.0, self.risk_tolerance))
        self.patience_level = max(0.0, min(1.0, self.patience_level))
        
        # Initialize learning components
        if self.strategy_memory is None:
            self.strategy_memory = {}
        if self.failure_patterns is None:
            self.failure_patterns = []
        if self.adaptation_history is None:
            self.adaptation_history = []
    
    def get_success_rate(self) -> float:
        """Calculate current success rate"""
        if self.total_decisions == 0:
            return 0.0
        return self.successful_decisions / self.total_decisions
    
    def should_adapt(self) -> bool:
        """Determine if player should adapt their strategy"""
        return self.get_success_rate() < self.adaptation_threshold
    
    def learn_from_decision(self, decision_result: Dict[str, Any]):
        """Learn from a decision outcome"""
        self.total_decisions += 1
        
        if decision_result.get('success', False):
            self.successful_decisions += 1
            
            # Remember successful strategies
            scenario = decision_result.get('scenario', 'unknown')
            action = decision_result.get('action', 'unknown')
            reasoning = decision_result.get('reasoning', '')
            
            if scenario not in self.strategy_memory:
                self.strategy_memory[scenario] = {}
            
            if action not in self.strategy_memory[scenario]:
                self.strategy_memory[scenario][action] = {
                    'count': 0,
                    'success_rate': 0.0,
                    'reasoning_patterns': []
                }
            
            strategy = self.strategy_memory[scenario][action]
            strategy['count'] += 1
            strategy['success_rate'] = (strategy['success_rate'] * (strategy['count'] - 1) + 1.0) / strategy['count']
            strategy['reasoning_patterns'].append(reasoning)
            
        else:
            # Track failure patterns
            failure_key = f"{decision_result.get('scenario', 'unknown')}_{decision_result.get('action', 'unknown')}"
            if failure_key not in self.failure_patterns:
                self.failure_patterns.append(failure_key)
    
    def adapt_strategy(self, scenario: str, context: Dict[str, Any]):
        """Adapt strategy based on learning"""
        if not self.should_adapt():
            return
        
        # Analyze recent performance
        recent_success_rate = self.get_success_rate()
        
        # Create adaptation record
        adaptation = {
            'timestamp': time.time(),
            'scenario': scenario,
            'previous_success_rate': recent_success_rate,
            'changes_made': []
        }
        
        # Adjust based on skill level and personality
        if self.skill_level == "noob":
            # Noobs adapt slowly and conservatively
            if recent_success_rate < 0.3:
                self.risk_tolerance = max(0.1, self.risk_tolerance - 0.1)
                adaptation['changes_made'].append("reduced_risk_tolerance")
        
        elif self.skill_level == "master":
            # Masters adapt quickly and strategically
            if recent_success_rate < 0.8:
                # Analyze failure patterns and adjust
                if "combat_defend" in self.failure_patterns:
                    self.risk_tolerance = min(1.0, self.risk_tolerance + 0.2)
                    adaptation['changes_made'].append("increased_aggression")
        
        # Personality-based adaptations
        if self.personality == "strategic":
            # Strategic players analyze and adapt methodically
            if recent_success_rate < 0.6:
                self.patience_level = min(1.0, self.patience_level + 0.1)
                adaptation['changes_made'].append("increased_patience")
        
        elif self.personality == "impulsive":
            # Impulsive players adapt quickly but chaotically
            if recent_success_rate < 0.4:
                self.risk_tolerance = max(0.1, self.risk_tolerance - 0.15)
                adaptation['changes_made'].append("reduced_risk_tolerance")
        
        self.adaptation_history.append(adaptation)
    
    def get_team_behavior(self, team_size: int, team_composition: List[str]) -> Dict[str, Any]:
        """Get team-oriented behavior based on role and team composition"""
        # Default skill distribution if not available
        default_distribution = {"damage": 0.5, "healing": 0.25, "mitigation": 0.25}
        
        team_behavior = {
            'coordination_level': self.team_coordination,
            'communication_style': self.communication_style,
            'role_focus': self.team_role,
            'team_adaptations': [],
            'skill_distribution': default_distribution,
            'toolbelt_size': 2,  # Default hybrid
            'damage_multiplier': 1.0  # Default multiplier
        }
        
        # Adjust behavior based on team composition
        if team_size > 1:
            if self.team_role == "pure_dps":
                # Pure DPS focus on maximum damage output
                team_behavior['priority'] = "maximize_damage"
                team_behavior['risk_tolerance'] = min(1.0, self.risk_tolerance + 0.2)
                team_behavior['self_sufficiency'] = 0.3  # Low self-sufficiency, rely on team
                team_behavior['skill_distribution'] = {"damage": 0.8, "healing": 0.1, "mitigation": 0.1}
                team_behavior['toolbelt_size'] = 1
                team_behavior['damage_multiplier'] = 1.5
            
            elif self.team_role == "hybrid_dps":
                # Hybrid DPS balance damage with some utility
                team_behavior['priority'] = "balanced_damage"
                team_behavior['risk_tolerance'] = min(1.0, self.risk_tolerance + 0.1)
                team_behavior['self_sufficiency'] = 0.6  # Moderate self-sufficiency
                team_behavior['skill_distribution'] = {"damage": 0.6, "healing": 0.2, "mitigation": 0.2}
                team_behavior['toolbelt_size'] = 2
                team_behavior['damage_multiplier'] = 1.2
            
            elif self.team_role == "support":
                # Support roles provide utility and some healing
                team_behavior['priority'] = "team_utility"
                team_behavior['patience_level'] = min(1.0, self.patience_level + 0.2)
                team_behavior['self_sufficiency'] = 0.7  # Good self-sufficiency
                team_behavior['skill_distribution'] = {"damage": 0.3, "healing": 0.4, "mitigation": 0.3}
                team_behavior['toolbelt_size'] = 3
                team_behavior['damage_multiplier'] = 0.8
            
            elif self.team_role == "hybrid_support":
                # Hybrid support focus on healing with some utility
                team_behavior['priority'] = "team_healing"
                team_behavior['patience_level'] = min(1.0, self.patience_level + 0.3)
                team_behavior['self_sufficiency'] = 0.8  # High self-sufficiency
                team_behavior['skill_distribution'] = {"damage": 0.2, "healing": 0.5, "mitigation": 0.3}
                team_behavior['toolbelt_size'] = 2
                team_behavior['damage_multiplier'] = 0.6
            
            elif self.team_role == "pure_support":
                # Pure support focus on maximum healing and survival
                team_behavior['priority'] = "team_survival"
                team_behavior['patience_level'] = min(1.0, self.patience_level + 0.4)
                team_behavior['self_sufficiency'] = 0.9  # Very high self-sufficiency
                team_behavior['skill_distribution'] = {"damage": 0.1, "healing": 0.6, "mitigation": 0.3}
                team_behavior['toolbelt_size'] = 1
                team_behavior['damage_multiplier'] = 0.4
            
            # Team coordination adjustments based on composition
            pure_dps_count = team_composition.count("pure_dps")
            support_count = team_composition.count("pure_support") + team_composition.count("hybrid_support")
            
            if pure_dps_count > 2:
                team_behavior['team_adaptations'].append("high_damage_team")
                team_behavior['coordination_level'] = min(1.0, team_behavior['coordination_level'] + 0.1)
            
            if support_count > 2:
                team_behavior['team_adaptations'].append("high_survival_team")
                team_behavior['patience_level'] = min(1.0, team_behavior['patience_level'] + 0.1)
            
            # Everyone has access to healing and damage mitigation
            team_behavior['universal_abilities'] = True
            team_behavior['healing_capability'] = team_behavior['skill_distribution']["healing"]
            team_behavior['mitigation_capability'] = team_behavior['skill_distribution']["mitigation"]
        
        return team_behavior

@dataclass
class GameContext:
    """Current game context for AI decision making"""
    player_level: int
    player_health: int
    player_mana: int
    current_location: str
    available_actions: List[str]
    recent_events: List[str]
    inventory: Dict[str, Any]
    skills: Dict[str, Any]
    quests: List[Dict[str, Any]]
    combat_situation: Optional[Dict[str, Any]] = None
    exploration_options: Optional[List[str]] = None

@dataclass
class PlayerDecision:
    """AI Player decision result"""
    action: str
    reasoning: str
    confidence: float  # 0.0 to 1.0
    alternatives: List[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.alternatives is None:
            self.alternatives = []
        if self.metadata is None:
            self.metadata = {}

class AIPlayerSystem:
    """AI Player system using Ollama to simulate human player behavior"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.ai_players_dir = self.base_dir / "ai_players"
        self.decisions_dir = self.base_dir / "ai_decisions"
        self.simulation_dir = self.base_dir / "ai_simulations"
        
        # Create directories
        for dir_path in [self.ai_players_dir, self.decisions_dir, self.simulation_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # Initialize logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.base_dir / "ai_player.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Ollama configuration
        self.ollama_url = "http://localhost:11434"
        self.model_name = "llama3.1:8b"
        self.max_tokens = 1500  # Longer responses for complex decisions
        self.temperature = 0.8  # Slightly higher for more creative decisions
        
        # AI Player profiles
        self.ai_players = {}
        self._load_ai_player_profiles()
        
        # Decision history
        self.decision_history = []
        
    def _load_ai_player_profiles(self):
        """Load AI player profiles from disk"""
        profiles_file = self.ai_players_dir / "ai_profiles.json"
        if profiles_file.exists():
            try:
                with open(profiles_file, 'r') as f:
                    profiles_data = json.load(f)
                    for profile_data in profiles_data:
                        # Handle legacy profiles that don't have new fields
                        if 'skill_level' not in profile_data:
                            profile_data['skill_level'] = 'experienced'
                        if 'experience_points' not in profile_data:
                            profile_data['experience_points'] = 0
                        if 'games_played' not in profile_data:
                            profile_data['games_played'] = 0
                        if 'successful_decisions' not in profile_data:
                            profile_data['successful_decisions'] = 0
                        if 'total_decisions' not in profile_data:
                            profile_data['total_decisions'] = 0
                        if 'learning_rate' not in profile_data:
                            profile_data['learning_rate'] = 0.1
                        if 'adaptation_threshold' not in profile_data:
                            profile_data['adaptation_threshold'] = 0.7
                        if 'team_role' not in profile_data:
                            profile_data['team_role'] = 'solo'
                        if 'team_coordination' not in profile_data:
                            profile_data['team_coordination'] = 0.5
                        if 'communication_style' not in profile_data:
                            profile_data['communication_style'] = 'direct'
                        if 'strategy_memory' not in profile_data:
                            profile_data['strategy_memory'] = {}
                        if 'failure_patterns' not in profile_data:
                            profile_data['failure_patterns'] = []
                        if 'adaptation_history' not in profile_data:
                            profile_data['adaptation_history'] = []
                        
                        profile = PlayerProfile(**profile_data)
                        self.ai_players[profile.name] = profile
                self.logger.info(f"Loaded {len(self.ai_players)} AI player profiles")
            except Exception as e:
                self.logger.error(f"Error loading AI player profiles: {e}")
                # If loading fails, create sample players
                self.create_sample_ai_players()
    
    def _save_ai_player_profiles(self):
        """Save AI player profiles to disk"""
        profiles_file = self.ai_players_dir / "ai_profiles.json"
        try:
            profiles_data = [asdict(profile) for profile in self.ai_players.values()]
            with open(profiles_file, 'w') as f:
                json.dump(profiles_data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving AI player profiles: {e}")
    
    def check_ollama_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"Ollama connection failed: {e}")
            return False
    
    def create_ai_player_profile(self, name: str, playstyle: str, personality: str,
                               preferred_archetype: str, decision_style: str,
                               risk_tolerance: float = 0.5, patience_level: float = 0.5,
                               optimization_focus: str = "balanced") -> PlayerProfile:
        """Create a new AI player profile"""
        profile = PlayerProfile(
            name=name,
            playstyle=playstyle,
            personality=personality,
            preferred_archetype=preferred_archetype,
            decision_style=decision_style,
            risk_tolerance=risk_tolerance,
            patience_level=patience_level,
            optimization_focus=optimization_focus
        )
        
        self.ai_players[name] = profile
        self._save_ai_player_profiles()
        self.logger.info(f"Created AI player profile: {name}")
        return profile
    
    def get_ai_player_profile(self, name: str) -> Optional[PlayerProfile]:
        """Get an AI player profile by name"""
        return self.ai_players.get(name)
    
    def list_ai_players(self) -> List[str]:
        """List all AI player names"""
        return list(self.ai_players.keys())
    
    def _build_decision_prompt(self, player_profile: PlayerProfile, action_type: PlayerActionType,
                              context: GameContext, available_choices: List[str]) -> str:
        """Build a prompt for AI decision making"""
        
        # Base system prompt
        prompt = f"""You are an AI player in the RPG game "Chronicles of Ruin: Sunderfall". 
You are simulating a human player with the following characteristics:

PLAYER PROFILE:
- Name: {player_profile.name}
- Playstyle: {player_profile.playstyle}
- Personality: {player_profile.personality}
- Preferred Archetype: {player_profile.preferred_archetype}
- Decision Style: {player_profile.decision_style}
- Risk Tolerance: {player_profile.risk_tolerance} (0=cautious, 1=aggressive)
- Patience Level: {player_profile.patience_level} (0=impulsive, 1=patient)
- Optimization Focus: {player_profile.optimization_focus}

CURRENT GAME CONTEXT:
- Player Level: {context.player_level}
- Health: {context.player_health}
    - Mana: {context.player_mana}
- Location: {context.current_location}
- Recent Events: {', '.join(context.recent_events[-3:]) if context.recent_events else 'None'}

AVAILABLE CHOICES: {', '.join(available_choices)}

ACTION TYPE: {action_type.value}

INSTRUCTIONS:
1. Think like a human player with the given personality and playstyle
2. Consider the current game context and recent events
3. Make a decision that aligns with your character's preferences
4. Provide your reasoning for the choice
5. Rate your confidence in this decision (0.0 to 1.0)
6. Consider alternative choices if applicable

Respond in JSON format:
{{
    "decision": "your_choice",
    "reasoning": "why you chose this",
    "confidence": 0.85,
    "alternatives": ["other_options_considered"],
    "thought_process": "your_analysis"
}}

Make your decision now:"""

        return prompt
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API for decision making"""
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens
                }
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                self.logger.error(f"Ollama API error: {response.status_code}")
                return ""
                
        except Exception as e:
            self.logger.error(f"Error calling Ollama: {e}")
            return ""
    
    def make_decision(self, player_name: str, action_type: PlayerActionType,
                     context: GameContext, available_choices: List[str]) -> PlayerDecision:
        """Make a decision as an AI player"""
        
        if not self.check_ollama_connection():
            return self._make_fallback_decision(player_name, action_type, context, available_choices)
        
        player_profile = self.get_ai_player_profile(player_name)
        if not player_profile:
            self.logger.error(f"AI player profile not found: {player_name}")
            return self._make_fallback_decision(player_name, action_type, context, available_choices)
        
        # Build prompt
        prompt = self._build_decision_prompt(player_profile, action_type, context, available_choices)
        
        # Get AI response
        response_text = self._call_ollama(prompt)
        
        # Parse response
        try:
            # Try to extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                decision_data = json.loads(json_str)
                
                decision = PlayerDecision(
                    action=decision_data.get("decision", available_choices[0]),
                    reasoning=decision_data.get("reasoning", "No reasoning provided"),
                    confidence=decision_data.get("confidence", 0.5),
                    alternatives=decision_data.get("alternatives", []),
                    metadata={"thought_process": decision_data.get("thought_process", "")}
                )
            else:
                # Fallback parsing
                decision = self._parse_text_response(response_text, available_choices)
                
        except Exception as e:
            self.logger.error(f"Error parsing AI response: {e}")
            decision = self._make_fallback_decision(player_name, action_type, context, available_choices)
        
        # Save decision to history
        self._save_decision(player_name, action_type, context, decision)
        
        return decision
    
    def _parse_text_response(self, response_text: str, available_choices: List[str]) -> PlayerDecision:
        """Parse text response when JSON parsing fails"""
        # Simple fallback parsing
        lines = response_text.strip().split('\n')
        
        # Try to find a decision in the text
        decision = available_choices[0]  # Default to first choice
        reasoning = "Fallback decision"
        confidence = 0.5
        
        for line in lines:
            line = line.strip().lower()
            for choice in available_choices:
                if choice.lower() in line:
                    decision = choice
                    reasoning = f"Found '{choice}' in response"
                    break
        
        return PlayerDecision(
            action=decision,
            reasoning=reasoning,
            confidence=confidence,
            alternatives=available_choices[:2] if len(available_choices) > 1 else []
        )
    
    def _make_fallback_decision(self, player_name: str, action_type: PlayerActionType,
                               context: GameContext, available_choices: List[str]) -> PlayerDecision:
        """Make a fallback decision when AI is unavailable"""
        
        # Simple rule-based decision making
        if action_type == PlayerActionType.CHARACTER_CREATION:
            # Default to balanced character
            decision = "balanced"
            reasoning = "Fallback: Creating balanced character"
            
        elif action_type == PlayerActionType.COMBAT_DECISION:
            # Default to attack if health is good, otherwise defensive
            if context.player_health > 50:
                decision = "attack"
                reasoning = "Fallback: Health is good, attacking"
            else:
                decision = "defend"
                reasoning = "Fallback: Health is low, defending"
                
        elif action_type == PlayerActionType.SKILL_ALLOCATION:
            # Default to damage optimization
            decision = "damage"
            reasoning = "Fallback: Allocating to damage"
            
        else:
            # Default to first available choice
            decision = available_choices[0] if available_choices else "wait"
            reasoning = f"Fallback: Choosing first available option"
        
        return PlayerDecision(
            action=decision,
            reasoning=reasoning,
            confidence=0.3,  # Low confidence for fallback
            alternatives=available_choices[:2] if len(available_choices) > 1 else []
        )
    
    def _save_decision(self, player_name: str, action_type: PlayerActionType,
                      context: GameContext, decision: PlayerDecision):
        """Save decision to history"""
        decision_record = {
            "timestamp": time.time(),
            "player_name": player_name,
            "action_type": action_type.value,
            "context": asdict(context),
            "decision": asdict(decision)
        }
        
        self.decision_history.append(decision_record)
        
        # Save to file
        decisions_file = self.decisions_dir / f"{player_name}_decisions.json"
        try:
            if decisions_file.exists():
                with open(decisions_file, 'r') as f:
                    history = json.load(f)
            else:
                history = []
            
            history.append(decision_record)
            
            with open(decisions_file, 'w') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error saving decision: {e}")
    
    def simulate_character_creation(self, player_name: str) -> PlayerDecision:
        """Simulate AI player creating a character"""
        context = GameContext(
            player_level=1,
            player_health=100,
            player_mana=50,
            current_location="Character Creation",
            available_actions=["create_character"],
            recent_events=["Starting new game"],
            inventory={},
            skills={},
            quests=[]
        )
        
        # Archetype choices
        archetype_choices = [
            "Melee (Power/Toughness - Close combat specialists)",
            "Ranged (Agility/Finesse - Distance fighters)", 
            "Magic (Knowledge/Wisdom - Spellcasters)",
            "Hybrid (Balanced approach)"
        ]
        
        return self.make_decision(player_name, PlayerActionType.CHARACTER_CREATION, 
                                context, archetype_choices)
    
    def simulate_combat_decision(self, player_name: str, player_health: int, 
                                enemy_info: Dict[str, Any], available_actions: List[str]) -> PlayerDecision:
        """Simulate AI player making combat decisions"""
        context = GameContext(
            player_level=player_health // 10,  # Rough estimate
            player_health=player_health,
            player_mana=50,  # Default
            current_location="Combat",
            available_actions=available_actions,
            recent_events=[f"Fighting {enemy_info.get('name', 'enemy')}"],
            inventory={},
            skills={},
            quests=[],
            combat_situation=enemy_info
        )
        
        return self.make_decision(player_name, PlayerActionType.COMBAT_DECISION, 
                                context, available_actions)
    
    def simulate_skill_allocation(self, player_name: str, available_points: int,
                                current_skills: Dict[str, Any]) -> PlayerDecision:
        """Simulate AI player allocating skill points"""
        context = GameContext(
            player_level=available_points // 2,  # Rough estimate
            player_health=100,
            player_mana=50,
            current_location="Skill Allocation",
            available_actions=["allocate_skills"],
            recent_events=[f"Gained {available_points} skill points"],
            inventory={},
            skills=current_skills,
            quests=[]
        )
        
        skill_choices = [
            "Damage (Increase attack power)",
            "Defense (Increase survivability)",
            "Utility (Increase versatility)",
            "Balanced (Mix of all types)"
        ]
        
        return self.make_decision(player_name, PlayerActionType.SKILL_ALLOCATION,
                                context, skill_choices)
    
    def simulate_exploration_choice(self, player_name: str, available_areas: List[str],
                                   current_location: str) -> PlayerDecision:
        """Simulate AI player choosing exploration destination"""
        context = GameContext(
            player_level=10,  # Default
            player_health=100,
            player_mana=50,
            current_location=current_location,
            available_actions=available_areas,
            recent_events=[f"Currently in {current_location}"],
            inventory={},
            skills={},
            quests=[],
            exploration_options=available_areas
        )
        
        return self.make_decision(player_name, PlayerActionType.EXPLORATION_CHOICE,
                                context, available_areas)
    
    def get_decision_history(self, player_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get decision history for an AI player"""
        decisions_file = self.decisions_dir / f"{player_name}_decisions.json"
        if decisions_file.exists():
            try:
                with open(decisions_file, 'r') as f:
                    history = json.load(f)
                    return history[-limit:]  # Return last N decisions
            except Exception as e:
                self.logger.error(f"Error loading decision history: {e}")
        
        return []
    
    def create_sample_ai_players(self):
        """Create sample AI player profiles for testing"""
        sample_players = [
            {
                "name": "Alex",
                "playstyle": "aggressive",
                "personality": "risk_taker",
                "preferred_archetype": "melee",
                "decision_style": "impulsive",
                "risk_tolerance": 0.8,
                "patience_level": 0.2,
                "optimization_focus": "damage"
            },
            {
                "name": "Sam",
                "playstyle": "defensive",
                "personality": "cautious",
                "preferred_archetype": "magic",
                "decision_style": "analytical",
                "risk_tolerance": 0.3,
                "patience_level": 0.9,
                "optimization_focus": "survival"
            },
            {
                "name": "Jordan",
                "playstyle": "balanced",
                "personality": "strategic",
                "preferred_archetype": "hybrid",
                "decision_style": "analytical",
                "risk_tolerance": 0.5,
                "patience_level": 0.7,
                "optimization_focus": "balanced"
            },
            {
                "name": "Casey",
                "playstyle": "explorer",
                "personality": "curious",
                "preferred_archetype": "ranged",
                "decision_style": "intuitive",
                "risk_tolerance": 0.6,
                "patience_level": 0.8,
                "optimization_focus": "utility"
            }
        ]
        
        for player_data in sample_players:
            self.create_ai_player_profile(**player_data)
        
        self.logger.info(f"Created {len(sample_players)} sample AI players")
    
    def run_simulation(self, player_name: str, simulation_type: str, **kwargs) -> Dict[str, Any]:
        """Run a simulation with an AI player"""
        
        if not self.check_ollama_connection():
            return {"error": "Ollama not available", "fallback": True}
        
        player_profile = self.get_ai_player_profile(player_name)
        if not player_profile:
            return {"error": f"AI player '{player_name}' not found"}
        
        simulation_results = {
            "player_name": player_name,
            "simulation_type": simulation_type,
            "timestamp": time.time(),
            "decisions": [],
            "outcomes": []
        }
        
        if simulation_type == "character_creation":
            decision = self.simulate_character_creation(player_name)
            simulation_results["decisions"].append({
                "type": "character_creation",
                "decision": asdict(decision)
            })
            
        elif simulation_type == "combat_scenario":
            enemy_info = kwargs.get("enemy_info", {"name": "Goblin", "level": 5})
            available_actions = kwargs.get("available_actions", ["attack", "defend", "use_item"])
            player_health = kwargs.get("player_health", 80)
            
            decision = self.simulate_combat_decision(player_name, player_health, enemy_info, available_actions)
            simulation_results["decisions"].append({
                "type": "combat_decision",
                "decision": asdict(decision)
            })
            
        elif simulation_type == "skill_allocation":
            available_points = kwargs.get("available_points", 5)
            current_skills = kwargs.get("current_skills", {})
            
            decision = self.simulate_skill_allocation(player_name, available_points, current_skills)
            simulation_results["decisions"].append({
                "type": "skill_allocation",
                "decision": asdict(decision)
            })
            
        elif simulation_type == "exploration":
            available_areas = kwargs.get("available_areas", ["Forest", "Cave", "Town"])
            current_location = kwargs.get("current_location", "Starting Area")
            
            decision = self.simulate_exploration_choice(player_name, available_areas, current_location)
            simulation_results["decisions"].append({
                "type": "exploration_choice",
                "decision": asdict(decision)
            })
        
        # Save simulation results
        simulation_file = self.simulation_dir / f"{player_name}_{simulation_type}_{int(time.time())}.json"
        try:
            with open(simulation_file, 'w') as f:
                json.dump(simulation_results, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving simulation: {e}")
        
        return simulation_results

    def make_decision_enhanced(self, player_name: str, action_type: PlayerActionType,
                              context: GameContext, available_choices: List[str], 
                              verbose: bool = True) -> PlayerDecision:
        """Make AI decision with enhanced logging showing full thinking process"""
        try:
            # Get player profile
            player_profile = self.get_ai_player_profile(player_name)
            if not player_profile:
                return self._make_fallback_decision(player_name, action_type, context, available_choices)
            
            # Build enhanced prompt with full context
            prompt = self._build_decision_prompt_enhanced(player_profile, action_type, context, available_choices)
            
            # Call Ollama with timing
            start_time = time.time()
            response_text = self._call_ollama_enhanced(prompt, verbose)
            response_time = time.time() - start_time
            
            # Parse response
            decision = self._parse_text_response_enhanced(response_text, available_choices, verbose)
            
            # Add metadata
            decision.metadata.update({
                'full_prompt': prompt,
                'full_response': response_text,
                'response_time': response_time,
                'tokens_used': len(prompt.split()) + len(response_text.split()),  # Approximate
                'player_profile': asdict(player_profile),
                'action_type': action_type.value,
                'available_choices': available_choices
            })
            
            # Save decision with enhanced data
            self._save_decision_enhanced(player_name, action_type, context, decision)
            
            return decision
            
        except Exception as e:
            self.logger.error(f"Error in enhanced decision making: {e}")
            return self._make_fallback_decision(player_name, action_type, context, available_choices)
    
    def _build_decision_prompt_enhanced(self, player_profile: PlayerProfile, action_type: PlayerActionType,
                                       context: GameContext, available_choices: List[str]) -> str:
        """Build enhanced prompt with full context and detailed instructions"""
        
        # Base prompt structure
        prompt = f"""You are an AI player in a fantasy RPG game called "Chronicles of Ruin: Sunderfall".

PLAYER PROFILE:
- Name: {player_profile.name}
- Playstyle: {player_profile.playstyle}
- Personality: {player_profile.personality}
- Preferred Archetype: {player_profile.preferred_archetype}
- Decision Style: {player_profile.decision_style}
- Risk Tolerance: {player_profile.risk_tolerance}
- Patience Level: {player_profile.patience_level}
- Optimization Focus: {player_profile.optimization_focus}

CURRENT GAME CONTEXT:
- Player Level: {context.player_level}
- Player Health: {context.player_health}
- Player Mana: {context.player_mana}
- Current Location: {context.current_location}
- Available Actions: {', '.join(context.available_actions)}
- Recent Events: {', '.join(context.recent_events) if context.recent_events else 'None'}
- Inventory: {context.inventory}
- Skills: {context.skills}
- Active Quests: {len(context.quests)} quests

ACTION TYPE: {action_type.value.replace('_', ' ').title()}
AVAILABLE CHOICES: {', '.join(available_choices)}

INSTRUCTIONS:
1. Consider your player profile and personality when making decisions
2. Analyze the current game context carefully
3. Choose the action that best fits your playstyle and current situation
4. Provide detailed reasoning for your choice
5. Express your confidence level (0.0 to 1.0)
6. Consider alternative options and why you didn't choose them

RESPONSE FORMAT:
Action: [your chosen action from the available choices]
Reasoning: [detailed explanation of your decision-making process]
Confidence: [confidence level as a number between 0.0 and 1.0]
Alternatives: [list of other options you considered and why you didn't choose them]

Now make your decision:"""

        # Add scenario-specific context
        if action_type == PlayerActionType.COMBAT_DECISION and context.combat_situation:
            prompt += f"""

COMBAT SITUATION:
- Enemy: {context.combat_situation.get('name', 'Unknown')}
- Enemy Health: {context.combat_situation.get('health', 100)}
- Enemy Level: {context.combat_situation.get('level', 1)}
- Enemy Attack: {context.combat_situation.get('attack', 10)}
- Enemy Defense: {context.combat_situation.get('defense', 5)}"""

        elif action_type == PlayerActionType.SKILL_ALLOCATION:
            prompt += f"""

SKILL ALLOCATION CONTEXT:
- Available Points: {context.player_level * 2} (estimated)
- Current Skills: {context.skills}
- Consider your archetype and playstyle when choosing skills"""

        elif action_type == PlayerActionType.EXPLORATION_CHOICE and context.exploration_options:
            prompt += f"""

EXPLORATION OPTIONS:
- Available Areas: {', '.join(context.exploration_options)}
- Consider risk vs reward for each area
- Think about your current health and resources"""

        return prompt
    
    def _call_ollama_enhanced(self, prompt: str, verbose: bool = True) -> str:
        """Call Ollama with enhanced error handling and logging"""
        try:
            if verbose:
                print(f"   Calling Ollama API...")
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": self.temperature,
                        "num_predict": self.max_tokens
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '')
                
                if verbose:
                    print(f"   Ollama response received ({len(response_text)} characters)")
                
                return response_text
            else:
                raise Exception(f"Ollama API error: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Error calling Ollama: {e}")
            return f"Error: {str(e)}"
    
    def _parse_text_response_enhanced(self, response_text: str, available_choices: List[str], 
                                     verbose: bool = True) -> PlayerDecision:
        """Parse enhanced AI response with detailed extraction"""
        try:
            # Extract action
            action = None
            reasoning = "No reasoning provided"
            confidence = 0.5
            alternatives = []
            
            # Parse response line by line
            lines = response_text.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line.lower().startswith('action:'):
                    action = line.split(':', 1)[1].strip()
                elif line.lower().startswith('reasoning:'):
                    reasoning = line.split(':', 1)[1].strip()
                elif line.lower().startswith('confidence:'):
                    try:
                        confidence = float(line.split(':', 1)[1].strip())
                        confidence = max(0.0, min(1.0, confidence))
                    except:
                        confidence = 0.5
                elif line.lower().startswith('alternatives:'):
                    alt_text = line.split(':', 1)[1].strip()
                    alternatives = [alt.strip() for alt in alt_text.split(',') if alt.strip()]
            
            # Validate action
            if not action or action not in available_choices:
                if verbose:
                    print(f"   Warning: Invalid action '{action}', using fallback")
                action = available_choices[0] if available_choices else "unknown"
            
            if verbose:
                print(f"   Parsed - Action: {action}, Confidence: {confidence}")
            
            return PlayerDecision(
                action=action,
                reasoning=reasoning,
                confidence=confidence,
                alternatives=alternatives,
                metadata={
                    'parsing_success': True,
                    'original_response': response_text
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error parsing enhanced response: {e}")
            return PlayerDecision(
                action=available_choices[0] if available_choices else "unknown",
                reasoning=f"Fallback: {action_type.value}",
                confidence=0.5,
                alternatives=available_choices[1:] if len(available_choices) > 1 else [],
                metadata={
                    'parsing_success': False,
                    'error': str(e),
                    'original_response': response_text
                }
            )
    
    def _save_decision_enhanced(self, player_name: str, action_type: PlayerActionType,
                                context: GameContext, decision: PlayerDecision):
        """Save enhanced decision with full metadata"""
        decision_record = {
            'timestamp': time.time(),
            'player_name': player_name,
            'action_type': action_type.value,
            'action': decision.action,
            'reasoning': decision.reasoning,
            'confidence': decision.confidence,
            'alternatives': decision.alternatives,
            'context': asdict(context),
            'metadata': decision.metadata
        }
        
        self.decision_history.append(decision_record)
        
        # Save to file
        decisions_file = self.decisions_dir / f"{player_name}_decisions.json"
        try:
            if decisions_file.exists():
                with open(decisions_file, 'r') as f:
                    existing_decisions = json.load(f)
            else:
                existing_decisions = []
            
            existing_decisions.append(decision_record)
            
            with open(decisions_file, 'w') as f:
                json.dump(existing_decisions, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Error saving enhanced decision: {e}")


class LearningAIPartySystem:
    """Manages a learning AI party with 5 players of different skill levels"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.party_dir = self.base_dir / "ai_party"
        self.party_dir.mkdir(exist_ok=True)
        
        # Party configuration
        self.party_size = 5
        self.party_members = []
        self.team_dynamics = {}
        self.learning_sessions = []
        
        # Skill level configurations
        self.skill_levels = {
            "noob": {
                "learning_rate": 0.15,
                "adaptation_threshold": 0.6,
                "decision_confidence": 0.3,
                "team_coordination": 0.3
            },
            "casual": {
                "learning_rate": 0.12,
                "adaptation_threshold": 0.65,
                "decision_confidence": 0.5,
                "team_coordination": 0.5
            },
            "experienced": {
                "learning_rate": 0.10,
                "adaptation_threshold": 0.7,
                "decision_confidence": 0.7,
                "team_coordination": 0.7
            },
            "expert": {
                "learning_rate": 0.08,
                "adaptation_threshold": 0.75,
                "decision_confidence": 0.8,
                "team_coordination": 0.8
            },
            "master": {
                "learning_rate": 0.05,
                "adaptation_threshold": 0.8,
                "decision_confidence": 0.9,
                "team_coordination": 0.9
            }
        }
        
        # Team roles and compositions
        self.team_roles = ["pure_dps", "hybrid_dps", "support", "hybrid_support", "pure_support"]
        self.role_specializations = {
            "pure_dps": {
                "playstyle": "aggressive", 
                "optimization_focus": "damage",
                "skill_distribution": {"damage": 0.8, "healing": 0.1, "mitigation": 0.1},
                "toolbelt_size": 1,
                "damage_multiplier": 1.5
            },
            "hybrid_dps": {
                "playstyle": "balanced", 
                "optimization_focus": "damage",
                "skill_distribution": {"damage": 0.6, "healing": 0.2, "mitigation": 0.2},
                "toolbelt_size": 2,
                "damage_multiplier": 1.2
            },
            "support": {
                "playstyle": "balanced", 
                "optimization_focus": "utility",
                "skill_distribution": {"damage": 0.3, "healing": 0.4, "mitigation": 0.3},
                "toolbelt_size": 3,
                "damage_multiplier": 0.8
            },
            "hybrid_support": {
                "playstyle": "defensive", 
                "optimization_focus": "survival",
                "skill_distribution": {"damage": 0.2, "healing": 0.5, "mitigation": 0.3},
                "toolbelt_size": 2,
                "damage_multiplier": 0.6
            },
            "pure_support": {
                "playstyle": "defensive", 
                "optimization_focus": "survival",
                "skill_distribution": {"damage": 0.1, "healing": 0.6, "mitigation": 0.3},
                "toolbelt_size": 1,
                "damage_multiplier": 0.4
            }
        }
    
    def create_learning_party(self, skill_levels: List[str] = None) -> List[PlayerProfile]:
        """Create a 5-player party with different skill levels"""
        if skill_levels is None:
            skill_levels = ["noob", "casual", "experienced", "expert", "master"]
        
        party = []
        names = ["Alex", "Sam", "Jordan", "Casey", "Riley"]
        
        for i, (name, skill_level, role) in enumerate(zip(names, skill_levels, self.team_roles)):
            # Get skill level configuration
            skill_config = self.skill_levels[skill_level]
            
            # Create player profile with learning capabilities
            player = PlayerProfile(
                name=name,
                playstyle=self.role_specializations[role]["playstyle"],
                personality=self._get_personality_for_role(role, skill_level),
                preferred_archetype=self._get_archetype_for_role(role),
                decision_style=self._get_decision_style_for_skill(skill_level),
                risk_tolerance=self._get_risk_tolerance_for_role(role, skill_level),
                patience_level=self._get_patience_for_role(role, skill_level),
                optimization_focus=self.role_specializations[role]["optimization_focus"],
                skill_level=skill_level,
                learning_rate=skill_config["learning_rate"],
                adaptation_threshold=skill_config["adaptation_threshold"],
                team_role=role,
                team_coordination=skill_config["team_coordination"],
                communication_style=self._get_communication_style_for_role(role)
            )
            
            party.append(player)
        
        self.party_members = party
        self._save_party_state()
        return party
    
    def _get_personality_for_role(self, role: str, skill_level: str) -> str:
        """Get appropriate personality for role and skill level"""
        if role == "pure_dps":
            return "risk_taker" if skill_level in ["expert", "master"] else "impulsive"
        elif role == "hybrid_dps":
            return "strategic" if skill_level in ["experienced", "expert", "master"] else "balanced"
        elif role == "support":
            return "strategic" if skill_level in ["experienced", "expert", "master"] else "cautious"
        elif role == "hybrid_support":
            return "cautious" if skill_level in ["noob", "casual"] else "strategic"
        elif role == "pure_support":
            return "cautious" if skill_level in ["noob", "casual"] else "strategic"
        return "balanced"
    
    def _get_archetype_for_role(self, role: str) -> str:
        """Get appropriate archetype for role"""
        if role == "pure_dps":
            return "melee"  # Could be "ranged" for some pure DPS
        elif role == "hybrid_dps":
            return "hybrid"  # Mix of melee and magic
        elif role == "support":
            return "magic"  # Balanced magic user
        elif role == "hybrid_support":
            return "hybrid"  # Mix of magic and utility
        elif role == "pure_support":
            return "magic"  # Pure magic support
        return "hybrid"
    
    def _get_decision_style_for_skill(self, skill_level: str) -> str:
        """Get decision style based on skill level"""
        if skill_level == "noob":
            return "conservative"
        elif skill_level in ["casual", "experienced"]:
            return "intuitive"
        else:
            return "analytical"
    
    def _get_risk_tolerance_for_role(self, role: str, skill_level: str) -> float:
        """Get risk tolerance based on role and skill level"""
        base_risk = {
            "pure_dps": 0.8,
            "hybrid_dps": 0.6,
            "support": 0.4,
            "hybrid_support": 0.3,
            "pure_support": 0.2
        }
        
        skill_multiplier = {
            "noob": 0.8,
            "casual": 0.9,
            "experienced": 1.0,
            "expert": 1.1,
            "master": 1.2
        }
        
        return min(1.0, base_risk[role] * skill_multiplier[skill_level])
    
    def _get_patience_for_role(self, role: str, skill_level: str) -> float:
        """Get patience level based on role and skill level"""
        base_patience = {
            "pure_dps": 0.3,
            "hybrid_dps": 0.5,
            "support": 0.7,
            "hybrid_support": 0.8,
            "pure_support": 0.9
        }
        
        skill_multiplier = {
            "noob": 0.9,
            "casual": 0.95,
            "experienced": 1.0,
            "expert": 1.05,
            "master": 1.1
        }
        
        return min(1.0, base_patience[role] * skill_multiplier[skill_level])
    
    def _get_communication_style_for_role(self, role: str) -> str:
        """Get communication style for role"""
        if role == "pure_dps":
            return "direct"  # Pure DPS are direct and focused
        elif role == "hybrid_dps":
            return "strategic"  # Hybrid DPS think strategically
        elif role == "support":
            return "supportive"  # Support roles are encouraging
        elif role == "hybrid_support":
            return "supportive"  # Hybrid support are also encouraging
        elif role == "pure_support":
            return "supportive"  # Pure support are most encouraging
        return "strategic"
    
    def run_learning_session(self, scenarios: List[str], session_name: str = None) -> Dict[str, Any]:
        """Run a learning session with the entire party"""
        if session_name is None:
            session_name = f"learning_session_{int(time.time())}"
        
        print(f"🎮 LEARNING AI PARTY SESSION")
        print(f"=" * 50)
        print(f"Session: {session_name}")
        print(f"Party Size: {len(self.party_members)}")
        print(f"Scenarios: {', '.join(scenarios)}")
        print()
        
        # Display party composition
        print(f"PARTY COMPOSITION:")
        for i, player in enumerate(self.party_members, 1):
            print(f"  {i}. {player.name} ({player.skill_level} {player.team_role})")
            print(f"     Playstyle: {player.playstyle}, Personality: {player.personality}")
            print(f"     Success Rate: {player.get_success_rate():.1%}")
        print()
        
        session_results = {
            "session_name": session_name,
            "timestamp": time.time(),
            "party_members": [player.name for player in self.party_members],
            "scenarios": scenarios,
            "individual_results": {},
            "team_results": {},
            "learning_insights": []
        }
        
        # Run solo scenarios for each player
        print(f"🏃 SOLO PERFORMANCE TESTING")
        print(f"=" * 30)
        for player in self.party_members:
            print(f"\n--- Testing {player.name} (Solo) ---")
            solo_results = self._run_solo_scenarios(player, scenarios)
            session_results["individual_results"][player.name] = solo_results
            
            # Apply learning
            self._apply_learning(player, solo_results)
        
        # Run team scenarios
        print(f"\n👥 TEAM PERFORMANCE TESTING")
        print(f"=" * 30)
        team_results = self._run_team_scenarios(scenarios)
        session_results["team_results"] = team_results
        
        # Analyze team learning
        self._analyze_team_learning(team_results)
        
        # Generate learning insights
        session_results["learning_insights"] = self._generate_learning_insights()
        
        # Save session
        self.learning_sessions.append(session_results)
        self._save_party_state()
        
        # Display session summary
        self._display_session_summary(session_results)
        
        return session_results
    
    def _run_solo_scenarios(self, player: PlayerProfile, scenarios: List[str]) -> Dict[str, Any]:
        """Run scenarios for a single player"""
        results = {
            "player_name": player.name,
            "skill_level": player.skill_level,
            "scenarios": {},
            "learning_progress": {},
            "adaptations_made": []
        }
        
        for scenario in scenarios:
            print(f"   Testing {scenario.replace('_', ' ').title()}...")
            
            # Check if player should adapt before this scenario
            if player.should_adapt():
                player.adapt_strategy(scenario, {})
                results["adaptations_made"].append({
                    "scenario": scenario,
                    "changes": player.adaptation_history[-1]["changes_made"] if player.adaptation_history else []
                })
            
            # Run scenario (simplified for now)
            scenario_result = {
                "success": random.random() > 0.3,  # 70% success rate for demo
                "action": "demo_action",
                "reasoning": f"Demo reasoning for {scenario}",
                "confidence": random.uniform(0.5, 0.9)
            }
            
            # Apply learning
            player.learn_from_decision(scenario_result)
            
            results["scenarios"][scenario] = scenario_result
        
        # Track learning progress
        results["learning_progress"] = {
            "success_rate": player.get_success_rate(),
            "total_decisions": player.total_decisions,
            "successful_decisions": player.successful_decisions,
            "strategy_memory_size": len(player.strategy_memory),
            "failure_patterns_count": len(player.failure_patterns)
        }
        
        return results
    
    def _run_team_scenarios(self, scenarios: List[str]) -> Dict[str, Any]:
        """Run scenarios with the entire team"""
        results = {
            "team_composition": [player.team_role for player in self.party_members],
            "team_dynamics": {},
            "scenarios": {},
            "coordination_score": 0.0
        }
        
        # Calculate team dynamics
        for player in self.party_members:
            team_behavior = player.get_team_behavior(
                len(self.party_members),
                [p.team_role for p in self.party_members]
            )
            results["team_dynamics"][player.name] = team_behavior
        
        # Run team scenarios
        for scenario in scenarios:
            print(f"   Testing Team {scenario.replace('_', ' ').title()}...")
            
            # Simulate team coordination
            team_success = self._simulate_team_coordination(scenario)
            
            results["scenarios"][scenario] = {
                "success": team_success,
                "team_actions": self._generate_team_actions(scenario),
                "coordination_level": sum(p.team_coordination for p in self.party_members) / len(self.party_members)
            }
        
        # Calculate overall coordination score
        results["coordination_score"] = sum(
            results["scenarios"][s]["coordination_level"] 
            for s in results["scenarios"]
        ) / len(results["scenarios"])
        
        return results
    
    def _simulate_team_coordination(self, scenario: str) -> bool:
        """Simulate team coordination success"""
        # Higher skill players contribute more to team success
        team_success_chance = sum(
            self.skill_levels[player.skill_level]["team_coordination"]
            for player in self.party_members
        ) / len(self.party_members)
        
        return random.random() < team_success_chance
    
    def _generate_team_actions(self, scenario: str) -> List[Dict[str, Any]]:
        """Generate actions for each team member"""
        actions = []
        for player in self.party_members:
            team_behavior = player.get_team_behavior(
                len(self.party_members),
                [p.team_role for p in self.party_members]
            )
            
            actions.append({
                "player": player.name,
                "role": player.team_role,
                "action": f"team_{scenario}_action",
                "coordination": team_behavior["coordination_level"],
                "priority": team_behavior.get("priority", "balanced")
            })
        
        return actions
    
    def _apply_learning(self, player: PlayerProfile, results: Dict[str, Any]):
        """Apply learning from session results"""
        # Update experience
        player.games_played += 1
        player.experience_points += len(results["scenarios"])
        
        # Check for skill level progression
        self._check_skill_progression(player)
    
    def _check_skill_progression(self, player: PlayerProfile):
        """Check if player should progress to next skill level"""
        skill_progression = {
            "noob": {"threshold": 50, "next": "casual"},
            "casual": {"threshold": 100, "next": "experienced"},
            "experienced": {"threshold": 200, "next": "expert"},
            "expert": {"threshold": 500, "next": "master"}
        }
        
        if player.skill_level in skill_progression:
            progression = skill_progression[player.skill_level]
            if player.experience_points >= progression["threshold"] and player.get_success_rate() >= 0.6:
                old_level = player.skill_level
                player.skill_level = progression["next"]
                
                # Update learning parameters for new skill level
                new_config = self.skill_levels[player.skill_level]
                player.learning_rate = new_config["learning_rate"]
                player.adaptation_threshold = new_config["adaptation_threshold"]
                player.team_coordination = new_config["team_coordination"]
                
                print(f"🎉 {player.name} progressed from {old_level} to {player.skill_level}!")
    
    def _analyze_team_learning(self, team_results: Dict[str, Any]):
        """Analyze team learning patterns"""
        # Track team coordination improvements
        coordination_score = team_results["coordination_score"]
        
        # Update team dynamics based on performance
        for player in self.party_members:
            if coordination_score > 0.7:
                # Team is working well together
                player.team_coordination = min(1.0, player.team_coordination + 0.05)
            elif coordination_score < 0.4:
                # Team needs improvement
                player.team_coordination = max(0.1, player.team_coordination - 0.02)
    
    def _generate_learning_insights(self) -> List[str]:
        """Generate insights about the learning session"""
        insights = []
        
        # Analyze individual learning
        for player in self.party_members:
            success_rate = player.get_success_rate()
            if success_rate > 0.8:
                insights.append(f"{player.name} ({player.skill_level}) is performing excellently with {success_rate:.1%} success rate")
            elif success_rate < 0.4:
                insights.append(f"{player.name} ({player.skill_level}) is struggling with {success_rate:.1%} success rate")
        
        # Analyze team dynamics
        avg_coordination = sum(p.team_coordination for p in self.party_members) / len(self.party_members)
        if avg_coordination > 0.7:
            insights.append("Team coordination is excellent - players are working well together")
        elif avg_coordination < 0.4:
            insights.append("Team coordination needs improvement - players need to work better as a team")
        
        # Analyze skill progression
        progressing_players = [p for p in self.party_members if p.experience_points > 50]
        if progressing_players:
            insights.append(f"{len(progressing_players)} players are showing good progression")
        
        return insights
    
    def _display_session_summary(self, session_results: Dict[str, Any]):
        """Display a summary of the learning session"""
        print(f"\n📊 LEARNING SESSION SUMMARY")
        print(f"=" * 50)
        print(f"Session: {session_results['session_name']}")
        print(f"Duration: {len(session_results['individual_results'])} individual tests + team tests")
        
        # Individual performance
        print(f"\nINDIVIDUAL PERFORMANCE:")
        for player_name, results in session_results["individual_results"].items():
            progress = results["learning_progress"]
            print(f"  {player_name}: {progress['success_rate']:.1%} success rate, {progress['total_decisions']} decisions")
        
        # Team performance
        team_results = session_results["team_results"]
        print(f"\nTEAM PERFORMANCE:")
        print(f"  Coordination Score: {team_results['coordination_score']:.2f}")
        print(f"  Team Composition: {' → '.join(team_results['team_composition'])}")
        
        # Learning insights
        print(f"\nLEARNING INSIGHTS:")
        for insight in session_results["learning_insights"]:
            print(f"  • {insight}")
    
    def _save_party_state(self):
        """Save current party state"""
        party_file = self.party_dir / "party_state.json"
        try:
            party_data = {
                "party_members": [asdict(player) for player in self.party_members],
                "learning_sessions": self.learning_sessions,
                "last_updated": time.time()
            }
            with open(party_file, 'w') as f:
                json.dump(party_data, f, indent=2)
        except Exception as e:
            print(f"Error saving party state: {e}")


def main():
    """Main function for testing the AI Player System"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Player System for Chronicles of Ruin")
    parser.add_argument("--base-dir", type=str, default=".", help="Base directory for data")
    parser.add_argument("--action", choices=["create-profile", "simulate", "list", "history", "samples"], 
                       required=True, help="Action to perform")
    parser.add_argument("--player-name", type=str, help="AI player name")
    parser.add_argument("--simulation-type", type=str, help="Type of simulation to run")
    
    args = parser.parse_args()
    
    ai_system = AIPlayerSystem(Path(args.base_dir))
    
    if args.action == "create-profile":
        if not args.player_name:
            print("Error: --player-name required for create-profile")
            return
        
        # Create a sample profile
        profile = ai_system.create_ai_player_profile(
            name=args.player_name,
            playstyle="balanced",
            personality="strategic",
            preferred_archetype="hybrid",
            decision_style="analytical",
            risk_tolerance=0.5,
            patience_level=0.7,
            optimization_focus="balanced"
        )
        print(f"Created AI player profile: {profile.name}")
        
    elif args.action == "simulate":
        if not args.player_name or not args.simulation_type:
            print("Error: --player-name and --simulation-type required for simulate")
            return
        
        result = ai_system.run_simulation(args.player_name, args.simulation_type)
        print(f"Simulation result: {json.dumps(result, indent=2)}")
        
    elif args.action == "list":
        players = ai_system.list_ai_players()
        print(f"AI Players: {players}")
        
    elif args.action == "history":
        if not args.player_name:
            print("Error: --player-name required for history")
            return
        
        history = ai_system.get_decision_history(args.player_name)
        print(f"Decision history for {args.player_name}:")
        for decision in history[-5:]:  # Show last 5 decisions
            print(f"  {decision['action_type']}: {decision['decision']['action']}")
            
    elif args.action == "samples":
        ai_system.create_sample_ai_players()
        print("Created sample AI players")


if __name__ == "__main__":
    main()

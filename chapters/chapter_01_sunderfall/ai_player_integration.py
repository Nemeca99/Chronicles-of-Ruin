#!/usr/bin/env python3
"""
AI Player Integration for Chronicles of Ruin: Sunderfall
Integrates AI players into the main game loop for testing and refinement
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import asdict

# Add the tools directory to the path for AI Player System
sys.path.append(str(Path(__file__).parent.parent.parent / "tools"))

from ai_player_system import AIPlayerSystem, PlayerActionType, GameContext, PlayerDecision

class AIPlayerIntegration:
    """Integrates AI players into the main game loop"""
    
    def __init__(self, game_launcher):
        self.game_launcher = game_launcher
        self.base_dir = Path(__file__).parent.parent.parent
        self.ai_system = AIPlayerSystem(self.base_dir)
        self.current_ai_player = None
        self.ai_game_log = []
        
    def setup_ai_player(self, player_name: str) -> bool:
        """Set up an AI player for the current game session"""
        try:
            # Check if AI player exists
            profile = self.ai_system.get_ai_player_profile(player_name)
            if not profile:
                print(f"❌ AI player '{player_name}' not found. Create one first using the AI Player Tool.")
                return False
            
            # Test Ollama connection
            if not self.ai_system.check_ollama_connection():
                print("❌ Ollama is not running. Please start Ollama first.")
                return False
            
            self.current_ai_player = profile
            print(f"✅ AI Player '{player_name}' loaded successfully!")
            print(f"   Playstyle: {profile.playstyle}")
            print(f"   Personality: {profile.personality}")
            print(f"   Preferred Archetype: {profile.preferred_archetype}")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up AI player: {e}")
            return False
    
    def _build_game_context(self, action_type: PlayerActionType) -> GameContext:
        """Build current game context for AI decision making"""
        player = self.game_launcher.current_player
        if not player:
            return GameContext(
                player_level=1,
                player_health=100,
                player_mana=50,
                current_location="Starting Area",
                available_actions=[],
                recent_events=[],
                inventory={},
                skills={},
                quests=[]
            )
        
        # Get current player stats
        stats = player.get("stats", {})
        inventory = player.get("inventory", {})
        skills = player.get("skills", {})
        quests = player.get("quests", [])
        
        # Build available actions based on action type
        available_actions = []
        if action_type == PlayerActionType.CHARACTER_CREATION:
            available_actions = ["Melee", "Ranged", "Magic", "Wild"]
        elif action_type == PlayerActionType.COMBAT_DECISION:
            available_actions = ["attack", "defend", "use_item", "flee"]
        elif action_type == PlayerActionType.SKILL_ALLOCATION:
            available_actions = ["strength", "agility", "intelligence", "wisdom", "charisma"]
        elif action_type == PlayerActionType.EXPLORATION_CHOICE:
            available_actions = ["explore", "travel", "search", "rest"]
        
        return GameContext(
            player_level=stats.get("level", 1),
            player_health=stats.get("health", 100),
            player_mana=stats.get("mana", 50),
            current_location=player.get("location", "Unknown"),
            available_actions=available_actions,
            recent_events=self.ai_game_log[-5:] if self.ai_game_log else [],
            inventory=inventory,
            skills=skills,
            quests=quests
        )
    
    def ai_make_decision(self, action_type: PlayerActionType, available_choices: List[str], 
                        additional_context: Optional[Dict[str, Any]] = None) -> PlayerDecision:
        """Have the AI player make a decision"""
        if not self.current_ai_player:
            raise ValueError("No AI player is currently set up")
        
        # Build game context
        context = self._build_game_context(action_type)
        
        # Add additional context if provided
        if additional_context:
            if "combat_situation" in additional_context:
                context.combat_situation = additional_context["combat_situation"]
            if "exploration_options" in additional_context:
                context.exploration_options = additional_context["exploration_options"]
        
        # Make decision
        decision = self.ai_system.make_decision(
            self.current_ai_player.name,
            action_type,
            context,
            available_choices
        )
        
        # Log the decision
        self.ai_game_log.append(f"AI Decision: {decision.action} (Confidence: {decision.confidence:.2f})")
        
        return decision
    
    def ai_make_decision_enhanced(self, action_type: PlayerActionType, available_choices: List[str], 
                                 verbose: bool = True, **kwargs) -> Dict[str, Any]:
        """Make AI decision with enhanced logging showing full thinking process"""
        try:
            # Build game context
            context = self._build_game_context(action_type)
            
            # Add additional context from kwargs
            if 'enemy_info' in kwargs:
                context.combat_situation = kwargs['enemy_info']
            if 'player_health' in kwargs:
                context.player_health = kwargs['player_health']
            if 'available_areas' in kwargs:
                context.exploration_options = kwargs['available_areas']
            
            # Get AI decision with full prompt and response logging
            decision_result = self.ai_system.make_decision_enhanced(
                self.current_ai_player.name,
                action_type,
                context,
                available_choices,
                verbose
            )
            
            # Log the decision
            self.ai_game_log.append({
                'timestamp': time.time(),
                'action_type': action_type.value,
                'available_choices': available_choices,
                'chosen_action': decision_result.action,
                'reasoning': decision_result.reasoning,
                'confidence': decision_result.confidence,
                'context': asdict(context)
            })
            
            return {
                'action': decision_result.action,
                'reasoning': decision_result.reasoning,
                'confidence': decision_result.confidence,
                'alternatives': decision_result.alternatives,
                'metadata': decision_result.metadata,
                'full_prompt': decision_result.metadata.get('full_prompt', ''),
                'full_response': decision_result.metadata.get('full_response', ''),
                'tokens_used': decision_result.metadata.get('tokens_used', 0),
                'response_time': decision_result.metadata.get('response_time', 0)
            }
            
        except Exception as e:
            print(f"❌ Error making AI decision: {e}")
            return {
                'action': available_choices[0] if available_choices else 'unknown',
                'reasoning': f'Fallback: {action_type.value}',
                'confidence': 0.5,
                'alternatives': available_choices[1:] if len(available_choices) > 1 else [],
                'metadata': {},
                'full_prompt': '',
                'full_response': '',
                'tokens_used': 0,
                'response_time': 0
            }
    
    def _analyze_playstyle(self, scenario_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the AI player's playstyle from results"""
        analysis = {
            "aggression_level": 0.0,
            "risk_tolerance": 0.0,
            "optimization_focus": "balanced",
            "preferred_actions": [],
            "decision_patterns": {}
        }
        
        # Analyze decisions across scenarios
        all_decisions = []
        for result in scenario_results:
            all_decisions.extend(result.get("decisions", []))
        
        if all_decisions:
            # Count action preferences
            action_counts = {}
            for decision in all_decisions:
                # Handle different decision types
                action = decision.get("action", "")
                if not action:
                    action = decision.get("chosen_archetype", "")
                if not action:
                    action = decision.get("skill_chosen", "")
                if not action:
                    action = decision.get("chosen_area", "")
                
                if action:
                    action_counts[action] = action_counts.get(action, 0) + 1
            
            analysis["preferred_actions"] = sorted(action_counts.items(), key=lambda x: x[1], reverse=True)
            
            # Analyze confidence levels
            confidences = [d.get("confidence", 0.5) for d in all_decisions]
            if confidences:
                analysis["average_confidence"] = sum(confidences) / len(confidences)
        
        return analysis
    
    def _analyze_playstyle_enhanced(self, scenario_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Enhanced playstyle analysis with detailed patterns"""
        analysis = {
            'average_confidence': 0.0,
            'decision_patterns': {},
            'reasoning_themes': {},
            'response_time_analysis': {},
            'token_usage_analysis': {}
        }
        
        all_decisions = []
        all_confidences = []
        all_response_times = []
        all_tokens = []
        
        # Collect all decisions
        for scenario_result in scenario_results:
            for decision in scenario_result.get('decisions', []):
                all_decisions.append(decision)
                if 'confidence' in decision:
                    all_confidences.append(decision['confidence'])
                if 'response_time' in decision:
                    all_response_times.append(decision['response_time'])
                if 'tokens_used' in decision:
                    all_tokens.append(decision['tokens_used'])
        
        # Calculate average confidence
        if all_confidences:
            analysis['average_confidence'] = sum(all_confidences) / len(all_confidences)
        
        # Analyze decision patterns
        action_counts = {}
        for decision in all_decisions:
            action = decision.get('action', 'unknown')
            action_counts[action] = action_counts.get(action, 0) + 1
        analysis['decision_patterns'] = action_counts
        
        # Analyze reasoning themes
        reasoning_themes = {}
        for decision in all_decisions:
            reasoning = decision.get('reasoning', '').lower()
            # Extract common themes from reasoning
            themes = self._extract_reasoning_themes(reasoning)
            for theme in themes:
                reasoning_themes[theme] = reasoning_themes.get(theme, 0) + 1
        analysis['reasoning_themes'] = reasoning_themes
        
        # Analyze response times
        if all_response_times:
            analysis['response_time_analysis'] = {
                'average': sum(all_response_times) / len(all_response_times),
                'min': min(all_response_times),
                'max': max(all_response_times),
                'total': sum(all_response_times)
            }
        
        # Analyze token usage
        if all_tokens:
            analysis['token_usage_analysis'] = {
                'average': sum(all_tokens) / len(all_tokens),
                'min': min(all_tokens),
                'max': max(all_tokens),
                'total': sum(all_tokens)
            }
        
        return analysis
    
    def _extract_reasoning_themes(self, reasoning: str) -> List[str]:
        """Extract common themes from AI reasoning"""
        themes = []
        reasoning_lower = reasoning.lower()
        
        # Define theme keywords
        theme_keywords = {
            'aggressive': ['attack', 'offensive', 'damage', 'strength', 'power'],
            'defensive': ['defend', 'protect', 'survive', 'caution', 'safety'],
            'strategic': ['plan', 'strategy', 'analyze', 'consider', 'evaluate'],
            'risk_taking': ['risk', 'chance', 'gamble', 'bold', 'daring'],
            'conservative': ['safe', 'careful', 'conservative', 'steady', 'stable'],
            'efficiency': ['efficient', 'optimal', 'best', 'effective', 'productive'],
            'exploration': ['explore', 'discover', 'investigate', 'search', 'find'],
            'social': ['interact', 'talk', 'communicate', 'social', 'relationship']
        }
        
        for theme, keywords in theme_keywords.items():
            for keyword in keywords:
                if keyword in reasoning_lower:
                    themes.append(theme)
                    break
        
        return themes
    
    def _generate_balance_insights(self, scenario_results: List[Dict[str, Any]]) -> List[str]:
        """Generate insights about game balance from AI playtest"""
        insights = []
        
        # Analyze decision patterns
        all_decisions = []
        for result in scenario_results:
            all_decisions.extend(result.get("decisions", []))
        
        if all_decisions:
            # Check for repetitive choices
            action_counts = {}
            for decision in all_decisions:
                # Handle different decision types
                action = decision.get("action", "")
                if not action:
                    action = decision.get("chosen_archetype", "")
                if not action:
                    action = decision.get("skill_chosen", "")
                if not action:
                    action = decision.get("chosen_area", "")
                
                if action:
                    action_counts[action] = action_counts.get(action, 0) + 1
            
            most_common = max(action_counts.items(), key=lambda x: x[1]) if action_counts else None
            if most_common and most_common[1] > len(all_decisions) * 0.6:
                insights.append(f"AI heavily favors '{most_common[0]}' - may indicate balance issue")
            
            # Check confidence patterns
            low_confidence_decisions = [d for d in all_decisions if d.get("confidence", 1.0) < 0.5]
            if len(low_confidence_decisions) > len(all_decisions) * 0.3:
                insights.append("AI shows low confidence in many decisions - may indicate unclear choices")
        
        return insights
    
    def save_playtest_results(self, results: Dict[str, Any], filename: Optional[str] = None) -> str:
        """Save playtest results to a file"""
        if not filename:
            timestamp = int(time.time())
            filename = f"ai_playtest_{results['player_name']}_{timestamp}.json"
        
        filepath = self.base_dir / "ai_simulations" / filename
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"📁 Playtest results saved to: {filepath}")
        return str(filepath)
    
    def get_ai_game_log(self) -> List[str]:
        """Get the current AI game log"""
        return self.ai_game_log.copy()
    
    def clear_ai_game_log(self):
        """Clear the AI game log"""
        self.ai_game_log.clear()

    def run_ai_playtest_enhanced(self, player_name: str, test_scenarios: List[str], verbose: bool = True) -> Dict[str, Any]:
        """Run AI playtest with enhanced logging showing full thinking process"""
        print(f"Starting AI Playtest with '{player_name}'")
        print(f"   Test scenarios: {', '.join(test_scenarios)}")
        print(f"   Verbose logging: {'Enabled' if verbose else 'Disabled'}")
        print()
        
        results = {
            "player_name": player_name,
            "scenarios": test_scenarios,
            "scenario_results": [],
            "overall_playstyle_analysis": {},
            "game_balance_insights": [],
            "ai_performance_metrics": {
                "total_tokens": 0,
                "avg_response_time": 0,
                "success_rate": 0,
                "total_decisions": 0
            }
        }
        
        total_start_time = time.time()
        total_tokens = 0
        response_times = []
        successful_decisions = 0
        total_decisions = 0
        
        for scenario in test_scenarios:
            print(f"--- Running Scenario: {scenario.replace('_', ' ').title()} ---")
            print()
            
            scenario_start_time = time.time()
            scenario_result = self._run_scenario_enhanced(scenario, verbose)
            scenario_duration = time.time() - scenario_start_time
            
            # Track performance metrics
            if 'tokens_used' in scenario_result:
                total_tokens += scenario_result['tokens_used']
            if 'response_time' in scenario_result:
                response_times.append(scenario_result['response_time'])
            if 'decisions' in scenario_result:
                total_decisions += len(scenario_result['decisions'])
                successful_decisions += len([d for d in scenario_result['decisions'] if d.get('success', True)])
            
            scenario_result['duration'] = scenario_duration
            results['scenario_results'].append(scenario_result)
            
            print(f"   Scenario completed in {scenario_duration:.1f}s")
            print()
        
        # Calculate overall metrics
        total_duration = time.time() - total_start_time
        results['ai_performance_metrics'].update({
            "total_tokens": total_tokens,
            "avg_response_time": sum(response_times) / len(response_times) if response_times else 0,
            "success_rate": (successful_decisions / total_decisions * 100) if total_decisions > 0 else 0,
            "total_decisions": total_decisions,
            "total_duration": total_duration
        })
        
        # Analyze playstyle
        results['overall_playstyle_analysis'] = self._analyze_playstyle_enhanced(results['scenario_results'])
        
        # Generate balance insights
        results['game_balance_insights'] = self._generate_balance_insights(results['scenario_results'])
        
        print(f"AI Playtest completed!")
        print(f"   Scenarios tested: {len(results['scenario_results'])}")
        print(f"   Decisions made: {total_decisions}")
        print(f"   Total tokens used: {total_tokens}")
        print(f"   Average response time: {results['ai_performance_metrics']['avg_response_time']:.2f}s")
        print(f"   Success rate: {results['ai_performance_metrics']['success_rate']:.1f}%")
        
        return results
    
    def _run_scenario(self, scenario: str) -> Dict[str, Any]:
        """Run a specific test scenario"""
        scenario_results = {
            "scenario": scenario,
            "decisions": [],
            "outcomes": [],
            "duration": 0
        }
        
        start_time = time.time()
        
        try:
            if scenario == "character_creation":
                result = self.ai_character_creation()
                scenario_results["decisions"].append(result)
                scenario_results["outcomes"].append(f"Created character with {result['chosen_archetype']} archetype")
                
            elif scenario == "combat_test":
                # Create a test monster
                monster = self.game_launcher.monster_system.spawn_monster(5, 5, 5)
                result = self.ai_combat_decision(monster, 100)
                scenario_results["decisions"].append(result)
                scenario_results["outcomes"].append(f"Combat against {monster.get('name', 'Unknown')}")
                
            elif scenario == "skill_allocation":
                result = self.ai_skill_allocation(5)
                scenario_results["decisions"].append(result)
                scenario_results["outcomes"].append(f"Allocated points to {result['skill_chosen']}")
                
            elif scenario == "exploration_test":
                areas = ["Forest", "Cave", "Town", "Dungeon"]
                result = self.ai_exploration_choice(areas)
                scenario_results["decisions"].append(result)
                scenario_results["outcomes"].append(f"Explored {result['chosen_area']}")
                
            elif scenario == "full_gameplay":
                # Run a sequence of scenarios
                scenarios = ["character_creation", "skill_allocation", "combat_test", "exploration_test"]
                for sub_scenario in scenarios:
                    sub_result = self._run_scenario(sub_scenario)
                    scenario_results["decisions"].extend(sub_result["decisions"])
                    
        except Exception as e:
            scenario_results["error"] = str(e)
            
        scenario_results["duration"] = time.time() - start_time
        return scenario_results
    
    def _run_scenario_enhanced(self, scenario: str, verbose: bool = True) -> Dict[str, Any]:
        """Run a single scenario with enhanced logging"""
        result = {
            "scenario": scenario,
            "decisions": [],
            "duration": 0,
            "tokens_used": 0,
            "response_time": 0,
            "average_confidence": 0
        }
        
        if scenario == "character_creation":
            print("AI Player is creating a character...")
            decision_result = self.ai_character_creation_enhanced(verbose)
            
        elif scenario == "combat_test":
            # Create a test enemy
            enemy_info = {
                "name": "Test Enemy",
                "level": 1,
                "health": 100,
                "attack": 15,
                "defense": 5
            }
            print(f"AI Player is making a combat decision...")
            print(f"   Enemy: {enemy_info['name']} (HP: {enemy_info['health']})")
            decision_result = self.ai_combat_decision_enhanced(enemy_info, 100, verbose)
            
        elif scenario == "skill_allocation":
            print("AI Player is allocating skill points...")
            print(f"   Available points: 5")
            decision_result = self.ai_skill_allocation_enhanced(5, verbose)
            
        elif scenario == "exploration_test":
            available_areas = ["Forest", "Cave", "Town", "Mountain"]
            print("AI Player is choosing exploration path...")
            print(f"   Available areas: {', '.join(available_areas)}")
            decision_result = self.ai_exploration_choice_enhanced(available_areas, verbose)
            
        else:
            print(f"Unknown scenario: {scenario}")
            return result
        
        # Extract metrics from decision result
        if 'tokens_used' in decision_result:
            result['tokens_used'] = decision_result['tokens_used']
        if 'response_time' in decision_result:
            result['response_time'] = decision_result['response_time']
        if 'confidence' in decision_result:
            result['average_confidence'] = decision_result['confidence']
        
        result['decisions'].append(decision_result)
        return result
    
    def ai_character_creation(self) -> Dict[str, Any]:
        """Have AI player create a character"""
        print(f"\nAI Player '{self.current_ai_player.name}' is creating a character...")
        
        available_choices = ["Melee", "Ranged", "Magic", "Wild"]
        decision = self.ai_make_decision(PlayerActionType.CHARACTER_CREATION, available_choices)
        
        print(f"   AI chose: {decision.action}")
        print(f"   Reasoning: {decision.reasoning}")
        
        # Create character based on AI choice
        base_archetypes = {decision.action: 3}
        player_data = self.game_launcher.player_system.create_player(
            f"{self.current_ai_player.name}_AI", base_archetypes
        )
        
        self.game_launcher.current_player = player_data
        print(f"AI character '{self.current_ai_player.name}_AI' created successfully!")
        
        return {
            "character_name": f"{self.current_ai_player.name}_AI",
            "chosen_archetype": decision.action,
            "reasoning": decision.reasoning,
            "confidence": decision.confidence
        }
    
    def ai_combat_decision(self, enemy_info: Dict[str, Any], player_health: int) -> Dict[str, Any]:
        """Have AI player make a combat decision"""
        print(f"\nAI Player '{self.current_ai_player.name}' is making a combat decision...")
        
        available_actions = ["attack", "defend", "use_item", "flee"]
        combat_context = {
            "combat_situation": {
                "enemy": enemy_info,
                "player_health": player_health,
                "enemy_health": enemy_info.get("health", 100)
            }
        }
        
        decision = self.ai_make_decision(PlayerActionType.COMBAT_DECISION, available_actions, combat_context)
        
        print(f"   Enemy: {enemy_info.get('name', 'Unknown')} (HP: {enemy_info.get('health', 100)})")
        print(f"   AI chose: {decision.action}")
        print(f"   Reasoning: {decision.reasoning}")
        
        return {
            "action": decision.action,
            "reasoning": decision.reasoning,
            "confidence": decision.confidence,
            "enemy_info": enemy_info
        }
    
    def ai_skill_allocation(self, available_points: int) -> Dict[str, Any]:
        """Have AI player allocate skill points"""
        print(f"\nAI Player '{self.current_ai_player.name}' is allocating skill points...")
        
        available_skills = ["strength", "agility", "intelligence", "wisdom", "charisma"]
        decision = self.ai_make_decision(PlayerActionType.SKILL_ALLOCATION, available_skills)
        
        print(f"   Available points: {available_points}")
        print(f"   AI chose to invest in: {decision.action}")
        print(f"   Reasoning: {decision.reasoning}")
        
        return {
            "skill_chosen": decision.action,
            "reasoning": decision.reasoning,
            "confidence": decision.confidence,
            "available_points": available_points
        }
    
    def ai_exploration_choice(self, available_areas: List[str]) -> Dict[str, Any]:
        """Have AI player make an exploration choice"""
        print(f"\nAI Player '{self.current_ai_player.name}' is choosing where to explore...")
        
        exploration_context = {
            "exploration_options": available_areas
        }
        
        decision = self.ai_make_decision(PlayerActionType.EXPLORATION_CHOICE, available_areas, exploration_context)
        
        print(f"   Available areas: {', '.join(available_areas)}")
        print(f"   AI chose: {decision.action}")
        print(f"   Reasoning: {decision.reasoning}")
        
        return {
            "chosen_area": decision.action,
            "reasoning": decision.reasoning,
            "confidence": decision.confidence,
            "available_areas": available_areas
        }
    
    def ai_character_creation_enhanced(self, verbose: bool = True) -> Dict[str, Any]:
        """AI character creation with enhanced logging"""
        start_time = time.time()
        
        # Get AI decision with full prompt logging
        decision_result = self.ai_make_decision_enhanced(
            PlayerActionType.CHARACTER_CREATION,
            ["Melee", "Ranged", "Magic", "Hybrid"],
            verbose
        )
        
        response_time = time.time() - start_time
        
        # Display full thinking process if verbose
        if verbose and 'full_prompt' in decision_result:
            print(f"   AI Prompt:")
            print(f"   {'='*40}")
            print(decision_result['full_prompt'])
            print(f"   {'='*40}")
            print()
        
        if verbose and 'full_response' in decision_result:
            print(f"   AI Response:")
            print(f"   {'='*40}")
            print(decision_result['full_response'])
            print(f"   {'='*40}")
            print()
        
        print(f"   AI chose: {decision_result.get('action', 'unknown')}")
        print(f"   Reasoning: {decision_result.get('reasoning', 'No reasoning provided')}")
        print()
        
        return {
            'action': decision_result.get('action', 'unknown'),
            'reasoning': decision_result.get('reasoning', ''),
            'confidence': decision_result.get('confidence', 0.5),
            'response_time': response_time,
            'tokens_used': decision_result.get('tokens_used', 0),
            'full_prompt': decision_result.get('full_prompt', ''),
            'full_response': decision_result.get('full_response', ''),
            'success': True
        }
    
    def ai_combat_decision_enhanced(self, enemy_info: Dict[str, Any], player_health: int, verbose: bool = True) -> Dict[str, Any]:
        """AI combat decision with enhanced logging"""
        start_time = time.time()
        
        # Get AI decision with full prompt logging
        decision_result = self.ai_make_decision_enhanced(
            PlayerActionType.COMBAT_DECISION,
            ["attack", "defend", "use_item", "flee"],
            verbose,
            enemy_info=enemy_info,
            player_health=player_health
        )
        
        response_time = time.time() - start_time
        
        # Display full thinking process if verbose
        if verbose and 'full_prompt' in decision_result:
            print(f"   AI Prompt:")
            print(f"   {'='*40}")
            print(decision_result['full_prompt'])
            print(f"   {'='*40}")
            print()
        
        if verbose and 'full_response' in decision_result:
            print(f"   AI Response:")
            print(f"   {'='*40}")
            print(decision_result['full_response'])
            print(f"   {'='*40}")
            print()
        
        print(f"   AI chose: {decision_result.get('action', 'unknown')}")
        print(f"   Reasoning: {decision_result.get('reasoning', 'No reasoning provided')}")
        print()
        
        return {
            'action': decision_result.get('action', 'unknown'),
            'reasoning': decision_result.get('reasoning', ''),
            'confidence': decision_result.get('confidence', 0.5),
            'response_time': response_time,
            'tokens_used': decision_result.get('tokens_used', 0),
            'full_prompt': decision_result.get('full_prompt', ''),
            'full_response': decision_result.get('full_response', ''),
            'success': True
        }
    
    def ai_skill_allocation_enhanced(self, available_points: int, verbose: bool = True) -> Dict[str, Any]:
        """AI skill allocation with enhanced logging"""
        start_time = time.time()
        
        # Get AI decision with full prompt logging
        decision_result = self.ai_make_decision_enhanced(
            PlayerActionType.SKILL_ALLOCATION,
            ["strength", "agility", "intelligence", "wisdom", "charisma"],
            verbose,
            available_points=available_points
        )
        
        response_time = time.time() - start_time
        
        # Display full thinking process if verbose
        if verbose and 'full_prompt' in decision_result:
            print(f"   AI Prompt:")
            print(f"   {'='*40}")
            print(decision_result['full_prompt'])
            print(f"   {'='*40}")
            print()
        
        if verbose and 'full_response' in decision_result:
            print(f"   AI Response:")
            print(f"   {'='*40}")
            print(decision_result['full_response'])
            print(f"   {'='*40}")
            print()
        
        print(f"   AI chose to invest in: {decision_result.get('action', 'unknown')}")
        print(f"   Reasoning: {decision_result.get('reasoning', 'No reasoning provided')}")
        print()
        
        return {
            'action': decision_result.get('action', 'unknown'),
            'reasoning': decision_result.get('reasoning', ''),
            'confidence': decision_result.get('confidence', 0.5),
            'response_time': response_time,
            'tokens_used': decision_result.get('tokens_used', 0),
            'full_prompt': decision_result.get('full_prompt', ''),
            'full_response': decision_result.get('full_response', ''),
            'success': True
        }
    
    def ai_exploration_choice_enhanced(self, available_areas: List[str], verbose: bool = True) -> Dict[str, Any]:
        """AI exploration choice with enhanced logging"""
        start_time = time.time()
        
        # Get AI decision with full prompt logging
        decision_result = self.ai_make_decision_enhanced(
            PlayerActionType.EXPLORATION_CHOICE,
            available_areas,
            verbose,
            available_areas=available_areas
        )
        
        response_time = time.time() - start_time
        
        # Display full thinking process if verbose
        if verbose and 'full_prompt' in decision_result:
            print(f"   AI Prompt:")
            print(f"   {'='*40}")
            print(decision_result['full_prompt'])
            print(f"   {'='*40}")
            print()
        
        if verbose and 'full_response' in decision_result:
            print(f"   AI Response:")
            print(f"   {'='*40}")
            print(decision_result['full_response'])
            print(f"   {'='*40}")
            print()
        
        print(f"   AI chose: {decision_result.get('action', 'unknown')}")
        print(f"   Reasoning: {decision_result.get('reasoning', 'No reasoning provided')}")
        print()
        
        return {
            'action': decision_result.get('action', 'unknown'),
            'reasoning': decision_result.get('reasoning', ''),
            'confidence': decision_result.get('confidence', 0.5),
            'response_time': response_time,
            'tokens_used': decision_result.get('tokens_used', 0),
            'full_prompt': decision_result.get('full_prompt', ''),
            'full_response': decision_result.get('full_response', ''),
            'success': True
        }

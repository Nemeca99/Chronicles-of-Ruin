#!/usr/bin/env python3
"""
AI Playtest Tool for Chronicles of Ruin
Runs AI playtests to evaluate game balance and player behavior
"""

import sys
import os
import json
import argparse
import time
import random
from pathlib import Path
from typing import List, Dict, Any

# Handle Windows console encoding
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# Add the chapter directory to the path
sys.path.append(str(Path(__file__).parent.parent / "chapters" / "chapter_01_sunderfall"))

from ai_player_integration import AIPlayerIntegration
from game_launcher import GameLauncher
from performance_monitor import PerformanceMonitor

# Import the Learning AI Party System
sys.path.append(str(Path(__file__).parent))
from ai_player_system import LearningAIPartySystem

class AIPlaytestTool:
    """Tool for running AI playtests with enhanced logging"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.game_launcher = GameLauncher()
        self.ai_integration = AIPlayerIntegration(self.game_launcher)
        self.performance_monitor = PerformanceMonitor()
        self.verbose_logging = True  # Enable detailed logging
        self.learning_party_system = LearningAIPartySystem(self.base_dir)
        
    def run_learning_party_session(self, scenarios: List[str], session_name: str = None, 
                                 skill_levels: List[str] = None) -> Dict[str, Any]:
        """Run a learning session with a 5-player party"""
        print(f"🎮 LEARNING AI PARTY SYSTEM")
        print(f"=" * 50)
        print(f"Creating 5-player party with different skill levels...")
        
        # Create or load party
        if not self.learning_party_system.party_members:
            print(f"Creating new learning party...")
            party = self.learning_party_system.create_learning_party(skill_levels)
        else:
            print(f"Using existing party...")
            party = self.learning_party_system.party_members
        
        # Run learning session
        results = self.learning_party_system.run_learning_session(scenarios, session_name)
        
        return results
    
    def run_adaptive_testing(self, test_sessions: int = 5, scenarios: List[str] = None) -> Dict[str, Any]:
        """Run multiple learning sessions to test adaptation over time"""
        if scenarios is None:
            scenarios = ["character_creation", "combat_test", "skill_allocation", "exploration_test"]
        
        print(f"🔄 ADAPTIVE TESTING SYSTEM")
        print(f"=" * 50)
        print(f"Running {test_sessions} learning sessions to test AI adaptation...")
        print(f"Scenarios: {', '.join(scenarios)}")
        print()
        
        # Create party if needed
        if not self.learning_party_system.party_members:
            self.learning_party_system.create_learning_party()
        
        adaptive_results = {
            "test_sessions": test_sessions,
            "scenarios": scenarios,
            "sessions": [],
            "adaptation_tracking": {},
            "skill_progression": {},
            "team_evolution": {}
        }
        
        # Track initial state
        initial_state = {}
        for player in self.learning_party_system.party_members:
            initial_state[player.name] = {
                "skill_level": player.skill_level,
                "success_rate": player.get_success_rate(),
                "experience_points": player.experience_points,
                "team_coordination": player.team_coordination
            }
        
        # Run multiple sessions
        for session_num in range(1, test_sessions + 1):
            print(f"\n📊 SESSION {session_num}/{test_sessions}")
            print(f"=" * 30)
            
            session_name = f"adaptive_session_{session_num}"
            session_results = self.learning_party_system.run_learning_session(scenarios, session_name)
            adaptive_results["sessions"].append(session_results)
            
            # Track adaptations
            for player in self.learning_party_system.party_members:
                if player.adaptation_history:
                    latest_adaptation = player.adaptation_history[-1]
                    if player.name not in adaptive_results["adaptation_tracking"]:
                        adaptive_results["adaptation_tracking"][player.name] = []
                    adaptive_results["adaptation_tracking"][player.name].append(latest_adaptation)
            
            # Track skill progression
            for player in self.learning_party_system.party_members:
                if player.name not in adaptive_results["skill_progression"]:
                    adaptive_results["skill_progression"][player.name] = []
                
                adaptive_results["skill_progression"][player.name].append({
                    "session": session_num,
                    "skill_level": player.skill_level,
                    "success_rate": player.get_success_rate(),
                    "experience_points": player.experience_points,
                    "total_decisions": player.total_decisions
                })
            
            # Track team evolution
            team_results = session_results["team_results"]
            adaptive_results["team_evolution"][f"session_{session_num}"] = {
                "coordination_score": team_results["coordination_score"],
                "team_composition": team_results["team_composition"],
                "scenario_success_rates": {
                    scenario: results["success"] 
                    for scenario, results in team_results["scenarios"].items()
                }
            }
        
        # Analyze adaptation patterns
        self._analyze_adaptation_patterns(adaptive_results)
        
        # Display final results
        self._display_adaptive_testing_summary(adaptive_results, initial_state)
        
        return adaptive_results
    
    def _analyze_adaptation_patterns(self, results: Dict[str, Any]):
        """Analyze how AI players adapted over time"""
        print(f"\n🧠 ADAPTATION ANALYSIS")
        print(f"=" * 30)
        
        for player_name, adaptations in results["adaptation_tracking"].items():
            if adaptations:
                print(f"\n{player_name} Adaptations:")
                for i, adaptation in enumerate(adaptations, 1):
                    changes = adaptation.get("changes_made", [])
                    if changes:
                        print(f"  Session {i}: {', '.join(changes)}")
                    else:
                        print(f"  Session {i}: No changes needed")
        
        # Analyze skill progression
        print(f"\n📈 SKILL PROGRESSION:")
        for player_name, progression in results["skill_progression"].items():
            if len(progression) > 1:
                initial = progression[0]
                final = progression[-1]
                
                if initial["skill_level"] != final["skill_level"]:
                    print(f"  {player_name}: {initial['skill_level']} → {final['skill_level']}")
                
                success_improvement = final["success_rate"] - initial["success_rate"]
                if abs(success_improvement) > 0.1:
                    print(f"  {player_name}: Success rate {initial['success_rate']:.1%} → {final['success_rate']:.1%}")
    
    def _display_adaptive_testing_summary(self, results: Dict[str, Any], initial_state: Dict[str, Any]):
        """Display summary of adaptive testing results"""
        print(f"\n📊 ADAPTIVE TESTING SUMMARY")
        print(f"=" * 50)
        print(f"Total Sessions: {results['test_sessions']}")
        print(f"Scenarios Tested: {len(results['scenarios'])}")
        
        # Individual progress
        print(f"\nINDIVIDUAL PROGRESS:")
        for player_name, progression in results["skill_progression"].items():
            if progression:
                initial = progression[0]
                final = progression[-1]
                
                print(f"  {player_name}:")
                print(f"    Skill Level: {initial['skill_level']} → {final['skill_level']}")
                print(f"    Success Rate: {initial['success_rate']:.1%} → {final['success_rate']:.1%}")
                print(f"    Experience: {initial['experience_points']} → {final['experience_points']}")
                print(f"    Decisions: {final['total_decisions']}")
        
        # Team evolution
        print(f"\nTEAM EVOLUTION:")
        team_scores = []
        for session_key, team_data in results["team_evolution"].items():
            team_scores.append(team_data["coordination_score"])
        
        if team_scores:
            avg_coordination = sum(team_scores) / len(team_scores)
            print(f"  Average Team Coordination: {avg_coordination:.2f}")
            print(f"  Coordination Range: {min(team_scores):.2f} - {max(team_scores):.2f}")
        
        # Learning insights
        print(f"\nKEY INSIGHTS:")
        insights = []
        
        # Check for skill progression
        progressed_players = []
        for player_name, progression in results["skill_progression"].items():
            if len(progression) > 1:
                initial = progression[0]
                final = progression[-1]
                if initial["skill_level"] != final["skill_level"]:
                    progressed_players.append(player_name)
        
        if progressed_players:
            insights.append(f"{len(progressed_players)} players progressed in skill level")
        
        # Check for adaptation frequency
        adaptation_counts = {}
        for player_name, adaptations in results["adaptation_tracking"].items():
            adaptation_counts[player_name] = len([a for a in adaptations if a.get("changes_made")])
        
        most_adaptive = max(adaptation_counts.items(), key=lambda x: x[1]) if adaptation_counts else None
        if most_adaptive and most_adaptive[1] > 0:
            insights.append(f"{most_adaptive[0]} was most adaptive with {most_adaptive[1]} strategy changes")
        
        # Check team coordination trends
        if len(team_scores) > 1:
            if team_scores[-1] > team_scores[0]:
                insights.append("Team coordination improved over time")
            elif team_scores[-1] < team_scores[0]:
                insights.append("Team coordination decreased over time")
            else:
                insights.append("Team coordination remained stable")
        
        for insight in insights:
            print(f"  • {insight}")
    
    def run_playtest(self, player_name: str, scenarios: List[str], 
                    save_results: bool = True, output_file: str = None,
                    monitor_performance: bool = True, verbose: bool = True) -> Dict[str, Any]:
        """Run a comprehensive AI playtest with optional performance monitoring"""
        self.verbose_logging = verbose
        
        print(f"AI PLAYTEST TOOL")
        print(f"=" * 50)
        print(f"Player: {player_name}")
        print(f"Scenarios: {', '.join(scenarios)}")
        print(f"Performance Monitoring: {'Enabled' if monitor_performance else 'Disabled'}")
        print(f"Verbose Logging: {'Enabled' if verbose else 'Disabled'}")
        print()
        
        # Start performance monitoring if requested
        if monitor_performance:
            session_name = f"ai_playtest_{player_name}_{int(time.time())}"
            self.performance_monitor.start_monitoring(session_name)
            print(f"Performance monitoring started: {session_name}")
            print(f"Logging CPU/GPU usage and thermal readings per second...")
        
        try:
            # Setup AI player
            if not self.ai_integration.setup_ai_player(player_name):
                return {"success": False, "error": "Failed to setup AI player"}
            
            # Run playtest with enhanced logging
            results = self.ai_integration.run_ai_playtest_enhanced(player_name, scenarios, verbose)
            
            if results.get("success") is False:
                return results
            
            # Display summary
            self._display_results_summary(results)
            
            # Save results if requested
            if save_results:
                filename = output_file or f"ai_playtest_{player_name}_{int(time.time())}.json"
                filepath = self.ai_integration.save_playtest_results(results, filename)
                results["saved_to"] = filepath
            
            return results
            
        finally:
            # Stop performance monitoring
            if monitor_performance:
                self.performance_monitor.stop_monitoring()
                
                # Get and display detailed performance summary
                performance_summary = self.performance_monitor.get_summary()
                if isinstance(performance_summary, dict):
                    print(f"\nDETAILED PERFORMANCE SUMMARY:")
                    print(f"=" * 50)
                    print(f"Duration: {performance_summary['duration_seconds']} seconds")
                    print(f"CPU Usage - Avg: {performance_summary['cpu_percent_avg']}%, Max: {performance_summary['cpu_percent_max']}%")
                    print(f"Memory Usage - Avg: {performance_summary['memory_percent_avg']}%, Max: {performance_summary['memory_percent_max']}%")
                    
                    if performance_summary.get('cpu_temp_avg', 0) > 0:
                        print(f"CPU Temp - Avg: {performance_summary['cpu_temp_avg']}°C, Max: {performance_summary['cpu_temp_max']}°C")
                    if performance_summary.get('gpu_temp_avg', 0) > 0:
                        print(f"GPU Temp - Avg: {performance_summary['gpu_temp_avg']}°C, Max: {performance_summary['gpu_temp_max']}°C")
                    if performance_summary.get('gpu_utilization_avg', 0) > 0:
                        print(f"GPU Utilization - Avg: {performance_summary['gpu_utilization_avg']}%, Max: {performance_summary['gpu_utilization_max']}%")
                    
                    # Show performance trends
                    if 'performance_trends' in performance_summary:
                        print(f"\nPERFORMANCE TRENDS:")
                        trends = performance_summary['performance_trends']
                        if 'cpu_spikes' in trends:
                            print(f"   CPU Spikes: {trends['cpu_spikes']} times")
                        if 'gpu_spikes' in trends:
                            print(f"   GPU Spikes: {trends['gpu_spikes']} times")
                        if 'thermal_thresholds' in trends:
                            print(f"   Thermal Thresholds Exceeded: {trends['thermal_thresholds']} times")
                    
                    # Add performance data to results
                    results["performance_summary"] = performance_summary
    
    def _display_results_summary(self, results: Dict[str, Any]):
        """Display a summary of playtest results with enhanced details"""
        print(f"\nPLAYTEST RESULTS SUMMARY")
        print(f"=" * 50)
        print(f"Player: {results['player_name']}")
        print(f"Scenarios Tested: {len(results['scenario_results'])}")
        print(f"Total Decisions: {len(self.ai_integration.ai_game_log)}")
        
        # Show scenario breakdown with detailed timing
        print(f"\nSCENARIO BREAKDOWN:")
        for scenario_result in results['scenario_results']:
            scenario = scenario_result['scenario']
            decisions = len(scenario_result.get('decisions', []))
            duration = scenario_result.get('duration', 0)
            avg_confidence = scenario_result.get('average_confidence', 0)
            print(f"   • {scenario.replace('_', ' ').title()}: {decisions} decisions ({duration:.1f}s, avg confidence: {avg_confidence:.2f})")
        
        # Show detailed playstyle analysis
        if results.get('overall_playstyle_analysis'):
            analysis = results['overall_playstyle_analysis']
            print(f"\nDETAILED PLAYSTYLE ANALYSIS:")
            if 'average_confidence' in analysis:
                print(f"   Average Confidence: {analysis['average_confidence']:.2f}")
            if 'decision_patterns' in analysis:
                print(f"   Decision Patterns:")
                for pattern, count in analysis['decision_patterns'].items():
                    print(f"     • {pattern}: {count} times")
            if 'reasoning_themes' in analysis:
                print(f"   Reasoning Themes:")
                for theme, count in analysis['reasoning_themes'].items():
                    print(f"     • {theme}: {count} mentions")
        
        # Show balance insights
        if results.get('game_balance_insights'):
            print(f"\nGAME BALANCE INSIGHTS:")
            for insight in results['game_balance_insights']:
                print(f"   • {insight}")
        
        # Show AI performance metrics
        if results.get('ai_performance_metrics'):
            metrics = results['ai_performance_metrics']
            print(f"\nAI PERFORMANCE METRICS:")
            print(f"   Average Response Time: {metrics.get('avg_response_time', 0):.2f}s")
            print(f"   Total Tokens Used: {metrics.get('total_tokens', 0)}")
            print(f"   Decision Success Rate: {metrics.get('success_rate', 0):.1f}%")
    
    def run_quick_test(self, player_name: str) -> Dict[str, Any]:
        """Run a quick test with basic scenarios"""
        scenarios = ["character_creation", "combat_test", "skill_allocation"]
        return self.run_playtest(player_name, scenarios, save_results=False, monitor_performance=True)
    
    def run_comprehensive_test(self, player_name: str) -> Dict[str, Any]:
        """Run a comprehensive test with all scenarios"""
        scenarios = ["character_creation", "combat_test", "skill_allocation", 
                   "exploration_test", "full_gameplay"]
        return self.run_playtest(player_name, scenarios, save_results=True, monitor_performance=True)
    
    def compare_players(self, player_names: List[str], scenarios: List[str]) -> Dict[str, Any]:
        """Compare multiple AI players"""
        print(f"COMPARING AI PLAYERS")
        print(f"=" * 50)
        print(f"Players: {', '.join(player_names)}")
        print(f"Scenarios: {', '.join(scenarios)}")
        print()
        
        comparison_results = {
            "players": player_names,
            "scenarios": scenarios,
            "player_results": {},
            "comparison_analysis": {}
        }
        
        for player_name in player_names:
            print(f"\n--- Testing {player_name} ---")
            result = self.run_playtest(player_name, scenarios, save_results=False, monitor_performance=True)
            comparison_results["player_results"][player_name] = result
            
            # Clear game log for next player
            self.ai_integration.clear_ai_game_log()
        
        # Analyze comparisons
        comparison_results["comparison_analysis"] = self._analyze_player_comparisons(
            comparison_results["player_results"]
        )
        
        # Display comparison summary
        self._display_comparison_summary(comparison_results)
        
        return comparison_results
    
    def _analyze_player_comparisons(self, player_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze differences between players"""
        analysis = {
            "decision_patterns": {},
            "confidence_comparison": {},
            "playstyle_differences": []
        }
        
        # Compare decision patterns
        all_decisions = {}
        for player_name, results in player_results.items():
            decisions = []
            for scenario_result in results.get('scenario_results', []):
                decisions.extend(scenario_result.get('decisions', []))
            
            action_counts = {}
            for decision in decisions:
                action = decision.get('action', '')
                action_counts[action] = action_counts.get(action, 0) + 1
            
            all_decisions[player_name] = action_counts
        
        analysis["decision_patterns"] = all_decisions
        
        # Compare confidence levels
        confidence_levels = {}
        for player_name, results in player_results.items():
            confidences = []
            for scenario_result in results.get('scenario_results', []):
                for decision in scenario_result.get('decisions', []):
                    confidences.append(decision.get('confidence', 0.5))
            
            if confidences:
                confidence_levels[player_name] = sum(confidences) / len(confidences)
        
        analysis["confidence_comparison"] = confidence_levels
        
        return analysis
    
    def _display_comparison_summary(self, comparison_results: Dict[str, Any]):
        """Display comparison summary"""
        print(f"\nCOMPARISON SUMMARY")
        print(f"=" * 50)
        
        # Show confidence comparison
        confidence_comparison = comparison_results["comparison_analysis"]["confidence_comparison"]
        if confidence_comparison:
            print(f"\nCONFIDENCE COMPARISON:")
            for player, confidence in sorted(confidence_comparison.items(), 
                                          key=lambda x: x[1], reverse=True):
                print(f"   • {player}: {confidence:.2f}")
        
        # Show decision pattern differences
        decision_patterns = comparison_results["comparison_analysis"]["decision_patterns"]
        if decision_patterns:
            print(f"\nDECISION PATTERN COMPARISON:")
            all_actions = set()
            for patterns in decision_patterns.values():
                all_actions.update(patterns.keys())
            
            for action in sorted(all_actions):
                print(f"   {action}:")
                for player, patterns in decision_patterns.items():
                    count = patterns.get(action, 0)
                    print(f"     • {player}: {count} times")

    def demo_learning_party(self):
        """Demo the Learning AI Party System"""
        print(f"🎮 LEARNING AI PARTY SYSTEM DEMO")
        print(f"=" * 50)
        
        # Create a learning party
        party = self.learning_party_system.create_learning_party()
        
        print(f"Created 5-player party:")
        for i, player in enumerate(party, 1):
            print(f"  {i}. {player.name} ({player.skill_level} {player.team_role})")
            print(f"     Playstyle: {player.playstyle}, Personality: {player.personality}")
            print(f"     Success Rate: {player.get_success_rate():.1%}")
        print()
        
        # Run a simple learning session
        scenarios = ["character_creation", "combat_test"]
        results = self.learning_party_system.run_learning_session(scenarios, "demo_session")
        
        print(f"✅ Learning AI Party System demo completed!")
        return results

def main():
    """Main function"""
    
    parser = argparse.ArgumentParser(description="AI Playtest Tool for Chronicles of Ruin")
    parser.add_argument("action", choices=["playtest", "quick", "comprehensive", "compare", "adaptive", "demo"],
                       help="Action to perform")
    parser.add_argument("--player", type=str, help="AI player name")
    parser.add_argument("--players", nargs="+", help="Multiple AI player names for comparison")
    parser.add_argument("--scenarios", nargs="+", 
                       choices=["character_creation", "combat_test", "skill_allocation", 
                               "exploration_test", "full_gameplay"],
                       help="Scenarios to test")
    parser.add_argument("--output", type=str, help="Output filename for results")
    parser.add_argument("--no-save", action="store_true", help="Don't save results")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--test-sessions", type=int, help="Number of test sessions for adaptive testing")
    
    args = parser.parse_args()
    
    tool = AIPlaytestTool()
    
    try:
        if args.action == "playtest":
            if not args.player:
                print("❌ --player required for playtest action")
                return
            
            # Default scenarios if none provided
            scenarios = args.scenarios if args.scenarios else ["character_creation", "combat_test", "skill_allocation"]
            
            results = tool.run_playtest(
                args.player, 
                scenarios,
                save_results=not args.no_save,
                output_file=args.output,
                monitor_performance=True,
                verbose=args.verbose
            )
            
        elif args.action == "quick":
            if not args.player:
                print("❌ --player required for quick action")
                return
            
            results = tool.run_quick_test(args.player)
            
        elif args.action == "comprehensive":
            if not args.player:
                print("❌ --player required for comprehensive action")
                return
            
            results = tool.run_comprehensive_test(args.player)
            
        elif args.action == "compare":
            if not args.players or not args.scenarios:
                print("❌ --players and --scenarios required for compare action")
                return
            
            results = tool.compare_players(args.players, args.scenarios)
            
        elif args.action == "adaptive":
            # Default scenarios if none provided
            scenarios = args.scenarios if args.scenarios else ["character_creation", "combat_test", "skill_allocation", "exploration_test"]
            
            # Default test_sessions if not provided
            test_sessions = args.test_sessions if args.test_sessions else 5
            
            results = tool.run_adaptive_testing(test_sessions, scenarios)
            
        elif args.action == "demo":
            results = tool.demo_learning_party()
            
        print(f"\nAI Playtest completed successfully!")
        
    except Exception as e:
        print(f"Error running AI playtest: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

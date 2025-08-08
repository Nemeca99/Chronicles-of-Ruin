#!/usr/bin/env python3
"""
AI Player Tool - Chronicles of Ruin
CLI tool for testing and managing AI player simulations
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Optional, List, Dict, Any

# Add the tools directory to the path
sys.path.append(str(Path(__file__).parent))

from ai_player_system import AIPlayerSystem, PlayerActionType, GameContext


class AIPlayerTool:
    """CLI tool for AI Player System management"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.ai_system = AIPlayerSystem(self.base_dir)
        
    def show_menu(self):
        """Show the main menu"""
        print("\n=== AI PLAYER SYSTEM ===")
        print("1. Create AI Player Profile")
        print("2. List AI Players")
        print("3. Run Character Creation Simulation")
        print("4. Run Combat Decision Simulation")
        print("5. Run Skill Allocation Simulation")
        print("6. Run Exploration Simulation")
        print("7. View Decision History")
        print("8. Create Sample AI Players")
        print("9. Test Ollama Connection")
        print("0. Exit")
        print()
    
    def create_ai_player(self):
        """Create a new AI player profile"""
        print("\n=== CREATE AI PLAYER PROFILE ===")
        
        name = input("Player Name: ").strip()
        if not name:
            print("Error: Name is required")
            return
        
        print("\nPlaystyle Options:")
        print("1. aggressive - Focus on damage and speed")
        print("2. defensive - Focus on survival and protection")
        print("3. balanced - Mix of offense and defense")
        print("4. explorer - Focus on discovery and utility")
        print("5. minmaxer - Focus on optimization")
        
        playstyle_choice = input("Choose playstyle (1-5): ").strip()
        playstyles = ["aggressive", "defensive", "balanced", "explorer", "minmaxer"]
        playstyle = playstyles[int(playstyle_choice) - 1] if playstyle_choice.isdigit() and 1 <= int(playstyle_choice) <= 5 else "balanced"
        
        print("\nPersonality Options:")
        print("1. risk_taker - Makes bold decisions")
        print("2. cautious - Prefers safe choices")
        print("3. strategic - Plans ahead")
        print("4. impulsive - Acts on instinct")
        
        personality_choice = input("Choose personality (1-4): ").strip()
        personalities = ["risk_taker", "cautious", "strategic", "impulsive"]
        personality = personalities[int(personality_choice) - 1] if personality_choice.isdigit() and 1 <= int(personality_choice) <= 4 else "strategic"
        
        print("\nPreferred Archetype:")
        print("1. melee - Close combat")
        print("2. ranged - Distance fighting")
        print("3. magic - Spellcasting")
        print("4. hybrid - Mixed approach")
        
        archetype_choice = input("Choose archetype (1-4): ").strip()
        archetypes = ["melee", "ranged", "magic", "hybrid"]
        preferred_archetype = archetypes[int(archetype_choice) - 1] if archetype_choice.isdigit() and 1 <= int(archetype_choice) <= 4 else "hybrid"
        
        print("\nDecision Style:")
        print("1. analytical - Detailed analysis")
        print("2. intuitive - Gut feeling")
        print("3. conservative - Safe choices")
        print("4. experimental - Tries new things")
        
        decision_choice = input("Choose decision style (1-4): ").strip()
        decision_styles = ["analytical", "intuitive", "conservative", "experimental"]
        decision_style = decision_styles[int(decision_choice) - 1] if decision_choice.isdigit() and 1 <= int(decision_choice) <= 4 else "analytical"
        
        risk_tolerance = float(input("Risk Tolerance (0.0-1.0, default 0.5): ").strip() or "0.5")
        patience_level = float(input("Patience Level (0.0-1.0, default 0.5): ").strip() or "0.5")
        
        print("\nOptimization Focus:")
        print("1. damage - Maximize attack power")
        print("2. survival - Maximize survivability")
        print("3. utility - Maximize versatility")
        print("4. balanced - Mix of all types")
        
        focus_choice = input("Choose optimization focus (1-4): ").strip()
        focus_options = ["damage", "survival", "utility", "balanced"]
        optimization_focus = focus_options[int(focus_choice) - 1] if focus_choice.isdigit() and 1 <= int(focus_choice) <= 4 else "balanced"
        
        # Create the profile
        profile = self.ai_system.create_ai_player_profile(
            name=name,
            playstyle=playstyle,
            personality=personality,
            preferred_archetype=preferred_archetype,
            decision_style=decision_style,
            risk_tolerance=risk_tolerance,
            patience_level=patience_level,
            optimization_focus=optimization_focus
        )
        
        print(f"\nCreated AI player profile: {profile.name}")
        print(f"Playstyle: {profile.playstyle}")
        print(f"Personality: {profile.personality}")
        print(f"Preferred Archetype: {profile.preferred_archetype}")
    
    def list_ai_players(self):
        """List all AI players"""
        print("\n=== AI PLAYERS ===")
        players = self.ai_system.list_ai_players()
        
        if not players:
            print("No AI players found.")
            return
        
        for i, player_name in enumerate(players, 1):
            profile = self.ai_system.get_ai_player_profile(player_name)
            if profile:
                print(f"{i}. {profile.name}")
                print(f"   Playstyle: {profile.playstyle}")
                print(f"   Personality: {profile.personality}")
                print(f"   Preferred Archetype: {profile.preferred_archetype}")
                print(f"   Risk Tolerance: {profile.risk_tolerance}")
                print(f"   Patience Level: {profile.patience_level}")
                print()
    
    def run_character_creation_simulation(self):
        """Run character creation simulation"""
        print("\n=== CHARACTER CREATION SIMULATION ===")
        
        # List available players
        players = self.ai_system.list_ai_players()
        if not players:
            print("No AI players found. Create some first.")
            return
        
        print("Available AI Players:")
        for i, player_name in enumerate(players, 1):
            print(f"{i}. {player_name}")
        
        choice = input("\nSelect player (number): ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(players):
            print("Invalid choice")
            return
        
        player_name = players[int(choice) - 1]
        
        print(f"\nRunning character creation simulation for {player_name}...")
        
        # Run simulation
        result = self.ai_system.run_simulation(player_name, "character_creation")
        
        if "error" in result:
            print(f"Error: {result['error']}")
            if result.get("fallback"):
                print("Using fallback decision system")
        else:
            print("Simulation completed!")
            for decision in result["decisions"]:
                print(f"\nDecision Type: {decision['type']}")
                print(f"Action: {decision['decision']['action']}")
                print(f"Reasoning: {decision['decision']['reasoning']}")
                print(f"Confidence: {decision['decision']['confidence']}")
    
    def run_combat_decision_simulation(self):
        """Run combat decision simulation"""
        print("\n=== COMBAT DECISION SIMULATION ===")
        
        # List available players
        players = self.ai_system.list_ai_players()
        if not players:
            print("No AI players found. Create some first.")
            return
        
        print("Available AI Players:")
        for i, player_name in enumerate(players, 1):
            print(f"{i}. {player_name}")
        
        choice = input("\nSelect player (number): ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(players):
            print("Invalid choice")
            return
        
        player_name = players[int(choice) - 1]
        
        # Get simulation parameters
        enemy_name = input("Enemy name (default: Goblin): ").strip() or "Goblin"
        enemy_level = int(input("Enemy level (default: 5): ").strip() or "5")
        player_health = int(input("Player health (default: 80): ").strip() or "80")
        
        print("\nAvailable actions:")
        actions = ["attack", "defend", "use_item", "flee"]
        for i, action in enumerate(actions, 1):
            print(f"{i}. {action}")
        
        action_choice = input("Select actions to include (comma-separated numbers, default: all): ").strip()
        if action_choice:
            try:
                indices = [int(x.strip()) - 1 for x in action_choice.split(",")]
                available_actions = [actions[i] for i in indices if 0 <= i < len(actions)]
            except:
                available_actions = actions
        else:
            available_actions = actions
        
        print(f"\nRunning combat simulation for {player_name}...")
        print(f"Enemy: {enemy_name} (Level {enemy_level})")
        print(f"Player Health: {player_health}")
        print(f"Available Actions: {', '.join(available_actions)}")
        
        # Run simulation
        enemy_info = {"name": enemy_name, "level": enemy_level}
        result = self.ai_system.run_simulation(
            player_name, "combat_scenario",
            enemy_info=enemy_info,
            available_actions=available_actions,
            player_health=player_health
        )
        
        if "error" in result:
            print(f"Error: {result['error']}")
            if result.get("fallback"):
                print("Using fallback decision system")
        else:
            print("Simulation completed!")
            for decision in result["decisions"]:
                print(f"\nDecision Type: {decision['type']}")
                print(f"Action: {decision['decision']['action']}")
                print(f"Reasoning: {decision['decision']['reasoning']}")
                print(f"Confidence: {decision['decision']['confidence']}")
    
    def run_skill_allocation_simulation(self):
        """Run skill allocation simulation"""
        print("\n=== SKILL ALLOCATION SIMULATION ===")
        
        # List available players
        players = self.ai_system.list_ai_players()
        if not players:
            print("No AI players found. Create some first.")
            return
        
        print("Available AI Players:")
        for i, player_name in enumerate(players, 1):
            print(f"{i}. {player_name}")
        
        choice = input("\nSelect player (number): ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(players):
            print("Invalid choice")
            return
        
        player_name = players[int(choice) - 1]
        
        # Get simulation parameters
        available_points = int(input("Available skill points (default: 5): ").strip() or "5")
        
        print(f"\nRunning skill allocation simulation for {player_name}...")
        print(f"Available Points: {available_points}")
        
        # Run simulation
        result = self.ai_system.run_simulation(
            player_name, "skill_allocation",
            available_points=available_points,
            current_skills={}
        )
        
        if "error" in result:
            print(f"Error: {result['error']}")
            if result.get("fallback"):
                print("Using fallback decision system")
        else:
            print("Simulation completed!")
            for decision in result["decisions"]:
                print(f"\nDecision Type: {decision['type']}")
                print(f"Action: {decision['decision']['action']}")
                print(f"Reasoning: {decision['decision']['reasoning']}")
                print(f"Confidence: {decision['decision']['confidence']}")
    
    def run_exploration_simulation(self):
        """Run exploration simulation"""
        print("\n=== EXPLORATION SIMULATION ===")
        
        # List available players
        players = self.ai_system.list_ai_players()
        if not players:
            print("No AI players found. Create some first.")
            return
        
        print("Available AI Players:")
        for i, player_name in enumerate(players, 1):
            print(f"{i}. {player_name}")
        
        choice = input("\nSelect player (number): ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(players):
            print("Invalid choice")
            return
        
        player_name = players[int(choice) - 1]
        
        # Get simulation parameters
        current_location = input("Current location (default: Starting Area): ").strip() or "Starting Area"
        
        print("\nAvailable areas:")
        areas = ["Forest", "Cave", "Town", "Dungeon", "Mountain"]
        for i, area in enumerate(areas, 1):
            print(f"{i}. {area}")
        
        area_choice = input("Select areas to include (comma-separated numbers, default: all): ").strip()
        if area_choice:
            try:
                indices = [int(x.strip()) - 1 for x in area_choice.split(",")]
                available_areas = [areas[i] for i in indices if 0 <= i < len(areas)]
            except:
                available_areas = areas
        else:
            available_areas = areas
        
        print(f"\nRunning exploration simulation for {player_name}...")
        print(f"Current Location: {current_location}")
        print(f"Available Areas: {', '.join(available_areas)}")
        
        # Run simulation
        result = self.ai_system.run_simulation(
            player_name, "exploration",
            available_areas=available_areas,
            current_location=current_location
        )
        
        if "error" in result:
            print(f"Error: {result['error']}")
            if result.get("fallback"):
                print("Using fallback decision system")
        else:
            print("Simulation completed!")
            for decision in result["decisions"]:
                print(f"\nDecision Type: {decision['type']}")
                print(f"Action: {decision['decision']['action']}")
                print(f"Reasoning: {decision['decision']['reasoning']}")
                print(f"Confidence: {decision['decision']['confidence']}")
    
    def view_decision_history(self):
        """View decision history for an AI player"""
        print("\n=== DECISION HISTORY ===")
        
        # List available players
        players = self.ai_system.list_ai_players()
        if not players:
            print("No AI players found.")
            return
        
        print("Available AI Players:")
        for i, player_name in enumerate(players, 1):
            print(f"{i}. {player_name}")
        
        choice = input("\nSelect player (number): ").strip()
        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(players):
            print("Invalid choice")
            return
        
        player_name = players[int(choice) - 1]
        
        # Get history limit
        limit = int(input("Number of recent decisions to show (default: 10): ").strip() or "10")
        
        print(f"\nDecision History for {player_name}:")
        history = self.ai_system.get_decision_history(player_name, limit)
        
        if not history:
            print("No decision history found.")
            return
        
        for i, decision in enumerate(history, 1):
            print(f"\n{i}. {decision['action_type']}")
            print(f"   Action: {decision['decision']['action']}")
            print(f"   Reasoning: {decision['decision']['reasoning']}")
            print(f"   Confidence: {decision['decision']['confidence']}")
            print(f"   Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(decision['timestamp']))}")
    
    def create_sample_players(self):
        """Create sample AI players"""
        print("\n=== CREATING SAMPLE AI PLAYERS ===")
        
        self.ai_system.create_sample_ai_players()
        print("Created sample AI players:")
        print("- Alex (Aggressive, Risk-taker, Melee)")
        print("- Sam (Defensive, Cautious, Magic)")
        print("- Jordan (Balanced, Strategic, Hybrid)")
        print("- Casey (Explorer, Curious, Ranged)")
    
    def test_ollama_connection(self):
        """Test Ollama connection"""
        print("\n=== TESTING OLLAMA CONNECTION ===")
        
        if self.ai_system.check_ollama_connection():
            print("✓ Ollama is running and accessible")
            print(f"Model: {self.ai_system.model_name}")
            print(f"URL: {self.ai_system.ollama_url}")
        else:
            print("✗ Ollama is not accessible")
            print("Make sure Ollama is running and the model is available")
    
    def run(self):
        """Run the AI Player Tool"""
        while True:
            self.show_menu()
            choice = input("Enter your choice (0-9): ").strip()
            
            if choice == "0":
                print("Exiting AI Player Tool...")
                break
            elif choice == "1":
                self.create_ai_player()
            elif choice == "2":
                self.list_ai_players()
            elif choice == "3":
                self.run_character_creation_simulation()
            elif choice == "4":
                self.run_combat_decision_simulation()
            elif choice == "5":
                self.run_skill_allocation_simulation()
            elif choice == "6":
                self.run_exploration_simulation()
            elif choice == "7":
                self.view_decision_history()
            elif choice == "8":
                self.create_sample_players()
            elif choice == "9":
                self.test_ollama_connection()
            else:
                print("Invalid choice. Please enter a number between 0 and 9.")
            
            input("\nPress Enter to continue...")


def main():
    """Main function"""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="AI Player Tool for Chronicles of Ruin")
    parser.add_argument("--base-dir", type=str, default=".", help="Base directory for data")
    parser.add_argument("--action", choices=["interactive", "create-profile", "simulate", "list", "history", "samples", "test"], 
                       default="interactive", help="Action to perform")
    parser.add_argument("--player-name", type=str, help="AI player name")
    parser.add_argument("--simulation-type", type=str, help="Type of simulation to run")
    parser.add_argument("--enemy_name", type=str, help="Enemy name for combat simulation")
    parser.add_argument("--enemy_level", type=int, help="Enemy level for combat simulation")
    parser.add_argument("--player_health", type=int, help="Player health for combat simulation")
    parser.add_argument("--available_points", type=int, help="Available skill points for skill allocation")
    parser.add_argument("--available_areas", type=str, help="Available areas for exploration (comma-separated)")
    parser.add_argument("--current_location", type=str, help="Current location for exploration")
    
    # Handle positional arguments for dev_master.py integration
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        # Positional arguments from dev_master.py
        action = sys.argv[1]
        if action == "list":
            sys.argv[1] = "--action"
            sys.argv.insert(2, "list")
        elif action == "samples":
            sys.argv[1] = "--action"
            sys.argv.insert(2, "samples")
        elif action == "test":
            sys.argv[1] = "--action"
            sys.argv.insert(2, "test")
        elif action == "create-profile":
            sys.argv[1] = "--action"
            sys.argv.insert(2, "create-profile")
            if len(sys.argv) > 3:
                sys.argv.insert(3, "--player-name")
                sys.argv.insert(5, sys.argv[4])
                sys.argv.pop(4)
        elif action == "simulate":
            sys.argv[1] = "--action"
            sys.argv.insert(2, "simulate")
            if len(sys.argv) > 3:
                sys.argv.insert(3, "--player-name")
                sys.argv.insert(5, "--simulation-type")
                sys.argv.insert(7, sys.argv[6])
                sys.argv.pop(6)
        elif action == "history":
            sys.argv[1] = "--action"
            sys.argv.insert(2, "history")
            if len(sys.argv) > 3:
                sys.argv.insert(3, "--player-name")
    
    args = parser.parse_args()
    
    tool = AIPlayerTool(Path(args.base_dir))
    
    if args.action == "interactive":
        tool.run()
    elif args.action == "create-profile":
        if not args.player_name:
            print("Error: --player-name required for create-profile")
            return
        tool.create_ai_player()
    elif args.action == "simulate":
        if not args.player_name or not args.simulation_type:
            print("Error: --player-name and --simulation-type required for simulate")
            return
        
        # Build kwargs based on simulation type
        kwargs = {}
        if args.simulation_type == "combat_scenario":
            if args.enemy_name:
                kwargs["enemy_info"] = {"name": args.enemy_name, "level": args.enemy_level or 5}
            if args.player_health:
                kwargs["player_health"] = args.player_health
            kwargs["available_actions"] = ["attack", "defend", "use_item", "flee"]
        elif args.simulation_type == "skill_allocation":
            if args.available_points:
                kwargs["available_points"] = args.available_points
            kwargs["current_skills"] = {}
        elif args.simulation_type == "exploration":
            if args.available_areas:
                kwargs["available_areas"] = args.available_areas.split(",")
            if args.current_location:
                kwargs["current_location"] = args.current_location
        
        result = tool.ai_system.run_simulation(args.player_name, args.simulation_type, **kwargs)
        print(f"Simulation result: {json.dumps(result, indent=2)}")
    elif args.action == "list":
        tool.list_ai_players()
    elif args.action == "history":
        if not args.player_name:
            print("Error: --player-name required for history")
            return
        history = tool.ai_system.get_decision_history(args.player_name)
        print(f"Decision history for {args.player_name}:")
        for decision in history[-5:]:
            print(f"  {decision['action_type']}: {decision['decision']['action']}")
    elif args.action == "samples":
        tool.create_sample_players()
    elif args.action == "test":
        tool.test_ollama_connection()
    elif args.action == "history":
        if not args.player_name:
            print("Error: --player-name required for history")
            return
        history = tool.ai_system.get_decision_history(args.player_name)
        print(f"Decision history for {args.player_name}:")
        for decision in history[-5:]:
            print(f"  {decision['action_type']}: {decision['decision']['action']}")
    elif args.action == "samples":
        tool.create_sample_players()
    elif args.action == "test":
        tool.test_ollama_connection()


if __name__ == "__main__":
    main()

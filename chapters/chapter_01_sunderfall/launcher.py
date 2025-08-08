#!/usr/bin/env python3
"""
CHRONICLES OF RUIN: SUNDERFALL LAUNCHER
========================================

This is the main launcher script for the Chronicles of Ruin: Sunderfall game.
It handles initialization, configuration loading, and game startup.

USAGE:
    python launcher.py [options]

OPTIONS:
    --debug     Enable debug mode
    --fullscreen    Launch in fullscreen mode
    --config <file> Use custom config file
    --help      Show this help message
"""

import sys
import os
import argparse
import json
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))


def load_config(config_path=None):
    """Load game configuration."""
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), "config.json")

    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load config from {config_path}: {e}")

    # Default configuration
    return {
        "project_name": "Chronicles of Ruin: Sunderfall",
        "version": "0.1.0",
        "game_settings": {
            "window_width": 1280,
            "window_height": 720,
            "fps": 60,
            "fullscreen": False,
        },
        "development": {"debug_mode": False, "log_level": "INFO"},
    }


def validate_environment():
    """Validate that all required files and directories exist."""
    print("Validating game environment...")

    required_files = [
        "src/core/sunderfall.py",
        "config.json",
        "src/tools/build_tool_cli.py",
    ]

    required_dirs = [
        "src",
        "src/core",
        "src/systems",
        "src/tools",
        "data",
        "assets",
        "docs",
    ]

    errors = []

    # Check required files
    for file_path in required_files:
        if not os.path.exists(file_path):
            errors.append(f"Missing required file: {file_path}")

    # Check required directories
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            errors.append(f"Missing required directory: {dir_path}")

    if errors:
        print("❌ Environment validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False

    print("✅ Environment validation passed!")
    return True


def main():
    """Main launcher function."""
    parser = argparse.ArgumentParser(
        description="Chronicles of Ruin: Sunderfall Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launcher.py                    # Launch with default settings
  python launcher.py --debug           # Launch in debug mode
  python launcher.py --fullscreen      # Launch in fullscreen
  python launcher.py --config custom.json  # Use custom config
        """,
    )

    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument(
        "--fullscreen", action="store_true", help="Launch in fullscreen mode"
    )
    parser.add_argument("--config", type=str, help="Path to custom config file")
    parser.add_argument(
        "--validate", action="store_true", help="Validate environment and exit"
    )
    parser.add_argument(
        "--test", action="store_true", help="Run autonomous testing mode"
    )
    parser.add_argument(
        "--demo", action="store_true", help="Run demo mode with automated gameplay"
    )
    parser.add_argument(
        "--simulation",
        type=str,
        choices=[
            "new_player",
            "combat_focused",
            "exploration",
            "multiplayer",
            "full_gameplay",
        ],
        help="Run specific gameplay simulation",
    )

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)

    # Override config with command line arguments
    if args.debug:
        config["development"]["debug_mode"] = True
    if args.fullscreen:
        config["game_settings"]["fullscreen"] = True

    # Validate environment
    if not validate_environment():
        print("❌ Cannot launch game due to missing files/directories.")
        print("Please run: python src/tools/build_tool_cli.py setup")
        sys.exit(1)

    if args.validate:
        print("✅ Environment validation completed successfully!")
        sys.exit(0)

    # Handle autonomous testing modes
    if args.test:
        print("🤖 Running autonomous testing mode...")
        try:
            from tests.test_runner import TestRunner

            runner = TestRunner()
            runner.run("quick", generate_report=True)
            sys.exit(0)
        except Exception as e:
            print(f"❌ Testing failed: {e}")
            sys.exit(1)

    if args.demo:
        print("🎮 Running demo mode...")
        try:
            from tests.autonomous_test import AutonomousTester

            tester = AutonomousTester()
            tester.run_demo()
            sys.exit(0)
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            sys.exit(1)

    if args.simulation:
        print(f"🎮 Running {args.simulation} simulation...")
        try:
            from tests.game_simulation import GameSimulator

            simulator = GameSimulator()
            simulator.run(args.simulation)
            sys.exit(0)
        except Exception as e:
            print(f"❌ Simulation failed: {e}")
            sys.exit(1)

    # Launch the game
    print(f"🚀 Launching {config['project_name']} v{config['version']}")
    print(f"📁 Working directory: {os.getcwd()}")

    try:
        # Import and run the main game
        from core.sunderfall import SunderfallGame

        game = SunderfallGame(config)
        game.run()

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all required modules are available.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Game launch failed: {e}")
        if config["development"]["debug_mode"]:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

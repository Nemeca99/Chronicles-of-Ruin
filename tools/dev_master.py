#!/usr/bin/env python3
"""
Master Development Script for Chronicles of Ruin Saga
Unified interface for all development tools and build system.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

class DevMaster:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.tools_dir = self.root_dir / "tools"
        
        # Available tools
        self.tools = {
            "build": "build_system.py",
            "saga": "saga_manager.py",
            "dev": "dev_tools.py",
            "cross": "cross_chapter_features.py",
            "build_cli": "build_tool_cli.py",
            "sd": "stable_diffusion_tool.py",
            "img": "simple_image_generator.py",
            "npc": "npc_ai_system.py",
            "discord": "discord_bot_system.py",
            "balance": "balance_testing_tool.py",
            "set_manager": "set_item_manager.py",
            "perf": "performance_optimizer.py",
            "boss": "boss_encounter_tool.py",
            "ai_player": "ai_player_tool.py",
            "ai_playtest": "ai_playtest_tool.py",
        "performance": "performance_monitor.py"
        }
    
    def run_tool(self, tool_name: str, *args) -> bool:
        """Run a specific tool with arguments."""
        if tool_name not in self.tools:
            print(f"Unknown tool: {tool_name}")
            print(f"Available tools: {', '.join(self.tools.keys())}")
            return False
        
        tool_path = self.tools_dir / self.tools[tool_name]
        if not tool_path.exists():
            print(f"Tool not found: {tool_path}")
            return False
        
        # Use venv Python to avoid environment issues
        python_exe = self.root_dir / "venv" / "Scripts" / "python.exe"
        if not python_exe.exists():
            python_exe = "python"  # Fallback
        
        cmd = [str(python_exe), str(tool_path)] + list(args)
        
        try:
            result = subprocess.run(cmd, cwd=self.root_dir, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
            return result.returncode == 0
        except Exception as e:
            print(f"Failed to run {tool_name}: {e}")
            return False
    
    def build_all(self) -> bool:
        """Build all chapters and run tests."""
        print("=== Building Chronicles of Ruin Saga ===")
        return self.run_tool("build", "all")
    
    def build_chapter(self, chapter_name: str) -> bool:
        """Build a specific chapter."""
        return self.run_tool("build", "chapter", chapter_name)
    
    def run_chapter(self, chapter_name: str) -> bool:
        """Run a specific chapter."""
        return self.run_tool("saga", "run", chapter_name)
    
    def list_chapters(self) -> bool:
        """List all available chapters."""
        return self.run_tool("saga", "list-chapters")
    
    def create_chapter(self, chapter_name: str, template: Optional[str] = None) -> bool:
        """Create a new chapter."""
        if template:
            return self.run_tool("saga", "create", chapter_name, template)
        else:
            return self.run_tool("saga", "create", chapter_name)
    
    def backup_chapter(self, chapter_name: str) -> bool:
        """Backup a chapter."""
        return self.run_tool("saga", "backup", chapter_name)
    
    def list_dev_tools(self, tool_type: Optional[str] = None) -> bool:
        """List available development tools."""
        if tool_type:
            return self.run_tool("dev", "list", tool_type)
        else:
            return self.run_tool("dev", "list")
    
    def generate_system(self, system_name: str, chapter: str, template: str = "basic") -> bool:
        """Generate a new game system."""
        return self.run_tool("dev", "generate_system", system_name, chapter, template)
    
    def organize_assets(self, chapter: str) -> bool:
        """Organize assets for a chapter."""
        return self.run_tool("dev", "organize_assets", chapter)
    
    def migrate_character(self, character: str, from_chapter: str, to_chapter: str) -> bool:
        """Migrate a character between chapters."""
        return self.run_tool("cross", "migrate", character, from_chapter, to_chapter)
    
    def sync_save_data(self, character: str, chapter: str) -> bool:
        """Sync save data for a character."""
        return self.run_tool("cross", "sync", character, chapter)
    
    def register_achievement(self, achievement_id: str, name: str, description: str, chapter: str) -> bool:
        """Register a new achievement."""
        return self.run_tool("cross", "register_achievement", achievement_id, name, description, chapter)
    
    def unlock_achievement(self, character: str, achievement_id: str) -> bool:
        """Unlock an achievement for a character."""
        return self.run_tool("cross", "unlock", character, achievement_id)
    
    def get_achievements(self, character: str) -> bool:
        """Get achievements for a character."""
        return self.run_tool("cross", "achievements", character)
    
    def get_progress(self, character: str) -> bool:
        """Get saga progress for a character."""
        return self.run_tool("cross", "progress", character)
    
    def create_asset_library(self) -> bool:
        """Create shared asset library."""
        return self.run_tool("cross", "create_asset_library")
    
    # Stable Diffusion methods
    def sd_check(self) -> bool:
        """Check Stable Diffusion API connection."""
        return self.run_tool("sd", "check")
    
    def sd_models(self) -> bool:
        """List available Stable Diffusion models."""
        return self.run_tool("sd", "models")
    
    def sd_generate(self, prompt: str, **kwargs) -> bool:
        """Generate a single image."""
        args = ["generate", "--prompt", prompt]
        for key, value in kwargs.items():
            if value is not None:
                args.extend([f"--{key.replace('_', '-')}", str(value)])
        return self.run_tool("sd", *args)
    
    def sd_discord(self, prompt: str, style: str = "dark_fantasy") -> bool:
        """Generate Discord-optimized image."""
        return self.run_tool("sd", "discord", "--prompt", prompt, "--style", style)
    
    def sd_batch(self, prompt: str, **kwargs) -> bool:
        """Generate batch of images."""
        args = ["batch", "--prompt", prompt]
        for key, value in kwargs.items():
            if value is not None:
                args.extend([f"--{key.replace('_', '-')}", str(value)])
        return self.run_tool("sd", *args)
    
    def sd_list(self) -> bool:
        """List generated images."""
        return self.run_tool("sd", "list")
    
    def sd_cleanup(self, days: int = 30) -> bool:
        """Clean up old generated images."""
        return self.run_tool("sd", "cleanup", "--days", str(days))
    
    # NPC AI methods
    def npc_check(self) -> bool:
        """Check Ollama connection for NPC AI."""
        return self.run_tool("npc", "check")
    
    def npc_list(self) -> bool:
        """List available NPCs."""
        return self.run_tool("npc", "list")
    
    def npc_create(self, name: str, role: str, personality: str, background: str, location: str) -> bool:
        """Create a new NPC profile."""
        return self.run_tool("npc", "create", "--npc", name, "--role", role, "--personality", personality, "--background", background, "--location", location)
    
    def npc_interact(self, npc_name: str, message: str, interaction_type: str = "text") -> bool:
        """Interact with an NPC."""
        return self.run_tool("npc", "interact", "--npc", npc_name, "--message", message, "--type", interaction_type)
    
    def npc_history(self, npc_name: str) -> bool:
        """Get conversation history with an NPC."""
        return self.run_tool("npc", "history", "--npc", npc_name)
    
    def npc_samples(self) -> bool:
        """Create sample NPCs."""
        return self.run_tool("npc", "samples")
    
    # Image Generator methods
    def img_monster(self, monster_type: str, level: int = 1) -> bool:
        """Generate a monster image."""
        return self.run_tool("img", "monster", "--type", monster_type, "--level", str(level))
    
    def img_character(self, race: str = "human", class_type: str = "warrior", equipment: str = "{}") -> bool:
        """Generate a character portrait."""
        return self.run_tool("img", "character", "--race", race, "--class", class_type, "--equipment", equipment)
    
    def img_generate(self, prompt: str) -> bool:
        """Generate a custom image."""
        return self.run_tool("img", "generate", "--prompt", prompt)
    
    def img_list(self) -> bool:
        """List generated images."""
        return self.run_tool("img", "list")
    
    # Balance Testing methods
    def balance_quick(self) -> bool:
        """Run quick balance test."""
        return self.run_tool("balance", "quick")
    
    def balance_comprehensive(self) -> bool:
        """Run comprehensive balance test."""
        return self.run_tool("balance", "comprehensive")
    
    # Set Item Manager methods
    def set_create_template(self, template: str, name: Optional[str] = None, description: Optional[str] = None) -> bool:
        """Create set from template."""
        args = ["template", template]
        if name:
            args.extend(["--name", name])
        if description:
            args.extend(["--description", description])
        return self.run_tool("set_manager", *args)
    
    def set_create_custom(self, name: str, description: str, bonuses: str, items: str) -> bool:
        """Create custom set."""
        return self.run_tool("set_manager", "custom", "--name", name, "--description", description, 
                            "--bonuses", bonuses, "--items", items)
    
    def set_list(self) -> bool:
        """List all sets."""
        return self.run_tool("set_manager", "list")
    
    def set_info(self, set_id: str) -> bool:
        """Get set information."""
        return self.run_tool("set_manager", "info", set_id)
    
    # Performance Optimizer methods
    def perf_quick(self) -> bool:
        """Run quick performance test."""
        return self.run_tool("perf", "quick")
    
    def perf_comprehensive(self) -> bool:
        """Run comprehensive performance test."""
        return self.run_tool("perf", "comprehensive")
    
    def perf_optimize(self, system: str) -> bool:
        """Optimize specific system."""
        return self.run_tool("perf", "optimize", system)
    
    def perf_optimize_all(self) -> bool:
        """Optimize all systems."""
        return self.run_tool("perf", "optimize_all")
    
    # Boss Encounter methods
    def boss_create_district(self, district_name: str, district_level: int, player_level: int) -> bool:
        """Create a district boss."""
        return self.run_tool("boss", "create-district", district_name, str(district_level), str(player_level))
    
    def boss_create_unique(self, district_level: int, player_level: int) -> bool:
        """Create a unique monster."""
        return self.run_tool("boss", "create-unique", str(district_level), str(player_level))
    
    def boss_create_world(self, player_level: int, boss_name: Optional[str] = None) -> bool:
        """Create a world boss."""
        if boss_name:
            return self.run_tool("boss", "create-world", str(player_level), boss_name)
        else:
            return self.run_tool("boss", "create-world", str(player_level))
    
    def boss_simulate(self, boss_type: str, district_level: int, player_level: int) -> bool:
        """Simulate a boss fight."""
        return self.run_tool("boss", "create-world", boss_type, str(district_level), str(player_level))
    
    def boss_test_abilities(self) -> bool:
        """Test boss abilities."""
        return self.run_tool("boss", "test-abilities")
    
    # AI Player methods
    def ai_player_create_profile(self, name: str, playstyle: str, personality: str,
                               preferred_archetype: str, decision_style: str,
                               risk_tolerance: float = 0.5, patience_level: float = 0.5,
                               optimization_focus: str = "balanced") -> bool:
        """Create an AI player profile."""
        return self.run_tool("ai_player", "create-profile", name, playstyle, personality,
                           preferred_archetype, decision_style, str(risk_tolerance),
                           str(patience_level), optimization_focus)
    
    def ai_player_simulate(self, player_name: str, simulation_type: str, **kwargs) -> bool:
        """Run an AI player simulation."""
        args = [player_name, simulation_type]
        for key, value in kwargs.items():
            args.extend([f"--{key}", str(value)])
        return self.run_tool("ai_player", "simulate", *args)
    
    def ai_player_list(self) -> bool:
        """List AI players."""
        return self.run_tool("ai_player", "list")
    
    def ai_player_history(self, player_name: str, limit: int = 10) -> bool:
        """View AI player decision history."""
        return self.run_tool("ai_player", "history", player_name, str(limit))
    
    def ai_player_create_samples(self) -> bool:
        """Create sample AI players."""
        return self.run_tool("ai_player", "samples")
    
    def ai_player_test_connection(self) -> bool:
        """Test Ollama connection for AI players."""
        return self.run_tool("ai_player", "test")
    
    # AI Playtest methods
    def ai_playtest_quick(self, player_name: str) -> bool:
        """Run quick AI playtest with basic scenarios"""
        return self.run_tool("ai_playtest", "quick", "--player", player_name)
    
    def ai_playtest_comprehensive(self, player_name: str) -> bool:
        """Run comprehensive AI playtest with all scenarios"""
        return self.run_tool("ai_playtest", "comprehensive", "--player", player_name)
    
    def ai_playtest_custom(self, player_name: str, scenarios: List[str]) -> bool:
        """Run custom AI playtest with specified scenarios"""
        args = ["custom", "--player", player_name] + scenarios
        return self.run_tool("ai_playtest", *args)
    
    def ai_playtest_compare(self, players: List[str], scenarios: List[str]) -> bool:
        """Compare multiple AI players"""
        args = ["compare", "--players"] + players + ["--scenarios"] + scenarios
        return self.run_tool("ai_playtest", *args)
    
    def ai_playtest_enhanced(self, player_name: str, scenarios: List[str] = None, verbose: bool = True) -> bool:
        """Run enhanced AI playtest with full thinking process and detailed performance monitoring"""
        if scenarios is None:
            scenarios = ["character_creation", "combat_test", "skill_allocation"]
        
        args = ["playtest", "--player", player_name]
        if verbose:
            args.append("--verbose")
        
        return self.run_tool("ai_playtest", *args)
    
    def ai_playtest_learning_party(self, scenarios: List[str] = None, skill_levels: List[str] = None) -> bool:
        """Run learning session with 5-player party of different skill levels"""
        if scenarios is None:
            scenarios = ["character_creation", "combat_test", "skill_allocation", "exploration_test"]
        
        args = ["learning-party", "--scenarios"] + scenarios
        if skill_levels:
            args.extend(["--skill-levels"] + skill_levels)
        
        return self.run_tool("ai_playtest", *args)
    
    def ai_playtest_adaptive(self, test_sessions: int = 5, scenarios: List[str] = None) -> bool:
        """Run adaptive testing with multiple sessions to test AI learning over time"""
        if scenarios is None:
            scenarios = ["character_creation", "combat_test", "skill_allocation", "exploration_test"]
        
        args = ["adaptive", "--test-sessions", str(test_sessions), "--scenarios"] + scenarios
        return self.run_tool("ai_playtest", *args)
    
    # Performance Monitoring methods
    def performance_start(self, session_name: Optional[str] = None) -> bool:
        """Start performance monitoring"""
        args = ["start"]
        if session_name:
            args.extend(["--session", session_name])
        return self.run_tool("performance", *args)
    
    def performance_stop(self) -> bool:
        """Stop performance monitoring"""
        return self.run_tool("performance", "stop")
    
    def performance_summary(self, log_file: Optional[str] = None) -> bool:
        """Get performance summary"""
        args = ["summary"]
        if log_file:
            args.extend(["--log-file", log_file])
        return self.run_tool("performance", *args)
    
    def performance_list(self) -> bool:
        """List available performance logs"""
        return self.run_tool("performance", "list")
    
    # Discord Bot methods
    def discord_setup(self, token: Optional[str] = None, prefix: str = "!", llm_prefix: str = "@") -> bool:
        """Setup Discord bot configuration."""
        args = ["setup"]
        if token:
            args.extend(["--token", token])
        args.extend(["--prefix", prefix, "--llm-prefix", llm_prefix])
        return self.run_tool("discord", *args)
    
    def discord_run(self) -> bool:
        """Run the Discord bot."""
        return self.run_tool("discord", "run")
    
    def discord_test(self) -> bool:
        """Test Discord bot configuration."""
        return self.run_tool("discord", "test")
    
    def show_help(self):
        """Show help information."""
        help_text = """
Master Development Script for Chronicles of Ruin Saga

BUILD COMMANDS:
  build-all                    Build all chapters and run tests
  build-chapter <name>         Build a specific chapter
  clean                        Clean build artifacts

CHAPTER MANAGEMENT:
  list-chapters                List all available chapters
  run-chapter <name>           Run a specific chapter
  create-chapter <name> [template]  Create a new chapter
  backup-chapter <name>        Backup a chapter

DEVELOPMENT TOOLS:
  list-tools [type]            List available development tools
  generate-system <name> <chapter> [template]  Generate new system
  organize-assets <chapter>    Organize assets for a chapter

STABLE DIFFUSION:
  sd-check                     Check SD API connection
  sd-models                    List available models
  sd-generate <prompt>         Generate single image
  sd-discord <prompt> [style]  Generate Discord-optimized image
  sd-batch <prompt>            Generate batch of images
  sd-list                      List generated images
  sd-cleanup [days]            Clean up old images

NPC AI SYSTEM:
  npc-check                    Check Ollama connection
  npc-list                     List available NPCs
  npc-create <name> <role> <personality> <background> <location>  Create NPC
  npc-interact <name> <message> [type]  Talk to NPC
  npc-history <name>           Get conversation history
      npc-samples                  Create sample NPCs

    IMAGE GENERATOR:
      img-monster <type> [level]   Generate monster image
      img-character [race] [class] Generate character portrait
      img-generate <prompt>        Generate custom image
      img-list                     List generated images

    BALANCE TESTING:
      balance-quick                Run quick balance test
      balance-comprehensive        Run comprehensive balance test

    SET ITEM MANAGER:
      set-create-template <template> [name] [description]  Create set from template
      set-create-custom <name> <description> <bonuses> <items>  Create custom set
      set-list                     List all sets
      set-info <set_id>            Get set information

    PERFORMANCE OPTIMIZER:
      perf-quick                   Run quick performance test
      perf-comprehensive           Run comprehensive performance test
      perf-optimize <system>       Optimize specific system
              perf-optimize-all            Optimize all systems

    BOSS ENCOUNTERS:
      boss-create-district <name> <level> <player_level>  Create district boss
      boss-create-unique <level> <player_level>           Create unique monster
      boss-create-world <player_level> [name]             Create world boss
      boss-simulate <type> <level> <player_level>         Simulate boss fight
      boss-test-abilities                                 Test boss abilities

    AI PLAYER SYSTEM:
      ai-player-create-profile <name> <playstyle> <personality> <archetype> <decision_style> [risk] [patience] [focus]  Create AI player
      ai-player-simulate <player> <type> [options]        Run AI player simulation
      ai-player-list                                      List AI players
      ai-player-history <player> [limit]                  View decision history
                 ai-player-samples                                    Create sample AI players
           ai-player-test                                       Test Ollama connection
           
           AI PLAYTEST:
           ai-playtest-quick <player>                          Run quick AI playtest
           ai-playtest-comprehensive <player>                  Run comprehensive AI playtest
           ai-playtest-custom <player> <scenarios>            Run custom AI playtest
           ai-playtest-compare <players> <scenarios>          Compare multiple AI players
           ai-playtest-enhanced <player> [scenario1] [scenario2] ... [--verbose]  Run enhanced AI playtest
           ai-playtest-learning-party [scenarios] [skill_levels]  Run learning party
           ai-playtest-adaptive [test_sessions] [scenarios]  Run adaptive testing

    PERFORMANCE MONITORING:
      performance-start [session]                              Start performance monitoring
      performance-stop                                         Stop performance monitoring
      performance-summary [log_file]                          Get performance summary
      performance-list                                        List available logs

    DISCORD BOT:
      discord-setup [token]        Setup Discord bot configuration
      discord-run                  Run the Discord bot
      discord-test                 Test bot configuration

CROSS-CHAPTER FEATURES:
  migrate <char> <from> <to>   Migrate character between chapters
  sync-save <char> <chapter>   Sync save data
  register-achievement <id> <name> <desc> <chapter>  Register achievement
  unlock <char> <achievement>  Unlock achievement
  achievements <char>           Get character achievements
  progress <char>              Get saga progress
  create-asset-library         Create shared asset library

EXAMPLES:
  python dev_master.py build-all
  python dev_master.py run-chapter chapter_01_sunderfall
  python dev_master.py generate-system Combat chapter_01_sunderfall combat
  python dev_master.py migrate Player1 chapter_01_sunderfall chapter_02_voidreach
  python dev_master.py sd-discord "dark fantasy warrior"
"""
        print(help_text)

def main():
    """CLI interface for the master development script."""
    master = DevMaster()
    
    if len(sys.argv) < 2:
        master.show_help()
        return
    
    command = sys.argv[1]
    
    # Build commands
    if command == "build-all":
        master.build_all()
    
    elif command == "build-chapter" and len(sys.argv) >= 3:
        chapter_name = sys.argv[2]
        master.build_chapter(chapter_name)
    
    elif command == "clean":
        master.run_tool("build", "clean")
    
    # Chapter management
    elif command == "list-chapters":
        master.list_chapters()
    
    elif command == "run-chapter" and len(sys.argv) >= 3:
        chapter_name = sys.argv[2]
        master.run_chapter(chapter_name)
    
    elif command == "create-chapter" and len(sys.argv) >= 3:
        chapter_name = sys.argv[2]
        template = sys.argv[3] if len(sys.argv) > 3 else None
        master.create_chapter(chapter_name, template)
    
    elif command == "backup-chapter" and len(sys.argv) >= 3:
        chapter_name = sys.argv[2]
        master.backup_chapter(chapter_name)
    
    # Development tools
    elif command == "list-tools":
        tool_type = sys.argv[2] if len(sys.argv) > 2 else None
        if tool_type:
            master.list_dev_tools(tool_type)
        else:
            master.list_dev_tools()
    
    elif command == "generate-system" and len(sys.argv) >= 4:
        system_name = sys.argv[2]
        chapter = sys.argv[3]
        template = sys.argv[4] if len(sys.argv) > 4 else "basic"
        master.generate_system(system_name, chapter, template)
    
    elif command == "organize-assets" and len(sys.argv) >= 3:
        chapter = sys.argv[2]
        master.organize_assets(chapter)
    
    # Cross-chapter features
    elif command == "migrate" and len(sys.argv) >= 5:
        character = sys.argv[2]
        from_chapter = sys.argv[3]
        to_chapter = sys.argv[4]
        master.migrate_character(character, from_chapter, to_chapter)
    
    elif command == "sync-save" and len(sys.argv) >= 4:
        character = sys.argv[2]
        chapter = sys.argv[3]
        master.sync_save_data(character, chapter)
    
    elif command == "register-achievement" and len(sys.argv) >= 6:
        achievement_id = sys.argv[2]
        name = sys.argv[3]
        description = sys.argv[4]
        chapter = sys.argv[5]
        master.register_achievement(achievement_id, name, description, chapter)
    
    elif command == "unlock" and len(sys.argv) >= 4:
        character = sys.argv[2]
        achievement_id = sys.argv[3]
        master.unlock_achievement(character, achievement_id)
    
    elif command == "achievements" and len(sys.argv) >= 3:
        character = sys.argv[2]
        master.get_achievements(character)
    
    elif command == "progress" and len(sys.argv) >= 3:
        character = sys.argv[2]
        master.get_progress(character)
    
    elif command == "create-asset-library":
        master.create_asset_library()
    
    # Stable Diffusion commands
    elif command == "sd-check":
        master.sd_check()
    
    elif command == "sd-models":
        master.sd_models()
    
    elif command == "sd-generate" and len(sys.argv) >= 3:
        prompt = sys.argv[2]
        # Parse optional arguments
        kwargs = {}
        for i in range(3, len(sys.argv), 2):
            if i + 1 < len(sys.argv):
                key = sys.argv[i].lstrip('-').replace('-', '_')
                value = sys.argv[i + 1]
                kwargs[key] = value
        master.sd_generate(prompt, **kwargs)
    
    elif command == "sd-discord" and len(sys.argv) >= 3:
        prompt = sys.argv[2]
        style = sys.argv[3] if len(sys.argv) > 3 else "dark_fantasy"
        master.sd_discord(prompt, style)
    
    elif command == "sd-batch" and len(sys.argv) >= 3:
        prompt = sys.argv[2]
        # Parse optional arguments
        kwargs = {}
        for i in range(3, len(sys.argv), 2):
            if i + 1 < len(sys.argv):
                key = sys.argv[i].lstrip('-').replace('-', '_')
                value = sys.argv[i + 1]
                kwargs[key] = value
        master.sd_batch(prompt, **kwargs)
    
    elif command == "sd-list":
        master.sd_list()
    
    elif command == "sd-cleanup":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        master.sd_cleanup(days)
    
    # NPC AI commands
    elif command == "npc-check":
        master.npc_check()
    
    elif command == "npc-list":
        master.npc_list()
    
    elif command == "npc-create" and len(sys.argv) >= 7:
        name = sys.argv[2]
        role = sys.argv[3]
        personality = sys.argv[4]
        background = sys.argv[5]
        location = sys.argv[6]
        master.npc_create(name, role, personality, background, location)
    
    elif command == "npc-interact" and len(sys.argv) >= 4:
        npc_name = sys.argv[2]
        message = sys.argv[3]
        interaction_type = sys.argv[4] if len(sys.argv) > 4 else "text"
        master.npc_interact(npc_name, message, interaction_type)
    
    elif command == "npc-history" and len(sys.argv) >= 3:
        npc_name = sys.argv[2]
        master.npc_history(npc_name)
    
    elif command == "npc-samples":
        master.npc_samples()
    
    # Image Generator commands
    elif command == "img-monster":
        monster_type = sys.argv[2] if len(sys.argv) > 2 else "goblin"
        level = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        master.img_monster(monster_type, level)
    
    elif command == "img-character":
        race = sys.argv[2] if len(sys.argv) > 2 else "human"
        class_type = sys.argv[3] if len(sys.argv) > 3 else "warrior"
        equipment = "{}"
        master.img_character(race, class_type, equipment)
    
    elif command == "img-generate":
        prompt = sys.argv[2] if len(sys.argv) > 2 else "fantasy landscape"
        master.img_generate(prompt)
    
    elif command == "img-list":
        master.img_list()
    
    # Balance Testing commands
    elif command == "balance-quick":
        master.balance_quick()
    
    elif command == "balance-comprehensive":
        master.balance_comprehensive()
    
    # Set Item Manager commands
    elif command == "set-create-template":
        template = sys.argv[2] if len(sys.argv) > 2 else "warrior_set"
        name = sys.argv[3] if len(sys.argv) > 3 else None
        description = sys.argv[4] if len(sys.argv) > 4 else None
        master.set_create_template(template, name, description)
    
    elif command == "set-create-custom":
        if len(sys.argv) >= 6:
            name = sys.argv[2]
            description = sys.argv[3]
            bonuses = sys.argv[4]
            items = sys.argv[5]
            master.set_create_custom(name, description, bonuses, items)
        else:
            print("Usage: set-create-custom <name> <description> <bonuses> <items>")
    
    elif command == "set-list":
        master.set_list()
    
    elif command == "set-info":
        set_id = sys.argv[2] if len(sys.argv) > 2 else ""
        if set_id:
            master.set_info(set_id)
        else:
            print("Usage: set-info <set_id>")
    
    # Performance Optimizer commands
    elif command == "perf-quick":
        master.perf_quick()
    
    elif command == "perf-comprehensive":
        master.perf_comprehensive()
    
    elif command == "perf-optimize":
        system = sys.argv[2] if len(sys.argv) > 2 else "combat"
        master.perf_optimize(system)
    
    elif command == "perf-optimize-all":
        master.perf_optimize_all()
    
    # Boss Encounter commands
    elif command == "boss-create-district":
        if len(sys.argv) >= 5:
            district_name = sys.argv[2]
            district_level = int(sys.argv[3])
            player_level = int(sys.argv[4])
            master.boss_create_district(district_name, district_level, player_level)
        else:
            print("Usage: boss-create-district <name> <level> <player_level>")
    
    elif command == "boss-create-unique":
        if len(sys.argv) >= 4:
            district_level = int(sys.argv[2])
            player_level = int(sys.argv[3])
            master.boss_create_unique(district_level, player_level)
        else:
            print("Usage: boss-create-unique <level> <player_level>")
    
    elif command == "boss-create-world":
        if len(sys.argv) >= 3:
            player_level = int(sys.argv[2])
            boss_name = sys.argv[3] if len(sys.argv) > 3 else None
            master.boss_create_world(player_level, boss_name)
        else:
            print("Usage: boss-create-world <player_level> [name]")
    
    elif command == "boss-simulate":
        if len(sys.argv) >= 5:
            boss_type = sys.argv[2]
            district_level = int(sys.argv[3])
            player_level = int(sys.argv[4])
            master.boss_simulate(boss_type, district_level, player_level)
        else:
            print("Usage: boss-simulate <type> <level> <player_level>")
    
    elif command == "boss-test-abilities":
        master.boss_test_abilities()
    
    # AI Player commands
    elif command == "ai-player-create-profile":
        if len(sys.argv) >= 7:
            name = sys.argv[2]
            playstyle = sys.argv[3]
            personality = sys.argv[4]
            archetype = sys.argv[5]
            decision_style = sys.argv[6]
            risk_tolerance = float(sys.argv[7]) if len(sys.argv) > 7 else 0.5
            patience_level = float(sys.argv[8]) if len(sys.argv) > 8 else 0.5
            optimization_focus = sys.argv[9] if len(sys.argv) > 9 else "balanced"
            master.ai_player_create_profile(name, playstyle, personality, archetype, 
                                         decision_style, risk_tolerance, patience_level, optimization_focus)
        else:
            print("Usage: ai-player-create-profile <name> <playstyle> <personality> <archetype> <decision_style> [risk] [patience] [focus]")
    
    elif command == "ai-player-simulate":
        if len(sys.argv) >= 4:
            player_name = sys.argv[2]
            simulation_type = sys.argv[3]
            # Parse additional options
            kwargs = {}
            for i in range(4, len(sys.argv), 2):
                if i + 1 < len(sys.argv):
                    key = sys.argv[i].lstrip('-')
                    value = sys.argv[i + 1]
                    kwargs[key] = value
            master.ai_player_simulate(player_name, simulation_type, **kwargs)
        else:
            print("Usage: ai-player-simulate <player> <type> [options]")
    
    elif command == "ai-player-list":
        master.ai_player_list()
    
    elif command == "ai-player-history":
        if len(sys.argv) >= 3:
            player_name = sys.argv[2]
            limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
            master.ai_player_history(player_name, limit)
        else:
            print("Usage: ai-player-history <player> [limit]")
    
    elif command == "ai-player-samples":
        master.ai_player_create_samples()
    
    elif command == "ai-player-test":
        master.ai_player_test_connection()
    
    # AI Playtest commands
    elif command == "ai-playtest-quick":
        if len(sys.argv) >= 3:
            player_name = sys.argv[2]
            master.ai_playtest_quick(player_name)
        else:
            print("Usage: ai-playtest-quick <player>")
    
    elif command == "ai-playtest-comprehensive":
        if len(sys.argv) >= 3:
            player_name = sys.argv[2]
            master.ai_playtest_comprehensive(player_name)
        else:
            print("Usage: ai-playtest-comprehensive <player>")
    
    elif command == "ai-playtest-custom":
        if len(sys.argv) >= 4:
            player_name = sys.argv[2]
            scenarios = sys.argv[3:]
            master.ai_playtest_custom(player_name, scenarios)
        else:
            print("Usage: ai-playtest-custom <player> <scenario1> <scenario2> ...")
    
    elif command == "ai-playtest-compare":
        if len(sys.argv) >= 4:
            # Parse players and scenarios
            args = sys.argv[2:]
            try:
                separator_index = args.index("--scenarios")
                players = args[:separator_index]
                scenarios = args[separator_index + 1:]
                master.ai_playtest_compare(players, scenarios)
            except ValueError:
                print("Usage: ai-playtest-compare <player1> <player2> ... --scenarios <scenario1> <scenario2> ...")
        else:
            print("Usage: ai-playtest-compare <player1> <player2> ... --scenarios <scenario1> <scenario2> ...")
    
    elif command == "ai-playtest-enhanced":
        if len(sys.argv) >= 3:
            player_name = sys.argv[2]
            scenarios = sys.argv[3:] if len(sys.argv) > 3 else None
            verbose = "--verbose" in sys.argv
            master.ai_playtest_enhanced(player_name, scenarios, verbose)
        else:
            print("Usage: ai-playtest-enhanced <player> [scenario1] [scenario2] ... [--verbose]")
    
    elif command == "ai-playtest-learning-party":
        if len(sys.argv) >= 3:
            scenarios = sys.argv[2:] if len(sys.argv) > 2 else None
            skill_levels = sys.argv[2:] if len(sys.argv) > 2 else None # Assuming skill_levels are also optional args
            master.ai_playtest_learning_party(scenarios, skill_levels)
        else:
            print("Usage: ai-playtest-learning-party [scenarios] [skill_levels]")
    
    elif command == "ai-playtest-adaptive":
        if len(sys.argv) >= 3:
            test_sessions = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            scenarios = sys.argv[3:] if len(sys.argv) > 3 else None
            master.ai_playtest_adaptive(test_sessions, scenarios)
        else:
            print("Usage: ai-playtest-adaptive [test_sessions] [scenarios]")
    
    # Performance Monitoring commands
    elif command == "performance-start":
        session_name = sys.argv[2] if len(sys.argv) > 2 else None
        master.performance_start(session_name)
    
    elif command == "performance-stop":
        master.performance_stop()
    
    elif command == "performance-summary":
        log_file = sys.argv[2] if len(sys.argv) > 2 else None
        master.performance_summary(log_file)
    
    elif command == "performance-list":
        master.performance_list()
    
    # Discord Bot commands
    elif command == "discord-setup":
        token = sys.argv[2] if len(sys.argv) > 2 else None
        master.discord_setup(token)
    
    elif command == "discord-run":
        master.discord_run()
    
    elif command == "discord-test":
        master.discord_test()
    
    else:
        print(f"Unknown command: {command}")
        master.show_help()

if __name__ == "__main__":
    main()

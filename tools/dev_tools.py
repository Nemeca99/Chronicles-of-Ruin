#!/usr/bin/env python3
"""
Shared Development Tools for Chronicles of Ruin Saga
Framework for code generators, asset management, and development utilities.
"""

import os
import sys
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class ToolType(Enum):
    CODE_GENERATOR = "code_generator"
    ASSET_MANAGER = "asset_manager"
    DATABASE_TOOL = "database_tool"
    PERFORMANCE_TOOL = "performance_tool"

@dataclass
class DevTool:
    name: str
    tool_type: ToolType
    description: str
    command: str
    parameters: Dict[str, Any]

class DevToolsFramework:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.chapters_dir = self.root_dir / "chapters"
        self.tools_dir = self.root_dir / "tools"
        self.shared_dir = self.root_dir / "shared"
        
        # Register available tools
        self.tools = self._register_tools()
    
    def _register_tools(self) -> Dict[str, DevTool]:
        """Register all available development tools."""
        tools = {}
        
        # Code Generators
        tools["generate_system"] = DevTool(
            name="System Generator",
            tool_type=ToolType.CODE_GENERATOR,
            description="Generate new game systems (combat, items, etc.)",
            command="generate_system",
            parameters={"system_name": "str", "chapter": "str", "template": "str"}
        )
        
        tools["generate_monster"] = DevTool(
            name="Monster Generator",
            tool_type=ToolType.CODE_GENERATOR,
            description="Generate new monster types and AI",
            command="generate_monster",
            parameters={"monster_name": "str", "difficulty": "int", "chapter": "str"}
        )
        
        tools["generate_item"] = DevTool(
            name="Item Generator",
            tool_type=ToolType.CODE_GENERATOR,
            description="Generate new items and equipment",
            command="generate_item",
            parameters={"item_name": "str", "item_type": "str", "rarity": "str"}
        )
        
        # Asset Management
        tools["asset_organizer"] = DevTool(
            name="Asset Organizer",
            tool_type=ToolType.ASSET_MANAGER,
            description="Organize and validate game assets",
            command="organize_assets",
            parameters={"chapter": "str", "validate": "bool"}
        )
        
        tools["asset_optimizer"] = DevTool(
            name="Asset Optimizer",
            tool_type=ToolType.ASSET_MANAGER,
            description="Optimize game assets for performance",
            command="optimize_assets",
            parameters={"chapter": "str", "quality": "str"}
        )
        
        # Database Tools
        tools["db_migrate"] = DevTool(
            name="Database Migration",
            tool_type=ToolType.DATABASE_TOOL,
            description="Migrate database schemas between chapters",
            command="migrate_db",
            parameters={"from_chapter": "str", "to_chapter": "str"}
        )
        
        tools["db_backup"] = DevTool(
            name="Database Backup",
            tool_type=ToolType.DATABASE_TOOL,
            description="Backup chapter databases",
            command="backup_db",
            parameters={"chapter": "str", "backup_name": "str"}
        )
        
        # Performance Tools
        tools["performance_profiler"] = DevTool(
            name="Performance Profiler",
            tool_type=ToolType.PERFORMANCE_TOOL,
            description="Profile game performance",
            command="profile_performance",
            parameters={"chapter": "str", "duration": "int"}
        )
        
        tools["memory_analyzer"] = DevTool(
            name="Memory Analyzer",
            tool_type=ToolType.PERFORMANCE_TOOL,
            description="Analyze memory usage",
            command="analyze_memory",
            parameters={"chapter": "str", "detailed": "bool"}
        )
        
        return tools
    
    def list_tools(self, tool_type: Optional[ToolType] = None) -> List[DevTool]:
        """List available tools, optionally filtered by type."""
        if tool_type:
            return [tool for tool in self.tools.values() if tool.tool_type == tool_type]
        return list(self.tools.values())
    
    def get_tool(self, tool_name: str) -> Optional[DevTool]:
        """Get a specific tool by name."""
        return self.tools.get(tool_name)
    
    def generate_system(self, system_name: str, chapter: str, template: str = "basic") -> bool:
        """Generate a new game system."""
        print(f"Generating {system_name} system for chapter {chapter}")
        
        chapter_path = self.chapters_dir / chapter
        if not chapter_path.exists():
            print(f"Chapter {chapter} not found!")
            return False
        
        # Create system directory
        system_dir = chapter_path / "src" / "systems" / system_name.lower()
        system_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate system files based on template
        if template == "basic":
            self._generate_basic_system(system_dir, system_name)
        elif template == "combat":
            self._generate_combat_system(system_dir, system_name)
        elif template == "item":
            self._generate_item_system(system_dir, system_name)
        
        print(f"✓ Generated {system_name} system")
        return True
    
    def _generate_basic_system(self, system_dir: Path, system_name: str):
        """Generate a basic system template."""
        # Create __init__.py
        init_content = f'''"""
{system_name} System
Generated by DevTools Framework
"""

from .{system_name.lower()}_core import {system_name}System

__all__ = ["{system_name}System"]
'''
        (system_dir / "__init__.py").write_text(init_content)
        
        # Create core system file
        core_content = f'''"""
{system_name} System Core Implementation
"""

class {system_name}System:
    def __init__(self):
        self.name = "{system_name}"
        self.initialized = False
    
    def initialize(self):
        """Initialize the {system_name} system."""
        self.initialized = True
        print(f"{{self.name}} system initialized")
    
    def update(self):
        """Update the {system_name} system."""
        if not self.initialized:
            self.initialize()
    
    def cleanup(self):
        """Cleanup the {system_name} system."""
        self.initialized = False
'''
        (system_dir / f"{system_name.lower()}_core.py").write_text(core_content)
    
    def _generate_combat_system(self, system_dir: Path, system_name: str):
        """Generate a combat system template."""
        self._generate_basic_system(system_dir, system_name)
        
        # Add combat-specific files
        combat_content = f'''"""
{system_name} Combat Implementation
"""

class {system_name}Combat:
    def __init__(self):
        self.damage_multiplier = 1.0
        self.critical_chance = 0.05
    
    def calculate_damage(self, base_damage: float) -> float:
        """Calculate damage with modifiers."""
        return base_damage * self.damage_multiplier
    
    def roll_critical(self) -> bool:
        """Roll for critical hit."""
        import random
        return random.random() < self.critical_chance
'''
        (system_dir / f"{system_name.lower()}_combat.py").write_text(combat_content)
    
    def _generate_item_system(self, system_dir: Path, system_name: str):
        """Generate an item system template."""
        self._generate_basic_system(system_dir, system_name)
        
        # Add item-specific files
        item_content = f'''"""
{system_name} Item Implementation
"""

class {system_name}Item:
    def __init__(self, name: str, item_type: str):
        self.name = name
        self.item_type = item_type
        self.rarity = "common"
        self.value = 0
    
    def get_description(self) -> str:
        """Get item description."""
        return f"{{self.rarity.title()}} {{self.item_type}}: {{self.name}}"
'''
        (system_dir / f"{system_name.lower()}_item.py").write_text(item_content)
    
    def organize_assets(self, chapter: str, validate: bool = True) -> bool:
        """Organize assets for a chapter."""
        print(f"Organizing assets for chapter {chapter}")
        
        chapter_path = self.chapters_dir / chapter
        if not chapter_path.exists():
            print(f"Chapter {chapter} not found!")
            return False
        
        assets_dir = chapter_path / "assets"
        if not assets_dir.exists():
            print(f"No assets directory found for chapter {chapter}")
            return False
        
        # Create organized structure
        organized_dirs = ["sprites", "sounds", "music", "ui", "fonts"]
        for dir_name in organized_dirs:
            (assets_dir / dir_name).mkdir(exist_ok=True)
        
        # Move files to appropriate directories based on extension
        for file in assets_dir.rglob("*"):
            if file.is_file():
                self._organize_asset_file(file, assets_dir)
        
        if validate:
            self._validate_assets(assets_dir)
        
        print(f"✓ Assets organized for chapter {chapter}")
        return True
    
    def _organize_asset_file(self, file: Path, assets_dir: Path):
        """Organize a single asset file."""
        extension = file.suffix.lower()
        
        if extension in [".png", ".jpg", ".jpeg", ".gif", ".bmp"]:
            dest = assets_dir / "sprites" / file.name
        elif extension in [".wav", ".mp3", ".ogg", ".flac"]:
            dest = assets_dir / "sounds" / file.name
        elif extension in [".ttf", ".otf"]:
            dest = assets_dir / "fonts" / file.name
        else:
            # Keep in root or move to ui
            dest = assets_dir / "ui" / file.name
        
        if file != dest and not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file), str(dest))
    
    def _validate_assets(self, assets_dir: Path):
        """Validate asset files."""
        issues = []
        
        for file in assets_dir.rglob("*"):
            if file.is_file():
                # Check file size
                if file.stat().st_size > 10 * 1024 * 1024:  # 10MB
                    issues.append(f"Large file: {file.relative_to(assets_dir)}")
                
                # Check for common issues
                if file.name.startswith("."):
                    issues.append(f"Hidden file: {file.relative_to(assets_dir)}")
        
        if issues:
            print("Asset validation issues found:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("✓ All assets validated successfully")

def main():
    """CLI interface for development tools."""
    framework = DevToolsFramework()
    
    if len(sys.argv) < 2:
        print("Shared Development Tools for Chronicles of Ruin")
        print("Usage:")
        print("  python dev_tools.py list [type]")
        print("  python dev_tools.py generate_system <name> <chapter> [template]")
        print("  python dev_tools.py organize_assets <chapter>")
        return
    
    command = sys.argv[1]
    
    if command == "list":
        tool_type = None
        if len(sys.argv) > 2:
            try:
                tool_type = ToolType(sys.argv[2])
            except ValueError:
                print(f"Invalid tool type: {sys.argv[2]}")
                return
        
        tools = framework.list_tools(tool_type)
        print("Available tools:")
        for tool in tools:
            print(f"  {tool.name} ({tool.tool_type.value})")
            print(f"    {tool.description}")
            print(f"    Command: {tool.command}")
            print()
    
    elif command == "generate_system" and len(sys.argv) >= 4:
        system_name = sys.argv[2]
        chapter = sys.argv[3]
        template = sys.argv[4] if len(sys.argv) > 4 else "basic"
        framework.generate_system(system_name, chapter, template)
    
    elif command == "organize_assets" and len(sys.argv) >= 3:
        chapter = sys.argv[2]
        framework.organize_assets(chapter)
    
    else:
        print("Invalid command or missing arguments!")

if __name__ == "__main__":
    main()

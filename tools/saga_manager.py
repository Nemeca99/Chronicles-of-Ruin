#!/usr/bin/env python3
"""
Saga Manager for Chronicles of Ruin
Handles cross-chapter operations and shared utilities for the entire saga.
"""

import os
import sys
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional

class SagaManager:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.chapters_dir = self.root_dir / "chapters"
        self.tools_dir = self.root_dir / "tools"
        self.shared_dir = self.root_dir / "shared"
        self.venv_dir = self.root_dir / "venv"
        
    def get_chapters(self) -> List[str]:
        """Get list of available chapters."""
        chapters = []
        if self.chapters_dir.exists():
            for item in self.chapters_dir.iterdir():
                if item.is_dir() and item.name.startswith("chapter_"):
                    chapters.append(item.name)
        return sorted(chapters)
    
    def get_chapter_path(self, chapter_name: str) -> Path:
        """Get the full path to a specific chapter."""
        return self.chapters_dir / chapter_name
    
    def create_new_chapter(self, chapter_name: str, template_from: Optional[str] = None) -> bool:
        """Create a new chapter based on an existing one or from scratch."""
        new_chapter_path = self.get_chapter_path(chapter_name)
        
        if new_chapter_path.exists():
            print(f"Chapter {chapter_name} already exists!")
            return False
            
        if template_from:
            template_path = self.get_chapter_path(template_from)
            if not template_path.exists():
                print(f"Template chapter {template_from} not found!")
                return False
                
            # Copy template chapter
            shutil.copytree(template_path, new_chapter_path)
            print(f"Created chapter {chapter_name} from template {template_from}")
        else:
            # Create basic structure
            new_chapter_path.mkdir(parents=True, exist_ok=True)
            self._create_basic_chapter_structure(new_chapter_path)
            print(f"Created new chapter {chapter_name}")
            
        return True
    
    def _create_basic_chapter_structure(self, chapter_path: Path):
        """Create basic directory structure for a new chapter."""
        dirs = ["src", "assets", "data", "docs", "tests", "logs", "saves"]
        for dir_name in dirs:
            (chapter_path / dir_name).mkdir(exist_ok=True)
    
    def run_chapter(self, chapter_name: str, *args) -> bool:
        """Run a specific chapter's launcher."""
        chapter_path = self.get_chapter_path(chapter_name)
        launcher_path = chapter_path / "game_launcher.py"
        
        if not launcher_path.exists():
            print(f"Launcher not found for chapter {chapter_name}")
            return False
            
        # Change to chapter directory and run
        os.chdir(chapter_path)
        os.system(f"python game_launcher.py {' '.join(args)}")
        return True
    
    def backup_chapter(self, chapter_name: str) -> bool:
        """Create a backup of a chapter."""
        chapter_path = self.get_chapter_path(chapter_name)
        if not chapter_path.exists():
            print(f"Chapter {chapter_name} not found!")
            return False
            
        backup_path = self.root_dir / "backups" / f"{chapter_name}_backup"
        backup_path.parent.mkdir(exist_ok=True)
        
        shutil.copytree(chapter_path, backup_path)
        print(f"Backup created: {backup_path}")
        return True
    
    def list_shared_tools(self) -> List[str]:
        """List available shared tools."""
        tools = []
        if self.tools_dir.exists():
            for item in self.tools_dir.iterdir():
                if item.is_file() and item.suffix == ".py":
                    tools.append(item.stem)
        return tools
    
    def get_saga_info(self) -> Dict:
        """Get information about the entire saga."""
        return {
            "name": "Chronicles of Ruin",
            "chapters": self.get_chapters(),
            "shared_tools": self.list_shared_tools(),
            "venv_path": str(self.venv_dir),
            "root_path": str(self.root_dir)
        }

def main():
    """CLI interface for saga management."""
    manager = SagaManager()
    
    if len(sys.argv) < 2:
        print("Saga Manager for Chronicles of Ruin")
        print("Usage:")
        print("  python saga_manager.py info")
        print("  python saga_manager.py list-chapters")
        print("  python saga_manager.py run <chapter_name>")
        print("  python saga_manager.py create <chapter_name> [template]")
        print("  python saga_manager.py backup <chapter_name>")
        return
    
    command = sys.argv[1]
    
    if command == "info":
        info = manager.get_saga_info()
        print(json.dumps(info, indent=2))
        
    elif command == "list-chapters":
        chapters = manager.get_chapters()
        print("Available chapters:")
        for chapter in chapters:
            print(f"  - {chapter}")
            
    elif command == "run" and len(sys.argv) >= 3:
        chapter_name = sys.argv[2]
        manager.run_chapter(chapter_name, *sys.argv[3:])
        
    elif command == "create" and len(sys.argv) >= 3:
        chapter_name = sys.argv[2]
        template = sys.argv[3] if len(sys.argv) > 3 else None
        manager.create_new_chapter(chapter_name, template)
        
    elif command == "backup" and len(sys.argv) >= 3:
        chapter_name = sys.argv[2]
        manager.backup_chapter(chapter_name)
        
    else:
        print("Invalid command or missing arguments!")

if __name__ == "__main__":
    main()

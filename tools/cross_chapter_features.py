#!/usr/bin/env python3
"""
Cross-Chapter Features Framework for Chronicles of Ruin Saga
Handles shared save data, character migration, and cross-chapter achievements.
"""

import os
import sys
import json
import shutil
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

class FeatureType(Enum):
    SAVE_DATA = "save_data"
    CHARACTER_MIGRATION = "character_migration"
    ACHIEVEMENTS = "achievements"
    SHARED_ASSETS = "shared_assets"

@dataclass
class SaveData:
    player_name: str
    chapter: str
    level: int
    experience: int
    inventory: List[str]
    achievements: List[str]
    timestamp: str
    version: str

@dataclass
class CharacterData:
    name: str
    class_type: str
    level: int
    experience: int
    stats: Dict[str, int]
    skills: List[str]
    equipment: Dict[str, str]
    inventory: List[str]
    gold: int
    chapter_progress: Dict[str, bool]

@dataclass
class Achievement:
    id: str
    name: str
    description: str
    chapter: str
    unlocked: bool
    unlocked_at: Optional[str]
    requirements: Dict[str, Any]

class CrossChapterFeatures:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.chapters_dir = self.root_dir / "chapters"
        self.shared_dir = self.root_dir / "shared"
        self.saves_dir = self.shared_dir / "saves"
        self.achievements_dir = self.shared_dir / "achievements"
        
        # Ensure directories exist
        self.saves_dir.mkdir(parents=True, exist_ok=True)
        self.achievements_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize shared database
        self.shared_db_path = self.shared_dir / "saga_data.db"
        self._init_shared_database()
    
    def _init_shared_database(self):
        """Initialize the shared saga database."""
        conn = sqlite3.connect(self.shared_db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                class_type TEXT NOT NULL,
                level INTEGER DEFAULT 1,
                experience INTEGER DEFAULT 0,
                stats TEXT NOT NULL,
                skills TEXT NOT NULL,
                equipment TEXT NOT NULL,
                inventory TEXT NOT NULL,
                gold INTEGER DEFAULT 0,
                chapter_progress TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                chapter TEXT NOT NULL,
                requirements TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS unlocked_achievements (
                character_name TEXT NOT NULL,
                achievement_id TEXT NOT NULL,
                unlocked_at TEXT NOT NULL,
                PRIMARY KEY (character_name, achievement_id),
                FOREIGN KEY (achievement_id) REFERENCES achievements (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS save_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_name TEXT NOT NULL,
                chapter TEXT NOT NULL,
                save_data TEXT NOT NULL,
                created_at TEXT NOT NULL,
                version TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def migrate_character(self, character_name: str, from_chapter: str, to_chapter: str) -> bool:
        """Migrate a character from one chapter to another."""
        print(f"Migrating character {character_name} from {from_chapter} to {to_chapter}")
        
        # Load character data from source chapter
        character_data = self._load_character_data(character_name, from_chapter)
        if not character_data:
            print(f"Character {character_name} not found in {from_chapter}")
            return False
        
        # Validate target chapter exists
        target_chapter_path = self.chapters_dir / to_chapter
        if not target_chapter_path.exists():
            print(f"Target chapter {to_chapter} not found")
            return False
        
        # Update character progress
        character_data.chapter_progress[to_chapter] = True
        
        # Save character data to target chapter
        success = self._save_character_data(character_data, to_chapter)
        if success:
            print(f"✓ Character {character_name} migrated successfully")
            return True
        else:
            print(f"Failed to save character data to {to_chapter}")
            return False
    
    def _load_character_data(self, character_name: str, chapter: str) -> Optional[CharacterData]:
        """Load character data from a specific chapter."""
        chapter_path = self.chapters_dir / chapter
        if not chapter_path.exists():
            return None
        
        # Try to load from chapter's save system
        save_file = chapter_path / "saves" / f"{character_name}.json"
        if save_file.exists():
            try:
                with open(save_file, 'r') as f:
                    data = json.load(f)
                    return CharacterData(**data)
            except Exception as e:
                print(f"Failed to load character data: {e}")
                return None
        
        return None
    
    def _save_character_data(self, character_data: CharacterData, chapter: str) -> bool:
        """Save character data to a specific chapter."""
        chapter_path = self.chapters_dir / chapter
        if not chapter_path.exists():
            return False
        
        saves_dir = chapter_path / "saves"
        saves_dir.mkdir(exist_ok=True)
        
        save_file = saves_dir / f"{character_data.name}.json"
        try:
            with open(save_file, 'w') as f:
                json.dump(asdict(character_data), f, indent=2)
            return True
        except Exception as e:
            print(f"Failed to save character data: {e}")
            return False
    
    def sync_save_data(self, character_name: str, chapter: str) -> bool:
        """Sync save data between chapter and shared storage."""
        print(f"Syncing save data for {character_name} in {chapter}")
        
        # Load from chapter
        chapter_save = self._load_chapter_save(character_name, chapter)
        if not chapter_save:
            print(f"No save data found for {character_name} in {chapter}")
            return False
        
        # Save to shared storage
        shared_save = SaveData(
            player_name=character_name,
            chapter=chapter,
            level=chapter_save.get("level", 1),
            experience=chapter_save.get("experience", 0),
            inventory=chapter_save.get("inventory", []),
            achievements=chapter_save.get("achievements", []),
            timestamp=datetime.now().isoformat(),
            version="1.0"
        )
        
        success = self._save_to_shared_storage(shared_save)
        if success:
            print(f"✓ Save data synced for {character_name}")
            return True
        else:
            print(f"Failed to sync save data for {character_name}")
            return False
    
    def _load_chapter_save(self, character_name: str, chapter: str) -> Optional[Dict]:
        """Load save data from a specific chapter."""
        chapter_path = self.chapters_dir / chapter
        if not chapter_path.exists():
            return None
        
        save_file = chapter_path / "saves" / f"{character_name}.json"
        if save_file.exists():
            try:
                with open(save_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load save data: {e}")
                return None
        
        return None
    
    def _save_to_shared_storage(self, save_data: SaveData) -> bool:
        """Save data to shared storage."""
        conn = sqlite3.connect(self.shared_db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO save_files 
                (character_name, chapter, save_data, created_at, version)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                save_data.player_name,
                save_data.chapter,
                json.dumps(asdict(save_data)),
                save_data.timestamp,
                save_data.version
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Failed to save to shared storage: {e}")
            return False
        finally:
            conn.close()
    
    def register_achievement(self, achievement: Achievement) -> bool:
        """Register a new achievement."""
        conn = sqlite3.connect(self.shared_db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO achievements 
                (id, name, description, chapter, requirements, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                achievement.id,
                achievement.name,
                achievement.description,
                achievement.chapter,
                json.dumps(achievement.requirements),
                datetime.now().isoformat()
            ))
            conn.commit()
            print(f"✓ Achievement '{achievement.name}' registered")
            return True
        except Exception as e:
            print(f"Failed to register achievement: {e}")
            return False
        finally:
            conn.close()
    
    def unlock_achievement(self, character_name: str, achievement_id: str) -> bool:
        """Unlock an achievement for a character."""
        conn = sqlite3.connect(self.shared_db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO unlocked_achievements 
                (character_name, achievement_id, unlocked_at)
                VALUES (?, ?, ?)
            ''', (
                character_name,
                achievement_id,
                datetime.now().isoformat()
            ))
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f"✓ Achievement unlocked for {character_name}")
                return True
            else:
                print(f"Achievement already unlocked for {character_name}")
                return False
        except Exception as e:
            print(f"Failed to unlock achievement: {e}")
            return False
        finally:
            conn.close()
    
    def get_character_achievements(self, character_name: str) -> List[Achievement]:
        """Get all achievements for a character."""
        conn = sqlite3.connect(self.shared_db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT a.id, a.name, a.description, a.chapter, a.requirements,
                       ua.unlocked_at
                FROM achievements a
                LEFT JOIN unlocked_achievements ua 
                    ON a.id = ua.achievement_id AND ua.character_name = ?
                ORDER BY a.chapter, a.name
            ''', (character_name,))
            
            achievements = []
            for row in cursor.fetchall():
                achievement = Achievement(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    chapter=row[3],
                    unlocked=row[5] is not None,
                    unlocked_at=row[5],
                    requirements=json.loads(row[4])
                )
                achievements.append(achievement)
            
            return achievements
        except Exception as e:
            print(f"Failed to get character achievements: {e}")
            return []
        finally:
            conn.close()
    
    def create_shared_asset_library(self) -> bool:
        """Create a shared asset library for cross-chapter use."""
        print("Creating shared asset library...")
        
        shared_assets_dir = self.shared_dir / "assets"
        shared_assets_dir.mkdir(exist_ok=True)
        
        # Create organized structure
        asset_types = ["sprites", "sounds", "music", "ui", "fonts", "templates"]
        for asset_type in asset_types:
            (shared_assets_dir / asset_type).mkdir(exist_ok=True)
        
        # Create asset manifest
        manifest = {
            "created_at": datetime.now().isoformat(),
            "version": "1.0",
            "asset_types": asset_types,
            "assets": {}
        }
        
        manifest_file = shared_assets_dir / "manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print("✓ Shared asset library created")
        return True
    
    def get_saga_progress(self, character_name: str) -> Dict[str, Any]:
        """Get overall saga progress for a character."""
        conn = sqlite3.connect(self.shared_db_path)
        cursor = conn.cursor()
        
        try:
            # Get character data
            cursor.execute('''
                SELECT chapter_progress FROM characters WHERE name = ?
            ''', (character_name,))
            
            row = cursor.fetchone()
            if not row:
                return {"error": "Character not found"}
            
            chapter_progress = json.loads(row[0])
            
            # Get achievement count
            cursor.execute('''
                SELECT COUNT(*) FROM unlocked_achievements WHERE character_name = ?
            ''', (character_name,))
            
            achievement_count = cursor.fetchone()[0]
            
            # Get total achievements
            cursor.execute('SELECT COUNT(*) FROM achievements')
            total_achievements = cursor.fetchone()[0]
            
            return {
                "character_name": character_name,
                "chapters_completed": sum(chapter_progress.values()),
                "total_chapters": len(chapter_progress),
                "achievements_unlocked": achievement_count,
                "total_achievements": total_achievements,
                "progress_percentage": (achievement_count / total_achievements * 100) if total_achievements > 0 else 0
            }
        except Exception as e:
            return {"error": f"Failed to get progress: {e}"}
        finally:
            conn.close()

def main():
    """CLI interface for cross-chapter features."""
    features = CrossChapterFeatures()
    
    if len(sys.argv) < 2:
        print("Cross-Chapter Features for Chronicles of Ruin")
        print("Usage:")
        print("  python cross_chapter_features.py migrate <character> <from_chapter> <to_chapter>")
        print("  python cross_chapter_features.py sync <character> <chapter>")
        print("  python cross_chapter_features.py register_achievement <id> <name> <description> <chapter>")
        print("  python cross_chapter_features.py unlock <character> <achievement_id>")
        print("  python cross_chapter_features.py achievements <character>")
        print("  python cross_chapter_features.py progress <character>")
        print("  python cross_chapter_features.py create_asset_library")
        return
    
    command = sys.argv[1]
    
    if command == "migrate" and len(sys.argv) >= 5:
        character = sys.argv[2]
        from_chapter = sys.argv[3]
        to_chapter = sys.argv[4]
        features.migrate_character(character, from_chapter, to_chapter)
    
    elif command == "sync" and len(sys.argv) >= 4:
        character = sys.argv[2]
        chapter = sys.argv[3]
        features.sync_save_data(character, chapter)
    
    elif command == "register_achievement" and len(sys.argv) >= 6:
        achievement_id = sys.argv[2]
        name = sys.argv[3]
        description = sys.argv[4]
        chapter = sys.argv[5]
        
        achievement = Achievement(
            id=achievement_id,
            name=name,
            description=description,
            chapter=chapter,
            unlocked=False,
            unlocked_at=None,
            requirements={}
        )
        features.register_achievement(achievement)
    
    elif command == "unlock" and len(sys.argv) >= 4:
        character = sys.argv[2]
        achievement_id = sys.argv[3]
        features.unlock_achievement(character, achievement_id)
    
    elif command == "achievements" and len(sys.argv) >= 3:
        character = sys.argv[2]
        achievements = features.get_character_achievements(character)
        print(f"Achievements for {character}:")
        for achievement in achievements:
            status = "✓" if achievement.unlocked else "○"
            print(f"  {status} {achievement.name} ({achievement.chapter})")
    
    elif command == "progress" and len(sys.argv) >= 3:
        character = sys.argv[2]
        progress = features.get_saga_progress(character)
        if "error" in progress:
            print(f"Error: {progress['error']}")
        else:
            print(f"Saga Progress for {character}:")
            print(f"  Chapters completed: {progress['chapters_completed']}/{progress['total_chapters']}")
            print(f"  Achievements: {progress['achievements_unlocked']}/{progress['total_achievements']}")
            print(f"  Progress: {progress['progress_percentage']:.1f}%")
    
    elif command == "create_asset_library":
        features.create_shared_asset_library()
    
    else:
        print("Invalid command or missing arguments!")

if __name__ == "__main__":
    main()

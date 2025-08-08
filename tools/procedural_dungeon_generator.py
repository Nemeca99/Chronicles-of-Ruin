#!/usr/bin/env python3
"""
Procedural Dungeon Generator for Chronicles of Ruin - Phase 2
Advanced dungeon generation with AI testing and balance validation
"""

import sys
import json
import time
import random
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

class RoomType(Enum):
    """Types of dungeon rooms"""
    ENTRANCE = "entrance"
    COMBAT = "combat"
    TREASURE = "treasure"
    BOSS = "boss"
    PUZZLE = "puzzle"
    TRAP = "trap"
    SANCTUARY = "sanctuary"  # Safe rest area
    SECRET = "secret"
    MERCHANT = "merchant"
    STORY = "story"

class DungeonTheme(Enum):
    """Dungeon visual/thematic styles"""
    ANCIENT_RUINS = "ancient_ruins"
    CORRUPTED_FOREST = "corrupted_forest"
    UNDERGROUND_CAVERNS = "underground_caverns"
    ABANDONED_TEMPLE = "abandoned_temple"
    CRYSTAL_CAVES = "crystal_caves"
    SHADOW_REALM = "shadow_realm"
    ELEMENTAL_PLANE = "elemental_plane"

class DungeonDifficulty(Enum):
    """Dungeon difficulty levels"""
    EASY = "easy"         # 3-5 rooms, basic encounters
    MEDIUM = "medium"     # 6-10 rooms, moderate challenges
    HARD = "hard"         # 11-15 rooms, difficult encounters
    EXTREME = "extreme"   # 16-20 rooms, very challenging
    LEGENDARY = "legendary" # 20+ rooms, epic challenges

@dataclass
class DungeonRoom:
    """Individual dungeon room"""
    id: str
    room_type: RoomType
    x: int
    y: int
    width: int
    height: int
    connections: List[str]  # Connected room IDs
    monsters: List[Dict[str, Any]]
    treasures: List[Dict[str, Any]]
    special_features: List[str]
    difficulty_rating: float
    description: str

@dataclass
class DungeonLayout:
    """Complete dungeon layout"""
    id: str
    name: str
    theme: DungeonTheme
    difficulty: DungeonDifficulty
    level_range: Tuple[int, int]
    rooms: Dict[str, DungeonRoom]
    entrance_room: str
    boss_room: Optional[str]
    estimated_completion_time: int  # Minutes
    loot_quality: str
    special_mechanics: List[str]
    ai_test_results: Dict[str, Any]

class ProceduralDungeonGenerator:
    """Advanced procedural dungeon generation system"""
    
    def __init__(self):
        self.dungeons_file = Path("chapters/chapter_01_sunderfall/data/procedural_dungeons.json")
        self.generated_dungeons: Dict[str, DungeonLayout] = self._load_dungeons()
        
        # Generation parameters
        self.room_templates = self._initialize_room_templates()
        self.theme_configs = self._initialize_theme_configs()
        self.difficulty_configs = self._initialize_difficulty_configs()
        
    def _load_dungeons(self) -> Dict[str, DungeonLayout]:
        """Load existing dungeons from file"""
        if self.dungeons_file.exists():
            try:
                with open(self.dungeons_file, 'r') as f:
                    data = json.load(f)
                
                dungeons = {}
                for dungeon_id, dungeon_data in data.items():
                    # Reconstruct DungeonLayout objects
                    rooms = {}
                    for room_id, room_data in dungeon_data['rooms'].items():
                        rooms[room_id] = DungeonRoom(
                            id=room_data['id'],
                            room_type=RoomType(room_data['room_type']),
                            x=room_data['x'],
                            y=room_data['y'],
                            width=room_data['width'],
                            height=room_data['height'],
                            connections=room_data['connections'],
                            monsters=room_data['monsters'],
                            treasures=room_data['treasures'],
                            special_features=room_data['special_features'],
                            difficulty_rating=room_data['difficulty_rating'],
                            description=room_data['description']
                        )
                    
                    dungeons[dungeon_id] = DungeonLayout(
                        id=dungeon_data['id'],
                        name=dungeon_data['name'],
                        theme=DungeonTheme(dungeon_data['theme']),
                        difficulty=DungeonDifficulty(dungeon_data['difficulty']),
                        level_range=tuple(dungeon_data['level_range']),
                        rooms=rooms,
                        entrance_room=dungeon_data['entrance_room'],
                        boss_room=dungeon_data.get('boss_room'),
                        estimated_completion_time=dungeon_data['estimated_completion_time'],
                        loot_quality=dungeon_data['loot_quality'],
                        special_mechanics=dungeon_data['special_mechanics'],
                        ai_test_results=dungeon_data.get('ai_test_results', {})
                    )
                
                return dungeons
                
            except Exception as e:
                print(f"Error loading dungeons: {e}")
        
        return {}
    
    def _save_dungeons(self):
        """Save dungeons to file"""
        self.dungeons_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to JSON-serializable format
        data = {}
        for dungeon_id, dungeon in self.generated_dungeons.items():
            data[dungeon_id] = {
                'id': dungeon.id,
                'name': dungeon.name,
                'theme': dungeon.theme.value,
                'difficulty': dungeon.difficulty.value,
                'level_range': list(dungeon.level_range),
                'rooms': {
                    room_id: {
                        'id': room.id,
                        'room_type': room.room_type.value,
                        'x': room.x,
                        'y': room.y,
                        'width': room.width,
                        'height': room.height,
                        'connections': room.connections,
                        'monsters': room.monsters,
                        'treasures': room.treasures,
                        'special_features': room.special_features,
                        'difficulty_rating': room.difficulty_rating,
                        'description': room.description
                    }
                    for room_id, room in dungeon.rooms.items()
                },
                'entrance_room': dungeon.entrance_room,
                'boss_room': dungeon.boss_room,
                'estimated_completion_time': dungeon.estimated_completion_time,
                'loot_quality': dungeon.loot_quality,
                'special_mechanics': dungeon.special_mechanics,
                'ai_test_results': dungeon.ai_test_results
            }
        
        with open(self.dungeons_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _initialize_room_templates(self) -> Dict[RoomType, Dict]:
        """Initialize room generation templates"""
        return {
            RoomType.ENTRANCE: {
                'size_range': (3, 5),
                'monster_count': (0, 1),
                'treasure_chance': 0.1,
                'special_features': ['entrance_door', 'warning_sign'],
                'difficulty_multiplier': 0.8
            },
            RoomType.COMBAT: {
                'size_range': (4, 8),
                'monster_count': (2, 5),
                'treasure_chance': 0.3,
                'special_features': ['combat_arena', 'weapon_rack'],
                'difficulty_multiplier': 1.0
            },
            RoomType.TREASURE: {
                'size_range': (3, 6),
                'monster_count': (0, 2),
                'treasure_chance': 0.8,
                'special_features': ['treasure_chest', 'golden_altar'],
                'difficulty_multiplier': 0.7
            },
            RoomType.BOSS: {
                'size_range': (8, 12),
                'monster_count': (1, 1),  # Single boss
                'treasure_chance': 1.0,
                'special_features': ['boss_arena', 'ritual_circle', 'throne'],
                'difficulty_multiplier': 2.0
            },
            RoomType.PUZZLE: {
                'size_range': (4, 7),
                'monster_count': (0, 1),
                'treasure_chance': 0.6,
                'special_features': ['ancient_mechanism', 'rune_stones', 'pressure_plates'],
                'difficulty_multiplier': 1.2
            },
            RoomType.TRAP: {
                'size_range': (3, 6),
                'monster_count': (0, 2),
                'treasure_chance': 0.4,
                'special_features': ['spike_trap', 'poison_darts', 'collapsing_ceiling'],
                'difficulty_multiplier': 1.3
            },
            RoomType.SANCTUARY: {
                'size_range': (4, 6),
                'monster_count': (0, 0),
                'treasure_chance': 0.2,
                'special_features': ['healing_fountain', 'safe_campfire', 'blessed_shrine'],
                'difficulty_multiplier': 0.0
            },
            RoomType.SECRET: {
                'size_range': (2, 4),
                'monster_count': (0, 3),
                'treasure_chance': 0.9,
                'special_features': ['hidden_passage', 'secret_cache', 'ancient_artifact'],
                'difficulty_multiplier': 1.5
            }
        }
    
    def _initialize_theme_configs(self) -> Dict[DungeonTheme, Dict]:
        """Initialize theme-specific configurations"""
        return {
            DungeonTheme.ANCIENT_RUINS: {
                'monster_types': ['skeleton', 'ancient_guardian', 'stone_golem'],
                'treasure_types': ['ancient_artifact', 'gold_coins', 'ritual_tome'],
                'special_mechanics': ['crumbling_walls', 'ancient_traps'],
                'description_words': ['crumbling', 'ancient', 'weathered', 'moss-covered']
            },
            DungeonTheme.CORRUPTED_FOREST: {
                'monster_types': ['corrupted_wolf', 'dark_sprite', 'twisted_treant'],
                'treasure_types': ['nature_essence', 'corrupted_seed', 'forest_bow'],
                'special_mechanics': ['growing_vines', 'poisonous_air'],
                'description_words': ['twisted', 'dark', 'overgrown', 'corrupted']
            },
            DungeonTheme.UNDERGROUND_CAVERNS: {
                'monster_types': ['cave_troll', 'crystal_spider', 'underground_dweller'],
                'treasure_types': ['rare_crystals', 'cave_pearls', 'mining_equipment'],
                'special_mechanics': ['cave_ins', 'crystal_formations'],
                'description_words': ['echoing', 'damp', 'crystalline', 'shadowy']
            },
            DungeonTheme.ABANDONED_TEMPLE: {
                'monster_types': ['temple_guardian', 'possessed_statue', 'shadow_priest'],
                'treasure_types': ['holy_relic', 'blessed_weapon', 'divine_scroll'],
                'special_mechanics': ['divine_barriers', 'holy_trials'],
                'description_words': ['sacred', 'abandoned', 'divine', 'marble']
            }
        }
    
    def _initialize_difficulty_configs(self) -> Dict[DungeonDifficulty, Dict]:
        """Initialize difficulty-specific configurations"""
        return {
            DungeonDifficulty.EASY: {
                'room_count': (3, 5),
                'monster_level_bonus': 0,
                'treasure_quality': 'common',
                'special_room_chance': 0.2,
                'completion_time': (10, 20)
            },
            DungeonDifficulty.MEDIUM: {
                'room_count': (6, 10),
                'monster_level_bonus': 2,
                'treasure_quality': 'uncommon',
                'special_room_chance': 0.3,
                'completion_time': (20, 40)
            },
            DungeonDifficulty.HARD: {
                'room_count': (11, 15),
                'monster_level_bonus': 5,
                'treasure_quality': 'rare',
                'special_room_chance': 0.4,
                'completion_time': (40, 70)
            },
            DungeonDifficulty.EXTREME: {
                'room_count': (16, 20),
                'monster_level_bonus': 8,
                'treasure_quality': 'epic',
                'special_room_chance': 0.5,
                'completion_time': (70, 120)
            },
            DungeonDifficulty.LEGENDARY: {
                'room_count': (20, 30),
                'monster_level_bonus': 12,
                'treasure_quality': 'legendary',
                'special_room_chance': 0.6,
                'completion_time': (120, 200)
            }
        }
    
    def generate_dungeon_interactive(self, creator_id: str) -> Optional[str]:
        """Interactive dungeon generation"""
        print("=== Procedural Dungeon Generator ===\n")
        
        # Basic dungeon information
        name = input("Dungeon name: ").strip()
        if not name:
            print("Name required!")
            return None
        
        # Choose theme
        print("\nAvailable themes:")
        themes = list(DungeonTheme)
        for i, theme in enumerate(themes, 1):
            print(f"  {i}. {theme.value.replace('_', ' ').title()}")
        
        try:
            theme_choice = int(input("Choose theme (1-7): ")) - 1
            theme = themes[theme_choice]
        except (ValueError, IndexError):
            print("Invalid choice!")
            return None
        
        # Choose difficulty
        print("\nAvailable difficulties:")
        difficulties = list(DungeonDifficulty)
        for i, difficulty in enumerate(difficulties, 1):
            config = self.difficulty_configs[difficulty]
            room_range = config['room_count']
            time_range = config['completion_time']
            print(f"  {i}. {difficulty.value.title()} ({room_range[0]}-{room_range[1]} rooms, {time_range[0]}-{time_range[1]} min)")
        
        try:
            diff_choice = int(input("Choose difficulty (1-5): ")) - 1
            difficulty = difficulties[diff_choice]
        except (ValueError, IndexError):
            print("Invalid choice!")
            return None
        
        # Level range
        try:
            min_level = int(input("Minimum player level: "))
            max_level = int(input("Maximum player level: "))
            if min_level > max_level:
                min_level, max_level = max_level, min_level
        except ValueError:
            print("Invalid level range!")
            return None
        
        # Generate the dungeon
        print(f"\nGenerating {difficulty.value} {theme.value.replace('_', ' ')} dungeon...")
        dungeon = self._generate_dungeon_layout(name, theme, difficulty, (min_level, max_level), creator_id)
        
        if dungeon:
            self.generated_dungeons[dungeon.id] = dungeon
            self._save_dungeons()
            
            print(f"\n✅ Dungeon '{name}' generated successfully!")
            print(f"Dungeon ID: {dungeon.id}")
            print(f"Theme: {theme.value.replace('_', ' ').title()}")
            print(f"Difficulty: {difficulty.value.title()}")
            print(f"Rooms: {len(dungeon.rooms)}")
            print(f"Estimated time: {dungeon.estimated_completion_time} minutes")
            print(f"Special mechanics: {', '.join(dungeon.special_mechanics)}")
            
            return dungeon.id
        
        return None
    
    def _generate_dungeon_layout(self, name: str, theme: DungeonTheme, difficulty: DungeonDifficulty, 
                                level_range: Tuple[int, int], creator_id: str) -> DungeonLayout:
        """Generate complete dungeon layout"""
        dungeon_id = f"dungeon_{creator_id}_{int(time.time())}"
        
        # Get configuration
        diff_config = self.difficulty_configs[difficulty]
        theme_config = self.theme_configs[theme]
        
        # Determine room count
        room_count = random.randint(*diff_config['room_count'])
        
        # Generate room layout
        rooms = self._generate_room_layout(room_count, theme, difficulty, level_range)
        
        # Identify special rooms
        entrance_room = next(room_id for room_id, room in rooms.items() if room.room_type == RoomType.ENTRANCE)
        boss_room = next((room_id for room_id, room in rooms.items() if room.room_type == RoomType.BOSS), None)
        
        # Calculate completion time
        base_time = random.randint(*diff_config['completion_time'])
        complexity_bonus = max(0, (room_count - diff_config['room_count'][0]) * 2)
        estimated_time = base_time + complexity_bonus
        
        # Select special mechanics
        special_mechanics = theme_config['special_mechanics'].copy()
        if random.random() < 0.3:  # 30% chance for additional mechanic
            additional_mechanics = ['time_pressure', 'limited_resources', 'puzzle_chains', 'environmental_hazards']
            special_mechanics.append(random.choice(additional_mechanics))
        
        return DungeonLayout(
            id=dungeon_id,
            name=name,
            theme=theme,
            difficulty=difficulty,
            level_range=level_range,
            rooms=rooms,
            entrance_room=entrance_room,
            boss_room=boss_room,
            estimated_completion_time=estimated_time,
            loot_quality=diff_config['treasure_quality'],
            special_mechanics=special_mechanics,
            ai_test_results={}
        )
    
    def _generate_room_layout(self, room_count: int, theme: DungeonTheme, difficulty: DungeonDifficulty, 
                             level_range: Tuple[int, int]) -> Dict[str, DungeonRoom]:
        """Generate the layout and connections of rooms"""
        rooms = {}
        
        # Always have entrance and boss rooms
        required_rooms = [RoomType.ENTRANCE]
        if room_count >= 5:  # Only add boss room for larger dungeons
            required_rooms.append(RoomType.BOSS)
        
        # Fill remaining slots with various room types
        available_room_types = [
            RoomType.COMBAT, RoomType.COMBAT, RoomType.COMBAT,  # Combat is most common
            RoomType.TREASURE, RoomType.TREASURE,
            RoomType.PUZZLE, RoomType.TRAP,
            RoomType.SANCTUARY, RoomType.SECRET
        ]
        
        room_types = required_rooms.copy()
        for _ in range(room_count - len(required_rooms)):
            room_types.append(random.choice(available_room_types))
        
        # Generate individual rooms
        grid_size = int((room_count ** 0.5) * 1.5) + 2  # Rough grid for layout
        used_positions = set()
        
        for i, room_type in enumerate(room_types):
            # Find position
            attempts = 0
            while attempts < 50:
                x = random.randint(0, grid_size - 1)
                y = random.randint(0, grid_size - 1)
                
                if (x, y) not in used_positions:
                    used_positions.add((x, y))
                    break
                attempts += 1
            else:
                # Fallback positioning
                x, y = i % grid_size, i // grid_size
            
            # Generate room
            room = self._generate_individual_room(
                f"room_{i:02d}",
                room_type,
                x, y,
                theme,
                difficulty,
                level_range
            )
            
            rooms[room.id] = room
        
        # Connect rooms
        self._connect_rooms(rooms, grid_size)
        
        return rooms
    
    def _generate_individual_room(self, room_id: str, room_type: RoomType, x: int, y: int,
                                 theme: DungeonTheme, difficulty: DungeonDifficulty, 
                                 level_range: Tuple[int, int]) -> DungeonRoom:
        """Generate an individual room"""
        template = self.room_templates[room_type]
        theme_config = self.theme_configs[theme]
        diff_config = self.difficulty_configs[difficulty]
        
        # Room size
        size = random.randint(*template['size_range'])
        
        # Monsters
        monsters = []
        if template['monster_count'][1] > 0:
            monster_count = random.randint(*template['monster_count'])
            for _ in range(monster_count):
                monster_type = random.choice(theme_config['monster_types'])
                monster_level = random.randint(*level_range) + diff_config['monster_level_bonus']
                
                monster = {
                    'type': monster_type,
                    'level': monster_level,
                    'is_boss': room_type == RoomType.BOSS,
                    'special_abilities': self._generate_monster_abilities(room_type, theme)
                }
                monsters.append(monster)
        
        # Treasures
        treasures = []
        if random.random() < template['treasure_chance']:
            treasure_count = 1 if room_type != RoomType.TREASURE else random.randint(1, 3)
            for _ in range(treasure_count):
                treasure_type = random.choice(theme_config['treasure_types'])
                treasure = {
                    'type': treasure_type,
                    'quality': diff_config['treasure_quality'],
                    'level_requirement': level_range[0]
                }
                treasures.append(treasure)
        
        # Special features
        num_features = random.randint(1, 3)
        special_features = random.sample(template['special_features'], 
                                       min(num_features, len(template['special_features'])))
        
        # Add theme-specific features
        if random.random() < 0.3:
            theme_features = {
                DungeonTheme.ANCIENT_RUINS: ['cracked_pillars', 'ancient_murals'],
                DungeonTheme.CORRUPTED_FOREST: ['twisted_roots', 'dark_mist'],
                DungeonTheme.UNDERGROUND_CAVERNS: ['stalactites', 'underground_stream'],
                DungeonTheme.ABANDONED_TEMPLE: ['prayer_alcoves', 'broken_statues']
            }
            if theme in theme_features:
                special_features.append(random.choice(theme_features[theme]))
        
        # Calculate difficulty rating
        monster_difficulty = sum(m['level'] for m in monsters) * template['difficulty_multiplier']
        puzzle_difficulty = 5.0 if 'puzzle' in [f.lower() for f in special_features] else 0.0
        base_difficulty = len(monsters) * 2 + len(treasures) + len(special_features)
        
        difficulty_rating = (monster_difficulty + puzzle_difficulty + base_difficulty) / 10.0
        
        # Generate description
        theme_words = theme_config['description_words']
        description = self._generate_room_description(room_type, theme_words, special_features)
        
        return DungeonRoom(
            id=room_id,
            room_type=room_type,
            x=x,
            y=y,
            width=size,
            height=size,
            connections=[],  # Will be filled by _connect_rooms
            monsters=monsters,
            treasures=treasures,
            special_features=special_features,
            difficulty_rating=difficulty_rating,
            description=description
        )
    
    def _generate_monster_abilities(self, room_type: RoomType, theme: DungeonTheme) -> List[str]:
        """Generate special abilities for monsters based on room type and theme"""
        abilities = []
        
        # Room type abilities
        if room_type == RoomType.BOSS:
            abilities.extend(['boss_immunity', 'phase_transition', 'area_attack'])
        elif room_type == RoomType.TRAP:
            abilities.extend(['trap_synergy', 'environmental_damage'])
        elif room_type == RoomType.COMBAT:
            abilities.extend(['combat_expertise', 'pack_tactics'])
        
        # Theme abilities
        theme_abilities = {
            DungeonTheme.CORRUPTED_FOREST: ['poison_aura', 'nature_magic'],
            DungeonTheme.ANCIENT_RUINS: ['ancient_knowledge', 'stone_skin'],
            DungeonTheme.UNDERGROUND_CAVERNS: ['tremor_attack', 'darkness_vision'],
            DungeonTheme.ABANDONED_TEMPLE: ['divine_resistance', 'holy_vulnerability']
        }
        
        if theme in theme_abilities:
            abilities.extend(random.sample(theme_abilities[theme], 
                                         min(2, len(theme_abilities[theme]))))
        
        return abilities[:3]  # Max 3 abilities
    
    def _connect_rooms(self, rooms: Dict[str, DungeonRoom], grid_size: int):
        """Create connections between rooms"""
        room_list = list(rooms.values())
        
        # Create a minimum spanning tree-like connection
        connected = set()
        
        # Start with entrance room
        entrance = next(room for room in room_list if room.room_type == RoomType.ENTRANCE)
        connected.add(entrance.id)
        
        while len(connected) < len(room_list):
            # Find closest unconnected room to any connected room
            best_connection = None
            best_distance = float('inf')
            
            for connected_room_id in connected:
                connected_room = rooms[connected_room_id]
                
                for room in room_list:
                    if room.id not in connected:
                        # Calculate Manhattan distance
                        distance = abs(room.x - connected_room.x) + abs(room.y - connected_room.y)
                        
                        if distance < best_distance:
                            best_distance = distance
                            best_connection = (connected_room_id, room.id)
            
            if best_connection:
                room1_id, room2_id = best_connection
                rooms[room1_id].connections.append(room2_id)
                rooms[room2_id].connections.append(room1_id)
                connected.add(room2_id)
        
        # Add some additional connections for complexity (create loops)
        additional_connections = min(3, len(room_list) // 3)
        for _ in range(additional_connections):
            room1 = random.choice(room_list)
            nearby_rooms = [
                room for room in room_list 
                if room.id != room1.id 
                and abs(room.x - room1.x) + abs(room.y - room1.y) <= 2
                and room.id not in room1.connections
            ]
            
            if nearby_rooms:
                room2 = random.choice(nearby_rooms)
                room1.connections.append(room2.id)
                room2.connections.append(room1.id)
    
    def _generate_room_description(self, room_type: RoomType, theme_words: List[str], 
                                  special_features: List[str]) -> str:
        """Generate descriptive text for a room"""
        theme_word = random.choice(theme_words)
        
        base_descriptions = {
            RoomType.ENTRANCE: f"A {theme_word} chamber that serves as the entrance to this forgotten place",
            RoomType.COMBAT: f"A {theme_word} arena where countless battles have been fought",
            RoomType.TREASURE: f"A {theme_word} vault containing precious treasures",
            RoomType.BOSS: f"A massive {theme_word} hall dominated by an ominous presence",
            RoomType.PUZZLE: f"A {theme_word} chamber filled with ancient mechanisms and riddles",
            RoomType.TRAP: f"A {theme_word} corridor riddled with dangerous contraptions",
            RoomType.SANCTUARY: f"A peaceful {theme_word} sanctuary offering respite from danger",
            RoomType.SECRET: f"A hidden {theme_word} chamber concealed from prying eyes"
        }
        
        description = base_descriptions.get(room_type, f"A {theme_word} room of unknown purpose")
        
        # Add feature descriptions
        if special_features:
            feature_desc = ", ".join(special_features[:2])
            description += f". Notable features include {feature_desc}."
        
        return description
    
    def test_dungeon_with_ai(self, dungeon_id: str) -> Dict[str, Any]:
        """Test dungeon with AI players"""
        if dungeon_id not in self.generated_dungeons:
            return {'error': 'Dungeon not found'}
        
        dungeon = self.generated_dungeons[dungeon_id]
        print(f"\n=== AI Testing Dungeon: {dungeon.name} ===")
        
        # Simulate AI testing
        test_sessions = []
        
        for party_size in [1, 3, 5]:
            for skill_level in ['noob', 'expert']:
                # Simulate dungeon run
                success_rate = self._calculate_success_rate(dungeon, party_size, skill_level)
                completion_time = self._simulate_completion_time(dungeon, party_size, skill_level)
                
                session = {
                    'party_size': party_size,
                    'skill_level': skill_level,
                    'success_rate': success_rate,
                    'completion_time': completion_time,
                    'rooms_completed': self._simulate_rooms_completed(dungeon, success_rate),
                    'loot_obtained': self._simulate_loot_obtained(dungeon, success_rate),
                    'difficulty_feedback': self._generate_difficulty_feedback(dungeon, success_rate)
                }
                test_sessions.append(session)
        
        # Analyze results
        avg_success_rate = sum(s['success_rate'] for s in test_sessions) / len(test_sessions)
        avg_completion_time = sum(s['completion_time'] for s in test_sessions if s['success_rate'] > 0.5) / max(1, len([s for s in test_sessions if s['success_rate'] > 0.5]))
        
        balance_rating = self._assess_dungeon_balance(test_sessions, dungeon)
        
        test_results = {
            'test_time': time.time(),
            'sessions': test_sessions,
            'average_success_rate': avg_success_rate,
            'average_completion_time': avg_completion_time,
            'balance_rating': balance_rating,
            'recommendations': self._generate_dungeon_recommendations(test_sessions, dungeon)
        }
        
        # Save results
        self.generated_dungeons[dungeon_id].ai_test_results = test_results
        self._save_dungeons()
        
        print(f"Average Success Rate: {avg_success_rate:.1%}")
        print(f"Average Completion Time: {avg_completion_time:.1f} minutes")
        print(f"Balance Rating: {balance_rating:.2f}")
        print("Recommendations:")
        for rec in test_results['recommendations']:
            print(f"  - {rec}")
        
        return test_results
    
    def _calculate_success_rate(self, dungeon: DungeonLayout, party_size: int, skill_level: str) -> float:
        """Calculate predicted success rate for dungeon"""
        base_rate = 0.3  # Base 30% success rate
        
        # Party size bonus
        party_bonus = (party_size - 1) * 0.15  # 15% per additional party member
        
        # Skill level bonus
        skill_bonus = 0.3 if skill_level == 'expert' else -0.2
        
        # Difficulty penalty
        difficulty_penalty = {
            DungeonDifficulty.EASY: 0.0,
            DungeonDifficulty.MEDIUM: -0.1,
            DungeonDifficulty.HARD: -0.2,
            DungeonDifficulty.EXTREME: -0.3,
            DungeonDifficulty.LEGENDARY: -0.4
        }[dungeon.difficulty]
        
        # Room count penalty
        room_penalty = max(0, (len(dungeon.rooms) - 5) * 0.02)  # 2% per room over 5
        
        success_rate = base_rate + party_bonus + skill_bonus + difficulty_penalty - room_penalty
        return max(0.05, min(0.95, success_rate))  # Clamp between 5% and 95%
    
    def _simulate_completion_time(self, dungeon: DungeonLayout, party_size: int, skill_level: str) -> float:
        """Simulate completion time"""
        base_time = dungeon.estimated_completion_time
        
        # Party efficiency
        party_multiplier = max(0.7, 1.0 - (party_size - 1) * 0.1)  # Larger parties are more efficient
        
        # Skill multiplier
        skill_multiplier = 0.8 if skill_level == 'expert' else 1.3
        
        # Add randomness
        randomness = random.uniform(0.8, 1.2)
        
        return base_time * party_multiplier * skill_multiplier * randomness
    
    def _simulate_rooms_completed(self, dungeon: DungeonLayout, success_rate: float) -> int:
        """Simulate number of rooms completed"""
        total_rooms = len(dungeon.rooms)
        if success_rate >= 0.8:
            return total_rooms  # Full completion
        else:
            # Partial completion based on success rate
            return max(1, int(total_rooms * success_rate * random.uniform(0.8, 1.2)))
    
    def _simulate_loot_obtained(self, dungeon: DungeonLayout, success_rate: float) -> Dict[str, int]:
        """Simulate loot obtained"""
        loot = {'common': 0, 'uncommon': 0, 'rare': 0, 'epic': 0, 'legendary': 0}
        
        # Base loot based on rooms completed
        rooms_completed = self._simulate_rooms_completed(dungeon, success_rate)
        
        for room in list(dungeon.rooms.values())[:rooms_completed]:
            for treasure in room.treasures:
                quality = treasure.get('quality', 'common')
                if quality in loot:
                    loot[quality] += 1
        
        return loot
    
    def _generate_difficulty_feedback(self, dungeon: DungeonLayout, success_rate: float) -> str:
        """Generate difficulty feedback"""
        if success_rate >= 0.8:
            return "Dungeon feels well-balanced and engaging"
        elif success_rate >= 0.6:
            return "Challenging but fair difficulty"
        elif success_rate >= 0.4:
            return "High difficulty, may frustrate casual players"
        elif success_rate >= 0.2:
            return "Very difficult, suitable only for experienced players"
        else:
            return "Extremely difficult, may be unbalanced"
    
    def _assess_dungeon_balance(self, sessions: List[Dict], dungeon: DungeonLayout) -> float:
        """Assess overall dungeon balance (0.0 to 1.0)"""
        avg_success_rate = sum(s['success_rate'] for s in sessions) / len(sessions)
        
        # Target success rates by difficulty
        target_rates = {
            DungeonDifficulty.EASY: 0.8,
            DungeonDifficulty.MEDIUM: 0.6,
            DungeonDifficulty.HARD: 0.4,
            DungeonDifficulty.EXTREME: 0.25,
            DungeonDifficulty.LEGENDARY: 0.15
        }
        
        target = target_rates[dungeon.difficulty]
        difference = abs(avg_success_rate - target)
        
        return max(0.0, 1.0 - (difference / target))
    
    def _generate_dungeon_recommendations(self, sessions: List[Dict], dungeon: DungeonLayout) -> List[str]:
        """Generate recommendations for dungeon improvement"""
        recommendations = []
        avg_success_rate = sum(s['success_rate'] for s in sessions) / len(sessions)
        
        if avg_success_rate > 0.8:
            recommendations.append("Dungeon may be too easy - consider adding more challenging encounters")
        elif avg_success_rate < 0.2:
            recommendations.append("Dungeon may be too difficult - consider reducing monster levels or trap intensity")
        
        # Check completion time
        completion_times = [s['completion_time'] for s in sessions if s['success_rate'] > 0.5]
        if completion_times:
            avg_time = sum(completion_times) / len(completion_times)
            if avg_time > dungeon.estimated_completion_time * 1.5:
                recommendations.append("Dungeon takes longer than expected - consider streamlining some encounters")
        
        # Check party size impact
        solo_success = sum(s['success_rate'] for s in sessions if s['party_size'] == 1) / len([s for s in sessions if s['party_size'] == 1])
        party_success = sum(s['success_rate'] for s in sessions if s['party_size'] > 1) / len([s for s in sessions if s['party_size'] > 1])
        
        if party_success / max(solo_success, 0.1) > 3:
            recommendations.append("Dungeon heavily favors group play - consider adding solo-friendly elements")
        
        return recommendations
    
    def list_dungeons(self, creator_id: Optional[str] = None) -> List[Dict]:
        """List all generated dungeons"""
        dungeons_list = []
        
        for dungeon_id, dungeon in self.generated_dungeons.items():
            dungeon_info = {
                'id': dungeon.id,
                'name': dungeon.name,
                'theme': dungeon.theme.value,
                'difficulty': dungeon.difficulty.value,
                'level_range': dungeon.level_range,
                'room_count': len(dungeon.rooms),
                'estimated_time': dungeon.estimated_completion_time,
                'tested': bool(dungeon.ai_test_results)
            }
            dungeons_list.append(dungeon_info)
        
        return sorted(dungeons_list, key=lambda x: x['estimated_time'])
    
    def get_dungeon_details(self, dungeon_id: str) -> Optional[Dict]:
        """Get detailed dungeon information"""
        if dungeon_id not in self.generated_dungeons:
            return None
        
        dungeon = self.generated_dungeons[dungeon_id]
        
        return {
            'basic_info': {
                'id': dungeon.id,
                'name': dungeon.name,
                'theme': dungeon.theme.value,
                'difficulty': dungeon.difficulty.value,
                'level_range': dungeon.level_range,
                'estimated_time': dungeon.estimated_completion_time,
                'loot_quality': dungeon.loot_quality
            },
            'layout': {
                'room_count': len(dungeon.rooms),
                'entrance_room': dungeon.entrance_room,
                'boss_room': dungeon.boss_room,
                'special_mechanics': dungeon.special_mechanics
            },
            'rooms': {
                room_id: {
                    'type': room.room_type.value,
                    'position': (room.x, room.y),
                    'size': (room.width, room.height),
                    'connections': len(room.connections),
                    'monsters': len(room.monsters),
                    'treasures': len(room.treasures),
                    'difficulty': room.difficulty_rating,
                    'description': room.description
                }
                for room_id, room in dungeon.rooms.items()
            },
            'ai_test_results': dungeon.ai_test_results
        }
    
    def delete_dungeon(self, dungeon_id: str) -> bool:
        """Delete a generated dungeon"""
        if dungeon_id not in self.generated_dungeons:
            return False
        
        del self.generated_dungeons[dungeon_id]
        self._save_dungeons()
        return True

def main():
    """Main CLI interface"""
    generator = ProceduralDungeonGenerator()
    
    while True:
        print("\n=== Procedural Dungeon Generator ===")
        print("1. Generate new dungeon")
        print("2. List dungeons")
        print("3. View dungeon details")
        print("4. Test dungeon with AI")
        print("5. Delete dungeon")
        print("0. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            creator_id = input("Creator ID: ").strip()
            if creator_id:
                generator.generate_dungeon_interactive(creator_id)
        
        elif choice == "2":
            dungeons = generator.list_dungeons()
            if dungeons:
                print(f"\n{'ID':<25} {'Name':<20} {'Theme':<15} {'Difficulty':<10} {'Rooms':<6} {'Time':<5} {'Tested'}")
                print("-" * 90)
                for d in dungeons:
                    theme = d['theme'].replace('_', ' ').title()
                    tested = "Yes" if d['tested'] else "No"
                    print(f"{d['id']:<25} {d['name']:<20} {theme:<15} {d['difficulty']:<10} {d['room_count']:<6} {d['estimated_time']:<5} {tested}")
            else:
                print("No dungeons generated yet.")
        
        elif choice == "3":
            dungeon_id = input("Dungeon ID: ").strip()
            details = generator.get_dungeon_details(dungeon_id)
            if details:
                info = details['basic_info']
                layout = details['layout']
                
                print(f"\n=== {info['name']} ===")
                print(f"Theme: {info['theme'].replace('_', ' ').title()}")
                print(f"Difficulty: {info['difficulty'].title()}")
                print(f"Level Range: {info['level_range'][0]}-{info['level_range'][1]}")
                print(f"Estimated Time: {info['estimated_time']} minutes")
                print(f"Room Count: {layout['room_count']}")
                print(f"Special Mechanics: {', '.join(layout['special_mechanics'])}")
                
                print(f"\nRooms:")
                for room_id, room_info in details['rooms'].items():
                    print(f"  {room_id}: {room_info['type']} (Difficulty: {room_info['difficulty']:.1f})")
                    print(f"    {room_info['description']}")
                
                if details['ai_test_results']:
                    results = details['ai_test_results']
                    print(f"\nAI Test Results:")
                    print(f"  Average Success Rate: {results['average_success_rate']:.1%}")
                    print(f"  Average Completion Time: {results['average_completion_time']:.1f} minutes")
            else:
                print("Dungeon not found.")
        
        elif choice == "4":
            dungeon_id = input("Dungeon ID to test: ").strip()
            if dungeon_id in generator.generated_dungeons:
                generator.test_dungeon_with_ai(dungeon_id)
            else:
                print("Dungeon not found.")
        
        elif choice == "5":
            dungeon_id = input("Dungeon ID to delete: ").strip()
            if generator.delete_dungeon(dungeon_id):
                print("Dungeon deleted.")
            else:
                print("Delete failed (dungeon not found).")
        
        elif choice == "0":
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()

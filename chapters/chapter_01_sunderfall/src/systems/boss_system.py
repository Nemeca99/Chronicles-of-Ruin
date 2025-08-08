#!/usr/bin/env python3
"""
Boss System - Chronicles of Ruin: Sunderfall

This module implements boss encounters including district bosses, unique monsters,
world bosses, phase systems, and special abilities.
"""

import random
import math
import time
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum
from .monster_system import MonsterSystem, MonsterArchetype, MonsterClassification
from .player_system import PlayerSystem
from .combat_system import CombatSystem


class BossType(Enum):
    """Types of boss encounters."""
    DISTRICT_BOSS = "district_boss"
    UNIQUE_MONSTER = "unique_monster"
    WORLD_BOSS = "world_boss"
    EVENT_BOSS = "event_boss"


class BossPhase(Enum):
    """Boss fight phases."""
    PHASE_1 = "phase_1"
    PHASE_2 = "phase_2"
    PHASE_3 = "phase_3"
    ENRAGE = "enrage"


class BossAbility(Enum):
    """Special boss abilities."""
    SUMMON_MINIONS = "summon_minions"
    PHASE_TRANSITION = "phase_transition"
    ENVIRONMENTAL_HAZARD = "environmental_hazard"
    HEAL = "heal"
    BUFF = "buff"
    DEBUFF = "debuff"
    AOE_ATTACK = "aoe_attack"
    TELEPORT = "teleport"
    SHIELD = "shield"
    ENRAGE = "enrage"


class BossSystem:
    """
    Boss encounter system implementing complex boss mechanics,
    phase transitions, and special abilities.
    """

    def __init__(self, monster_system: MonsterSystem, player_system: PlayerSystem, 
                 combat_system: CombatSystem):
        """Initialize the boss system."""
        self.monster_system = monster_system
        self.player_system = player_system
        self.combat_system = combat_system
        
        # Boss configurations
        self.boss_configs = self._initialize_boss_configs()
        self.phase_configs = self._initialize_phase_configs()
        self.ability_configs = self._initialize_ability_configs()
        
        # Active boss encounters
        self.active_bosses = {}
        self.boss_cooldowns = {}

    def _initialize_boss_configs(self) -> Dict[str, Dict]:
        """Initialize boss configurations."""
        return {
            "district_boss": {
                "health_multiplier": 5.0,
                "damage_multiplier": 2.0,
                "defense_multiplier": 3.0,
                "level_bonus": 5,
                "phases": 2,
                "abilities": ["summon_minions", "phase_transition"],
                "loot_quality": "rare",
                "unique_item_chance": 0.25
            },
            "unique_monster": {
                "health_multiplier": 3.0,
                "damage_multiplier": 2.5,
                "defense_multiplier": 2.0,
                "level_bonus": 10,
                "phases": 3,
                "abilities": ["environmental_hazard", "teleport", "aoe_attack"],
                "loot_quality": "unique",
                "unique_item_chance": 1.0
            },
            "world_boss": {
                "health_multiplier": 8.0,
                "damage_multiplier": 3.0,
                "defense_multiplier": 4.0,
                "level_bonus": 15,
                "phases": 4,
                "abilities": ["summon_minions", "environmental_hazard", "heal", "enrage"],
                "loot_quality": "legendary",
                "unique_item_chance": 1.0
            },
            "event_boss": {
                "health_multiplier": 6.0,
                "damage_multiplier": 2.8,
                "defense_multiplier": 3.5,
                "level_bonus": 12,
                "phases": 3,
                "abilities": ["buff", "debuff", "aoe_attack", "shield"],
                "loot_quality": "epic",
                "unique_item_chance": 0.75
            }
        }

    def _initialize_phase_configs(self) -> Dict[BossPhase, Dict]:
        """Initialize phase configurations."""
        return {
            BossPhase.PHASE_1: {
                "health_threshold": 1.0,
                "damage_bonus": 0.0,
                "ability_frequency": 0.2,
                "description": "Initial phase - testing the waters"
            },
            BossPhase.PHASE_2: {
                "health_threshold": 0.7,
                "damage_bonus": 0.25,
                "ability_frequency": 0.4,
                "description": "Boss becomes more aggressive"
            },
            BossPhase.PHASE_3: {
                "health_threshold": 0.4,
                "damage_bonus": 0.5,
                "ability_frequency": 0.6,
                "description": "Desperate measures - boss pulls out all stops"
            },
            BossPhase.ENRAGE: {
                "health_threshold": 0.2,
                "damage_bonus": 1.0,
                "ability_frequency": 0.8,
                "description": "Final enrage - boss is unstoppable!"
            }
        }

    def _initialize_ability_configs(self) -> Dict[BossAbility, Dict]:
        """Initialize ability configurations."""
        return {
            BossAbility.SUMMON_MINIONS: {
                "cooldown": 3,
                "minions_count": 2,
                "minion_level": 0.5,
                "description": "Summons minions to aid the boss"
            },
            BossAbility.PHASE_TRANSITION: {
                "cooldown": 0,
                "phase_bonus": 0.25,
                "description": "Transitions to next phase with increased power"
            },
            BossAbility.ENVIRONMENTAL_HAZARD: {
                "cooldown": 4,
                "damage": 0.3,
                "duration": 2,
                "description": "Creates hazardous environment"
            },
            BossAbility.HEAL: {
                "cooldown": 5,
                "heal_percentage": 0.2,
                "description": "Boss heals a portion of health"
            },
            BossAbility.BUFF: {
                "cooldown": 4,
                "damage_bonus": 0.3,
                "defense_bonus": 0.2,
                "duration": 3,
                "description": "Boss gains temporary buffs"
            },
            BossAbility.DEBUFF: {
                "cooldown": 3,
                "player_damage_reduction": 0.25,
                "player_defense_reduction": 0.25,
                "duration": 2,
                "description": "Reduces player effectiveness"
            },
            BossAbility.AOE_ATTACK: {
                "cooldown": 2,
                "damage_multiplier": 1.5,
                "description": "Area of effect attack"
            },
            BossAbility.TELEPORT: {
                "cooldown": 3,
                "dodge_chance": 0.5,
                "description": "Boss teleports to avoid damage"
            },
            BossAbility.SHIELD: {
                "cooldown": 4,
                "damage_reduction": 0.75,
                "duration": 2,
                "description": "Boss gains temporary damage immunity"
            },
            BossAbility.ENRAGE: {
                "cooldown": 0,
                "damage_bonus": 1.0,
                "speed_bonus": 0.5,
                "description": "Final enrage - maximum power!"
            }
        }

    def create_district_boss(self, district_level: int, player_level: int, 
                           district_name: str) -> Dict[str, Any]:
        """Create a district boss for the specified district."""
        boss_config = self.boss_configs["district_boss"]
        
        # Determine boss archetype and classification
        archetype, classification = self.monster_system.determine_monster_type(
            district_level, player_level
        )
        
        # Calculate boss level
        boss_level = district_level + boss_config["level_bonus"]
        
        # Generate base monster stats
        base_stats = self.monster_system.generate_monster_stats(
            boss_level, archetype, classification, is_wild=False
        )
        
        # Apply boss multipliers
        boss_stats = self._apply_boss_multipliers(base_stats, boss_config)
        
        # Generate boss name
        boss_name = self._generate_boss_name(district_name, archetype, classification)
        
        # Create boss encounter
        boss_encounter = {
            "id": f"boss_{district_name.lower().replace(' ', '_')}_{int(time.time())}",
            "name": boss_name,
            "type": BossType.DISTRICT_BOSS,
            "district": district_name,
            "level": boss_level,
            "archetype": archetype,
            "classification": classification,
            "stats": boss_stats,
            "phases": self._create_boss_phases(boss_config["phases"]),
            "current_phase": BossPhase.PHASE_1,
            "abilities": self._select_boss_abilities(boss_config["abilities"]),
            "ability_cooldowns": {},
            "minions": [],
            "buffs": [],
            "debuffs": [],
            "loot_table": self._generate_boss_loot_table(boss_stats, boss_config),
            "experience_reward": self._calculate_boss_experience(boss_stats),
            "gold_reward": self._calculate_boss_gold(boss_stats),
            "spawn_time": time.time(),
            "is_active": True
        }
        
        return boss_encounter

    def create_unique_monster(self, district_level: int, player_level: int,
                            forced_archetype: MonsterArchetype = None,
                            forced_classification: MonsterClassification = None) -> Dict[str, Any]:
        """Create a unique monster encounter."""
        boss_config = self.boss_configs["unique_monster"]
        
        # Determine monster type
        if forced_archetype and forced_classification:
            archetype = forced_archetype
            classification = forced_classification
        else:
            archetype, classification = self.monster_system.determine_monster_type(
                district_level, player_level
            )
        
        # Calculate monster level with random bonus
        level_bonus = random.randint(1, 10)
        monster_level = district_level + boss_config["level_bonus"] + level_bonus
        
        # Generate base stats
        base_stats = self.monster_system.generate_monster_stats(
            monster_level, archetype, classification, is_wild=True
        )
        
        # Apply boss multipliers
        boss_stats = self._apply_boss_multipliers(base_stats, boss_config)
        
        # Generate unique name
        monster_name = self._generate_unique_monster_name(archetype, classification)
        
        # Create unique monster encounter
        unique_encounter = {
            "id": f"unique_{archetype.value}_{classification.value}_{int(time.time())}",
            "name": monster_name,
            "type": BossType.UNIQUE_MONSTER,
            "level": monster_level,
            "archetype": archetype,
            "classification": classification,
            "stats": boss_stats,
            "phases": self._create_boss_phases(boss_config["phases"]),
            "current_phase": BossPhase.PHASE_1,
            "abilities": self._select_boss_abilities(boss_config["abilities"]),
            "ability_cooldowns": {},
            "minions": [],
            "buffs": [],
            "debuffs": [],
            "loot_table": self._generate_boss_loot_table(boss_stats, boss_config),
            "experience_reward": self._calculate_boss_experience(boss_stats),
            "gold_reward": self._calculate_boss_gold(boss_stats),
            "spawn_time": time.time(),
            "is_active": True
        }
        
        return unique_encounter

    def create_world_boss(self, player_level: int, boss_name: str = None) -> Dict[str, Any]:
        """Create a world boss encounter."""
        boss_config = self.boss_configs["world_boss"]
        
        # World bosses are always high level
        boss_level = player_level + boss_config["level_bonus"]
        
        # Random archetype and classification
        archetype = random.choice(list(MonsterArchetype))
        classification = random.choice(list(MonsterClassification))
        
        # Generate base stats
        base_stats = self.monster_system.generate_monster_stats(
            boss_level, archetype, classification, is_wild=True
        )
        
        # Apply boss multipliers
        boss_stats = self._apply_boss_multipliers(base_stats, boss_config)
        
        # Generate or use provided name
        if not boss_name:
            boss_name = self._generate_world_boss_name(archetype, classification)
        
        # Create world boss encounter
        world_boss = {
            "id": f"world_boss_{archetype.value}_{int(time.time())}",
            "name": boss_name,
            "type": BossType.WORLD_BOSS,
            "level": boss_level,
            "archetype": archetype,
            "classification": classification,
            "stats": boss_stats,
            "phases": self._create_boss_phases(boss_config["phases"]),
            "current_phase": BossPhase.PHASE_1,
            "abilities": self._select_boss_abilities(boss_config["abilities"]),
            "ability_cooldowns": {},
            "minions": [],
            "buffs": [],
            "debuffs": [],
            "loot_table": self._generate_boss_loot_table(boss_stats, boss_config),
            "experience_reward": self._calculate_boss_experience(boss_stats),
            "gold_reward": self._calculate_boss_gold(boss_stats),
            "spawn_time": time.time(),
            "is_active": True
        }
        
        return world_boss

    def _apply_boss_multipliers(self, base_stats: Dict, boss_config: Dict) -> Dict:
        """Apply boss multipliers to base stats."""
        boss_stats = base_stats.copy()
        
        # Apply health multiplier
        boss_stats["max_health"] = int(base_stats["max_health"] * boss_config["health_multiplier"])
        boss_stats["current_health"] = boss_stats["max_health"]
        
        # Apply damage multiplier
        boss_stats["damage"] = int(base_stats["damage"] * boss_config["damage_multiplier"])
        
        # Apply defense multiplier
        boss_stats["defense"] = int(base_stats["defense"] * boss_config["defense_multiplier"])
        
        # Boss immunities
        boss_stats["status_immune"] = True
        boss_stats["stun_immune"] = True
        boss_stats["poison_immune"] = True
        boss_stats["burn_immune"] = True
        boss_stats["freeze_immune"] = True
        
        # Boss resistances (3x normal)
        for resistance in ["fire_resistance", "cold_resistance", "lightning_resistance", 
                         "poison_resistance", "stun_resistance"]:
            if resistance in base_stats:
                boss_stats[resistance] = base_stats[resistance] * 3
        
        return boss_stats

    def _create_boss_phases(self, num_phases: int) -> Dict[BossPhase, Dict]:
        """Create boss phases."""
        phases = {}
        
        if num_phases >= 1:
            phases[BossPhase.PHASE_1] = self.phase_configs[BossPhase.PHASE_1].copy()
        
        if num_phases >= 2:
            phases[BossPhase.PHASE_2] = self.phase_configs[BossPhase.PHASE_2].copy()
        
        if num_phases >= 3:
            phases[BossPhase.PHASE_3] = self.phase_configs[BossPhase.PHASE_3].copy()
        
        if num_phases >= 4:
            phases[BossPhase.ENRAGE] = self.phase_configs[BossPhase.ENRAGE].copy()
        
        return phases

    def _select_boss_abilities(self, ability_names: List[str]) -> List[BossAbility]:
        """Select boss abilities from available list."""
        abilities = []
        for ability_name in ability_names:
            try:
                ability = BossAbility(ability_name)
                abilities.append(ability)
            except ValueError:
                continue
        return abilities

    def _generate_boss_name(self, district_name: str, archetype: MonsterArchetype, 
                           classification: MonsterClassification) -> str:
        """Generate a boss name based on district and type."""
        archetype_names = {
            MonsterArchetype.MELEE: ["Brute", "Warlord", "Champion", "Titan"],
            MonsterArchetype.RANGED: ["Archer", "Sniper", "Hunter", "Marksman"],
            MonsterArchetype.MAGIC: ["Sorcerer", "Warlock", "Mage", "Wizard"],
            MonsterArchetype.WILD: ["Beast", "Monster", "Creature", "Abomination"]
        }
        
        classification_titles = {
            MonsterClassification.DEMONIC: "the Infernal",
            MonsterClassification.UNDEAD: "the Undying",
            MonsterClassification.BEAST: "the Savage",
            MonsterClassification.ELEMENTAL: "the Elemental",
            MonsterClassification.CONSTRUCT: "the Construct",
            MonsterClassification.HUMANOID: "the Tyrant"
        }
        
        archetype_name = random.choice(archetype_names[archetype])
        classification_title = classification_titles[classification]
        
        return f"{archetype_name} of {district_name} {classification_title}"

    def _generate_unique_monster_name(self, archetype: MonsterArchetype, 
                                    classification: MonsterClassification) -> str:
        """Generate a unique monster name."""
        unique_prefixes = ["Ancient", "Forgotten", "Cursed", "Legendary", "Mythical"]
        unique_suffixes = ["Horror", "Terror", "Nightmare", "Abomination", "Beast"]
        
        prefix = random.choice(unique_prefixes)
        suffix = random.choice(unique_suffixes)
        
        return f"The {prefix} {suffix}"

    def _generate_world_boss_name(self, archetype: MonsterArchetype, 
                                 classification: MonsterClassification) -> str:
        """Generate a world boss name."""
        world_titles = ["World Ender", "Apocalypse", "Doom Bringer", "Chaos Lord", "Void Master"]
        title = random.choice(world_titles)
        
        return f"{title} the {archetype.value.title()}"

    def _generate_boss_loot_table(self, boss_stats: Dict, boss_config: Dict) -> Dict:
        """Generate boss loot table."""
        loot_table = {
            "common_items": [],
            "rare_items": [],
            "epic_items": [],
            "legendary_items": [],
            "unique_items": []
        }
        
        # Add items based on boss level and quality
        boss_level = boss_stats.get("level", 1)
        loot_quality = boss_config["loot_quality"]
        
        # Guaranteed rare items for all bosses
        loot_table["rare_items"].extend([
            f"boss_weapon_{boss_level}",
            f"boss_armor_{boss_level}",
            f"boss_accessory_{boss_level}"
        ])
        
        # Add quality-specific items
        if loot_quality in ["epic", "legendary", "unique"]:
            loot_table["epic_items"].extend([
                f"epic_weapon_{boss_level}",
                f"epic_armor_{boss_level}"
            ])
        
        if loot_quality in ["legendary", "unique"]:
            loot_table["legendary_items"].extend([
                f"legendary_weapon_{boss_level}",
                f"legendary_armor_{boss_level}"
            ])
        
        if loot_quality == "unique":
            loot_table["unique_items"].extend([
                f"unique_weapon_{boss_level}",
                f"unique_armor_{boss_level}",
                f"unique_accessory_{boss_level}"
            ])
        
        return loot_table

    def _calculate_boss_experience(self, boss_stats: Dict) -> int:
        """Calculate boss experience reward."""
        base_xp = boss_stats.get("level", 1) * 50
        return int(base_xp * 3)  # 3x normal XP

    def _calculate_boss_gold(self, boss_stats: Dict) -> int:
        """Calculate boss gold reward."""
        base_gold = boss_stats.get("level", 1) * 25
        return int(base_gold * 5)  # 5x normal gold

    def start_boss_combat(self, player: Dict, boss: Dict) -> Dict[str, Any]:
        """Start a boss combat encounter."""
        # Initialize combat state
        combat_state = {
            "player": player.copy(),
            "boss": boss.copy(),
            "round": 1,
            "log": [],
            "phase_transitions": [],
            "abilities_used": [],
            "minions_spawned": [],
            "winner": None,
            "damage_dealt": 0,
            "damage_taken": 0
        }
        
        # Add to active bosses
        self.active_bosses[boss["id"]] = combat_state
        
        return combat_state

    def process_boss_combat_round(self, boss_id: str, player_action: str = "attack") -> Dict[str, Any]:
        """Process a single round of boss combat."""
        if boss_id not in self.active_bosses:
            return {"error": "Boss encounter not found"}
        
        combat_state = self.active_bosses[boss_id]
        player = combat_state["player"]
        boss = combat_state["boss"]
        
        # Check for phase transition
        self._check_phase_transition(combat_state)
        
        # Process player turn
        player_result = self._process_player_turn(combat_state, player_action)
        
        # Check if boss is defeated
        if boss["stats"]["current_health"] <= 0:
            combat_state["winner"] = "player"
            return self._end_boss_combat(combat_state)
        
        # Process boss turn
        boss_result = self._process_boss_turn(combat_state)
        
        # Check if player is defeated
        if player["current_health"] <= 0:
            combat_state["winner"] = "boss"
            return self._end_boss_combat(combat_state)
        
        # Update round
        combat_state["round"] += 1
        
        return {
            "combat_state": combat_state,
            "player_result": player_result,
            "boss_result": boss_result,
            "round": combat_state["round"]
        }

    def _check_phase_transition(self, combat_state: Dict):
        """Check if boss should transition to next phase."""
        boss = combat_state["boss"]
        current_phase = boss["current_phase"]
        phases = boss["phases"]
        
        # Get current health percentage
        health_percentage = boss["stats"]["current_health"] / boss["stats"]["max_health"]
        
        # Check phase thresholds
        if current_phase == BossPhase.PHASE_1 and health_percentage <= 0.7:
            if BossPhase.PHASE_2 in phases:
                self._transition_phase(combat_state, BossPhase.PHASE_2)
        elif current_phase == BossPhase.PHASE_2 and health_percentage <= 0.4:
            if BossPhase.PHASE_3 in phases:
                self._transition_phase(combat_state, BossPhase.PHASE_3)
        elif current_phase == BossPhase.PHASE_3 and health_percentage <= 0.2:
            if BossPhase.ENRAGE in phases:
                self._transition_phase(combat_state, BossPhase.ENRAGE)

    def _transition_phase(self, combat_state: Dict, new_phase: BossPhase):
        """Transition boss to new phase."""
        boss = combat_state["boss"]
        old_phase = boss["current_phase"]
        
        # Update phase
        boss["current_phase"] = new_phase
        
        # Apply phase bonuses
        phase_config = self.phase_configs[new_phase]
        boss["stats"]["damage"] = int(boss["stats"]["damage"] * (1 + phase_config["damage_bonus"]))
        
        # Log phase transition
        combat_state["phase_transitions"].append({
            "round": combat_state["round"],
            "old_phase": old_phase.value,
            "new_phase": new_phase.value,
            "description": phase_config["description"]
        })
        
        # Use phase transition ability
        if BossAbility.PHASE_TRANSITION in boss["abilities"]:
            self._use_boss_ability(combat_state, BossAbility.PHASE_TRANSITION)

    def _process_player_turn(self, combat_state: Dict, action: str) -> Dict[str, Any]:
        """Process player's turn in boss combat."""
        player = combat_state["player"]
        boss = combat_state["boss"]
        
        # Calculate player damage
        player_damage = self._calculate_player_damage(player, boss)
        
        # Apply damage to boss
        boss["stats"]["current_health"] = max(0, boss["stats"]["current_health"] - player_damage)
        
        # Update combat state
        combat_state["damage_dealt"] += player_damage
        
        return {
            "action": action,
            "damage_dealt": player_damage,
            "boss_health_remaining": boss["stats"]["current_health"]
        }

    def _process_boss_turn(self, combat_state: Dict) -> Dict[str, Any]:
        """Process boss's turn in combat."""
        player = combat_state["player"]
        boss = combat_state["boss"]
        
        # Check if boss should use ability
        if self._should_use_ability(combat_state):
            ability_result = self._use_random_ability(combat_state)
            return ability_result
        
        # Normal attack
        boss_damage = self._calculate_boss_damage(boss, player)
        
        # Apply damage to player
        player["current_health"] = max(0, player["current_health"] - boss_damage)
        
        # Update combat state
        combat_state["damage_taken"] += boss_damage
        
        return {
            "action": "attack",
            "damage_dealt": boss_damage,
            "player_health_remaining": player["current_health"]
        }

    def _should_use_ability(self, combat_state: Dict) -> bool:
        """Determine if boss should use an ability."""
        boss = combat_state["boss"]
        current_phase = boss["current_phase"]
        phase_config = self.phase_configs[current_phase]
        
        # Check ability frequency
        return random.random() < phase_config["ability_frequency"]

    def _use_random_ability(self, combat_state: Dict) -> Dict[str, Any]:
        """Use a random boss ability."""
        boss = combat_state["boss"]
        available_abilities = [ability for ability in boss["abilities"] 
                             if self._can_use_ability(combat_state, ability)]
        
        if not available_abilities:
            # Fall back to normal attack
            return self._process_boss_turn(combat_state)
        
        # Select random ability
        ability = random.choice(available_abilities)
        return self._use_boss_ability(combat_state, ability)

    def _can_use_ability(self, combat_state: Dict, ability: BossAbility) -> bool:
        """Check if boss can use the specified ability."""
        boss = combat_state["boss"]
        cooldowns = boss["ability_cooldowns"]
        
        # Check cooldown
        if ability.value in cooldowns:
            last_used = cooldowns[ability.value]
            ability_config = self.ability_configs[ability]
            cooldown_rounds = ability_config["cooldown"]
            
            if combat_state["round"] - last_used < cooldown_rounds:
                return False
        
        return True

    def _use_boss_ability(self, combat_state: Dict, ability: BossAbility) -> Dict[str, Any]:
        """Use a specific boss ability."""
        boss = combat_state["boss"]
        player = combat_state["player"]
        ability_config = self.ability_configs[ability]
        
        # Update cooldown
        boss["ability_cooldowns"][ability.value] = combat_state["round"]
        
        # Log ability use
        combat_state["abilities_used"].append({
            "round": combat_state["round"],
            "ability": ability.value,
            "description": ability_config["description"]
        })
        
        # Execute ability effects
        if ability == BossAbility.SUMMON_MINIONS:
            return self._execute_summon_minions(combat_state, ability_config)
        elif ability == BossAbility.HEAL:
            return self._execute_heal(combat_state, ability_config)
        elif ability == BossAbility.AOE_ATTACK:
            return self._execute_aoe_attack(combat_state, ability_config)
        elif ability == BossAbility.TELEPORT:
            return self._execute_teleport(combat_state, ability_config)
        elif ability == BossAbility.SHIELD:
            return self._execute_shield(combat_state, ability_config)
        elif ability == BossAbility.ENRAGE:
            return self._execute_enrage(combat_state, ability_config)
        else:
            # Default to normal attack
            return self._process_boss_turn(combat_state)

    def _execute_summon_minions(self, combat_state: Dict, ability_config: Dict) -> Dict[str, Any]:
        """Execute summon minions ability."""
        boss = combat_state["boss"]
        minion_count = ability_config["minions_count"]
        minion_level = int(boss["stats"]["level"] * ability_config["minion_level"])
        
        # Create minions
        minions = []
        for i in range(minion_count):
            minion = {
                "id": f"minion_{boss['id']}_{i}",
                "name": f"Minion {i+1}",
                "level": minion_level,
                "stats": {
                    "max_health": 20 + (minion_level * 5),
                    "current_health": 20 + (minion_level * 5),
                    "damage": 5 + (minion_level * 2),
                    "defense": 2 + minion_level
                }
            }
            minions.append(minion)
        
        # Add minions to boss
        boss["minions"].extend(minions)
        combat_state["minions_spawned"].extend(minions)
        
        return {
            "action": "summon_minions",
            "minions_spawned": minion_count,
            "description": f"Boss summons {minion_count} minions!"
        }

    def _execute_heal(self, combat_state: Dict, ability_config: Dict) -> Dict[str, Any]:
        """Execute heal ability."""
        boss = combat_state["boss"]
        heal_percentage = ability_config["heal_percentage"]
        heal_amount = int(boss["stats"]["max_health"] * heal_percentage)
        
        # Heal boss
        boss["stats"]["current_health"] = min(
            boss["stats"]["max_health"],
            boss["stats"]["current_health"] + heal_amount
        )
        
        return {
            "action": "heal",
            "heal_amount": heal_amount,
            "description": f"Boss heals for {heal_amount} health!"
        }

    def _execute_aoe_attack(self, combat_state: Dict, ability_config: Dict) -> Dict[str, Any]:
        """Execute area of effect attack."""
        player = combat_state["player"]
        boss = combat_state["boss"]
        
        # Calculate AOE damage
        base_damage = boss["stats"]["damage"]
        aoe_multiplier = ability_config["damage_multiplier"]
        aoe_damage = int(base_damage * aoe_multiplier)
        
        # Apply damage to player
        player["current_health"] = max(0, player["current_health"] - aoe_damage)
        
        # Update combat state
        combat_state["damage_taken"] += aoe_damage
        
        return {
            "action": "aoe_attack",
            "damage_dealt": aoe_damage,
            "description": f"Boss unleashes a devastating area attack!"
        }

    def _execute_teleport(self, combat_state: Dict, ability_config: Dict) -> Dict[str, Any]:
        """Execute teleport ability."""
        dodge_chance = ability_config["dodge_chance"]
        
        # Check if teleport dodges damage
        if random.random() < dodge_chance:
            return {
                "action": "teleport",
                "dodged": True,
                "description": "Boss teleports away, avoiding damage!"
            }
        else:
            return {
                "action": "teleport",
                "dodged": False,
                "description": "Boss teleports but still takes damage!"
            }

    def _execute_shield(self, combat_state: Dict, ability_config: Dict) -> Dict[str, Any]:
        """Execute shield ability."""
        boss = combat_state["boss"]
        duration = ability_config["duration"]
        damage_reduction = ability_config["damage_reduction"]
        
        # Add shield buff
        shield_buff = {
            "type": "shield",
            "damage_reduction": damage_reduction,
            "duration": duration,
            "rounds_remaining": duration
        }
        
        boss["buffs"].append(shield_buff)
        
        return {
            "action": "shield",
            "damage_reduction": damage_reduction,
            "duration": duration,
            "description": f"Boss gains a protective shield!"
        }

    def _execute_enrage(self, combat_state: Dict, ability_config: Dict) -> Dict[str, Any]:
        """Execute enrage ability."""
        boss = combat_state["boss"]
        damage_bonus = ability_config["damage_bonus"]
        speed_bonus = ability_config["speed_bonus"]
        
        # Apply enrage buffs
        boss["stats"]["damage"] = int(boss["stats"]["damage"] * (1 + damage_bonus))
        
        enrage_buff = {
            "type": "enrage",
            "damage_bonus": damage_bonus,
            "speed_bonus": speed_bonus,
            "duration": 999,  # Permanent until combat ends
            "rounds_remaining": 999
        }
        
        boss["buffs"].append(enrage_buff)
        
        return {
            "action": "enrage",
            "damage_bonus": damage_bonus,
            "description": "Boss enters a state of pure rage!"
        }

    def _calculate_player_damage(self, player: Dict, boss: Dict) -> int:
        """Calculate player damage against boss."""
        base_damage = player.get("damage", 10)
        
        # Apply boss defense
        boss_defense = boss["stats"].get("defense", 0)
        final_damage = max(1, base_damage - boss_defense)
        
        return final_damage

    def _calculate_boss_damage(self, boss: Dict, player: Dict) -> int:
        """Calculate boss damage against player."""
        base_damage = boss["stats"].get("damage", 10)
        
        # Apply player defense
        player_defense = player.get("defense", 0)
        final_damage = max(1, base_damage - player_defense)
        
        return final_damage

    def _end_boss_combat(self, combat_state: Dict) -> Dict[str, Any]:
        """End boss combat and return results."""
        boss_id = combat_state["boss"]["id"]
        
        # Remove from active bosses
        if boss_id in self.active_bosses:
            del self.active_bosses[boss_id]
        
        # Calculate rewards
        rewards = {
            "experience": combat_state["boss"]["experience_reward"],
            "gold": combat_state["boss"]["gold_reward"],
            "loot": combat_state["boss"]["loot_table"]
        }
        
        return {
            "winner": combat_state["winner"],
            "rounds": combat_state["round"],
            "damage_dealt": combat_state["damage_dealt"],
            "damage_taken": combat_state["damage_taken"],
            "rewards": rewards,
            "combat_log": combat_state["log"]
        }

    def get_active_bosses(self) -> List[Dict]:
        """Get all active boss encounters."""
        return list(self.active_bosses.values())

    def get_boss_by_id(self, boss_id: str) -> Optional[Dict]:
        """Get a specific boss encounter by ID."""
        return self.active_bosses.get(boss_id)

    def cleanup_expired_bosses(self):
        """Clean up expired boss encounters."""
        current_time = time.time()
        expired_bosses = []
        
        for boss_id, combat_state in self.active_bosses.items():
            boss = combat_state["boss"]
            spawn_time = boss["spawn_time"]
            
            # Boss expires after 1 hour
            if current_time - spawn_time > 3600:
                expired_bosses.append(boss_id)
        
        for boss_id in expired_bosses:
            del self.active_bosses[boss_id]


def test_boss_system():
    """Test the boss system."""
    from .monster_system import MonsterSystem
    from .player_system import PlayerSystem
    from .combat_system import CombatSystem
    
    # Initialize systems
    monster_system = MonsterSystem()
    player_system = PlayerSystem()
    combat_system = CombatSystem(player_system, monster_system, None)
    boss_system = BossSystem(monster_system, player_system, combat_system)
    
    # Create test player
    player = player_system.create_player("TestPlayer", "Warrior")
    
    # Create district boss
    district_boss = boss_system.create_district_boss(10, 15, "Dark District")
    print(f"Created district boss: {district_boss['name']}")
    print(f"Level: {district_boss['level']}")
    print(f"Health: {district_boss['stats']['max_health']}")
    print(f"Damage: {district_boss['stats']['damage']}")
    
    # Create unique monster
    unique_monster = boss_system.create_unique_monster(10, 15)
    print(f"\nCreated unique monster: {unique_monster['name']}")
    print(f"Level: {unique_monster['level']}")
    print(f"Health: {unique_monster['stats']['max_health']}")
    print(f"Damage: {unique_monster['stats']['damage']}")
    
    # Create world boss
    world_boss = boss_system.create_world_boss(20)
    print(f"\nCreated world boss: {world_boss['name']}")
    print(f"Level: {world_boss['level']}")
    print(f"Health: {world_boss['stats']['max_health']}")
    print(f"Damage: {world_boss['stats']['damage']}")


if __name__ == "__main__":
    test_boss_system()

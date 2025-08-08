"""
Skills System for Chronicles of Ruin
Guild Wars-style skill system where every archetype has access to all skill types
"""

import json
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path

class SkillType(Enum):
    """Skill categories available to all archetypes"""
    DAMAGE = "damage"      # Raw damage output
    DEFENSE = "defense"     # Damage mitigation and protection
    SUPPORT = "support"     # Healing and utility abilities
    ULTIMATE = "ultimate"   # Ultimate abilities (pure specializations only)

class SkillTarget(Enum):
    """Target types for skills"""
    SELF = "self"
    SINGLE_ALLY = "single_ally"
    ALL_ALLIES = "all_allies"
    SINGLE_ENEMY = "single_enemy"
    ALL_ENEMIES = "all_enemies"
    AREA = "area"

@dataclass
class Skill:
    """Individual skill definition"""
    id: str
    name: str
    description: str
    skill_type: SkillType
    target_type: SkillTarget
    base_power: int
    cooldown: int
    mana_cost: int
    range: int
    area_radius: int = 0
    duration: int = 0
    scaling_factor: float = 1.0
    special_effects: List[str] = None
    
    def __post_init__(self):
        if self.special_effects is None:
            self.special_effects = []

class SkillsSystem:
    """Guild Wars-style skills system where every archetype has access to all skill types"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.skills_file = self.data_dir / "skills.json"
        self.skills: Dict[str, Skill] = {}
        self.skill_sets: Dict[str, Dict[str, List[str]]] = {}
        
        # Skill distribution by archetype
        self.archetype_skill_distribution = {
            "pure_dps": {
                "damage": 0.8,
                "defense": 0.1,
                "support": 0.1,
                "ultimate_unlock": True
            },
            "hybrid_dps": {
                "damage": 0.6,
                "defense": 0.2,
                "support": 0.2,
                "ultimate_unlock": False
            },
            "support": {
                "damage": 0.3,
                "defense": 0.3,
                "support": 0.4,
                "ultimate_unlock": False
            },
            "hybrid_support": {
                "damage": 0.2,
                "defense": 0.3,
                "support": 0.5,
                "ultimate_unlock": False
            },
            "pure_support": {
                "damage": 0.1,
                "defense": 0.3,
                "support": 0.6,
                "ultimate_unlock": True
            }
        }
        
        self._load_skills()
        self._create_skill_sets()
    
    def _load_skills(self):
        """Load all skills from the skills database"""
        if self.skills_file.exists():
            try:
                with open(self.skills_file, 'r') as f:
                    skills_data = json.load(f)
                    for skill_data in skills_data:
                        skill = Skill(
                            id=skill_data['id'],
                            name=skill_data['name'],
                            description=skill_data['description'],
                            skill_type=SkillType(skill_data['skill_type']),
                            target_type=SkillTarget(skill_data['target_type']),
                            base_power=skill_data['base_power'],
                            cooldown=skill_data['cooldown'],
                            mana_cost=skill_data['mana_cost'],
                            range=skill_data['range'],
                            area_radius=skill_data.get('area_radius', 0),
                            duration=skill_data.get('duration', 0),
                            scaling_factor=skill_data.get('scaling_factor', 1.0),
                            special_effects=skill_data.get('special_effects', [])
                        )
                        self.skills[skill.id] = skill
            except Exception as e:
                print(f"Error loading skills: {e}")
                self._create_default_skills()
        else:
            self._create_default_skills()
    
    def _create_default_skills(self):
        """Create the default skill set with 9 regular skills (3 of each type) + 1 ultimate"""
        
        # DAMAGE SKILLS (3 skills)
        damage_skills = [
            Skill(
                id="fireball",
                name="Fireball",
                description="Launch a powerful fireball at your target",
                skill_type=SkillType.DAMAGE,
                target_type=SkillTarget.SINGLE_ENEMY,
                base_power=120,
                cooldown=3,
                mana_cost=25,
                range=6,
                scaling_factor=1.2,
                special_effects=["burning"]
            ),
            Skill(
                id="lightning_strike",
                name="Lightning Strike",
                description="Call down lightning from the sky",
                skill_type=SkillType.DAMAGE,
                target_type=SkillTarget.AREA,
                base_power=100,
                cooldown=4,
                mana_cost=30,
                range=8,
                area_radius=3,
                scaling_factor=1.1,
                special_effects=["shocked"]
            ),
            Skill(
                id="shadow_daggers",
                name="Shadow Daggers",
                description="Throw ethereal daggers that pierce armor",
                skill_type=SkillType.DAMAGE,
                target_type=SkillTarget.SINGLE_ENEMY,
                base_power=90,
                cooldown=2,
                mana_cost=20,
                range=5,
                scaling_factor=1.0,
                special_effects=["armor_pierce"]
            )
        ]
        
        # DEFENSE SKILLS (3 skills)
        defense_skills = [
            Skill(
                id="stone_skin",
                name="Stone Skin",
                description="Temporarily harden your skin like stone",
                skill_type=SkillType.DEFENSE,
                target_type=SkillTarget.SELF,
                base_power=0,
                cooldown=6,
                mana_cost=35,
                range=0,
                duration=4,
                scaling_factor=0.8,
                special_effects=["damage_reduction", "stun_resistance"]
            ),
            Skill(
                id="mirror_shield",
                name="Mirror Shield",
                description="Create a magical shield that reflects damage",
                skill_type=SkillType.DEFENSE,
                target_type=SkillTarget.SELF,
                base_power=0,
                cooldown=8,
                mana_cost=40,
                range=0,
                duration=3,
                scaling_factor=1.0,
                special_effects=["damage_reflection", "magic_resistance"]
            ),
            Skill(
                id="evasion",
                name="Evasion",
                description="Enhance your agility to dodge attacks",
                skill_type=SkillType.DEFENSE,
                target_type=SkillTarget.SELF,
                base_power=0,
                cooldown=5,
                mana_cost=25,
                range=0,
                duration=3,
                scaling_factor=0.9,
                special_effects=["dodge_chance", "movement_speed"]
            )
        ]
        
        # SUPPORT SKILLS (3 skills)
        support_skills = [
            Skill(
                id="healing_light",
                name="Healing Light",
                description="Channel healing energy to restore health",
                skill_type=SkillType.SUPPORT,
                target_type=SkillTarget.SINGLE_ALLY,
                base_power=150,
                cooldown=4,
                mana_cost=30,
                range=6,
                scaling_factor=1.3,
                special_effects=["healing", "regeneration"]
            ),
            Skill(
                id="group_heal",
                name="Group Heal",
                description="Heal all allies in an area",
                skill_type=SkillType.SUPPORT,
                target_type=SkillTarget.AREA,
                base_power=80,
                cooldown=6,
                mana_cost=45,
                range=5,
                area_radius=4,
                scaling_factor=1.1,
                special_effects=["healing", "area_heal"]
            ),
            Skill(
                id="haste",
                name="Haste",
                description="Increase movement and attack speed",
                skill_type=SkillType.SUPPORT,
                target_type=SkillTarget.SINGLE_ALLY,
                base_power=0,
                cooldown=5,
                mana_cost=25,
                range=4,
                duration=4,
                scaling_factor=0.8,
                special_effects=["speed_boost", "attack_speed"]
            )
        ]
        
        # ULTIMATE SKILLS (1 skill per pure specialization)
        ultimate_skills = [
            Skill(
                id="apocalypse",
                name="Apocalypse",
                description="Unleash devastating damage to all enemies",
                skill_type=SkillType.ULTIMATE,
                target_type=SkillTarget.ALL_ENEMIES,
                base_power=300,
                cooldown=12,
                mana_cost=100,
                range=10,
                scaling_factor=2.0,
                special_effects=["massive_damage", "fear"]
            ),
            Skill(
                id="immortality",
                name="Immortality",
                description="Become temporarily invulnerable and heal all allies",
                skill_type=SkillType.ULTIMATE,
                target_type=SkillTarget.ALL_ALLIES,
                base_power=200,
                cooldown=15,
                mana_cost=120,
                range=8,
                duration=5,
                scaling_factor=1.8,
                special_effects=["invulnerability", "mass_healing"]
            )
        ]
        
        # Add all skills to the system
        for skill in damage_skills + defense_skills + support_skills + ultimate_skills:
            self.skills[skill.id] = skill
    
    def _create_skill_sets(self):
        """Create skill sets for each archetype based on their specialization"""
        
        # Get all skills by type
        damage_skills = [s for s in self.skills.values() if s.skill_type == SkillType.DAMAGE]
        defense_skills = [s for s in self.skills.values() if s.skill_type == SkillType.DEFENSE]
        support_skills = [s for s in self.skills.values() if s.skill_type == SkillType.SUPPORT]
        ultimate_skills = [s for s in self.skills.values() if s.skill_type == SkillType.ULTIMATE]
        
        # Create skill sets for each archetype
        for archetype, distribution in self.archetype_skill_distribution.items():
            skill_set = {
                "damage": [],
                "defense": [],
                "support": [],
                "ultimate": []
            }
            
            # Assign 3 damage skills (all archetypes get access to all damage skills)
            skill_set["damage"] = [s.id for s in damage_skills]
            
            # Assign 3 defense skills (all archetypes get access to all defense skills)
            skill_set["defense"] = [s.id for s in defense_skills]
            
            # Assign 3 support skills (all archetypes get access to all support skills)
            skill_set["support"] = [s.id for s in support_skills]
            
            # Assign ultimate skills (only pure specializations get ultimates)
            if distribution["ultimate_unlock"]:
                if archetype == "pure_dps":
                    skill_set["ultimate"] = [s.id for s in ultimate_skills if "massive_damage" in s.special_effects]
                elif archetype == "pure_support":
                    skill_set["ultimate"] = [s.id for s in ultimate_skills if "mass_healing" in s.special_effects]
            
            self.skill_sets[archetype] = skill_set
    
    def get_skill_set_for_archetype(self, archetype: str) -> Dict[str, List[str]]:
        """Get the skill set for a specific archetype"""
        return self.skill_sets.get(archetype, {})
    
    def get_skill_by_id(self, skill_id: str) -> Optional[Skill]:
        """Get a skill by its ID"""
        return self.skills.get(skill_id)
    
    def get_skills_by_type(self, skill_type: SkillType) -> List[Skill]:
        """Get all skills of a specific type"""
        return [s for s in self.skills.values() if s.skill_type == skill_type]
    
    def get_available_skills_for_player(self, archetype: str, player_level: int) -> List[Skill]:
        """Get available skills for a player based on their archetype and level"""
        skill_set = self.get_skill_set_for_archetype(archetype)
        available_skills = []
        
        # Add regular skills (all available from level 1)
        for skill_type in ["damage", "defense", "support"]:
            for skill_id in skill_set.get(skill_type, []):
                skill = self.get_skill_by_id(skill_id)
                if skill:
                    available_skills.append(skill)
        
        # Add ultimate skills (available at level 10 for pure specializations)
        if player_level >= 10:
            for skill_id in skill_set.get("ultimate", []):
                skill = self.get_skill_by_id(skill_id)
                if skill:
                    available_skills.append(skill)
        
        return available_skills
    
    def calculate_skill_effectiveness(self, skill: Skill, archetype: str, player_level: int) -> Dict[str, Any]:
        """Calculate skill effectiveness based on archetype specialization"""
        distribution = self.archetype_skill_distribution.get(archetype, {})
        
        # Base effectiveness
        effectiveness = {
            "damage": 1.0,
            "healing": 1.0,
            "defense": 1.0,
            "cooldown_reduction": 0.0,
            "mana_cost_reduction": 0.0
        }
        
        # Apply archetype bonuses
        if skill.skill_type == SkillType.DAMAGE:
            effectiveness["damage"] *= (1.0 + distribution.get("damage", 0.0))
        elif skill.skill_type == SkillType.DEFENSE:
            effectiveness["defense"] *= (1.0 + distribution.get("defense", 0.0))
        elif skill.skill_type == SkillType.SUPPORT:
            effectiveness["healing"] *= (1.0 + distribution.get("support", 0.0))
        
        # Level-based improvements
        level_bonus = (player_level - 1) * 0.05  # 5% improvement per level
        effectiveness["damage"] += level_bonus
        effectiveness["healing"] += level_bonus
        effectiveness["defense"] += level_bonus
        
        # Pure specialization bonuses
        if archetype in ["pure_dps", "pure_support"]:
            effectiveness["cooldown_reduction"] = 0.2  # 20% cooldown reduction
            effectiveness["mana_cost_reduction"] = 0.15  # 15% mana cost reduction
        
        return effectiveness
    
    def get_skill_description_for_archetype(self, skill: Skill, archetype: str, player_level: int) -> str:
        """Get a detailed description of how a skill works for a specific archetype"""
        effectiveness = self.calculate_skill_effectiveness(skill, archetype, player_level)
        
        description = f"{skill.name}\n"
        description += f"Type: {skill.skill_type.value.title()}\n"
        description += f"Target: {skill.target_type.value.replace('_', ' ').title()}\n"
        description += f"Base Power: {skill.base_power}\n"
        description += f"Cooldown: {skill.cooldown} turns\n"
        description += f"Mana Cost: {skill.mana_cost}\n"
        description += f"Range: {skill.range}\n"
        
        if skill.area_radius > 0:
            description += f"Area Radius: {skill.area_radius}\n"
        
        if skill.duration > 0:
            description += f"Duration: {skill.duration} turns\n"
        
        # Archetype-specific effectiveness
        if skill.skill_type == SkillType.DAMAGE:
            damage_multiplier = effectiveness["damage"]
            description += f"Damage Multiplier: {damage_multiplier:.2f}x\n"
        elif skill.skill_type == SkillType.SUPPORT:
            healing_multiplier = effectiveness["healing"]
            description += f"Healing Multiplier: {healing_multiplier:.2f}x\n"
        elif skill.skill_type == SkillType.DEFENSE:
            defense_multiplier = effectiveness["defense"]
            description += f"Defense Multiplier: {defense_multiplier:.2f}x\n"
        
        if effectiveness["cooldown_reduction"] > 0:
            description += f"Cooldown Reduction: {effectiveness['cooldown_reduction']:.1%}\n"
        
        if effectiveness["mana_cost_reduction"] > 0:
            description += f"Mana Cost Reduction: {effectiveness['mana_cost_reduction']:.1%}\n"
        
        if skill.special_effects:
            description += f"Special Effects: {', '.join(skill.special_effects)}\n"
        
        description += f"\n{skill.description}"
        
        return description
    
    def save_skills(self):
        """Save skills to the database"""
        try:
            skills_data = [asdict(skill) for skill in self.skills.values()]
            with open(self.skills_file, 'w') as f:
                json.dump(skills_data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving skills: {e}")
    
    def get_skill_recommendations(self, archetype: str, player_level: int) -> Dict[str, List[str]]:
        """Get skill recommendations based on archetype and level"""
        recommendations = {
            "primary": [],
            "secondary": [],
            "utility": []
        }
        
        skill_set = self.get_skill_set_for_archetype(archetype)
        distribution = self.archetype_skill_distribution.get(archetype, {})
        
        # Primary skills (highest effectiveness for archetype)
        if distribution.get("damage", 0) > 0.5:
            recommendations["primary"] = skill_set.get("damage", [])
        elif distribution.get("support", 0) > 0.5:
            recommendations["primary"] = skill_set.get("support", [])
        else:
            recommendations["primary"] = skill_set.get("defense", [])
        
        # Secondary skills (moderate effectiveness)
        if distribution.get("damage", 0) <= 0.5:
            recommendations["secondary"] = skill_set.get("damage", [])
        elif distribution.get("support", 0) <= 0.5:
            recommendations["secondary"] = skill_set.get("support", [])
        else:
            recommendations["secondary"] = skill_set.get("defense", [])
        
        # Utility skills (lowest effectiveness but still useful)
        remaining_skills = []
        for skill_type in ["damage", "defense", "support"]:
            if skill_type not in [s.skill_type.value for s in self.get_skills_by_type(SkillType.DAMAGE)]:
                remaining_skills.extend(skill_set.get(skill_type, []))
        recommendations["utility"] = remaining_skills
        
        return recommendations

def main():
    """Test the skills system"""
    skills_system = SkillsSystem(Path("data"))
    
    print("🎯 GUILD WARS-STYLE SKILLS SYSTEM")
    print("=" * 50)
    
    # Test skill sets for each archetype
    archetypes = ["pure_dps", "hybrid_dps", "support", "hybrid_support", "pure_support"]
    
    for archetype in archetypes:
        print(f"\n📚 {archetype.upper().replace('_', ' ')} SKILL SET:")
        skill_set = skills_system.get_skill_set_for_archetype(archetype)
        
        for skill_type, skill_ids in skill_set.items():
            print(f"  {skill_type.title()}: {len(skill_ids)} skills")
            for skill_id in skill_ids:
                skill = skills_system.get_skill_by_id(skill_id)
                if skill:
                    print(f"    - {skill.name}")
    
    # Test skill effectiveness
    print(f"\n⚡ SKILL EFFECTIVENESS EXAMPLE:")
    fireball = skills_system.get_skill_by_id("fireball")
    if fireball:
        for archetype in ["pure_dps", "support", "pure_support"]:
            effectiveness = skills_system.calculate_skill_effectiveness(fireball, archetype, 10)
            print(f"  {archetype}: Damage multiplier = {effectiveness['damage']:.2f}x")
    
    # Test skill recommendations
    print(f"\n💡 SKILL RECOMMENDATIONS:")
    for archetype in ["pure_dps", "pure_support"]:
        recommendations = skills_system.get_skill_recommendations(archetype, 10)
        print(f"  {archetype}:")
        print(f"    Primary: {len(recommendations['primary'])} skills")
        print(f"    Secondary: {len(recommendations['secondary'])} skills")
        print(f"    Utility: {len(recommendations['utility'])} skills")

if __name__ == "__main__":
    main()

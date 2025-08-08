# Skills System - Chronicles of Ruin: Sunderfall

## **OVERVIEW** ⚡

The Skills System is the primary tool for character customization in Chronicles of Ruin: Sunderfall, providing a deep and flexible skill tree that allows players to create unique builds and playstyles. The system balances accessibility with strategic depth, ensuring every skill point investment feels meaningful.

---

## **SKILL CATEGORIES** 🎯

### **Archetype-Based Skills**
Skills are organized by archetype, each with distinct characteristics:

| Archetype | Skill Focus | Primary Attribute | Secondary Attribute |
|-----------|-------------|------------------|-------------------|
| **Melee** | Physical Damage | Power | Toughness |
| **Ranged** | Precision & Speed | Agility | Finesse |
| **Magic** | Status Effects | Knowledge | Wisdom |
| **Wild** | Chaos & Utility | Chaos | Chaos |

### **Skill Types**
- **Active Skills**: Require activation, have cooldowns
- **Passive Skills**: Always active, provide constant bonuses
- **Ultimate Skills**: Powerful abilities with long cooldowns
- **Synergy Skills**: Skills that enhance other skills

---

## **MELEE SKILLS** ⚔️

### **Core Melee Skills**

#### **Heavy Strike**
- **Type**: Active, Single Target
- **Base Damage**: 15-20 physical damage
- **Cooldown**: 3 turns
- **Scaling**: +2 damage per skill level
- **Special**: 25% chance to stun for 1 turn

**Mathematical Formula:**
```
Damage = (15-20) + (Skill Level × 2) + Power Bonus
Stun Chance = 25% + (Skill Level × 2%)
```

#### **Whirlwind**
- **Type**: Active, Area of Effect
- **Base Damage**: 8-12 physical damage to all enemies
- **Cooldown**: 5 turns
- **Scaling**: +1 damage per skill level
- **Special**: +10% damage per enemy hit

**Mathematical Formula:**
```
Damage = (8-12) + Skill Level + Power Bonus
Bonus Damage = 10% × Number of Enemies Hit
```

#### **Defensive Stance**
- **Type**: Passive
- **Effect**: +5% damage reduction per skill level
- **Maximum**: 50% damage reduction
- **Requirement**: 3 points in Melee archetype

**Mathematical Formula:**
```
Damage Reduction = min(Skill Level × 5%, 50%)
```

### **Advanced Melee Skills**

#### **Berserker Rage**
- **Type**: Active, Self-Buff
- **Effect**: +50% damage, -25% defense for 3 turns
- **Cooldown**: 8 turns
- **Scaling**: +5% damage per skill level
- **Special**: Duration increases with skill level

**Mathematical Formula:**
```
Damage Bonus = 50% + (Skill Level × 5%)
Duration = 3 + (Skill Level // 2) turns
```

#### **Counter Attack**
- **Type**: Passive, Reactive
- **Effect**: 15% chance to counter-attack when hit
- **Scaling**: +2% chance per skill level
- **Damage**: 75% of normal attack damage
- **Special**: Ignores enemy defense

**Mathematical Formula:**
```
Counter Chance = 15% + (Skill Level × 2%)
Counter Damage = Normal Damage × 0.75
```

---

## **RANGED SKILLS** 🏹

### **Core Ranged Skills**

#### **Precise Shot**
- **Type**: Active, Single Target
- **Base Damage**: 12-18 physical damage
- **Cooldown**: 2 turns
- **Scaling**: +3 damage per skill level
- **Special**: +25% critical hit chance

**Mathematical Formula:**
```
Damage = (12-18) + (Skill Level × 3) + Agility Bonus
Critical Chance = 25% + (Skill Level × 3%)
```

#### **Multi-Shot**
- **Type**: Active, Multi-Target
- **Base Damage**: 6-10 physical damage to 3 targets
- **Cooldown**: 4 turns
- **Scaling**: +1 damage per skill level
- **Special**: +1 target per 3 skill levels

**Mathematical Formula:**
```
Damage = (6-10) + Skill Level + Agility Bonus
Targets = 3 + (Skill Level // 3)
```

#### **Evasive Maneuvers**
- **Type**: Passive
- **Effect**: +3% dodge chance per skill level
- **Maximum**: 40% dodge chance
- **Requirement**: 3 points in Ranged archetype

**Mathematical Formula:**
```
Dodge Chance = min(Skill Level × 3%, 40%)
```

### **Advanced Ranged Skills**

#### **Sniper's Focus**
- **Type**: Active, Self-Buff
- **Effect**: +100% critical damage for 2 turns
- **Cooldown**: 6 turns
- **Scaling**: +10% critical damage per skill level
- **Special**: Duration increases with skill level

**Mathematical Formula:**
```
Critical Bonus = 100% + (Skill Level × 10%)
Duration = 2 + (Skill Level // 3) turns
```

#### **Trap Mastery**
- **Type**: Passive, Utility
- **Effect**: 20% chance to place a trap when attacked
- **Scaling**: +3% chance per skill level
- **Trap Damage**: 50% of normal attack damage
- **Special**: Traps last 2 turns

**Mathematical Formula:**
```
Trap Chance = 20% + (Skill Level × 3%)
Trap Damage = Normal Damage × 0.5
```

---

## **MAGIC SKILLS** 🔮

### **Core Magic Skills**

#### **Fireball**
- **Type**: Active, Single Target
- **Base Damage**: 10-15 physical damage
- **Status Effect**: 30% chance to burn for 2 turns
- **Cooldown**: 3 turns
- **Scaling**: +2 damage per skill level
- **Burn Scaling**: +5% burn chance per skill level

**Mathematical Formula:**
```
Damage = (10-15) + (Skill Level × 2) + Knowledge Bonus
Burn Chance = 30% + (Skill Level × 5%)
Burn Damage = 50% of initial damage over 2 turns
```

#### **Frost Nova**
- **Type**: Active, Area of Effect
- **Base Damage**: 5-8 physical damage to all enemies
- **Status Effect**: 25% chance to freeze for 1 turn
- **Cooldown**: 4 turns
- **Scaling**: +1 damage per skill level
- **Freeze Scaling**: +3% freeze chance per skill level

**Mathematical Formula:**
```
Damage = (5-8) + Skill Level + Knowledge Bonus
Freeze Chance = 25% + (Skill Level × 3%)
```

#### **Arcane Shield**
- **Type**: Passive
- **Effect**: +4% magic resistance per skill level
- **Maximum**: 60% magic resistance
- **Requirement**: 3 points in Magic archetype

**Mathematical Formula:**
```
Magic Resistance = min(Skill Level × 4%, 60%)
```

### **Advanced Magic Skills**

#### **Chain Lightning**
- **Type**: Active, Chain Effect
- **Base Damage**: 8-12 physical damage, chains to 3 enemies
- **Status Effect**: 20% chance to stun for 1 turn
- **Cooldown**: 5 turns
- **Scaling**: +1 damage per skill level
- **Chain Scaling**: +1 chain per 2 skill levels

**Mathematical Formula:**
```
Damage = (8-12) + Skill Level + Knowledge Bonus
Chains = 3 + (Skill Level // 2)
Stun Chance = 20% + (Skill Level × 2%)
```

#### **Mana Surge**
- **Type**: Active, Self-Buff
- **Effect**: +50% status effect chance for 3 turns
- **Cooldown**: 7 turns
- **Scaling**: +5% chance per skill level
- **Special**: Duration increases with skill level

**Mathematical Formula:**
```
Status Bonus = 50% + (Skill Level × 5%)
Duration = 3 + (Skill Level // 2) turns
```

---

## **WILD SKILLS** 🌪️

### **Core Wild Skills**

#### **Chaos Bolt**
- **Type**: Active, Single Target
- **Base Damage**: 8-15 physical damage
- **Random Effect**: Random status effect (burn, freeze, stun, poison)
- **Cooldown**: 3 turns
- **Scaling**: +2 damage per skill level
- **Effect Scaling**: +5% effect chance per skill level

**Mathematical Formula:**
```
Damage = (8-15) + (Skill Level × 2) + Chaos Bonus
Effect Chance = 25% + (Skill Level × 5%)
Random Effect = Random(burn, freeze, stun, poison)
```

#### **Wild Surge**
- **Type**: Active, Self-Buff
- **Effect**: Random buff for 2 turns (+50% damage, +50% defense, +100% speed)
- **Cooldown**: 6 turns
- **Scaling**: +10% buff strength per skill level
- **Special**: Duration increases with skill level

**Mathematical Formula:**
```
Buff Strength = 50% + (Skill Level × 10%)
Duration = 2 + (Skill Level // 3) turns
Random Buff = Random(damage, defense, speed)
```

#### **Chaos Mastery**
- **Type**: Passive
- **Effect**: +2% chance for skills to trigger twice
- **Maximum**: 30% double-trigger chance
- **Requirement**: 3 points in Wild archetype

**Mathematical Formula:**
```
Double Trigger Chance = min(Skill Level × 2%, 30%)
```

### **Advanced Wild Skills**

#### **Reality Warp**
- **Type**: Active, Area of Effect
- **Effect**: Random area effect (damage all enemies, heal all allies, buff all allies)
- **Cooldown**: 8 turns
- **Scaling**: +5% effect strength per skill level
- **Special**: Effect type changes with skill level

**Mathematical Formula:**
```
Effect Strength = 100% + (Skill Level × 5%)
Effect Type = Random(damage, heal, buff)
```

#### **Chaos Resonance**
- **Type**: Passive, Synergy
- **Effect**: +10% damage for each different status effect on target
- **Scaling**: +2% per skill level
- **Maximum**: +50% damage bonus
- **Special**: Stacks with other damage bonuses

**Mathematical Formula:**
```
Damage Bonus = min(Status Effects × (10% + Skill Level × 2%), 50%)
```

---

## **CROSS-ARCHETYPE SYNERGIES** 🔗

### **Ranged + Wild Synergies**

#### **Shadow Shot**
- **Requirement**: 3 points in Ranged + 2 points in Wild
- **Effect**: Ranged attacks have 15% chance to apply random status effect
- **Scaling**: +3% chance per combined skill level
- **Special**: Status effects are 50% more powerful

**Mathematical Formula:**
```
Synergy Chance = 15% + (Combined Level × 3%)
Status Power = Normal Status × 1.5
```

### **Magic + Wild Synergies**

#### **Elemental Chaos**
- **Requirement**: 3 points in Magic + 2 points in Wild
- **Effect**: Magic skills have 20% chance to trigger additional random effect
- **Scaling**: +4% chance per combined skill level
- **Special**: Additional effects are 75% as powerful

**Mathematical Formula:**
```
Synergy Chance = 20% + (Combined Level × 4%)
Additional Power = Normal Effect × 0.75
```

### **Melee + Magic Synergies**

#### **Battle Magic**
- **Requirement**: 3 points in Melee + 2 points in Magic
- **Effect**: Melee attacks have 10% chance to trigger magic status effect
- **Scaling**: +2% chance per combined skill level
- **Special**: Status effects last 50% longer

**Mathematical Formula:**
```
Synergy Chance = 10% + (Combined Level × 2%)
Status Duration = Normal Duration × 1.5
```

### **Melee + Wild Synergies**

#### **Savage Instinct**
- **Requirement**: 3 points in Melee + 2 points in Wild
- **Effect**: Melee attacks have 12% chance to deal 150% damage
- **Scaling**: +3% chance per combined skill level
- **Special**: Critical hits apply random status effect

**Mathematical Formula:**
```
Synergy Chance = 12% + (Combined Level × 3%)
Critical Damage = Normal Damage × 1.5
```

---

## **SKILL POINT COSTS** 💰

### **Cost Scaling System**
Skill point costs increase with skill level:

| Skill Level | Cost | Total Cost |
|-------------|------|------------|
| **1** | 1 | 1 |
| **2** | 2 | 3 |
| **3** | 3 | 6 |
| **4** | 4 | 10 |
| **5** | 5 | 15 |
| **6** | 6 | 21 |
| **7** | 7 | 28 |
| **8** | 8 | 36 |
| **9** | 9 | 45 |
| **10** | 10 | 55 |

### **Mathematical Formula**
```
Skill Cost = Skill Level
Total Cost = (Skill Level × (Skill Level + 1)) / 2
```

---

## **SKILL RESET SYSTEM** 🔄

### **Reset Mechanics**
- **Gold Cost**: 100 gold per skill point
- **Partial Reset**: Can reset individual skills
- **Full Reset**: Can reset all skills at once
- **No Penalty**: Only cost is gold

### **Reset Strategy**
- **Early Game**: Frequent resets to experiment
- **Mid Game**: Strategic resets for build optimization
- **Late Game**: Rare resets for major build changes
- **Endgame**: Minimal resets, focus on optimization

---

## **TECHNICAL SPECIFICATIONS** 🔧

### **API Reference**

#### **Core Skill Methods**

##### `calculate_skill_damage(skill_level: int, base_damage: Dict, attributes: Dict) -> Dict`
Calculates damage for a skill based on its level and attributes.

**Parameters:**
- `skill_level`: Current level of the skill
- `base_damage`: Dictionary containing base damage information
- `attributes`: Dictionary containing character attributes

**Returns:**
- `Dict`: Complete damage calculation including bonuses

**Mathematical Implementation:**
```python
def calculate_skill_damage(skill_level, base_damage, attributes):
    base = base_damage['min'] + (skill_level * base_damage['scaling'])
    attribute_bonus = attributes.get('power', 0) + attributes.get('knowledge', 0)
    
    return {
        'min_damage': base + attribute_bonus,
        'max_damage': base + attribute_bonus + base_damage['range'],
        'critical_chance': base_damage.get('crit_chance', 0) + (skill_level * 2),
        'status_chance': base_damage.get('status_chance', 0) + (skill_level * 3)
    }
```

##### `calculate_skill_cost(skill_level: int) -> int`
Calculates the cost to level up a skill.

**Parameters:**
- `skill_level`: Current level of the skill

**Returns:**
- `int`: Skill points required to level up

**Mathematical Implementation:**
```python
def calculate_skill_cost(skill_level):
    return skill_level
```

##### `check_synergy_requirements(skill_id: str, archetype_points: Dict) -> bool`
Checks if a synergy skill's requirements are met.

**Parameters:**
- `skill_id`: ID of the synergy skill
- `archetype_points`: Dictionary of points in each archetype

**Returns:**
- `bool`: True if requirements are met

---

## **PERFORMANCE CONSIDERATIONS** ⚡

### **Calculation Optimization**
- **Skill Caching**: Cache frequently used skill calculations
- **Batch Processing**: Calculate multiple skills simultaneously
- **Memory Management**: Efficient data structures for skill trees
- **Network Optimization**: Minimal data transfer for skill updates

### **Scalability Features**
- **Dynamic Loading**: Load skill data on demand
- **Compression**: Compress skill data for storage
- **Indexing**: Fast lookup for skill searches
- **Garbage Collection**: Automatic cleanup of unused skills

---

## **FUTURE ENHANCEMENTS** 🚀

### **Planned Features**
- **Skill Trees**: Visual skill progression system
- **Skill Combinations**: Chain multiple skills together
- **Skill Evolution**: Skills that change with usage
- **Seasonal Skills**: Limited-time special skills

### **Technical Improvements**
- **Real-time Updates**: Live skill effect updates
- **Advanced Tooltips**: Detailed skill information
- **Visual Enhancements**: Improved skill visualization
- **Mobile Integration**: Cross-platform skill management

---

## **TROUBLESHOOTING** 🔧

### **Common Issues**
- **Skill Calculation Errors**: Verify skill level and attribute formulas
- **Synergy Activation Bugs**: Check archetype point requirements
- **Performance Issues**: Monitor skill calculation complexity
- **Data Corruption**: Validate skill data integrity

### **Debug Tools**
- **Skill Calculator**: Test skill damage scenarios
- **Synergy Checker**: Verify synergy requirements
- **Build Simulator**: Test skill combinations
- **Damage Analyzer**: Compare skill effectiveness

---

*The Skills System provides the foundation for character customization and build diversity in Chronicles of Ruin: Sunderfall, offering deep strategic choices while maintaining accessibility for all players.*

# Character Progression System - Chronicles of Ruin: Sunderfall

## **OVERVIEW** 📈

The Character Progression System is the foundation of player advancement in Chronicles of Ruin: Sunderfall, providing multiple layers of progression that create meaningful choices and long-term goals. The system balances immediate gratification with strategic depth, ensuring players always have clear advancement paths.

---

## **PROGRESSION TIERS** 🎯

### **Three-Tier System**
Character progression operates on three distinct but interconnected tiers:

| Tier | Source | Frequency | Reset Cost | Purpose |
|------|--------|-----------|------------|---------|
| **Base Points** | Character Creation | One-time | Character Delete | Archetype Selection |
| **Class Points** | Every 3 Player Levels | Permanent | All Player Levels | Power Foundation |
| **Skill Points** | Every Player Level | Resettable | Gold Cost | Build Customization |

---

## **BASE POINTS** 🎭

### **Character Creation Allocation**
- **Total Points**: 3 points to allocate
- **Archetype Costs**: 
  - **Melee/Ranged/Magic**: 1 point each
  - **Wild**: 2 points (high-risk, high-reward)
- **Combination Rules**: Can combine any archetypes within point budget

### **Archetype Combinations**
- **Pure Builds**: 3 points in single archetype (maximum damage, glass cannon, fewer skills)
- **Hybrid Builds**: 2+1 combinations (access to 2/3 archetypes + flexibility) or 1+1+1 (maximum skill variety, less damage)
- **Wild Builds**: Wild + one other archetype creates unique hybrid archetypes:
  - **Wild + Melee** = **Beastmaster** archetype
  - **Wild + Ranged** = **Shadow Hunter** archetype  
  - **Wild + Magic** = **Alchemist** archetype

### **Mathematical Impact**
```
Base Power = Sum of Archetype Base Stats
Starting Luck = +1 for each non-Wild archetype, -1 for Wild
```

---

## **CLASS POINTS** 👑

### **Acquisition Mechanics**
- **Gain Rate**: 1 Class Point every 3 Player Levels
- **Formula**: `Class Points = Floor(Player Level / 3)`
- **Permanent Nature**: Cannot be lost except through reset
- **Power Scaling**: Each Class Point provides significant power increase

### **Class Point Benefits**
- **Attribute Grants**: +2 to primary archetype attributes
- **Skill Caps**: Increase maximum skill level by 1
- **Build Flexibility**: Enable more complex skill combinations
- **Endgame Scaling**: Foundation for high-level content

### **Reset Mechanics**
- **Reset Cost**: All Player Levels (returns to Level 1)
- **Class Points Retained**: Reset only affects Player Levels
- **Strategic Choice**: High-risk option for build optimization
- **One-Time Decision**: Cannot be undone

### **Mathematical Formulas**

#### **Class Point Calculation**
```
Class Points = Floor(Player Level / 3)
```

#### **Attribute Bonus Calculation**
```
Attribute Bonus = Class Points × 2
```

#### **Skill Cap Calculation**
```
Maximum Skill Level = Base Cap + Class Points
```

---

## **SKILL POINTS** ⚡

### **Acquisition Mechanics**
- **Gain Rate**: 1 Skill Point every Player Level
- **Formula**: `Skill Points = Player Level`
- **Resettable**: Can be reset for gold cost
- **Build Flexibility**: Primary tool for character customization

### **Skill Point Allocation**
- **Skill Leveling**: Increase individual skill levels
- **Cost Scaling**: Higher skill levels cost more points
- **Synergy Bonuses**: Multiple skills in same archetype provide bonuses
- **Cross-Archetype**: Skills from different archetypes can synergize

### **Reset System**
- **Gold Cost**: 100 gold per skill point reset
- **Partial Reset**: Can reset individual skills or all skills
- **Strategic Timing**: Best done when changing build focus
- **No Penalty**: Reset cost is only gold

### **Mathematical Formulas**

#### **Skill Point Cost**
```
Skill Level Cost = Base Cost + (Level - 1) × Scaling Factor
```

#### **Total Skill Points**
```
Available Skill Points = Player Level - Spent Skill Points
```

---

## **ATTRIBUTE SYSTEM** 💪

### **Core Attributes**
Each archetype has two primary attributes:

| Archetype | Primary Attribute | Secondary Attribute | Purpose |
|-----------|------------------|-------------------|---------|
| **Melee** | Power | Toughness | Damage & Magic Defense |
| **Ranged** | Agility | Finesse | Speed & Melee Defense |
| **Magic** | Knowledge | Wisdom | Magic & Ranged Defense |
| **Wild** | Chaos | Chaos | Utility & Random Effects |

### **Attribute Scaling**
- **Base Values**: Start at 10 for each attribute
- **Class Point Bonus**: +2 per Class Point to primary attributes
- **Equipment Bonus**: Items can provide attribute bonuses
- **Skill Bonuses**: Some skills provide temporary attribute bonuses

### **Mathematical Formulas**

#### **Attribute Calculation**
```
Final Attribute = Base + Class Points × 2 + Equipment + Skills
```

#### **Damage Calculation**
```
Damage = Power + Weapon Damage + Skill Damage
```

#### **Defense Calculation**
```
Defense = Toughness/Finesse/Wisdom + Equipment + Skills
```

---

## **EXPERIENCE SYSTEM** 📊

### **Three-Pool XP System**
Experience is separated into three independent pools with different purposes:

| XP Type | Purpose | Leveling | Point Gain | Monster Sources |
|---------|---------|----------|------------|-----------------|
| **Base XP** | General progression | 1.025x exponential | None (set at creation) | All monsters |
| **Class XP** | Core build strength | 1.025x exponential | 1 per 3 levels | Class-specific monsters or mixed (reduced) |
| **Skill XP** | Ability variety | 1.025x exponential | 1 per level | Skill-specific monsters or mixed (reduced) |

### **Reset-Based Leveling**
Each XP pool uses a reset system where XP starts fresh at each level:
- **Level 1**: 0/100 XP needed
- **Level 2**: 0/102 XP needed (100 × 1.025)
- **Level 3**: 0/105 XP needed (102 × 1.025)

### **Player Level Calculation**
```
Player Level = Class Level + Skill Level
```
- **Monster Scaling**: Tied to combined Player Level
- **World Difficulty**: Increases with Player Level
- **Archetype Bonuses**: Apply to specific XP types

### **XP Progression Formula**
```
XP Required for Level N = 100 × (1.025^(N-1))
```

### **Monster XP Distribution**
- **Specialized Monsters**: Give only Class XP or only Skill XP
- **Mixed Monsters**: Give both types at reduced rates
- **Base XP**: All monsters provide Base XP for general progression

### **Archetype XP Bonuses**
| Archetype | Base XP | Class XP | Skill XP |
|-----------|---------|----------|----------|
| **Melee** | +10% | Normal | Normal |
| **Ranged** | Normal | +10% | Normal |
| **Magic** | Normal | Normal | +10% |
| **Wild** | +20% | +20% | +20% |

---

## **ACHIEVEMENT-BASED CLASS POINTS** 🏆

### **Special Class Point Sources**
Certain achievements grant permanent Class Points:

#### **Combat Achievements**
- **Wild Slayer**: Defeat 100 Wild monsters of your own archetype
- **Boss Hunter**: Defeat all unique monsters in a district
- **Perfect Victory**: Complete a district without taking damage

#### **Exploration Achievements**
- **District Master**: Fully explore all districts in a row
- **Secret Finder**: Discover all hidden areas in a district
- **Speed Runner**: Complete a district in under 10 minutes

#### **Social Achievements**
- **Guild Leader**: Lead a guild to control 5 territories
- **Trading Master**: Complete 1000 successful trades
- **PvP Champion**: Win 100 PvP matches

### **Achievement Class Point Formula**
```
Achievement Class Points = Floor(Achievement Difficulty / 10)
```

---

## **GUILD TERRITORY BENEFITS** 🏰

### **Territory Control Bonuses**
Guilds that control territories provide members with:

#### **Resource Bonuses**
- **Gold Bonus**: +10% gold from monsters in controlled territory
- **Experience Bonus**: +5% experience from monsters in controlled territory
- **Item Bonus**: +15% chance for rare items in controlled territory

#### **Territory Management**
- **Defense Costs**: Guilds must pay to maintain territory control
- **Member Benefits**: All guild members receive territory bonuses
- **Competition**: Other guilds can challenge for territory control
- **Strategic Value**: High-value territories provide better bonuses

### **Mathematical Formulas**

#### **Territory Bonus Calculation**
```
Territory Bonus = Base Bonus × Territory Quality × Guild Level
```

#### **Guild Contribution**
```
Member Benefit = Territory Bonus / Number of Active Members
```

---

## **PROGRESSION STRATEGIES** 🧠

### **Early Game (Levels 1-20)**
- **Focus**: Basic archetype mastery
- **Strategy**: Invest heavily in primary archetype skills
- **Key**: Understand core mechanics and build foundation

### **Mid Game (Levels 21-80)**
- **Focus**: Skill synergies and equipment optimization
- **Strategy**: Develop secondary archetype for utility
- **Key**: Balance damage output with survivability

### **Late Game (Levels 81+)**
- **Focus**: Min-maxing and set optimization
- **Strategy**: Perfect skill combinations and equipment sets
- **Key**: Wild monster hunting and unique item farming

### **Endgame (Level 100+)**
- **Focus**: Achievement hunting and territory control
- **Strategy**: Guild-based progression and PvP dominance
- **Key**: Social progression and competitive play

---

## **RESET MECHANICS** 🔄

### **Skill Point Reset**
- **Cost**: 100 gold per skill point
- **Process**: Instant reset with gold payment
- **Strategy**: Best done when changing build focus
- **No Penalty**: Only cost is gold

### **Class Point Reset**
- **Cost**: All Player Levels (returns to Level 1)
- **Process**: High-risk, high-reward option
- **Strategy**: Only for major build changes
- **Permanent**: Cannot be undone

### **Character Reset**
- **Cost**: Delete character and start over
- **Process**: Complete fresh start
- **Strategy**: Only for major archetype changes
- **Learning**: Apply knowledge to new character

---

## **TECHNICAL SPECIFICATIONS** 🔧

### **API Reference**

#### **Core Progression Methods**

##### `calculate_class_points(player_level: int) -> int`
Calculates Class Points based on Player Level.

**Parameters:**
- `player_level`: Current player level

**Returns:**
- `int`: Number of Class Points

**Mathematical Implementation:**
```python
def calculate_class_points(player_level):
    return player_level // 3
```

##### `calculate_skill_points(player_level: int, spent_points: int) -> int`
Calculates available Skill Points.

**Parameters:**
- `player_level`: Current player level
- `spent_points`: Skill points already spent

**Returns:**
- `int`: Available skill points

**Mathematical Implementation:**
```python
def calculate_skill_points(player_level, spent_points):
    return player_level - spent_points
```

##### `calculate_experience_required(level: int) -> int`
Calculates experience required for next level.

**Parameters:**
- `level`: Target level

**Returns:**
- `int`: Experience required

**Mathematical Implementation:**
```python
def calculate_experience_required(level):
    return int(100 * (level ** 1.5))
```

##### `grant_class_point_for_achievement(achievement_id: str, player_id: str) -> bool`
Grants a Class Point for completing an achievement.

**Parameters:**
- `achievement_id`: ID of the completed achievement
- `player_id`: ID of the player

**Returns:**
- `bool`: True if Class Point was granted

---

## **PERFORMANCE CONSIDERATIONS** ⚡

### **Calculation Optimization**
- **Cached Values**: Pre-calculate frequently used values
- **Batch Updates**: Update multiple progression values simultaneously
- **Memory Management**: Efficient data structures for large player bases
- **Network Optimization**: Minimal data transfer for progression updates

### **Scalability Features**
- **Progressive Loading**: Load progression data on demand
- **Compression**: Compress progression data for storage
- **Indexing**: Fast lookup for achievement tracking
- **Garbage Collection**: Automatic cleanup of unused data

---

## **FUTURE ENHANCEMENTS** 🚀

### **Planned Features**
- **Prestige System**: Additional progression layer after level 100
- **Skill Trees**: Visual skill progression system
- **Achievement Tiers**: Multiple levels of achievement difficulty
- **Guild Progression**: Guild-level advancement systems

### **Technical Improvements**
- **Real-time Updates**: Live progression tracking
- **Advanced Analytics**: Detailed progression analysis
- **Visual Enhancements**: Improved progression visualization
- **Mobile Integration**: Cross-platform progression tracking

---

## **TROUBLESHOOTING** 🔧

### **Common Issues**
- **Progression Calculation Errors**: Verify level and point formulas
- **Achievement Tracking Bugs**: Check achievement completion logic
- **Performance Issues**: Monitor progression calculation complexity
- **Data Corruption**: Validate progression data integrity

### **Debug Tools**
- **Progression Calculator**: Test progression scenarios
- **Achievement Tracker**: Monitor achievement completion
- **Level Simulator**: Test leveling mechanics
- **Reset Analyzer**: Analyze reset costs and benefits

---

*The Character Progression System provides the foundation for long-term player engagement in Chronicles of Ruin: Sunderfall, offering multiple advancement paths while maintaining strategic depth and meaningful choices.*

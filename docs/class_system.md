# Class System - Chronicles of Ruin: Sunderfall

## **OVERVIEW** 👑

The Class System is the foundation of character identity and progression in Chronicles of Ruin: Sunderfall, providing a flexible archetype-based system that allows players to create unique combinations and playstyles. The system balances specialization with hybridization, ensuring every archetype choice feels meaningful and impactful.

---

## **ARCHETYPE SYSTEM** 🎭

### **Core Archetypes**
The game features four primary archetypes, each with distinct characteristics:

| Archetype | Primary Attribute | Secondary Attribute | Playstyle | Complexity |
|-----------|------------------|-------------------|-----------|------------|
| **Melee** | Power | Toughness | Close Combat | Low |
| **Ranged** | Agility | Finesse | Precision | Medium |
| **Magic** | Knowledge | Wisdom | Status Effects | High |
| **Wild** | Chaos | Chaos | Random Effects | Very High |

### **Archetype Combinations**
Players can combine archetypes to create hybrid builds:

#### **Pure Builds (3 Points)**
- **Pure Melee**: Maximum physical damage and defense
- **Pure Ranged**: Maximum precision and mobility
- **Pure Magic**: Maximum status effect power
- **Pure Wild**: Maximum chaos and unpredictability

#### **Hybrid Builds (2+1 Points)**
- **Melee + Ranged**: Balanced combat with both close and ranged options
- **Melee + Magic**: Physical damage with status effect support
- **Ranged + Magic**: Precision with magical enhancement
- **Wild + Any**: Chaos effects combined with specialization

#### **Wild Combinations**
- **Melee + Wild = Beastmaster**: Physical damage with random enhancements
- **Ranged + Wild = Shadowhunter**: Precision with chaotic effects
- **Magic + Wild = Alchemist**: Status effects with random amplification

---

## **MELEE ARCHETYPE** ⚔️

### **Core Characteristics**
- **Primary Focus**: Physical damage and close combat
- **Attribute Scaling**: Power increases damage, Toughness reduces magic damage
- **Combat Style**: Direct confrontation and sustained damage
- **Complexity**: Low - straightforward and accessible

### **Melee Subtypes**

#### **Juggernaut (Pure Melee)**
- **Specialization**: Maximum damage and defense
- **Unique Ability**: "Unstoppable Force" - cannot be stunned
- **Attribute Bonus**: +50% Power, +25% Toughness
- **Skill Focus**: Heavy weapons and defensive abilities

#### **Fighter (Melee + Ranged)**
- **Specialization**: Balanced combat with weapon switching
- **Unique Ability**: "Weapon Mastery" - can use any weapon type
- **Attribute Bonus**: +25% Power, +25% Agility
- **Skill Focus**: Versatile combat and tactical positioning

#### **Brawler (Melee + Magic)**
- **Specialization**: Physical damage with magical enhancement
- **Unique Ability**: "Elemental Fists" - melee attacks apply status effects
- **Attribute Bonus**: +25% Power, +25% Knowledge
- **Skill Focus**: Close combat with magical support

### **Mathematical Formulas**

#### **Melee Damage Calculation**
```
Base Damage = Power + Weapon Damage + Skill Damage
Final Damage = Base Damage × (1 + Equipment Bonuses) × Combat Triangle
```

#### **Melee Defense Calculation**
```
Physical Defense = Toughness + Equipment + Skills
Magic Defense = Toughness × 1.5 + Equipment + Skills
```

---

## **RANGED ARCHETYPE** 🏹

### **Core Characteristics**
- **Primary Focus**: Precision attacks and mobility
- **Attribute Scaling**: Agility increases attack speed and critical chance, Finesse reduces melee damage
- **Combat Style**: Tactical positioning and burst damage
- **Complexity**: Medium - requires positioning and timing

### **Ranged Subtypes**

#### **Marksman (Pure Ranged)**
- **Specialization**: Maximum precision and critical damage
- **Unique Ability**: "Dead Eye" - guaranteed critical hits on stationary targets
- **Attribute Bonus**: +50% Agility, +25% Finesse
- **Skill Focus**: Single-target precision and critical strikes

#### **Trapper (Ranged + Magic)**
- **Specialization**: Area control with magical traps
- **Unique Ability**: "Arcane Traps" - traps apply status effects
- **Attribute Bonus**: +25% Agility, +25% Knowledge
- **Skill Focus**: Area denial and magical enhancement

#### **Gunslinger (Ranged + Wild)**
- **Specialization**: Rapid attacks with chaotic effects
- **Unique Ability**: "Chaos Bullets" - attacks have random additional effects
- **Attribute Bonus**: +25% Agility, +25% Chaos
- **Skill Focus**: Rapid fire and unpredictable effects

### **Mathematical Formulas**

#### **Ranged Damage Calculation**
```
Base Damage = Agility + Weapon Damage + Skill Damage
Critical Chance = Base 5% + Agility Bonus + Equipment + Skills
Critical Damage = Base 2.0x + Equipment + Skills
```

#### **Ranged Defense Calculation**
```
Melee Defense = Finesse + Equipment + Skills
Ranged Defense = Agility + Equipment + Skills
```

---

## **MAGIC ARCHETYPE** 🔮

### **Core Characteristics**
- **Primary Focus**: Status effects and magical damage
- **Attribute Scaling**: Knowledge increases magical damage and status power, Wisdom reduces ranged damage
- **Combat Style**: Strategic status application and area control
- **Complexity**: High - requires understanding of status interactions

### **Magic Subtypes**

#### **Elementalist (Pure Magic)**
- **Specialization**: Maximum status effect power and duration
- **Unique Ability**: "Elemental Mastery" - status effects are 50% more powerful
- **Attribute Bonus**: +50% Knowledge, +25% Wisdom
- **Skill Focus**: Status effect application and enhancement

#### **Arcanist (Magic + Ranged)**
- **Specialization**: Precision magic with ranged application
- **Unique Ability**: "Arcane Precision" - status effects can be applied at range
- **Attribute Bonus**: +25% Knowledge, +25% Agility
- **Skill Focus**: Long-range status application and magical precision

#### **Occultist (Magic + Wild)**
- **Specialization**: Chaotic magic with unpredictable effects
- **Unique Ability**: "Reality Warp" - status effects have random additional properties
- **Attribute Bonus**: +25% Knowledge, +25% Chaos
- **Skill Focus**: Chaotic status effects and reality manipulation

### **Mathematical Formulas**

#### **Magic Damage Calculation**
```
Base Damage = Knowledge + Skill Damage
Status Power = Knowledge × 1.5 + Skill Level + Equipment
Status Duration = Base Duration + (Knowledge / 10) + Skill Level
```

#### **Magic Defense Calculation**
```
Ranged Defense = Wisdom + Equipment + Skills
Magic Defense = Knowledge + Equipment + Skills
```

---

## **WILD ARCHETYPE** 🌪️

### **Core Characteristics**
- **Primary Focus**: Random effects and chaos manipulation
- **Attribute Scaling**: Chaos increases success rate of random effects
- **Combat Style**: Unpredictable and high-risk, high-reward
- **Complexity**: Very High - requires understanding of probability and risk management

### **Wild Subtypes**

#### **Beastmaster (Melee + Wild)**
- **Specialization**: Physical damage with chaotic enhancements
- **Unique Ability**: "Savage Instinct" - melee attacks have random additional effects
- **Attribute Bonus**: +25% Power, +25% Chaos
- **Skill Focus**: Enhanced melee combat with unpredictable bonuses

#### **Shadowhunter (Ranged + Wild)**
- **Specialization**: Precision with chaotic effects
- **Unique Ability**: "Chaos Arrows" - ranged attacks have random additional effects
- **Attribute Bonus**: +25% Agility, +25% Chaos
- **Skill Focus**: Enhanced ranged combat with unpredictable bonuses

#### **Alchemist (Magic + Wild)**
- **Specialization**: Status effects with chaotic amplification
- **Unique Ability**: "Chaos Alchemy" - status effects have random additional properties
- **Attribute Bonus**: +25% Knowledge, +25% Chaos
- **Skill Focus**: Chaotic status effects and reality manipulation

### **Mathematical Formulas**

#### **Wild Effect Calculation**
```
Chaos Success Rate = Base 25% + (Chaos × 2%) + Equipment + Skills
Effect Power = Base Power × (0.5 + Chaos / 100)
Effect Duration = Base Duration × (1 + Chaos / 50)
```

#### **Wild Defense Calculation**
```
All Defense = Chaos + Equipment + Skills
Chaos Resistance = Chaos × 1.5 + Equipment + Skills
```

---

## **CLASS POINT SYSTEM** 📈

### **Class Point Acquisition**
- **Gain Rate**: 1 Class Point every 3 Player Levels
- **Formula**: `Class Points = Floor(Player Level / 3)`
- **Permanent Nature**: Cannot be lost except through reset
- **Power Scaling**: Each Class Point provides significant power increase

### **Class Point Benefits**
- **Attribute Grants**: +2 to primary archetype attributes per Class Point
- **Skill Caps**: Increase maximum skill level by 1 per Class Point
- **Build Flexibility**: Enable more complex skill combinations
- **Endgame Scaling**: Foundation for high-level content

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

## **ARCHETYPE SYNERGIES** 🔗

### **Melee Synergies**

#### **Melee + Ranged**
- **Combat Flexibility**: Switch between close and ranged combat
- **Tactical Advantage**: Use ranged attacks to control engagement distance
- **Skill Synergy**: Melee skills enhance ranged damage, ranged skills enhance melee mobility

#### **Melee + Magic**
- **Enhanced Damage**: Physical attacks apply status effects
- **Defensive Magic**: Use magic for defense while focusing on physical damage
- **Skill Synergy**: Melee skills trigger magical effects, magic skills enhance physical power

#### **Melee + Wild**
- **Chaotic Combat**: Physical attacks have random additional effects
- **Unpredictable Power**: Melee damage varies with chaos effects
- **Skill Synergy**: Melee skills trigger chaos effects, chaos effects enhance physical damage

### **Ranged Synergies**

#### **Ranged + Magic**
- **Precision Magic**: Apply status effects with ranged precision
- **Area Control**: Use magic for area denial while maintaining distance
- **Skill Synergy**: Ranged skills apply status effects, magic skills enhance ranged precision

#### **Ranged + Wild**
- **Chaotic Precision**: Ranged attacks have random additional effects
- **Unpredictable Accuracy**: Ranged damage varies with chaos effects
- **Skill Synergy**: Ranged skills trigger chaos effects, chaos effects enhance ranged precision

### **Magic Synergies**

#### **Magic + Wild**
- **Chaotic Magic**: Status effects have random additional properties
- **Reality Manipulation**: Magic becomes unpredictable and powerful
- **Skill Synergy**: Magic skills trigger chaos effects, chaos effects amplify magical power

---

## **CLASS RESET SYSTEM** 🔄

### **Reset Mechanics**
- **Reset Cost**: All Player Levels (returns to Level 1)
- **Class Points Retained**: Reset only affects Player Levels
- **Strategic Choice**: High-risk option for build optimization
- **One-Time Decision**: Cannot be undone

### **Reset Strategy**
- **Early Game**: Rare resets, focus on learning archetype mechanics
- **Mid Game**: Strategic resets for build optimization
- **Late Game**: Rare resets for major build changes
- **Endgame**: Minimal resets, focus on optimization

---

## **TECHNICAL SPECIFICATIONS** 🔧

### **API Reference**

#### **Core Class Methods**

##### `calculate_archetype_bonuses(archetype_points: Dict, class_points: int) -> Dict`
Calculates attribute bonuses from archetype and class points.

**Parameters:**
- `archetype_points`: Dictionary of points in each archetype
- `class_points`: Number of class points

**Returns:**
- `Dict`: Complete attribute bonus calculations

**Mathematical Implementation:**
```python
def calculate_archetype_bonuses(archetype_points, class_points):
    bonuses = {}
    
    # Calculate archetype-specific bonuses
    if archetype_points.get('melee', 0) > 0:
        bonuses['power'] = archetype_points['melee'] * 10 + class_points * 2
        bonuses['toughness'] = archetype_points['melee'] * 5 + class_points * 2
    
    if archetype_points.get('ranged', 0) > 0:
        bonuses['agility'] = archetype_points['ranged'] * 10 + class_points * 2
        bonuses['finesse'] = archetype_points['ranged'] * 5 + class_points * 2
    
    if archetype_points.get('magic', 0) > 0:
        bonuses['knowledge'] = archetype_points['magic'] * 10 + class_points * 2
        bonuses['wisdom'] = archetype_points['magic'] * 5 + class_points * 2
    
    if archetype_points.get('wild', 0) > 0:
        bonuses['chaos'] = archetype_points['wild'] * 10 + class_points * 2
    
    return bonuses
```

##### `get_archetype_subtype(archetype_points: Dict) -> str`
Determines the subtype based on archetype point allocation.

**Parameters:**
- `archetype_points`: Dictionary of points in each archetype

**Returns:**
- `str`: Subtype name

**Implementation:**
```python
def get_archetype_subtype(archetype_points):
    if archetype_points.get('wild', 0) > 0:
        if archetype_points.get('melee', 0) > 0:
            return 'Beastmaster'
        elif archetype_points.get('ranged', 0) > 0:
            return 'Shadowhunter'
        elif archetype_points.get('magic', 0) > 0:
            return 'Alchemist'
        else:
            return 'Chaos Master'
    else:
        # Pure archetype subtypes
        if archetype_points.get('melee', 0) == 3:
            return 'Juggernaut'
        elif archetype_points.get('ranged', 0) == 3:
            return 'Marksman'
        elif archetype_points.get('magic', 0) == 3:
            return 'Elementalist'
        else:
            return 'Hybrid'
```

##### `calculate_skill_caps(archetype_points: Dict, class_points: int) -> Dict`
Calculates maximum skill levels for each archetype.

**Parameters:**
- `archetype_points`: Dictionary of points in each archetype
- `class_points`: Number of class points

**Returns:**
- `Dict`: Maximum skill levels for each archetype

---

## **PERFORMANCE CONSIDERATIONS** ⚡

### **Optimization Strategies**
- **Class Caching**: Cache frequently used class calculations
- **Batch Processing**: Calculate multiple archetype bonuses simultaneously
- **Memory Management**: Efficient data structures for class data
- **Network Optimization**: Minimal data transfer for class updates

### **Scalability Features**
- **Dynamic Loading**: Load class data on demand
- **Compression**: Compress class data for storage
- **Indexing**: Fast lookup for archetype combinations
- **Garbage Collection**: Automatic cleanup of unused class data

---

## **FUTURE ENHANCEMENTS** 🚀

### **Planned Features**
- **Advanced Subtypes**: More specialized archetype combinations
- **Class Evolution**: Classes that change over time
- **Prestige Classes**: Advanced classes unlocked at high levels
- **Class Specializations**: Unique abilities for each subtype

### **Technical Improvements**
- **Real-time Updates**: Live class effect visualization
- **Advanced Tooltips**: Detailed class information
- **Visual Enhancements**: Improved class visualization
- **Mobile Integration**: Cross-platform class management

---

## **TROUBLESHOOTING** 🔧

### **Common Issues**
- **Class Calculation Errors**: Verify archetype and class point formulas
- **Subtype Assignment Bugs**: Check archetype point allocation logic
- **Performance Issues**: Monitor class calculation complexity
- **Data Corruption**: Validate class data integrity

### **Debug Tools**
- **Class Calculator**: Test class scenarios
- **Subtype Checker**: Verify subtype assignments
- **Synergy Simulator**: Test archetype combinations
- **Attribute Analyzer**: Monitor attribute calculations

---

*The Class System provides the foundation for character identity and progression in Chronicles of Ruin: Sunderfall, offering deep customization while maintaining accessibility for all players.*

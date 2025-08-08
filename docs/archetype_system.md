# Archetype System - Chronicles of Ruin: Sunderfall

## **OVERVIEW** 🎭

The Archetype System is the foundation of character identity and combat specialization in Chronicles of Ruin: Sunderfall, providing four distinct combat styles that can be combined to create unique hybrid builds. Each archetype offers distinct advantages, disadvantages, and playstyles that cater to different player preferences.

---

## **CORE ARCHETYPES** ⚔️

### **Archetype Overview**
The game features four primary archetypes, each with unique characteristics:

| Archetype | Primary Attribute | Secondary Attribute | Combat Style | Complexity | Risk Level |
|-----------|------------------|-------------------|--------------|------------|------------|
| **Melee** | Power | Toughness | Close Combat | Low | Low |
| **Ranged** | Agility | Finesse | Precision | Medium | Medium |
| **Magic** | Knowledge | Wisdom | Status Effects | High | Medium |
| **Wild** | Chaos | Chaos | Random Effects | Very High | High |

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

---

## **MELEE ARCHETYPE** ⚔️

### **Core Characteristics**
- **Combat Range**: Close combat (melee range)
- **Primary Focus**: Physical damage and sustained combat
- **Defense Style**: High physical defense, moderate magic defense
- **Complexity**: Low - straightforward and accessible
- **Risk Level**: Low - predictable and reliable

### **Melee Advantages**
- **High Physical Damage**: Direct, reliable damage output
- **Strong Defense**: Excellent physical damage mitigation
- **Sustained Combat**: Can fight for extended periods
- **Equipment Flexibility**: Can use any melee weapon type
- **Beginner Friendly**: Simple mechanics and clear progression

### **Melee Disadvantages**
- **Limited Range**: Must be close to enemies to attack
- **Mobility Issues**: Slower movement and positioning
- **Magic Vulnerability**: Weaker against magical attacks
- **Crowd Control**: Limited area of effect abilities
- **Resource Management**: Can run out of stamina in long fights

### **Melee Combat Mechanics**

#### **Damage Calculation**
```
Base Damage = Power + Weapon Damage + Skill Damage
Physical Bonus = Equipment Physical Bonuses + Skill Physical Bonuses
Final Damage = (Base Damage × (1 + Physical Bonus)) × Combat Triangle
```

#### **Defense Calculation**
```
Physical Defense = Toughness + Equipment + Skills
Magic Defense = Toughness × 0.5 + Equipment + Skills
Damage Reduction = min(Physical Defense / 100, 0.9)
```

#### **Combat Triangle Position**
- **Strong Against**: Ranged (+25% damage, -25% taken)
- **Weak Against**: Magic (-25% damage, +25% taken)
- **Neutral Against**: Melee (no bonus/penalty)

### **Melee Skills Focus**
- **Heavy Strike**: High damage single-target attack
- **Whirlwind**: Area of effect attack
- **Defensive Stance**: Passive damage reduction
- **Berserker Rage**: Temporary damage boost
- **Counter Attack**: Reactive damage when hit

---

## **RANGED ARCHETYPE** 🏹

### **Core Characteristics**
- **Combat Range**: Long distance combat
- **Primary Focus**: Precision attacks and tactical positioning
- **Defense Style**: High mobility, moderate defense
- **Complexity**: Medium - requires positioning and timing
- **Risk Level**: Medium - vulnerable if caught in close combat

### **Ranged Advantages**
- **Safe Distance**: Can attack from outside enemy range
- **High Critical Damage**: Excellent critical hit mechanics
- **Tactical Positioning**: Can control engagement distance
- **Mobility**: Fast movement and positioning
- **Precision**: High accuracy and critical chance

### **Ranged Disadvantages**
- **Close Combat Vulnerability**: Weak when enemies get close
- **Ammunition Management**: Limited ammunition for some weapons
- **Lower Base Damage**: Generally lower damage than melee
- **Equipment Dependency**: Requires specific ranged weapons
- **Positioning Requirements**: Needs tactical positioning

### **Ranged Combat Mechanics**

#### **Damage Calculation**
```
Base Damage = Agility + Weapon Damage + Skill Damage
Critical Chance = Base 5% + Agility Bonus + Equipment + Skills
Critical Damage = Base 2.0x + Equipment + Skills
Final Damage = Base Damage × (1 + Critical Chance × Critical Damage)
```

#### **Accuracy Calculation**
```
Base Accuracy = 90% + Agility Bonus + Equipment + Skills
Final Accuracy = min(Base Accuracy, 100%)
Miss Chance = 100% - Final Accuracy
```

#### **Combat Triangle Position**
- **Strong Against**: Magic (+25% damage, -25% taken)
- **Weak Against**: Melee (-25% damage, +25% taken)
- **Neutral Against**: Ranged (no bonus/penalty)

### **Ranged Skills Focus**
- **Precise Shot**: High accuracy single-target attack
- **Multi-Shot**: Attack multiple targets
- **Evasive Maneuvers**: Passive dodge chance
- **Sniper's Focus**: Temporary critical damage boost
- **Trap Mastery**: Place traps for area control

---

## **MAGIC ARCHETYPE** 🔮

### **Core Characteristics**
- **Combat Range**: Variable (close to long range)
- **Primary Focus**: Status effects and magical damage
- **Defense Style**: Low physical defense, high magical resistance
- **Complexity**: High - requires understanding of status interactions
- **Risk Level**: Medium - vulnerable to physical attacks

### **Magic Advantages**
- **Status Effects**: Powerful crowd control and damage over time
- **Area Control**: Excellent area of effect abilities
- **Versatility**: Can adapt to different situations
- **Synergy**: Status effects can combine for powerful combinations
- **Strategic Depth**: Complex but rewarding gameplay

### **Magic Disadvantages**
- **Physical Vulnerability**: Weak against physical attacks
- **Resource Management**: Requires mana management
- **Complex Mechanics**: Steep learning curve
- **Status Resistance**: Enemies can resist status effects
- **Boss Immunity**: Bosses are immune to status effects

### **Magic Combat Mechanics**

#### **Damage Calculation**
```
Base Damage = Knowledge + Skill Damage
Status Power = Knowledge × 1.5 + Skill Level + Equipment
Status Duration = Base Duration + (Knowledge / 10) + Skill Level
Status Chance = Base 15% + Skill Level + Equipment
```

#### **Status Effect Application**
```
Resistance Check = Target Resistance - Status Power
Final Status Power = max(Status Power - Resistance, 1)
Final Duration = max(Duration - (Resistance / 10), 0.1)
```

#### **Combat Triangle Position**
- **Strong Against**: Melee (+25% damage, -25% taken)
- **Weak Against**: Ranged (-25% damage, +25% taken)
- **Neutral Against**: Magic (no bonus/penalty)

### **Magic Skills Focus**
- **Fireball**: Single-target damage with burn chance
- **Frost Nova**: Area of effect with freeze chance
- **Arcane Shield**: Passive magic resistance
- **Chain Lightning**: Chain damage to multiple targets
- **Mana Surge**: Temporary status effect boost

---

## **WILD ARCHETYPE** 🌪️

### **Core Characteristics**
- **Combat Range**: Variable (random effects)
- **Primary Focus**: Random effects and chaos manipulation
- **Defense Style**: Unpredictable, moderate overall defense
- **Complexity**: Very High - requires understanding of probability
- **Risk Level**: High - unpredictable and potentially dangerous

### **Wild Advantages**
- **Unpredictable Power**: Can achieve incredible results
- **Unique Effects**: Access to effects no other archetype has
- **High Risk/Reward**: Potential for massive damage
- **Chaos Mastery**: Can manipulate random effects
- **Surprise Factor**: Enemies cannot predict your actions

### **Wild Disadvantages**
- **Unpredictability**: Results can be inconsistent
- **High Risk**: Can backfire and harm the player
- **Complex Mechanics**: Very difficult to master
- **Resource Intensive**: Chaos energy is limited
- **Team Coordination**: Hard to coordinate with other players

### **Wild Combat Mechanics**

#### **Chaos Effect Calculation**
```
Chaos Success Rate = Base 25% + (Chaos × 2%) + Equipment + Skills
Effect Power = Base Power × (0.5 + Chaos / 100)
Effect Duration = Base Duration × (1 + Chaos / 50)
Random Effect = Random(burn, freeze, stun, poison, heal, damage, buff, debuff)
```

#### **Chaos Energy Management**
```
Max Chaos Energy = 25 + (Chaos × 1.5) + Equipment + Skills
Chaos Cost = Base Cost × (1 - Chaos / 100)
Chaos Regeneration = Random(1, 5) per turn
```

#### **Combat Triangle Position**
- **Neutral Against**: All archetypes (no bonus/penalty)
- **Special Rule**: Wild monsters deal +50% damage to players of same archetype
- **Chaos Bonus**: Random effects can ignore combat triangle

### **Wild Skills Focus**
- **Chaos Bolt**: Random damage with random status effect
- **Wild Surge**: Random buff for self
- **Chaos Mastery**: Passive chance for skills to trigger twice
- **Reality Warp**: Random area effect
- **Chaos Resonance**: Damage bonus for each status effect on target

---

## **HYBRID ARCHETYPES** 🔗

### **Melee + Ranged (Fighter)**
- **Combat Style**: Versatile combat with weapon switching
- **Advantages**: Can adapt to any combat situation
- **Disadvantages**: Jack of all trades, master of none
- **Unique Ability**: "Weapon Mastery" - can use any weapon type

### **Melee + Magic (Brawler)**
- **Combat Style**: Physical damage with magical enhancement
- **Advantages**: High damage with status effect support
- **Disadvantages**: Resource intensive, complex management
- **Unique Ability**: "Elemental Fists" - melee attacks apply status effects

### **Ranged + Magic (Trapper)**
- **Combat Style**: Precision with magical area control
- **Advantages**: Excellent area denial and control
- **Disadvantages**: Vulnerable to close combat
- **Unique Ability**: "Arcane Traps" - traps apply status effects

### **Wild + Melee (Beastmaster)**
- **Combat Style**: Physical damage with chaotic enhancements
- **Advantages**: Unpredictable but powerful melee combat
- **Disadvantages**: Inconsistent results, high risk
- **Unique Ability**: "Savage Instinct" - melee attacks have random effects

### **Wild + Ranged (Shadowhunter)**
- **Combat Style**: Precision with chaotic effects
- **Advantages**: Unpredictable but accurate ranged combat
- **Disadvantages**: Inconsistent damage, positioning critical
- **Unique Ability**: "Chaos Arrows" - ranged attacks have random effects

### **Wild + Magic (Alchemist)**
- **Combat Style**: Status effects with chaotic amplification
- **Advantages**: Most powerful status effects in the game
- **Disadvantages**: Extremely complex, high resource cost
- **Unique Ability**: "Chaos Alchemy" - status effects have random properties

---

## **ARCHETYPE SYNERGIES** ⚡

### **Damage Synergies**
- **Melee + Ranged**: Melee skills enhance ranged damage, ranged skills enhance melee mobility
- **Melee + Magic**: Physical attacks apply status effects, magic enhances physical power
- **Ranged + Magic**: Precision applies status effects, magic enhances ranged accuracy
- **Wild + Any**: Chaos effects amplify all other archetype abilities

### **Defense Synergies**
- **Melee + Ranged**: Physical defense from melee, mobility from ranged
- **Melee + Magic**: Physical defense from melee, magical resistance from magic
- **Ranged + Magic**: Mobility from ranged, magical resistance from magic
- **Wild + Any**: Chaos resistance applies to all damage types

### **Utility Synergies**
- **Melee + Ranged**: Combat flexibility and tactical options
- **Melee + Magic**: Enhanced damage with status support
- **Ranged + Magic**: Area control with precision
- **Wild + Any**: Unique abilities not available to other combinations

---

## **ARCHETYPE PROGRESSION** 📈

### **Early Game (Levels 1-20)**
- **Focus**: Master basic archetype mechanics
- **Strategy**: Invest heavily in primary archetype
- **Goal**: Understand core strengths and weaknesses

### **Mid Game (Levels 21-80)**
- **Focus**: Develop hybrid synergies
- **Strategy**: Balance primary and secondary archetypes
- **Goal**: Create effective hybrid combinations

### **Late Game (Levels 81+)**
- **Focus**: Min-max archetype combinations
- **Strategy**: Perfect skill and equipment synergies
- **Goal**: Achieve maximum archetype effectiveness

### **Endgame (Level 100+)**
- **Focus**: Master complex archetype interactions
- **Strategy**: Optimize for specific content and challenges
- **Goal**: Push archetype combinations to their limits

---

## **TECHNICAL SPECIFICATIONS** 🔧

### **API Reference**

#### **Core Archetype Methods**

##### `calculate_archetype_bonuses(archetype_points: Dict) -> Dict`
Calculates attribute bonuses from archetype point allocation.

**Parameters:**
- `archetype_points`: Dictionary of points in each archetype

**Returns:**
- `Dict`: Complete attribute bonus calculations

**Mathematical Implementation:**
```python
def calculate_archetype_bonuses(archetype_points):
    bonuses = {}
    
    # Melee bonuses
    if archetype_points.get('melee', 0) > 0:
        bonuses['power'] = archetype_points['melee'] * 10
        bonuses['toughness'] = archetype_points['melee'] * 5
    
    # Ranged bonuses
    if archetype_points.get('ranged', 0) > 0:
        bonuses['agility'] = archetype_points['ranged'] * 10
        bonuses['finesse'] = archetype_points['ranged'] * 5
    
    # Magic bonuses
    if archetype_points.get('magic', 0) > 0:
        bonuses['knowledge'] = archetype_points['magic'] * 10
        bonuses['wisdom'] = archetype_points['magic'] * 5
    
    # Wild bonuses
    if archetype_points.get('wild', 0) > 0:
        bonuses['chaos'] = archetype_points['wild'] * 10
    
    return bonuses
```

##### `get_archetype_subtype(archetype_points: Dict) -> str`
Determines the subtype based on archetype point allocation.

**Parameters:**
- `archetype_points`: Dictionary of points in each archetype

**Returns:**
- `str`: Subtype name

##### `calculate_combat_triangle_bonus(attacker_archetype: str, defender_archetype: str) -> float`
Calculates combat triangle bonus for archetype matchups.

**Parameters:**
- `attacker_archetype`: Archetype of the attacker
- `defender_archetype`: Archetype of the defender

**Returns:**
- `float`: Damage multiplier (1.25 for advantage, 0.75 for disadvantage, 1.0 for neutral)

---

## **PERFORMANCE CONSIDERATIONS** ⚡

### **Optimization Strategies**
- **Archetype Caching**: Cache frequently used archetype calculations
- **Batch Processing**: Calculate multiple archetype bonuses simultaneously
- **Memory Management**: Efficient data structures for archetype data
- **Network Optimization**: Minimal data transfer for archetype updates

### **Scalability Features**
- **Dynamic Loading**: Load archetype data on demand
- **Compression**: Compress archetype data for storage
- **Indexing**: Fast lookup for archetype combinations
- **Garbage Collection**: Automatic cleanup of unused archetype data

---

## **FUTURE ENHANCEMENTS** 🚀

### **Planned Features**
- **Advanced Archetypes**: Additional archetypes with unique mechanics
- **Archetype Evolution**: Archetypes that change over time
- **Prestige Archetypes**: Advanced archetypes unlocked at high levels
- **Archetype Specializations**: Unique abilities for each archetype

### **Technical Improvements**
- **Real-time Updates**: Live archetype effect visualization
- **Advanced Tooltips**: Detailed archetype information
- **Visual Enhancements**: Improved archetype visualization
- **Mobile Integration**: Cross-platform archetype management

---

## **TROUBLESHOOTING** 🔧

### **Common Issues**
- **Archetype Calculation Errors**: Verify archetype point formulas
- **Combat Triangle Bugs**: Check archetype matchup logic
- **Performance Issues**: Monitor archetype calculation complexity
- **Data Corruption**: Validate archetype data integrity

### **Debug Tools**
- **Archetype Calculator**: Test archetype scenarios
- **Combat Triangle Checker**: Verify archetype matchups
- **Synergy Simulator**: Test archetype combinations
- **Attribute Analyzer**: Monitor archetype attribute calculations

---

*The Archetype System provides the foundation for character identity and combat specialization in Chronicles of Ruin: Sunderfall, offering deep customization while maintaining accessibility for all players.*

# Status & Elemental System - Chronicles of Ruin: Sunderfall

## **OVERVIEW** 🔥❄️⚡

The Status & Elemental System is the foundation of magical combat in Chronicles of Ruin: Sunderfall, providing a sophisticated status effect system that creates strategic depth without traditional elemental damage types. The system focuses on status effects that can be resisted, stacked, and synergized for powerful combinations.

---

## **STATUS EFFECT TYPES** 🎯

### **Primary Status Effects**
The system features four core status effects, each with unique mechanics:

| Status Effect | Type | Base Effect | Resistance | Scaling |
|---------------|------|-------------|------------|---------|
| **Burn** | Damage Over Time | 50% damage over 2s | Burn Resistance | +10% damage, +1s per level |
| **Freeze** | Crowd Control | Slow/Freeze | Cold Resistance | +5% chance, +0.5s per level |
| **Stun** | Crowd Control | Action Prevention | Stun Resistance | +3% chance, +0.3s per level |
| **Poison** | Damage Over Time | 30% damage over 3s | Poison Resistance | +8% damage, +0.8s per level |

### **Secondary Status Effects**
Advanced status effects that combine or enhance primary effects:

| Status Effect | Type | Trigger | Effect |
|---------------|------|---------|--------|
| **Bleed** | Physical DoT | Melee Critical | 25% damage over 4s |
| **Chaos** | Random Effect | Wild Skills | Random status application |
| **Corruption** | Debuff | Magic Skills | Reduces target effectiveness |
| **Vulnerability** | Debuff | Status Synergy | Increases damage taken |

---

## **BURN STATUS EFFECT** 🔥

### **Base Mechanics**
- **Damage Type**: Fire-based damage over time
- **Base Effect**: 50% of initial damage over 2 seconds
- **Resistance**: Reduced by Burn Resistance (flat number)
- **Stacking**: Multiple burns stack damage, not duration
- **Immunity**: Bosses are immune to burn effects

### **Mathematical Formulas**

#### **Burn Damage Calculation**
```
Burn Damage = (Initial Damage × 0.5) + (Skill Level × 0.1)
Burn Duration = 2 + Skill Level seconds
```

#### **Burn Resistance Application**
```
Final Burn Damage = max(Burn Damage - Burn Resistance, 1)
Final Burn Duration = max(Burn Duration - (Burn Resistance / 10), 0.5)
```

#### **Burn Stacking**
```
Total Burn Damage = Sum of all active burn effects
Burn Duration = Longest remaining burn duration
```

### **Burn Scaling**
- **Skill Level 1**: 50% damage over 2 seconds
- **Skill Level 5**: 100% damage over 6 seconds
- **Skill Level 10**: 150% damage over 11 seconds
- **Maximum**: 200% damage over 15 seconds

### **Burn Synergies**
- **Burn + Freeze**: Frozen targets take 25% more burn damage
- **Burn + Stun**: Stunned targets burn 50% faster
- **Burn + Poison**: Poisoned targets take 15% more burn damage

---

## **FREEZE STATUS EFFECT** ❄️

### **Base Mechanics**
- **Effect Type**: Crowd control with damage reduction
- **Base Effect**: 25% slow, chance to freeze completely
- **Resistance**: Reduced by Cold Resistance (flat number)
- **Duration**: 1-5 seconds based on skill level
- **Immunity**: Bosses are immune to freeze effects

### **Mathematical Formulas**

#### **Freeze Chance Calculation**
```
Freeze Chance = 25% + (Skill Level × 3%) - (Cold Resistance / 5)
```

#### **Freeze Duration Calculation**
```
Freeze Duration = 1 + (Skill Level × 0.4) - (Cold Resistance / 10)
```

#### **Slow Effect Calculation**
```
Slow Percentage = min(25% + (Skill Level × 2%), 75%)
Final Slow = max(Slow Percentage - (Cold Resistance / 4), 5%)
```

### **Freeze Mechanics**
- **Complete Freeze**: Target cannot act for duration
- **Partial Slow**: Target acts at reduced speed
- **Resistance Threshold**: If resistance > freeze power, only slow applies
- **Double Resistance**: If resistance > 2× freeze power, no effect

### **Freeze Scaling**
- **Skill Level 1**: 25% chance, 1.4 seconds duration
- **Skill Level 5**: 40% chance, 3.0 seconds duration
- **Skill Level 10**: 55% chance, 5.0 seconds duration
- **Maximum**: 70% chance, 7.0 seconds duration

### **Freeze Synergies**
- **Freeze + Burn**: Frozen targets take 25% more burn damage
- **Freeze + Stun**: Stunned targets freeze 50% longer
- **Freeze + Poison**: Poisoned targets freeze 30% longer

---

## **STUN STATUS EFFECT** ⚡

### **Base Mechanics**
- **Effect Type**: Complete action prevention
- **Base Effect**: Target cannot act for duration
- **Resistance**: Reduced by Stun Resistance (flat number)
- **Duration**: 0.5-3 seconds based on skill level
- **Immunity**: Bosses are immune to stun effects

### **Mathematical Formulas**

#### **Stun Chance Calculation**
```
Stun Chance = 20% + (Skill Level × 2%) - (Stun Resistance / 3)
```

#### **Stun Duration Calculation**
```
Stun Duration = 0.5 + (Skill Level × 0.25) - (Stun Resistance / 8)
```

#### **Stun Resistance Application**
```
Final Stun Chance = max(Stun Chance, 5%)
Final Stun Duration = max(Stun Duration, 0.1)
```

### **Stun Mechanics**
- **Complete Prevention**: Target cannot attack, move, or use skills
- **No Resistance**: Stun has no damage component
- **Priority Effect**: Stun overrides other status effects
- **Break on Damage**: Stun breaks when target takes damage

### **Stun Scaling**
- **Skill Level 1**: 22% chance, 0.75 seconds duration
- **Skill Level 5**: 30% chance, 1.75 seconds duration
- **Skill Level 10**: 40% chance, 3.0 seconds duration
- **Maximum**: 50% chance, 4.5 seconds duration

### **Stun Synergies**
- **Stun + Burn**: Stunned targets burn 50% faster
- **Stun + Freeze**: Stunned targets freeze 50% longer
- **Stun + Poison**: Stunned targets take 25% more poison damage

---

## **POISON STATUS EFFECT** ☠️

### **Base Mechanics**
- **Damage Type**: Nature-based damage over time
- **Base Effect**: 30% of initial damage over 3 seconds
- **Resistance**: Reduced by Poison Resistance (flat number)
- **Stacking**: Multiple poisons stack damage and duration
- **Immunity**: Bosses are immune to poison effects

### **Mathematical Formulas**

#### **Poison Damage Calculation**
```
Poison Damage = (Initial Damage × 0.3) + (Skill Level × 0.08)
Poison Duration = 3 + (Skill Level × 0.8) seconds
```

#### **Poison Resistance Application**
```
Final Poison Damage = max(Poison Damage - Poison Resistance, 1)
Final Poison Duration = max(Poison Duration - (Poison Resistance / 15), 0.5)
```

#### **Poison Stacking**
```
Total Poison Damage = Sum of all active poison effects
Poison Duration = Sum of all poison durations
```

### **Poison Scaling**
- **Skill Level 1**: 30% damage over 3.8 seconds
- **Skill Level 5**: 70% damage over 7.0 seconds
- **Skill Level 10**: 110% damage over 11.0 seconds
- **Maximum**: 150% damage over 15.0 seconds

### **Poison Synergies**
- **Poison + Burn**: Poisoned targets take 15% more burn damage
- **Poison + Freeze**: Poisoned targets freeze 30% longer
- **Poison + Stun**: Stunned targets take 25% more poison damage

---

## **RESISTANCE SYSTEM** 🛡️

### **Resistance Mechanics**
- **Flat Reduction**: Resistances reduce status effect power by flat numbers
- **No Immunity**: Players can never be completely immune to status effects
- **Equipment Source**: Resistances primarily come from equipment
- **Skill Bonuses**: Some skills provide temporary resistance bonuses

### **Resistance Calculation**
```
Effective Status Power = Status Power - Resistance
Minimum Effect = 1 point of damage or 0.1 seconds duration
```

### **Resistance Sources**
- **Equipment**: Helmets, chest pieces, accessories
- **Skills**: Passive skills and buffs
- **Set Bonuses**: Custom set bonuses
- **Temporary**: Potions and scrolls

### **Resistance Scaling**
- **Early Game**: 1-5 resistance points
- **Mid Game**: 5-15 resistance points
- **Late Game**: 15-30 resistance points
- **Endgame**: 30-50 resistance points

---

## **STATUS EFFECT INTERACTIONS** 🔗

### **Synergy Combinations**
Status effects can interact to create powerful combinations:

#### **Damage Amplification**
- **Burn + Freeze**: +25% burn damage to frozen targets
- **Burn + Stun**: +50% burn damage to stunned targets
- **Poison + Stun**: +25% poison damage to stunned targets

#### **Duration Extension**
- **Freeze + Stun**: +50% freeze duration to stunned targets
- **Freeze + Poison**: +30% freeze duration to poisoned targets
- **Stun + Poison**: +25% stun duration to poisoned targets

#### **Chance Enhancement**
- **Multiple Status**: Each active status increases chance of new status by 10%
- **Status Stacking**: Multiple applications of same status increase power by 15%

### **Mathematical Formulas**

#### **Synergy Damage Bonus**
```
Synergy Bonus = Base Status Damage × Synergy Multiplier
```

#### **Duration Extension**
```
Extended Duration = Base Duration × (1 + Synergy Bonus)
```

#### **Chance Enhancement**
```
Enhanced Chance = Base Chance + (Active Status Count × 10%)
```

---

## **WILD CHAOS EFFECTS** 🌪️

### **Chaos Mechanics**
- **Random Application**: Wild skills apply random status effects
- **Power Variation**: Chaos effects are 75% as powerful as direct effects
- **Duration Variation**: Chaos effects last 50% longer than direct effects
- **Resistance**: Chaos effects are reduced by general resistance

### **Chaos Effect Types**
- **Random Burn**: 75% power, 150% duration
- **Random Freeze**: 75% power, 150% duration
- **Random Stun**: 75% power, 150% duration
- **Random Poison**: 75% power, 150% duration

### **Mathematical Formulas**

#### **Chaos Effect Calculation**
```
Chaos Power = Direct Power × 0.75
Chaos Duration = Direct Duration × 1.5
Chaos Chance = Direct Chance × 0.8
```

---

## **BOSS IMMUNITY SYSTEM** 👑

### **Immunity Mechanics**
- **Complete Immunity**: Bosses are immune to all status effects
- **Phase Immunity**: Some bosses are immune during certain phases
- **Conditional Immunity**: Bosses may be immune to specific effects
- **Resistance Scaling**: Boss resistance increases with level

### **Boss Resistance Calculation**
```
Boss Resistance = Base Resistance + (Boss Level × 2)
Effective Status Power = max(Status Power - Boss Resistance, 0)
```

---

## **TECHNICAL SPECIFICATIONS** 🔧

### **API Reference**

#### **Core Status Methods**

##### `apply_status_effect(target_id: str, effect_type: str, power: float, duration: float, source: str) -> bool`
Applies a status effect to a target.

**Parameters:**
- `target_id`: ID of the target entity
- `effect_type`: Type of status effect ('burn', 'freeze', 'stun', 'poison')
- `power`: Strength of the status effect
- `duration`: Duration of the status effect
- `source`: Source of the status effect

**Returns:**
- `bool`: True if effect was successfully applied

**Mathematical Implementation:**
```python
def apply_status_effect(target_id, effect_type, power, duration, source):
    resistance = get_target_resistance(target_id, effect_type)
    final_power = max(power - resistance, 1)
    final_duration = max(duration - (resistance / 10), 0.1)
    
    return create_status_effect(target_id, effect_type, final_power, final_duration, source)
```

##### `calculate_status_damage(effect_type: str, base_damage: float, skill_level: int) -> float`
Calculates damage for a status effect.

**Parameters:**
- `effect_type`: Type of status effect
- `base_damage`: Base damage of the attack
- `skill_level`: Level of the skill applying the effect

**Returns:**
- `float`: Calculated status effect damage

**Mathematical Implementation:**
```python
def calculate_status_damage(effect_type, base_damage, skill_level):
    if effect_type == 'burn':
        return (base_damage * 0.5) + (skill_level * 0.1)
    elif effect_type == 'poison':
        return (base_damage * 0.3) + (skill_level * 0.08)
    else:
        return 0
```

##### `check_status_synergy(active_effects: List[str], new_effect: str) -> float`
Calculates synergy bonus for status effects.

**Parameters:**
- `active_effects`: List of currently active status effects
- `new_effect`: New status effect being applied

**Returns:**
- `float`: Synergy bonus multiplier

---

## **PERFORMANCE CONSIDERATIONS** ⚡

### **Optimization Strategies**
- **Status Caching**: Cache frequently used status calculations
- **Batch Processing**: Process multiple status effects simultaneously
- **Memory Management**: Efficient data structures for status tracking
- **Network Optimization**: Minimal data transfer for status updates

### **Scalability Features**
- **Dynamic Loading**: Load status data on demand
- **Compression**: Compress status data for storage
- **Indexing**: Fast lookup for status effects
- **Garbage Collection**: Automatic cleanup of expired effects

---

## **FUTURE ENHANCEMENTS** 🚀

### **Planned Features**
- **Status Combinations**: New effects from combining existing statuses
- **Status Evolution**: Status effects that change over time
- **Environmental Status**: Status effects based on terrain
- **Status Immunity**: Temporary immunity after status effects expire

### **Technical Improvements**
- **Real-time Updates**: Live status effect visualization
- **Advanced Tooltips**: Detailed status effect information
- **Visual Enhancements**: Improved status effect graphics
- **Mobile Integration**: Cross-platform status tracking

---

## **TROUBLESHOOTING** 🔧

### **Common Issues**
- **Status Calculation Errors**: Verify power and duration formulas
- **Resistance Application Bugs**: Check resistance calculation logic
- **Performance Issues**: Monitor status effect complexity
- **Data Corruption**: Validate status effect data integrity

### **Debug Tools**
- **Status Calculator**: Test status effect scenarios
- **Resistance Checker**: Verify resistance calculations
- **Synergy Simulator**: Test status effect combinations
- **Duration Tracker**: Monitor status effect timing

---

*The Status & Elemental System provides the foundation for magical combat in Chronicles of Ruin: Sunderfall, offering strategic depth through status effects while maintaining accessibility for all players.*

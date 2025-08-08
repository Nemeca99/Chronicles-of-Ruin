# Combat System - Chronicles of Ruin: Sunderfall

## **OVERVIEW** ⚔️

The Combat System is the heart of Chronicles of Ruin: Sunderfall, implementing a sophisticated damage calculation system that balances accessibility with strategic depth. Combat follows a rock-paper-scissors triangle system while incorporating complex damage modifiers, status effects, and character progression mechanics.

---

## **CORE MECHANICS** 🎯

### **Combat Triangle System**
The foundation of all combat interactions follows a percentage-based triangle:

- **Melee > Ranged**: +25% damage dealt, -25% damage taken
- **Ranged > Magic**: +25% damage dealt, -25% damage taken  
- **Magic > Melee**: +25% damage dealt, -25% damage taken
- **Wild**: Neutral in triangle, but Wild monsters deal +50% damage to players of the same archetype

### **Damage Calculation Order**
All damage calculations follow this strict order of operations:

1. **Base Stats**: Sum all base stats (Power + Weapon Damage + Skill Damage + Equipment Bonuses)
2. **Item Percentages**: Apply all percentage bonuses from equipment
3. **Combat Triangle**: Apply final combat triangle multiplier (+/- 25%)
4. **Damage Floor**: Ensure minimum damage threshold is met

**Mathematical Formula:**
```
Final Damage = (Base Stats × Item Percentages) × Combat Triangle Multiplier
```

### **Damage Floor System**
Players can never fully mitigate all damage, ensuring every hit matters:
- **Minimum Damage**: 1 point of damage minimum
- **Resistance Cap**: Maximum 90% damage reduction
- **Status Immunity**: Bosses are immune to all status effects

---

## **DAMAGE TYPES** 🔥❄️⚡

### **Physical Damage**
- **Source**: Basic attacks, weapon damage, non-elemental skills
- **Calculation**: Direct damage based on Power attribute + weapon damage
- **Resistance**: Reduced by Toughness attribute and physical resistance gear

### **Status Effect Damage**
- **Burn**: 50% of initial damage over 2 seconds (base), scales with skill level
- **Freeze**: Crowd control effect, reduced by cold resistance
- **Stun**: Instant crowd control, no resistance
- **Poison**: Damage over time, reduced by poison resistance

**Status Effect Scaling:**
- **Base Effect**: 50% damage over 2 seconds
- **Per Skill Level**: +10% damage, +1 second duration
- **Maximum Effect**: 100% damage over 7 seconds

---

## **WILD MONSTER MECHANICS** 🌪️

### **Spawn Mechanics**
- **Random Chance**: Regular monsters have a chance to spawn as "Wild" variants
- **Archetype Matching**: Wild monsters match the archetype of the base monster
- **Enhanced Rewards**: Bonus experience, gold, and better loot drops

### **Wild Combat Bonuses**
- **Damage Bonus**: +50% damage to players of the same archetype
- **Experience Bonus**: +100% experience when defeated
- **Loot Bonus**: +50% chance for rare items
- **Gold Bonus**: +75% gold drops

### **Pure Archetype Bonus**
Players with all Class Points in a single archetype gain:
- **Damage Bonus**: +25% damage against enemies of their own type
- **Stacking**: Combines with combat triangle bonuses

---

## **COMBAT FLOW** ⚡

### **Turn Structure**
1. **Initiative**: Determined by Agility attribute
2. **Action Selection**: Player chooses skill or basic attack
3. **Damage Calculation**: Apply all modifiers and bonuses
4. **Status Application**: Roll for status effect application
5. **Combat Resolution**: Apply damage and effects

### **Critical Hit System**
- **Base Chance**: 5% critical hit chance
- **Critical Multiplier**: 2.0x damage
- **Critical Sources**: Equipment bonuses, skill effects, character abilities

### **Status Effect Application**
- **Base Chance**: 15% chance to apply status effects
- **Resistance Reduction**: Target's resistance reduces effect power
- **Duration**: Status effects last 2-7 seconds based on skill level

---

## **TECHNICAL SPECIFICATIONS** 🔧

### **API Reference**

#### **Core Combat Methods**

##### `start_combat(player_id: str, enemy_id: str, enemy_data: Dict) -> str`
Initiates a new combat encounter.

**Parameters:**
- `player_id`: Unique identifier for the player character
- `enemy_id`: Unique identifier for the enemy
- `enemy_data`: Dictionary containing enemy statistics and abilities

**Returns:**
- `str`: Combat session identifier for tracking

**Example:**
```python
enemy_data = {
    'hp': 150,
    'damage': 25,
    'defense': 8,
    'archetype': 'melee',
    'resistances': {'physical': 0.15, 'burn': 0.25, 'freeze': 0.10}
}
combat_id = combat_system.start_combat("player_123", "goblin_001", enemy_data)
```

##### `calculate_damage(attacker_id: str, target_id: str, skill_data: Dict, weapon_data: Dict, attacker_stats: Dict) -> Tuple[float, List[str]]`
Calculates final damage using the complete calculation system.

**Parameters:**
- `attacker_id`: ID of the attacking entity
- `target_id`: ID of the defending entity
- `skill_data`: Dictionary containing skill information and modifiers
- `weapon_data`: Dictionary containing weapon statistics and bonuses
- `attacker_stats`: Dictionary containing attacker's current attributes

**Returns:**
- `Tuple[float, List[str]]`: (final_damage, applied_status_effects)

**Mathematical Implementation:**
```python
def calculate_damage(attacker_id, target_id, skill_data, weapon_data, attacker_stats):
    # Step 1: Calculate base stats
    base_damage = (
        attacker_stats['power'] + 
        weapon_data['damage'] + 
        skill_data['base_damage']
    )
    
    # Step 2: Apply item percentages
    item_bonus = sum(weapon_data['percentage_bonuses'])
    modified_damage = base_damage * (1 + item_bonus)
    
    # Step 3: Apply combat triangle
    triangle_multiplier = get_combat_triangle_multiplier(
        attacker_stats['archetype'], 
        target_stats['archetype']
    )
    final_damage = modified_damage * triangle_multiplier
    
    # Step 4: Apply damage floor
    final_damage = max(final_damage, 1.0)
    
    return final_damage, applied_status_effects
```

##### `apply_status_effect(target_id: str, effect_type: str, power: float, duration: int) -> bool`
Applies a status effect to a target.

**Parameters:**
- `target_id`: ID of the target entity
- `effect_type`: Type of status effect ('burn', 'freeze', 'stun', 'poison')
- `power`: Strength of the status effect
- `duration`: Duration in combat turns

**Returns:**
- `bool`: True if effect was successfully applied

---

## **COMBAT STRATEGIES** 🧠

### **Early Game (Levels 1-10)**
- **Focus**: Basic damage optimization
- **Strategy**: Maximize base damage through equipment
- **Key**: Understand combat triangle relationships

### **Mid Game (Levels 11-50)**
- **Focus**: Status effect utilization
- **Strategy**: Build around specific status effects
- **Key**: Resistance management and skill synergies

### **Late Game (Levels 51+)**
- **Focus**: Min-maxing and set optimization
- **Strategy**: Perfect gear combinations and set bonuses
- **Key**: Wild monster hunting and unique item farming

---

## **PERFORMANCE CONSIDERATIONS** ⚡

### **Calculation Optimization**
- **Caching**: Pre-calculate static bonuses
- **Batch Processing**: Handle multiple calculations simultaneously
- **Memory Management**: Efficient data structures for combat state

### **Network Optimization**
- **State Synchronization**: Minimal data transfer for multiplayer
- **Prediction**: Client-side damage prediction for responsiveness
- **Validation**: Server-side verification of all calculations

---

## **FUTURE ENHANCEMENTS** 🚀

### **Planned Features**
- **Combo System**: Chain attacks for bonus damage
- **Environmental Effects**: Terrain-based combat modifiers
- **Advanced Status Effects**: Stacking and interaction mechanics
- **PvP Balance**: Specialized rules for player vs player combat

### **Technical Improvements**
- **Real-time Combat**: Turn-based to real-time transition
- **Visual Effects**: Enhanced status effect visualization
- **Sound Integration**: Audio feedback for combat events

---

## **TROUBLESHOOTING** 🔧

### **Common Issues**
- **Damage Calculation Errors**: Verify order of operations
- **Status Effect Bugs**: Check resistance calculations
- **Performance Issues**: Monitor calculation complexity

### **Debug Tools**
- **Combat Log**: Detailed calculation breakdown
- **Damage Simulator**: Test damage scenarios
- **Status Tracker**: Monitor active status effects

---

*This combat system provides the foundation for all player interactions in Chronicles of Ruin: Sunderfall, ensuring engaging and strategic gameplay while maintaining accessibility for new players.*

# Player System - Chronicles of Ruin: Sunderfall

## **OVERVIEW** 👤

The Player System is the central hub of character management in Chronicles of Ruin: Sunderfall, handling all aspects of player progression, attributes, equipment, and state management. The system provides a comprehensive framework for character development while maintaining performance and scalability.

---

## **CHARACTER ATTRIBUTES** 💪

### **Core Attributes**
Each character has six primary attributes that define their capabilities:

| Attribute | Primary Archetype | Secondary Archetype | Effect | Scaling |
|-----------|------------------|-------------------|---------|---------|
| **Power** | Melee | - | Physical Damage | Linear |
| **Agility** | Ranged | - | Attack Speed & Critical | Linear |
| **Knowledge** | Magic | - | Magical Damage & Status | Linear |
| **Toughness** | Melee | - | Magic Defense | Linear |
| **Finesse** | Ranged | - | Melee Defense | Linear |
| **Wisdom** | Magic | - | Ranged Defense | Linear |
| **Chaos** | Wild | - | Random Effects | Exponential |

### **Attribute Calculation**
Attributes are calculated from multiple sources:

#### **Base Attributes**
```
Base Attribute = 10 + Archetype Bonus + Class Points × 2
```

#### **Equipment Bonuses**
```
Equipment Bonus = Sum of all equipment attribute bonuses
```

#### **Skill Bonuses**
```
Skill Bonus = Sum of all skill attribute bonuses
```

#### **Final Attribute**
```
Final Attribute = Base + Equipment + Skills + Temporary Bonuses
```

### **Attribute Scaling**

#### **Linear Scaling (Power, Agility, Knowledge, Toughness, Finesse, Wisdom)**
```
Effect = Attribute Value × Scaling Factor
```

#### **Exponential Scaling (Chaos)**
```
Effect = Base Effect × (1 + Chaos / 100)^2
```

---

## **EXPERIENCE & LEVELING** 📈

### **Experience System**
- **Experience Sources**: Combat, quests, achievements, exploration
- **Level Scaling**: Each level requires more experience
- **No Cap**: No maximum level limit
- **Soft Cap**: Level 100 where monster scaling increases

### **Experience Calculation**

#### **Experience Required**
```
Experience = 100 × Level^1.5
```

#### **Experience Gained**
```
Experience = Base XP × Monster Level × Difficulty Multiplier × Bonus Multipliers
```

#### **Level Progression**
```
Level = Floor(Experience / 100)^(2/3)
```

### **Level Benefits**
- **Skill Points**: 1 skill point per level
- **Class Points**: 1 class point every 3 levels
- **Attribute Bonuses**: Automatic attribute increases
- **Unlock Requirements**: Higher levels unlock new content

---

## **HEALTH & RESOURCES** ❤️

### **Health System**
- **Base Health**: 100 + (Toughness × 5)
- **Equipment Bonus**: Health bonuses from equipment
- **Skill Bonuses**: Health bonuses from skills
- **Regeneration**: Natural health regeneration over time

### **Resource Systems**

#### **Mana (Magic Users)**
- **Base Mana**: 50 + (Knowledge × 3)
- **Mana Cost**: Skills consume mana
- **Mana Regeneration**: Natural regeneration and potions

#### **Stamina (Physical Users)**
- **Base Stamina**: 100 + (Agility × 2)
- **Stamina Cost**: Physical skills consume stamina
- **Stamina Regeneration**: Natural regeneration and rest

#### **Chaos Energy (Wild Users)**
- **Base Chaos**: 25 + (Chaos × 1.5)
- **Chaos Cost**: Wild skills consume chaos energy
- **Chaos Regeneration**: Random regeneration and special items

### **Mathematical Formulas**

#### **Health Calculation**
```
Max Health = 100 + (Toughness × 5) + Equipment + Skills
Current Health = Max Health - Damage Taken + Healing
```

#### **Resource Calculation**
```
Max Resource = Base + (Primary Attribute × Multiplier) + Equipment + Skills
Current Resource = Max Resource - Consumed + Regeneration
```

---

## **EQUIPMENT SYSTEM** 🛡️

### **Equipment Slots**
- **Weapon Main**: Primary weapon
- **Weapon Off**: Secondary weapon or shield
- **Helmet**: Head protection
- **Chest**: Body armor
- **Legs**: Leg protection
- **Feet**: Foot protection
- **Gloves**: Hand protection
- **Ring 1**: First accessory
- **Ring 2**: Second accessory
- **Amulet**: Neck accessory

### **Equipment Bonuses**
- **Attribute Bonuses**: Direct increases to attributes
- **Percentage Bonuses**: Multiplicative bonuses to damage/defense
- **Special Effects**: Unique abilities and bonuses
- **Set Bonuses**: Bonuses from wearing multiple set items

### **Equipment Management**
- **Equipping**: Automatic stat calculation and application
- **Unequipping**: Removal of bonuses and recalculation
- **Comparison**: Automatic comparison with currently equipped items
- **Stash**: Storage system for unused equipment

---

## **INVENTORY SYSTEM** 📦

### **Inventory Structure**
- **Equipment Slots**: 10 fixed equipment slots
- **Inventory Slots**: 50 base inventory slots
- **Stash Storage**: 200 base stash slots
- **Gold Storage**: Unlimited gold storage

### **Inventory Management**
- **Item Stacking**: Automatic stacking of identical items
- **Weight System**: Items have weight that affects movement
- **Sorting**: Automatic sorting by type, rarity, and value
- **Search**: Text-based search and filtering

### **Mathematical Formulas**

#### **Inventory Capacity**
```
Base Capacity = 50 + (Agility / 10) + Equipment Bonuses
Current Usage = Sum of all item weights
Available Space = Base Capacity - Current Usage
```

---

## **GOLD & ECONOMY** 💰

### **Gold System**
- **Gold Sources**: Combat, quests, selling items, achievements
- **Gold Sinks**: Equipment, consumables, skill resets, set creation
- **Gold Storage**: Unlimited storage with no penalties
- **Gold Transfer**: Player-to-player trading and guild sharing

### **Economic Balance**
- **Income Scaling**: Gold income scales with level and difficulty
- **Expense Scaling**: Costs scale with item tier and quality
- **Inflation Control**: Automatic price adjustments based on server economy
- **Market Dynamics**: Supply and demand affect item prices

### **Mathematical Formulas**

#### **Gold Drop Calculation**
```
Base Gold = Monster Level × 2 + Random(1, Monster Level)
Final Gold = Base Gold × Difficulty Multiplier × Gold Find Bonus
```

#### **Item Value Calculation**
```
Base Value = Item Tier × Item Level × Quality Multiplier
Final Value = Base Value × Market Multiplier × Condition Multiplier
```

---

## **ACHIEVEMENT SYSTEM** 🏆

### **Achievement Categories**
- **Combat Achievements**: Defeat specific enemies or complete challenges
- **Exploration Achievements**: Discover areas and complete objectives
- **Social Achievements**: Interact with other players and guilds
- **Collection Achievements**: Gather specific items or sets

### **Achievement Rewards**
- **Experience**: Bonus experience for completing achievements
- **Class Points**: Special class points for difficult achievements
- **Unique Items**: Special items only available through achievements
- **Titles**: Custom titles and cosmetic rewards

### **Achievement Tracking**
- **Progress Tracking**: Real-time progress updates
- **Completion History**: Permanent record of achievements
- **Leaderboards**: Competitive achievement rankings
- **Guild Achievements**: Group achievements for guilds

---

## **GUILD SYSTEM** 🏰

### **Guild Structure**
- **Guild Master**: Leader with full administrative powers
- **Officers**: Members with limited administrative powers
- **Members**: Regular guild members
- **Recruits**: New members on probation

### **Guild Features**
- **Guild Chat**: Private communication channel
- **Guild Bank**: Shared storage for guild resources
- **Guild Quests**: Special quests for guild members
- **Guild Territories**: Control of specific game areas

### **Guild Benefits**
- **Experience Bonus**: Bonus experience for guild activities
- **Resource Sharing**: Shared access to guild resources
- **Territory Bonuses**: Bonuses for controlling territories
- **Social Features**: Enhanced social interaction

---

## **TERRITORY SYSTEM** 🗺️

### **Territory Control**
- **Guild Ownership**: Guilds can control specific territories
- **Territory Bonuses**: Bonuses for guild members in controlled areas
- **Territory Management**: Administrative tools for territory control
- **Territory Conflict**: Competition between guilds for control

### **Territory Benefits**
- **Resource Bonuses**: Increased resource gathering in controlled areas
- **Experience Bonuses**: Bonus experience for guild activities
- **Item Bonuses**: Increased item drop rates in controlled areas
- **Defense Bonuses**: Enhanced defense in controlled areas

### **Mathematical Formulas**

#### **Territory Bonus Calculation**
```
Base Bonus = 10% + (Guild Level × 2%) + (Territory Quality × 5%)
Member Bonus = Base Bonus / Number of Active Members
```

---

## **TECHNICAL SPECIFICATIONS** 🔧

### **API Reference**

#### **Core Player Methods**

##### `calculate_player_stats(player_id: str) -> Dict`
Calculates all player statistics from attributes, equipment, and skills.

**Parameters:**
- `player_id`: Unique identifier for the player

**Returns:**
- `Dict`: Complete player statistics

**Mathematical Implementation:**
```python
def calculate_player_stats(player_id):
    # Get base attributes
    base_attrs = get_base_attributes(player_id)
    
    # Get equipment bonuses
    equipment_bonuses = get_equipment_bonuses(player_id)
    
    # Get skill bonuses
    skill_bonuses = get_skill_bonuses(player_id)
    
    # Calculate final attributes
    final_attrs = {}
    for attr in base_attrs:
        final_attrs[attr] = (
            base_attrs[attr] + 
            equipment_bonuses.get(attr, 0) + 
            skill_bonuses.get(attr, 0)
        )
    
    # Calculate derived stats
    stats = {
        'max_health': 100 + (final_attrs['toughness'] * 5),
        'max_mana': 50 + (final_attrs['knowledge'] * 3),
        'max_stamina': 100 + (final_attrs['agility'] * 2),
        'damage': final_attrs['power'] + final_attrs['agility'],
        'defense': final_attrs['toughness'] + final_attrs['finesse']
    }
    
    return stats
```

##### `update_player_experience(player_id: str, experience_gained: int) -> Dict`
Updates player experience and handles level-ups.

**Parameters:**
- `player_id`: Unique identifier for the player
- `experience_gained`: Amount of experience to add

**Returns:**
- `Dict`: Level-up information and new stats

**Mathematical Implementation:**
```python
def update_player_experience(player_id, experience_gained):
    current_exp = get_player_experience(player_id)
    current_level = get_player_level(player_id)
    
    new_exp = current_exp + experience_gained
    new_level = floor((new_exp / 100) ** (2/3))
    
    level_ups = new_level - current_level
    
    if level_ups > 0:
        # Grant skill points
        skill_points_gained = level_ups
        
        # Grant class points
        class_points_gained = floor(new_level / 3) - floor(current_level / 3)
        
        return {
            'level_ups': level_ups,
            'skill_points_gained': skill_points_gained,
            'class_points_gained': class_points_gained,
            'new_level': new_level,
            'new_experience': new_exp
        }
    
    return {'level_ups': 0}
```

##### `equip_item(player_id: str, item_id: str, slot: str) -> bool`
Equips an item to a specific slot.

**Parameters:**
- `player_id`: Unique identifier for the player
- `item_id`: Unique identifier for the item
- `slot`: Equipment slot to equip the item to

**Returns:**
- `bool`: True if successfully equipped

---

## **PERFORMANCE CONSIDERATIONS** ⚡

### **Optimization Strategies**
- **Stat Caching**: Cache frequently calculated player statistics
- **Batch Updates**: Update multiple player attributes simultaneously
- **Memory Management**: Efficient data structures for player data
- **Network Optimization**: Minimal data transfer for player updates

### **Scalability Features**
- **Dynamic Loading**: Load player data on demand
- **Compression**: Compress player data for storage
- **Indexing**: Fast lookup for player searches
- **Garbage Collection**: Automatic cleanup of unused player data

---

## **FUTURE ENHANCEMENTS** 🚀

### **Planned Features**
- **Player Housing**: Personal housing system with customization
- **Pet System**: Companion creatures with unique abilities
- **Reputation System**: Dynamic reputation with different factions
- **Player Titles**: Customizable titles and achievements

### **Technical Improvements**
- **Real-time Updates**: Live player stat visualization
- **Advanced Analytics**: Detailed player performance analysis
- **Visual Enhancements**: Improved player interface
- **Mobile Integration**: Cross-platform player management

---

## **TROUBLESHOOTING** 🔧

### **Common Issues**
- **Stat Calculation Errors**: Verify attribute and equipment formulas
- **Experience Bugs**: Check experience and level-up logic
- **Performance Issues**: Monitor player calculation complexity
- **Data Corruption**: Validate player data integrity

### **Debug Tools**
- **Player Calculator**: Test player scenarios
- **Stat Checker**: Verify player statistics
- **Experience Simulator**: Test leveling mechanics
- **Equipment Analyzer**: Monitor equipment effects

---

*The Player System provides the foundation for character management and progression in Chronicles of Ruin: Sunderfall, offering comprehensive character development while maintaining performance and accessibility.*

# Itemization System - Chronicles of Ruin: Sunderfall

## **OVERVIEW** 🛡️

The Itemization System is the cornerstone of character progression in Chronicles of Ruin: Sunderfall, providing a deep and rewarding loot experience that scales from simple early-game decisions to complex endgame optimization. The system balances accessibility with strategic depth, ensuring every item find feels meaningful.

---

## **ITEM TIERS & RARITY** 💎

### **Tier Progression**
Items follow a clear progression system with increasing complexity and power:

| Tier | Affixes | Max Value | Status Effects | Drop Rate |
|------|---------|-----------|---------------|-----------|
| **Common** | 1 | +3 | ❌ | 45% |
| **Uncommon** | 2 | +5 | ❌ | 30% |
| **Rare** | 3 | +8 | ❌ | 15% |
| **Magical Rare** | 4 | +12 | ✅ | 8% |
| **Legendary** | 5 | +20 | ✅ | 2% |
| **Unique** | Fixed | Fixed | ✅ | 0.1% |

### **Affix System**
- **Minimum Value**: All affixes have a minimum value of 1
- **Maximum Scaling**: Maximum values increase with item tier
- **Random Selection**: Affixes are randomly selected from pools
- **No Duplicates**: Items cannot have duplicate affixes

---

## **AFFIX POOLS** 🎯

### **Core Attribute Affixes**
- **Power**: +1 to +20 (increases physical damage)
- **Agility**: +1 to +20 (increases attack speed and critical chance)
- **Knowledge**: +1 to +20 (increases magical damage and status effect power)
- **Toughness**: +1 to +20 (reduces damage taken from magic)
- **Finesse**: +1 to +20 (reduces damage taken from melee)
- **Wisdom**: +1 to +20 (reduces damage taken from ranged)
- **Chaos**: +1 to +20 (increases Wild ability success rate)

### **Combat Stat Affixes**
- **Damage Percentage**: +1% to +25% (increases all damage)
- **Critical Chance**: +1% to +15% (increases critical hit chance)
- **Critical Multiplier**: +5% to +50% (increases critical damage)
- **Attack Speed**: +1% to +20% (increases attack frequency)
- **Accuracy**: +1% to +25% (reduces miss chance)

### **Status Effect Affixes**
*Available on Magical Rare items and above*

- **Burn Chance**: +1% to +15% (chance to inflict burn on hit)
- **Freeze Chance**: +1% to +12% (chance to freeze target)
- **Stun Chance**: +1% to +10% (chance to stun target)
- **Poison Chance**: +1% to +12% (chance to poison target)

### **Resistance Affixes**
- **Physical Resistance**: +1 to +15 (reduces physical damage)
- **Burn Resistance**: +1 to +20 (reduces burn damage and duration)
- **Freeze Resistance**: +1 to +20 (reduces freeze duration)
- **Poison Resistance**: +1 to +20 (reduces poison damage)
- **Stun Resistance**: +1 to +15 (reduces stun duration)

### **Utility Affixes**
- **Luck**: +1 to +10 (increases item quality on drops)
- **Gold Find**: +1% to +25% (increases gold drops)
- **Experience Gain**: +1% to +15% (increases experience gained)
- **Movement Speed**: +1% to +20% (increases travel speed)

---

## **LUCK SYSTEM** 🍀

### **Luck Mechanics**
The Luck stat is a unique affix that affects item quality rather than drop rates:

- **Base Effect**: Each point of Luck gives a 5% chance to increase an item's base stats by 1 point
- **Per Stat Roll**: Luck is rolled separately for each base stat on an item
- **Stacking**: Multiple Luck sources stack additively
- **No Cap**: Luck has no theoretical maximum

### **Luck Scaling**
- **Early Game (Levels 1-20)**: Very powerful, small bonuses create large percentage increases
- **Mid Game (Levels 21-80)**: Diminished effectiveness, other stats become more valuable
- **Late Game (Levels 81+)**: Powerful again, high Luck can create incredibly strong items

### **Archetype Luck Bonuses**
- **Melee/Ranged/Magic**: Start with +1 Luck bonus
- **Wild**: Start with -1 Luck penalty (high-risk, high-reward)

### **Mathematical Formula**
```
Luck Success Chance = Luck Points × 5%
Base Stat Bonus = Random(1, Luck Points) per successful roll
```

---

## **UNIQUE ITEMS** ⭐

### **Unique Item Characteristics**
- **Fixed Affixes**: Pre-determined affixes that never change
- **Special Effects**: Unique abilities not available on other items
- **Level Scaling**: Item level tied to the unique monster's level
- **100% Drop Rate**: Always drop from their unique monster
- **Perpetual Scaling**: Only items that scale infinitely with level

### **Unique Item Examples**
- **Helmet**: 25% chance to freeze all enemies for 5 seconds
- **Weapon**: 15% chance to deal 200% damage to stunned enemies
- **Chest**: 20% chance to reflect 50% of damage taken
- **Boots**: 30% chance to gain 3 seconds of invulnerability when hit

### **Unique Item Acquisition**
- **Spawn Mechanics**: Unique monsters randomly spawn in districts
- **Level Scaling**: Unique monster level = District level + random bonus
- **Item Level**: Unique item level = Unique monster level
- **Respawn**: Unique monsters respawn after 24 hours

---

## **SET ITEM SYSTEM** 🔗

### **Custom Set Creation**
Players can create their own custom sets using any items they own:

- **Maximum Items**: Up to 10 items per set
- **Item Types**: Weapon, Chest, Helmet, Legs, Feet, Gloves, Rings (2), Amulet
- **Creation Cost**: Gold cost based on item tier and quantity
- **One-Time Process**: Sets cannot be modified after creation

### **Set Bonus Mechanics**
- **Random Pool**: Bonuses selected from randomized pools
- **Tiered Bonuses**: More items = more powerful bonuses
- **Luck Influence**: Higher Luck on items = better bonus pools
- **Soulbound**: Items become bound to character after set creation

### **Set Bonus Examples**

#### **2-Item Set Bonuses**
- +5% to all attributes
- +10% damage against specific monster types
- +15% resistance to specific status effects

#### **5-Item Set Bonuses**
- +25% damage against all enemies
- +50% critical hit chance
- +100% status effect duration
- +200% gold find

#### **10-Item Set Bonuses**
- **Unique Abilities**: Special effects not available elsewhere
- **Synergy Bonuses**: Powerful combinations of multiple effects
- **Build-Defining**: Bonuses that fundamentally change gameplay

### **Set Naming Convention**
```
[Character Name]'s Set of [Random Descriptive Phrase]
```
**Examples:**
- "Nemeca's Set of Glorious Charms"
- "Thunder's Set of Eternal Might"
- "Shadow's Set of Hidden Power"

---

## **ITEM CALCULATION SYSTEM** 🧮

### **Damage Calculation Integration**
Items contribute to damage calculations in specific ways:

1. **Base Stats**: Flat bonuses add directly to base damage
2. **Percentage Bonuses**: Applied after base stats are calculated
3. **Accessory Combination**: Ring and amulet percentages are combined
4. **Set Bonuses**: Applied as final multipliers

### **Mathematical Formulas**

#### **Base Damage Calculation**
```
Base Damage = Power + Weapon Damage + Equipment Bonuses + Skill Damage
```

#### **Percentage Application**
```
Modified Damage = Base Damage × (1 + Total Item Percentages)
```

#### **Accessory Combination**
```
Combined Accessory Bonus = (Ring 1 % + Ring 2 % + Amulet %) × 1.5
```

#### **Set Bonus Application**
```
Final Damage = Modified Damage × (1 + Set Bonus Percentages)
```

---

## **ITEM DROP SYSTEM** 📦

### **Drop Rate Mechanics**
- **Base Drop Rate**: 15% chance for any item to drop
- **Tier Scaling**: Higher tiers have exponentially lower drop rates
- **Level Scaling**: Item level = Monster level ± 3 levels
- **Quality Scaling**: Higher level monsters drop higher quality items

### **Drop Rate Formula**
```
Drop Chance = Base Rate × Tier Multiplier × Level Bonus
```

### **Tier Multipliers**
- **Common**: 1.0x
- **Uncommon**: 0.67x
- **Rare**: 0.33x
- **Magical Rare**: 0.18x
- **Legendary**: 0.04x
- **Unique**: 0.007x

---

## **ITEM MANAGEMENT** 📋

### **Inventory System**
- **Slot-Based**: Fixed number of equipment slots
- **Stash Storage**: Additional storage for items
- **Item Comparison**: Automatic stat comparison when equipping
- **Quick Equip**: One-click equipment changes

### **Item Quality Indicators**
- **Color Coding**: Each tier has distinct color
- **Stat Display**: Clear numerical values for all stats
- **Comparison Tooltips**: Shows differences when hovering
- **Set Indicators**: Visual markers for set items

### **Item Maintenance**
- **Repair System**: Items degrade with use
- **Enhancement**: Optional item improvement system
- **Transmutation**: Convert items between tiers
- **Salvage**: Break down items for materials

---

## **TECHNICAL SPECIFICATIONS** 🔧

### **API Reference**

#### **Core Item Methods**

##### `generate_item(item_tier: str, monster_level: int, luck_bonus: int) -> Dict`
Generates a random item of specified tier.

**Parameters:**
- `item_tier`: Tier of item to generate ('common', 'uncommon', etc.)
- `monster_level`: Level of monster that dropped the item
- `luck_bonus`: Luck bonus from character and equipment

**Returns:**
- `Dict`: Complete item data structure

**Example:**
```python
item_data = items_system.generate_item('rare', 25, 3)
# Returns: {
#     'name': 'Steel Sword',
#     'tier': 'rare',
#     'level': 25,
#     'affixes': [
#         {'type': 'power', 'value': 8},
#         {'type': 'damage_percent', 'value': 12},
#         {'type': 'critical_chance', 'value': 5}
#     ],
#     'base_stats': {'damage': 15, 'durability': 100}
# }
```

##### `calculate_item_power(item_data: Dict) -> float`
Calculates the overall power level of an item.

**Parameters:**
- `item_data`: Complete item data structure

**Returns:**
- `float`: Numerical power rating

**Mathematical Implementation:**
```python
def calculate_item_power(item_data):
    base_power = sum(item_data['base_stats'].values())
    affix_power = sum(affix['value'] for affix in item_data['affixes'])
    tier_multiplier = get_tier_multiplier(item_data['tier'])
    
    return (base_power + affix_power) * tier_multiplier
```

##### `create_custom_set(items: List[Dict], character_name: str) -> Dict`
Creates a custom set from provided items.

**Parameters:**
- `items`: List of items to include in set
- `character_name`: Name of character creating the set

**Returns:**
- `Dict`: Set data with bonus and name

---

## **PERFORMANCE CONSIDERATIONS** ⚡

### **Optimization Strategies**
- **Item Caching**: Cache frequently accessed item data
- **Batch Generation**: Generate multiple items simultaneously
- **Memory Management**: Efficient data structures for large inventories
- **Network Optimization**: Minimal data transfer for multiplayer

### **Scalability Features**
- **Dynamic Loading**: Load item data on demand
- **Compression**: Compress item data for storage
- **Indexing**: Fast lookup for item searches
- **Garbage Collection**: Automatic cleanup of unused items

---

## **FUTURE ENHANCEMENTS** 🚀

### **Planned Features**
- **Item Enchanting**: Add temporary bonuses to items
- **Item Fusion**: Combine items to create new ones
- **Dynamic Affixes**: Affixes that change based on usage
- **Seasonal Items**: Limited-time special items

### **Technical Improvements**
- **Real-time Updates**: Live item stat updates
- **Advanced Filtering**: Complex item search and filtering
- **Visual Enhancements**: Improved item visualization
- **Mobile Integration**: Cross-platform item management

---

## **TROUBLESHOOTING** 🔧

### **Common Issues**
- **Item Generation Errors**: Check tier and level parameters
- **Set Creation Failures**: Verify item compatibility
- **Performance Issues**: Monitor item cache usage
- **Data Corruption**: Validate item data integrity

### **Debug Tools**
- **Item Inspector**: Detailed item analysis tool
- **Drop Simulator**: Test item drop mechanics
- **Set Builder**: Visual set creation tool
- **Power Calculator**: Item power comparison tool

---

*The Itemization System provides the foundation for character progression and endgame content in Chronicles of Ruin: Sunderfall, offering deep customization while maintaining accessibility for all players.*

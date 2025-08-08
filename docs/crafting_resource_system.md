# Crafting & Resource System - Chronicles of Ruin: Sunderfall

## **OVERVIEW** 🔨

The Crafting & Resource System is the foundation of item creation and economic progression in Chronicles of Ruin: Sunderfall, providing players with the ability to create powerful equipment, consumables, and unique items. The system balances resource gathering, crafting complexity, and reward value to create a meaningful crafting experience.

---

## **RESOURCE TYPES** 📦

### **Monster-Type Resources**
Resources dropped by specific monster types:

| Resource Type | Source Monster | Drop Rate | Base Value | Crafting Use |
|---------------|----------------|-----------|------------|--------------|
| **Demon Essence** | Demonic | 15% | 25 gold | Fire items, chaos items |
| **Undead Bone** | Undead | 20% | 15 gold | Dark items, defensive items |
| **Beast Hide** | Beast | 25% | 10 gold | Nature items, leather items |
| **Elemental Core** | Elemental | 10% | 50 gold | Magic items, status items |
| **Construct Metal** | Construct | 30% | 20 gold | Metal items, mechanical items |
| **Humanoid Cloth** | Humanoid | 35% | 5 gold | Light items, utility items |

### **Environmental Resources**
Resources found in the world environment:

| Resource Type | Location | Rarity | Base Value | Crafting Use |
|---------------|----------|--------|------------|--------------|
| **Herbs** | All districts | Common | 2 gold | Potions, status items |
| **Ore** | Industrial districts | Uncommon | 8 gold | Metal items, weapons |
| **Gems** | Noble districts | Rare | 25 gold | Jewelry, magical items |
| **Wood** | Residential districts | Common | 3 gold | Light items, tools |
| **Water** | All districts | Common | 1 gold | Potions, utility items |
| **Crystals** | Magic districts | Rare | 40 gold | Magical items, status items |

### **Resource Drop Mechanics**

#### **Monster Resource Drops**
```
Base Drop Rate = Monster Type Drop Rate
Level Bonus = Monster Level × 0.5%
Luck Bonus = Player Luck × 0.2%
Final Drop Rate = Base Drop Rate + Level Bonus + Luck Bonus
```

#### **Environmental Resource Spawns**
```
Spawn Chance = District Level × 2% + Random(1, 10%)
Resource Quality = District Level + Random(-2, +2)
Resource Quantity = 1 + Random(0, 2)
```

---

## **CRAFTING TIERS** ⚡

### **Tier Progression**
Crafting follows a clear progression system:

| Tier | Level Requirement | Resource Cost | Success Rate | Quality Bonus |
|-------|------------------|---------------|--------------|---------------|
| **Basic** | Level 1 | Low | 90% | +0% |
| **Apprentice** | Level 10 | Medium | 80% | +10% |
| **Journeyman** | Level 25 | High | 70% | +25% |
| **Expert** | Level 50 | Very High | 60% | +50% |
| **Master** | Level 75 | Extreme | 50% | +100% |
| **Grandmaster** | Level 100 | Maximum | 40% | +200% |

### **Crafting Success Calculation**

#### **Base Success Rate**
```
Base Success = Tier Success Rate
Skill Bonus = Crafting Skill Level × 2%
Quality Bonus = Resource Quality × 1%
Final Success = Base Success + Skill Bonus + Quality Bonus
```

#### **Critical Success**
```
Critical Success Chance = 5% + (Crafting Skill Level × 1%)
Critical Success Bonus = +50% item quality
```

---

## **CRAFTING RECIPES** 📋

### **Recipe Categories**

#### **Weapon Crafting**
- **Basic Weapons**: Simple melee and ranged weapons
- **Enhanced Weapons**: Weapons with special properties
- **Magical Weapons**: Weapons with status effects
- **Unique Weapons**: One-of-a-kind weapons

#### **Armor Crafting**
- **Basic Armor**: Simple protective equipment
- **Enhanced Armor**: Armor with special properties
- **Magical Armor**: Armor with status resistances
- **Unique Armor**: One-of-a-kind armor

#### **Consumable Crafting**
- **Health Potions**: Restore health
- **Mana Potions**: Restore mana
- **Status Potions**: Provide temporary buffs
- **Utility Items**: Tools and special items

#### **Enhancement Crafting**
- **Enhancement Stones**: Improve existing items
- **Transmutation Items**: Change item properties
- **Repair Items**: Fix damaged equipment
- **Special Items**: Unique crafting products

### **Recipe Discovery**

#### **Vendor Recipes**
- **Basic Recipes**: Available from all vendors
- **Advanced Recipes**: Available from specialized vendors
- **Rare Recipes**: Available from master craftsmen
- **Unique Recipes**: Available from special NPCs

#### **Recipe Unlocking**
```
Recipe Level = Player Level + Crafting Skill Level
Recipe Availability = Recipe Level >= Required Level
Recipe Cost = Recipe Tier × 100 gold
```

---

## **CRAFTING VENDORS** 🏪

### **Vendor Types**

#### **General Crafters**
- **Location**: All districts
- **Services**: Basic crafting, repairs, enhancements
- **Specialization**: None (general purpose)
- **Cost**: Standard rates

#### **Specialized Crafters**
- **Location**: Specific districts
- **Services**: Advanced crafting, unique items
- **Specialization**: Weapon, armor, or consumable focus
- **Cost**: Premium rates

#### **Master Craftsmen**
- **Location**: Noble districts only
- **Services**: Master crafting, unique recipes
- **Specialization**: All types with master bonuses
- **Cost**: High rates

### **Vendor Services**

#### **Crafting Services**
```
Base Crafting Cost = Recipe Tier × 50 gold
Material Cost = Sum of all material values
Quality Bonus = +10% for specialized vendors
Master Bonus = +25% for master craftsmen
Final Cost = (Base Crafting Cost + Material Cost) × (1 + Quality Bonus + Master Bonus)
```

#### **Repair Services**
```
Repair Cost = Item Value × 0.1 × Damage Percentage
Quality Bonus = +5% for specialized vendors
Master Bonus = +10% for master craftsmen
```

#### **Enhancement Services**
```
Enhancement Cost = Item Value × 0.5 × Enhancement Level
Quality Bonus = +15% for specialized vendors
Master Bonus = +30% for master craftsmen
```

---

## **CRAFTING MECHANICS** ⚙️

### **Crafting Process**

#### **Recipe Selection**
- **Available Recipes**: Based on player level and crafting skill
- **Material Requirements**: Check if player has required materials
- **Cost Calculation**: Calculate total crafting cost
- **Success Rate**: Calculate final success probability

#### **Crafting Execution**
```
Crafting Roll = Random(1, 100)
Success = Crafting Roll <= Final Success Rate
Critical Success = Crafting Roll <= Critical Success Chance
```

#### **Result Calculation**
```
Base Quality = Recipe Base Quality
Skill Bonus = Crafting Skill Level × 2%
Quality Bonus = Resource Quality × 1%
Critical Bonus = +50% if critical success
Final Quality = Base Quality × (1 + Skill Bonus + Quality Bonus + Critical Bonus)
```

### **Crafting Failures**

#### **Failure Types**
- **Complete Failure**: Item is destroyed, materials lost
- **Partial Failure**: Item created with reduced quality
- **Material Loss**: Some materials are consumed but no item created

#### **Failure Recovery**
```
Material Recovery = 50% of material value
Gold Recovery = 25% of crafting cost
Failure Cooldown = 1 hour before retry
```

---

## **ENHANCEMENT SYSTEM** ⬆️

### **Enhancement Types**

#### **Stat Enhancements**
- **Attribute Bonuses**: Increase item attributes
- **Damage Bonuses**: Increase weapon damage
- **Defense Bonuses**: Increase armor defense
- **Utility Bonuses**: Add special properties

#### **Quality Enhancements**
- **Durability**: Increase item durability
- **Rarity**: Increase item rarity tier
- **Special Effects**: Add unique abilities
- **Set Bonuses**: Add set item properties

### **Enhancement Mechanics**

#### **Enhancement Success**
```
Base Success = 80% - (Enhancement Level × 10%)
Skill Bonus = Enhancement Skill Level × 2%
Quality Bonus = Item Quality × 1%
Final Success = Base Success + Skill Bonus + Quality Bonus
```

#### **Enhancement Failure**
```
Failure Penalty = Enhancement Level × 5%
Item Degradation = Random(1, Failure Penalty)
Material Loss = 100% of enhancement materials
```

---

## **RESOURCE ECONOMY** 💰

### **Resource Value Calculation**

#### **Base Value**
```
Base Value = Resource Type Base Value
Quality Multiplier = Resource Quality / 10
Level Bonus = Resource Level × 0.5
Final Value = Base Value × Quality Multiplier + Level Bonus
```

#### **Market Fluctuations**
```
Supply Factor = Available Resources / Demand
Price Multiplier = 1 + (Supply Factor - 1) × 0.5
Final Price = Base Value × Price Multiplier
```

### **Resource Trading**

#### **Player-to-Player Trading**
- **Direct Trading**: Face-to-face resource exchange
- **Auction House**: Public resource marketplace
- **Guild Trading**: Guild-only resource exchange
- **Vendor Trading**: Sell resources to NPCs

#### **Trading Mechanics**
```
Trade Tax = 5% of transaction value
Guild Discount = -2% for guild members
Bulk Discount = -1% per 10 items
Final Cost = Base Cost × (1 + Trade Tax - Guild Discount - Bulk Discount)
```

---

## **CRAFTING SKILLS** 📚

### **Skill Progression**

#### **Skill Experience**
```
Crafting XP = Recipe Tier × 10 + Item Quality
Skill Level = Floor(Crafting XP / 100)
Skill Bonus = Skill Level × 2%
```

#### **Skill Specializations**
- **Weapon Crafting**: Specialized in weapon creation
- **Armor Crafting**: Specialized in armor creation
- **Consumable Crafting**: Specialized in potion creation
- **Enhancement Crafting**: Specialized in item improvement

### **Skill Bonuses**

#### **Crafting Bonuses**
```
Success Bonus = Skill Level × 2%
Quality Bonus = Skill Level × 1%
Critical Bonus = Skill Level × 0.5%
Cost Reduction = Skill Level × 1%
```

#### **Specialization Bonuses**
```
Specialization Bonus = +10% for specialized crafting
Master Bonus = +25% for master level crafting
Expert Bonus = +50% for expert level crafting
```

---

## **UNIQUE CRAFTING** ⭐

### **Unique Item Creation**

#### **Requirements**
- **Master Level**: Crafting skill level 75+
- **Unique Materials**: Rare materials from unique monsters
- **Special Recipe**: Unique recipes from achievements
- **High Cost**: Expensive crafting process

#### **Unique Item Properties**
- **Unique Abilities**: Special abilities not available elsewhere
- **High Quality**: Maximum quality and durability
- **Set Compatibility**: Can be used in custom sets
- **Tradable**: Can be traded to other players

### **Unique Crafting Process**

#### **Material Gathering**
```
Unique Material = Unique Monster Drop (100% chance)
Rare Material = High-level monster drops (5% chance)
Special Material = Achievement rewards
```

#### **Crafting Process**
```
Unique Success Rate = 25% + (Crafting Skill Level × 1%)
Unique Quality Bonus = +200% quality
Unique Cost = Standard Cost × 5
```

---

## **TECHNICAL SPECIFICATIONS** 🔧

### **API Reference**

#### **Core Crafting Methods**

##### `craft_item(recipe_id: str, materials: List[str], player_level: int, crafting_skill: int) -> Dict`
Crafts an item using the specified recipe and materials.

**Parameters:**
- `recipe_id`: Unique identifier for the recipe
- `materials`: List of material IDs to use
- `player_level`: Level of the player
- `crafting_skill`: Crafting skill level of the player

**Returns:**
- `Dict`: Crafting result with success status and item data

**Mathematical Implementation:**
```python
def craft_item(recipe_id, materials, player_level, crafting_skill):
    # Get recipe data
    recipe = get_recipe_data(recipe_id)
    
    # Check material requirements
    if not check_material_requirements(recipe, materials):
        return {'success': False, 'error': 'Insufficient materials'}
    
    # Calculate success rate
    base_success = recipe['success_rate']
    skill_bonus = crafting_skill * 2
    quality_bonus = calculate_material_quality(materials) * 1
    final_success = base_success + skill_bonus + quality_bonus
    
    # Roll for success
    roll = random.randint(1, 100)
    success = roll <= final_success
    critical = roll <= (5 + crafting_skill * 1)
    
    if success:
        # Calculate item quality
        base_quality = recipe['base_quality']
        skill_bonus = crafting_skill * 2
        quality_bonus = calculate_material_quality(materials) * 1
        critical_bonus = 50 if critical else 0
        final_quality = base_quality * (1 + skill_bonus + quality_bonus + critical_bonus)
        
        return {
            'success': True,
            'critical': critical,
            'item_quality': final_quality,
            'item_data': generate_crafted_item(recipe, final_quality)
        }
    else:
        return {
            'success': False,
            'materials_lost': calculate_material_loss(materials)
        }
```

##### `calculate_crafting_cost(recipe_id: str, materials: List[str], vendor_type: str) -> float`
Calculates the total cost for crafting an item.

**Parameters:**
- `recipe_id`: Unique identifier for the recipe
- `materials`: List of material IDs to use
- `vendor_type`: Type of vendor ('general', 'specialized', 'master')

**Returns:**
- `float`: Total crafting cost

##### `enhance_item(item_id: str, enhancement_type: str, player_level: int) -> Dict`
Enhances an existing item with new properties.

**Parameters:**
- `item_id`: Unique identifier for the item
- `enhancement_type`: Type of enhancement to apply
- `player_level`: Level of the player

**Returns:**
- `Dict`: Enhancement result with success status and updated item data

---

## **PERFORMANCE CONSIDERATIONS** ⚡

### **Optimization Strategies**
- **Recipe Caching**: Cache frequently used recipe data
- **Batch Processing**: Process multiple crafting operations simultaneously
- **Memory Management**: Efficient data structures for crafting data
- **Network Optimization**: Minimal data transfer for crafting updates

### **Scalability Features**
- **Dynamic Loading**: Load recipe data on demand
- **Compression**: Compress crafting data for storage
- **Indexing**: Fast lookup for recipes and materials
- **Garbage Collection**: Automatic cleanup of unused crafting data

---

## **FUTURE ENHANCEMENTS** 🚀

### **Planned Features**
- **Advanced Crafting**: More complex crafting mechanics
- **Crafting Guilds**: Player-run crafting organizations
- **Seasonal Crafting**: Limited-time special crafting events
- **Crafting Competitions**: Competitive crafting challenges

### **Technical Improvements**
- **Real-time Updates**: Live crafting progress visualization
- **Advanced Analytics**: Detailed crafting success analysis
- **Visual Enhancements**: Improved crafting interface
- **Mobile Integration**: Cross-platform crafting management

---

## **TROUBLESHOOTING** 🔧

### **Common Issues**
- **Crafting Calculation Errors**: Verify recipe and material formulas
- **Success Rate Bugs**: Check crafting success calculation logic
- **Performance Issues**: Monitor crafting calculation complexity
- **Data Corruption**: Validate crafting data integrity

### **Debug Tools**
- **Crafting Calculator**: Test crafting scenarios
- **Success Rate Checker**: Verify crafting success calculations
- **Material Simulator**: Test material requirement logic
- **Cost Analyzer**: Monitor crafting cost calculations

---

*The Crafting & Resource System provides the foundation for item creation and economic progression in Chronicles of Ruin: Sunderfall, offering deep customization while maintaining accessibility for all players.*

# Chronicles of Ruin - Gambling System Mathematics

## **📊 DAMAGE CALCULATION FORMULAS**

### **Step 1: Base Damage Calculation**

```
Base Damage = (All Positive Bonuses) - (All Negative Bonuses)
```

**Example:**

- Power: +8 damage
- Weapon: +12 damage
- Skill: +5 damage
- Cursed Ring: -3 damage
- Debuff: -2 damage

**Calculation:**

```
Positive: 8 + 12 + 5 = 25
Negative: 3 + 2 = 5
Base Damage = 25 - 5 = 20
```

### **Step 2: Apply Percentage Modifiers**

```
Modified Damage = Base Damage × (1 + Total Percentage Bonuses)
```

**Example:**

- Base Damage: 20
- Fire Damage: +15%
- Weapon Enchant: +10%
- Set Bonus: +25%

**Calculation:**

```
Total Percentage = 0.15 + 0.10 + 0.25 = 0.50 (50%)
Modified Damage = 20 × (1 + 0.50) = 20 × 1.50 = 30
```

### **Step 3: Combat Triangle Multiplier**

```
Final Damage = Modified Damage × Triangle Multiplier
```

**Example:**

- Modified Damage: 30
- Melee vs Ranged: +25% bonus

**Calculation:**

```
Final Damage = 30 × 1.25 = 37.5
```

### **Complete Example:**

```
Your stats: 2+3-1+5-3+8-1
Positive: 2+3+5+8 = 18
Negative: 1+3+1 = 5
Base: 18-5 = 13

With +20% gear bonus:
Modified: 13 × 1.20 = 15.6

Against weak enemy (+25%):
Final: 15.6 × 1.25 = 19.5 damage
```

---

## **🎰 GAMBLING TAX SYSTEM**

### **Base Reroll Cost Formula**

```
Base Cost = 100 × Number of Pieces
```

**Examples:**

- 2-piece set: 200 gold
- 4-piece set: 400 gold
- 6-piece set: 600 gold
- 10-piece set: 1,000 gold

### **Escalation Multiplier**

```
Escalation Cost = Base Cost × (2^Reroll Count)
```

**6-Piece Set Example:**

- Reroll #1: 600 × (2^0) = 600 × 1 = **600 gold**
- Reroll #2: 600 × (2^1) = 600 × 2 = **1,200 gold**
- Reroll #3: 600 × (2^2) = 600 × 4 = **2,400 gold**
- Reroll #4: 600 × (2^3) = 600 × 8 = **4,800 gold**
- Reroll #5: 600 × (2^4) = 600 × 16 = **9,600 gold**

### **Gambling Tax Per Piece**

```
Each Reroll Adds: 0.001% to 0.01% tax per piece
Tax Range: 0.00001 to 0.0001 (as decimal)
```

**Random Tax Examples:**

- Helmet: +0.0034%
- Chest: +0.0078%
- Gloves: +0.0012%
- Boots: +0.0056%
- Weapon: +0.0089%
- Shield: +0.0023%

### **Total Tax Calculation**

```
Total Tax = Sum of all piece taxes
Tax Multiplier = 1 + Total Tax
Final Cost = Escalation Cost × Tax Multiplier
```

### **Complete Gambling Example**

**"Fire Lord's Regalia" - 6-piece set:**

**Initial State:**

- Base Cost: 600 gold
- Gambling Tax: 0% on all pieces

**After 1st Reroll:**

- Escalation: 600 × 2^1 = 1,200 gold
- New taxes applied:
  - Helmet: +0.0045%
  - Chest: +0.0067%
  - Gloves: +0.0023%
  - Boots: +0.0034%
  - Weapon: +0.0089%
  - Shield: +0.0012%
- Total Tax: 0.0270% = 0.00027
- **Cost: 1,200 × 1.00027 = 1,200.32 gold**

**After 2nd Reroll:**

- Escalation: 600 × 2^2 = 2,400 gold
- Additional taxes:
  - Helmet: 0.0045% + 0.0056% = 0.0101%
  - Chest: 0.0067% + 0.0078% = 0.0145%
  - Gloves: 0.0023% + 0.0034% = 0.0057%
  - Boots: 0.0034% + 0.0067% = 0.0101%
  - Weapon: 0.0089% + 0.0045% = 0.0134%
  - Shield: 0.0012% + 0.0089% = 0.0101%
- Total Tax: 0.0639% = 0.000639
- **Cost: 2,400 × 1.000639 = 2,401.53 gold**

**After 5th Reroll:**

- Escalation: 600 × 2^5 = 19,200 gold
- Accumulated taxes (example):
  - Total Tax: ~0.25% = 0.0025
- **Cost: 19,200 × 1.0025 = 19,248 gold**

**After 10th Reroll:**

- Escalation: 600 × 2^10 = 614,400 gold
- Accumulated taxes (example):
  - Total Tax: ~1.2% = 0.012
- **Cost: 614,400 × 1.012 = 621,773 gold**

---

## **💸 GAMBLING PROGRESSION TABLE**

| Reroll # | Base (6pc) | Escalation | Tax Example | Final Cost |
| -------- | ---------- | ---------- | ----------- | ---------- |
| 0        | 600        | 600        | 0%          | 600        |
| 1        | 600        | 1,200      | 0.03%       | 1,200      |
| 2        | 600        | 2,400      | 0.06%       | 2,401      |
| 3        | 600        | 4,800      | 0.12%       | 4,806      |
| 4        | 600        | 9,600      | 0.18%       | 9,617      |
| 5        | 600        | 19,200     | 0.25%       | 19,248     |
| 6        | 600        | 38,400     | 0.35%       | 38,534     |
| 7        | 600        | 76,800     | 0.47%       | 77,161     |
| 8        | 600        | 153,600    | 0.62%       | 154,553    |
| 9        | 600        | 307,200    | 0.84%       | 309,780    |
| 10       | 600        | 614,400    | 1.20%       | 621,773    |

---

## **🎲 PROBABILITY BREAKDOWN**

### **Tax Range Per Piece**

- **Minimum**: 0.001% (0.00001)
- **Maximum**: 0.01% (0.0001)
- **Average**: 0.0055% (0.000055)

### **6-Piece Set Tax Accumulation**

- **Per Reroll Minimum**: 6 × 0.001% = 0.006%
- **Per Reroll Maximum**: 6 × 0.01% = 0.06%
- **Per Reroll Average**: 6 × 0.0055% = 0.033%

### **After 10 Rerolls (Worst Case)**

- **Maximum Possible Tax**: 10 × 0.06% = 0.6%
- **Cost at Reroll 10**: 614,400 × 1.006 = 618,086 gold
- **Best Case Tax**: 10 × 0.006% = 0.06%
- **Cost at Reroll 10**: 614,400 × 1.0006 = 614,769 gold

---

## **⚠️ THE GAMBLING TRAP**

### **Psychological Escalation**

Players will experience this progression:

1. **"Just 600 gold? Easy!"** ✅
2. **"1,200 isn't bad for better bonuses..."** 🤔
3. **"2,400 is steep but I'm invested now..."** 😬
4. **"4,800?! But I've already spent 4,000..."** 😰
5. **"One more roll, it HAS to be good!"** 🎰
6. **"I'm broke but the taxes keep growing..."** 💸

### **Sunk Cost Fallacy**

The exponential cost + permanent taxes create perfect conditions for gambling addiction:

- Each failed reroll makes the next one more expensive
- Players feel they "must" continue to justify previous spending
- The permanent tax means switching sets feels like "losing" all that investment

### **The Tax Visualization**

```
Set: "Nemeca's Fire Build"
Rerolls: 7
Current Cost: 77,161 gold

Gambling Taxes:
  Helmet: +0.0234%
  Chest: +0.0456%
  Gloves: +0.0123%
  Boots: +0.0345%
  Weapon: +0.0567%
  Shield: +0.0189%

Total Tax: +0.1914%
Next Reroll: 154,553 gold
```

This creates the perfect **"just one more roll"** mentality while the taxes grow forever! 😈

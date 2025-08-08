# Chronicles of Ruin Saga

A comprehensive AI-driven game development project featuring an advanced Learning AI Party System for autonomous testing and refinement.

## 🎮 **Learning AI Party System**

### **Core Features**

- **5 AI Players**: Work solo and as a coordinated team
- **Adaptive Learning**: Improve over time through experience
- **Human-like Behavior**: Treat AI players exactly like human players
- **Skill Level Variation**: From "noob" to "master" for diverse testing
- **Autonomous Testing**: Reduce need for human intervention

### **AI Player Capabilities**

- **Emotional Intelligence**: AI players have emotional states (confidence, stress, frustration, excitement, determination)
- **Strategic Depth**: Analyze risk levels, urgency, resource availability, and team coordination needs
- **Pattern Recognition**: Learn from successful and failed strategies
- **Advanced Decision Making**: Generate multiple options with detailed reasoning and confidence levels
- **Adaptive Behavior**: Modify parameters based on performance and game changes

### **Enhanced Learning System**

- **Combat Pattern Learning**: Analyze damage patterns, effective skill combinations, defensive strategies
- **Exploration Pattern Learning**: Learn efficient routes, area discovery, resource gathering
- **Social Pattern Learning**: NPC interactions, quest completion efficiency, reputation building
- **Emotional Pattern Learning**: Stress management, confidence building, frustration handling
- **Advanced Pattern Recognition**: Complex skill combinations, enemy behavior, environmental interactions

## 🎯 **Role System (Guild Wars Style)**

### **Universal Skill Access**

Every player has access to healing, DPS, and damage mitigation skills, but specialization determines effectiveness:

- **Pure Roles (3 points in one specialization)**:

  - `pure_dps`: Maximum damage output, ultimate skill access
  - `pure_support`: Maximum healing and utility, ultimate skill access
  - `pure_tank`: Maximum damage mitigation, ultimate skill access

- **Hybrid Roles (2 points in different specializations)**:

  - `hybrid_dps_support`: Balanced damage and healing
  - `hybrid_dps_tank`: Balanced damage and mitigation
  - `hybrid_support_tank`: Balanced healing and mitigation

- **Support Role (1 point in each specialization)**:
  - `support`: Access to all skill types, largest toolbelt

### **Toolbelt System**

- **Pure Roles**: 3 skill types (Damage, Defense, Support) + Ultimate
- **Hybrid Roles**: 4 skill types (2 primary + 2 secondary)
- **Support Role**: 5 skill types (all types available)

## 🎯 **Skill System**

### **Skill Types**

- **Damage**: Raw damage output skills
- **Defense**: Damage mitigation and protection skills
- **Support**: Healing and utility skills
- **Ultimate**: Powerful skills available only to pure specializations

### **Skill Distribution**

- **9 Regular Skills**: 3 Damage, 3 Defense, 3 Support
- **1 Ultimate Skill**: Available only to pure specializations (3 points in one base)
- **Unique Playstyles**: Each skill has distinct mechanics and effects

### **Archetype Effectiveness**

- **Pure Specializations**: 150% effectiveness in their primary skill type
- **Hybrid Specializations**: 125% effectiveness in their primary types, 100% in secondary
- **Support Role**: 100% effectiveness in all skill types, but largest variety

## 🛡️ **Resistance System**

### **Entity Types**

- **Regular Monsters**: Max ±99% resistance
- **Bosses**: 100% immunity to specific CC, can be slowed
- **Players**: Max ±99% resistance
- **NPCs**: Max ±99% resistance

### **Boss Immunities**

- **Immune to**: Stun, Freeze, and most crowd control
- **Vulnerable to**: Slow effects, damage over time, damage reductions
- **Resistance Application**: Applied to BASE damage, not modified damage

### **Damage Calculation**

1. Calculate base damage from stats and skills
2. Apply resistance to base damage
3. Apply other modifiers (combat triangle, items, etc.)
4. Apply damage floor

## 📈 **Progression System**

### **Chapter 1 Content**

- **25 Quests**: 10 story, 6 side, 3 exploration, 2 combat, 2 crafting, 2 social
- **17 Areas**: 4 town, 6 forest, 6 ruins, 1 boss arena
- **Story Progression**: 4 acts from village to corruption heart
- **Level Progression**: Start at level 1, progress through Chapter 1

### **Quest Types**

- **Story Quests**: Main narrative progression
- **Side Quests**: Optional content and world building
- **Exploration Quests**: Area discovery and lore
- **Combat Quests**: Training and combat challenges
- **Crafting Quests**: Item creation and resource gathering
- **Social Quests**: NPC interactions and relationships

### **Area Types**

- **Town Areas**: Safe zones with NPCs and services
- **Forest Areas**: Wilderness with corrupted creatures
- **Ruins Areas**: Ancient civilization remains
- **Boss Arena**: Special areas for boss encounters

## 🔧 **Development Tools**

### **Master Development Script**

```bash
python dev_master.py [command] [options]
```

### **Available Commands**

- `ai-playtest`: Run AI playtest with detailed logging
- `ai-playtest-adaptive`: Run adaptive AI testing with learning
- `ai-party`: Test the Learning AI Party System
- `demo`: Quick demonstration of AI capabilities
- `performance`: Monitor system performance and AI learning
- `build`: Build and test the game systems
- `test`: Run comprehensive test suite

### **AI Learning Session System**

- **Realistic Game Simulation**: Combat, quests, exploration, boss encounters
- **Comprehensive Analytics**: Performance tracking, learning insights, adaptation metrics
- **Campaign Mode**: Multiple sessions for long-term learning analysis

## 📊 **Performance Monitoring**

### **Enhanced Analytics**

- **System Performance**: CPU, GPU, memory, temperatures, network I/O
- **AI Learning Metrics**: Decision success rates, combat analytics, adaptation patterns
- **Combat Analytics**: Skill effectiveness, boss encounter data, strategy success rates
- **Learning Insights**: Pattern recognition, emotional state analysis, strategic depth

### **Real-time Monitoring**

- **Per-second Tracking**: Detailed resource usage over time
- **Thermal Monitoring**: CPU and GPU temperature tracking
- **AI Decision Logging**: Full prompts, responses, and reasoning
- **Combat Analysis**: Damage patterns, skill usage, status effect success

## 🚀 **Quick Start**

### **Setup**

```bash
# Clone the repository
git clone https://github.com/Nemeca99/Chronicles-of-Ruin.git
cd Chronicles-of-Ruin

# Install dependencies
pip install -r requirements.txt

# Run AI playtest
python dev_master.py ai-playtest

# Test AI party system
python dev_master.py ai-party

# Monitor performance
python dev_master.py performance
```

### **AI Learning Campaign**

```bash
# Run comprehensive AI learning campaign
python dev_master.py ai-playtest-adaptive --test-sessions 10

# Monitor AI learning progress
python dev_master.py performance --export-report
```

## 📁 **Project Structure**

```
Chronicles_of_Ruin/
├── tools/                          # Development tools
│   ├── ai_player_system.py        # AI player management
│   ├── ai_playtest_tool.py        # AI playtest orchestration
│   ├── performance_monitor.py     # Enhanced performance monitoring
│   └── dev_master.py              # Master development CLI
├── chapters/
│   └── chapter_01_sunderfall/     # Chapter 1 content
│       ├── src/systems/           # Game systems
│       │   ├── skills_system.py   # Guild Wars-style skills
│       │   ├── resistance_system.py # Resistance and immunities
│       │   ├── progression_system.py # Quest and area progression
│       │   ├── combat_system.py   # Enhanced combat with resistance
│       │   └── ai_learning_session.py # AI learning orchestration
│       ├── data/                  # Game data
│       │   ├── skills.json        # Skill definitions
│       │   ├── quests.json        # Quest definitions
│       │   ├── areas.json         # Area definitions
│       │   └── player_progress.json # AI player progress
│       └── lore/                  # Story and lore
│           └── chapter_01_lore_and_story.md
└── docs/                          # Documentation
    └── README.md                  # Documentation index
```

## 🎯 **Current Development Focus**

### **AI Learning Enhancement**

- **Emotional Intelligence**: AI players now analyze their emotional state and adjust decisions accordingly
- **Strategic Depth**: Advanced analysis of risk, urgency, resources, and team coordination
- **Pattern Recognition**: Learning from historical successes and failures
- **Enhanced Decision Making**: Multiple options with detailed reasoning and confidence levels

### **Combat System Integration**

- **Resistance System**: Full integration with boss immunities and damage calculation
- **Status Effects**: Enhanced status effect system with boss immunity handling
- **Combat Analytics**: Detailed analysis for AI learning and skill effectiveness tracking
- **Boss Encounters**: Special handling for boss mechanics and learning

### **Performance Monitoring**

- **AI Learning Analytics**: Track decision success rates, combat patterns, adaptation metrics
- **Comprehensive Reporting**: Generate detailed insights and recommendations
- **Real-time Monitoring**: Per-second tracking of system resources and AI performance
- **Export Capabilities**: Generate full analytics reports for analysis

## 🤝 **Contributing**

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on contributing to the project.

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Current Status**: Enhanced AI learning system with emotional intelligence and strategic depth. Combat system fully integrated with resistance mechanics. Performance monitoring provides comprehensive analytics. Chapter 1 content expanded with 25 quests across 17 areas. Ready for autonomous testing and refinement.

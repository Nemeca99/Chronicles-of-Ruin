# Chronicles of Ruin

A revolutionary RPG game development framework featuring **AI Learning Party Systems** for automated testing and game balance evaluation.

![Chronicles of Ruin](https://img.shields.io/badge/Status-Active%20Development-brightgreen)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![AI Testing](https://img.shields.io/badge/AI%20Testing-Learning%20Party%20System-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## 🎮 Overview

Chronicles of Ruin is a multi-chapter RPG saga with an innovative **AI Learning Party System** that creates intelligent playtesters that learn, adapt, and work together like human players. This system enables automated game testing, balance evaluation, and continuous improvement without manual intervention.

## 🚀 Key Features

### 🤖 AI Learning Party System

- **5-Player Teams** with different skill levels (noob to master)
- **Adaptive Learning** - AI players learn from decisions and adapt strategies
- **Team Dynamics** - Players work together with roles (tank, dps, support, healer)
- **Skill Progression** - AI players can level up and improve over time
- **Performance Monitoring** - Real-time CPU/GPU usage and thermal tracking

### 🎯 Game Development Tools

- **Automated Testing** - AI players test your game 24/7
- **Balance Evaluation** - Detailed feedback on game mechanics
- **Performance Profiling** - System resource monitoring during gameplay
- **Cross-Chapter Features** - Shared save data and achievements

### 🛠️ Development Infrastructure

- **CLI Tools** - Comprehensive command-line interface for all development tasks
- **Modular Architecture** - Self-contained chapters with shared utilities
- **Database Integration** - SQLite for cross-chapter features
- **Testing Framework** - Automated testing with pytest integration

## 📁 Project Structure

```
Chronicles_of_Ruin/
├── chapters/                    # Individual game chapters
│   └── chapter_01_sunderfall/  # First chapter implementation
├── tools/                      # Development tools and utilities
│   ├── ai_playtest_tool.py     # AI playtesting system
│   ├── ai_player_system.py     # AI player management
│   ├── performance_monitor.py  # System performance tracking
│   └── dev_master.py          # Master CLI interface
├── docs/                       # Comprehensive documentation
├── shared/                     # Cross-chapter resources
├── tests/                      # Test suites
└── venv/                      # Python virtual environment
```

## 🎯 AI Learning Party System

### Party Composition

- **Alex** (Noob Pure DPS) - Maximum damage output, low self-sufficiency
- **Sam** (Casual Hybrid DPS) - Balanced damage with utility, moderate self-sufficiency
- **Jordan** (Experienced Support) - Team utility and healing, good self-sufficiency
- **Casey** (Expert Hybrid Support) - Healing with utility, high self-sufficiency
- **Riley** (Master Pure Support) - Maximum healing and survival, very high self-sufficiency

#### Team Roles

- **Pure DPS** - Maximum damage output, rely on team for survival
- **Hybrid DPS** - Balanced damage with utility, moderate self-sufficiency
- **Support** - Team utility and healing, good self-sufficiency
- **Hybrid Support** - Healing with utility, high self-sufficiency
- **Pure Support** - Maximum healing and survival, very high self-sufficiency

### Role System (Guild Wars Style)

**Everyone has access to healing, DPS, and damage mitigation - specialization determines effectiveness:**

- **Pure DPS** - 80% damage, 10% healing, 10% mitigation (1.5x damage multiplier)
- **Hybrid DPS** - 60% damage, 20% healing, 20% mitigation (1.2x damage multiplier)
- **Support** - 30% damage, 40% healing, 30% mitigation (0.8x damage multiplier)
- **Hybrid Support** - 20% damage, 50% healing, 30% mitigation (0.6x damage multiplier)
- **Pure Support** - 10% damage, 60% healing, 30% mitigation (0.4x damage multiplier)

**Toolbelt Size:**
- **Pure roles** (1 skill type) - Maximum specialization, highest effectiveness
- **Hybrid roles** (2 skill types) - Balanced approach, moderate effectiveness
- **Support role** (3 skill types) - Maximum versatility, lowest specialization

### 🎯 Skill System

**Universal Skill Access - Every archetype has access to all skill types:**

#### **Damage Skills (3 skills available to all):**
- **Fireball** - Single target fire damage with burning effect
- **Lightning Strike** - Area lightning damage with shock effect  
- **Shadow Daggers** - Armor-piercing single target damage

#### **Defense Skills (3 skills available to all):**
- **Stone Skin** - Damage reduction and stun resistance
- **Mirror Shield** - Damage reflection and magic resistance
- **Evasion** - Dodge chance and movement speed boost

#### **Support Skills (3 skills available to all):**
- **Healing Light** - Single target healing with regeneration
- **Group Heal** - Area healing for all allies
- **Haste** - Speed boost and attack speed increase

#### **Ultimate Skills (Pure specializations only):**
- **Apocalypse** (Pure DPS) - Massive damage to all enemies
- **Immortality** (Pure Support) - Invulnerability and mass healing

**Skill Effectiveness by Archetype:**
- **Pure DPS** - 2.25x damage multiplier, 20% cooldown reduction
- **Hybrid DPS** - 1.8x damage multiplier, balanced effectiveness
- **Support** - 1.75x damage multiplier, 1.4x healing multiplier
- **Hybrid Support** - 1.6x damage multiplier, 1.5x healing multiplier
- **Pure Support** - 1.55x damage multiplier, 1.6x healing multiplier, 20% cooldown reduction

### Learning Capabilities

- **Success Rate Tracking** - Monitors decision outcomes
- **Strategy Memory** - Remembers successful approaches
- **Failure Pattern Recognition** - Avoids unsuccessful strategies
- **Adaptation Thresholds** - Changes strategies when needed
- **Team Coordination** - Improves teamwork over time

## 🚀 Quick Start

### Prerequisites

- Python 3.12
- Git
- Ollama (for AI model integration)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Nemeca99/Chronicles-of-Ruin.git
   cd Chronicles-of-Ruin
   ```

2. **Set up virtual environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize development environment**
   ```bash
   python setup_dev.py
   ```

### Running AI Playtests

1. **Enhanced AI Playtest** (with full thinking process)

   ```bash
   venv\Scripts\python.exe tools\dev_master.py ai-playtest-enhanced Alex --verbose
   ```

2. **Learning Party Session** (5-player team)

   ```bash
   venv\Scripts\python.exe tools\dev_master.py ai-playtest-learning-party
   ```

3. **Adaptive Testing** (multiple sessions)

   ```bash
   venv\Scripts\python.exe tools\dev_master.py ai-playtest-adaptive 5
   ```

4. **Demo the Learning System**
   ```bash
   venv\Scripts\python.exe tools\ai_playtest_tool.py demo
   ```

## 🛠️ Development Commands

### Master CLI Interface

```bash
# AI Playtesting
ai-playtest-quick <player>              # Quick test
ai-playtest-comprehensive <player>       # Comprehensive test
ai-playtest-compare <players> <scenarios> # Compare players
ai-playtest-enhanced <player> [scenarios] # Enhanced with thinking process
ai-playtest-learning-party [scenarios]   # 5-player learning party
ai-playtest-adaptive [sessions] [scenarios] # Adaptive testing

# Performance Monitoring
performance-start [session_name]         # Start monitoring
performance-stop                         # Stop monitoring
performance-summary                      # Get summary

# AI Player Management
ai-player-create-profile <name> <params> # Create AI player
ai-player-samples                        # Create sample players
ai-player-list                           # List all players
```

### Available Scenarios

- `character_creation` - Character building and customization
- `combat_test` - Combat system evaluation
- `skill_allocation` - Skill tree and progression testing
- `exploration_test` - World exploration and discovery
- `full_gameplay` - Complete game session simulation

## 📊 Performance Monitoring

The system includes comprehensive performance monitoring:

- **CPU Usage** - Real-time CPU utilization tracking
- **GPU Monitoring** - GPU usage, temperature, and power draw
- **Memory Tracking** - RAM usage and memory patterns
- **Thermal Monitoring** - CPU and GPU temperature logging
- **Network I/O** - Network activity monitoring
- **Performance Trends** - Analysis of system stress over time

## 🎮 Game Systems

### Core Systems

- **Combat System** - Turn-based tactical combat
- **Character Progression** - Leveling, skills, and abilities
- **Quest System** - Dynamic quest generation and tracking
- **Economy System** - Trading, crafting, and resource management
- **Monster System** - AI-driven enemy behavior
- **World System** - Dynamic environment and exploration

### Advanced Features

- **Achievement System** - Cross-chapter progression tracking
- **Multiplayer Foundation** - Social features and team coordination
- **UI/UX System** - Modern, responsive interface design
- **Status Effects** - Elemental and magical status systems
- **Itemization** - Comprehensive item and equipment system

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **System Documentation** - Detailed technical specifications
- **Implementation Guides** - Step-by-step development guides
- **API Reference** - Code documentation and examples
- **Testing Documentation** - QA procedures and test cases

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **AI Integration** - Powered by Ollama and local language models
- **Performance Monitoring** - Advanced system resource tracking
- **Game Development** - Comprehensive RPG framework
- **Testing Automation** - Intelligent AI playtesting system

## 📞 Support

- **Issues** - Report bugs and request features on GitHub
- **Discussions** - Join community discussions
- **Documentation** - Comprehensive guides and tutorials

---

**Chronicles of Ruin** - Where AI meets game development, creating the future of automated testing and intelligent game design.

_Built with ❤️ and 🤖_

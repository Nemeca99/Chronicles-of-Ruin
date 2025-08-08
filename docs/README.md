# Chronicles of Ruin Documentation

Welcome to the comprehensive documentation for Chronicles of Ruin. This directory contains detailed technical documentation for all systems and components.

## 📚 Documentation Index

### 🎮 Game Systems

#### Core Systems
- **[Combat System](combat_system.md)** - Turn-based tactical combat mechanics
- **[Character Progression](character_progression_system.md)** - Leveling, skills, and abilities
- **[Quest System](quest_progression_system.md)** - Dynamic quest generation and tracking
- **[Economy System](economy_trading_system.md)** - Trading, crafting, and resource management
- **[Monster System](monster_system_detailed.md)** - AI-driven enemy behavior
- **[World System](world_environment_system.md)** - Dynamic environment and exploration

#### Advanced Systems
- **[Achievement System](achievement_progression_system.md)** - Cross-chapter progression tracking
- **[Multiplayer System](multiplayer_social_system.md)** - Social features and team coordination
- **[UI/UX System](ui_ux_system.md)** - Modern, responsive interface design
- **[Status Effects](status_elemental_system.md)** - Elemental and magical status systems
- **[Itemization](itemization_system.md)** - Comprehensive item and equipment system
- **[Crafting System](crafting_resource_system.md)** - Resource gathering and crafting mechanics

### 🤖 AI Systems

#### AI Player Management
- **[AI Player System](ai_player_system.md)** - AI player profiles and decision-making
- **[AI Learning Party](ai_learning_party_system.md)** - 5-player team dynamics and learning
- **[AI Playtesting](ai_playtesting_system.md)** - Automated game testing and balance evaluation

#### AI Integration
- **[AI Decision Making](ai_decision_making.md)** - How AI players make decisions
- **[AI Learning Algorithms](ai_learning_algorithms.md)** - Machine learning for game adaptation
- **[AI Team Dynamics](ai_team_dynamics.md)** - Team coordination and role-based behavior

### 🛠️ Development Tools

#### Core Tools
- **[Master CLI](dev_master_cli.md)** - Comprehensive command-line interface
- **[Build System](build_system.md)** - Automated building and testing
- **[Performance Monitor](performance_monitor.md)** - System resource tracking
- **[AI Playtest Tool](ai_playtest_tool.md)** - AI testing and evaluation

#### Development Infrastructure
- **[Technical Architecture](technical_architecture_system.md)** - System architecture overview
- **[Performance System](technical_architecture_performance_system.md)** - Performance optimization
- **[Testing Framework](testing_quality_assurance_system.md)** - QA procedures and test cases
- **[Implementation Roadmap](implementation_roadmap.md)** - Development timeline and milestones

### 📊 Game Design

#### Design Framework
- **[Game Design Framework](game_design_framework.md)** - Core design principles and philosophy
- **[Class System](class_system.md)** - Character classes and specializations
- **[Archetype System](archetype_system.md)** - Character archetypes and roles
- **[Skills System](skills_system.md)** - Skill trees and progression
- **[Items System](items_system.md)** - Equipment and item management

#### Content Systems
- **[Monster Database](monster_database.md)** - Enemy types and behaviors
- **[Combat Mechanics](combat_system_detailed.md)** - Detailed combat system
- **[Skill Progression](skill_system_detailed.md)** - Advanced skill system
- **[Testing QA](testing_qa_system.md)** - Quality assurance procedures

### 📈 Project Status

#### Completed Systems
- **[Database Setup](DATABASE_SETUP_COMPLETE.md)** - Database implementation status
- **[Project Reorganization](PROJECT_REORGANIZATION_COMPLETE.md)** - Project structure updates
- **[Autonomous Testing](AUTONOMOUS_TESTING_COMPLETE.md)** - AI testing implementation
- **[Alignment and Enhancements](ALIGNMENT_AND_ENHANCEMENTS_COMPLETE.md)** - System alignment status

### 🚀 Quick Reference

#### Common Commands
```bash
# AI Playtesting
venv\Scripts\python.exe tools\dev_master.py ai-playtest-enhanced Alex --verbose
venv\Scripts\python.exe tools\dev_master.py ai-playtest-learning-party
venv\Scripts\python.exe tools\dev_master.py ai-playtest-adaptive 5

# Performance Monitoring
venv\Scripts\python.exe tools\dev_master.py performance-start session_name
venv\Scripts\python.exe tools\dev_master.py performance-stop
venv\Scripts\python.exe tools\dev_master.py performance-summary

# Development
venv\Scripts\python.exe tools\dev_master.py build-all
venv\Scripts\python.exe tools\dev_master.py run-chapter chapter_01_sunderfall
```

#### AI Player Types
- **Noob** - Cautious, defensive, learns slowly
- **Casual** - Impulsive, aggressive, moderate learning
- **Experienced** - Impulsive, aggressive, good learning
- **Expert** - Strategic, balanced, fast learning
- **Master** - Strategic, defensive, fastest learning

#### Team Roles
- **Tank** - Protection and aggro management
- **DPS** - Damage output and aggression
- **Support** - Buffing and utility
- **Healer** - Healing and survival

### 📖 Reading Order

For new developers:

1. **Start with** [Game Design Framework](game_design_framework.md) to understand the project philosophy
2. **Read** [Technical Architecture](technical_architecture_system.md) for system overview
3. **Explore** [AI Learning Party System](ai_learning_party_system.md) for the unique AI features
4. **Review** [Implementation Roadmap](implementation_roadmap.md) for development timeline
5. **Check** [Testing Framework](testing_quality_assurance_system.md) for quality procedures

For AI system developers:

1. **Begin with** [AI Player System](ai_player_system.md) for core AI concepts
2. **Study** [AI Learning Algorithms](ai_learning_algorithms.md) for learning mechanisms
3. **Review** [AI Team Dynamics](ai_team_dynamics.md) for team behavior
4. **Explore** [AI Playtesting](ai_playtesting_system.md) for testing capabilities

For game developers:

1. **Start with** [Combat System](combat_system.md) for core gameplay
2. **Review** [Character Progression](character_progression_system.md) for player advancement
3. **Explore** [World System](world_environment_system.md) for environment design
4. **Check** [Quest System](quest_progression_system.md) for content creation

---

*This documentation is continuously updated as the project evolves. For the latest information, check the main [README.md](../README.md) in the project root.*

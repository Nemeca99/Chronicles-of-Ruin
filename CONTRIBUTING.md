# Contributing to Chronicles of Ruin

Thank you for your interest in contributing to Chronicles of Ruin! This document provides guidelines for contributing to the project.

## 🎯 Project Overview

Chronicles of Ruin is a revolutionary RPG game development framework featuring AI Learning Party Systems for automated testing and game balance evaluation. We welcome contributions that enhance the AI testing capabilities, improve game systems, or add new features.

## 🤝 How to Contribute

### Types of Contributions

We welcome the following types of contributions:

- **AI System Enhancements** - Improve the AI learning algorithms, add new AI player types, or enhance team dynamics
- **Game Systems** - Add new game mechanics, improve existing systems, or fix bugs
- **Performance Monitoring** - Enhance system monitoring capabilities or add new metrics
- **Documentation** - Improve documentation, add tutorials, or create guides
- **Testing** - Add new test scenarios, improve test coverage, or enhance the testing framework
- **Tools and Utilities** - Create new development tools or improve existing ones

### Development Setup

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Chronicles-of-Ruin.git
   cd Chronicles-of-Ruin
   ```

2. **Set up the development environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   python setup_dev.py
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes**
   - Follow the coding standards below
   - Add tests for new functionality
   - Update documentation as needed

5. **Test your changes**
   ```bash
   # Run the AI playtest system
   venv\Scripts\python.exe tools\dev_master.py ai-playtest-enhanced Alex --verbose
   
   # Run the learning party demo
   venv\Scripts\python.exe tools\ai_playtest_tool.py demo
   
   # Run performance monitoring
   venv\Scripts\python.exe tools\dev_master.py performance-start test_session
   ```

6. **Submit a pull request**
   - Provide a clear description of your changes
   - Include any relevant test results
   - Reference any related issues

## 📋 Coding Standards

### Python Code

- **Python 3.12** - Use Python 3.12 features and syntax
- **Type Hints** - Use type hints for all function parameters and return values
- **Docstrings** - Include comprehensive docstrings for all functions and classes
- **Error Handling** - Use proper exception handling with meaningful error messages
- **Logging** - Use structured logging for debugging and monitoring

### Code Style

- **PEP 8** - Follow PEP 8 style guidelines
- **Line Length** - Keep lines under 120 characters
- **Naming** - Use descriptive names for variables, functions, and classes
- **Comments** - Add comments for complex logic or non-obvious code

### Example Code Structure

```python
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ExampleSystem:
    """Example system demonstrating coding standards."""
    
    def __init__(self, config_path: Path) -> None:
        """Initialize the example system.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.logger = logger
        self._load_config()
    
    def process_data(self, data: List[Dict[str, Any]]) -> bool:
        """Process the provided data.
        
        Args:
            data: List of data dictionaries to process
            
        Returns:
            True if processing was successful, False otherwise
            
        Raises:
            ValueError: If data format is invalid
        """
        try:
            # Process the data
            for item in data:
                self._validate_item(item)
                self._process_item(item)
            
            self.logger.info(f"Successfully processed {len(data)} items")
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing data: {e}")
            return False
    
    def _load_config(self) -> None:
        """Load configuration from file."""
        # Implementation here
        pass
    
    def _validate_item(self, item: Dict[str, Any]) -> None:
        """Validate a single data item."""
        # Implementation here
        pass
    
    def _process_item(self, item: Dict[str, Any]) -> None:
        """Process a single data item."""
        # Implementation here
        pass
```

## 🧪 Testing Guidelines

### AI System Testing

When contributing to AI systems:

1. **Test AI Learning** - Verify that AI players learn and adapt properly
2. **Test Team Dynamics** - Ensure team coordination works correctly
3. **Test Performance** - Monitor system resource usage during AI testing
4. **Test Edge Cases** - Test with unusual scenarios or configurations

### Running Tests

```bash
# Run AI playtest
venv\Scripts\python.exe tools\dev_master.py ai-playtest-enhanced Alex --verbose

# Run learning party demo
venv\Scripts\python.exe tools\ai_playtest_tool.py demo

# Run performance monitoring
venv\Scripts\python.exe tools\dev_master.py performance-start test_session
venv\Scripts\python.exe tools\dev_master.py performance-stop
venv\Scripts\python.exe tools\dev_master.py performance-summary
```

### Test Scenarios

- **Character Creation** - Test AI character building decisions
- **Combat Testing** - Test AI combat strategy and tactics
- **Skill Allocation** - Test AI skill tree decisions
- **Exploration** - Test AI exploration and discovery behavior
- **Team Coordination** - Test AI team dynamics and cooperation

## 📚 Documentation Standards

### Code Documentation

- **Docstrings** - Use Google-style docstrings for all functions and classes
- **Type Hints** - Include comprehensive type hints
- **Examples** - Provide usage examples in docstrings
- **Error Handling** - Document all possible exceptions

### Documentation Files

- **README.md** - Update the main README for significant changes
- **System Documentation** - Update relevant system docs in `docs/`
- **API Documentation** - Document new APIs and interfaces
- **Tutorials** - Create tutorials for new features

### Documentation Example

```python
def create_ai_player(name: str, skill_level: str, role: str) -> PlayerProfile:
    """Create a new AI player with specified characteristics.
    
    Args:
        name: The player's name
        skill_level: Skill level ('noob', 'casual', 'experienced', 'expert', 'master')
        role: Team role ('tank', 'dps', 'support', 'healer')
        
    Returns:
        A new PlayerProfile instance
        
    Raises:
        ValueError: If skill_level or role is invalid
        
    Example:
        >>> player = create_ai_player("Alex", "noob", "tank")
        >>> print(player.name)
        Alex
        >>> print(player.skill_level)
        noob
    """
    # Implementation here
    pass
```

## 🚀 Pull Request Guidelines

### Before Submitting

1. **Test thoroughly** - Ensure all tests pass
2. **Check performance** - Verify no performance regressions
3. **Update documentation** - Update relevant documentation
4. **Follow style guidelines** - Ensure code follows project standards

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] AI system enhancement

## Testing
- [ ] AI playtest passes
- [ ] Performance monitoring works
- [ ] Documentation updated
- [ ] No breaking changes

## Additional Notes
Any additional information or context
```

## 🐛 Bug Reports

When reporting bugs:

1. **Use the issue template** - Provide all requested information
2. **Include reproduction steps** - Clear steps to reproduce the issue
3. **Include system information** - OS, Python version, etc.
4. **Include logs** - Relevant log files or error messages
5. **Test with AI systems** - Include AI playtest results if relevant

## 💡 Feature Requests

When requesting features:

1. **Describe the feature** - Clear description of what you want
2. **Explain the benefit** - Why this feature would be useful
3. **Provide examples** - How the feature would be used
4. **Consider AI integration** - How it might affect AI testing

## 📞 Getting Help

- **GitHub Issues** - Use GitHub issues for bug reports and feature requests
- **Discussions** - Use GitHub discussions for questions and ideas
- **Documentation** - Check the docs directory for guides and tutorials

## 🏆 Recognition

Contributors will be recognized in:
- **README.md** - List of contributors
- **Release notes** - Credit for significant contributions
- **Documentation** - Attribution for documentation contributions

## 📄 License

By contributing to Chronicles of Ruin, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Chronicles of Ruin! Your contributions help make this project better for everyone.

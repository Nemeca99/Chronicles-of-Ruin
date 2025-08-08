#!/usr/bin/env python3
"""
CHRONICLES OF RUIN: SUNDERFALL - DEVELOPMENT SETUP
==================================================

This script automates the development environment setup for the Chronicles of Ruin project.
It handles virtual environment creation, dependency installation, and project validation.

USAGE:
    python setup_dev.py [options]

OPTIONS:
    --skip-venv     Skip virtual environment creation
    --skip-deps     Skip dependency installation
    --validate      Run validation after setup
    --help          Show this help message
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def create_virtual_environment():
    """Create a virtual environment."""
    if os.path.exists("venv"):
        print("ℹ️  Virtual environment already exists")
        return True
    
    return run_command("python -m venv venv", "Creating virtual environment")

def activate_virtual_environment():
    """Activate the virtual environment."""
    if os.name == 'nt':  # Windows
        activate_script = "venv\\Scripts\\activate"
    else:  # Unix/Linux/Mac
        activate_script = "venv/bin/activate"
    
    if os.path.exists(activate_script):
        print("✅ Virtual environment is ready")
        return True
    else:
        print("❌ Virtual environment activation script not found")
        return False

def install_dependencies():
    """Install project dependencies."""
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        pip_cmd = "venv/bin/pip"
    
    return run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies")

def validate_project():
    """Validate the project structure."""
    print("🔍 Validating project structure...")
    
    # Check required files
    required_files = [
        "src/core/sunderfall.py",
        "src/tools/build_tool_cli.py",
        "config.json",
        "requirements.txt",
        "README.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    # Check required directories
    required_dirs = [
        "src",
        "src/core",
        "src/systems", 
        "src/tools",
        "data",
        "docs",
        "assets"
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print("❌ Missing required directories:")
        for dir_path in missing_dirs:
            print(f"   - {dir_path}")
        return False
    
    print("✅ Project structure validation passed")
    return True

def run_cli_validation():
    """Run the CLI tool validation."""
    print("🔍 Running CLI tool validation...")
    
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/Mac
        python_cmd = "venv/bin/python"
    
    return run_command(f"{python_cmd} src/tools/build_tool_cli.py validate", "CLI validation")

def main():
    """Main setup function."""
    parser = argparse.ArgumentParser(
        description="Chronicles of Ruin: Sunderfall Development Setup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python setup_dev.py                    # Full setup
  python setup_dev.py --skip-venv       # Skip virtual environment
  python setup_dev.py --validate        # Run validation only
        """
    )
    
    parser.add_argument("--skip-venv", action="store_true",
                       help="Skip virtual environment creation")
    parser.add_argument("--skip-deps", action="store_true",
                       help="Skip dependency installation")
    parser.add_argument("--validate", action="store_true",
                       help="Run validation after setup")
    
    args = parser.parse_args()
    
    print("🚀 Chronicles of Ruin: Sunderfall - Development Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not args.skip_venv:
        if not create_virtual_environment():
            sys.exit(1)
        
        if not activate_virtual_environment():
            sys.exit(1)
    
    # Install dependencies
    if not args.skip_deps:
        if not install_dependencies():
            print("❌ Dependency installation failed")
            print("   Try running: pip install -r requirements.txt manually")
            sys.exit(1)
    
    # Validate project
    if not validate_project():
        print("❌ Project validation failed")
        print("   Please check the project structure")
        sys.exit(1)
    
    # Run CLI validation
    if not run_cli_validation():
        print("❌ CLI validation failed")
        sys.exit(1)
    
    print("\n🎉 Development environment setup completed successfully!")
    print("\n📋 Next Steps:")
    print("   1. Activate virtual environment:")
    if os.name == 'nt':
        print("      venv\\Scripts\\activate")
    else:
        print("      source venv/bin/activate")
    print("   2. Test the CLI tool:")
    print("      python src/tools/build_tool_cli.py status")
    print("   3. Review the phase map:")
    print("      phasemap.md")
    print("\n🚀 Ready to begin development!")

if __name__ == "__main__":
    main()

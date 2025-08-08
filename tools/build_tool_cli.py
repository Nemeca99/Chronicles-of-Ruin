"""
CHRONICLES OF RUIN: BUILD TOOL CLI
==================================

This is the primary CLI tool for managing the Chronicles of Ruin project.
It handles building, modifying, updating, and removing project files and systems.

PURPOSE:
- Build and modify project files and systems
- Version control and backup management
- Testing new systems before integration
- Project structure management
- Development workflow automation

ARCHITECTURE:
- CommandParser: Handles CLI argument parsing
- BuildManager: Manages project builds and modifications
- VersionControl: Handles backups and version management
- TestRunner: Runs tests on new systems
- ProjectManager: Manages project structure and files

USAGE:
- python build_tool_cli.py build [system]
- python build_tool_cli.py test [system]
- python build_tool_cli.py backup
- python build_tool_cli.py modify [file] [operation]
- python build_tool_cli.py create [type] [name]

This tool serves as the primary interface for all project management tasks,
ensuring consistent development practices and proper system integration.
"""

import sys
import os
import shutil
import json
import argparse
from typing import Dict, List, Optional, Any
from datetime import datetime
import subprocess


class BuildToolCLI:
    """
    Main CLI tool for managing the Chronicles of Ruin project.
    Handles all build, test, and modification operations.
    """

    def __init__(self):
        """Initialize the CLI tool with project configuration."""
        # Get the Sunderfall directory (parent of src)
        # Since we're running from the Sunderfall directory, the current directory is the sunderfall_path
        self.sunderfall_path = os.getcwd()
        self.src_path = os.path.join(self.sunderfall_path, "src")
        self.core_path = os.path.join(self.src_path, "core")
        self.systems_path = os.path.join(self.src_path, "systems")
        self.tools_path = os.path.join(self.src_path, "tools")
        self.docs_path = os.path.join(self.sunderfall_path, "docs")
        self.data_path = os.path.join(self.sunderfall_path, "data")
        self.tests_path = os.path.join(self.sunderfall_path, "tests")

        # Additional paths for enhanced structure
        self.assets_path = os.path.join(self.sunderfall_path, "assets")
        self.config_path = os.path.join(self.sunderfall_path, "config")
        self.logs_path = os.path.join(self.sunderfall_path, "logs")
        self.saves_path = os.path.join(self.sunderfall_path, "saves")
        self.temp_path = os.path.join(self.sunderfall_path, "temp")
        self.build_path = os.path.join(self.sunderfall_path, "build")

        # Load configuration
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load project configuration from config file."""
        config_path = os.path.join(self.sunderfall_path, "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load config: {e}")

        # Default configuration
        return {
            "project_name": "Chronicles of Ruin: Sunderfall",
            "version": "0.1.0",
            "systems": [
                "class",
                "combat",
                "status_elemental",
                "items",
                "player",
                "skills",
            ],
            "backup_enabled": True,
            "auto_test": True,
        }

    def _save_config(self):
        """Save current configuration to file."""
        config_path = os.path.join(self.sunderfall_path, "config.json")
        try:
            with open(config_path, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save config: {e}")

    def build_system(self, system_name: str) -> bool:
        """
        Build a specific system or all systems.

        Args:
            system_name: Name of system to build, or "all" for all systems

        Returns:
            True if build successful, False otherwise
        """
        print(f"Building system: {system_name}")

        if system_name == "all":
            success = True
            for system in self.config["systems"]:
                if not self._build_single_system(system):
                    success = False
            return success
        else:
            return self._build_single_system(system_name)

    def _build_single_system(self, system_name: str) -> bool:
        """Build a single system."""
        system_file = os.path.join(self.systems_path, f"{system_name}_system.py")

        if not os.path.exists(system_file):
            print(f"Error: System file {system_file} not found")
            return False

        try:
            # Import and test the system
            sys.path.insert(0, self.systems_path)
            module = __import__(f"{system_name}_system")

            # Test basic functionality
            # Convert system_name to proper class name (e.g., "status_elemental" -> "StatusElemental")
            class_name = (
                "".join(word.title() for word in system_name.split("_")) + "System"
            )
            if hasattr(module, class_name):
                system_class = getattr(module, class_name)
                instance = system_class()
                print(f"✓ {system_name} system built successfully")
                return True
            else:
                print(f"Error: {system_name} system class not found")
                return False

        except Exception as e:
            print(f"Error building {system_name} system: {e}")
            return False
        finally:
            if self.systems_path in sys.path:
                sys.path.remove(self.systems_path)

    def test_system(self, system_name: str) -> bool:
        """
        Test a specific system.

        Args:
            system_name: Name of system to test

        Returns:
            True if tests pass, False otherwise
        """
        print(f"Testing system: {system_name}")

        test_file = os.path.join(self.tests_path, f"test_{system_name}_system.py")

        if not os.path.exists(test_file):
            print(f"Warning: No test file found for {system_name}")
            return self._run_basic_test(system_name)

        try:
            result = subprocess.run(
                [sys.executable, test_file],
                capture_output=True,
                text=True,
                cwd=self.sunderfall_path,
            )

            if result.returncode == 0:
                print(f"✓ {system_name} tests passed")
                return True
            else:
                print(f"✗ {system_name} tests failed:")
                print(result.stderr)
                return False

        except Exception as e:
            print(f"Error running tests for {system_name}: {e}")
            return False

    def _run_basic_test(self, system_name: str) -> bool:
        """Run basic import and instantiation test for a system."""
        try:
            sys.path.insert(0, self.systems_path)
            module = __import__(f"{system_name}_system")

            # Convert system_name to proper class name (e.g., "status_elemental" -> "StatusElemental")
            class_name = (
                "".join(word.title() for word in system_name.split("_")) + "System"
            )
            if hasattr(module, class_name):
                system_class = getattr(module, class_name)
                instance = system_class()
                print(f"✓ Basic test passed for {system_name}")
                return True
            else:
                print(f"✗ System class not found for {system_name}")
                return False

        except Exception as e:
            print(f"✗ Basic test failed for {system_name}: {e}")
            return False
        finally:
            if self.systems_path in sys.path:
                sys.path.remove(self.systems_path)

    def create_backup(self) -> bool:
        """
        Create a backup of the current project state.

        Returns:
            True if backup successful, False otherwise
        """
        if not self.config.get("backup_enabled", True):
            print("Backups are disabled in config")
            return True

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(
            self.sunderfall_path, "backups", f"backup_{timestamp}"
        )

        try:
            os.makedirs(backup_dir, exist_ok=True)

            # Copy source files
            shutil.copytree(
                self.src_path, os.path.join(backup_dir, "src"), dirs_exist_ok=True
            )

            # Copy docs and data
            if os.path.exists(self.docs_path):
                shutil.copytree(
                    self.docs_path, os.path.join(backup_dir, "docs"), dirs_exist_ok=True
                )
            if os.path.exists(self.data_path):
                shutil.copytree(
                    self.data_path, os.path.join(backup_dir, "data"), dirs_exist_ok=True
                )

            # Save current config
            shutil.copy2(
                os.path.join(self.sunderfall_path, "config.json"),
                os.path.join(backup_dir, "config.json"),
            )

            print(f"✓ Backup created: {backup_dir}")
            return True

        except Exception as e:
            print(f"Error creating backup: {e}")
            return False

    def modify_file(self, file_path: str, operation: str, **kwargs) -> bool:
        """
        Modify a file with a specific operation.

        Args:
            file_path: Path to file to modify
            operation: Operation to perform (add, remove, update)
            **kwargs: Additional arguments for the operation

        Returns:
            True if modification successful, False otherwise
        """
        full_path = os.path.join(self.sunderfall_path, file_path)

        if not os.path.exists(full_path):
            print(f"Error: File {full_path} not found")
            return False

        try:
            if operation == "add":
                return self._add_to_file(full_path, **kwargs)
            elif operation == "remove":
                return self._remove_from_file(full_path, **kwargs)
            elif operation == "update":
                return self._update_file(full_path, **kwargs)
            else:
                print(f"Error: Unknown operation '{operation}'")
                return False

        except Exception as e:
            print(f"Error modifying file: {e}")
            return False

    def _add_to_file(self, file_path: str, content: str, position: str = "end") -> bool:
        """Add content to a file."""
        try:
            with open(file_path, "r") as f:
                current_content = f.read()

            if position == "end":
                new_content = current_content + "\n" + content
            elif position == "start":
                new_content = content + "\n" + current_content
            else:
                print(f"Error: Unknown position '{position}'")
                return False

            with open(file_path, "w") as f:
                f.write(new_content)

            print(f"✓ Added content to {file_path}")
            return True

        except Exception as e:
            print(f"Error adding to file: {e}")
            return False

    def _remove_from_file(self, file_path: str, pattern: str) -> bool:
        """Remove content matching pattern from file."""
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()

            new_lines = [line for line in lines if pattern not in line]

            with open(file_path, "w") as f:
                f.writelines(new_lines)

            print(f"✓ Removed content from {file_path}")
            return True

        except Exception as e:
            print(f"Error removing from file: {e}")
            return False

    def _update_file(self, file_path: str, old_content: str, new_content: str) -> bool:
        """Update content in a file."""
        try:
            with open(file_path, "r") as f:
                content = f.read()

            if old_content in content:
                content = content.replace(old_content, new_content)

                with open(file_path, "w") as f:
                    f.write(content)

                print(f"✓ Updated content in {file_path}")
                return True
            else:
                print(f"Error: Old content not found in {file_path}")
                return False

        except Exception as e:
            print(f"Error updating file: {e}")
            return False

    def create_system(self, system_name: str) -> bool:
        """
        Create a new system file.

        Args:
            system_name: Name of the system to create

        Returns:
            True if creation successful, False otherwise
        """
        system_file = os.path.join(self.systems_path, f"{system_name}_system.py")

        if os.path.exists(system_file):
            print(f"Warning: System file {system_file} already exists")
            return False

        try:
            template = self._get_system_template(system_name)

            with open(system_file, "w") as f:
                f.write(template)

            print(f"✓ Created system: {system_file}")

            # Add to config
            if system_name not in self.config["systems"]:
                self.config["systems"].append(system_name)
                self._save_config()

            return True

        except Exception as e:
            print(f"Error creating system: {e}")
            return False

    def _get_system_template(self, system_name: str) -> str:
        """Get template for a new system file."""
        return f'''"""
CHRONICLES OF RUIN: {system_name.upper()} SYSTEM
==============================================

This module handles the {system_name} system for Chronicles of Ruin.
[Add specific description here]

PURPOSE:
- [Add specific purposes here]
- [Add more purposes as needed]

ARCHITECTURE:
- [Add architecture description here]

[Add more documentation as needed]

This system provides [add description of what this system provides].
"""

from typing import Dict, List, Optional, Any
from enum import Enum

class {system_name.title()}System:
    """
    Main {system_name} system for Chronicles of Ruin.
    [Add specific description here]
    """
    
    def __init__(self):
        """Initialize the {system_name} system."""
        self.data = {{}}
        print(f"{system_name.title()} system initialized")
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the {system_name} system."""
        return {{
            'name': '{system_name}',
            'description': '[Add description here]',
            'data_count': len(self.data)
        }}

# Example usage and testing
if __name__ == "__main__":
    {system_name}_system = {system_name.title()}System()
    info = {system_name}_system.get_info()
    print(f"{system_name.title()} system info: {{info}}")
'''

    def run_game(self) -> bool:
        """
        Run the main game.

        Returns:
            True if game runs successfully, False otherwise
        """
        game_file = os.path.join(self.core_path, "sunderfall.py")

        if not os.path.exists(game_file):
            print(f"Error: Game file {game_file} not found")
            return False

        try:
            print("Starting Chronicles of Ruin: Sunderfall...")
            result = subprocess.run(
                [sys.executable, game_file], cwd=self.sunderfall_path
            )
            return result.returncode == 0

        except Exception as e:
            print(f"Error running game: {e}")
            return False

    def show_status(self):
        """Show current project status."""
        print("\nCHRONICLES OF RUIN: SUNDERFALL - PROJECT STATUS")
        print("=" * 50)

        # Check systems
        print("\nSystems:")
        for system in self.config["systems"]:
            system_file = os.path.join(self.systems_path, f"{system}_system.py")
            if os.path.exists(system_file):
                print(f"  ✓ {system}_system.py")
            else:
                print(f"  ✗ {system}_system.py (missing)")

        # Check core files
        print("\nCore Files:")
        core_files = ["sunderfall.py"]
        for file in core_files:
            file_path = os.path.join(self.core_path, file)
            if os.path.exists(file_path):
                print(f"  ✓ {file}")
            else:
                print(f"  ✗ {file} (missing)")

        # Check tools
        print("\nTools:")
        tools_files = ["build_tool_cli.py"]
        for file in tools_files:
            file_path = os.path.join(self.tools_path, file)
            if os.path.exists(file_path):
                print(f"  ✓ {file}")
            else:
                print(f"  ✗ {file} (missing)")

        print(f"\nProject Version: {self.config.get('version', '0.1.0')}")
        print(f"Backup Enabled: {self.config.get('backup_enabled', True)}")
        print(f"Auto Test: {self.config.get('auto_test', True)}")

    def setup_project_structure(self):
        """Create all necessary folders and files for the project."""
        print("Setting up project structure...")

        # Create all necessary directories
        directories = [
            self.assets_path,
            os.path.join(self.assets_path, "sprites"),
            os.path.join(self.assets_path, "sounds"),
            os.path.join(self.assets_path, "music"),
            os.path.join(self.assets_path, "fonts"),
            os.path.join(self.assets_path, "ui"),
            self.config_path,
            self.logs_path,
            self.saves_path,
            self.temp_path,
            self.build_path,
            os.path.join(self.docs_path, "API"),
            os.path.join(self.docs_path, "Design"),
            os.path.join(self.docs_path, "Technical"),
            os.path.join(self.docs_path, "User"),
        ]

        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created directory: {directory}")

        print("Project structure setup complete!")

    def create_documentation(self):
        """Generate documentation for all systems."""
        print("Generating documentation...")

        # Create system documentation
        for system in self.config["systems"]:
            doc_file = os.path.join(self.docs_path, f"{system}_system.md")
            if not os.path.exists(doc_file):
                content = f"# {system.title()} System\n\n## Overview\nThis document describes the {system} system.\n\n## API\n[Documentation to be generated]\n"
                with open(doc_file, "w") as f:
                    f.write(content)
                print(f"Created documentation: {doc_file}")

        print("Documentation generation complete!")

    def validate_project(self):
        """Validate the entire project structure and files."""
        print("Validating project structure...")

        errors = []
        warnings = []

        # Check required directories
        required_dirs = [
            self.src_path,
            self.core_path,
            self.systems_path,
            self.tools_path,
            self.docs_path,
            self.data_path,
            self.tests_path,
            self.assets_path,
            self.config_path,
            self.logs_path,
            self.saves_path,
            self.temp_path,
            self.build_path,
        ]

        for directory in required_dirs:
            if not os.path.exists(directory):
                errors.append(f"Missing directory: {directory}")

        # Check required files
        required_files = [
            os.path.join(self.core_path, "sunderfall.py"),
            os.path.join(self.tools_path, "build_tool_cli.py"),
            os.path.join(self.sunderfall_path, "config.json"),
        ]

        for file_path in required_files:
            if not os.path.exists(file_path):
                errors.append(f"Missing file: {file_path}")

        # Check system files
        for system in self.config["systems"]:
            system_file = os.path.join(self.systems_path, f"{system}_system.py")
            if not os.path.exists(system_file):
                warnings.append(f"System file missing: {system_file}")

        # Report results
        if errors:
            print("❌ Validation Errors:")
            for error in errors:
                print(f"  - {error}")

        if warnings:
            print("⚠️  Validation Warnings:")
            for warning in warnings:
                print(f"  - {warning}")

        if not errors and not warnings:
            print("[SUCCESS] Project validation passed!")
        elif not errors:
            print("[SUCCESS] Project validation passed with warnings!")
        else:
            print("[ERROR] Project validation failed!")

        return len(errors) == 0

    def manage_database(self):
        """Manage database operations"""
        import argparse

        parser = argparse.ArgumentParser(description="Database management")
        parser.add_argument(
            "action",
            choices=["init", "create", "drop", "health", "migrate"],
            help="Database action to perform",
        )
        parser.add_argument("--url", help="Database URL")

        # Parse remaining arguments
        import sys

        db_args = sys.argv[2:]  # Skip the main command and 'db'

        try:
            args = parser.parse_args(db_args)
        except SystemExit:
            print("Database management commands:")
            print("  init     - Initialize database connection")
            print("  create   - Create all database tables")
            print("  drop     - Drop all database tables (DANGEROUS!)")
            print("  health   - Check database connectivity")
            print("  migrate  - Run database migrations")
            return

        try:
            import sys

            sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
            from database import initialize_database, create_tables, health_check

            if args.action == "init":
                print("Initializing database...")
                initialize_database(args.url)
                print("[SUCCESS] Database initialized successfully!")

            elif args.action == "create":
                print("Creating database tables...")
                initialize_database(args.url)
                create_tables()
                print("[SUCCESS] Database tables created successfully!")

            elif args.action == "drop":
                confirm = input(
                    "[WARNING] This will DELETE ALL DATA! Type 'YES' to confirm: "
                )
                if confirm == "YES":
                    from database import get_db_manager

                    initialize_database(args.url)
                    get_db_manager().drop_tables()
                    print("[SUCCESS] Database tables dropped successfully!")
                else:
                    print("[ERROR] Operation cancelled")

            elif args.action == "health":
                print("Checking database health...")
                initialize_database(args.url)
                if health_check():
                    print("[SUCCESS] Database is healthy!")
                else:
                    print("[ERROR] Database health check failed!")

            elif args.action == "migrate":
                print("Running database migrations...")
                # TODO: Implement Alembic migrations
                print("[WARNING] Migrations not yet implemented")

        except Exception as e:
            print(f"[ERROR] Database operation failed: {e}")
            return False

        return True


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Chronicles of Ruin Build Tool")
    parser.add_argument(
        "command",
        choices=[
            "build",
            "test",
            "backup",
            "modify",
            "create",
            "run",
            "status",
            "setup",
            "docs",
            "validate",
            "db",
        ],
        help="Command to execute",
    )
    parser.add_argument("target", nargs="?", help="Target for the command")
    parser.add_argument("--operation", help="Operation for modify command")
    parser.add_argument("--content", help="Content for modify command")
    parser.add_argument("--position", default="end", help="Position for add operation")

    args = parser.parse_args()

    cli = BuildToolCLI()

    if args.command == "build":
        target = args.target or "all"
        success = cli.build_system(target)
        sys.exit(0 if success else 1)

    elif args.command == "test":
        target = args.target or "all"
        success = cli.test_system(target)
        sys.exit(0 if success else 1)

    elif args.command == "backup":
        success = cli.create_backup()
        sys.exit(0 if success else 1)

    elif args.command == "modify":
        if not args.target or not args.operation:
            print("Error: modify command requires target and operation")
            sys.exit(1)

        kwargs = {}
        if args.content:
            kwargs["content"] = args.content
        if args.position:
            kwargs["position"] = args.position

        success = cli.modify_file(args.target, args.operation, **kwargs)
        sys.exit(0 if success else 1)

    elif args.command == "create":
        if not args.target:
            print("Error: create command requires target")
            sys.exit(1)

        success = cli.create_system(args.target)
        sys.exit(0 if success else 1)

    elif args.command == "run":
        success = cli.run_game()
        sys.exit(0 if success else 1)

    elif args.command == "status":
        cli.show_status()
        sys.exit(0)

    elif args.command == "setup":
        cli.setup_project_structure()
        sys.exit(0)

    elif args.command == "docs":
        cli.create_documentation()
        sys.exit(0)

    elif args.command == "validate":
        success = cli.validate_project()
        sys.exit(0 if success else 1)
    elif args.command == "db":
        cli.manage_database()


if __name__ == "__main__":
    main()

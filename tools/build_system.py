#!/usr/bin/env python3
"""
Enhanced Build System for Chronicles of Ruin Saga
Handles building, testing, and managing all chapters in the saga.
"""

import os
import sys
import json
import shutil
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class BuildTarget(Enum):
    ALL = "all"
    CHAPTER = "chapter"
    TESTS = "tests"
    DOCS = "docs"
    CLEAN = "clean"

@dataclass
class BuildResult:
    success: bool
    target: str
    duration: float
    errors: List[str]
    warnings: List[str]

class BuildSystem:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.chapters_dir = self.root_dir / "chapters"
        self.tools_dir = self.root_dir / "tools"
        self.docs_dir = self.root_dir / "docs"
        self.tests_dir = self.root_dir / "tests"
        self.build_dir = self.root_dir / "build"
        self.logs_dir = self.root_dir / "logs"
        
        # Ensure directories exist
        self.build_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        
    def get_chapters(self) -> List[str]:
        """Get list of available chapters."""
        chapters = []
        if self.chapters_dir.exists():
            for item in self.chapters_dir.iterdir():
                if item.is_dir() and item.name.startswith("chapter_"):
                    chapters.append(item.name)
        return sorted(chapters)
    
    def build_chapter(self, chapter_name: str) -> BuildResult:
        """Build a specific chapter."""
        start_time = time.time()
        errors = []
        warnings = []
        
        chapter_path = self.chapters_dir / chapter_name
        if not chapter_path.exists():
            return BuildResult(False, chapter_name, time.time() - start_time, 
                             [f"Chapter {chapter_name} not found"], warnings)
        
        print(f"Building chapter: {chapter_name}")
        
        # Check for required files
        required_files = ["game_launcher.py", "config.json", "src"]
        for file in required_files:
            if not (chapter_path / file).exists():
                errors.append(f"Missing required file: {file}")
        
        if errors:
            return BuildResult(False, chapter_name, time.time() - start_time, errors, warnings)
        
        # Validate Python syntax
        try:
            result = subprocess.run([sys.executable, "-m", "py_compile", 
                                   str(chapter_path / "game_launcher.py")],
                                  capture_output=True, text=True)
            if result.returncode != 0:
                errors.append(f"Syntax error in game_launcher.py: {result.stderr}")
        except Exception as e:
            errors.append(f"Failed to validate syntax: {e}")
        
        # Check for common issues
        self._check_chapter_issues(chapter_path, warnings)
        
        # Create build artifacts
        build_artifacts = self.build_dir / chapter_name
        build_artifacts.mkdir(exist_ok=True)
        
        # Copy chapter files to build directory
        try:
            if build_artifacts.exists():
                shutil.rmtree(build_artifacts)
            shutil.copytree(chapter_path, build_artifacts)
            print(f"SUCCESS: Chapter {chapter_name} built successfully")
        except Exception as e:
            errors.append(f"Failed to create build artifacts: {e}")
        
        duration = time.time() - start_time
        return BuildResult(len(errors) == 0, chapter_name, duration, errors, warnings)
    
    def _check_chapter_issues(self, chapter_path: Path, warnings: List[str]):
        """Check for common issues in a chapter."""
        # Check for large files
        for file in chapter_path.rglob("*"):
            if file.is_file() and file.stat().st_size > 10 * 1024 * 1024:  # 10MB
                warnings.append(f"Large file detected: {file.relative_to(chapter_path)}")
        
        # Check for missing __init__.py files
        for py_dir in chapter_path.rglob("*/"):
            if py_dir.is_dir() and any(py_dir.glob("*.py")):
                if not (py_dir / "__init__.py").exists():
                    warnings.append(f"Missing __init__.py in: {py_dir.relative_to(chapter_path)}")
    
    def run_tests(self, target: str = "all") -> BuildResult:
        """Run tests for the specified target."""
        start_time = time.time()
        errors = []
        warnings = []
        
        print(f"Running tests for: {target}")
        
        if target == "all":
            # Run all tests
            test_files = list(self.tests_dir.glob("test_*.py"))
        else:
            # Run specific chapter tests
            test_files = list(self.tests_dir.glob(f"test_{target}_*.py"))
        
        if not test_files:
            warnings.append(f"No test files found for target: {target}")
            return BuildResult(True, f"tests_{target}", time.time() - start_time, errors, warnings)
        
        for test_file in test_files:
            try:
                result = subprocess.run([sys.executable, "-m", "pytest", str(test_file), "-v"],
                                      capture_output=True, text=True, cwd=self.root_dir)
                if result.returncode != 0:
                    errors.append(f"Test failed in {test_file.name}: {result.stderr}")
                else:
                    print(f"SUCCESS: Tests passed: {test_file.name}")
            except Exception as e:
                errors.append(f"Failed to run tests in {test_file.name}: {e}")
        
        duration = time.time() - start_time
        return BuildResult(len(errors) == 0, f"tests_{target}", duration, errors, warnings)
    
    def build_docs(self) -> BuildResult:
        """Build documentation."""
        start_time = time.time()
        errors = []
        warnings = []
        
        print("Building documentation...")
        
        if not self.docs_dir.exists():
            warnings.append("No docs directory found")
            return BuildResult(True, "docs", time.time() - start_time, errors, warnings)
        
        # Create docs build directory
        docs_build = self.build_dir / "docs"
        docs_build.mkdir(exist_ok=True)
        
        # Copy documentation files
        try:
            for file in self.docs_dir.rglob("*.md"):
                dest = docs_build / file.relative_to(self.docs_dir)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, dest)
            print("SUCCESS: Documentation built successfully")
        except Exception as e:
            errors.append(f"Failed to build docs: {e}")
        
        duration = time.time() - start_time
        return BuildResult(len(errors) == 0, "docs", duration, errors, warnings)
    
    def clean_build(self) -> BuildResult:
        """Clean build artifacts."""
        start_time = time.time()
        errors = []
        warnings = []
        
        print("Cleaning build artifacts...")
        
        try:
            if self.build_dir.exists():
                shutil.rmtree(self.build_dir)
                self.build_dir.mkdir()
            print("SUCCESS: Build artifacts cleaned")
        except Exception as e:
            errors.append(f"Failed to clean build: {e}")
        
        duration = time.time() - start_time
        return BuildResult(len(errors) == 0, "clean", duration, errors, warnings)
    
    def build_all(self) -> List[BuildResult]:
        """Build all chapters and run all tests."""
        results = []
        
        print("=== Building Chronicles of Ruin Saga ===")
        
        # Clean first
        results.append(self.clean_build())
        
        # Build all chapters
        chapters = self.get_chapters()
        for chapter in chapters:
            results.append(self.build_chapter(chapter))
        
        # Run all tests
        results.append(self.run_tests("all"))
        
        # Build docs
        results.append(self.build_docs())
        
        return results
    
    def generate_build_report(self, results: List[BuildResult]) -> str:
        """Generate a build report."""
        report = []
        report.append("=== Build Report ===")
        report.append(f"Build completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        total_duration = sum(r.duration for r in results)
        successful_builds = sum(1 for r in results if r.success)
        
        report.append(f"Total duration: {total_duration:.2f}s")
        report.append(f"Successful builds: {successful_builds}/{len(results)}")
        report.append("")
        
        for result in results:
            status = "PASS" if result.success else "FAIL"
            report.append(f"{status} {result.target} ({result.duration:.2f}s)")
            
            if result.errors:
                for error in result.errors:
                    report.append(f"  ERROR: {error}")
            
            if result.warnings:
                for warning in result.warnings:
                    report.append(f"  WARNING: {warning}")
        
        return "\n".join(report)
    
    def save_build_log(self, results: List[BuildResult]):
        """Save build results to log file."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        log_file = self.logs_dir / f"build_{timestamp}.log"
        
        report = self.generate_build_report(results)
        
        with open(log_file, "w") as f:
            f.write(report)
        
        print(f"Build log saved to: {log_file}")

def main():
    """CLI interface for the build system."""
    build_system = BuildSystem()
    
    if len(sys.argv) < 2:
        print("Enhanced Build System for Chronicles of Ruin")
        print("Usage:")
        print("  python build_system.py all")
        print("  python build_system.py chapter <chapter_name>")
        print("  python build_system.py tests [target]")
        print("  python build_system.py docs")
        print("  python build_system.py clean")
        return
    
    command = sys.argv[1]
    
    if command == "all":
        results = build_system.build_all()
        print(build_system.generate_build_report(results))
        build_system.save_build_log(results)
        
    elif command == "chapter" and len(sys.argv) >= 3:
        chapter_name = sys.argv[2]
        result = build_system.build_chapter(chapter_name)
        print(build_system.generate_build_report([result]))
        
    elif command == "tests":
        target = sys.argv[2] if len(sys.argv) > 2 else "all"
        result = build_system.run_tests(target)
        print(build_system.generate_build_report([result]))
        
    elif command == "docs":
        result = build_system.build_docs()
        print(build_system.generate_build_report([result]))
        
    elif command == "clean":
        result = build_system.clean_build()
        print(build_system.generate_build_report([result]))
        
    else:
        print("Invalid command or missing arguments!")

if __name__ == "__main__":
    main()

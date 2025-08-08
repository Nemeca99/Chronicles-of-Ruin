#!/usr/bin/env python3
"""
QUICK AUTONOMOUS TEST FOR SUNDERFALL
====================================

This script provides immediate autonomous testing of the Sunderfall
game system without requiring manual input or complex setup.

FEATURES:
- System validation
- Game system testing
- Database operations
- Gameplay simulation
- Performance checks

USAGE:
    python quick_test.py
"""

import sys
import os
import time
import subprocess
from datetime import datetime

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")

def print_result(test_name, status, details=""):
    """Print a test result"""
    icon = "✅" if status == "PASSED" else "❌"
    print(f"{icon} {test_name}: {details}")

def test_system_structure():
    """Test the project structure"""
    print_header("SYSTEM STRUCTURE VALIDATION")
    
    required_dirs = ['src', 'data', 'docs', 'tests', 'assets', 'config', 'logs', 'saves', 'temp', 'build']
    required_files = ['config.json', 'requirements.txt', 'launcher.py', 'phasemap.md', 'README.md']
    
    passed = 0
    total = len(required_dirs) + len(required_files)
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print_result(f"Directory: {dir_name}", "PASSED", "exists")
            passed += 1
        else:
            print_result(f"Directory: {dir_name}", "FAILED", "missing")
    
    for file_name in required_files:
        if os.path.exists(file_name):
            print_result(f"File: {file_name}", "PASSED", "exists")
            passed += 1
        else:
            print_result(f"File: {file_name}", "FAILED", "missing")
    
    print(f"\n📊 Structure Test: {passed}/{total} passed")
    return passed == total

def test_python_environment():
    """Test Python environment"""
    print_header("PYTHON ENVIRONMENT")
    
    try:
        import sys
        print_result("Python Version", "PASSED", f"{sys.version.split()[0]}")
        
        # Test required packages
        required_packages = ['json', 'os', 'sys', 'time', 'random']
        for package in required_packages:
            try:
                __import__(package)
                print_result(f"Package: {package}", "PASSED", "available")
            except ImportError:
                print_result(f"Package: {package}", "FAILED", "not available")
        
        return True
    except Exception as e:
        print_result("Python Environment", "FAILED", str(e))
        return False

def test_cli_tools():
    """Test CLI tool functionality"""
    print_header("CLI TOOL TESTING")
    
    commands = [
        ['python', 'src/tools/build_tool_cli.py', 'status'],
        ['python', 'src/tools/build_tool_cli.py', 'validate'],
    ]
    
    passed = 0
    total = len(commands)
    
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print_result(f"CLI: {' '.join(cmd)}", "PASSED", "executed successfully")
                passed += 1
            else:
                print_result(f"CLI: {' '.join(cmd)}", "FAILED", f"return code {result.returncode}")
        except Exception as e:
            print_result(f"CLI: {' '.join(cmd)}", "FAILED", str(e))
    
    print(f"\n📊 CLI Test: {passed}/{total} passed")
    return passed == total

def test_database_operations():
    """Test database operations"""
    print_header("DATABASE OPERATIONS")
    
    commands = [
        ['python', 'src/tools/build_tool_cli.py', 'db', 'health'],
    ]
    
    passed = 0
    total = len(commands)
    
    for cmd in commands:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print_result(f"Database: {' '.join(cmd)}", "PASSED", "operation successful")
                passed += 1
            else:
                print_result(f"Database: {' '.join(cmd)}", "FAILED", f"return code {result.returncode}")
        except Exception as e:
            print_result(f"Database: {' '.join(cmd)}", "FAILED", str(e))
    
    print(f"\n📊 Database Test: {passed}/{total} passed")
    return passed == total

def test_game_systems():
    """Test game system imports"""
    print_header("GAME SYSTEMS TESTING")
    
    try:
        # Add src to path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
        
        # Test importing game systems
        systems = [
            'systems.class_system',
            'systems.combat_system',
            'systems.items_system',
            'systems.player_system',
            'systems.skills_system'
        ]
        
        passed = 0
        total = len(systems)
        
        for system in systems:
            try:
                __import__(system)
                print_result(f"System: {system}", "PASSED", "imported successfully")
                passed += 1
            except ImportError as e:
                print_result(f"System: {system}", "FAILED", f"import failed: {e}")
        
        print(f"\n📊 Systems Test: {passed}/{total} passed")
        return passed == total
        
    except Exception as e:
        print_result("Game Systems", "FAILED", str(e))
        return False

def test_game_launcher():
    """Test game launcher"""
    print_header("GAME LAUNCHER TESTING")
    
    try:
        result = subprocess.run(['python', 'launcher.py', '--help'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print_result("Game Launcher", "PASSED", "help command successful")
            return True
        else:
            print_result("Game Launcher", "FAILED", f"return code {result.returncode}")
            return False
    except Exception as e:
        print_result("Game Launcher", "FAILED", str(e))
        return False

def test_autonomous_demo():
    """Test autonomous demo functionality"""
    print_header("AUTONOMOUS DEMO TESTING")
    
    try:
        # Test if autonomous test script exists
        if os.path.exists('autonomous_test.py'):
            print_result("Autonomous Test Script", "PASSED", "file exists")
            
            # Try to run a quick demo
            result = subprocess.run(['python', 'autonomous_test.py', '--demo'], 
                                  capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print_result("Autonomous Demo", "PASSED", "demo completed successfully")
                return True
            else:
                print_result("Autonomous Demo", "FAILED", f"return code {result.returncode}")
                return False
        else:
            print_result("Autonomous Test Script", "FAILED", "file missing")
            return False
    except Exception as e:
        print_result("Autonomous Demo", "FAILED", str(e))
        return False

def test_game_simulation():
    """Test game simulation"""
    print_header("GAME SIMULATION TESTING")
    
    try:
        # Test if game simulation script exists
        if os.path.exists('game_simulation.py'):
            print_result("Game Simulation Script", "PASSED", "file exists")
            
            # Try to run a quick simulation
            result = subprocess.run(['python', 'game_simulation.py', '--scenario', 'new_player'], 
                                  capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                print_result("Game Simulation", "PASSED", "simulation completed successfully")
                return True
            else:
                print_result("Game Simulation", "FAILED", f"return code {result.returncode}")
                return False
        else:
            print_result("Game Simulation Script", "FAILED", "file missing")
            return False
    except Exception as e:
        print_result("Game Simulation", "FAILED", str(e))
        return False

def run_performance_test():
    """Run a quick performance test"""
    print_header("PERFORMANCE TESTING")
    
    try:
        start_time = time.time()
        
        # Test system import performance
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
        
        import time as time_module
        import random
        import json
        
        # Simple performance test
        test_data = [random.randint(1, 100) for _ in range(1000)]
        
        # Test JSON serialization
        start = time_module.time()
        json.dumps(test_data)
        json_time = time_module.time() - start
        
        # Test list operations
        start = time_module.time()
        sorted_data = sorted(test_data)
        sort_time = time_module.time() - start
        
        total_time = time.time() - start_time
        
        print_result("Performance Test", "PASSED", f"completed in {total_time:.3f}s")
        print_result("JSON Operations", "PASSED", f"{json_time:.3f}s")
        print_result("List Operations", "PASSED", f"{sort_time:.3f}s")
        
        return True
    except Exception as e:
        print_result("Performance Test", "FAILED", str(e))
        return False

def main():
    """Main test execution"""
    print("🚀 SUNDERFALL QUICK AUTONOMOUS TEST")
    print("=" * 50)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_results = {}
    
    # Run all tests
    tests = [
        ("System Structure", test_system_structure),
        ("Python Environment", test_python_environment),
        ("CLI Tools", test_cli_tools),
        ("Database Operations", test_database_operations),
        ("Game Systems", test_game_systems),
        ("Game Launcher", test_game_launcher),
        ("Autonomous Demo", test_autonomous_demo),
        ("Game Simulation", test_game_simulation),
        ("Performance", run_performance_test),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            test_results[test_name] = result
            if result:
                passed += 1
        except Exception as e:
            print_result(test_name, "FAILED", f"Exception: {e}")
            test_results[test_name] = False
    
    # Print final results
    print_header("FINAL RESULTS")
    print(f"📊 Overall: {passed}/{total} tests passed")
    print(f"📈 Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for development.")
    else:
        print("⚠️ Some tests failed. Please check the implementation.")
    
    # Print failed tests
    if passed < total:
        print("\n❌ Failed Tests:")
        for test_name, result in test_results.items():
            if not result:
                print(f"  • {test_name}")
    
    print(f"\n🏁 Test completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

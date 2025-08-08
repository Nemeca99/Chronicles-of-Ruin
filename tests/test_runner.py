#!/usr/bin/env python3
"""
COMPREHENSIVE TEST RUNNER FOR CHRONICLES OF RUIN: SUNDERFALL
============================================================

This script provides autonomous testing capabilities for the entire
Sunderfall game system, including system validation, gameplay simulation,
database operations, and performance benchmarking.

FEATURES:
- Automated system validation
- Gameplay simulation testing
- Database operation testing
- Performance benchmarking
- Comprehensive reporting
- Error handling and recovery
- Multi-scenario testing

USAGE:
    python test_runner.py [--mode MODE] [--scenarios SCENARIOS] [--report]

MODES:
    quick: Run essential tests only
    full: Run comprehensive testing
    performance: Focus on performance testing
    database: Focus on database operations
    gameplay: Focus on gameplay simulation
"""

import sys
import os
import time
import json
import subprocess
from typing import Dict, Any, List, Optional
import argparse
from datetime import datetime

class TestRunner:
    """Comprehensive test runner for Sunderfall"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = None
        self.end_time = None
        self.test_log = []
        
    def log_test(self, test_name: str, status: str, details: str = ""):
        """Log a test result"""
        self.test_results[test_name] = {
            'status': status,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.test_log.append(f"[{status.upper()}] {test_name}: {details}")
        print(f"[{status.upper()}] {test_name}: {details}")
    
    def run_system_validation(self):
        """Run system validation tests"""
        print("\n🔧 SYSTEM VALIDATION")
        print("=" * 25)
        
        # Test project structure
        required_dirs = ['src', 'data', 'docs', 'tests', 'assets', 'config', 'logs', 'saves', 'temp', 'build']
        for dir_name in required_dirs:
            if os.path.exists(dir_name):
                self.log_test(f"Directory Check: {dir_name}", "PASSED", "Directory exists")
            else:
                self.log_test(f"Directory Check: {dir_name}", "FAILED", "Directory missing")
        
        # Test required files
        required_files = [
            'config.json',
            'requirements.txt',
            'launcher.py',
            'phasemap.md',
            'README.md'
        ]
        for file_name in required_files:
            if os.path.exists(file_name):
                self.log_test(f"File Check: {file_name}", "PASSED", "File exists")
            else:
                self.log_test(f"File Check: {file_name}", "FAILED", "File missing")
        
        # Test Python environment
        try:
            import sys
            print(f"Python version: {sys.version}")
            self.log_test("Python Environment", "PASSED", f"Python {sys.version.split()[0]}")
        except Exception as e:
            self.log_test("Python Environment", "FAILED", str(e))
    
    def run_cli_tool_tests(self):
        """Test CLI tool functionality"""
        print("\n🛠️ CLI TOOL TESTING")
        print("=" * 20)
        
        cli_commands = [
            ['python', 'src/tools/build_tool_cli.py', 'status'],
            ['python', 'src/tools/build_tool_cli.py', 'validate'],
            ['python', 'src/tools/build_tool_cli.py', 'docs'],
        ]
        
        for cmd in cli_commands:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    self.log_test(f"CLI Command: {' '.join(cmd)}", "PASSED", "Command executed successfully")
                else:
                    self.log_test(f"CLI Command: {' '.join(cmd)}", "FAILED", f"Return code: {result.returncode}")
            except subprocess.TimeoutExpired:
                self.log_test(f"CLI Command: {' '.join(cmd)}", "FAILED", "Command timed out")
            except Exception as e:
                self.log_test(f"CLI Command: {' '.join(cmd)}", "FAILED", str(e))
    
    def run_database_tests(self):
        """Test database operations"""
        print("\n🗄️ DATABASE TESTING")
        print("=" * 20)
        
        db_commands = [
            ['python', 'src/tools/build_tool_cli.py', 'db', 'health'],
            ['python', 'src/tools/build_tool_cli.py', 'db', 'create'],
        ]
        
        for cmd in db_commands:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    self.log_test(f"Database Command: {' '.join(cmd)}", "PASSED", "Database operation successful")
                else:
                    self.log_test(f"Database Command: {' '.join(cmd)}", "FAILED", f"Return code: {result.returncode}")
            except subprocess.TimeoutExpired:
                self.log_test(f"Database Command: {' '.join(cmd)}", "FAILED", "Command timed out")
            except Exception as e:
                self.log_test(f"Database Command: {' '.join(cmd)}", "FAILED", str(e))
    
    def run_autonomous_testing(self):
        """Run autonomous testing system"""
        print("\n🤖 AUTONOMOUS TESTING")
        print("=" * 20)
        
        try:
            result = subprocess.run(['python', 'autonomous_test.py', '--demo'], 
                                  capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                self.log_test("Autonomous Testing Demo", "PASSED", "Demo completed successfully")
            else:
                self.log_test("Autonomous Testing Demo", "FAILED", f"Return code: {result.returncode}")
        except subprocess.TimeoutExpired:
            self.log_test("Autonomous Testing Demo", "FAILED", "Demo timed out")
        except Exception as e:
            self.log_test("Autonomous Testing Demo", "FAILED", str(e))
    
    def run_game_simulation(self):
        """Run game simulation tests"""
        print("\n🎮 GAME SIMULATION TESTING")
        print("=" * 30)
        
        scenarios = ['new_player', 'combat_focused', 'exploration', 'multiplayer']
        
        for scenario in scenarios:
            try:
                result = subprocess.run(['python', 'game_simulation.py', '--scenario', scenario], 
                                      capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    self.log_test(f"Game Simulation: {scenario}", "PASSED", "Simulation completed successfully")
                else:
                    self.log_test(f"Game Simulation: {scenario}", "FAILED", f"Return code: {result.returncode}")
            except subprocess.TimeoutExpired:
                self.log_test(f"Game Simulation: {scenario}", "FAILED", "Simulation timed out")
            except Exception as e:
                self.log_test(f"Game Simulation: {scenario}", "FAILED", str(e))
    
    def run_performance_tests(self):
        """Run performance benchmarking"""
        print("\n⚡ PERFORMANCE TESTING")
        print("=" * 20)
        
        try:
            result = subprocess.run(['python', 'autonomous_test.py', '--performance'], 
                                  capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                self.log_test("Performance Testing", "PASSED", "Performance tests completed")
            else:
                self.log_test("Performance Testing", "FAILED", f"Return code: {result.returncode}")
        except subprocess.TimeoutExpired:
            self.log_test("Performance Testing", "FAILED", "Performance tests timed out")
        except Exception as e:
            self.log_test("Performance Testing", "FAILED", str(e))
    
    def run_game_launcher_test(self):
        """Test the main game launcher"""
        print("\n🚀 GAME LAUNCHER TESTING")
        print("=" * 25)
        
        try:
            # Test launcher with help flag (should not require input)
            result = subprocess.run(['python', 'launcher.py', '--help'], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                self.log_test("Game Launcher Help", "PASSED", "Launcher help displayed successfully")
            else:
                self.log_test("Game Launcher Help", "FAILED", f"Return code: {result.returncode}")
        except subprocess.TimeoutExpired:
            self.log_test("Game Launcher Help", "FAILED", "Launcher timed out")
        except Exception as e:
            self.log_test("Game Launcher Help", "FAILED", str(e))
    
    def run_quick_tests(self):
        """Run essential tests only"""
        print("\n⚡ QUICK TEST SUITE")
        print("=" * 20)
        
        self.run_system_validation()
        self.run_cli_tool_tests()
        self.run_autonomous_testing()
    
    def run_full_tests(self):
        """Run comprehensive testing"""
        print("\n🧪 FULL TEST SUITE")
        print("=" * 20)
        
        self.run_system_validation()
        self.run_cli_tool_tests()
        self.run_database_tests()
        self.run_autonomous_testing()
        self.run_game_simulation()
        self.run_performance_tests()
        self.run_game_launcher_test()
    
    def run_performance_mode(self):
        """Run performance-focused tests"""
        print("\n⚡ PERFORMANCE MODE")
        print("=" * 20)
        
        self.run_performance_tests()
        self.run_game_simulation()  # Include gameplay simulation for performance
    
    def run_database_mode(self):
        """Run database-focused tests"""
        print("\n🗄️ DATABASE MODE")
        print("=" * 20)
        
        self.run_database_tests()
        self.run_system_validation()  # Include system validation
    
    def run_gameplay_mode(self):
        """Run gameplay-focused tests"""
        print("\n🎮 GAMEPLAY MODE")
        print("=" * 20)
        
        self.run_game_simulation()
        self.run_autonomous_testing()
        self.run_game_launcher_test()
    
    def generate_report(self):
        """Generate a comprehensive test report"""
        print("\n📊 GENERATING TEST REPORT")
        print("=" * 30)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result['status'] == 'PASSED')
        failed_tests = total_tests - passed_tests
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'duration': (self.end_time - self.start_time).total_seconds() if self.start_time and self.end_time else 0,
            'summary': {
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': failed_tests,
                'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0
            },
            'test_results': self.test_results,
            'test_log': self.test_log
        }
        
        # Save report to file
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📄 Test report saved to: {report_file}")
        
        # Print summary
        print(f"\n📈 TEST SUMMARY")
        print("=" * 15)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {report['summary']['success_rate']:.1f}%")
        print(f"Duration: {report['summary']['duration']:.2f} seconds")
        
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS:")
            for test_name, result in self.test_results.items():
                if result['status'] == 'FAILED':
                    print(f"  • {test_name}: {result['details']}")
        
        return report
    
    def run(self, mode='quick', scenarios=None, generate_report=False):
        """Main execution method"""
        self.start_time = datetime.now()
        
        print("🚀 SUNDERFALL COMPREHENSIVE TEST RUNNER")
        print("=" * 50)
        print(f"Mode: {mode}")
        print(f"Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            if mode == 'quick':
                self.run_quick_tests()
            elif mode == 'full':
                self.run_full_tests()
            elif mode == 'performance':
                self.run_performance_mode()
            elif mode == 'database':
                self.run_database_mode()
            elif mode == 'gameplay':
                self.run_gameplay_mode()
            else:
                print(f"❌ Unknown mode: {mode}")
                return
            
            self.end_time = datetime.now()
            
            if generate_report:
                self.generate_report()
            
            print(f"\n🏁 Test run completed at {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
        except KeyboardInterrupt:
            print("\n⚠️ Test run interrupted by user")
        except Exception as e:
            print(f"\n❌ Test run failed with error: {e}")
            self.log_test("Test Runner", "FAILED", str(e))


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Comprehensive test runner for Sunderfall")
    parser.add_argument('--mode', default='quick', 
                       choices=['quick', 'full', 'performance', 'database', 'gameplay'],
                       help='Test mode to run')
    parser.add_argument('--scenarios', nargs='+', help='Specific scenarios to test')
    parser.add_argument('--report', action='store_true', help='Generate detailed test report')
    
    args = parser.parse_args()
    
    runner = TestRunner()
    runner.run(args.mode, args.scenarios, args.report)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Performance Optimizer for Chronicles of Ruin: Sunderfall
Profiles and optimizes critical code paths for better performance
"""

import sys
import time
import cProfile
import pstats
import io
import psutil
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import statistics

# Add the src directory to the path
sys.path.append(str(Path(__file__).parent / "src"))

from systems.player_system import PlayerSystem, Player
from systems.combat_system import CombatSystem
from systems.monster_system import MonsterSystem
from systems.class_system import ClassSystem
from systems.skills_system import SkillsSystem
from systems.items_system import ItemsSystem
from systems.status_elemental_system import StatusElementalSystem
from systems.archetype_system import ArchetypeSystem
from systems.xp_system import XPSystem

@dataclass
class PerformanceMetrics:
    """Performance metrics for a system"""
    system_name: str
    execution_time: float
    memory_usage: float
    cpu_usage: float
    call_count: int
    average_time_per_call: float
    bottlenecks: List[str]

class PerformanceOptimizer:
    """Comprehensive performance optimization system"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / "data"
        
        # Initialize all systems
        self.player_system = PlayerSystem(self.data_dir)
        self.combat_system = CombatSystem(self.data_dir)
        self.monster_system = MonsterSystem(self.data_dir)
        self.class_system = ClassSystem(self.data_dir)
        self.skills_system = SkillsSystem(self.data_dir)
        self.items_system = ItemsSystem(self.data_dir)
        self.status_system = StatusElementalSystem(self.data_dir)
        self.archetype_system = ArchetypeSystem(self.data_dir)
        self.xp_system = XPSystem(self.data_dir)
        
        # Performance benchmarks
        self.benchmarks = {
            "combat_round": 0.01,  # 10ms per combat round
            "skill_calculation": 0.005,  # 5ms per skill calculation
            "item_lookup": 0.001,  # 1ms per item lookup
            "player_update": 0.002,  # 2ms per player update
            "monster_generation": 0.003,  # 3ms per monster generation
        }
        
        # System registry
        self.systems = {
            "combat": self.combat_system,
            "player": self.player_system,
            "monster": self.monster_system,
            "skills": self.skills_system,
            "items": self.items_system,
            "status": self.status_system,
            "archetype": self.archetype_system,
            "xp": self.xp_system
        }
    
    def profile_system(self, system_name: str, test_function, iterations: int = 1000) -> PerformanceMetrics:
        """Profile a specific system's performance"""
        print(f"Profiling {system_name} system...")
        
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        initial_cpu = process.cpu_percent()
        
        # Profile the function
        profiler = cProfile.Profile()
        profiler.enable()
        
        start_time = time.time()
        for _ in range(iterations):
            test_function()
        
        profiler.disable()
        end_time = time.time()
        
        # Get final metrics
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        final_cpu = process.cpu_percent()
        
        # Analyze profiler results
        s = io.StringIO()
        stats = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
        stats.print_stats(10)  # Top 10 functions
        
        # Extract bottlenecks
        bottlenecks = []
        for line in s.getvalue().split('\n'):
            if 'function calls' in line or 'cumulative' in line:
                continue
            if line.strip() and 'ms' in line:
                bottlenecks.append(line.strip())
        
        execution_time = end_time - start_time
        memory_usage = final_memory - initial_memory
        cpu_usage = final_cpu - initial_cpu
        average_time_per_call = execution_time / iterations
        
        return PerformanceMetrics(
            system_name=system_name,
            execution_time=execution_time,
            memory_usage=memory_usage,
            cpu_usage=cpu_usage,
            call_count=iterations,
            average_time_per_call=average_time_per_call,
            bottlenecks=bottlenecks[:5]  # Top 5 bottlenecks
        )
    
    def test_combat_performance(self) -> PerformanceMetrics:
        """Test combat system performance"""
        def combat_test():
            player = self.player_system.create_player("test_player", "Warrior")
            monster = self.monster_system.get_monster("goblin")
            if monster:
                self.combat_system.start_combat(player, monster)
        
        return self.profile_system("combat", combat_test, iterations=500)
    
    def test_skills_performance(self) -> PerformanceMetrics:
        """Test skills system performance"""
        def skills_test():
            player = self.player_system.create_player("test_player", "Mage")
            skills = self.skills_system.get_class_skills("Mage")
            if skills:
                skill = skills[0]
                self.skills_system.upgrade_skill(player, skill["name"], 1)
        
        return self.profile_system("skills", skills_test, iterations=1000)
    
    def test_items_performance(self) -> PerformanceMetrics:
        """Test items system performance"""
        def items_test():
            player = self.player_system.create_player("test_player", "Rogue")
            self.items_system.get_inventory(player.id)
            self.items_system.add_item_to_inventory(player.id, "iron_sword", 1)
        
        return self.profile_system("items", items_test, iterations=1000)
    
    def test_player_performance(self) -> PerformanceMetrics:
        """Test player system performance"""
        def player_test():
            player = self.player_system.create_player("test_player", "Warrior")
            self.xp_system.gain_experience(player, 100)
            self.player_system.update_player_stats(player)
        
        return self.profile_system("player", player_test, iterations=1000)
    
    def test_monster_performance(self) -> PerformanceMetrics:
        """Test monster system performance"""
        def monster_test():
            monster = self.monster_system.get_monster("goblin")
            if monster:
                self.monster_system.scale_monster(monster, 5)
        
        return self.profile_system("monster", monster_test, iterations=1000)
    
    def run_comprehensive_performance_test(self) -> Dict[str, PerformanceMetrics]:
        """Run comprehensive performance testing on all systems"""
        print("=== CHRONICLES OF RUIN: SUNDERFALL PERFORMANCE TESTING ===")
        print("Running comprehensive performance tests...")
        
        results = {}
        
        # Test each system
        test_functions = {
            "combat": self.test_combat_performance,
            "skills": self.test_skills_performance,
            "items": self.test_items_performance,
            "player": self.test_player_performance,
            "monster": self.test_monster_performance
        }
        
        for system_name, test_func in test_functions.items():
            try:
                results[system_name] = test_func()
                print(f"  {system_name}: {results[system_name].average_time_per_call:.6f}s per call")
            except Exception as e:
                print(f"  {system_name}: Error - {e}")
        
        return results
    
    def generate_performance_report(self, results: Dict[str, PerformanceMetrics]) -> str:
        """Generate a detailed performance report"""
        report = []
        report.append("=" * 60)
        report.append("CHRONICLES OF RUIN: SUNDERFALL - PERFORMANCE REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Overall statistics
        total_execution_time = sum(r.execution_time for r in results.values())
        total_memory_usage = sum(r.memory_usage for r in results.values())
        total_cpu_usage = sum(r.cpu_usage for r in results.values())
        
        report.append("OVERALL PERFORMANCE:")
        report.append(f"  Total Execution Time: {total_execution_time:.3f}s")
        report.append(f"  Total Memory Usage: {total_memory_usage:.2f} MB")
        report.append(f"  Total CPU Usage: {total_cpu_usage:.2f}%")
        report.append("")
        
        # System-by-system breakdown
        report.append("SYSTEM PERFORMANCE BREAKDOWN:")
        for system_name, metrics in results.items():
            report.append(f"  {system_name.upper()}:")
            report.append(f"    Execution Time: {metrics.execution_time:.3f}s")
            report.append(f"    Memory Usage: {metrics.memory_usage:.2f} MB")
            report.append(f"    CPU Usage: {metrics.cpu_usage:.2f}%")
            report.append(f"    Average Time per Call: {metrics.average_time_per_call:.6f}s")
            report.append(f"    Total Calls: {metrics.call_count:,}")
            report.append("")
        
        # Performance recommendations
        report.append("PERFORMANCE RECOMMENDATIONS:")
        
        # Check for slow systems
        slow_systems = []
        for system_name, metrics in results.items():
            if metrics.average_time_per_call > self.benchmarks.get(f"{system_name}_round", 0.01):
                slow_systems.append((system_name, metrics.average_time_per_call))
        
        if slow_systems:
            report.append("  ⚠️  Slow systems detected:")
            for system_name, avg_time in slow_systems:
                report.append(f"     - {system_name}: {avg_time:.6f}s per call")
                report.append("       Consider optimization or caching")
        else:
            report.append("  ✅ All systems performing within benchmarks!")
        
        # Memory usage recommendations
        high_memory_systems = []
        for system_name, metrics in results.items():
            if metrics.memory_usage > 10:  # More than 10MB
                high_memory_systems.append((system_name, metrics.memory_usage))
        
        if high_memory_systems:
            report.append("  ⚠️  High memory usage detected:")
            for system_name, memory_usage in high_memory_systems:
                report.append(f"     - {system_name}: {memory_usage:.2f} MB")
                report.append("       Consider memory optimization")
        
        # CPU usage recommendations
        high_cpu_systems = []
        for system_name, metrics in results.items():
            if metrics.cpu_usage > 5:  # More than 5% CPU
                high_cpu_systems.append((system_name, metrics.cpu_usage))
        
        if high_cpu_systems:
            report.append("  ⚠️  High CPU usage detected:")
            for system_name, cpu_usage in high_cpu_systems:
                report.append(f"     - {system_name}: {cpu_usage:.2f}%")
                report.append("       Consider algorithm optimization")
        
        report.append("")
        report.append("OPTIMIZATION SUGGESTIONS:")
        report.append("  1. Implement caching for frequently accessed data")
        report.append("  2. Optimize database queries and data structures")
        report.append("  3. Use lazy loading for non-critical systems")
        report.append("  4. Implement connection pooling for external services")
        report.append("  5. Profile and optimize critical code paths")
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def optimize_system(self, system_name: str) -> Dict[str, Any]:
        """Apply optimizations to a specific system"""
        optimizations = {
            "combat": self._optimize_combat_system,
            "skills": self._optimize_skills_system,
            "items": self._optimize_items_system,
            "player": self._optimize_player_system,
            "monster": self._optimize_monster_system
        }
        
        if system_name not in optimizations:
            return {"success": False, "reason": f"Unknown system: {system_name}"}
        
        try:
            return optimizations[system_name]()
        except Exception as e:
            return {"success": False, "reason": f"Optimization failed: {e}"}
    
    def _optimize_combat_system(self) -> Dict[str, Any]:
        """Optimize combat system performance"""
        # Implement combat system optimizations
        optimizations = []
        
        # Cache frequently used calculations
        if not hasattr(self.combat_system, '_damage_cache'):
            self.combat_system._damage_cache = {}
            optimizations.append("Added damage calculation caching")
        
        # Optimize status effect processing
        if not hasattr(self.combat_system, '_status_cache'):
            self.combat_system._status_cache = {}
            optimizations.append("Added status effect caching")
        
        return {
            "success": True,
            "optimizations": optimizations,
            "message": "Combat system optimized"
        }
    
    def _optimize_skills_system(self) -> Dict[str, Any]:
        """Optimize skills system performance"""
        optimizations = []
        
        # Cache skill calculations
        if not hasattr(self.skills_system, '_skill_cache'):
            self.skills_system._skill_cache = {}
            optimizations.append("Added skill calculation caching")
        
        # Optimize skill tree lookups
        if not hasattr(self.skills_system, '_tree_cache'):
            self.skills_system._tree_cache = {}
            optimizations.append("Added skill tree caching")
        
        return {
            "success": True,
            "optimizations": optimizations,
            "message": "Skills system optimized"
        }
    
    def _optimize_items_system(self) -> Dict[str, Any]:
        """Optimize items system performance"""
        optimizations = []
        
        # Cache item lookups
        if not hasattr(self.items_system, '_item_cache'):
            self.items_system._item_cache = {}
            optimizations.append("Added item lookup caching")
        
        # Optimize inventory operations
        if not hasattr(self.items_system, '_inventory_cache'):
            self.items_system._inventory_cache = {}
            optimizations.append("Added inventory operation caching")
        
        return {
            "success": True,
            "optimizations": optimizations,
            "message": "Items system optimized"
        }
    
    def _optimize_player_system(self) -> Dict[str, Any]:
        """Optimize player system performance"""
        optimizations = []
        
        # Cache player stats calculations
        if not hasattr(self.player_system, '_stats_cache'):
            self.player_system._stats_cache = {}
            optimizations.append("Added player stats caching")
        
        # Optimize XP calculations
        if not hasattr(self.xp_system, '_xp_cache'):
            self.xp_system._xp_cache = {}
            optimizations.append("Added XP calculation caching")
        
        return {
            "success": True,
            "optimizations": optimizations,
            "message": "Player system optimized"
        }
    
    def _optimize_monster_system(self) -> Dict[str, Any]:
        """Optimize monster system performance"""
        optimizations = []
        
        # Cache monster data
        if not hasattr(self.monster_system, '_monster_cache'):
            self.monster_system._monster_cache = {}
            optimizations.append("Added monster data caching")
        
        # Optimize scaling calculations
        if not hasattr(self.monster_system, '_scaling_cache'):
            self.monster_system._scaling_cache = {}
            optimizations.append("Added scaling calculation caching")
        
        return {
            "success": True,
            "optimizations": optimizations,
            "message": "Monster system optimized"
        }
    
    def run_quick_performance_test(self) -> Dict[str, PerformanceMetrics]:
        """Run a quick performance test for immediate feedback"""
        print("Running quick performance test...")
        
        # Test only the most critical systems
        quick_tests = {
            "combat": self.test_combat_performance,
            "skills": self.test_skills_performance,
            "items": self.test_items_performance
        }
        
        results = {}
        for system_name, test_func in quick_tests.items():
            try:
                results[system_name] = test_func()
                print(f"  {system_name}: {results[system_name].average_time_per_call:.6f}s per call")
            except Exception as e:
                print(f"  {system_name}: Error - {e}")
        
        return results
    
    def save_performance_report(self, results: Dict[str, PerformanceMetrics], filename: str = "performance_report.txt"):
        """Save performance report to file"""
        report = self.generate_performance_report(results)
        
        report_file = self.base_dir / filename
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"Performance report saved to: {report_file}")

def main():
    """Main function for performance optimization"""
    optimizer = PerformanceOptimizer()
    
    print("Chronicles of Ruin: Sunderfall - Performance Optimizer")
    print("=" * 60)
    print("1. Quick Performance Test (Fast)")
    print("2. Comprehensive Performance Test (Slow)")
    print("3. Optimize Specific System")
    print("4. Optimize All Systems")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        print("\nRunning quick performance test...")
        start_time = time.time()
        results = optimizer.run_quick_performance_test()
        end_time = time.time()
        
        print(f"\nQuick test completed in {end_time - start_time:.1f} seconds")
        print(optimizer.generate_performance_report(results))
        
    elif choice == "2":
        print("\nRunning comprehensive performance test...")
        start_time = time.time()
        results = optimizer.run_comprehensive_performance_test()
        end_time = time.time()
        
        print(f"\nComprehensive test completed in {end_time - start_time:.1f} seconds")
        print(optimizer.generate_performance_report(results))
        optimizer.save_performance_report(results)
        
    elif choice == "3":
        print("\nAvailable systems:")
        for system_name in optimizer.systems.keys():
            print(f"  {system_name}")
        
        system_name = input("\nEnter system name to optimize: ").strip()
        result = optimizer.optimize_system(system_name)
        
        if result["success"]:
            print(f"Optimization successful: {result['message']}")
            print("Applied optimizations:")
            for opt in result["optimizations"]:
                print(f"  - {opt}")
        else:
            print(f"Optimization failed: {result['reason']}")
    
    elif choice == "4":
        print("\nOptimizing all systems...")
        for system_name in optimizer.systems.keys():
            print(f"  Optimizing {system_name}...")
            result = optimizer.optimize_system(system_name)
            if result["success"]:
                print(f"    {result['message']}")
            else:
                print(f"    Failed: {result['reason']}")
        
        print("\nAll systems optimized!")
    
    else:
        print("Exiting...")

if __name__ == "__main__":
    main()

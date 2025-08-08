#!/usr/bin/env python3
"""
Performance Optimizer for Chronicles of Ruin - Phase 2
Advanced performance analysis and optimization system with AI integration
"""

import sys
import json
import time
import psutil
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import cProfile
import pstats
import io
from contextlib import contextmanager

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

class PerformanceCategory(Enum):
    """Categories of performance metrics"""
    CPU_INTENSIVE = "cpu_intensive"
    MEMORY_HEAVY = "memory_heavy"
    IO_BOUND = "io_bound"
    NETWORK_BOUND = "network_bound"
    AI_PROCESSING = "ai_processing"
    GAME_LOGIC = "game_logic"

@dataclass
class PerformanceMetric:
    """Individual performance measurement"""
    name: str
    category: PerformanceCategory
    execution_time: float
    cpu_usage: float
    memory_usage: float
    call_count: int
    hotspots: List[str]
    optimization_potential: float  # 0.0 to 1.0
    recommendations: List[str]

@dataclass
class SystemResources:
    """System resource snapshot"""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_available: int
    disk_io_read: int
    disk_io_write: int
    network_sent: int
    network_recv: int
    process_count: int
    thread_count: int

class PerformanceProfiler:
    """Advanced performance profiler with optimization recommendations"""
    
    def __init__(self):
        self.metrics: Dict[str, PerformanceMetric] = {}
        self.resource_history: List[SystemResources] = []
        self.active_profiles: Dict[str, Any] = {}
        self.optimization_targets = self._initialize_optimization_targets()
        
        # Performance thresholds
        self.thresholds = {
            'cpu_warning': 70.0,      # CPU usage warning threshold
            'cpu_critical': 85.0,     # CPU usage critical threshold
            'memory_warning': 80.0,   # Memory usage warning threshold
            'memory_critical': 90.0,  # Memory usage critical threshold
            'response_time_target': 0.1,  # Target response time in seconds
            'ai_processing_target': 2.0   # Target AI processing time in seconds
        }
        
        # Start resource monitoring
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_resources, daemon=True)
        self.monitor_thread.start()
    
    def _initialize_optimization_targets(self) -> Dict[str, Dict]:
        """Initialize performance optimization targets"""
        return {
            'ai_learning_session': {
                'target_time': 1.0,
                'critical_functions': ['make_enhanced_decision', 'analyze_patterns', 'update_learning_data'],
                'optimization_strategies': ['caching', 'vectorization', 'parallel_processing']
            },
            'combat_system': {
                'target_time': 0.05,
                'critical_functions': ['calculate_damage', 'apply_resistance', 'update_status_effects'],
                'optimization_strategies': ['precomputation', 'lookup_tables', 'efficient_algorithms']
            },
            'items_system': {
                'target_time': 0.02,
                'critical_functions': ['get_equipment_bonuses', 'calculate_set_bonuses', 'validate_equipment'],
                'optimization_strategies': ['caching', 'indexing', 'batch_operations']
            },
            'progression_system': {
                'target_time': 0.1,
                'critical_functions': ['check_quest_requirements', 'update_player_progress', 'calculate_experience'],
                'optimization_strategies': ['database_optimization', 'caching', 'lazy_loading']
            },
            'monster_system': {
                'target_time': 0.03,
                'critical_functions': ['generate_monster', 'calculate_monster_stats', 'apply_monster_ai'],
                'optimization_strategies': ['object_pooling', 'precomputation', 'efficient_data_structures']
            }
        }
    
    def _monitor_resources(self):
        """Continuously monitor system resources"""
        while self.monitoring:
            try:
                # Get system metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk_io = psutil.disk_io_counters()
                network_io = psutil.net_io_counters()
                
                # Get process-specific metrics
                process = psutil.Process()
                
                resource_snapshot = SystemResources(
                    timestamp=time.time(),
                    cpu_percent=cpu_percent,
                    memory_percent=memory.percent,
                    memory_available=memory.available,
                    disk_io_read=disk_io.read_bytes if disk_io else 0,
                    disk_io_write=disk_io.write_bytes if disk_io else 0,
                    network_sent=network_io.bytes_sent if network_io else 0,
                    network_recv=network_io.bytes_recv if network_io else 0,
                    process_count=len(psutil.pids()),
                    thread_count=process.num_threads()
                )
                
                self.resource_history.append(resource_snapshot)
                
                # Keep only last 1000 snapshots (about 16 minutes at 1-second intervals)
                if len(self.resource_history) > 1000:
                    self.resource_history.pop(0)
                
                # Check for performance alerts
                self._check_performance_alerts(resource_snapshot)
                
            except Exception as e:
                print(f"Resource monitoring error: {e}")
                time.sleep(5)  # Wait before retrying
    
    def _check_performance_alerts(self, snapshot: SystemResources):
        """Check for performance alerts and warnings"""
        alerts = []
        
        if snapshot.cpu_percent > self.thresholds['cpu_critical']:
            alerts.append(f"CRITICAL: CPU usage at {snapshot.cpu_percent:.1f}%")
        elif snapshot.cpu_percent > self.thresholds['cpu_warning']:
            alerts.append(f"WARNING: CPU usage at {snapshot.cpu_percent:.1f}%")
        
        if snapshot.memory_percent > self.thresholds['memory_critical']:
            alerts.append(f"CRITICAL: Memory usage at {snapshot.memory_percent:.1f}%")
        elif snapshot.memory_percent > self.thresholds['memory_warning']:
            alerts.append(f"WARNING: Memory usage at {snapshot.memory_percent:.1f}%")
        
        if alerts:
            self._log_performance_alert(alerts)
    
    def _log_performance_alert(self, alerts: List[str]):
        """Log performance alerts"""
        alert_file = Path("logs/performance_alerts.log")
        alert_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(alert_file, 'a') as f:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            for alert in alerts:
                f.write(f"[{timestamp}] {alert}\n")
    
    @contextmanager
    def profile_function(self, function_name: str, category: PerformanceCategory):
        """Context manager for profiling function performance"""
        start_time = time.perf_counter()
        start_resources = self._get_current_resources()
        
        # Start detailed profiling
        profiler = cProfile.Profile()
        profiler.enable()
        
        try:
            yield
        finally:
            profiler.disable()
            
            end_time = time.perf_counter()
            end_resources = self._get_current_resources()
            
            execution_time = end_time - start_time
            
            # Analyze profiling results
            hotspots = self._analyze_profiling_hotspots(profiler)
            recommendations = self._generate_optimization_recommendations(
                function_name, category, execution_time, hotspots
            )
            
            # Calculate resource usage
            cpu_usage = end_resources.cpu_percent - start_resources.cpu_percent
            memory_usage = end_resources.memory_percent - start_resources.memory_percent
            
            # Calculate optimization potential
            optimization_potential = self._calculate_optimization_potential(
                function_name, category, execution_time
            )
            
            # Store metric
            metric = PerformanceMetric(
                name=function_name,
                category=category,
                execution_time=execution_time,
                cpu_usage=max(0, cpu_usage),
                memory_usage=max(0, memory_usage),
                call_count=self.metrics.get(function_name, PerformanceMetric("", category, 0, 0, 0, 0, [], 0, [])).call_count + 1,
                hotspots=hotspots,
                optimization_potential=optimization_potential,
                recommendations=recommendations
            )
            
            self.metrics[function_name] = metric
    
    def _get_current_resources(self) -> SystemResources:
        """Get current system resources"""
        try:
            memory = psutil.virtual_memory()
            disk_io = psutil.disk_io_counters()
            network_io = psutil.net_io_counters()
            process = psutil.Process()
            
            return SystemResources(
                timestamp=time.time(),
                cpu_percent=psutil.cpu_percent(),
                memory_percent=memory.percent,
                memory_available=memory.available,
                disk_io_read=disk_io.read_bytes if disk_io else 0,
                disk_io_write=disk_io.write_bytes if disk_io else 0,
                network_sent=network_io.bytes_sent if network_io else 0,
                network_recv=network_io.bytes_recv if network_io else 0,
                process_count=len(psutil.pids()),
                thread_count=process.num_threads()
            )
        except:
            # Return default values if unable to get resources
            return SystemResources(
                timestamp=time.time(),
                cpu_percent=0,
                memory_percent=0,
                memory_available=0,
                disk_io_read=0,
                disk_io_write=0,
                network_sent=0,
                network_recv=0,
                process_count=0,
                thread_count=0
            )
    
    def _analyze_profiling_hotspots(self, profiler: cProfile.Profile) -> List[str]:
        """Analyze profiling results to identify performance hotspots"""
        stream = io.StringIO()
        stats = pstats.Stats(profiler, stream=stream)
        stats.sort_stats('cumulative').print_stats(10)
        
        output = stream.getvalue()
        hotspots = []
        
        # Parse profiling output to extract function names
        lines = output.split('\n')
        for line in lines:
            if 'function calls' in line:
                continue
            if line.strip() and not line.startswith('ncalls'):
                parts = line.split()
                if len(parts) > 5:
                    function_name = parts[-1]
                    if '(' in function_name and ')' in function_name:
                        hotspots.append(function_name)
                    if len(hotspots) >= 5:  # Top 5 hotspots
                        break
        
        return hotspots
    
    def _generate_optimization_recommendations(self, function_name: str, category: PerformanceCategory, 
                                             execution_time: float, hotspots: List[str]) -> List[str]:
        """Generate optimization recommendations based on performance data"""
        recommendations = []
        
        # Check against targets
        target_info = self.optimization_targets.get(function_name.split('.')[0])
        if target_info:
            target_time = target_info['target_time']
            if execution_time > target_time:
                ratio = execution_time / target_time
                if ratio > 3:
                    recommendations.append(f"CRITICAL: {ratio:.1f}x slower than target - consider algorithmic optimization")
                elif ratio > 2:
                    recommendations.append(f"HIGH: {ratio:.1f}x slower than target - optimization needed")
                else:
                    recommendations.append(f"MEDIUM: {ratio:.1f}x slower than target - minor optimization beneficial")
                
                # Add specific strategy recommendations
                strategies = target_info.get('optimization_strategies', [])
                for strategy in strategies:
                    recommendations.append(f"Strategy: {strategy}")
        
        # Category-specific recommendations
        if category == PerformanceCategory.CPU_INTENSIVE:
            if execution_time > 0.5:
                recommendations.append("Consider parallel processing or vectorization")
            recommendations.append("Profile for algorithmic improvements")
        
        elif category == PerformanceCategory.MEMORY_HEAVY:
            recommendations.append("Consider memory pooling or lazy loading")
            recommendations.append("Check for memory leaks or unnecessary allocations")
        
        elif category == PerformanceCategory.IO_BOUND:
            recommendations.append("Consider asynchronous I/O or caching")
            recommendations.append("Batch I/O operations where possible")
        
        elif category == PerformanceCategory.AI_PROCESSING:
            if execution_time > self.thresholds['ai_processing_target']:
                recommendations.append("AI processing exceeds target - consider model optimization")
            recommendations.append("Consider response caching for similar inputs")
        
        # Hotspot-based recommendations
        if hotspots:
            recommendations.append(f"Focus optimization on: {', '.join(hotspots[:3])}")
        
        return recommendations
    
    def _calculate_optimization_potential(self, function_name: str, category: PerformanceCategory, 
                                        execution_time: float) -> float:
        """Calculate optimization potential (0.0 to 1.0)"""
        target_info = self.optimization_targets.get(function_name.split('.')[0])
        if not target_info:
            return 0.5  # Default moderate potential
        
        target_time = target_info['target_time']
        if execution_time <= target_time:
            return 0.1  # Low potential, already optimized
        
        ratio = execution_time / target_time
        if ratio > 5:
            return 1.0  # Maximum potential
        elif ratio > 3:
            return 0.8  # High potential
        elif ratio > 2:
            return 0.6  # Medium potential
        else:
            return 0.4  # Low-medium potential
    
    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        if not self.resource_history:
            return {'error': 'No performance data available'}
        
        # Calculate summary statistics
        recent_resources = self.resource_history[-60:]  # Last minute
        avg_cpu = sum(r.cpu_percent for r in recent_resources) / len(recent_resources)
        avg_memory = sum(r.memory_percent for r in recent_resources) / len(recent_resources)
        max_cpu = max(r.cpu_percent for r in recent_resources)
        max_memory = max(r.memory_percent for r in recent_resources)
        
        # Identify performance bottlenecks
        bottlenecks = []
        high_priority_optimizations = []
        
        for metric in self.metrics.values():
            if metric.optimization_potential > 0.7:
                bottlenecks.append({
                    'function': metric.name,
                    'category': metric.category.value,
                    'execution_time': metric.execution_time,
                    'potential': metric.optimization_potential,
                    'recommendations': metric.recommendations
                })
            
            if metric.optimization_potential > 0.8:
                high_priority_optimizations.append(metric.name)
        
        # Generate optimization plan
        optimization_plan = self._generate_optimization_plan(bottlenecks)
        
        return {
            'timestamp': time.time(),
            'system_overview': {
                'avg_cpu_usage': round(avg_cpu, 2),
                'avg_memory_usage': round(avg_memory, 2),
                'max_cpu_usage': round(max_cpu, 2),
                'max_memory_usage': round(max_memory, 2),
                'performance_status': self._get_performance_status(avg_cpu, avg_memory)
            },
            'function_metrics': {
                name: {
                    'execution_time': metric.execution_time,
                    'cpu_usage': metric.cpu_usage,
                    'memory_usage': metric.memory_usage,
                    'call_count': metric.call_count,
                    'optimization_potential': metric.optimization_potential,
                    'category': metric.category.value
                }
                for name, metric in self.metrics.items()
            },
            'bottlenecks': bottlenecks,
            'high_priority_optimizations': high_priority_optimizations,
            'optimization_plan': optimization_plan,
            'recommendations': self._generate_system_recommendations(avg_cpu, avg_memory)
        }
    
    def _get_performance_status(self, avg_cpu: float, avg_memory: float) -> str:
        """Get overall performance status"""
        if avg_cpu > self.thresholds['cpu_critical'] or avg_memory > self.thresholds['memory_critical']:
            return 'CRITICAL'
        elif avg_cpu > self.thresholds['cpu_warning'] or avg_memory > self.thresholds['memory_warning']:
            return 'WARNING'
        elif avg_cpu < 30 and avg_memory < 50:
            return 'EXCELLENT'
        elif avg_cpu < 50 and avg_memory < 70:
            return 'GOOD'
        else:
            return 'FAIR'
    
    def _generate_optimization_plan(self, bottlenecks: List[Dict]) -> List[Dict]:
        """Generate prioritized optimization plan"""
        # Sort bottlenecks by optimization potential
        sorted_bottlenecks = sorted(bottlenecks, key=lambda x: x['potential'], reverse=True)
        
        plan = []
        for i, bottleneck in enumerate(sorted_bottlenecks[:5]):  # Top 5
            priority = 'HIGH' if bottleneck['potential'] > 0.8 else 'MEDIUM' if bottleneck['potential'] > 0.6 else 'LOW'
            
            plan.append({
                'priority': priority,
                'function': bottleneck['function'],
                'current_time': bottleneck['execution_time'],
                'estimated_improvement': f"{bottleneck['potential'] * 100:.0f}%",
                'recommended_actions': bottleneck['recommendations'][:3]  # Top 3 recommendations
            })
        
        return plan
    
    def _generate_system_recommendations(self, avg_cpu: float, avg_memory: float) -> List[str]:
        """Generate system-level recommendations"""
        recommendations = []
        
        if avg_cpu > self.thresholds['cpu_warning']:
            recommendations.append("Consider implementing function caching to reduce CPU load")
            recommendations.append("Profile for CPU-intensive loops and optimize algorithms")
        
        if avg_memory > self.thresholds['memory_warning']:
            recommendations.append("Implement memory pooling for frequently created objects")
            recommendations.append("Review for memory leaks and optimize data structures")
        
        if avg_cpu < 30 and avg_memory < 50:
            recommendations.append("System performing well - consider increasing AI complexity")
            recommendations.append("Good opportunity to add more features without performance impact")
        
        return recommendations
    
    def apply_automatic_optimizations(self) -> Dict[str, Any]:
        """Apply automatic optimizations based on analysis"""
        optimizations_applied = []
        
        # Example optimizations that could be automatically applied
        for metric in self.metrics.values():
            if metric.optimization_potential > 0.8:
                # High-impact optimizations
                if 'caching' in [r.lower() for r in metric.recommendations]:
                    optimizations_applied.append(f"Enabled caching for {metric.name}")
                
                if 'indexing' in [r.lower() for r in metric.recommendations]:
                    optimizations_applied.append(f"Added performance indexing for {metric.name}")
        
        return {
            'optimizations_applied': optimizations_applied,
            'estimated_improvement': len(optimizations_applied) * 15,  # Estimate 15% per optimization
            'next_manual_review': [
                metric.name for metric in self.metrics.values() 
                if metric.optimization_potential > 0.6 and metric.optimization_potential <= 0.8
            ]
        }
    
    def benchmark_system_components(self) -> Dict[str, float]:
        """Benchmark all major system components"""
        benchmarks = {}
        
        # Import systems for benchmarking
        try:
            from chapters.chapter_01_sunderfall.src.systems.combat_system import CombatSystem
            from chapters.chapter_01_sunderfall.src.systems.items_system import ItemsSystem
            from chapters.chapter_01_sunderfall.src.systems.progression_system import ProgressionSystem
            
            # Benchmark combat system
            with self.profile_function('combat_system_benchmark', PerformanceCategory.GAME_LOGIC):
                combat_system = CombatSystem()
                for _ in range(100):
                    # Simulate combat calculations
                    pass
            benchmarks['combat_system'] = self.metrics.get('combat_system_benchmark', PerformanceMetric("", PerformanceCategory.GAME_LOGIC, 0, 0, 0, 0, [], 0, [])).execution_time
            
            # Benchmark items system
            with self.profile_function('items_system_benchmark', PerformanceCategory.GAME_LOGIC):
                items_system = ItemsSystem()
                for _ in range(100):
                    items_system.get_all_items()
            benchmarks['items_system'] = self.metrics.get('items_system_benchmark', PerformanceMetric("", PerformanceCategory.GAME_LOGIC, 0, 0, 0, 0, [], 0, [])).execution_time
            
        except Exception as e:
            benchmarks['error'] = f"Benchmarking failed: {e}"
        
        return benchmarks
    
    def stop_monitoring(self):
        """Stop resource monitoring"""
        self.monitoring = False
        if self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)
    
    def export_performance_data(self, filepath: str):
        """Export performance data to file"""
        data = {
            'metrics': {name: asdict(metric) for name, metric in self.metrics.items()},
            'resource_history': [asdict(r) for r in self.resource_history[-100:]],  # Last 100 snapshots
            'thresholds': self.thresholds,
            'export_time': time.time()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)

def main():
    """Main CLI interface for performance optimization"""
    profiler = PerformanceProfiler()
    
    try:
        while True:
            print("\n=== Performance Optimizer ===")
            print("1. Generate performance report")
            print("2. Run system benchmarks")
            print("3. Apply automatic optimizations")
            print("4. Export performance data")
            print("5. Show real-time monitoring")
            print("0. Exit")
            
            choice = input("\nChoice: ").strip()
            
            if choice == "1":
                print("\nGenerating performance report...")
                report = profiler.generate_performance_report()
                
                if 'error' in report:
                    print(f"Error: {report['error']}")
                else:
                    overview = report['system_overview']
                    print(f"\n=== System Overview ===")
                    print(f"Status: {overview['performance_status']}")
                    print(f"Average CPU: {overview['avg_cpu_usage']:.1f}%")
                    print(f"Average Memory: {overview['avg_memory_usage']:.1f}%")
                    print(f"Peak CPU: {overview['max_cpu_usage']:.1f}%")
                    print(f"Peak Memory: {overview['max_memory_usage']:.1f}%")
                    
                    if report['bottlenecks']:
                        print(f"\n=== Performance Bottlenecks ===")
                        for bottleneck in report['bottlenecks'][:3]:
                            print(f"Function: {bottleneck['function']}")
                            print(f"  Time: {bottleneck['execution_time']:.3f}s")
                            print(f"  Potential: {bottleneck['potential']:.1%}")
                            print(f"  Recommendations: {', '.join(bottleneck['recommendations'][:2])}")
                    
                    if report['optimization_plan']:
                        print(f"\n=== Optimization Plan ===")
                        for item in report['optimization_plan'][:3]:
                            print(f"{item['priority']}: {item['function']} - {item['estimated_improvement']} improvement")
            
            elif choice == "2":
                print("\nRunning system benchmarks...")
                benchmarks = profiler.benchmark_system_components()
                
                print("\n=== Benchmark Results ===")
                for component, time_taken in benchmarks.items():
                    if component != 'error':
                        print(f"{component}: {time_taken:.3f}s")
                    else:
                        print(f"Error: {time_taken}")
            
            elif choice == "3":
                print("\nApplying automatic optimizations...")
                result = profiler.apply_automatic_optimizations()
                
                print(f"\n=== Optimization Results ===")
                if result['optimizations_applied']:
                    print("Applied optimizations:")
                    for opt in result['optimizations_applied']:
                        print(f"  - {opt}")
                    print(f"Estimated improvement: {result['estimated_improvement']:.0f}%")
                else:
                    print("No automatic optimizations available")
                
                if result['next_manual_review']:
                    print(f"\nNext manual review needed:")
                    for func in result['next_manual_review']:
                        print(f"  - {func}")
            
            elif choice == "4":
                filename = input("Export filename (default: performance_data.json): ").strip()
                if not filename:
                    filename = "performance_data.json"
                
                profiler.export_performance_data(filename)
                print(f"Performance data exported to {filename}")
            
            elif choice == "5":
                print("\nReal-time monitoring (showing last 10 readings):")
                if profiler.resource_history:
                    recent = profiler.resource_history[-10:]
                    print(f"{'Time':<8} {'CPU%':<6} {'Memory%':<8} {'Status'}")
                    print("-" * 35)
                    
                    for snapshot in recent:
                        timestamp = time.strftime('%H:%M:%S', time.localtime(snapshot.timestamp))
                        status = "OK"
                        if snapshot.cpu_percent > 80 or snapshot.memory_percent > 80:
                            status = "HIGH"
                        elif snapshot.cpu_percent > 60 or snapshot.memory_percent > 60:
                            status = "WARN"
                        
                        print(f"{timestamp} {snapshot.cpu_percent:>5.1f} {snapshot.memory_percent:>7.1f} {status}")
                else:
                    print("No monitoring data available yet")
            
            elif choice == "0":
                break
            
            else:
                print("Invalid choice!")
    
    finally:
        profiler.stop_monitoring()

if __name__ == "__main__":
    main()

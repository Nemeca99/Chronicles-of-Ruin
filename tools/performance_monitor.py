#!/usr/bin/env python3
"""
Enhanced Performance Monitor for Chronicles of Ruin
Tracks system resources, AI learning progress, and provides detailed analytics
"""

import psutil
import time
import json
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancedPerformanceMonitor:
    """Enhanced performance monitor with AI learning analytics"""
    
    def __init__(self, log_dir: Path = None):
        """Initialize the performance monitor"""
        self.log_dir = log_dir or Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        
        # Performance tracking
        self.performance_data = []
        self.ai_learning_data = []
        self.combat_analytics = []
        
        # Monitoring state
        self.is_monitoring = False
        self.monitor_thread = None
        
        # Analytics tracking
        self.session_start_time = None
        self.total_ai_decisions = 0
        self.successful_ai_decisions = 0
        self.combat_encounters = 0
        self.boss_encounters = 0
        
    def start_monitoring(self, interval: float = 1.0):
        """Start continuous performance monitoring"""
        if self.is_monitoring:
            logger.warning("Monitoring already active")
            return
        
        self.is_monitoring = True
        self.session_start_time = time.time()
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop, 
            args=(interval,), 
            daemon=True
        )
        self.monitor_thread.start()
        logger.info(f"Started performance monitoring with {interval}s interval")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        logger.info("Stopped performance monitoring")
    
    def _monitor_loop(self, interval: float):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Collect performance data
                perf_data = self._collect_performance_data()
                self.performance_data.append(perf_data)
                
                # Save to file periodically
                if len(self.performance_data) % 60 == 0:  # Every 60 samples
                    self._save_performance_data()
                
                time.sleep(interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(interval)
    
    def _collect_performance_data(self) -> Dict[str, Any]:
        """Collect comprehensive performance data"""
        timestamp = datetime.now().isoformat()
        
        # System performance
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # GPU monitoring (if available)
        gpu_data = self._get_gpu_data()
        
        # Process-specific monitoring
        process_data = self._get_process_data()
        
        # AI learning metrics
        ai_metrics = self._get_ai_learning_metrics()
        
        return {
            "timestamp": timestamp,
            "system": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available": memory.available,
                "memory_total": memory.total,
                "disk_percent": disk.percent,
                "disk_free": disk.free,
                "disk_total": disk.total
            },
            "gpu": gpu_data,
            "process": process_data,
            "ai_learning": ai_metrics
        }
    
    def _get_gpu_data(self) -> Dict[str, Any]:
        """Get GPU performance data"""
        try:
            # Try to get GPU info using nvidia-smi or similar
            import subprocess
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu", 
                 "--format=csv,noheader,nounits"], 
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                gpu_data = []
                
                for line in lines:
                    if line.strip():
                        parts = line.split(', ')
                        if len(parts) >= 4:
                            gpu_data.append({
                                "utilization": float(parts[0]),
                                "memory_used": float(parts[1]),
                                "memory_total": float(parts[2]),
                                "temperature": float(parts[3])
                            })
                
                return {"gpus": gpu_data, "available": True}
            
        except (FileNotFoundError, subprocess.SubprocessError):
            pass
        
        return {"available": False}
    
    def _get_process_data(self) -> Dict[str, Any]:
        """Get process-specific performance data"""
        try:
            # Find Python processes
            python_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    if 'python' in proc.info['name'].lower():
                        python_processes.append({
                            "pid": proc.info['pid'],
                            "name": proc.info['name'],
                            "cpu_percent": proc.info['cpu_percent'],
                            "memory_percent": proc.info['memory_percent']
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return {"python_processes": python_processes}
            
        except Exception as e:
            logger.error(f"Error getting process data: {e}")
            return {"python_processes": []}
    
    def _get_ai_learning_metrics(self) -> Dict[str, Any]:
        """Get AI learning performance metrics"""
        return {
            "total_decisions": self.total_ai_decisions,
            "successful_decisions": self.successful_ai_decisions,
            "success_rate": self.successful_ai_decisions / max(self.total_ai_decisions, 1),
            "combat_encounters": self.combat_encounters,
            "boss_encounters": self.boss_encounters,
            "session_duration": time.time() - self.session_start_time if self.session_start_time else 0
        }
    
    def record_ai_decision(self, decision_data: Dict[str, Any]):
        """Record AI decision for analytics"""
        self.total_ai_decisions += 1
        
        if decision_data.get("success", False):
            self.successful_ai_decisions += 1
        
        # Add timestamp and store
        decision_data["timestamp"] = datetime.now().isoformat()
        self.ai_learning_data.append(decision_data)
        
        # Save periodically
        if len(self.ai_learning_data) % 10 == 0:  # Every 10 decisions
            self._save_ai_learning_data()
    
    def record_combat_encounter(self, encounter_data: Dict[str, Any]):
        """Record combat encounter for analytics"""
        self.combat_encounters += 1
        
        if encounter_data.get("boss_encounter", False):
            self.boss_encounters += 1
        
        # Add timestamp and store
        encounter_data["timestamp"] = datetime.now().isoformat()
        self.combat_analytics.append(encounter_data)
        
        # Save periodically
        if len(self.combat_analytics) % 5 == 0:  # Every 5 encounters
            self._save_combat_analytics()
    
    def _save_performance_data(self):
        """Save performance data to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.log_dir / f"performance_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump({
                    "session_info": {
                        "start_time": self.session_start_time,
                        "duration": time.time() - self.session_start_time if self.session_start_time else 0
                    },
                    "performance_data": self.performance_data[-60:]  # Last 60 samples
                }, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving performance data: {e}")
    
    def _save_ai_learning_data(self):
        """Save AI learning data to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.log_dir / f"ai_learning_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump({
                    "session_info": {
                        "start_time": self.session_start_time,
                        "total_decisions": self.total_ai_decisions,
                        "success_rate": self.successful_ai_decisions / max(self.total_ai_decisions, 1)
                    },
                    "learning_data": self.ai_learning_data[-50:]  # Last 50 decisions
                }, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving AI learning data: {e}")
    
    def _save_combat_analytics(self):
        """Save combat analytics to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.log_dir / f"combat_analytics_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump({
                    "session_info": {
                        "start_time": self.session_start_time,
                        "total_encounters": self.combat_encounters,
                        "boss_encounters": self.boss_encounters
                    },
                    "combat_data": self.combat_analytics[-20:]  # Last 20 encounters
                }, f, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving combat analytics: {e}")
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        if not self.performance_data:
            return {"error": "No performance data available"}
        
        # Calculate averages
        cpu_values = [p["system"]["cpu_percent"] for p in self.performance_data]
        memory_values = [p["system"]["memory_percent"] for p in self.performance_data]
        
        # AI learning summary
        ai_success_rate = self.successful_ai_decisions / max(self.total_ai_decisions, 1)
        
        return {
            "system_performance": {
                "avg_cpu": sum(cpu_values) / len(cpu_values),
                "max_cpu": max(cpu_values),
                "avg_memory": sum(memory_values) / len(memory_values),
                "max_memory": max(memory_values),
                "samples_collected": len(self.performance_data)
            },
            "ai_learning": {
                "total_decisions": self.total_ai_decisions,
                "successful_decisions": self.successful_ai_decisions,
                "success_rate": ai_success_rate,
                "combat_encounters": self.combat_encounters,
                "boss_encounters": self.boss_encounters,
                "session_duration": time.time() - self.session_start_time if self.session_start_time else 0
            },
            "learning_insights": self._generate_learning_insights()
        }
    
    def _generate_learning_insights(self) -> List[str]:
        """Generate insights from AI learning data"""
        insights = []
        
        if not self.ai_learning_data:
            return ["No AI learning data available"]
        
        # Analyze decision patterns
        recent_decisions = self.ai_learning_data[-20:]  # Last 20 decisions
        successful_recent = sum(1 for d in recent_decisions if d.get("success", False))
        recent_success_rate = successful_recent / len(recent_decisions)
        
        if recent_success_rate > 0.8:
            insights.append("AI showing strong recent performance")
        elif recent_success_rate < 0.4:
            insights.append("AI struggling with recent decisions")
        
        # Analyze combat performance
        if self.combat_encounters > 0:
            boss_success_rate = self.boss_encounters / self.combat_encounters
            if boss_success_rate > 0.5:
                insights.append("AI performing well in boss encounters")
            else:
                insights.append("AI needs improvement in boss encounters")
        
        # Analyze decision confidence trends
        confidence_values = [d.get("confidence", 0.5) for d in recent_decisions if "confidence" in d]
        if confidence_values:
            avg_confidence = sum(confidence_values) / len(confidence_values)
            if avg_confidence > 0.7:
                insights.append("AI showing high confidence in decisions")
            elif avg_confidence < 0.4:
                insights.append("AI showing low confidence - may need adaptation")
        
        return insights
    
    def export_analytics_report(self, filename: str = None) -> str:
        """Export comprehensive analytics report"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.log_dir / f"analytics_report_{timestamp}.json"
        
        report = {
            "report_generated": datetime.now().isoformat(),
            "session_summary": self.get_performance_summary(),
            "performance_trends": self._analyze_performance_trends(),
            "ai_learning_analysis": self._analyze_ai_learning_patterns(),
            "recommendations": self._generate_recommendations()
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            return str(filename)
        except Exception as e:
            logger.error(f"Error exporting analytics report: {e}")
            return None
    
    def _analyze_performance_trends(self) -> Dict[str, Any]:
        """Analyze performance trends over time"""
        if len(self.performance_data) < 10:
            return {"error": "Insufficient data for trend analysis"}
        
        # Split data into time periods
        mid_point = len(self.performance_data) // 2
        early_data = self.performance_data[:mid_point]
        late_data = self.performance_data[mid_point:]
        
        early_cpu = [p["system"]["cpu_percent"] for p in early_data]
        late_cpu = [p["system"]["cpu_percent"] for p in late_data]
        
        early_avg = sum(early_cpu) / len(early_cpu)
        late_avg = sum(late_cpu) / len(late_cpu)
        
        return {
            "cpu_trend": "increasing" if late_avg > early_avg else "decreasing",
            "early_avg_cpu": early_avg,
            "late_avg_cpu": late_avg,
            "performance_stability": "stable" if abs(late_avg - early_avg) < 5 else "variable"
        }
    
    def _analyze_ai_learning_patterns(self) -> Dict[str, Any]:
        """Analyze AI learning patterns"""
        if not self.ai_learning_data:
            return {"error": "No AI learning data available"}
        
        # Analyze decision patterns
        decisions_by_type = {}
        for decision in self.ai_learning_data:
            decision_type = decision.get("scenario", "unknown")
            if decision_type not in decisions_by_type:
                decisions_by_type[decision_type] = {"total": 0, "successful": 0}
            
            decisions_by_type[decision_type]["total"] += 1
            if decision.get("success", False):
                decisions_by_type[decision_type]["successful"] += 1
        
        # Calculate success rates by type
        type_success_rates = {}
        for decision_type, stats in decisions_by_type.items():
            type_success_rates[decision_type] = stats["successful"] / stats["total"]
        
        return {
            "decisions_by_type": decisions_by_type,
            "success_rates_by_type": type_success_rates,
            "most_successful_type": max(type_success_rates.items(), key=lambda x: x[1])[0] if type_success_rates else None,
            "least_successful_type": min(type_success_rates.items(), key=lambda x: x[1])[0] if type_success_rates else None
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on analytics"""
        recommendations = []
        
        # Performance recommendations
        summary = self.get_performance_summary()
        avg_cpu = summary["system_performance"]["avg_cpu"]
        
        if avg_cpu > 80:
            recommendations.append("High CPU usage detected - consider optimizing AI decision frequency")
        elif avg_cpu < 20:
            recommendations.append("Low CPU usage - can increase AI learning intensity")
        
        # AI learning recommendations
        ai_success_rate = summary["ai_learning"]["success_rate"]
        
        if ai_success_rate < 0.5:
            recommendations.append("Low AI success rate - consider adjusting learning parameters")
        elif ai_success_rate > 0.9:
            recommendations.append("High AI success rate - consider increasing difficulty")
        
        # Combat recommendations
        if self.combat_encounters > 0:
            boss_rate = self.boss_encounters / self.combat_encounters
            if boss_rate < 0.1:
                recommendations.append("Low boss encounter rate - consider adding more boss content")
            elif boss_rate > 0.5:
                recommendations.append("High boss encounter rate - consider balancing regular encounters")
        
        return recommendations


def main():
    """Test the enhanced performance monitor"""
    monitor = EnhancedPerformanceMonitor()
    
    print("Starting enhanced performance monitoring...")
    monitor.start_monitoring(interval=2.0)
    
    try:
        # Simulate some AI decisions and combat encounters
        for i in range(10):
            time.sleep(3)
            
            # Simulate AI decision
            decision_data = {
                "scenario": "combat_decision",
                "success": random.choice([True, False]),
                "confidence": random.uniform(0.3, 0.9),
                "reasoning": "Simulated decision reasoning"
            }
            monitor.record_ai_decision(decision_data)
            
            # Simulate combat encounter
            encounter_data = {
                "boss_encounter": random.choice([True, False]),
                "damage_dealt": random.randint(50, 200),
                "damage_taken": random.randint(10, 100),
                "skills_used": ["skill1", "skill2"]
            }
            monitor.record_combat_encounter(encounter_data)
            
            print(f"Recorded data point {i+1}/10")
        
        # Generate report
        print("\nGenerating analytics report...")
        report_file = monitor.export_analytics_report()
        if report_file:
            print(f"Report saved to: {report_file}")
        
        # Show summary
        summary = monitor.get_performance_summary()
        print(f"\nPerformance Summary:")
        print(f"AI Success Rate: {summary['ai_learning']['success_rate']:.2%}")
        print(f"Combat Encounters: {summary['ai_learning']['combat_encounters']}")
        print(f"Boss Encounters: {summary['ai_learning']['boss_encounters']}")
        
    except KeyboardInterrupt:
        print("\nStopping monitoring...")
    finally:
        monitor.stop_monitoring()
        print("Monitoring stopped.")


if __name__ == "__main__":
    import random
    main()

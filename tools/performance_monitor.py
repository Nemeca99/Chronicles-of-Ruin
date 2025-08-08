import psutil
import time
import csv
import os
from datetime import datetime
from pathlib import Path
import threading
import json
import sys

class PerformanceMonitor:
    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.monitoring = False
        self.monitor_thread = None
        self.log_file = None
        self.csv_writer = None
        self.performance_data = []
        
    def start_monitoring(self, session_name=None):
        """Start performance monitoring with 1-second intervals and detailed logging"""
        if self.monitoring:
            print("Monitoring already active")
            return
            
        if session_name is None:
            session_name = f"ai_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
        self.log_file = self.log_dir / f"{session_name}_performance.csv"
        
        # Create CSV file with enhanced headers
        self.csv_file = open(self.log_file, 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow([
            'timestamp',
            'cpu_percent',
            'cpu_freq_current',
            'cpu_freq_min',
            'cpu_freq_max',
            'cpu_temp',
            'cpu_cores_active',
            'memory_percent',
            'memory_used_gb',
            'memory_total_gb',
            'disk_usage_percent',
            'gpu_name',
            'gpu_memory_percent',
            'gpu_memory_used_mb',
            'gpu_memory_total_mb',
            'gpu_temp',
            'gpu_utilization',
            'gpu_power_watts',
            'network_sent_mb',
            'network_recv_mb'
        ])
        
        self.monitoring = True
        self.performance_data = []
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        print(f"Performance monitoring started: {self.log_file}")
        print(f"Logging CPU/GPU usage and thermal readings per second...")
        
    def stop_monitoring(self):
        """Stop performance monitoring"""
        if not self.monitoring:
            print("No monitoring active")
            return
            
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        
        # Close the CSV file
        if hasattr(self, 'csv_file') and self.csv_file:
            self.csv_file.close()
            
        if self.log_file and self.log_file.exists():
            print(f"Performance monitoring stopped. Log saved: {self.log_file}")
            
    def _monitor_loop(self):
        """Main monitoring loop with 1-second intervals and detailed metrics"""
        while self.monitoring:
            try:
                timestamp = datetime.now().isoformat()
                
                # CPU metrics with enhanced detail
                cpu_percent = psutil.cpu_percent(interval=0.1)
                cpu_freq = psutil.cpu_freq()
                cpu_freq_current = cpu_freq.current if cpu_freq else 0
                cpu_freq_min = cpu_freq.min if cpu_freq else 0
                cpu_freq_max = cpu_freq.max if cpu_freq else 0
                cpu_cores_active = len([c for c in psutil.cpu_percent(percpu=True) if c > 0])
                
                # CPU temperature (platform dependent)
                cpu_temp = self._get_cpu_temperature()
                
                # Memory metrics
                memory = psutil.virtual_memory()
                memory_percent = memory.percent
                memory_used_gb = memory.used / (1024**3)
                memory_total_gb = memory.total / (1024**3)
                
                # Disk usage
                disk_usage = psutil.disk_usage('/').percent
                
                # Network metrics
                network = psutil.net_io_counters()
                network_sent_mb = network.bytes_sent / (1024**2)
                network_recv_mb = network.bytes_recv / (1024**2)
                
                # GPU metrics (enhanced)
                gpu_info = self._get_gpu_info_enhanced()
                
                # Create data row
                data_row = [
                    timestamp,
                    cpu_percent,
                    cpu_freq_current,
                    cpu_freq_min,
                    cpu_freq_max,
                    cpu_temp,
                    cpu_cores_active,
                    memory_percent,
                    memory_used_gb,
                    memory_total_gb,
                    disk_usage,
                    gpu_info.get('name', 'Unknown'),
                    gpu_info.get('memory_percent', 0),
                    gpu_info.get('memory_used_mb', 0),
                    gpu_info.get('memory_total_mb', 0),
                    gpu_info.get('temp', 0),
                    gpu_info.get('utilization', 0),
                    gpu_info.get('power_watts', 0),
                    network_sent_mb,
                    network_recv_mb
                ]
                
                # Write to CSV
                self.csv_writer.writerow(data_row)
                self.csv_file.flush()
                
                # Store in memory for analysis
                self.performance_data.append({
                    'timestamp': timestamp,
                    'cpu_percent': cpu_percent,
                    'cpu_temp': cpu_temp,
                    'memory_percent': memory_percent,
                    'gpu_utilization': gpu_info.get('utilization', 0),
                    'gpu_temp': gpu_info.get('temp', 0)
                })
                
                # Sleep for 1 second
                time.sleep(1)
                
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(1)
    
    def _get_cpu_temperature(self):
        """Get CPU temperature with enhanced platform support"""
        try:
            # Windows
            if os.name == 'nt':
                try:
                    import wmi
                    w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
                    temperature_infos = w.Sensor()
                    for sensor in temperature_infos:
                        if sensor.SensorType == 'Temperature' and 'CPU' in sensor.Name:
                            return float(sensor.Value)
                except:
                    pass
                
                # Try alternative method
                try:
                    import subprocess
                    result = subprocess.run(['wmic', 'cpu', 'get', 'temperature'], 
                                         capture_output=True, text=True)
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        if len(lines) > 1:
                            temp = lines[1].strip()
                            if temp.isdigit():
                                return float(temp)
                except:
                    pass
            
            # Linux
            elif os.name == 'posix':
                try:
                    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                        temp = int(f.read().strip()) / 1000.0
                        return temp
                except:
                    pass
                    
                    # Try alternative Linux method
                    try:
                        import subprocess
                        result = subprocess.run(['sensors'], capture_output=True, text=True)
                        if result.returncode == 0:
                            for line in result.stdout.split('\n'):
                                if 'Core' in line and '°C' in line:
                                    temp_str = line.split('°C')[0].split()[-1]
                                    return float(temp_str)
                    except:
                        pass
            
            # macOS
            elif sys.platform == 'darwin':
                try:
                    import subprocess
                    result = subprocess.run(['sudo', 'powermetrics', '-n', '1', '-i', '1000'], 
                                         capture_output=True, text=True)
                    if result.returncode == 0:
                        for line in result.stdout.split('\n'):
                            if 'CPU die temperature' in line:
                                temp_str = line.split()[-1].replace('°C', '')
                                return float(temp_str)
                except:
                    pass
            
            return 0
            
        except Exception as e:
            return 0
    
    def _get_gpu_info_enhanced(self):
        """Get enhanced GPU information with thermal and power data"""
        gpu_info = {
            'name': 'Unknown',
            'memory_percent': 0,
            'memory_used_mb': 0,
            'memory_total_mb': 0,
            'temp': 0,
            'utilization': 0,
            'power_watts': 0
        }
        
        try:
            # Try NVIDIA GPU
            try:
                import subprocess
                result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.used,memory.total,temperature.gpu,utilization.gpu,power.draw', 
                                       '--format=csv,noheader,nounits'], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    if lines and lines[0]:
                        parts = lines[0].split(', ')
                        if len(parts) >= 6:
                            gpu_info['name'] = parts[0]
                            gpu_info['memory_used_mb'] = float(parts[1])
                            gpu_info['memory_total_mb'] = float(parts[2])
                            gpu_info['temp'] = float(parts[3])
                            gpu_info['utilization'] = float(parts[4])
                            gpu_info['power_watts'] = float(parts[5])
                            gpu_info['memory_percent'] = (gpu_info['memory_used_mb'] / gpu_info['memory_total_mb']) * 100
            except:
                pass
            
            # Try AMD GPU
            try:
                import subprocess
                result = subprocess.run(['rocm-smi', '--showproductname', '--showmeminfo', 'VRAM', 
                                       '--showtemp', '--showpower'], capture_output=True, text=True)
                if result.returncode == 0:
                    # Parse AMD output (simplified)
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if 'GPU' in line and '°C' in line:
                            temp_str = line.split('°C')[0].split()[-1]
                            gpu_info['temp'] = float(temp_str)
                        elif 'GPU' in line and 'W' in line:
                            power_str = line.split('W')[0].split()[-1]
                            gpu_info['power_watts'] = float(power_str)
            except:
                pass
            
            # Try Intel GPU
            try:
                import subprocess
                result = subprocess.run(['intel_gpu_top', '-J'], capture_output=True, text=True)
                if result.returncode == 0:
                    import json
                    data = json.loads(result.stdout)
                    if 'engines' in data:
                        for engine in data['engines']:
                            if engine.get('name') == 'Render/3D/0':
                                gpu_info['utilization'] = engine.get('busy', 0)
                                break
            except:
                pass
                
        except Exception as e:
            pass
        
        return gpu_info
    
    def get_summary(self, log_file=None):
        """Get enhanced performance summary with trend analysis"""
        if log_file is None:
            log_file = self.log_file
            
        if not log_file or not log_file.exists():
            return {"error": "No performance log found"}
        
        try:
            # Read CSV data
            data = []
            with open(log_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            
            if not data:
                return {"error": "No performance data found"}
            
            # Calculate basic statistics
            cpu_percents = [float(row['cpu_percent']) for row in data]
            memory_percents = [float(row['memory_percent']) for row in data]
            cpu_temps = [float(row['cpu_temp']) for row in data if float(row['cpu_temp']) > 0]
            gpu_temps = [float(row['gpu_temp']) for row in data if float(row['gpu_temp']) > 0]
            gpu_utilizations = [float(row['gpu_utilization']) for row in data if float(row['gpu_utilization']) > 0]
            
            # Calculate duration
            start_time = datetime.fromisoformat(data[0]['timestamp'])
            end_time = datetime.fromisoformat(data[-1]['timestamp'])
            duration_seconds = (end_time - start_time).total_seconds()
            
            # Performance trends analysis
            trends = self._analyze_performance_trends(data)
            
            summary = {
                'duration_seconds': duration_seconds,
                'cpu_percent_avg': sum(cpu_percents) / len(cpu_percents),
                'cpu_percent_max': max(cpu_percents),
                'memory_percent_avg': sum(memory_percents) / len(memory_percents),
                'memory_percent_max': max(memory_percents),
                'cpu_temp_avg': sum(cpu_temps) / len(cpu_temps) if cpu_temps else 0,
                'cpu_temp_max': max(cpu_temps) if cpu_temps else 0,
                'gpu_temp_avg': sum(gpu_temps) / len(gpu_temps) if gpu_temps else 0,
                'gpu_temp_max': max(gpu_temps) if gpu_temps else 0,
                'gpu_utilization_avg': sum(gpu_utilizations) / len(gpu_utilizations) if gpu_utilizations else 0,
                'gpu_utilization_max': max(gpu_utilizations) if gpu_utilizations else 0,
                'performance_trends': trends,
                'data_points': len(data)
            }
            
            return summary
            
        except Exception as e:
            return {"error": f"Error analyzing performance data: {e}"}
    
    def _analyze_performance_trends(self, data):
        """Analyze performance trends and identify spikes"""
        trends = {
            'cpu_spikes': 0,
            'gpu_spikes': 0,
            'thermal_thresholds': 0,
            'memory_pressure': 0
        }
        
        cpu_threshold = 80  # CPU usage spike threshold
        gpu_threshold = 80  # GPU usage spike threshold
        temp_threshold = 80  # Temperature threshold (°C)
        memory_threshold = 90  # Memory usage threshold
        
        for row in data:
            cpu_percent = float(row['cpu_percent'])
            gpu_utilization = float(row['gpu_utilization'])
            cpu_temp = float(row['cpu_temp'])
            gpu_temp = float(row['gpu_temp'])
            memory_percent = float(row['memory_percent'])
            
            if cpu_percent > cpu_threshold:
                trends['cpu_spikes'] += 1
            if gpu_utilization > gpu_threshold:
                trends['gpu_spikes'] += 1
            if cpu_temp > temp_threshold or gpu_temp > temp_threshold:
                trends['thermal_thresholds'] += 1
            if memory_percent > memory_threshold:
                trends['memory_pressure'] += 1
        
        return trends

    def list_logs(self):
        """List all available performance logs"""
        log_files = list(self.log_dir.glob("*_performance.csv"))
        if not log_files:
            return "No performance logs found"
            
        logs = []
        for log_file in sorted(log_files, key=lambda x: x.stat().st_mtime, reverse=True):
            stats = log_file.stat()
            logs.append({
                'filename': log_file.name,
                'size_mb': round(stats.st_size / (1024**2), 2),
                'modified': datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })
            
        return logs

def main():
    """CLI interface for performance monitoring"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Performance Monitor for AI Player Tests")
    parser.add_argument('action', nargs='?', choices=['start', 'stop', 'summary', 'list'], default='start')
    parser.add_argument('--session', help='Session name for logging')
    parser.add_argument('--log-file', help='Specific log file for summary')
    
    args = parser.parse_args()
    
    monitor = PerformanceMonitor()
    
    if args.action == 'start':
        monitor.start_monitoring(args.session)
        print("Press Ctrl+C to stop monitoring...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            monitor.stop_monitoring()
            
    elif args.action == 'stop':
        monitor.stop_monitoring()
        
    elif args.action == 'summary':
        summary = monitor.get_summary(args.log_file)
        if isinstance(summary, dict):
            print("Performance Summary:")
            for key, value in summary.items():
                print(f"  {key}: {value}")
        else:
            print(summary)
            
    elif args.action == 'list':
        logs = monitor.list_logs()
        if isinstance(logs, list):
            print("Available Performance Logs:")
            for log in logs:
                print(f"  {log['filename']} ({log['size_mb']}MB) - {log['modified']}")
        else:
            print(logs)

if __name__ == "__main__":
    main()

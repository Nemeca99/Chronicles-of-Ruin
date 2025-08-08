#!/usr/bin/env python3
"""
Dynamic Difficulty Scaling System
Automatically adjusts game difficulty based on AI player performance in real-time
"""

import sys
import json
import time
import math
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from dataclasses import dataclass
from collections import deque

# Add project paths
sys.path.append(str(Path(__file__).parent.parent))

class DifficultyMetric(Enum):
    DAMAGE_SCALING = "damage_scaling"
    ENEMY_HEALTH = "enemy_health"
    ENEMY_DAMAGE = "enemy_damage"
    SPAWN_RATE = "spawn_rate"
    RESOURCE_SCARCITY = "resource_scarcity"
    XP_MODIFIER = "xp_modifier"
    GOLD_MODIFIER = "gold_modifier"
    SKILL_COOLDOWNS = "skill_cooldowns"
    RESISTANCE_SCALING = "resistance_scaling"

class PerformanceIndicator(Enum):
    WIN_RATE = "win_rate"
    SURVIVAL_TIME = "survival_time"
    DAMAGE_EFFICIENCY = "damage_efficiency"
    RESOURCE_EFFICIENCY = "resource_efficiency"
    DECISION_SPEED = "decision_speed"
    LEARNING_RATE = "learning_rate"
    ENGAGEMENT_LEVEL = "engagement_level"

@dataclass
class PerformanceWindow:
    """Sliding window of performance data"""
    timestamp: float
    win_rate: float
    survival_time: float
    damage_efficiency: float
    resource_efficiency: float
    decision_speed: float
    engagement_score: float

@dataclass
class DifficultyAdjustment:
    """Represents a difficulty adjustment"""
    metric: DifficultyMetric
    old_value: float
    new_value: float
    adjustment_factor: float
    reason: str
    timestamp: float
    confidence: float

class DynamicDifficultyScaler:
    """Main class for dynamic difficulty scaling"""
    
    def __init__(self, window_size: int = 50, adjustment_threshold: float = 0.1):
        self.window_size = window_size
        self.adjustment_threshold = adjustment_threshold
        
        # Performance tracking
        self.performance_windows = deque(maxlen=window_size)
        self.adjustment_history = []
        
        # Current difficulty state
        self.current_difficulty = self._initialize_difficulty_state()
        
        # Scaling parameters
        self.scaling_parameters = self._initialize_scaling_parameters()
        
        # Target performance ranges
        self.target_ranges = {
            PerformanceIndicator.WIN_RATE: (0.60, 0.80),
            PerformanceIndicator.SURVIVAL_TIME: (0.70, 0.85),
            PerformanceIndicator.DAMAGE_EFFICIENCY: (0.65, 0.85),
            PerformanceIndicator.RESOURCE_EFFICIENCY: (0.55, 0.75),
            PerformanceIndicator.DECISION_SPEED: (0.50, 0.90),
            PerformanceIndicator.ENGAGEMENT_LEVEL: (0.70, 0.95)
        }
        
        # Adjustment sensitivity
        self.sensitivity = {
            DifficultyMetric.DAMAGE_SCALING: 0.05,
            DifficultyMetric.ENEMY_HEALTH: 0.10,
            DifficultyMetric.ENEMY_DAMAGE: 0.08,
            DifficultyMetric.SPAWN_RATE: 0.15,
            DifficultyMetric.RESOURCE_SCARCITY: 0.12,
            DifficultyMetric.XP_MODIFIER: 0.05,
            DifficultyMetric.GOLD_MODIFIER: 0.05,
            DifficultyMetric.SKILL_COOLDOWNS: 0.10,
            DifficultyMetric.RESISTANCE_SCALING: 0.08
        }
    
    def _initialize_difficulty_state(self) -> Dict[DifficultyMetric, float]:
        """Initialize baseline difficulty values"""
        return {
            DifficultyMetric.DAMAGE_SCALING: 1.0,
            DifficultyMetric.ENEMY_HEALTH: 1.0,
            DifficultyMetric.ENEMY_DAMAGE: 1.0,
            DifficultyMetric.SPAWN_RATE: 1.0,
            DifficultyMetric.RESOURCE_SCARCITY: 1.0,
            DifficultyMetric.XP_MODIFIER: 1.0,
            DifficultyMetric.GOLD_MODIFIER: 1.0,
            DifficultyMetric.SKILL_COOLDOWNS: 1.0,
            DifficultyMetric.RESISTANCE_SCALING: 1.0
        }
    
    def _initialize_scaling_parameters(self) -> Dict[str, Any]:
        """Initialize scaling parameters and constraints"""
        return {
            "min_values": {
                DifficultyMetric.DAMAGE_SCALING: 0.5,
                DifficultyMetric.ENEMY_HEALTH: 0.3,
                DifficultyMetric.ENEMY_DAMAGE: 0.4,
                DifficultyMetric.SPAWN_RATE: 0.2,
                DifficultyMetric.RESOURCE_SCARCITY: 0.5,
                DifficultyMetric.XP_MODIFIER: 0.8,
                DifficultyMetric.GOLD_MODIFIER: 0.8,
                DifficultyMetric.SKILL_COOLDOWNS: 0.7,
                DifficultyMetric.RESISTANCE_SCALING: 0.6
            },
            "max_values": {
                DifficultyMetric.DAMAGE_SCALING: 3.0,
                DifficultyMetric.ENEMY_HEALTH: 5.0,
                DifficultyMetric.ENEMY_DAMAGE: 2.5,
                DifficultyMetric.SPAWN_RATE: 3.0,
                DifficultyMetric.RESOURCE_SCARCITY: 2.0,
                DifficultyMetric.XP_MODIFIER: 1.5,
                DifficultyMetric.GOLD_MODIFIER: 1.5,
                DifficultyMetric.SKILL_COOLDOWNS: 2.0,
                DifficultyMetric.RESISTANCE_SCALING: 1.8
            },
            "adjustment_speed": 0.15,  # How quickly to make adjustments
            "stability_bonus": 0.05,   # Bonus for stable performance
            "volatility_penalty": 0.10  # Penalty for erratic performance
        }
    
    def record_performance(self, player_id: str, session_data: Dict[str, Any]) -> None:
        """Record performance data from a play session"""
        
        # Extract performance metrics from session data
        performance = PerformanceWindow(
            timestamp=time.time(),
            win_rate=session_data.get("win_rate", 0.5),
            survival_time=session_data.get("survival_time", 0.5),
            damage_efficiency=session_data.get("damage_efficiency", 0.5),
            resource_efficiency=session_data.get("resource_efficiency", 0.5),
            decision_speed=session_data.get("decision_speed", 0.5),
            engagement_score=session_data.get("engagement_score", 0.5)
        )
        
        self.performance_windows.append(performance)
        
        # Check if adjustment is needed
        if len(self.performance_windows) >= min(10, self.window_size // 5):
            self._evaluate_and_adjust()
    
    def _evaluate_and_adjust(self) -> List[DifficultyAdjustment]:
        """Evaluate current performance and make difficulty adjustments"""
        
        if len(self.performance_windows) < 5:
            return []
        
        # Calculate recent performance metrics
        recent_performance = self._calculate_recent_performance()
        
        # Analyze performance trends
        trends = self._analyze_performance_trends()
        
        # Determine needed adjustments
        adjustments = self._determine_adjustments(recent_performance, trends)
        
        # Apply adjustments
        applied_adjustments = []
        for adjustment in adjustments:
            if self._apply_adjustment(adjustment):
                applied_adjustments.append(adjustment)
                self.adjustment_history.append(adjustment)
        
        return applied_adjustments
    
    def _calculate_recent_performance(self) -> Dict[PerformanceIndicator, float]:
        """Calculate average performance over recent windows"""
        
        recent_count = min(10, len(self.performance_windows))
        recent_windows = list(self.performance_windows)[-recent_count:]
        
        return {
            PerformanceIndicator.WIN_RATE: sum(w.win_rate for w in recent_windows) / len(recent_windows),
            PerformanceIndicator.SURVIVAL_TIME: sum(w.survival_time for w in recent_windows) / len(recent_windows),
            PerformanceIndicator.DAMAGE_EFFICIENCY: sum(w.damage_efficiency for w in recent_windows) / len(recent_windows),
            PerformanceIndicator.RESOURCE_EFFICIENCY: sum(w.resource_efficiency for w in recent_windows) / len(recent_windows),
            PerformanceIndicator.DECISION_SPEED: sum(w.decision_speed for w in recent_windows) / len(recent_windows),
            PerformanceIndicator.ENGAGEMENT_LEVEL: sum(w.engagement_score for w in recent_windows) / len(recent_windows)
        }
    
    def _analyze_performance_trends(self) -> Dict[str, float]:
        """Analyze trends in performance data"""
        
        if len(self.performance_windows) < 10:
            return {"stability": 1.0, "trend": 0.0, "volatility": 0.0}
        
        # Calculate trend over time
        windows = list(self.performance_windows)[-20:]  # Last 20 windows
        timestamps = [w.timestamp for w in windows]
        win_rates = [w.win_rate for w in windows]
        
        # Simple linear trend calculation
        if len(windows) > 1:
            time_span = timestamps[-1] - timestamps[0]
            if time_span > 0:
                trend = (win_rates[-1] - win_rates[0]) / time_span
            else:
                trend = 0.0
        else:
            trend = 0.0
        
        # Calculate volatility (standard deviation of recent win rates)
        if len(win_rates) > 1:
            mean_wr = sum(win_rates) / len(win_rates)
            variance = sum((wr - mean_wr) ** 2 for wr in win_rates) / len(win_rates)
            volatility = math.sqrt(variance)
        else:
            volatility = 0.0
        
        # Calculate stability (inverse of volatility)
        stability = max(0.0, 1.0 - volatility * 2)
        
        return {
            "stability": stability,
            "trend": trend,
            "volatility": volatility
        }
    
    def _determine_adjustments(self, performance: Dict[PerformanceIndicator, float], 
                             trends: Dict[str, float]) -> List[DifficultyAdjustment]:
        """Determine what difficulty adjustments are needed"""
        
        adjustments = []
        current_time = time.time()
        
        # Check each performance indicator against target ranges
        for indicator, value in performance.items():
            target_min, target_max = self.target_ranges[indicator]
            
            if value < target_min - self.adjustment_threshold:
                # Performance too low - reduce difficulty
                adjustments.extend(self._generate_difficulty_reductions(indicator, value, target_min, trends, current_time))
            elif value > target_max + self.adjustment_threshold:
                # Performance too high - increase difficulty
                adjustments.extend(self._generate_difficulty_increases(indicator, value, target_max, trends, current_time))
        
        # Apply trend-based adjustments
        if trends["trend"] > 0.5:  # Strong positive trend
            adjustments.extend(self._generate_preemptive_increases(trends, current_time))
        elif trends["trend"] < -0.5:  # Strong negative trend
            adjustments.extend(self._generate_preemptive_reductions(trends, current_time))
        
        return adjustments
    
    def _generate_difficulty_reductions(self, indicator: PerformanceIndicator, current_value: float,
                                      target_value: float, trends: Dict[str, float], 
                                      timestamp: float) -> List[DifficultyAdjustment]:
        """Generate adjustments to reduce difficulty"""
        
        adjustments = []
        severity = (target_value - current_value) / target_value
        
        # Map performance indicators to difficulty metrics
        if indicator == PerformanceIndicator.WIN_RATE:
            # Reduce enemy power
            adjustments.append(DifficultyAdjustment(
                metric=DifficultyMetric.ENEMY_DAMAGE,
                old_value=self.current_difficulty[DifficultyMetric.ENEMY_DAMAGE],
                new_value=0.0,  # Will be calculated in _apply_adjustment
                adjustment_factor=-severity * 0.2,
                reason=f"Low win rate ({current_value:.2%})",
                timestamp=timestamp,
                confidence=min(1.0, severity + trends["stability"])
            ))
            
            adjustments.append(DifficultyAdjustment(
                metric=DifficultyMetric.ENEMY_HEALTH,
                old_value=self.current_difficulty[DifficultyMetric.ENEMY_HEALTH],
                new_value=0.0,
                adjustment_factor=-severity * 0.15,
                reason=f"Low win rate ({current_value:.2%})",
                timestamp=timestamp,
                confidence=min(1.0, severity + trends["stability"])
            ))
        
        elif indicator == PerformanceIndicator.SURVIVAL_TIME:
            # Reduce enemy aggression
            adjustments.append(DifficultyAdjustment(
                metric=DifficultyMetric.SPAWN_RATE,
                old_value=self.current_difficulty[DifficultyMetric.SPAWN_RATE],
                new_value=0.0,
                adjustment_factor=-severity * 0.25,
                reason=f"Low survival time ({current_value:.2%})",
                timestamp=timestamp,
                confidence=min(1.0, severity + trends["stability"])
            ))
        
        elif indicator == PerformanceIndicator.RESOURCE_EFFICIENCY:
            # Improve resource availability
            adjustments.append(DifficultyAdjustment(
                metric=DifficultyMetric.RESOURCE_SCARCITY,
                old_value=self.current_difficulty[DifficultyMetric.RESOURCE_SCARCITY],
                new_value=0.0,
                adjustment_factor=-severity * 0.2,
                reason=f"Low resource efficiency ({current_value:.2%})",
                timestamp=timestamp,
                confidence=min(1.0, severity + trends["stability"])
            ))
        
        return adjustments
    
    def _generate_difficulty_increases(self, indicator: PerformanceIndicator, current_value: float,
                                     target_value: float, trends: Dict[str, float], 
                                     timestamp: float) -> List[DifficultyAdjustment]:
        """Generate adjustments to increase difficulty"""
        
        adjustments = []
        severity = (current_value - target_value) / target_value
        
        if indicator == PerformanceIndicator.WIN_RATE:
            # Increase enemy power
            adjustments.append(DifficultyAdjustment(
                metric=DifficultyMetric.ENEMY_DAMAGE,
                old_value=self.current_difficulty[DifficultyMetric.ENEMY_DAMAGE],
                new_value=0.0,
                adjustment_factor=severity * 0.15,
                reason=f"High win rate ({current_value:.2%})",
                timestamp=timestamp,
                confidence=min(1.0, severity + trends["stability"])
            ))
        
        elif indicator == PerformanceIndicator.SURVIVAL_TIME:
            # Increase enemy aggression
            adjustments.append(DifficultyAdjustment(
                metric=DifficultyMetric.SPAWN_RATE,
                old_value=self.current_difficulty[DifficultyMetric.SPAWN_RATE],
                new_value=0.0,
                adjustment_factor=severity * 0.2,
                reason=f"High survival time ({current_value:.2%})",
                timestamp=timestamp,
                confidence=min(1.0, severity + trends["stability"])
            ))
        
        elif indicator == PerformanceIndicator.DAMAGE_EFFICIENCY:
            # Increase enemy resistances
            adjustments.append(DifficultyAdjustment(
                metric=DifficultyMetric.RESISTANCE_SCALING,
                old_value=self.current_difficulty[DifficultyMetric.RESISTANCE_SCALING],
                new_value=0.0,
                adjustment_factor=severity * 0.1,
                reason=f"High damage efficiency ({current_value:.2%})",
                timestamp=timestamp,
                confidence=min(1.0, severity + trends["stability"])
            ))
        
        return adjustments
    
    def _generate_preemptive_increases(self, trends: Dict[str, float], timestamp: float) -> List[DifficultyAdjustment]:
        """Generate preemptive difficulty increases based on positive trends"""
        adjustments = []
        
        trend_strength = abs(trends["trend"])
        stability = trends["stability"]
        
        if stability > 0.7:  # Only make preemptive adjustments for stable trends
            adjustments.append(DifficultyAdjustment(
                metric=DifficultyMetric.DAMAGE_SCALING,
                old_value=self.current_difficulty[DifficultyMetric.DAMAGE_SCALING],
                new_value=0.0,
                adjustment_factor=trend_strength * 0.05,
                reason=f"Preemptive increase for positive trend ({trend_strength:.3f})",
                timestamp=timestamp,
                confidence=stability
            ))
        
        return adjustments
    
    def _generate_preemptive_reductions(self, trends: Dict[str, float], timestamp: float) -> List[DifficultyAdjustment]:
        """Generate preemptive difficulty reductions based on negative trends"""
        adjustments = []
        
        trend_strength = abs(trends["trend"])
        stability = trends["stability"]
        
        if stability > 0.7:
            adjustments.append(DifficultyAdjustment(
                metric=DifficultyMetric.DAMAGE_SCALING,
                old_value=self.current_difficulty[DifficultyMetric.DAMAGE_SCALING],
                new_value=0.0,
                adjustment_factor=-trend_strength * 0.05,
                reason=f"Preemptive reduction for negative trend ({trend_strength:.3f})",
                timestamp=timestamp,
                confidence=stability
            ))
        
        return adjustments
    
    def _apply_adjustment(self, adjustment: DifficultyAdjustment) -> bool:
        """Apply a difficulty adjustment if within constraints"""
        
        current_value = self.current_difficulty[adjustment.metric]
        sensitivity = self.sensitivity[adjustment.metric]
        
        # Calculate new value
        raw_adjustment = adjustment.adjustment_factor * sensitivity
        new_value = current_value + raw_adjustment
        
        # Apply constraints
        min_value = self.scaling_parameters["min_values"][adjustment.metric]
        max_value = self.scaling_parameters["max_values"][adjustment.metric]
        
        constrained_value = max(min_value, min(max_value, new_value))
        
        # Only apply if the change is significant enough
        if abs(constrained_value - current_value) < 0.01:
            return False
        
        # Update the adjustment with the actual new value
        adjustment.new_value = constrained_value
        
        # Apply the change
        self.current_difficulty[adjustment.metric] = constrained_value
        
        return True
    
    def get_current_difficulty_state(self) -> Dict[str, Any]:
        """Get the current difficulty state for game systems to use"""
        return {
            "difficulty_multipliers": {metric.value: value for metric, value in self.current_difficulty.items()},
            "last_adjustment_time": self.adjustment_history[-1].timestamp if self.adjustment_history else 0,
            "total_adjustments": len(self.adjustment_history),
            "performance_window_size": len(self.performance_windows)
        }
    
    def simulate_ai_performance_test(self, num_sessions: int = 50) -> Dict[str, Any]:
        """Simulate AI performance testing with dynamic difficulty scaling"""
        
        print(f"🎯 Simulating {num_sessions} AI performance sessions...")
        
        # Simulate different AI skill levels improving over time
        base_performance = 0.4  # Starting performance
        improvement_rate = 0.015  # Performance improvement per session
        noise_level = 0.1  # Random variation
        
        session_results = []
        
        for session in range(num_sessions):
            # Simulate AI performance improving over time with noise
            current_skill = base_performance + (session * improvement_rate)
            
            # Add random noise
            noise = (random.random() - 0.5) * noise_level * 2
            session_performance = max(0.1, min(0.95, current_skill + noise))
            
            # Simulate session data
            session_data = {
                "win_rate": session_performance,
                "survival_time": session_performance * 0.9 + random.random() * 0.1,
                "damage_efficiency": session_performance * 1.1 + random.random() * 0.1,
                "resource_efficiency": session_performance * 0.8 + random.random() * 0.2,
                "decision_speed": 0.6 + random.random() * 0.3,
                "engagement_score": session_performance * 0.9 + random.random() * 0.2
            }
            
            # Record performance and get any adjustments
            self.record_performance(f"ai_player_test", session_data)
            
            # Track results
            session_results.append({
                "session": session + 1,
                "performance": session_performance,
                "difficulty_state": self.current_difficulty.copy(),
                "adjustments_made": len(self.adjustment_history)
            })
            
            if (session + 1) % 10 == 0:
                current_diff = self.current_difficulty[DifficultyMetric.DAMAGE_SCALING]
                print(f"  Session {session + 1}: Performance {session_performance:.2%}, Difficulty Scale {current_diff:.2f}")
        
        return {
            "total_sessions": num_sessions,
            "session_results": session_results,
            "final_difficulty": self.current_difficulty.copy(),
            "total_adjustments": len(self.adjustment_history),
            "adjustment_history": [
                {
                    "metric": adj.metric.value,
                    "old_value": adj.old_value,
                    "new_value": adj.new_value,
                    "reason": adj.reason,
                    "confidence": adj.confidence
                }
                for adj in self.adjustment_history
            ]
        }
    
    def save_difficulty_data(self, filename: str = "difficulty_scaling_data.json") -> str:
        """Save difficulty scaling data to file"""
        
        data = {
            "timestamp": time.time(),
            "current_difficulty": {metric.value: value for metric, value in self.current_difficulty.items()},
            "performance_windows": [
                {
                    "timestamp": window.timestamp,
                    "win_rate": window.win_rate,
                    "survival_time": window.survival_time,
                    "damage_efficiency": window.damage_efficiency,
                    "resource_efficiency": window.resource_efficiency,
                    "decision_speed": window.decision_speed,
                    "engagement_score": window.engagement_score
                }
                for window in self.performance_windows
            ],
            "adjustment_history": [
                {
                    "metric": adj.metric.value,
                    "old_value": adj.old_value,
                    "new_value": adj.new_value,
                    "adjustment_factor": adj.adjustment_factor,
                    "reason": adj.reason,
                    "timestamp": adj.timestamp,
                    "confidence": adj.confidence
                }
                for adj in self.adjustment_history
            ],
            "statistics": {
                "total_adjustments": len(self.adjustment_history),
                "performance_sessions": len(self.performance_windows),
                "average_adjustment_confidence": sum(adj.confidence for adj in self.adjustment_history) / len(self.adjustment_history) if self.adjustment_history else 0.0
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filename

def main():
    """Test the dynamic difficulty scaling system"""
    print("⚖️ DYNAMIC DIFFICULTY SCALING TEST")
    print("=" * 50)
    
    scaler = DynamicDifficultyScaler()
    
    # Run simulation
    results = scaler.simulate_ai_performance_test(75)
    
    print(f"\n📊 SCALING RESULTS:")
    print(f"Total Sessions: {results['total_sessions']}")
    print(f"Total Adjustments: {results['total_adjustments']}")
    
    print(f"\nFinal Difficulty State:")
    for metric, value in results['final_difficulty'].items():
        print(f"  {metric.value}: {value:.3f}")
    
    # Show key adjustments
    print(f"\nKey Adjustments Made:")
    for adj in results['adjustment_history'][-5:]:  # Last 5 adjustments
        print(f"  {adj['metric']}: {adj['old_value']:.3f} → {adj['new_value']:.3f}")
        print(f"    Reason: {adj['reason']}")
        print(f"    Confidence: {adj['confidence']:.2%}")
    
    # Save data
    filename = scaler.save_difficulty_data()
    print(f"\n💾 Saved scaling data to: {filename}")
    
    print("\n🎉 Dynamic difficulty scaling test completed!")
    
    return True

if __name__ == "__main__":
    import random
    random.seed(42)  # For reproducible results
    main()

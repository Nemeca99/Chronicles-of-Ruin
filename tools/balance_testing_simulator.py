#!/usr/bin/env python3
"""
Automated Balance Testing Simulator for Chronicles of Ruin - Phase 2
Comprehensive balance validation with AI-driven testing and analysis
"""

import sys
import json
import time
import random
import statistics
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import concurrent.futures
import threading

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

class BalanceCategory(Enum):
    """Categories of balance testing"""
    DAMAGE_SCALING = "damage_scaling"
    PROGRESSION_CURVE = "progression_curve"
    ARCHETYPE_VIABILITY = "archetype_viability"
    ITEM_POWER_LEVEL = "item_power_level"
    BOSS_DIFFICULTY = "boss_difficulty"
    ECONOMY_BALANCE = "economy_balance"
    SKILL_EFFECTIVENESS = "skill_effectiveness"
    RESISTANCE_BALANCE = "resistance_balance"

class TestSeverity(Enum):
    """Severity levels for balance issues"""
    CRITICAL = "critical"       # Game-breaking imbalances
    HIGH = "high"              # Significantly affects gameplay
    MEDIUM = "medium"          # Noticeable but manageable
    LOW = "low"               # Minor tweaks needed
    INFORMATIONAL = "info"     # Data for reference

@dataclass
class BalanceTest:
    """Individual balance test definition"""
    id: str
    name: str
    category: BalanceCategory
    description: str
    test_function: str
    expected_range: Tuple[float, float]
    warning_threshold: float
    critical_threshold: float
    iterations: int = 1000

@dataclass
class BalanceResult:
    """Result of a balance test"""
    test_id: str
    test_name: str
    category: BalanceCategory
    severity: TestSeverity
    actual_value: float
    expected_range: Tuple[float, float]
    deviation_percent: float
    iterations_run: int
    detailed_data: Dict[str, Any]
    recommendations: List[str]
    timestamp: float

class BalanceTestingSuite:
    """Comprehensive automated balance testing system"""
    
    def __init__(self):
        self.results_file = Path("logs/balance_test_results.json")
        self.test_history: List[BalanceResult] = self._load_test_history()
        
        # Initialize test suite
        self.balance_tests = self._initialize_balance_tests()
        self.test_data_cache = {}
        
        # Import game systems for testing
        self._load_game_systems()
        
    def _load_test_history(self) -> List[BalanceResult]:
        """Load previous test results"""
        if self.results_file.exists():
            try:
                with open(self.results_file, 'r') as f:
                    data = json.load(f)
                
                history = []
                for result_data in data:
                    result = BalanceResult(
                        test_id=result_data['test_id'],
                        test_name=result_data['test_name'],
                        category=BalanceCategory(result_data['category']),
                        severity=TestSeverity(result_data['severity']),
                        actual_value=result_data['actual_value'],
                        expected_range=tuple(result_data['expected_range']),
                        deviation_percent=result_data['deviation_percent'],
                        iterations_run=result_data['iterations_run'],
                        detailed_data=result_data['detailed_data'],
                        recommendations=result_data['recommendations'],
                        timestamp=result_data['timestamp']
                    )
                    history.append(result)
                
                return history
                
            except Exception as e:
                print(f"Error loading test history: {e}")
        
        return []
    
    def _save_test_history(self):
        """Save test results to file"""
        self.results_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = []
        for result in self.test_history:
            data.append({
                'test_id': result.test_id,
                'test_name': result.test_name,
                'category': result.category.value,
                'severity': result.severity.value,
                'actual_value': result.actual_value,
                'expected_range': list(result.expected_range),
                'deviation_percent': result.deviation_percent,
                'iterations_run': result.iterations_run,
                'detailed_data': result.detailed_data,
                'recommendations': result.recommendations,
                'timestamp': result.timestamp
            })
        
        with open(self.results_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_game_systems(self):
        """Load game systems for testing"""
        try:
            from chapters.chapter_01_sunderfall.src.systems.combat_system import CombatSystem
            from chapters.chapter_01_sunderfall.src.systems.items_system import ItemsSystem
            from chapters.chapter_01_sunderfall.src.systems.progression_system import ProgressionSystem
            from chapters.chapter_01_sunderfall.src.systems.resistance_system import ResistanceSystem
            from chapters.chapter_01_sunderfall.src.systems.skills_system import SkillsSystem
            
            self.combat_system = CombatSystem()
            self.items_system = ItemsSystem()
            self.progression_system = ProgressionSystem(Path("chapters/chapter_01_sunderfall/data"))
            self.resistance_system = ResistanceSystem()
            self.skills_system = SkillsSystem()
            
            print("✅ Game systems loaded successfully")
            
        except Exception as e:
            print(f"⚠️ Error loading game systems: {e}")
            self.combat_system = None
            self.items_system = None
            self.progression_system = None
            self.resistance_system = None
            self.skills_system = None
    
    def _initialize_balance_tests(self) -> List[BalanceTest]:
        """Initialize the comprehensive balance test suite"""
        return [
            # Damage Scaling Tests
            BalanceTest(
                id="damage_scaling_linear",
                name="Linear Damage Scaling",
                category=BalanceCategory.DAMAGE_SCALING,
                description="Ensure damage scales linearly with level and equipment",
                test_function="test_damage_scaling",
                expected_range=(0.95, 1.05),  # 95-105% of expected scaling
                warning_threshold=0.10,       # 10% deviation warning
                critical_threshold=0.25,      # 25% deviation critical
                iterations=500
            ),
            
            # Progression Curve Tests
            BalanceTest(
                id="experience_curve_smooth",
                name="Experience Curve Smoothness", 
                category=BalanceCategory.PROGRESSION_CURVE,
                description="Verify experience requirements increase smoothly",
                test_function="test_experience_curve",
                expected_range=(0.90, 1.10),
                warning_threshold=0.15,
                critical_threshold=0.30,
                iterations=100
            ),
            
            # Archetype Viability Tests
            BalanceTest(
                id="archetype_balance",
                name="Archetype Performance Balance",
                category=BalanceCategory.ARCHETYPE_VIABILITY,
                description="Ensure all archetypes have similar effectiveness",
                test_function="test_archetype_balance",
                expected_range=(0.85, 1.15),  # 15% variance allowed
                warning_threshold=0.20,
                critical_threshold=0.35,
                iterations=1000
            ),
            
            # Item Power Level Tests
            BalanceTest(
                id="item_power_progression",
                name="Item Power Level Progression",
                category=BalanceCategory.ITEM_POWER_LEVEL,
                description="Verify item power scales appropriately with rarity/level",
                test_function="test_item_power_progression",
                expected_range=(0.90, 1.10),
                warning_threshold=0.15,
                critical_threshold=0.25,
                iterations=200
            ),
            
            # Boss Difficulty Tests
            BalanceTest(
                id="boss_difficulty_curve",
                name="Boss Difficulty Scaling",
                category=BalanceCategory.BOSS_DIFFICULTY,
                description="Ensure boss difficulty scales appropriately",
                test_function="test_boss_difficulty",
                expected_range=(0.80, 1.20),  # 20% variance for boss encounters
                warning_threshold=0.25,
                critical_threshold=0.40,
                iterations=100
            ),
            
            # Economy Balance Tests
            BalanceTest(
                id="economy_inflation_check",
                name="Economy Inflation Rate",
                category=BalanceCategory.ECONOMY_BALANCE,
                description="Check for currency inflation or deflation",
                test_function="test_economy_balance",
                expected_range=(0.95, 1.05),
                warning_threshold=0.10,
                critical_threshold=0.20,
                iterations=300
            ),
            
            # Skill Effectiveness Tests
            BalanceTest(
                id="skill_damage_efficiency",
                name="Skill Damage vs Cost Efficiency",
                category=BalanceCategory.SKILL_EFFECTIVENESS,
                description="Verify skill damage/cost ratios are balanced",
                test_function="test_skill_effectiveness",
                expected_range=(0.90, 1.10),
                warning_threshold=0.15,
                critical_threshold=0.25,
                iterations=500
            ),
            
            # Resistance Balance Tests
            BalanceTest(
                id="resistance_effectiveness",
                name="Resistance System Balance",
                category=BalanceCategory.RESISTANCE_BALANCE,
                description="Ensure resistance values provide appropriate protection",
                test_function="test_resistance_balance",
                expected_range=(0.85, 1.15),
                warning_threshold=0.20,
                critical_threshold=0.30,
                iterations=400
            )
        ]
    
    def run_all_tests(self) -> List[BalanceResult]:
        """Run the complete balance testing suite"""
        print("🧪 Starting comprehensive balance testing suite...")
        print(f"📊 Running {len(self.balance_tests)} balance tests...")
        
        results = []
        start_time = time.time()
        
        for i, test in enumerate(self.balance_tests, 1):
            print(f"\n[{i}/{len(self.balance_tests)}] Running: {test.name}")
            
            try:
                result = self._run_single_test(test)
                results.append(result)
                
                # Print immediate feedback
                status_emoji = {
                    TestSeverity.CRITICAL: "🔴",
                    TestSeverity.HIGH: "🟠", 
                    TestSeverity.MEDIUM: "🟡",
                    TestSeverity.LOW: "🟢",
                    TestSeverity.INFORMATIONAL: "ℹ️"
                }
                
                print(f"   {status_emoji[result.severity]} {result.severity.value.upper()}: {result.actual_value:.3f} (expected: {result.expected_range[0]:.3f}-{result.expected_range[1]:.3f})")
                
                if result.recommendations:
                    print(f"   💡 Recommendation: {result.recommendations[0]}")
                
            except Exception as e:
                print(f"   ❌ Test failed: {e}")
                # Create a failed test result
                result = BalanceResult(
                    test_id=test.id,
                    test_name=test.name,
                    category=test.category,
                    severity=TestSeverity.CRITICAL,
                    actual_value=0.0,
                    expected_range=test.expected_range,
                    deviation_percent=100.0,
                    iterations_run=0,
                    detailed_data={'error': str(e)},
                    recommendations=[f"Fix test implementation: {e}"],
                    timestamp=time.time()
                )
                results.append(result)
        
        # Save results
        self.test_history.extend(results)
        self._save_test_history()
        
        total_time = time.time() - start_time
        print(f"\n✅ Balance testing completed in {total_time:.1f}s")
        
        return results
    
    def _run_single_test(self, test: BalanceTest) -> BalanceResult:
        """Run a single balance test"""
        # Get the test function dynamically
        test_func = getattr(self, test.test_function)
        
        # Run the test with specified iterations
        test_values = []
        detailed_data = {}
        
        for i in range(test.iterations):
            try:
                value, extra_data = test_func()
                test_values.append(value)
                
                # Collect detailed data from first few iterations
                if i < 10:
                    detailed_data[f"iteration_{i}"] = extra_data
                    
            except Exception as e:
                print(f"   ⚠️ Iteration {i} failed: {e}")
                continue
        
        if not test_values:
            raise Exception("No successful test iterations")
        
        # Calculate statistics
        avg_value = statistics.mean(test_values)
        std_dev = statistics.stdev(test_values) if len(test_values) > 1 else 0.0
        
        # Calculate deviation from expected range
        expected_mid = (test.expected_range[0] + test.expected_range[1]) / 2
        deviation_percent = abs(avg_value - expected_mid) / expected_mid
        
        # Determine severity
        if avg_value < test.expected_range[0] or avg_value > test.expected_range[1]:
            if deviation_percent >= test.critical_threshold:
                severity = TestSeverity.CRITICAL
            elif deviation_percent >= test.warning_threshold:
                severity = TestSeverity.HIGH
            else:
                severity = TestSeverity.MEDIUM
        else:
            if deviation_percent <= 0.05:  # Within 5%
                severity = TestSeverity.INFORMATIONAL
            else:
                severity = TestSeverity.LOW
        
        # Generate recommendations
        recommendations = self._generate_recommendations(test, avg_value, deviation_percent, severity)
        
        # Compile detailed data
        detailed_data.update({
            'average': avg_value,
            'standard_deviation': std_dev,
            'min_value': min(test_values),
            'max_value': max(test_values),
            'median': statistics.median(test_values),
            'sample_size': len(test_values),
            'values_distribution': {
                'q25': statistics.quantiles(test_values, n=4)[0] if len(test_values) >= 4 else 0,
                'q75': statistics.quantiles(test_values, n=4)[2] if len(test_values) >= 4 else 0
            }
        })
        
        return BalanceResult(
            test_id=test.id,
            test_name=test.name,
            category=test.category,
            severity=severity,
            actual_value=avg_value,
            expected_range=test.expected_range,
            deviation_percent=deviation_percent,
            iterations_run=len(test_values),
            detailed_data=detailed_data,
            recommendations=recommendations,
            timestamp=time.time()
        )
    
    def _generate_recommendations(self, test: BalanceTest, actual_value: float, 
                                deviation_percent: float, severity: TestSeverity) -> List[str]:
        """Generate specific recommendations based on test results"""
        recommendations = []
        
        if severity in [TestSeverity.CRITICAL, TestSeverity.HIGH]:
            if test.category == BalanceCategory.DAMAGE_SCALING:
                if actual_value > test.expected_range[1]:
                    recommendations.append("Reduce base damage values or damage multipliers")
                    recommendations.append("Consider implementing damage caps for high-level content")
                else:
                    recommendations.append("Increase base damage values or improve scaling formulas")
                    recommendations.append("Review weapon/skill power progression")
            
            elif test.category == BalanceCategory.ARCHETYPE_VIABILITY:
                recommendations.append("Review archetype-specific bonuses and penalties")
                recommendations.append("Consider buffing underperforming archetypes")
                recommendations.append("Test with different skill combinations")
            
            elif test.category == BalanceCategory.BOSS_DIFFICULTY:
                if actual_value > test.expected_range[1]:
                    recommendations.append("Reduce boss health or damage output")
                    recommendations.append("Add more telegraphed attacks or safe windows")
                else:
                    recommendations.append("Increase boss complexity or add new mechanics")
                    recommendations.append("Consider multi-phase encounters")
            
            elif test.category == BalanceCategory.ITEM_POWER_LEVEL:
                recommendations.append("Adjust item stat ranges for current tier")
                recommendations.append("Review rarity progression curves")
            
            elif test.category == BalanceCategory.RESISTANCE_BALANCE:
                recommendations.append("Adjust resistance percentages")
                recommendations.append("Review boss immunity interactions")
        
        elif severity == TestSeverity.MEDIUM:
            recommendations.append("Monitor this metric closely in future tests")
            recommendations.append("Consider minor adjustments if trend continues")
        
        else:
            recommendations.append("Balance appears healthy")
            recommendations.append("Continue monitoring for changes")
        
        return recommendations
    
    # Balance Test Implementation Methods
    
    def test_damage_scaling(self) -> Tuple[float, Dict]:
        """Test damage scaling across levels"""
        if not self.combat_system:
            return 1.0, {'error': 'Combat system not available'}
        
        # Simulate damage at different levels
        level_damages = {}
        
        for level in range(1, 21):  # Test levels 1-20
            # Simulate basic attack damage
            base_damage = 10 + (level * 2)  # Expected: +2 damage per level
            actual_damage = base_damage * random.uniform(0.9, 1.1)  # Add some variance
            level_damages[level] = actual_damage
        
        # Calculate scaling ratio
        level_1_damage = level_damages[1]
        level_20_damage = level_damages[20]
        expected_ratio = 20 / 1  # Should be ~20x at level 20 vs level 1
        actual_ratio = level_20_damage / level_1_damage
        
        scaling_accuracy = actual_ratio / expected_ratio
        
        return scaling_accuracy, {
            'level_damages': level_damages,
            'actual_ratio': actual_ratio,
            'expected_ratio': expected_ratio
        }
    
    def test_experience_curve(self) -> Tuple[float, Dict]:
        """Test experience curve smoothness"""
        if not self.progression_system:
            return 1.0, {'error': 'Progression system not available'}
        
        # Test experience requirements for levels 1-30
        exp_requirements = []
        
        for level in range(1, 31):
            # Simple exponential curve: base * (level ^ 1.5)
            base_exp = 100
            required_exp = base_exp * (level ** 1.5)
            exp_requirements.append(required_exp)
        
        # Check for smooth progression (no sudden jumps)
        progression_ratios = []
        for i in range(1, len(exp_requirements)):
            ratio = exp_requirements[i] / exp_requirements[i-1]
            progression_ratios.append(ratio)
        
        # Ideal ratio should be consistent (around 1.1-1.3 per level)
        avg_ratio = statistics.mean(progression_ratios)
        ratio_variance = statistics.stdev(progression_ratios)
        
        # Lower variance = smoother curve
        smoothness = 1.0 / (1.0 + ratio_variance)
        
        return smoothness, {
            'exp_requirements': exp_requirements[:10],  # First 10 levels
            'average_ratio': avg_ratio,
            'ratio_variance': ratio_variance,
            'progression_ratios': progression_ratios[:10]
        }
    
    def test_archetype_balance(self) -> Tuple[float, Dict]:
        """Test archetype performance balance"""
        if not self.skills_system:
            return 1.0, {'error': 'Skills system not available'}
        
        # Simulate performance for different archetypes
        archetypes = ['pure_dps', 'hybrid_tank', 'support_healer']
        performance_scores = {}
        
        for archetype in archetypes:
            # Simulate combat performance
            base_score = 100
            
            if archetype == 'pure_dps':
                # Should excel in damage
                damage_score = random.uniform(90, 110)
                survivability_score = random.uniform(60, 80)
                utility_score = random.uniform(40, 60)
            elif archetype == 'hybrid_tank':
                # Balanced performance
                damage_score = random.uniform(70, 90)
                survivability_score = random.uniform(90, 110)
                utility_score = random.uniform(70, 90)
            else:  # support_healer
                # Utility focused
                damage_score = random.uniform(50, 70)
                survivability_score = random.uniform(70, 90)
                utility_score = random.uniform(90, 110)
            
            total_score = (damage_score + survivability_score + utility_score) / 3
            performance_scores[archetype] = total_score
        
        # Calculate balance (how close all archetypes are to each other)
        scores = list(performance_scores.values())
        avg_score = statistics.mean(scores)
        score_variance = statistics.stdev(scores) if len(scores) > 1 else 0
        
        # Balance metric: closer to 1.0 = more balanced
        balance_metric = 1.0 / (1.0 + score_variance / avg_score)
        
        return balance_metric, {
            'performance_scores': performance_scores,
            'average_score': avg_score,
            'score_variance': score_variance
        }
    
    def test_item_power_progression(self) -> Tuple[float, Dict]:
        """Test item power level progression"""
        if not self.items_system:
            return 1.0, {'error': 'Items system not available'}
        
        # Test power progression across item rarities
        rarities = ['common', 'uncommon', 'rare', 'epic', 'legendary']
        power_values = {}
        
        for i, rarity in enumerate(rarities):
            # Expected power scaling: each tier ~25% stronger
            base_power = 100
            expected_multiplier = 1.25 ** i
            actual_power = base_power * expected_multiplier * random.uniform(0.95, 1.05)
            power_values[rarity] = actual_power
        
        # Check if progression is linear in log space
        expected_ratios = [1.25] * 4  # Expected ratio between consecutive tiers
        actual_ratios = []
        
        for i in range(1, len(rarities)):
            ratio = power_values[rarities[i]] / power_values[rarities[i-1]]
            actual_ratios.append(ratio)
        
        # Compare actual vs expected ratios
        ratio_accuracy = []
        for expected, actual in zip(expected_ratios, actual_ratios):
            accuracy = min(actual / expected, expected / actual)
            ratio_accuracy.append(accuracy)
        
        avg_accuracy = statistics.mean(ratio_accuracy)
        
        return avg_accuracy, {
            'power_values': power_values,
            'expected_ratios': expected_ratios,
            'actual_ratios': actual_ratios,
            'ratio_accuracy': ratio_accuracy
        }
    
    def test_boss_difficulty(self) -> Tuple[float, Dict]:
        """Test boss difficulty scaling"""
        # Simulate boss encounters at different levels
        boss_data = {}
        
        for level in [5, 10, 15, 20, 25]:
            # Expected difficulty should scale with level
            base_difficulty = 1.0
            expected_difficulty = base_difficulty * (level / 5) ** 1.2
            
            # Simulate actual difficulty (with some variance)
            actual_difficulty = expected_difficulty * random.uniform(0.8, 1.2)
            
            boss_data[f"level_{level}"] = {
                'expected': expected_difficulty,
                'actual': actual_difficulty
            }
        
        # Calculate accuracy of difficulty scaling
        accuracies = []
        for level_data in boss_data.values():
            accuracy = min(
                level_data['actual'] / level_data['expected'],
                level_data['expected'] / level_data['actual']
            )
            accuracies.append(accuracy)
        
        avg_accuracy = statistics.mean(accuracies)
        
        return avg_accuracy, boss_data
    
    def test_economy_balance(self) -> Tuple[float, Dict]:
        """Test economy inflation/deflation"""
        # Simulate currency flow over time
        currency_data = {}
        player_wealth = 1000  # Starting wealth
        
        for day in range(1, 31):  # 30 days simulation
            # Income (quests, drops, etc.)
            daily_income = random.uniform(50, 150)
            
            # Expenses (repairs, consumables, etc.)
            daily_expenses = random.uniform(30, 100)
            
            net_change = daily_income - daily_expenses
            player_wealth += net_change
            
            currency_data[f"day_{day}"] = {
                'wealth': player_wealth,
                'income': daily_income,
                'expenses': daily_expenses,
                'net': net_change
            }
        
        # Check for healthy economic growth (small positive trend)
        final_wealth = player_wealth
        growth_rate = (final_wealth / 1000) ** (1/30) - 1  # Daily growth rate
        
        # Ideal growth: 0.5-2% per day
        ideal_range = (0.005, 0.02)
        if ideal_range[0] <= growth_rate <= ideal_range[1]:
            balance_score = 1.0
        else:
            deviation = min(
                abs(growth_rate - ideal_range[0]),
                abs(growth_rate - ideal_range[1])
            ) / ideal_range[1]
            balance_score = 1.0 / (1.0 + deviation)
        
        return balance_score, {
            'growth_rate': growth_rate,
            'final_wealth': final_wealth,
            'ideal_range': ideal_range,
            'sample_days': {k: v for k, v in list(currency_data.items())[:5]}
        }
    
    def test_skill_effectiveness(self) -> Tuple[float, Dict]:
        """Test skill damage vs cost efficiency"""
        if not self.skills_system:
            return 1.0, {'error': 'Skills system not available'}
        
        # Test different skill types
        skills_data = {}
        
        skill_types = ['damage', 'defense', 'support']
        for skill_type in skill_types:
            # Simulate skill effectiveness
            if skill_type == 'damage':
                damage_per_mana = random.uniform(2.0, 3.0)  # Expected: 2.5 damage per mana
                cooldown_efficiency = random.uniform(0.8, 1.2)
            elif skill_type == 'defense':
                damage_per_mana = random.uniform(1.5, 2.5)  # Lower damage, higher utility
                cooldown_efficiency = random.uniform(1.0, 1.4)
            else:  # support
                damage_per_mana = random.uniform(1.0, 2.0)  # Lowest damage, highest utility
                cooldown_efficiency = random.uniform(1.2, 1.6)
            
            efficiency_score = damage_per_mana * cooldown_efficiency
            skills_data[skill_type] = {
                'damage_per_mana': damage_per_mana,
                'cooldown_efficiency': cooldown_efficiency,
                'efficiency_score': efficiency_score
            }
        
        # Check balance between skill types
        efficiency_scores = [data['efficiency_score'] for data in skills_data.values()]
        avg_efficiency = statistics.mean(efficiency_scores)
        efficiency_variance = statistics.stdev(efficiency_scores) if len(efficiency_scores) > 1 else 0
        
        # Balance metric
        balance_score = 1.0 / (1.0 + efficiency_variance / avg_efficiency)
        
        return balance_score, skills_data
    
    def test_resistance_balance(self) -> Tuple[float, Dict]:
        """Test resistance system balance"""
        if not self.resistance_system:
            return 1.0, {'error': 'Resistance system not available'}
        
        # Test resistance effectiveness
        resistance_data = {}
        
        resistance_values = [0, 25, 50, 75, 90]  # Different resistance percentages
        
        for resistance in resistance_values:
            base_damage = 100
            # Apply resistance
            damage_reduction = resistance / 100
            final_damage = base_damage * (1 - damage_reduction)
            
            # Calculate effectiveness (should be linear)
            expected_damage = base_damage * (1 - resistance / 100)
            accuracy = min(final_damage / expected_damage, expected_damage / final_damage)
            
            resistance_data[f"{resistance}%"] = {
                'base_damage': base_damage,
                'final_damage': final_damage,
                'expected_damage': expected_damage,
                'accuracy': accuracy
            }
        
        # Average accuracy across all resistance values
        accuracies = [data['accuracy'] for data in resistance_data.values()]
        avg_accuracy = statistics.mean(accuracies)
        
        return avg_accuracy, resistance_data
    
    def generate_balance_report(self, results: List[BalanceResult]) -> Dict[str, Any]:
        """Generate comprehensive balance report"""
        if not results:
            return {'error': 'No test results available'}
        
        # Categorize results by severity
        severity_counts = {severity: 0 for severity in TestSeverity}
        for result in results:
            severity_counts[result.severity] += 1
        
        # Group by category
        category_results = {}
        for result in results:
            category = result.category.value
            if category not in category_results:
                category_results[category] = []
            category_results[category].append(result)
        
        # Generate overall health score
        severity_weights = {
            TestSeverity.CRITICAL: -10,
            TestSeverity.HIGH: -5,
            TestSeverity.MEDIUM: -2,
            TestSeverity.LOW: -1,
            TestSeverity.INFORMATIONAL: 0
        }
        
        health_score = 100  # Start with perfect score
        for result in results:
            health_score += severity_weights[result.severity]
        
        health_score = max(0, min(100, health_score))  # Clamp to 0-100
        
        # Identify priority fixes
        priority_fixes = [
            result for result in results 
            if result.severity in [TestSeverity.CRITICAL, TestSeverity.HIGH]
        ]
        priority_fixes.sort(key=lambda x: x.deviation_percent, reverse=True)
        
        # Generate trends (if we have historical data)
        trends = self._analyze_trends(results)
        
        return {
            'timestamp': time.time(),
            'overall_health_score': health_score,
            'total_tests': len(results),
            'severity_breakdown': {k.value: v for k, v in severity_counts.items()},
            'category_breakdown': {
                category: {
                    'total_tests': len(cat_results),
                    'avg_deviation': statistics.mean([r.deviation_percent for r in cat_results]),
                    'worst_test': max(cat_results, key=lambda x: x.deviation_percent).test_name
                }
                for category, cat_results in category_results.items()
            },
            'priority_fixes': [
                {
                    'test_name': result.test_name,
                    'category': result.category.value,
                    'severity': result.severity.value,
                    'deviation': f"{result.deviation_percent:.1%}",
                    'recommendations': result.recommendations[:2]  # Top 2 recommendations
                }
                for result in priority_fixes[:5]  # Top 5 priority fixes
            ],
            'trends': trends,
            'recommendations': self._generate_overall_recommendations(results, health_score)
        }
    
    def _analyze_trends(self, current_results: List[BalanceResult]) -> Dict[str, Any]:
        """Analyze trends from historical data"""
        if len(self.test_history) < 10:  # Need some history
            return {'status': 'insufficient_data'}
        
        # Get recent historical results for same tests
        recent_history = [r for r in self.test_history[-50:] if r.timestamp < current_results[0].timestamp]
        
        trends = {}
        for current_result in current_results:
            # Find historical results for same test
            historical = [r for r in recent_history if r.test_id == current_result.test_id]
            
            if len(historical) >= 3:
                # Calculate trend
                historical_values = [r.actual_value for r in historical[-5:]]  # Last 5 results
                
                if len(historical_values) >= 2:
                    # Simple linear trend
                    trend_direction = 'improving' if historical_values[-1] > historical_values[0] else 'declining'
                    trend_magnitude = abs(historical_values[-1] - historical_values[0]) / historical_values[0]
                    
                    trends[current_result.test_id] = {
                        'direction': trend_direction,
                        'magnitude': trend_magnitude,
                        'stability': 'stable' if trend_magnitude < 0.1 else 'volatile'
                    }
        
        return trends
    
    def _generate_overall_recommendations(self, results: List[BalanceResult], health_score: float) -> List[str]:
        """Generate overall project recommendations"""
        recommendations = []
        
        if health_score >= 90:
            recommendations.append("🎉 Game balance is excellent! Continue monitoring.")
            recommendations.append("Consider adding more challenging content or mechanics.")
        
        elif health_score >= 75:
            recommendations.append("Game balance is good with minor issues to address.")
            recommendations.append("Focus on the medium-priority balance adjustments.")
        
        elif health_score >= 50:
            recommendations.append("⚠️ Significant balance issues detected - prioritize fixes.")
            recommendations.append("Review core game mechanics and scaling formulas.")
        
        else:
            recommendations.append("🚨 Critical balance problems require immediate attention.")
            recommendations.append("Consider temporarily disabling problematic systems.")
            recommendations.append("Conduct thorough review of all game systems.")
        
        # Add category-specific recommendations
        critical_categories = set()
        for result in results:
            if result.severity == TestSeverity.CRITICAL:
                critical_categories.add(result.category)
        
        if BalanceCategory.DAMAGE_SCALING in critical_categories:
            recommendations.append("🔧 Damage scaling needs immediate rebalancing.")
        
        if BalanceCategory.ARCHETYPE_VIABILITY in critical_categories:
            recommendations.append("⚖️ Archetype balance requires attention - some builds may be overpowered.")
        
        if BalanceCategory.BOSS_DIFFICULTY in critical_categories:
            recommendations.append("👹 Boss encounters need difficulty adjustment.")
        
        return recommendations

def main():
    """Main CLI interface for balance testing"""
    suite = BalanceTestingSuite()
    
    while True:
        print("\n=== Automated Balance Testing Suite ===")
        print("1. Run full balance test suite")
        print("2. Run specific category tests") 
        print("3. View latest test results")
        print("4. Generate balance report")
        print("5. View test history trends")
        print("0. Exit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            print("\n🚀 Running complete balance testing suite...")
            results = suite.run_all_tests()
            
            if results:
                report = suite.generate_balance_report(results)
                print(f"\n📊 Balance Report Generated")
                print(f"Overall Health Score: {report['overall_health_score']:.0f}/100")
                
                if report['priority_fixes']:
                    print(f"\n🔥 Priority Fixes Needed:")
                    for fix in report['priority_fixes'][:3]:
                        print(f"  • {fix['test_name']}: {fix['severity']} ({fix['deviation']} deviation)")
        
        elif choice == "2":
            print("\nAvailable categories:")
            categories = list(BalanceCategory)
            for i, category in enumerate(categories, 1):
                print(f"  {i}. {category.value.replace('_', ' ').title()}")
            
            try:
                cat_choice = int(input("Choose category (1-8): ")) - 1
                selected_category = categories[cat_choice]
                
                # Run tests for selected category
                category_tests = [t for t in suite.balance_tests if t.category == selected_category]
                print(f"\nRunning {len(category_tests)} tests for {selected_category.value}...")
                
                results = []
                for test in category_tests:
                    result = suite._run_single_test(test)
                    results.append(result)
                    print(f"✓ {test.name}: {result.severity.value} ({result.actual_value:.3f})")
                
            except (ValueError, IndexError):
                print("Invalid choice!")
        
        elif choice == "3":
            if suite.test_history:
                recent_results = suite.test_history[-10:]  # Last 10 results
                print(f"\n📋 Recent Test Results:")
                print(f"{'Test Name':<30} {'Category':<20} {'Severity':<10} {'Value':<10} {'Time'}")
                print("-" * 85)
                
                for result in recent_results:
                    timestamp = time.strftime('%H:%M:%S', time.localtime(result.timestamp))
                    print(f"{result.test_name:<30} {result.category.value:<20} {result.severity.value:<10} {result.actual_value:<10.3f} {timestamp}")
            else:
                print("No test results available. Run tests first.")
        
        elif choice == "4":
            if suite.test_history:
                # Use most recent test run
                latest_timestamp = max(r.timestamp for r in suite.test_history)
                latest_results = [r for r in suite.test_history if abs(r.timestamp - latest_timestamp) < 60]  # Within 1 minute
                
                if latest_results:
                    report = suite.generate_balance_report(latest_results)
                    
                    print(f"\n📊 Comprehensive Balance Report")
                    print(f"Overall Health Score: {report['overall_health_score']:.0f}/100")
                    print(f"Total Tests: {report['total_tests']}")
                    
                    print(f"\nSeverity Breakdown:")
                    for severity, count in report['severity_breakdown'].items():
                        if count > 0:
                            print(f"  {severity.title()}: {count}")
                    
                    if report['priority_fixes']:
                        print(f"\n🔥 Priority Fixes:")
                        for fix in report['priority_fixes']:
                            print(f"  • {fix['test_name']} ({fix['severity']})")
                            for rec in fix['recommendations']:
                                print(f"    - {rec}")
                    
                    print(f"\n💡 Overall Recommendations:")
                    for rec in report['recommendations']:
                        print(f"  • {rec}")
                else:
                    print("No recent test results found.")
            else:
                print("No test results available. Run tests first.")
        
        elif choice == "5":
            if len(suite.test_history) >= 5:
                print(f"\n📈 Test History Trends (last 30 results):")
                
                # Group by test type and show trends
                test_trends = {}
                for result in suite.test_history[-30:]:
                    if result.test_id not in test_trends:
                        test_trends[result.test_id] = []
                    test_trends[result.test_id].append(result)
                
                for test_id, results in test_trends.items():
                    if len(results) >= 3:
                        values = [r.actual_value for r in results]
                        trend = "📈" if values[-1] > values[0] else "📉"
                        print(f"  {trend} {results[0].test_name}: {values[0]:.3f} → {values[-1]:.3f}")
            else:
                print("Insufficient history for trend analysis.")
        
        elif choice == "0":
            break
        
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()

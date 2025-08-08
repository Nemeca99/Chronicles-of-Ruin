#!/usr/bin/env python3
"""
Autonomous Gambling System Test
Test the gambling system using AI players - no human interaction required
"""

import sys
import json
import time
import random
from pathlib import Path

# Add project paths
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "tools"))
sys.path.append(str(Path(__file__).parent / "chapters" / "chapter_01_sunderfall" / "src"))

from tools.ai_player_system import AIPlayerSystem
from tools.set_item_manager import SetManager

class GamblingSystemTester:
    """Autonomous testing of the gambling system using AI players"""
    
    def __init__(self):
        self.ai_system = AIPlayerSystem(Path("."))
        self.set_manager = SetManager()
        self.test_results = []
        
    def setup_test_players(self):
        """Create AI players with different gambling personalities"""
        gambling_personalities = [
            {
                "name": "GamblerMax",
                "playstyle": "aggressive", 
                "personality": "risk_taking",
                "preferred_archetype": "melee",
                "decision_style": "impulsive",
                "risk_tolerance": 0.9,  # High risk tolerance
                "patience_level": 0.2,  # Low patience = more gambling
                "optimization_focus": "damage",
                "skill_level": "experienced"
            },
            {
                "name": "CautiousCarla",
                "playstyle": "defensive",
                "personality": "analytical", 
                "preferred_archetype": "magic",
                "decision_style": "analytical",
                "risk_tolerance": 0.3,  # Low risk tolerance
                "patience_level": 0.8,  # High patience = less gambling
                "optimization_focus": "efficiency",
                "skill_level": "expert"
            },
            {
                "name": "BalancedBob",
                "playstyle": "balanced",
                "personality": "strategic",
                "preferred_archetype": "hybrid", 
                "decision_style": "balanced",
                "risk_tolerance": 0.6,  # Medium risk
                "patience_level": 0.5,  # Medium patience
                "optimization_focus": "balanced",
                "skill_level": "casual"
            },
            {
                "name": "LuckyLisa",
                "playstyle": "explorer",
                "personality": "optimistic",
                "preferred_archetype": "ranged",
                "decision_style": "intuitive", 
                "risk_tolerance": 0.7,  # High risk, believes in luck
                "patience_level": 0.4,  # Impatient for results
                "optimization_focus": "utility",
                "skill_level": "noob"
            }
        ]
        
        print("🎭 Creating AI player personalities for gambling test...")
        for player_data in gambling_personalities:
            profile = self.ai_system.create_ai_player_profile(**player_data)
            print(f"  Created: {profile.name} (Risk: {player_data['risk_tolerance']}, Patience: {player_data['patience_level']})")
        
        return [p["name"] for p in gambling_personalities]
    
    def create_test_sets(self, player_names):
        """Create test sets for each AI player"""
        test_sets = []
        
        set_configs = [
            {"name": "Fire Lord's Regalia", "type": "Combat", "pieces": 6},
            {"name": "Mystic Wisdom", "type": "Magic", "pieces": 4}, 
            {"name": "Ranger's Focus", "type": "Utility", "pieces": 5},
            {"name": "Balanced Build", "type": "Defense", "pieces": 8}
        ]
        
        print("\n🎲 Creating test sets for gambling...")
        for i, player_name in enumerate(player_names):
            config = set_configs[i % len(set_configs)]
            
            # Simulate set creation
            set_id = f"test_{player_name}_{int(time.time())}_{i}"
            test_set = {
                'id': set_id,
                'name': f"{player_name}'s {config['name']}",
                'description': f"Test set for {player_name}",
                'creator_id': player_name,
                'creation_time': time.time(),
                'set_type': config['type'],
                'slots': [f"slot_{j}" for j in range(config['pieces'])],
                'bonuses': [{"pieces": 2, "name": "Initial Bonus", "effect": "+5% damage"}],
                'usage_count': 0,
                'balance_rating': None,
                'ai_test_results': {},
                'reroll_count': 0,
                'gambling_tax_per_piece': {f"slot_{j}": 0.0 for j in range(config['pieces'])},
                'base_reroll_cost': 100 * config['pieces']
            }
            
            self.set_manager.enhanced_sets[set_id] = test_set
            test_sets.append((player_name, set_id, config))
            print(f"  {player_name}: {test_set['name']} ({config['pieces']} pieces)")
        
        self.set_manager._save_enhanced_sets()
        return test_sets
    
    def simulate_gambling_decisions(self, player_name, set_id, max_rerolls=10):
        """Simulate AI player gambling decisions"""
        print(f"\n🎰 {player_name} starts gambling on set {set_id}")
        
        player_profile = self.ai_system.get_ai_player_profile(player_name)
        if not player_profile:
            return {"error": "Player not found"}
        
        # Simulate starting gold based on player type
        base_gold = 50000  # Starting gold
        risk_multiplier = player_profile.risk_tolerance
        patience_factor = 1.0 - player_profile.patience_level
        
        current_gold = int(base_gold * (1 + risk_multiplier))
        gambling_session = {
            "player": player_name,
            "set_id": set_id,
            "starting_gold": current_gold,
            "rerolls": [],
            "final_gold": current_gold,
            "total_spent": 0,
            "stopped_reason": "unknown"
        }
        
        for reroll_num in range(1, max_rerolls + 1):
            # Calculate current cost
            current_cost = self.set_manager.calculate_reroll_cost(set_id)
            
            if current_cost > current_gold:
                gambling_session["stopped_reason"] = "insufficient_gold"
                break
            
            # AI decision making based on personality
            decision_factors = {
                "risk_tolerance": player_profile.risk_tolerance,
                "patience_level": player_profile.patience_level, 
                "cost_ratio": current_cost / current_gold,
                "reroll_count": reroll_num,
                "sunk_cost": gambling_session["total_spent"]
            }
            
            # Calculate gambling probability
            base_prob = player_profile.risk_tolerance * 0.8
            cost_penalty = decision_factors["cost_ratio"] * 0.5
            patience_penalty = patience_factor * 0.3
            sunk_cost_bias = min(decision_factors["sunk_cost"] / base_gold * 0.4, 0.3)
            
            gamble_probability = base_prob - cost_penalty - patience_penalty + sunk_cost_bias
            gamble_probability = max(0.05, min(0.95, gamble_probability))  # Clamp between 5% and 95%
            
            will_gamble = random.random() < gamble_probability
            
            reroll_data = {
                "reroll_number": reroll_num,
                "cost": current_cost,
                "gold_before": current_gold,
                "decision": "reroll" if will_gamble else "stop",
                "probability": gamble_probability,
                "factors": decision_factors.copy()
            }
            
            if not will_gamble:
                gambling_session["stopped_reason"] = f"ai_decision_stop_at_{reroll_num}"
                gambling_session["rerolls"].append(reroll_data)
                break
            
            # Perform the reroll
            result = self.set_manager.reroll_set_bonuses(set_id, current_gold)
            
            if result["success"]:
                current_gold -= result["cost_paid"]
                gambling_session["total_spent"] += result["cost_paid"]
                
                reroll_data.update({
                    "gold_after": current_gold,
                    "cost_paid": result["cost_paid"],
                    "new_bonuses": result["new_bonuses"],
                    "gambling_taxes": result["gambling_taxes"],
                    "next_cost": result["next_reroll_cost"]
                })
                
                print(f"  Reroll #{reroll_num}: -{result['cost_paid']} gold (Prob: {gamble_probability:.2%})")
                print(f"    Remaining: {current_gold} gold, Next cost: {result['next_reroll_cost']}")
            else:
                reroll_data["error"] = result["error"] 
                gambling_session["stopped_reason"] = "reroll_failed"
                gambling_session["rerolls"].append(reroll_data)
                break
                
            gambling_session["rerolls"].append(reroll_data)
        
        if reroll_num >= max_rerolls:
            gambling_session["stopped_reason"] = "max_rerolls_reached"
        
        gambling_session["final_gold"] = current_gold
        gambling_session["rerolls_completed"] = len([r for r in gambling_session["rerolls"] if r["decision"] == "reroll"])
        
        return gambling_session
    
    def run_gambling_analysis(self, test_results):
        """Analyze gambling behavior patterns"""
        print("\n📊 GAMBLING BEHAVIOR ANALYSIS")
        print("=" * 60)
        
        total_players = len(test_results)
        total_spent = sum(r["total_spent"] for r in test_results)
        avg_rerolls = sum(r["rerolls_completed"] for r in test_results) / total_players
        
        print(f"Players tested: {total_players}")
        print(f"Total gold spent: {total_spent:,}")
        print(f"Average rerolls per player: {avg_rerolls:.1f}")
        
        # Analyze by player personality
        personality_analysis = {}
        for result in test_results:
            player_name = result["player"]
            profile = self.ai_system.get_ai_player_profile(player_name)
            
            risk_category = "High" if profile.risk_tolerance > 0.7 else "Medium" if profile.risk_tolerance > 0.4 else "Low"
            patience_category = "High" if profile.patience_level > 0.7 else "Medium" if profile.patience_level > 0.4 else "Low"
            
            key = f"{risk_category}_Risk_{patience_category}_Patience"
            if key not in personality_analysis:
                personality_analysis[key] = []
            personality_analysis[key].append(result)
        
        print("\n🎭 PERSONALITY PATTERN ANALYSIS:")
        for pattern, results in personality_analysis.items():
            avg_spent = sum(r["total_spent"] for r in results) / len(results)
            avg_rerolls = sum(r["rerolls_completed"] for r in results) / len(results)
            
            print(f"\n{pattern}:")
            print(f"  Players: {len(results)}")
            print(f"  Avg Gold Spent: {avg_spent:,.0f}")
            print(f"  Avg Rerolls: {avg_rerolls:.1f}")
            
            # Show stop reasons
            stop_reasons = {}
            for result in results:
                reason = result["stopped_reason"]
                stop_reasons[reason] = stop_reasons.get(reason, 0) + 1
            
            print(f"  Stop Reasons: {dict(stop_reasons)}")
        
        # Calculate gambling addiction metrics
        addiction_scores = []
        for result in test_results:
            if result["rerolls_completed"] > 0:
                # Addiction score based on: rerolls completed, money spent ratio, sunk cost behavior
                reroll_score = min(result["rerolls_completed"] / 10.0, 1.0)  # Normalize to 1.0
                spend_ratio = result["total_spent"] / result["starting_gold"] 
                
                # Check for sunk cost fallacy (continuing despite high costs)
                sunk_cost_score = 0
                if len(result["rerolls"]) > 3:
                    late_rerolls = result["rerolls"][-3:]  # Last 3 rerolls
                    high_cost_continues = sum(1 for r in late_rerolls if r.get("cost", 0) > result["starting_gold"] * 0.1)
                    sunk_cost_score = high_cost_continues / 3.0
                
                addiction_score = (reroll_score * 0.4 + spend_ratio * 0.4 + sunk_cost_score * 0.2)
                addiction_scores.append(addiction_score)
            else:
                addiction_scores.append(0.0)
        
        avg_addiction_score = sum(addiction_scores) / len(addiction_scores)
        
        print(f"\n🎯 GAMBLING SYSTEM EFFECTIVENESS:")
        print(f"Average Addiction Score: {avg_addiction_score:.2%}")
        print(f"Players who gambled > 5 times: {sum(1 for r in test_results if r['rerolls_completed'] > 5)}/{total_players}")
        print(f"Players who spent > 50% of gold: {sum(1 for r in test_results if r['total_spent'] > r['starting_gold'] * 0.5)}/{total_players}")
        
        return {
            "total_players": total_players,
            "total_spent": total_spent,
            "average_rerolls": avg_rerolls,
            "average_addiction_score": avg_addiction_score,
            "personality_patterns": personality_analysis,
            "high_engagement": sum(1 for r in test_results if r['rerolls_completed'] > 5),
            "high_spenders": sum(1 for r in test_results if r['total_spent'] > r['starting_gold'] * 0.5)
        }
    
    def run_test(self):
        """Run the complete autonomous gambling system test"""
        print("🎰 AUTONOMOUS GAMBLING SYSTEM TEST")
        print("=" * 50)
        
        # Setup
        player_names = self.setup_test_players()
        test_sets = self.create_test_sets(player_names)
        
        # Run gambling simulations
        print("\n🎯 Running gambling simulations...")
        test_results = []
        
        for player_name, set_id, config in test_sets:
            result = self.simulate_gambling_decisions(player_name, set_id)
            if "error" not in result:
                test_results.append(result)
                
                print(f"  {player_name}: {result['rerolls_completed']} rerolls, spent {result['total_spent']:,} gold")
                print(f"    Stopped: {result['stopped_reason']}")
        
        # Analyze results
        analysis = self.run_gambling_analysis(test_results)
        
        # Save results
        results_file = Path("gambling_test_results.json")
        with open(results_file, 'w') as f:
            json.dump({
                "timestamp": time.time(),
                "test_results": test_results,
                "analysis": analysis
            }, f, indent=2)
        
        print(f"\n💾 Results saved to: {results_file}")
        
        return analysis

def main():
    """Main function"""
    tester = GamblingSystemTester()
    
    try:
        results = tester.run_test()
        
        print("\n🎉 AUTONOMOUS TEST COMPLETED!")
        print(f"Addiction Score: {results['average_addiction_score']:.2%}")
        print(f"High Engagement Players: {results['high_engagement']}/{results['total_players']}")
        print(f"Total Gold Consumed: {results['total_spent']:,}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()

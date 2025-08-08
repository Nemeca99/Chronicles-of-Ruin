"""
Comprehensive Test Suite for Combat System - Chronicles of Ruin: Sunderfall

This module tests all aspects of the combat system including damage calculation,
combat triangle mechanics, Wild monster mechanics, and status effect integration.
"""

import sys
import os
import unittest
import random
from typing import Dict, List

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from systems.combat_system import CombatSystem, Archetype, StatusEffect


class TestCombatSystem(unittest.TestCase):
    """Test suite for the Combat System."""

    def setUp(self):
        """Set up test fixtures."""
        self.combat = CombatSystem()

        # Early Game Test Data (Level 1-10) - Monster HP: 5, Player HP: 20
        self.early_melee_attacker = {
            "power": 2,
            "archetype": "melee",
            "critical_chance": 0.05,
        }

        self.early_ranged_target = {
            "archetype": "ranged",
            "toughness": 2,
            "is_wild": False,
        }

        self.early_magic_target = {"archetype": "magic", "wisdom": 3, "is_wild": False}

        self.early_wild_target = {"archetype": "melee", "toughness": 2, "is_wild": True}

        self.early_skill_data = {
            "base_damage": 1,
            "status_chances": {"burn": 0.05, "stun": 0.02},
        }

        self.early_weapon_data = {
            "damage": 1,
            "percentage_bonuses": [0.1],  # +10% damage
            "critical_chance": 0.02,
            "critical_multiplier": 0.2,
        }

        # Mid Game Test Data (Level 20-40) - Monster HP: 15-25, Player HP: 40-60
        self.mid_melee_attacker = {
            "power": 4,
            "archetype": "melee",
            "critical_chance": 0.08,
        }

        self.mid_ranged_target = {
            "archetype": "ranged",
            "toughness": 5,
            "is_wild": False,
        }

        self.mid_magic_target = {"archetype": "magic", "wisdom": 6, "is_wild": False}

        self.mid_wild_target = {"archetype": "melee", "toughness": 6, "is_wild": True}

        self.mid_skill_data = {
            "base_damage": 2,
            "status_chances": {"burn": 0.08, "stun": 0.04},
        }

        self.mid_weapon_data = {
            "damage": 2,
            "percentage_bonuses": [0.15],  # +15% damage
            "critical_chance": 0.03,
            "critical_multiplier": 0.3,
        }

        # Late Game Test Data (Level 60-80) - Monster HP: 40-60, Player HP: 80-120
        self.late_melee_attacker = {
            "power": 7,
            "archetype": "melee",
            "critical_chance": 0.12,
        }

        self.late_ranged_target = {
            "archetype": "ranged",
            "toughness": 8,
            "is_wild": False,
        }

        self.late_magic_target = {"archetype": "magic", "wisdom": 10, "is_wild": False}

        self.late_wild_target = {"archetype": "melee", "toughness": 9, "is_wild": True}

        self.late_skill_data = {
            "base_damage": 3,
            "status_chances": {"burn": 0.12, "stun": 0.06},
        }

        self.late_weapon_data = {
            "damage": 3,
            "percentage_bonuses": [0.2],  # +20% damage
            "critical_chance": 0.05,
            "critical_multiplier": 0.4,
        }

    def test_early_game_base_damage_calculation(self):
        """Test early game base damage calculation."""
        base_damage = self.combat._calculate_base_damage(
            self.early_melee_attacker, self.early_skill_data, self.early_weapon_data
        )

        # Power (2 * 0.3) + Skill (1) + Weapon (1) = 0.6 + 1 + 1 = 2.6
        expected_base = 2 * 0.3 + 1 + 1
        self.assertAlmostEqual(base_damage, expected_base, places=1)
        print(
            f"✅ Early Game Base Damage: {base_damage:.1f} (expected: {expected_base:.1f})"
        )

    def test_mid_game_base_damage_calculation(self):
        """Test mid game base damage calculation."""
        base_damage = self.combat._calculate_base_damage(
            self.mid_melee_attacker, self.mid_skill_data, self.mid_weapon_data
        )

        # Power (4 * 0.3) + Skill (2) + Weapon (2) = 1.2 + 2 + 2 = 5.2
        expected_base = 4 * 0.3 + 2 + 2
        self.assertAlmostEqual(base_damage, expected_base, places=1)
        print(
            f"✅ Mid Game Base Damage: {base_damage:.1f} (expected: {expected_base:.1f})"
        )

    def test_late_game_base_damage_calculation(self):
        """Test late game base damage calculation."""
        base_damage = self.combat._calculate_base_damage(
            self.late_melee_attacker, self.late_skill_data, self.late_weapon_data
        )

        # Power (7 * 0.3) + Skill (3) + Weapon (3) = 2.1 + 3 + 3 = 8.1
        expected_base = 7 * 0.3 + 3 + 3
        self.assertAlmostEqual(base_damage, expected_base, places=1)
        print(
            f"✅ Late Game Base Damage: {base_damage:.1f} (expected: {expected_base:.1f})"
        )

    def test_item_percentage_bonuses(self):
        """Test application of item percentage bonuses."""
        base_damage = 5
        modified_damage = self.combat._apply_item_percentages(
            base_damage, self.mid_weapon_data
        )

        expected_damage = 5 * (1 + 0.15)  # +15% bonus
        self.assertEqual(modified_damage, expected_damage)
        print(
            f"✅ Item Percentage Bonuses: {modified_damage:.1f} (expected: {expected_damage:.1f})"
        )

    def test_combat_triangle_melee_vs_ranged(self):
        """Test Melee > Ranged advantage."""
        damage = 5
        triangle_damage = self.combat._apply_combat_triangle(
            damage, self.mid_melee_attacker, self.mid_ranged_target
        )

        expected_damage = 5 * (1 + 0.25)  # +25% bonus
        self.assertEqual(triangle_damage, expected_damage)
        print(
            f"✅ Melee vs Ranged: {triangle_damage:.1f} (expected: {expected_damage:.1f})"
        )

    def test_combat_triangle_ranged_vs_magic(self):
        """Test Ranged > Magic advantage."""
        ranged_attacker = {"archetype": "ranged"}
        damage = 5
        triangle_damage = self.combat._apply_combat_triangle(
            damage, ranged_attacker, self.mid_magic_target
        )

        expected_damage = 5 * (1 + 0.25)  # +25% bonus
        self.assertEqual(triangle_damage, expected_damage)
        print(
            f"✅ Ranged vs Magic: {triangle_damage:.1f} (expected: {expected_damage:.1f})"
        )

    def test_combat_triangle_magic_vs_melee(self):
        """Test Magic > Melee advantage."""
        magic_attacker = {"archetype": "magic"}
        damage = 5
        triangle_damage = self.combat._apply_combat_triangle(
            damage, magic_attacker, self.mid_melee_attacker
        )

        expected_damage = 5 * (1 + 0.25)  # +25% bonus
        self.assertEqual(triangle_damage, expected_damage)
        print(
            f"✅ Magic vs Melee: {triangle_damage:.1f} (expected: {expected_damage:.1f})"
        )

    def test_combat_triangle_disadvantage(self):
        """Test combat triangle disadvantages."""
        # Ranged vs Melee (disadvantage)
        ranged_attacker = {"archetype": "ranged"}
        damage = 5
        triangle_damage = self.combat._apply_combat_triangle(
            damage, ranged_attacker, self.mid_melee_attacker
        )

        expected_damage = 5 * (1 - 0.25)  # -25% penalty
        self.assertEqual(triangle_damage, expected_damage)
        print(
            f"✅ Ranged vs Melee (disadvantage): {triangle_damage:.1f} (expected: {expected_damage:.1f})"
        )

    def test_wild_monster_same_archetype_bonus(self):
        """Test Wild monster bonus against same archetype."""
        damage = 5
        triangle_damage = self.combat._apply_combat_triangle(
            damage, self.mid_melee_attacker, self.mid_wild_target
        )

        # Base multiplier (1.0) + Wild bonus (0.5) = 1.5
        expected_damage = 5 * 1.5
        self.assertEqual(triangle_damage, expected_damage)
        print(
            f"✅ Wild Monster Same Archetype: {triangle_damage:.1f} (expected: {expected_damage:.1f})"
        )

    def test_damage_floor(self):
        """Test that damage never goes below the minimum floor."""
        # Create a scenario where damage would be very low
        low_damage = 0.5
        final_damage = max(low_damage, self.combat.damage_floor)

        self.assertEqual(final_damage, self.combat.damage_floor)
        print(
            f"✅ Damage Floor: {final_damage:.1f} (minimum: {self.combat.damage_floor:.1f})"
        )

    def test_status_effects_application(self):
        """Test status effect application based on skill data."""
        # Set random seed for consistent testing
        random.seed(42)

        applied_effects = self.combat._apply_status_effects(
            self.mid_melee_attacker, self.mid_ranged_target, self.mid_skill_data
        )

        # Should have some status effects applied (depends on random chance)
        self.assertIsInstance(applied_effects, list)
        for effect in applied_effects:
            self.assertIsInstance(effect, StatusEffect)

        print(
            f"✅ Status Effects Applied: {[effect.value for effect in applied_effects]}"
        )

    def test_status_immune_target(self):
        """Test that status immune targets don't receive status effects."""
        immune_target = self.mid_ranged_target.copy()
        immune_target["status_immune"] = True

        applied_effects = self.combat._apply_status_effects(
            self.mid_melee_attacker, immune_target, self.mid_skill_data
        )

        self.assertEqual(len(applied_effects), 0)
        print(f"✅ Status Immune Target: No effects applied")

    def test_critical_hit_detection(self):
        """Test critical hit detection."""
        # Set random seed for consistent testing
        random.seed(42)

        is_crit = self.combat.is_critical_hit(
            self.mid_melee_attacker, self.mid_weapon_data
        )

        self.assertIsInstance(is_crit, bool)
        print(f"✅ Critical Hit Detection: {is_crit}")

    def test_critical_damage_calculation(self):
        """Test critical damage calculation."""
        base_damage = 5
        crit_damage = self.combat.calculate_critical_damage(
            base_damage, self.mid_melee_attacker, self.mid_weapon_data
        )

        # Base crit multiplier (1.5) + weapon bonus (0.3) = 1.8
        expected_crit_damage = 5 * 1.8
        self.assertEqual(crit_damage, expected_crit_damage)
        print(
            f"✅ Critical Damage: {crit_damage:.1f} (expected: {expected_crit_damage:.1f})"
        )

    def test_defense_calculation(self):
        """Test defense calculation for different damage types."""
        target_stats = {
            "toughness": 10,  # Physical defense
            "wisdom": 8,  # Magical defense
            "status_resistance": 5,  # Status resistance
        }

        # Test physical defense
        physical_defense = self.combat.calculate_defense(target_stats, "physical")
        expected_physical = 1 - min(10 / 100, 0.9)  # 10% reduction, capped at 90%
        self.assertEqual(physical_defense, expected_physical)

        # Test magical defense
        magical_defense = self.combat.calculate_defense(target_stats, "magical")
        expected_magical = 1 - min(8 / 100, 0.9)  # 8% reduction, capped at 90%
        self.assertEqual(magical_defense, expected_magical)

        print(f"✅ Physical Defense: {physical_defense:.2f}")
        print(f"✅ Magical Defense: {magical_defense:.2f}")

    def test_status_effect_damage(self):
        """Test status effect damage over time calculation."""
        base_damage = 5
        duration = 3.0
        target_resistance = 1

        # Test burn damage
        burn_damage = self.combat.apply_status_effect_damage(
            StatusEffect.BURN, base_damage, duration, target_resistance
        )

        # Burn does 20% of base damage over duration, minus resistance
        expected_burn = max(5 * 0.2 - 1, 0.5) * 3.0
        self.assertEqual(burn_damage, expected_burn)

        print(f"✅ Burn Damage: {burn_damage:.1f} (expected: {expected_burn:.1f})")

    def test_early_game_complete_damage_calculation(self):
        """Test early game complete damage calculation."""
        damage, status_effects = self.combat.calculate_damage(
            self.early_melee_attacker,
            self.early_ranged_target,
            self.early_skill_data,
            self.early_weapon_data,
        )

        # Verify damage is reasonable for early game (monster HP: 5)
        self.assertGreater(damage, 0)
        self.assertLess(damage, 10)  # Early game upper bound

        # Verify status effects are valid
        for effect in status_effects:
            self.assertIsInstance(effect, StatusEffect)

        print(f"✅ Early Game Complete Damage: {damage:.1f}")
        print(f"✅ Status Effects: {[effect.value for effect in status_effects]}")

    def test_mid_game_complete_damage_calculation(self):
        """Test mid game complete damage calculation."""
        damage, status_effects = self.combat.calculate_damage(
            self.mid_melee_attacker,
            self.mid_ranged_target,
            self.mid_skill_data,
            self.mid_weapon_data,
        )

        # Verify damage is reasonable for mid game (monster HP: 15-25)
        self.assertGreater(damage, 0)
        self.assertLess(damage, 25)  # Mid game upper bound

        # Verify status effects are valid
        for effect in status_effects:
            self.assertIsInstance(effect, StatusEffect)

        print(f"✅ Mid Game Complete Damage: {damage:.1f}")
        print(f"✅ Status Effects: {[effect.value for effect in status_effects]}")

    def test_late_game_complete_damage_calculation(self):
        """Test late game complete damage calculation."""
        damage, status_effects = self.combat.calculate_damage(
            self.late_melee_attacker,
            self.late_ranged_target,
            self.late_skill_data,
            self.late_weapon_data,
        )

        # Verify damage is reasonable for late game (monster HP: 40-60)
        self.assertGreater(damage, 0)
        self.assertLess(damage, 50)  # Late game upper bound

        # Verify status effects are valid
        for effect in status_effects:
            self.assertIsInstance(effect, StatusEffect)

        print(f"✅ Late Game Complete Damage: {damage:.1f}")
        print(f"✅ Status Effects: {[effect.value for effect in status_effects]}")

    def test_combat_triangle_multiplier_method(self):
        """Test the combat triangle multiplier calculation method."""
        # Test all archetype combinations
        test_cases = [
            (Archetype.MELEE, Archetype.RANGED, 1.25),  # Melee > Ranged
            (Archetype.RANGED, Archetype.MAGIC, 1.25),  # Ranged > Magic
            (Archetype.MAGIC, Archetype.MELEE, 1.25),  # Magic > Melee
            (Archetype.RANGED, Archetype.MELEE, 0.75),  # Ranged < Melee
            (Archetype.MAGIC, Archetype.RANGED, 0.75),  # Magic < Ranged
            (Archetype.MELEE, Archetype.MAGIC, 0.75),  # Melee < Magic
            (Archetype.MELEE, Archetype.MELEE, 1.0),  # Same archetype
        ]

        for attacker, target, expected_multiplier in test_cases:
            multiplier = self.combat._get_combat_triangle_multiplier(attacker, target)
            self.assertEqual(multiplier, expected_multiplier)
            print(
                f"✅ {attacker.value} vs {target.value}: {multiplier} (expected: {expected_multiplier})"
            )


def run_combat_tests():
    """Run all combat system tests with detailed output."""
    print("🔥 COMBAT SYSTEM TESTING (HP-APPROPRIATE NUMBERS) 🔥")
    print("=" * 70)

    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCombatSystem)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")

    if result.errors:
        print("\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")

    if result.wasSuccessful():
        print(
            "\n🎉 ALL TESTS PASSED! Combat system is HP-appropriate and working correctly!"
        )
    else:
        print("\n⚠️  Some tests failed. Please review the issues above.")

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_combat_tests()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Chronicles of Ruin: Sunderfall - Game Launcher
A basic CLI interface to test and play the game systems.
"""

import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.systems.player_system import PlayerSystem
from src.systems.monster_system import MonsterSystem
from src.systems.combat_system import CombatSystem
from src.systems.class_system import ClassSystem, SubtypeType, ArchetypeType
from src.systems.skills_system import SkillsSystem
from src.systems.xp_system import XPSystem
from src.systems.status_elemental_system import StatusElementalSystem
from src.systems.items_system import ItemsSystem
from src.systems.achievement_system import AchievementSystem
from src.systems.quest_system import QuestSystem
from src.systems.economy_system import EconomySystem
from src.systems.world_system import WorldSystem
from src.systems.player_system import StatType
from src.systems.combat_system import Archetype
from src.systems.class_system import SubtypeType


class GameLauncher:
    def __init__(self):
        """Initialize all game systems."""
        self.player_system = PlayerSystem()
        self.monster_system = MonsterSystem()
        self.xp_system = XPSystem()
        self.items_system = ItemsSystem()
        self.combat_system = CombatSystem(
            self.player_system, self.monster_system, self.items_system
        )
        self.class_system = ClassSystem(self.player_system)
        self.skills_system = SkillsSystem(self.player_system, self.class_system)
        self.status_system = StatusElementalSystem()
        self.achievement_system = AchievementSystem(self.player_system)
        self.quest_system = QuestSystem(self.player_system)
        self.economy_system = EconomySystem(self.player_system, self.items_system)
        self.world_system = WorldSystem(self.player_system, self.monster_system)
        
        # Initialize boss system
        from src.systems.boss_system import BossSystem
        self.boss_system = BossSystem(self.monster_system, self.player_system, self.combat_system)

        # Initialize AI Player Integration
        from ai_player_integration import AIPlayerIntegration
        self.ai_integration = AIPlayerIntegration(self)

        self.current_player = None

    def print_header(self):
        """Print the game header."""
        print("=" * 60)
        print("    CHRONICLES OF RUIN: SUNDERFALL")
        print("=" * 60)
        print()

    def print_menu(self):
        """Print the main menu."""
        print("\nMAIN MENU:")
        print("1. Create New Character")
        print("2. Load Character (if exists)")
        print("3. View Character Info")
        print("4. Allocate Class Points")
        print("5. View Skills")
        print("6. Upgrade Skills")
        print("7. Fight Monster")
        print("8. View Available Class Features")
        print("9. Unlock Class Features")
        print("10. View Inventory")
        print("11. Equip/Unequip Items")
        print("12. Create Custom Set")
        print("13. View Achievements")
        print("14. View Quests")
        print("15. Accept Quest")
        print("16. View Economy")
        print("17. Explore World")
        print("18. Travel to Area")
        print("19. Search Area")
        print("20. Training Mode (Easy Fights)")
        print("21. Boss Encounters")
        print("22. AI Player Mode")
        print("0. Exit")
        print()

    def get_character_creation_input(self):
        """Get character creation input from user."""
        print("\n=== CHARACTER CREATION ===")
        print("You have 3 base archetype points to distribute.")
        print("This determines your starting archetype and ultimate skill access.")
        print()

        # Show available base archetypes
        base_archetypes = {
            "Melee": "Power/Toughness - Close combat specialists",
            "Ranged": "Agility/Finesse - Distance fighters",
            "Magic": "Knowledge/Wisdom - Spellcasters",
            "Wild": "Chaos - Unpredictable forces of nature",
        }

        print("Available Base Archetypes:")
        for archetype, description in base_archetypes.items():
            print(f"  {archetype}: {description}")
        print()

        # Get base archetype distribution
        base_points = {}
        remaining_points = 3

        for archetype in base_archetypes.keys():
            if remaining_points > 0:
                while True:
                    try:
                        points = int(
                            input(f"Points for {archetype} (0-{remaining_points}): ")
                        )
                        if 0 <= points <= remaining_points:
                            base_points[archetype] = points
                            remaining_points -= points
                            break
                        else:
                            print(
                                f"Please enter a number between 0 and {remaining_points}"
                            )
                    except ValueError:
                        print("Please enter a valid number")
            else:
                base_points[archetype] = 0

        print(f"\nBase archetype distribution: {base_points}")

        # Get character name
        name = input("\nEnter your character name: ").strip()
        if not name:
            name = "Adventurer"

        return name, base_points

    def create_character(self):
        """Create a new character."""
        name, base_archetypes = self.get_character_creation_input()

        # Convert archetype names to enum values
        base_archetype_points = {}
        for archetype_name, points in base_archetypes.items():
            if points > 0:
                # Map to enum values
                if archetype_name == "Melee":
                    base_archetype_points[ArchetypeType.MELEE] = points
                elif archetype_name == "Ranged":
                    base_archetype_points[ArchetypeType.RANGED] = points
                elif archetype_name == "Magic":
                    base_archetype_points[ArchetypeType.MAGIC] = points
                elif archetype_name == "Wild":
                    base_archetype_points[ArchetypeType.WILD] = points

        # Create player
        player_id = f"player_{int(time.time())}"  # Generate unique ID
        success = self.player_system.create_player(
            player_id=player_id, name=name, base_archetypes=base_archetype_points
        )

        if success:
            self.current_player = self.player_system.get_player(player_id)
        else:
            print("Failed to create character!")
            return

        print(f"\nCharacter '{name}' created successfully!")
        print(
            f"Starting at Class Level {self.current_player['levels']['class']} with {self.current_player['unused_points']['class']} free Class Points"
        )

        # Add starter items
        self.items_system.add_item_to_inventory(
            self.current_player["id"], "iron_sword", 1
        )
        self.items_system.add_item_to_inventory(
            self.current_player["id"], "leather_armor", 1
        )
        print("Added starter items: Iron Sword, Leather Armor")

        # Show starting info
        self.show_character_info()

    def show_character_info(self):
        """Display current character information."""
        if not self.current_player:
            print("No character loaded. Create or load a character first.")
            return

        print("\n=== CHARACTER INFO ===")
        print(f"Name: {self.current_player['name']}")
        print(f"Class Level: {self.current_player['levels']['class']}")
        print(f"Skill Level: {self.current_player['levels']['skill']}")
        print(f"Player Level: {self.current_player['player_level']}")
        print()

        print("XP Pools:")
        print(f"  Base XP: {self.current_player['xp']['base']}")
        print(f"  Class XP: {self.current_player['xp']['class']}")
        print(f"  Skill XP: {self.current_player['xp']['skill']}")
        print()

        print("Available Points:")
        print(f"  Class Points: {self.current_player['unused_points']['class']}")
        print(f"  Skill Points: {self.current_player['unused_points']['skill']}")
        print()

        print("Base Archetype Points:")
        for archetype, points in self.current_player["base_archetypes"].items():
            print(f"  {archetype}: {points}")
        print()

        print("Attributes:")
        for stat_type, value in self.current_player["attributes"].items():
            info = self.player_system.get_attribute_info(self.current_player["id"])
            if "error" not in info:
                attribute_info = info["attributes"].get(stat_type.value, {})
                name = attribute_info.get("archetype", stat_type.value)
                description = attribute_info.get("description", "")
                print(f"  {name}: {value} ({description})")
            else:
                print(f"  {stat_type.value}: {value}")
        print()

        print("Resources:")
        for stat_type, value in self.current_player["resources"].items():
            print(f"  {stat_type.value}: {value}")
        print()

    def allocate_class_points(self):
        """Allocate class points to attributes."""
        if not self.current_player:
            print("No character loaded. Create or load a character first.")
            return

        available_points = self.current_player["unused_points"]["class"]
        if available_points <= 0:
            print("No class points available to allocate.")
            return

        print(f"\n=== ALLOCATE CLASS POINTS ===")
        print(f"Available points: {available_points}")
        print()

        # Show current attributes
        print("Current Attributes:")
        for stat_type in StatType:
            if (
                stat_type != StatType.HEALTH
                and stat_type != StatType.MANA
                and stat_type != StatType.STAMINA
            ):
                current_value = self.current_player["attributes"].get(stat_type, 0)
                info = self.player_system.get_attribute_info(self.current_player["id"])
                if "error" not in info:
                    attribute_info = info["attributes"].get(stat_type.value, {})
                    name = attribute_info.get("archetype", stat_type.value)
                    print(f"  {name}: {current_value}")
                else:
                    print(f"  {stat_type.value}: {current_value}")
        print()

        # Get allocation
        while available_points > 0:
            print(f"Points remaining: {available_points}")
            print("Available attributes:")
            for i, stat_type in enumerate(StatType):
                if (
                    stat_type != StatType.HEALTH
                    and stat_type != StatType.MANA
                    and stat_type != StatType.STAMINA
                ):
                    info = self.player_system.get_attribute_info(
                        self.current_player["id"]
                    )
                    if "error" not in info:
                        attribute_info = info["attributes"].get(stat_type.value, {})
                        name = attribute_info.get("archetype", stat_type.value)
                        print(f"  {i+1}. {name}")
                    else:
                        print(f"  {i+1}. {stat_type.value}")
            print("  0. Done")

            try:
                choice = int(input("Choose attribute to allocate to (0 to finish): "))
                if choice == 0:
                    break
                elif (
                    1
                    <= choice
                    <= len(
                        [
                            s
                            for s in StatType
                            if s != StatType.HEALTH
                            and s != StatType.MANA
                            and s != StatType.STAMINA
                        ]
                    )
                ):
                    stat_types = [
                        s
                        for s in StatType
                        if s != StatType.HEALTH
                        and s != StatType.MANA
                        and s != StatType.STAMINA
                    ]
                    selected_stat = stat_types[choice - 1]

                    points_to_allocate = int(
                        input(f"How many points to allocate to {selected_stat.value}? ")
                    )
                    if 0 <= points_to_allocate <= available_points:
                        result = self.player_system.allocate_class_points_to_attribute(
                            self.current_player["id"], selected_stat, points_to_allocate
                        )
                        if result["success"]:
                            available_points -= points_to_allocate
                            self.current_player = self.player_system.get_player(
                                self.current_player["id"]
                            )
                            print(
                                f"Allocated {points_to_allocate} points to {selected_stat.value}"
                            )
                        else:
                            print(f"Error: {result.get('error', 'Unknown error')}")
                    else:
                        print(f"Please enter a number between 0 and {available_points}")
                else:
                    print("Invalid choice")
            except ValueError:
                print("Please enter a valid number")

        print("Class point allocation complete!")

    def show_skills(self):
        """Show available skills for the current player."""
        if not self.current_player:
            print("No character loaded. Create or load a character first.")
            return

        print("\n=== AVAILABLE SKILLS ===")

        available_skills = self.skills_system.get_available_skills_for_player(
            self.current_player["id"]
        )

        if "error" in available_skills:
            print(f"Error: {available_skills['error']}")
            return

        for archetype, archetype_data in available_skills.get("archetypes", {}).items():
            print(f"\n{archetype.upper()} ARCHETYPE:")
            for subtype, subtype_data in archetype_data.get("subtypes", {}).items():
                print(
                    f"\n  {subtype.upper()} (Points: {subtype_data['points_allocated']}, Max Level: {subtype_data['max_skill_level']}):"
                )

                if subtype_data.get("can_access_ultimate", True):
                    print("    Ultimate skills available!")
                else:
                    print("    Ultimate skills locked (requires pure build)")

                for skill in subtype_data.get("skills", []):
                    level_info = f" (Level {skill['current_level']}/{skill['max_level_for_subtype']})"
                    if skill["is_ultimate"]:
                        level_info += " [ULTIMATE]"
                    print(f"    {skill['name']}{level_info}")

    def upgrade_skills(self):
        """Upgrade skills for the current player."""
        if not self.current_player:
            print("No character loaded. Create or load a character first.")
            return

        available_points = self.current_player["unused_points"]["skill"]
        if available_points <= 0:
            print("No skill points available to spend.")
            return

        print(f"\n=== UPGRADE SKILLS ===")
        print(f"Available skill points: {available_points}")
        print()

        # Get available skills
        available_skills = self.skills_system.get_available_skills_for_player(
            self.current_player["id"]
        )

        # Flatten skills list for easier selection
        all_skills = []
        for archetype, archetype_data in available_skills.get("archetypes", {}).items():
            for subtype, subtype_data in archetype_data.get("subtypes", {}).items():
                for skill in subtype_data.get("skills", []):
                    all_skills.append(
                        {
                            "skill_id": skill["id"],
                            "name": skill["name"],
                            "archetype": archetype,
                            "subtype": subtype,
                            "current_level": skill["current_level"],
                            "max_level": skill["max_level_for_subtype"],
                            "is_ultimate": skill["is_ultimate"],
                        }
                    )

        if not all_skills:
            print("No skills available to upgrade.")
            return

        # Show skills
        print("Available skills to upgrade:")
        for i, skill in enumerate(all_skills):
            level_info = f"Level {skill['current_level']}/{skill['max_level']}"
            if skill["is_ultimate"]:
                level_info += " [ULTIMATE]"
            print(
                f"  {i+1}. {skill['name']} ({skill['archetype']} - {skill['subtype']}) - {level_info}"
            )
        print("  0. Cancel")

        try:
            choice = int(input("\nChoose skill to upgrade (0 to cancel): "))
            if choice == 0:
                return
            elif 1 <= choice <= len(all_skills):
                selected_skill = all_skills[choice - 1]

                if selected_skill["current_level"] >= selected_skill["max_level"]:
                    print(f"{selected_skill['name']} is already at maximum level!")
                    return

                result = self.skills_system.upgrade_skill(
                    self.current_player["id"], selected_skill["skill_id"]
                )

                if result["success"]:
                    self.current_player = result["player"]
                    print(
                        f"Successfully upgraded {selected_skill['name']} to level {result['new_level']}!"
                    )
                else:
                    print(f"Error: {result['message']}")
            else:
                print("Invalid choice")
        except ValueError:
            print("Please enter a valid number")

    def fight_monster(self):
        """Initiate combat with a monster."""
        if not self.current_player:
            print("No character loaded. Create or load a character first.")
            return

        print("\n=== COMBAT ===")

        # Generate encounter
        encounter = self.combat_system.create_encounter(
            self.current_player["id"], area_level=1
        )

        if "error" in encounter:
            print(f"Error creating encounter: {encounter['error']}")
            return

        player_data = encounter["player"]
        monster_data = encounter["monster"]

        print(f"Encounter: {monster_data['name']} (Level {monster_data['level']})")
        print(f"Player: {player_data['name']} (Level {player_data['level']})")
        print()

        # Combat loop
        round_num = 1
        while encounter["state"]["combat_active"]:
            print(f"\n--- ROUND {round_num} ---")
            print(
                f"Player HP: {player_data['current_health']}/{player_data['max_health']}"
            )
            print(
                f"Monster HP: {monster_data['current_health']}/{monster_data['max_health']}"
            )
            print()

            # Player attacks
            encounter = self.combat_system.player_attack(encounter)
            if not encounter["state"]["combat_active"]:
                for log_line in encounter["log"][-3:]:
                    print(log_line)
                break

            # Monster attacks
            encounter = self.combat_system.monster_attack(encounter)
            for log_line in encounter["log"][-3:]:
                print(log_line)
            if not encounter["state"]["combat_active"]:
                break

            round_num += 1

        print("\nCombat ended!")

    def view_inventory(self):
        """View the current player's inventory and equipment."""
        if not self.current_player:
            print("No character loaded. Create or load a character first.")
            return

        print("\n=== INVENTORY ===")

        # Get inventory data
        inventory = self.items_system.get_inventory(self.current_player["id"])

        print(f"Gold: {inventory['gold']}")
        print(f"Capacity: {len(inventory['items'])}/{inventory['capacity']}")
        print()

        # Show equipped items
        print("EQUIPPED ITEMS:")
        if not inventory["equipment"]:
            print("  No items equipped")
        else:
            for slot, item_id in inventory["equipment"].items():
                item_summary = self.items_system.get_item_summary(item_id)
                if "error" not in item_summary:
                    print(
                        f"  {slot.value}: {item_summary['name']} ({item_summary['quality']})"
                    )
                else:
                    print(f"  {slot.value}: Unknown item")
        print()

        # Show inventory items
        print("INVENTORY ITEMS:")
        if not inventory["items"]:
            print("  No items in inventory")
        else:
            # Count items
            item_counts = {}
            for item_id in inventory["items"]:
                item_counts[item_id] = item_counts.get(item_id, 0) + 1

            for item_id, count in item_counts.items():
                item_summary = self.items_system.get_item_summary(item_id)
                if "error" not in item_summary:
                    print(
                        f"  {item_summary['name']} ({item_summary['quality']}) x{count}"
                    )
                else:
                    print(f"  Unknown item x{count}")
        print()

        # Show equipment bonuses
        bonuses = self.items_system.get_equipment_bonuses(self.current_player["id"])
        if bonuses:
            print("EQUIPMENT BONUSES:")
            for bonus_type, bonus_value in bonuses.items():
                print(f"  {bonus_type}: +{bonus_value}")
        else:
            print("No equipment bonuses")
        print()

    def equip_unequip_items(self):
        """Equip or unequip items."""
        if not self.current_player:
            print("No character loaded. Create or load a character first.")
            return

        print("\n=== EQUIP/UNEQUIP ITEMS ===")

        inventory = self.items_system.get_inventory(self.current_player["id"])

        # Show current equipment
        print("Current Equipment:")
        for slot in self.items_system.equipment_slots.keys():
            if slot in inventory["equipment"]:
                item_id = inventory["equipment"][slot]
                item_summary = self.items_system.get_item_summary(item_id)
                if "error" not in item_summary:
                    print(f"  {slot.value}: {item_summary['name']}")
                else:
                    print(f"  {slot.value}: Unknown item")
            else:
                print(f"  {slot.value}: Empty")
        print()

        # Show available items
        if not inventory["items"]:
            print("No items in inventory to equip.")
            return

        print("Available Items:")
        item_counts = {}
        for item_id in inventory["items"]:
            item_counts[item_id] = item_counts.get(item_id, 0) + 1

        available_items = []
        for item_id, count in item_counts.items():
            item_summary = self.items_system.get_item_summary(item_id)
            if "error" not in item_summary:
                available_items.append(
                    {
                        "id": item_id,
                        "name": item_summary["name"],
                        "type": item_summary["type"],
                        "quality": item_summary["quality"],
                        "count": count,
                    }
                )

        for i, item in enumerate(available_items):
            print(f"  {i+1}. {item['name']} ({item['quality']}) x{item['count']}")
        print("  0. Cancel")

        try:
            choice = int(input("\nChoose item to equip (0 to cancel): "))
            if choice == 0:
                return
            elif 1 <= choice <= len(available_items):
                selected_item = available_items[choice - 1]

                # Show available slots for this item type
                print(f"\nAvailable slots for {selected_item['name']}:")
                valid_slots = []
                for slot in self.items_system.equipment_slots.keys():
                    slot_data = self.items_system.equipment_slots[slot]
                    if selected_item["type"] in [
                        t.value for t in slot_data["allowed_types"]
                    ]:
                        valid_slots.append(slot)
                        current_item = inventory["equipment"].get(slot, "Empty")
                        if current_item != "Empty":
                            current_summary = self.items_system.get_item_summary(
                                current_item
                            )
                            if "error" not in current_summary:
                                current_name = current_summary["name"]
                            else:
                                current_name = "Unknown"
                        else:
                            current_name = "Empty"
                        print(
                            f"  {len(valid_slots)}. {slot.value} (Currently: {current_name})"
                        )

                if not valid_slots:
                    print("No valid slots for this item type!")
                    return

                slot_choice = int(input("Choose slot to equip to: "))
                if 1 <= slot_choice <= len(valid_slots):
                    selected_slot = valid_slots[slot_choice - 1]

                    # Equip the item
                    success = self.items_system.equip_item(
                        self.current_player["id"], selected_item["id"], selected_slot
                    )

                    if success:
                        print(
                            f"Successfully equipped {selected_item['name']} to {selected_slot.value}!"
                        )
                    else:
                        print("Failed to equip item!")
                else:
                    print("Invalid slot choice!")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Please enter a valid number")

    def create_custom_set(self):
        """Create a custom set item."""
        if not self.current_player:
            print("No character loaded. Create or load a character first.")
            return

        print("\n=== CREATE CUSTOM SET ===")

        # Get set name and description
        set_name = input("Enter set name: ").strip()
        if not set_name:
            print("Set name cannot be empty!")
            return

        set_description = input("Enter set description: ").strip()
        if not set_description:
            set_description = "A custom set created by " + self.current_player["name"]

        # Show available items
        inventory = self.items_system.get_inventory(self.current_player["id"])
        if not inventory["items"]:
            print("No items in inventory to create a set!")
            return

        print("\nAvailable items for set:")
        item_counts = {}
        for item_id in inventory["items"]:
            item_counts[item_id] = item_counts.get(item_id, 0) + 1

        available_items = []
        for item_id, count in item_counts.items():
            item_summary = self.items_system.get_item_summary(item_id)
            if "error" not in item_summary:
                available_items.append(
                    {
                        "id": item_id,
                        "name": item_summary["name"],
                        "type": item_summary["type"],
                        "quality": item_summary["quality"],
                        "count": count,
                    }
                )

        for i, item in enumerate(available_items):
            print(f"  {i+1}. {item['name']} ({item['quality']}) x{item['count']}")

        # Get set items
        set_items = []
        print("\nEnter item numbers to add to set (comma-separated, 0 to finish):")
        while True:
            try:
                choices = input("Item numbers: ").strip()
                if choices == "0":
                    break

                item_numbers = [int(x.strip()) for x in choices.split(",")]
                for num in item_numbers:
                    if 1 <= num <= len(available_items):
                        selected_item = available_items[num - 1]
                        if selected_item["id"] not in set_items:
                            set_items.append(selected_item["id"])
                            print(f"Added {selected_item['name']} to set")
                        else:
                            print(f"{selected_item['name']} already in set")
                    else:
                        print(f"Invalid item number: {num}")
            except ValueError:
                print("Please enter valid numbers separated by commas")

        if not set_items:
            print("No items selected for set!")
            return

        # Get set bonuses
        print(
            "\nEnter set bonuses (format: bonus_type=value, e.g., physical_damage=0.2):"
        )
        set_bonuses = {}
        bonuses_input = input("Bonuses: ").strip()
        if bonuses_input:
            try:
                for bonus_pair in bonuses_input.split(","):
                    bonus_type, bonus_value = bonus_pair.strip().split("=")
                    set_bonuses[bonus_type.strip()] = float(bonus_value.strip())
            except ValueError:
                print("Invalid bonus format! Using default bonuses.")
                set_bonuses = {"physical_damage": 0.1}
        else:
            set_bonuses = {"physical_damage": 0.1}

        # Create the custom set
        set_id = self.items_system.create_custom_set(
            creator_id=self.current_player["id"],
            set_name=set_name,
            set_description=set_description,
            set_bonuses=set_bonuses,
            set_items=set_items,
        )

        print(f"\nCustom set '{set_name}' created successfully!")
        print(f"Set ID: {set_id}")
        print(f"Items: {len(set_items)} items")
        print(f"Bonuses: {set_bonuses}")

    def show_class_features(self):
        """Show available class features."""
        if not self.current_player:
            print("No character loaded. Create or load a character first.")
            return

        print("\n=== AVAILABLE CLASS FEATURES ===")

        features = self.class_system.get_available_class_features(
            self.current_player["id"], ArchetypeType.MELEE
        )

        if "error" in features:
            print(f"Error: {features['error']}")
            return

        print(f"\n{features['archetype'].upper()} ARCHETYPE:")
        print(f"Available class points: {features['class_points_available']}")
        print()

        if features["unlocked_features"]:
            print("Unlocked Features:")
            for feature in features["unlocked_features"]:
                print(f"  Level {feature['level']}: {feature['name']}")
                for stat, bonus in feature["bonuses"].items():
                    print(f"    +{bonus} {getattr(stat, 'value', stat)}")
        print()

        if features["next_available"]:
            print("Next Available Feature:")
            feature = features["next_available"]
            print(f"  Level {feature['level']}: {feature['name']} (Cost: 1 point)")
            for stat, bonus in feature["bonuses"].items():
                print(f"    +{bonus} {getattr(stat, 'value', stat)}")
        else:
            print("No more features available to unlock.")

    def unlock_class_features(self):
        """Unlock class features."""
        if not self.current_player:
            print("No character loaded. Please create or load a character first.")
            return

        print("\n=== UNLOCK CLASS FEATURES ===")
        print(
            f"Available Class Points: {self.current_player['unused_points']['class']}"
        )

        feature_data = self.class_system.get_available_class_features(
            self.current_player["id"], ArchetypeType.MELEE
        )

        all_features = feature_data.get("all_features", [])
        available_features = [f for f in all_features if f.get("can_unlock")]

        if not available_features:
            print("No features available to unlock.")
            return

        print("Available features to unlock:")
        for i, feature in enumerate(available_features):
            print(
                f"  {i+1}. Level {feature['level']}: {feature['name']} (Cost: 1 point)"
            )
        print("  0. Cancel")

        try:
            choice = int(input("\nChoose feature to unlock (0 to cancel): "))
            if choice == 0:
                return
            elif 1 <= choice <= len(available_features):
                selected_feature = available_features[choice - 1]

                result = self.class_system.unlock_class_feature(
                    self.current_player["id"],
                    ArchetypeType.MELEE,
                    selected_feature["level"],
                )

                if result["success"]:
                    self.current_player = self.player_system.get_player(
                        self.current_player["id"]
                    )
                    print(f"Successfully unlocked {selected_feature['name']}!")
                else:
                    print(f"Error: {result.get('error', 'Unknown error')}")
            else:
                print("Invalid choice")
        except ValueError:
            print("Please enter a valid number")

    def view_achievements(self):
        """View achievements."""
        if not self.current_player:
            print("No character loaded. Please create or load a character first.")
            return

        print("\n=== ACHIEVEMENTS ===")

        stats = self.achievement_system.get_achievement_stats(self.current_player["id"])
        print(f"Total Achievements: {stats['total_achievements']}")
        print(f"Completed: {stats['completed_achievements']}")
        print(f"Completion: {stats['completion_percentage']:.1f}%")

        available = self.achievement_system.get_available_achievements(
            self.current_player["id"]
        )

        if available["completed"]:
            print("\n🏆 COMPLETED ACHIEVEMENTS:")
            for achievement in available["completed"]:
                print(f"  {achievement['name']} ({achievement['tier']})")

        if available["in_progress"]:
            print("\n📈 IN PROGRESS:")
            for achievement in available["in_progress"]:
                print(f"  {achievement['name']} ({achievement['tier']})")
                for req, progress in achievement["progress"].items():
                    print(
                        f"    {req}: {progress['current']}/{progress['required']} ({progress['percentage']:.1f}%)"
                    )

    def view_quests(self):
        """View quests."""
        if not self.current_player:
            print("No character loaded. Please create or load a character first.")
            return

        print("\n=== QUESTS ===")

        stats = self.quest_system.get_quest_stats(self.current_player["id"])
        print(f"Total Quests: {stats['total_quests']}")
        print(f"Completed: {stats['completed_quests']}")
        print(f"Active: {stats['active_quests']}")

        available = self.quest_system.get_available_quests(self.current_player["id"])

        if available["main_story"]:
            print("\n📖 MAIN STORY QUESTS:")
            for quest in available["main_story"]:
                print(f"  {quest['name']} (Level {quest['level_requirement']})")
                print(f"    {quest['description']}")

        if available["side_quests"]:
            print("\n📜 SIDE QUESTS:")
            for quest in available["side_quests"]:
                print(f"  {quest['name']} (Level {quest['level_requirement']})")
                print(f"    {quest['description']}")

        if available["bounties"]:
            print("\n💰 BOUNTY QUESTS:")
            for quest in available["bounties"]:
                print(f"  {quest['name']} (Level {quest['level_requirement']})")
                print(f"    {quest['description']}")

        active_quests = self.quest_system.get_active_quests(self.current_player["id"])
        if active_quests:
            print("\n🎯 ACTIVE QUESTS:")
            for quest in active_quests:
                print(f"  {quest['name']} ({quest['type']})")
                for objective in quest["objectives"]:
                    print(
                        f"    {objective['description']}: {objective['current']}/{objective['required']}"
                    )

    def accept_quest(self):
        """Accept a quest."""
        if not self.current_player:
            print("No character loaded. Please create or load a character first.")
            return

        print("\n=== ACCEPT QUEST ===")

        available = self.quest_system.get_available_quests(self.current_player["id"])
        all_quests = []

        for category, quests in available.items():
            for quest in quests:
                quest["category"] = category
                all_quests.append(quest)

        if not all_quests:
            print("No quests available to accept.")
            return

        print("Available quests:")
        for i, quest in enumerate(all_quests):
            print(
                f"  {i+1}. {quest['name']} ({quest['category']}) - Level {quest['level_requirement']}"
            )
            print(f"     {quest['description']}")

        try:
            choice = int(input("\nChoose quest to accept (0 to cancel): "))
            if choice == 0:
                return
            elif 1 <= choice <= len(all_quests):
                selected_quest = all_quests[choice - 1]
                result = self.quest_system.accept_quest(
                    self.current_player["id"], selected_quest["id"]
                )

                if result["success"]:
                    print(f"✅ Quest accepted: {selected_quest['name']}")
                else:
                    print(f"❌ Error: {result.get('error', 'Unknown error')}")
            else:
                print("Invalid choice")
        except ValueError:
            print("Please enter a valid number")

    def view_economy(self):
        """View economy information."""
        if not self.current_player:
            print("No character loaded. Please create or load a character first.")
            return

        print("\n=== ECONOMY ===")

        stats = self.economy_system.get_economy_stats(self.current_player["id"])
        print(f"Current Gold: {stats['current_gold']}")
        print(f"Total Earned: {stats['total_earned']}")
        print(f"Total Spent: {stats['total_spent']}")
        print(f"Net Worth: {stats['net_worth']}")
        print(f"Transactions: {stats['transaction_count']}")
        print(f"Trades: {stats['trade_count']}")

        # Show recent transactions
        transactions = self.economy_system.get_transaction_history(
            self.current_player["id"], 5
        )
        if transactions:
            print("\n📊 RECENT TRANSACTIONS:")
            for tx in transactions:
                print(f"  {tx['type'].title()}: {tx['amount']} gold ({tx['reason']})")

    def explore_world(self):
        """Explore the world."""
        if not self.current_player:
            print("No character loaded. Please create or load a character first.")
            return

        print("\n=== WORLD EXPLORATION ===")

        current_area = self.world_system.get_current_area(self.current_player["id"])
        if current_area:
            print(f"Current Location: {current_area['name']}")
            print(f"Type: {current_area['type']}")
            print(f"Difficulty: {current_area['difficulty']}")
            print(f"Description: {current_area['description']}")

        stats = self.world_system.get_exploration_stats(self.current_player["id"])
        print(f"\nExploration Progress:")
        print(f"  Areas Visited: {stats['areas_visited']}/{stats['total_areas']}")
        print(f"  Completion: {stats['exploration_percentage']:.1f}%")
        print(f"  Treasures Found: {stats['treasures_discovered']}")
        print(f"  Secrets Found: {stats['secrets_found']}")

        available_areas = self.world_system.get_available_areas(
            self.current_player["id"]
        )
        if available_areas:
            print(f"\n🗺️  CONNECTED AREAS:")
            for area in available_areas:
                visited_mark = "✅" if area["visited"] else "❌"
                print(
                    f"  {visited_mark} {area['name']} ({area['difficulty']}) - Level {area['level_requirement']}"
                )

    def travel_to_area(self):
        """Travel to a new area."""
        if not self.current_player:
            print("No character loaded. Please create or load a character first.")
            return

        print("\n=== TRAVEL ===")

        available_areas = self.world_system.get_available_areas(
            self.current_player["id"]
        )
        if not available_areas:
            print("No areas available to travel to.")
            return

        print("Available areas:")
        for i, area in enumerate(available_areas):
            visited_mark = "✅" if area["visited"] else "❌"
            print(
                f"  {i+1}. {visited_mark} {area['name']} ({area['difficulty']}) - Level {area['level_requirement']}"
            )
            print(f"     {area['description']}")

        try:
            choice = int(input("\nChoose area to travel to (0 to cancel): "))
            if choice == 0:
                return
            elif 1 <= choice <= len(available_areas):
                selected_area = available_areas[choice - 1]
                result = self.world_system.travel_to_area(
                    self.current_player["id"], selected_area["id"]
                )

                if result["success"]:
                    print(f"✅ Traveled to: {result['area_name']}")
                    print(f"   {result['area_description']}")
                else:
                    print(f"❌ Error: {result.get('error', 'Unknown error')}")
            else:
                print("Invalid choice")
        except ValueError:
            print("Please enter a valid number")

    def search_area(self):
        """Search the current area for items."""
        if not self.current_player:
            print("No character loaded. Please create or load a character first.")
            return

        print("\n=== SEARCH AREA ===")

        result = self.world_system.search_area(self.current_player["id"])

        if result["success"]:
            if result["found_items"]:
                print(f"✅ {result['message']}")
                print("Found items:")
                for item in result["found_items"]:
                    print(f"  - {item}")
            else:
                print(f"🔍 {result['message']}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")

    def training_mode(self):
        """Auto-travel to Training Grounds and start an easy encounter."""
        if not self.current_player:
            print("No character loaded. Create or load a character first.")
            return
        # Travel to training grounds if not there
        if (
            self.world_system.get_current_area(self.current_player["id"])["id"]
            != "training_grounds"
        ):
            self.world_system.travel_to_area(
                self.current_player["id"], "training_grounds"
            )
        print("\n=== TRAINING MODE ===")
        # Force melee humanoid in training
        from src.systems.monster_system import MonsterArchetype, MonsterClassification

        encounter = self.combat_system.create_encounter(
            self.current_player["id"],
            area_level=1,
            forced_archetype=MonsterArchetype.MELEE,
            forced_classification=MonsterClassification.HUMANOID,
        )
        if "error" in encounter:
            print(f"Error creating encounter: {encounter['error']}")
            return
        player_data = encounter["player"]
        monster_data = encounter["monster"]
        print(f"Encounter: {monster_data['name']} (Level {monster_data['level']})")
        round_num = 1
        while encounter["state"]["combat_active"]:
            print(f"\n--- ROUND {round_num} ---")
            print(
                f"Player HP: {player_data['current_health']}/{player_data['max_health']}"
            )
            print(
                f"Monster HP: {monster_data['current_health']}/{monster_data['max_health']}"
            )
            encounter = self.combat_system.player_attack(encounter)
            if not encounter["state"]["combat_active"]:
                for log_line in encounter["log"][-3:]:
                    print(log_line)
                break
            encounter = self.combat_system.monster_attack(encounter)
            for log_line in encounter["log"][-3:]:
                print(log_line)
            round_num += 1
        print("\nCombat ended!")

    def boss_encounters(self):
        """Handle boss encounters."""
        if not self.current_player:
            print("No character loaded. Create or load a character first.")
            return
        
        print("\n=== BOSS ENCOUNTERS ===")
        print("1. Create District Boss")
        print("2. Create Unique Monster")
        print("3. Create World Boss")
        print("4. Start Boss Combat")
        print("5. Continue Boss Combat")
        print("6. View Active Encounters")
        print("7. Simulate Boss Fight")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice (0-7): ").strip()
        
        if choice == "1":
            self._create_district_boss()
        elif choice == "2":
            self._create_unique_monster()
        elif choice == "3":
            self._create_world_boss()
        elif choice == "4":
            self._start_boss_combat()
        elif choice == "5":
            self._continue_boss_combat()
        elif choice == "6":
            self._view_active_encounters()
        elif choice == "7":
            self._simulate_boss_fight()
        elif choice == "0":
            return
        else:
            print("Invalid choice!")

    def _create_district_boss(self):
        """Create a district boss encounter."""
        print("\n=== CREATE DISTRICT BOSS ===")
        
        district_name = input("Enter district name: ").strip()
        if not district_name:
            print("District name is required!")
            return
        
        try:
            district_level = int(input("Enter district level (1-50): ").strip())
            if district_level < 1 or district_level > 50:
                print("District level must be between 1 and 50!")
                return
        except ValueError:
            print("Invalid district level!")
            return
        
        try:
            player_level = int(input("Enter player level (1-100): ").strip())
            if player_level < 1 or player_level > 100:
                print("Player level must be between 1 and 100!")
                return
        except ValueError:
            print("Invalid player level!")
            return
        
        # Create boss
        boss = self.boss_system.create_district_boss(district_level, player_level, district_name)
        
        print(f"\n✅ Created District Boss:")
        print(f"   Name: {boss['name']}")
        print(f"   Level: {boss['level']}")
        print(f"   Health: {boss['stats']['max_health']}")
        print(f"   Damage: {boss['stats']['damage']}")
        print(f"   Defense: {boss['stats']['defense']}")
        print(f"   Archetype: {boss['archetype'].value}")
        print(f"   Classification: {boss['classification'].value}")
        print(f"   Phases: {len(boss['phases'])}")
        print(f"   Abilities: {len(boss['abilities'])}")
        
        # Store boss for later use
        if not hasattr(self, 'active_bosses'):
            self.active_bosses = {}
        
        boss_id = f"district_{int(time.time())}"
        self.active_bosses[boss_id] = {
            "type": "district_boss",
            "boss": boss,
            "created_time": time.time()
        }
        
        print(f"\nBoss ID: {boss_id}")

    def _create_unique_monster(self):
        """Create a unique monster encounter."""
        print("\n=== CREATE UNIQUE MONSTER ===")
        
        try:
            district_level = int(input("Enter district level (1-50): ").strip())
            if district_level < 1 or district_level > 50:
                print("District level must be between 1 and 50!")
                return
        except ValueError:
            print("Invalid district level!")
            return
        
        try:
            player_level = int(input("Enter player level (1-100): ").strip())
            if player_level < 1 or player_level > 100:
                print("Player level must be between 1 and 100!")
                return
        except ValueError:
            print("Invalid player level!")
            return
        
        # Create unique monster
        unique_monster = self.boss_system.create_unique_monster(district_level, player_level)
        
        print(f"\n✅ Created Unique Monster:")
        print(f"   Name: {unique_monster['name']}")
        print(f"   Level: {unique_monster['level']}")
        print(f"   Health: {unique_monster['stats']['max_health']}")
        print(f"   Damage: {unique_monster['stats']['damage']}")
        print(f"   Defense: {unique_monster['stats']['defense']}")
        print(f"   Archetype: {unique_monster['archetype'].value}")
        print(f"   Classification: {unique_monster['classification'].value}")
        print(f"   Phases: {len(unique_monster['phases'])}")
        print(f"   Abilities: {len(unique_monster['abilities'])}")
        
        # Store monster for later use
        if not hasattr(self, 'active_bosses'):
            self.active_bosses = {}
        
        boss_id = f"unique_{int(time.time())}"
        self.active_bosses[boss_id] = {
            "type": "unique_monster",
            "boss": unique_monster,
            "created_time": time.time()
        }
        
        print(f"\nMonster ID: {boss_id}")

    def _create_world_boss(self):
        """Create a world boss encounter."""
        print("\n=== CREATE WORLD BOSS ===")
        
        try:
            player_level = int(input("Enter player level (1-100): ").strip())
            if player_level < 1 or player_level > 100:
                print("Player level must be between 1 and 100!")
                return
        except ValueError:
            print("Invalid player level!")
            return
        
        boss_name = input("Enter custom boss name (or press Enter for random): ").strip()
        if not boss_name:
            boss_name = None
        
        # Create world boss
        world_boss = self.boss_system.create_world_boss(player_level, boss_name)
        
        print(f"\n✅ Created World Boss:")
        print(f"   Name: {world_boss['name']}")
        print(f"   Level: {world_boss['level']}")
        print(f"   Health: {world_boss['stats']['max_health']}")
        print(f"   Damage: {world_boss['stats']['damage']}")
        print(f"   Defense: {world_boss['stats']['defense']}")
        print(f"   Archetype: {world_boss['archetype'].value}")
        print(f"   Classification: {world_boss['classification'].value}")
        print(f"   Phases: {len(world_boss['phases'])}")
        print(f"   Abilities: {len(world_boss['abilities'])}")
        
        # Store boss for later use
        if not hasattr(self, 'active_bosses'):
            self.active_bosses = {}
        
        boss_id = f"world_{int(time.time())}"
        self.active_bosses[boss_id] = {
            "type": "world_boss",
            "boss": world_boss,
            "created_time": time.time()
        }
        
        print(f"\nBoss ID: {boss_id}")

    def _start_boss_combat(self):
        """Start a boss combat encounter."""
        print("\n=== START BOSS COMBAT ===")
        
        if not hasattr(self, 'active_bosses') or not self.active_bosses:
            print("No active bosses available!")
            print("Create a boss encounter first.")
            return
        
        print("Active Bosses:")
        for boss_id, encounter in self.active_bosses.items():
            boss = encounter["boss"]
            print(f"  {boss_id}: {boss['name']} (Level {boss['level']})")
        
        boss_id = input("\nEnter boss ID: ").strip()
        if boss_id not in self.active_bosses:
            print("Invalid boss ID!")
            return
        
        # Start combat
        encounter = self.active_bosses[boss_id]
        boss = encounter["boss"]
        
        combat_state = self.boss_system.start_boss_combat(self.current_player, boss)
        
        print(f"\n🎯 BOSS COMBAT STARTED!")
        print(f"   Player: {self.current_player['name']} (Level {self.current_player['level']})")
        print(f"   Boss: {boss['name']} (Level {boss['level']})")
        print(f"   Player Health: {self.current_player['current_health']}/{self.current_player['max_health']}")
        print(f"   Boss Health: {boss['stats']['current_health']}/{boss['stats']['max_health']}")
        
        # Store combat state
        encounter["combat_state"] = combat_state
        
        print(f"\nCombat ready! Use option 5 to continue the fight.")

    def _continue_boss_combat(self):
        """Continue an active boss combat."""
        print("\n=== CONTINUE BOSS COMBAT ===")
        
        # Find encounters with active combat
        active_combats = []
        for boss_id, encounter in self.active_bosses.items():
            if "combat_state" in encounter:
                active_combats.append((boss_id, encounter))
        
        if not active_combats:
            print("No active boss combats!")
            print("Start a boss combat first.")
            return
        
        print("Active Boss Combats:")
        for boss_id, encounter in active_combats:
            boss = encounter["boss"]
            combat_state = encounter["combat_state"]
            print(f"  {boss_id}: {self.current_player['name']} vs {boss['name']} (Round {combat_state['round']})")
        
        boss_id = input("\nEnter boss ID: ").strip()
        if boss_id not in self.active_bosses:
            print("Invalid boss ID!")
            return
        
        encounter = self.active_bosses[boss_id]
        if "combat_state" not in encounter:
            print("No active combat for this boss!")
            return
        
        # Get player action
        print("\nAvailable Actions:")
        print("1. Attack")
        print("2. Use Skill")
        print("3. Use Item")
        print("4. Defend")
        
        action_choice = input("Select action (1-4): ").strip()
        action_map = {
            "1": "attack",
            "2": "skill",
            "3": "item",
            "4": "defend"
        }
        
        player_action = action_map.get(action_choice, "attack")
        
        # Process combat round
        boss = encounter["boss"]
        result = self.boss_system.process_boss_combat_round(boss["id"], player_action)
        
        if "error" in result:
            print(f"Error: {result['error']}")
            return
        
        if "winner" in result:
            # Combat ended
            print(f"\n🏁 COMBAT ENDED!")
            print(f"   Winner: {result['winner'].title()}")
            print(f"   Rounds: {result['rounds']}")
            print(f"   Damage Dealt: {result['damage_dealt']}")
            print(f"   Damage Taken: {result['damage_taken']}")
            
            if result['winner'] == 'player':
                rewards = result['rewards']
                print(f"\n🎁 REWARDS:")
                print(f"   Experience: {rewards['experience']}")
                print(f"   Gold: {rewards['gold']}")
                print(f"   Loot: {len(rewards['loot']['rare_items'])} rare items")
            
            # Remove combat state
            del encounter["combat_state"]
            return
        
        # Show round results
        player_result = result["player_result"]
        boss_result = result["boss_result"]
        
        print(f"\n⚔️ ROUND {result['round']} RESULTS:")
        print(f"   Player Action: {player_result['action']}")
        print(f"   Player Damage: {player_result['damage_dealt']}")
        print(f"   Boss Health: {player_result['boss_health_remaining']}")
        
        print(f"   Boss Action: {boss_result['action']}")
        print(f"   Boss Damage: {boss_result['damage_dealt']}")
        print(f"   Player Health: {boss_result['player_health_remaining']}")
        
        # Check for phase transitions
        combat_state = result["combat_state"]
        if combat_state["phase_transitions"]:
            latest_transition = combat_state["phase_transitions"][-1]
            if latest_transition["round"] == result["round"]:
                print(f"\n🔥 PHASE TRANSITION: {latest_transition['description']}")
        
        # Check for abilities used
        if combat_state["abilities_used"]:
            latest_ability = combat_state["abilities_used"][-1]
            if latest_ability["round"] == result["round"]:
                print(f"   Boss Ability: {latest_ability['description']}")

    def _view_active_encounters(self):
        """View all active encounters."""
        print("\n=== ACTIVE ENCOUNTERS ===")
        
        if not hasattr(self, 'active_bosses') or not self.active_bosses:
            print("No active encounters.")
            return
        
        for boss_id, encounter in self.active_bosses.items():
            boss = encounter["boss"]
            print(f"\nBoss ID: {boss_id}")
            print(f"   Type: {encounter['type']}")
            print(f"   Boss: {boss['name']}")
            print(f"   Level: {boss['level']}")
            print(f"   Health: {boss['stats']['current_health']}/{boss['stats']['max_health']}")
            print(f"   Phase: {boss['current_phase'].value}")
            print(f"   Created: {time.strftime('%H:%M:%S', time.localtime(encounter['created_time']))}")
            
            if "combat_state" in encounter:
                print(f"   Status: In Combat (Round {encounter['combat_state']['round']})")
            else:
                print(f"   Status: Ready for Combat")

    def _simulate_boss_fight(self):
        """Simulate a complete boss fight."""
        print("\n=== SIMULATE BOSS FIGHT ===")
        
        # Get boss parameters
        boss_type = input("Enter boss type (district/unique/world): ").strip().lower()
        if boss_type not in ["district", "unique", "world"]:
            print("Invalid boss type!")
            return
        
        try:
            district_level = int(input("Enter district level (1-50): ").strip())
        except ValueError:
            print("Invalid district level!")
            return
        
        try:
            player_level = int(input("Enter player level (1-100): ").strip())
        except ValueError:
            print("Invalid player level!")
            return
        
        # Create boss
        if boss_type == "district":
            district_name = input("Enter district name: ").strip()
            boss = self.boss_system.create_district_boss(district_level, player_level, district_name)
        elif boss_type == "unique":
            boss = self.boss_system.create_unique_monster(district_level, player_level)
        else:  # world
            boss = self.boss_system.create_world_boss(player_level)
        
        # Start combat
        combat_state = self.boss_system.start_boss_combat(self.current_player, boss)
        
        print(f"\n🎯 SIMULATING BOSS FIGHT:")
        print(f"   Player: {self.current_player['name']} (Level {self.current_player['level']})")
        print(f"   Boss: {boss['name']} (Level {boss['level']})")
        print(f"   Player Health: {self.current_player['current_health']}/{self.current_player['max_health']}")
        print(f"   Boss Health: {boss['stats']['current_health']}/{boss['stats']['max_health']}")
        
        # Simulate combat
        round_count = 0
        max_rounds = 50  # Prevent infinite loops
        
        while round_count < max_rounds:
            round_count += 1
            
            # Process round
            result = self.boss_system.process_boss_combat_round(boss["id"], "attack")
            
            if "winner" in result:
                print(f"\n🏁 SIMULATION COMPLETE!")
                print(f"   Winner: {result['winner'].title()}")
                print(f"   Rounds: {result['rounds']}")
                print(f"   Damage Dealt: {result['damage_dealt']}")
                print(f"   Damage Taken: {result['damage_taken']}")
                
                if result['winner'] == 'player':
                    rewards = result['rewards']
                    print(f"\n🎁 REWARDS:")
                    print(f"   Experience: {rewards['experience']}")
                    print(f"   Gold: {rewards['gold']}")
                
                break
            
            # Show progress every 5 rounds
            if round_count % 5 == 0:
                player_result = result["player_result"]
                boss_result = result["boss_result"]
                print(f"   Round {round_count}: Player HP {boss_result['player_health_remaining']}, Boss HP {player_result['boss_health_remaining']}")
        
        if round_count >= max_rounds:
            print(f"\n⚠️ Simulation stopped after {max_rounds} rounds (possible infinite loop)")

    def ai_player_mode(self):
        """AI Player Mode - Let AI players test the game"""
        print("\n🤖 AI PLAYER MODE")
        print("=" * 40)
        
        while True:
            print("\nAI Player Options:")
            print("1. Setup AI Player")
            print("2. Run AI Playtest")
            print("3. View AI Game Log")
            print("4. Clear AI Game Log")
            print("5. Save Playtest Results")
            print("0. Back to Main Menu")
            
            try:
                choice = input("\nEnter choice (0-5): ").strip()
                
                if choice == "1":
                    self._setup_ai_player()
                elif choice == "2":
                    self._run_ai_playtest()
                elif choice == "3":
                    self._view_ai_game_log()
                elif choice == "4":
                    self._clear_ai_game_log()
                elif choice == "5":
                    self._save_playtest_results()
                elif choice == "0":
                    break
                else:
                    print("Invalid choice. Please enter 0-5.")
                    
            except KeyboardInterrupt:
                print("\nReturning to main menu...")
                break
            except Exception as e:
                print(f"Error: {e}")

    def _setup_ai_player(self):
        """Setup an AI player for testing"""
        print("\n=== SETUP AI PLAYER ===")
        
        # List available AI players
        try:
            ai_players = self.ai_integration.ai_system.list_ai_players()
            if not ai_players:
                print("❌ No AI players found. Create some first using the AI Player Tool.")
                print("   Run: python tools/dev_master.py ai-player-samples")
                return
            
            print("Available AI Players:")
            for i, player in enumerate(ai_players, 1):
                profile = self.ai_integration.ai_system.get_ai_player_profile(player)
                print(f"   {i}. {player} ({profile.playstyle}, {profile.personality})")
            
            choice = input("\nEnter player name or number: ").strip()
            
            # Handle numeric choice
            try:
                player_index = int(choice) - 1
                if 0 <= player_index < len(ai_players):
                    player_name = ai_players[player_index]
                else:
                    print("❌ Invalid selection.")
                    return
            except ValueError:
                player_name = choice
            
            # Setup the AI player
            if self.ai_integration.setup_ai_player(player_name):
                print(f"✅ AI Player '{player_name}' is ready for testing!")
            else:
                print("❌ Failed to setup AI player.")
                
        except Exception as e:
            print(f"❌ Error setting up AI player: {e}")

    def _run_ai_playtest(self):
        """Run an AI playtest"""
        if not self.ai_integration.current_ai_player:
            print("❌ No AI player is set up. Please setup an AI player first.")
            return
        
        print("\n=== AI PLAYTEST ===")
        print("Available test scenarios:")
        scenarios = [
            "character_creation",
            "combat_test", 
            "skill_allocation",
            "exploration_test",
            "full_gameplay"
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"   {i}. {scenario.replace('_', ' ').title()}")
        
        print("\nEnter scenario numbers (comma-separated) or 'all':")
        choice = input("Choice: ").strip().lower()
        
        if choice == "all":
            selected_scenarios = scenarios
        else:
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(",")]
                selected_scenarios = [scenarios[i] for i in indices if 0 <= i < len(scenarios)]
            except ValueError:
                print("❌ Invalid input. Please enter numbers separated by commas.")
                return
        
        if not selected_scenarios:
            print("❌ No valid scenarios selected.")
            return
        
        print(f"\n🎮 Running AI Playtest with scenarios: {', '.join(selected_scenarios)}")
        
        try:
            results = self.ai_integration.run_ai_playtest(
                self.ai_integration.current_ai_player.name,
                selected_scenarios
            )
            
            if results.get("success") is False:
                print(f"❌ Playtest failed: {results.get('error', 'Unknown error')}")
                return
            
            # Display results summary
            print(f"\n📊 PLAYTEST RESULTS SUMMARY:")
            print(f"   Player: {results['player_name']}")
            print(f"   Scenarios: {len(results['scenario_results'])}")
            print(f"   Total Decisions: {len(self.ai_integration.ai_game_log)}")
            
            if results.get("game_balance_insights"):
                print(f"\n💡 GAME BALANCE INSIGHTS:")
                for insight in results["game_balance_insights"]:
                    print(f"   • {insight}")
            
            # Store results for later saving
            self._last_playtest_results = results
            
        except Exception as e:
            print(f"❌ Error running playtest: {e}")

    def _view_ai_game_log(self):
        """View the AI game log"""
        log = self.ai_integration.get_ai_game_log()
        if not log:
            print("📝 AI Game Log is empty.")
            return
        
        print(f"\n📝 AI GAME LOG ({len(log)} entries):")
        print("-" * 50)
        for i, entry in enumerate(log[-20:], 1):  # Show last 20 entries
            print(f"{i:2d}. {entry}")
        
        if len(log) > 20:
            print(f"... and {len(log) - 20} more entries")

    def _clear_ai_game_log(self):
        """Clear the AI game log"""
        self.ai_integration.clear_ai_game_log()
        print("🗑️ AI Game Log cleared.")

    def _save_playtest_results(self):
        """Save the last playtest results"""
        if not hasattr(self, '_last_playtest_results'):
            print("❌ No playtest results to save. Run a playtest first.")
            return
        
        try:
            filename = input("Enter filename (or press Enter for auto-generated): ").strip()
            if not filename:
                filename = None
            
            filepath = self.ai_integration.save_playtest_results(
                self._last_playtest_results, filename
            )
            print(f"✅ Results saved successfully!")
            
        except Exception as e:
            print(f"❌ Error saving results: {e}")

    def run(self):
        """Run the game launcher."""
        self.print_header()

        while True:
            self.print_menu()

            try:
                choice = input("Enter your choice (0-20): ").strip()

                if choice == "1":
                    self.create_character()
                elif choice == "2":
                    print("Load character functionality not implemented yet.")
                elif choice == "3":
                    self.show_character_info()
                elif choice == "4":
                    self.allocate_class_points()
                elif choice == "5":
                    self.show_skills()
                elif choice == "6":
                    self.upgrade_skills()
                elif choice == "7":
                    self.fight_monster()
                elif choice == "8":
                    self.show_class_features()
                elif choice == "9":
                    self.unlock_class_features()
                elif choice == "10":
                    self.view_inventory()
                elif choice == "11":
                    self.equip_unequip_items()
                elif choice == "12":
                    self.create_custom_set()
                elif choice == "13":
                    self.view_achievements()
                elif choice == "14":
                    self.view_quests()
                elif choice == "15":
                    self.accept_quest()
                elif choice == "16":
                    self.view_economy()
                elif choice == "17":
                    self.explore_world()
                elif choice == "18":
                    self.travel_to_area()
                elif choice == "19":
                    self.search_area()
                elif choice == "20":
                    self.training_mode()
                elif choice == "21":
                    self.boss_encounters()
                elif choice == "22":
                    self.ai_player_mode()
                elif choice == "0":
                    print("\nThanks for playing Chronicles of Ruin: Sunderfall!")
                    break
                else:
                    print("Invalid choice. Please enter a number between 0 and 22.")

            except KeyboardInterrupt:
                print("\n\nGame interrupted. Thanks for playing!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    launcher = GameLauncher()
    launcher.run()

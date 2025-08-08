#!/usr/bin/env python3
"""
Simple Image Generator for Chronicles of Ruin
Lightweight image generation for monsters and character portraits
"""

import os
import sys
import json
import requests
import base64
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
import argparse
import time
import logging
from enum import Enum
from PIL import Image, ImageDraw, ImageFont
import random

# Add the tools directory to the path
sys.path.append(str(Path(__file__).parent))

class ImageType(Enum):
    """Types of images to generate"""
    MONSTER = "monster"
    CHARACTER = "character"
    LANDSCAPE = "landscape"
    ITEM = "item"

@dataclass
class ImageConfig:
    """Configuration for image generation"""
    prompt: str
    image_type: ImageType
    style: str = "fantasy"
    size: str = "512x512"
    quality: str = "medium"

@dataclass
class GeneratedImage:
    """Represents a generated image"""
    filename: str
    prompt: str
    image_type: str
    style: str
    generation_time: float
    file_size: int
    metadata: Dict[str, Any]

class SimpleImageGenerator:
    """Simple image generator using external APIs"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.output_dir = self.base_dir / "generated_images"
        self.config_file = self.base_dir / "image_generator_config.json"
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.base_dir / "image_generator.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        default_config = {
            "use_local_generation": True,
            "api_fallback": "https://api.replicate.com/v1/predictions",
            "default_style": "fantasy",
            "default_size": "512x512",
            "save_metadata": True,
            "auto_save_history": True
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    default_config.update(config)
            except Exception as e:
                self.logger.warning(f"Failed to load config: {e}")
        
        return default_config
    
    def generate_monster_image(self, monster_type: str, level: int = 1, 
                             attributes: Dict[str, Any] = None) -> Optional[GeneratedImage]:
        """Generate a monster image based on type and attributes"""
        
        # Build monster prompt
        base_prompts = {
            "goblin": "goblin warrior, green skin, sharp teeth, leather armor, fantasy creature",
            "orc": "orc berserker, muscular, tusks, battle scars, intimidating, fantasy",
            "troll": "troll monster, large, grey skin, regeneration, fantasy creature",
            "dragon": "dragon, scales, wings, fire breath, fantasy monster",
            "skeleton": "skeleton warrior, undead, bones, dark magic, fantasy",
            "zombie": "zombie, undead, rotting flesh, slow movement, horror fantasy",
            "ghost": "ghost, ethereal, transparent, haunting, fantasy spirit",
            "demon": "demon, horns, red skin, evil, dark fantasy creature",
            "golem": "stone golem, construct, magical, fantasy guardian",
            "wyvern": "wyvern, dragon-like, two legs, wings, fantasy beast"
        }
        
        base_prompt = base_prompts.get(monster_type.lower(), f"{monster_type} monster, fantasy creature")
        
        # Add level-based modifiers
        if level > 10:
            base_prompt += ", powerful, elite, detailed armor"
        elif level > 5:
            base_prompt += ", experienced, battle-worn"
        
        # Add attribute modifiers
        if attributes:
            if attributes.get("fire"):
                base_prompt += ", fire elemental, flames"
            if attributes.get("ice"):
                base_prompt += ", ice elemental, frost"
            if attributes.get("poison"):
                base_prompt += ", toxic, poison dripping"
            if attributes.get("undead"):
                base_prompt += ", undead, necromantic"
        
        config = ImageConfig(
            prompt=base_prompt,
            image_type=ImageType.MONSTER,
            style="dark_fantasy"
        )
        
        return self.generate_image(config)
    
    def generate_character_portrait(self, character_data: Dict[str, Any]) -> Optional[GeneratedImage]:
        """Generate a character portrait based on equipment and stats"""
        
        # Build character prompt
        race = character_data.get("race", "human")
        class_type = character_data.get("class", "warrior")
        equipment = character_data.get("equipment", {})
        
        base_prompt = f"{race} {class_type}, fantasy character portrait"
        
        # Add equipment details
        if equipment.get("weapon"):
            base_prompt += f", wielding {equipment['weapon']}"
        if equipment.get("armor"):
            base_prompt += f", wearing {equipment['armor']}"
        if equipment.get("helmet"):
            base_prompt += f", {equipment['helmet']} helmet"
        if equipment.get("shield"):
            base_prompt += ", with shield"
        
        # Add class-specific details
        class_details = {
            "warrior": "muscular, battle-scarred, determined expression",
            "mage": "mystical aura, glowing eyes, magical robes",
            "rogue": "stealthy, agile, leather armor, hooded",
            "cleric": "holy symbol, divine aura, priestly robes",
            "ranger": "wilderness gear, bow, nature connection"
        }
        
        base_prompt += f", {class_details.get(class_type, 'adventurer')}"
        
        config = ImageConfig(
            prompt=base_prompt,
            image_type=ImageType.CHARACTER,
            style="fantasy_portrait"
        )
        
        return self.generate_image(config)
    
    def generate_image(self, config: ImageConfig) -> Optional[GeneratedImage]:
        """Generate an image using the configured method"""
        start_time = time.time()
        
        try:
            if self.config.get("use_local_generation", True):
                return self._generate_local_image(config, start_time)
            else:
                return self._generate_api_image(config)
        except Exception as e:
            self.logger.error(f"Image generation failed: {e}")
            return None
    
    def _generate_local_image(self, config: ImageConfig, start_time: float) -> Optional[GeneratedImage]:
        """Generate a simple image using PIL"""
        timestamp = int(time.time())
        filename = f"gen_{config.image_type.value}_{timestamp}.png"
        filepath = self.output_dir / filename
        
        # Create image based on type
        if config.image_type == ImageType.MONSTER:
            image = self._create_monster_image(config.prompt, config.style)
        elif config.image_type == ImageType.CHARACTER:
            image = self._create_character_image(config.prompt, config.style)
        else:
            image = self._create_generic_image(config.prompt, config.style)
        
        # Save the image
        image.save(filepath, "PNG")
        
        metadata = {
            "prompt": config.prompt,
            "image_type": config.image_type.value,
            "style": config.style,
            "generation_time": time.time() - start_time,
            "timestamp": timestamp,
            "method": "local_pil",
            "size": f"{image.width}x{image.height}"
        }
        
        return GeneratedImage(
            filename=filename,
            prompt=config.prompt,
            image_type=config.image_type.value,
            style=config.style,
            generation_time=time.time() - start_time,
            file_size=filepath.stat().st_size,
            metadata=metadata
        )
    
    def _create_monster_image(self, prompt: str, style: str) -> Image.Image:
        """Create a monster image based on prompt"""
        # Create a 512x512 image
        width, height = 512, 512
        image = Image.new('RGB', (width, height), color='#2a2a2a')  # Dark background
        draw = ImageDraw.Draw(image)
        
        # Parse monster type from prompt
        monster_type = self._extract_monster_type(prompt)
        
        # Create monster silhouette
        self._draw_monster_silhouette(draw, monster_type, width, height)
        
        # Add text overlay
        self._add_text_overlay(draw, prompt, width, height)
        
        return image
    
    def _create_character_image(self, prompt: str, style: str) -> Image.Image:
        """Create a character portrait based on prompt"""
        # Create a 512x512 image
        width, height = 512, 512
        image = Image.new('RGB', (width, height), color='#4a4a6a')  # Blue-ish background
        draw = ImageDraw.Draw(image)
        
        # Parse character details from prompt
        character_info = self._extract_character_info(prompt)
        
        # Create character silhouette
        self._draw_character_silhouette(draw, character_info, width, height)
        
        # Add text overlay
        self._add_text_overlay(draw, prompt, width, height)
        
        return image
    
    def _create_generic_image(self, prompt: str, style: str) -> Image.Image:
        """Create a generic image based on prompt"""
        # Create a 512x512 image
        width, height = 512, 512
        image = Image.new('RGB', (width, height), color='#3a3a3a')  # Gray background
        draw = ImageDraw.Draw(image)
        
        # Create abstract pattern based on prompt
        self._draw_abstract_pattern(draw, prompt, width, height)
        
        # Add text overlay
        self._add_text_overlay(draw, prompt, width, height)
        
        return image
    
    def _extract_monster_type(self, prompt: str) -> str:
        """Extract monster type from prompt"""
        monster_types = ['goblin', 'orc', 'troll', 'dragon', 'skeleton', 'zombie', 'ghost', 'demon', 'golem', 'wyvern']
        prompt_lower = prompt.lower()
        for monster_type in monster_types:
            if monster_type in prompt_lower:
                return monster_type
        return 'monster'
    
    def _extract_character_info(self, prompt: str) -> Dict[str, str]:
        """Extract character information from prompt"""
        info = {'race': 'human', 'class': 'warrior'}
        prompt_lower = prompt.lower()
        
        races = ['human', 'elf', 'dwarf', 'orc', 'halfling']
        classes = ['warrior', 'mage', 'rogue', 'cleric', 'ranger']
        
        for race in races:
            if race in prompt_lower:
                info['race'] = race
                break
        
        for class_type in classes:
            if class_type in prompt_lower:
                info['class'] = class_type
                break
        
        return info
    
    def _draw_monster_silhouette(self, draw: ImageDraw.Draw, monster_type: str, width: int, height: int):
        """Draw monster silhouette based on type"""
        colors = {
            'goblin': '#4a7c59',      # Green
            'orc': '#8b4513',          # Brown
            'troll': '#696969',        # Gray
            'dragon': '#8b0000',       # Dark red
            'skeleton': '#f5f5dc',     # Beige
            'zombie': '#556b2f',       # Dark olive
            'ghost': '#e6e6fa',        # Lavender
            'demon': '#8b0000',        # Dark red
            'golem': '#708090',        # Slate gray
            'wyvern': '#2f4f4f'        # Dark slate
        }
        
        color = colors.get(monster_type, '#8b4513')
        
        # Draw monster body (simplified shapes)
        if monster_type == 'dragon':
            # Dragon with wings
            self._draw_dragon(draw, color, width, height)
        elif monster_type == 'skeleton':
            # Skeleton with bones
            self._draw_skeleton(draw, color, width, height)
        elif monster_type == 'ghost':
            # Ethereal ghost
            self._draw_ghost(draw, color, width, height)
        else:
            # Generic monster shape
            self._draw_generic_monster(draw, color, width, height)
    
    def _draw_character_silhouette(self, draw: ImageDraw.Draw, character_info: Dict[str, str], width: int, height: int):
        """Draw character silhouette based on class"""
        colors = {
            'warrior': '#8b4513',      # Brown
            'mage': '#4b0082',         # Purple
            'rogue': '#2f4f4f',        # Dark slate
            'cleric': '#ffd700',       # Gold
            'ranger': '#228b22'        # Forest green
        }
        
        color = colors.get(character_info['class'], '#8b4513')
        
        # Draw character based on class
        if character_info['class'] == 'mage':
            self._draw_mage(draw, color, width, height)
        elif character_info['class'] == 'warrior':
            self._draw_warrior(draw, color, width, height)
        elif character_info['class'] == 'rogue':
            self._draw_rogue(draw, color, width, height)
        else:
            self._draw_generic_character(draw, color, width, height)
    
    def _draw_abstract_pattern(self, draw: ImageDraw.Draw, prompt: str, width: int, height: int):
        """Draw abstract pattern based on prompt"""
        # Create random geometric patterns
        for _ in range(10):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            draw.line([(x1, y1), (x2, y2)], fill=color, width=3)
    
    def _draw_dragon(self, draw: ImageDraw.Draw, color: str, width: int, height: int):
        """Draw dragon silhouette"""
        # Dragon body
        body_points = [(width//2, height//2), (width//2-50, height//2+100), (width//2+50, height//2+100)]
        draw.polygon(body_points, fill=color)
        
        # Wings
        wing_points = [(width//2-80, height//2-50), (width//2-120, height//2-100), (width//2-60, height//2-80)]
        draw.polygon(wing_points, fill=color)
        
        wing_points2 = [(width//2+80, height//2-50), (width//2+120, height//2-100), (width//2+60, height//2-80)]
        draw.polygon(wing_points2, fill=color)
    
    def _draw_skeleton(self, draw: ImageDraw.Draw, color: str, width: int, height: int):
        """Draw skeleton silhouette"""
        # Head
        draw.ellipse([width//2-30, height//2-80, width//2+30, height//2-20], fill=color)
        
        # Body
        draw.rectangle([width//2-20, height//2-20, width//2+20, height//2+60], fill=color)
        
        # Arms
        draw.line([(width//2-20, height//2), (width//2-60, height//2-20)], fill=color, width=8)
        draw.line([(width//2+20, height//2), (width//2+60, height//2-20)], fill=color, width=8)
        
        # Legs
        draw.line([(width//2-10, height//2+60), (width//2-30, height//2+120)], fill=color, width=8)
        draw.line([(width//2+10, height//2+60), (width//2+30, height//2+120)], fill=color, width=8)
    
    def _draw_ghost(self, draw: ImageDraw.Draw, color: str, width: int, height: int):
        """Draw ghost silhouette"""
        # Ghostly form
        points = [(width//2, height//2-100), (width//2-40, height//2-20), (width//2-30, height//2+60),
                 (width//2, height//2+80), (width//2+30, height//2+60), (width//2+40, height//2-20)]
        draw.polygon(points, fill=color)
        
        # Eyes
        draw.ellipse([width//2-15, height//2-70, width//2-5, height//2-60], fill='white')
        draw.ellipse([width//2+5, height//2-70, width//2+15, height//2-60], fill='white')
    
    def _draw_generic_monster(self, draw: ImageDraw.Draw, color: str, width: int, height: int):
        """Draw generic monster silhouette"""
        # Body
        draw.ellipse([width//2-60, height//2-40, width//2+60, height//2+80], fill=color)
        
        # Head
        draw.ellipse([width//2-40, height//2-80, width//2+40, height//2-20], fill=color)
        
        # Eyes
        draw.ellipse([width//2-20, height//2-60, width//2-10, height//2-50], fill='red')
        draw.ellipse([width//2+10, height//2-60, width//2+20, height//2-50], fill='red')
    
    def _draw_mage(self, draw: ImageDraw.Draw, color: str, width: int, height: int):
        """Draw mage silhouette"""
        # Robe
        draw.rectangle([width//2-40, height//2-20, width//2+40, height//2+80], fill=color)
        
        # Head
        draw.ellipse([width//2-25, height//2-60, width//2+25, height//2-20], fill='#f4a460')
        
        # Staff
        draw.line([(width//2+50, height//2-40), (width//2+50, height//2+60)], fill='#8b4513', width=5)
        
        # Magic aura
        for i in range(5):
            x = width//2 + random.randint(-30, 30)
            y = height//2 + random.randint(-30, 30)
            draw.ellipse([x-5, y-5, x+5, y+5], fill='yellow')
    
    def _draw_warrior(self, draw: ImageDraw.Draw, color: str, width: int, height: int):
        """Draw warrior silhouette"""
        # Armor
        draw.rectangle([width//2-35, height//2-20, width//2+35, height//2+80], fill=color)
        
        # Head
        draw.ellipse([width//2-20, height//2-50, width//2+20, height//2-20], fill='#f4a460')
        
        # Helmet
        draw.arc([width//2-25, height//2-60, width//2+25, height//2-30], 0, 180, fill=color, width=8)
        
        # Sword
        draw.line([(width//2-60, height//2), (width//2-60, height//2+40)], fill='silver', width=8)
    
    def _draw_rogue(self, draw: ImageDraw.Draw, color: str, width: int, height: int):
        """Draw rogue silhouette"""
        # Leather armor
        draw.rectangle([width//2-30, height//2-20, width//2+30, height//2+70], fill=color)
        
        # Head with hood
        draw.ellipse([width//2-20, height//2-50, width//2+20, height//2-20], fill='#f4a460')
        draw.arc([width//2-25, height//2-60, width//2+25, height//2-30], 0, 180, fill=color, width=10)
        
        # Daggers
        draw.line([(width//2-50, height//2+10), (width//2-50, height//2+50)], fill='silver', width=4)
        draw.line([(width//2+50, height//2+10), (width//2+50, height//2+50)], fill='silver', width=4)
    
    def _draw_generic_character(self, draw: ImageDraw.Draw, color: str, width: int, height: int):
        """Draw generic character silhouette"""
        # Body
        draw.rectangle([width//2-25, height//2-20, width//2+25, height//2+60], fill=color)
        
        # Head
        draw.ellipse([width//2-20, height//2-50, width//2+20, height//2-20], fill='#f4a460')
        
        # Arms
        draw.line([(width//2-25, height//2), (width//2-50, height//2+20)], fill=color, width=8)
        draw.line([(width//2+25, height//2), (width//2+50, height//2+20)], fill=color, width=8)
    
    def _add_text_overlay(self, draw: ImageDraw.Draw, prompt: str, width: int, height: int):
        """Add text overlay to image"""
        try:
            # Try to use a default font
            font = ImageFont.load_default()
        except:
            font = None
        
        # Add semi-transparent overlay
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 100))
        draw_overlay = ImageDraw.Draw(overlay)
        
        # Add text
        text = prompt[:50] + "..." if len(prompt) > 50 else prompt
        bbox = draw_overlay.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = height - text_height - 20
        
        draw_overlay.text((x, y), text, fill='white', font=font)
        
        # Composite overlay onto main image
        # For now, just add text directly
        draw.text((x, y), text, fill='white', font=font)
    
    def _generate_api_image(self, config: ImageConfig) -> Optional[GeneratedImage]:
        """Generate image using external API (placeholder)"""
        # This would integrate with services like Replicate, Hugging Face, etc.
        # For now, return None to use local generation
        return None
    
    def list_generated_images(self) -> List[Dict[str, Any]]:
        """List all generated images"""
        images = []
        for file in self.output_dir.glob("*.*"):
            if file.suffix in ['.txt', '.png', '.jpg']:
                images.append({
                    "filename": file.name,
                    "filepath": str(file),
                    "size": file.stat().st_size,
                    "created": file.stat().st_ctime
                })
        
        return sorted(images, key=lambda x: x['created'], reverse=True)

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Simple Image Generator for Chronicles of Ruin")
    parser.add_argument("command", choices=["monster", "character", "generate", "list"])
    parser.add_argument("--type", help="Monster type (goblin, orc, dragon, etc.)")
    parser.add_argument("--level", type=int, default=1, help="Monster level")
    parser.add_argument("--race", help="Character race")
    parser.add_argument("--class", dest="class_type", help="Character class")
    parser.add_argument("--equipment", help="Equipment JSON string")
    parser.add_argument("--prompt", help="Custom generation prompt")
    
    args = parser.parse_args()
    
    # Initialize generator
    base_dir = Path.cwd()
    generator = SimpleImageGenerator(base_dir)
    
    if args.command == "monster":
        if not args.type:
            print("Error: --type is required for monster generation")
            return
        
        result = generator.generate_monster_image(args.type, args.level)
        if result:
            print(f"SUCCESS: Generated monster image: {result.filename}")
            print(f"  Type: {args.type}")
            print(f"  Level: {args.level}")
            print(f"  Time: {result.generation_time:.2f}s")
        else:
            print("ERROR: Monster generation failed")
    
    elif args.command == "character":
        character_data = {
            "race": args.race or "human",
            "class": args.class_type or "warrior",
            "equipment": {}
        }
        
        if args.equipment:
            try:
                character_data["equipment"] = json.loads(args.equipment)
            except:
                print("Warning: Invalid equipment JSON, using defaults")
        
        result = generator.generate_character_portrait(character_data)
        if result:
            print(f"SUCCESS: Generated character portrait: {result.filename}")
            print(f"  Race: {character_data['race']}")
            print(f"  Class: {character_data['class']}")
            print(f"  Time: {result.generation_time:.2f}s")
        else:
            print("ERROR: Character generation failed")
    
    elif args.command == "generate":
        if not args.prompt:
            print("Error: --prompt is required for generation")
            return
        
        config = ImageConfig(
            prompt=args.prompt,
            image_type=ImageType.MONSTER
        )
        
        result = generator.generate_image(config)
        if result:
            print(f"SUCCESS: Generated image: {result.filename}")
            print(f"  Prompt: {args.prompt}")
            print(f"  Time: {result.generation_time:.2f}s")
        else:
            print("ERROR: Generation failed")
    
    elif args.command == "list":
        images = generator.list_generated_images()
        if images:
            print(f"Generated images ({len(images)} total):")
            for img in images[:10]:  # Show last 10
                print(f"  {img['filename']} ({img['size']} bytes)")
        else:
            print("No generated images found")

if __name__ == "__main__":
    main()

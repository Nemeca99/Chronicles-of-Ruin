#!/usr/bin/env python3
"""
Stable Diffusion Tool for Chronicles of Ruin
Generates images for Discord integration and game assets
"""

import os
import sys
import json
import subprocess
import requests
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any
import argparse
import time
import logging

# Add the tools directory to the path
sys.path.append(str(Path(__file__).parent))

@dataclass
class SDConfig:
    """Configuration for Stable Diffusion generation"""
    prompt: str
    negative_prompt: str = ""
    width: int = 512
    height: int = 512
    steps: int = 20
    cfg_scale: float = 7.0
    seed: Optional[int] = None
    sampler: str = "Euler a"
    model: str = "stable-diffusion-v1-5"
    output_dir: str = "generated_images"
    
@dataclass
class GeneratedImage:
    """Represents a generated image"""
    filename: str
    prompt: str
    negative_prompt: str
    seed: int
    cfg_scale: float
    steps: int
    model: str
    generation_time: float
    file_size: int
    metadata: Dict[str, Any]

class StableDiffusionTool:
    """Tool for generating images using Stable Diffusion"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.output_dir = self.base_dir / "generated_images"
        self.config_file = self.base_dir / "sd_config.json"
        self.history_file = self.base_dir / "sd_history.json"
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.base_dir / "sd_generation.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        default_config = {
            "api_url": "http://127.0.0.1:7860",
            "default_model": "stable-diffusion-v1-5",
            "default_sampler": "Euler a",
            "default_steps": 20,
            "default_cfg_scale": 7.0,
            "default_width": 512,
            "default_height": 512,
            "max_batch_size": 4,
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
    
    def _save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
    
    def _load_history(self) -> List[Dict[str, Any]]:
        """Load generation history"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Failed to load history: {e}")
        return []
    
    def _save_history(self, history: List[Dict[str, Any]]):
        """Save generation history"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save history: {e}")
    
    def check_api_connection(self) -> bool:
        """Check if Stable Diffusion API is available"""
        try:
            response = requests.get(f"{self.config['api_url']}/sdapi/v1/sd-models", timeout=5)
            return response.status_code == 200
        except Exception as e:
            self.logger.error(f"API connection failed: {e}")
            return False
    
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        try:
            response = requests.get(f"{self.config['api_url']}/sdapi/v1/sd-models")
            if response.status_code == 200:
                models = response.json()
                return [model['title'] for model in models]
        except Exception as e:
            self.logger.error(f"Failed to get models: {e}")
        return []
    
    def generate_image(self, config: SDConfig) -> Optional[GeneratedImage]:
        """Generate a single image using Stable Diffusion"""
        start_time = time.time()
        
        # Prepare payload
        payload = {
            "prompt": config.prompt,
            "negative_prompt": config.negative_prompt,
            "width": config.width,
            "height": config.height,
            "steps": config.steps,
            "cfg_scale": config.cfg_scale,
            "sampler_name": config.sampler,
            "restore_faces": False,
            "tiling": False,
            "enable_hr": False,
            "denoising_strength": 0.7,
            "firstphase_width": 0,
            "firstphase_height": 0,
            "hr_scale": 2.0,
            "hr_upscaler": "Latent",
            "hr_second_pass_steps": 20,
            "hr_resize_x": 0,
            "hr_resize_y": 0,
            "hr_sampler_name": "Euler a",
            "hr_prompt": "",
            "hr_negative_prompt": "",
            "override_settings": {},
            "override_settings_restore_after": True,
            "script_args": [],
            "sampler_index": "Euler a",
            "send_images": True,
            "save_images": False,
            "alwayson_scripts": {}
        }
        
        if config.seed is not None:
            payload["seed"] = config.seed
        
        try:
            # Generate image
            response = requests.post(
                f"{self.config['api_url']}/sdapi/v1/txt2img",
                json=payload,
                timeout=300
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Save image
                import base64
                from PIL import Image
                import io
                
                image_data = base64.b64decode(result['images'][0])
                image = Image.open(io.BytesIO(image_data))
                
                # Generate filename
                timestamp = int(time.time())
                seed = result.get('info', {}).get('seed', config.seed or timestamp)
                filename = f"sd_gen_{timestamp}_{seed}.png"
                filepath = self.output_dir / filename
                
                # Save image
                image.save(filepath)
                
                # Create metadata
                metadata = {
                    "prompt": config.prompt,
                    "negative_prompt": config.negative_prompt,
                    "seed": seed,
                    "cfg_scale": config.cfg_scale,
                    "steps": config.steps,
                    "sampler": config.sampler,
                    "model": config.model,
                    "width": config.width,
                    "height": config.height,
                    "generation_time": time.time() - start_time,
                    "timestamp": timestamp
                }
                
                # Save metadata if enabled
                if self.config.get('save_metadata', True):
                    metadata_file = filepath.with_suffix('.json')
                    with open(metadata_file, 'w') as f:
                        json.dump(metadata, f, indent=2)
                
                # Update history
                if self.config.get('auto_save_history', True):
                    history = self._load_history()
                    history.append({
                        "filename": filename,
                        "metadata": metadata,
                        "filepath": str(filepath)
                    })
                    self._save_history(history)
                
                return GeneratedImage(
                    filename=filename,
                    prompt=config.prompt,
                    negative_prompt=config.negative_prompt,
                    seed=seed,
                    cfg_scale=config.cfg_scale,
                    steps=config.steps,
                    model=config.model,
                    generation_time=time.time() - start_time,
                    file_size=filepath.stat().st_size,
                    metadata=metadata
                )
            else:
                self.logger.error(f"Generation failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            self.logger.error(f"Generation error: {e}")
            return None
    
    def generate_batch(self, configs: List[SDConfig]) -> List[Optional[GeneratedImage]]:
        """Generate multiple images"""
        results = []
        for i, config in enumerate(configs):
            self.logger.info(f"Generating image {i+1}/{len(configs)}: {config.prompt[:50]}...")
            result = self.generate_image(config)
            results.append(result)
            if result:
                self.logger.info(f"Generated: {result.filename}")
            else:
                self.logger.error(f"Failed to generate image {i+1}")
        return results
    
    def generate_for_discord(self, prompt: str, style: str = "dark_fantasy") -> Optional[GeneratedImage]:
        """Generate an image optimized for Discord"""
        
        # Style-specific prompts
        style_prompts = {
            "dark_fantasy": {
                "base": "dark fantasy, atmospheric, detailed, high quality, 4k",
                "negative": "bright, cheerful, cartoon, anime, low quality, blurry"
            },
            "game_asset": {
                "base": "game asset, clean design, professional, high quality, 4k",
                "negative": "text, watermark, blurry, low quality"
            },
            "character_portrait": {
                "base": "character portrait, detailed face, fantasy, high quality, 4k",
                "negative": "full body, blurry, low quality, distorted"
            },
            "landscape": {
                "base": "fantasy landscape, atmospheric, detailed, high quality, 4k",
                "negative": "people, buildings, blurry, low quality"
            }
        }
        
        style_config = style_prompts.get(style, style_prompts["dark_fantasy"])
        
        config = SDConfig(
            prompt=f"{prompt}, {style_config['base']}",
            negative_prompt=style_config['negative'],
            width=512,
            height=512,
            steps=25,
            cfg_scale=7.5,
            sampler="Euler a"
        )
        
        return self.generate_image(config)
    
    def list_generated_images(self) -> List[Dict[str, Any]]:
        """List all generated images with metadata"""
        images = []
        for file in self.output_dir.glob("*.png"):
            metadata_file = file.with_suffix('.json')
            metadata = {}
            
            if metadata_file.exists():
                try:
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                except Exception as e:
                    self.logger.warning(f"Failed to load metadata for {file}: {e}")
            
            images.append({
                "filename": file.name,
                "filepath": str(file),
                "size": file.stat().st_size,
                "created": file.stat().st_ctime,
                "metadata": metadata
            })
        
        return sorted(images, key=lambda x: x['created'], reverse=True)
    
    def cleanup_old_images(self, days: int = 30):
        """Clean up images older than specified days"""
        import time
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        
        cleaned = 0
        for file in self.output_dir.glob("*.png"):
            if file.stat().st_ctime < cutoff_time:
                try:
                    file.unlink()
                    metadata_file = file.with_suffix('.json')
                    if metadata_file.exists():
                        metadata_file.unlink()
                    cleaned += 1
                except Exception as e:
                    self.logger.error(f"Failed to delete {file}: {e}")
        
        self.logger.info(f"Cleaned up {cleaned} old images")
        return cleaned

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Stable Diffusion Tool for Chronicles of Ruin")
    parser.add_argument("command", choices=[
        "generate", "batch", "discord", "list", "cleanup", "check", "models"
    ])
    parser.add_argument("--prompt", "-p", help="Image generation prompt")
    parser.add_argument("--negative", "-n", help="Negative prompt")
    parser.add_argument("--width", "-w", type=int, default=512, help="Image width")
    parser.add_argument("--height", type=int, default=512, help="Image height")
    parser.add_argument("--steps", "-s", type=int, default=20, help="Generation steps")
    parser.add_argument("--cfg-scale", "-c", type=float, default=7.0, help="CFG scale")
    parser.add_argument("--seed", type=int, help="Random seed")
    parser.add_argument("--sampler", default="Euler a", help="Sampler method")
    parser.add_argument("--model", default="stable-diffusion-v1-5", help="Model name")
    parser.add_argument("--style", choices=["dark_fantasy", "game_asset", "character_portrait", "landscape"], 
                       default="dark_fantasy", help="Style for Discord generation")
    parser.add_argument("--days", type=int, default=30, help="Days for cleanup")
    parser.add_argument("--config-file", help="Path to config file")
    
    args = parser.parse_args()
    
    # Initialize tool
    base_dir = Path.cwd()
    sd_tool = StableDiffusionTool(base_dir)
    
    if args.command == "check":
        if sd_tool.check_api_connection():
            print("SUCCESS: Stable Diffusion API is available")
        else:
            print("ERROR: Stable Diffusion API is not available")
            print("Make sure the SD WebUI is running on http://127.0.0.1:7860")
    
    elif args.command == "models":
        models = sd_tool.get_available_models()
        if models:
            print("Available models:")
            for model in models:
                print(f"  - {model}")
        else:
            print("No models available or API not connected")
    
    elif args.command == "generate":
        if not args.prompt:
            print("Error: --prompt is required for generation")
            return
        
        config = SDConfig(
            prompt=args.prompt,
            negative_prompt=args.negative or "",
            width=args.width,
            height=args.height,
            steps=args.steps,
            cfg_scale=args.cfg_scale,
            seed=args.seed,
            sampler=args.sampler,
            model=args.model
        )
        
        result = sd_tool.generate_image(config)
        if result:
            print(f"✓ Generated: {result.filename}")
            print(f"  Seed: {result.seed}")
            print(f"  Time: {result.generation_time:.2f}s")
        else:
            print("✗ Generation failed")
    
    elif args.command == "discord":
        if not args.prompt:
            print("Error: --prompt is required for Discord generation")
            return
        
        result = sd_tool.generate_for_discord(args.prompt, args.style)
        if result:
            print(f"✓ Generated Discord image: {result.filename}")
            print(f"  Style: {args.style}")
            print(f"  Seed: {result.seed}")
        else:
            print("✗ Discord generation failed")
    
    elif args.command == "list":
        images = sd_tool.list_generated_images()
        if images:
            print(f"Generated images ({len(images)} total):")
            for img in images[:10]:  # Show last 10
                print(f"  {img['filename']} ({img['size']} bytes)")
        else:
            print("No generated images found")
    
    elif args.command == "cleanup":
        cleaned = sd_tool.cleanup_old_images(args.days)
        print(f"Cleaned up {cleaned} images older than {args.days} days")
    
    elif args.command == "batch":
        if not args.prompt:
            print("Error: --prompt is required for batch generation")
            return
        
        # Generate multiple variations
        configs = []
        for i in range(4):  # Generate 4 variations
            config = SDConfig(
                prompt=args.prompt,
                negative_prompt=args.negative or "",
                width=args.width,
                height=args.height,
                steps=args.steps,
                cfg_scale=args.cfg_scale,
                seed=args.seed + i if args.seed else None,
                sampler=args.sampler,
                model=args.model
            )
            configs.append(config)
        
        results = sd_tool.generate_batch(configs)
        successful = sum(1 for r in results if r is not None)
        print(f"Generated {successful}/{len(configs)} images successfully")

if __name__ == "__main__":
    main()

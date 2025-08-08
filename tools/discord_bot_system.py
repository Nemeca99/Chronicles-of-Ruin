#!/usr/bin/env python3
"""
Discord Bot System for Chronicles of Ruin
Handles game commands (!) and LLM interactions (@)
"""

import os
import sys
import json
import asyncio
import discord
from discord.ext import commands
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any, Union
import argparse
import time
import logging
from enum import Enum

# Add the tools directory to the path
sys.path.append(str(Path(__file__).parent))

# Import our existing systems
from npc_ai_system import NPCAISystem, InteractionType
from simple_image_generator import SimpleImageGenerator, ImageConfig

class CommandType(Enum):
    """Types of Discord commands"""
    GAME = "game"      # ! commands
    LLM = "llm"        # @ commands

@dataclass
class BotConfig:
    """Discord bot configuration"""
    token: str
    prefix: str = "!"
    llm_prefix: str = "@"
    game_channel_id: Optional[int] = None
    llm_channel_id: Optional[int] = None
    admin_role_id: Optional[int] = None
    enable_npc_ai: bool = True
    enable_stable_diffusion: bool = True
    max_response_length: int = 2000
    cooldown_seconds: int = 3

class ChroniclesDiscordBot(commands.Bot):
    """Discord bot for Chronicles of Ruin saga"""
    
    def __init__(self, config: BotConfig):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix=config.prefix,
            intents=intents,
            help_command=None
        )
        
        self.config = config
        self.base_dir = Path.cwd()
        
        # Initialize systems
        self.npc_system = NPCAISystem(self.base_dir) if config.enable_npc_ai else None
        self.image_generator = SimpleImageGenerator(self.base_dir) if config.enable_stable_diffusion else None
        
        # Game state
        self.game_state = {}
        self.player_data = {}
        self.active_sessions = {}
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.base_dir / "discord_bot.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Register events
        self.setup_events()
        # Register commands
        self.setup_commands()
    
    def setup_events(self):
        """Setup bot events"""
        
        @self.event
        async def on_ready():
            self.logger.info(f"Bot logged in as {self.user}")
            await self.change_presence(activity=discord.Game(name="Chronicles of Ruin"))
        
        @self.event
        async def on_message(message):
            # Ignore bot messages
            if message.author == self.user:
                return
            
            # Handle @ commands for LLM interactions
            if message.content.startswith(self.config.llm_prefix):
                await self.handle_llm_command(message)
                return
            
            # Process regular commands
            await self.process_commands(message)
    
    def setup_commands(self):
        """Setup game commands (!)"""
        
        @self.command(name="start")
        async def start_game(ctx):
            """Start a new game session"""
            if not self._check_channel(ctx, CommandType.GAME):
                return
            
            player_id = str(ctx.author.id)
            if player_id in self.active_sessions:
                await ctx.send("You already have an active game session!")
                return
            
            # Initialize player data
            self.player_data[player_id] = {
                "name": ctx.author.display_name,
                "level": 1,
                "health": 100,
                "location": "Sunderfall Village",
                "inventory": [],
                "quests": [],
                "created_at": time.time()
            }
            
            self.active_sessions[player_id] = {
                "started_at": time.time(),
                "last_activity": time.time()
            }
            
            embed = discord.Embed(
                title="🎮 Chronicles of Ruin - Game Started",
                description=f"Welcome to the saga, {ctx.author.display_name}!",
                color=discord.Color.green()
            )
            embed.add_field(name="Location", value="Sunderfall Village", inline=True)
            embed.add_field(name="Level", value="1", inline=True)
            embed.add_field(name="Health", value="100/100", inline=True)
            embed.add_field(name="Commands", value="Use `!help` to see available commands", inline=False)
            
            await ctx.send(embed=embed)
        
        @self.command(name="status")
        async def player_status(ctx):
            """Show player status"""
            if not self._check_channel(ctx, CommandType.GAME):
                return
            
            player_id = str(ctx.author.id)
            if player_id not in self.player_data:
                await ctx.send("You need to start a game first! Use `!start`")
                return
            
            player = self.player_data[player_id]
            embed = discord.Embed(
                title=f"📊 {ctx.author.display_name}'s Status",
                color=discord.Color.blue()
            )
            embed.add_field(name="Level", value=str(player["level"]), inline=True)
            embed.add_field(name="Health", value=f"{player['health']}/100", inline=True)
            embed.add_field(name="Location", value=player["location"], inline=True)
            embed.add_field(name="Inventory", value=f"{len(player['inventory'])} items", inline=True)
            embed.add_field(name="Active Quests", value=str(len(player["quests"])), inline=True)
            
            await ctx.send(embed=embed)
        
        @self.command(name="move")
        async def move_location(ctx, location: str):
            """Move to a new location"""
            if not self._check_channel(ctx, CommandType.GAME):
                return
            
            player_id = str(ctx.author.id)
            if player_id not in self.player_data:
                await ctx.send("You need to start a game first! Use `!start`")
                return
            
            # Update player location
            self.player_data[player_id]["location"] = location
            self.active_sessions[player_id]["last_activity"] = time.time()
            
            embed = discord.Embed(
                title="🚶 Movement",
                description=f"You have moved to **{location}**",
                color=discord.Color.green()
            )
            
            await ctx.send(embed=embed)
        
        @self.command(name="inventory")
        async def show_inventory(ctx):
            """Show player inventory"""
            if not self._check_channel(ctx, CommandType.GAME):
                return
            
            player_id = str(ctx.author.id)
            if player_id not in self.player_data:
                await ctx.send("You need to start a game first! Use `!start`")
                return
            
            player = self.player_data[player_id]
            embed = discord.Embed(
                title=f"🎒 {ctx.author.display_name}'s Inventory",
                color=discord.Color.gold()
            )
            
            if player["inventory"]:
                for item in player["inventory"]:
                    embed.add_field(name=item["name"], value=item["description"], inline=True)
            else:
                embed.description = "Your inventory is empty."
            
            await ctx.send(embed=embed)
        
        @self.command(name="quests")
        async def show_quests(ctx):
            """Show active quests"""
            if not self._check_channel(ctx, CommandType.GAME):
                return
            
            player_id = str(ctx.author.id)
            if player_id not in self.player_data:
                await ctx.send("You need to start a game first! Use `!start`")
                return
            
            player = self.player_data[player_id]
            embed = discord.Embed(
                title=f"📜 {ctx.author.display_name}'s Quests",
                color=discord.Color.purple()
            )
            
            if player["quests"]:
                for quest in player["quests"]:
                    embed.add_field(name=quest["name"], value=quest["description"], inline=False)
            else:
                embed.description = "No active quests."
            
            await ctx.send(embed=embed)
        
        @self.command(name="help")
        async def show_help(ctx):
            """Show available commands"""
            embed = discord.Embed(
                title="🎮 Chronicles of Ruin - Commands",
                description="Available game commands:",
                color=discord.Color.blue()
            )
            
            game_commands = [
                ("!start", "Start a new game session"),
                ("!status", "Show your player status"),
                ("!move <location>", "Move to a new location"),
                ("!inventory", "Show your inventory"),
                ("!quests", "Show active quests"),
                ("!help", "Show this help message")
            ]
            
            for cmd, desc in game_commands:
                embed.add_field(name=cmd, value=desc, inline=False)
            
            embed.add_field(
                name="LLM Commands",
                value=f"Use `{self.config.llm_prefix}` to interact with NPCs and AI",
                inline=False
            )
            
            await ctx.send(embed=embed)
    
    async def handle_llm_command(self, message):
        """Handle @ commands for LLM interactions"""
        if not self._check_channel(message, CommandType.LLM):
            return
        
        content = message.content[len(self.config.llm_prefix):].strip()
        if not content:
            await message.channel.send("Please provide a message after @")
            return
        
        # Check for cooldown
        if not self._check_cooldown(message.author.id):
            await message.channel.send("Please wait a moment before making another request.")
            return
        
        # Show typing indicator
        async with message.channel.typing():
            try:
                # Check if it's an NPC interaction
                if content.startswith("talk to "):
                    await self._handle_npc_interaction(message, content)
                elif content.startswith("generate "):
                    await self._handle_image_generation(message, content)
                else:
                    await self._handle_general_llm(message, content)
                    
            except Exception as e:
                self.logger.error(f"Error handling LLM command: {e}")
                await message.channel.send("Sorry, I encountered an error. Please try again.")
    
    async def _handle_npc_interaction(self, message, content):
        """Handle NPC conversation"""
        if not self.npc_system:
            await message.channel.send("NPC AI system is not available.")
            return
        
        # Parse: "talk to <npc_name> <message>"
        parts = content.split(" ", 3)
        if len(parts) < 3:
            await message.channel.send("Usage: @talk to <npc_name> <message>")
            return
        
        npc_name = parts[2]
        player_message = parts[3] if len(parts) > 3 else "Hello"
        
        # Get player context
        player_id = str(message.author.id)
        player_context = self.player_data.get(player_id, {})
        
        # Interact with NPC
        response = self.npc_system.interact_with_npc(
            npc_name=npc_name,
            player_message=player_message,
            context={
                "player": player_context,
                "location": player_context.get("location", "unknown"),
                "game_state": self.game_state
            }
        )
        
        # Create response embed
        embed = discord.Embed(
            title=f"💬 {npc_name}",
            description=response.text,
            color=discord.Color.green()
        )
        embed.set_footer(text=f"Emotion: {response.emotion}")
        
        await message.channel.send(embed=embed)
    
    async def _handle_image_generation(self, message, content):
        """Handle image generation"""
        if not self.image_generator:
            await message.channel.send("Image generation system is not available.")
            return
        
        # Parse: "generate <prompt>"
        prompt = content[len("generate "):].strip()
        if not prompt:
            await message.channel.send("Usage: @generate <prompt>")
            return
        
        # Generate image
        config = ImageConfig(prompt=prompt, image_type="custom")
        result = self.image_generator.generate_image(config)
        
        if result:
            # Save image and send
            image_path = self.base_dir / "generated_images" / result.filename
            if image_path.exists():
                file = discord.File(str(image_path), filename=result.filename)
                embed = discord.Embed(
                    title="🎨 Generated Image",
                    description=f"Prompt: {prompt}",
                    color=discord.Color.purple()
                )
                embed.add_field(name="Type", value=result.image_type, inline=True)
                embed.add_field(name="Time", value=f"{result.generation_time:.2f}s", inline=True)
                
                await message.channel.send(file=file, embed=embed)
            else:
                await message.channel.send("Image generation completed but file not found.")
        else:
            await message.channel.send("Failed to generate image. Please try again.")
    
    async def _handle_general_llm(self, message, content):
        """Handle general LLM interactions"""
        # For now, redirect to a default NPC
        if self.npc_system:
            response = self.npc_system.interact_with_npc(
                npc_name="Sage",
                player_message=content,
                context={
                    "player": {"name": message.author.display_name},
                    "location": "Discord",
                    "game_state": {}
                }
            )
            
            embed = discord.Embed(
                title="🤖 AI Response",
                description=response.text,
                color=discord.Color.blue()
            )
            
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("LLM system is not available.")
    
    def _check_channel(self, ctx_or_message, command_type: CommandType) -> bool:
        """Check if command is in the correct channel"""
        if command_type == CommandType.GAME:
            if self.config.game_channel_id and ctx_or_message.channel.id != self.config.game_channel_id:
                return False
        elif command_type == CommandType.LLM:
            if self.config.llm_channel_id and ctx_or_message.channel.id != self.config.llm_channel_id:
                return False
        return True
    
    def _check_cooldown(self, user_id: int) -> bool:
        """Check if user is on cooldown"""
        current_time = time.time()
        if hasattr(self, '_cooldowns'):
            if user_id in self._cooldowns:
                if current_time - self._cooldowns[user_id] < self.config.cooldown_seconds:
                    return False
        
        if not hasattr(self, '_cooldowns'):
            self._cooldowns = {}
        self._cooldowns[user_id] = current_time
        return True

def load_config(config_file: Path) -> BotConfig:
    """Load bot configuration from file"""
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                data = json.load(f)
                return BotConfig(**data)
        except Exception as e:
            print(f"Failed to load config: {e}")
    
    # Return default config
    return BotConfig(
        token="YOUR_BOT_TOKEN_HERE",
        prefix="!",
        llm_prefix="@",
        enable_npc_ai=True,
        enable_stable_diffusion=True
    )

def save_config(config: BotConfig, config_file: Path):
    """Save bot configuration to file"""
    try:
        with open(config_file, 'w') as f:
            json.dump(asdict(config), f, indent=2)
    except Exception as e:
        print(f"Failed to save config: {e}")

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Discord Bot for Chronicles of Ruin")
    parser.add_argument("command", choices=["run", "setup", "test"])
    parser.add_argument("--config", default="discord_bot_config.json", help="Config file path")
    parser.add_argument("--token", help="Bot token")
    parser.add_argument("--prefix", default="!", help="Game command prefix")
    parser.add_argument("--llm-prefix", default="@", help="LLM command prefix")
    
    args = parser.parse_args()
    
    config_file = Path(args.config)
    
    if args.command == "setup":
        # Setup configuration
        config = BotConfig(
            token=args.token or "YOUR_BOT_TOKEN_HERE",
            prefix=args.prefix,
            llm_prefix=args.llm_prefix,
            enable_npc_ai=True,
            enable_stable_diffusion=True
        )
        
        save_config(config, config_file)
        print(f"SUCCESS: Configuration saved to {config_file}")
        print("Edit the config file to add your bot token and channel IDs")
        
    elif args.command == "run":
        # Run the bot
        config = load_config(config_file)
        
        if config.token == "YOUR_BOT_TOKEN_HERE":
            print("ERROR: Please set your bot token in the config file")
            return
        
        bot = ChroniclesDiscordBot(config)
        
        try:
            bot.run(config.token)
        except Exception as e:
            print(f"ERROR: Failed to start bot: {e}")
    
    elif args.command == "test":
        # Test configuration
        config = load_config(config_file)
        print("Bot Configuration:")
        print(f"  Token: {'*' * len(config.token) if config.token != 'YOUR_BOT_TOKEN_HERE' else 'NOT SET'}")
        print(f"  Game Prefix: {config.prefix}")
        print(f"  LLM Prefix: {config.llm_prefix}")
        print(f"  NPC AI: {'Enabled' if config.enable_npc_ai else 'Disabled'}")
        print(f"  Stable Diffusion: {'Enabled' if config.enable_stable_diffusion else 'Disabled'}")

if __name__ == "__main__":
    main()

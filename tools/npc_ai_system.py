#!/usr/bin/env python3
"""
NPC AI System for Chronicles of Ruin
Dynamic NPC interactions using Ollama with multimodal capabilities
"""

import os
import sys
import json
import requests
import base64
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any, Union
import argparse
import time
import logging
from enum import Enum

# Add the tools directory to the path
sys.path.append(str(Path(__file__).parent))

class InteractionType(Enum):
    """Types of NPC interactions"""
    TEXT_ONLY = "text"
    IMAGE_AND_TEXT = "image_text"
    VOICE_AND_TEXT = "voice_text"
    MULTIMODAL = "multimodal"

@dataclass
class NPCProfile:
    """NPC character profile"""
    name: str
    role: str
    personality: str
    background: str
    location: str
    voice_style: str = "neutral"
    image_prompt: str = ""
    conversation_style: str = "casual"
    knowledge_domains: List[str] = None
    relationship_to_player: str = "neutral"
    
    def __post_init__(self):
        if self.knowledge_domains is None:
            self.knowledge_domains = []

@dataclass
class InteractionContext:
    """Context for NPC interactions"""
    npc_profile: NPCProfile
    player_context: Dict[str, Any]
    conversation_history: List[Dict[str, str]]
    current_location: str
    game_state: Dict[str, Any]
    interaction_type: InteractionType = InteractionType.TEXT_ONLY

@dataclass
class NPCResponse:
    """Response from NPC AI"""
    text: str
    emotion: str = "neutral"
    voice_file: Optional[str] = None
    image_file: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class NPCAISystem:
    """NPC AI system using Ollama for dynamic interactions"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = Path(base_dir)
        self.npcs_dir = self.base_dir / "npcs"
        self.conversations_dir = self.base_dir / "conversations"
        self.voices_dir = self.base_dir / "voices"
        self.images_dir = self.base_dir / "npc_images"
        
        # Create directories
        for dir_path in [self.npcs_dir, self.conversations_dir, self.voices_dir, self.images_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # Initialize logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.base_dir / "npc_ai.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Ollama configuration
        self.ollama_url = "http://localhost:11434"
        self.model_name = "llama3.1:8b"  # Latest Llama 3.1 model
        self.max_tokens = 1000  # Increased for better responses
        self.temperature = 0.7
        
        # Load NPC profiles
        self.npc_profiles = self._load_npc_profiles()
        
    def _load_npc_profiles(self) -> Dict[str, NPCProfile]:
        """Load NPC profiles from files"""
        profiles = {}
        for profile_file in self.npcs_dir.glob("*.json"):
            try:
                with open(profile_file, 'r') as f:
                    data = json.load(f)
                    profiles[data['name']] = NPCProfile(**data)
            except Exception as e:
                self.logger.warning(f"Failed to load NPC profile {profile_file}: {e}")
        return profiles
    
    def _save_npc_profile(self, profile: NPCProfile):
        """Save NPC profile to file"""
        profile_file = self.npcs_dir / f"{profile.name.lower().replace(' ', '_')}.json"
        try:
            with open(profile_file, 'w') as f:
                json.dump(asdict(profile), f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save NPC profile: {e}")
    
    def check_ollama_connection(self) -> bool:
        """Check if Ollama is running and model is available"""
        try:
            # Check if Ollama is running
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code != 200:
                return False
            
            # Check if our model is available
            models = response.json().get('models', [])
            model_names = [model['name'] for model in models]
            return self.model_name in model_names
            
        except Exception as e:
            self.logger.error(f"Ollama connection failed: {e}")
            return False
    
    def create_npc_profile(self, name: str, role: str, personality: str, 
                          background: str, location: str, **kwargs) -> NPCProfile:
        """Create a new NPC profile"""
        profile = NPCProfile(
            name=name,
            role=role,
            personality=personality,
            background=background,
            location=location,
            **kwargs
        )
        
        self.npc_profiles[name] = profile
        self._save_npc_profile(profile)
        self.logger.info(f"Created NPC profile: {name}")
        return profile
    
    def get_npc_profile(self, name: str) -> Optional[NPCProfile]:
        """Get NPC profile by name"""
        return self.npc_profiles.get(name)
    
    def list_npcs(self) -> List[str]:
        """List all available NPCs"""
        return list(self.npc_profiles.keys())
    
    def _build_prompt(self, context: InteractionContext, player_message: str) -> str:
        """Build the prompt for NPC interaction"""
        npc = context.npc_profile
        
        # Base system prompt
        system_prompt = f"""You are {npc.name}, a {npc.role} in the Chronicles of Ruin saga.

PERSONALITY: {npc.personality}
BACKGROUND: {npc.background}
LOCATION: {npc.location}
CONVERSATION STYLE: {npc.conversation_style}
RELATIONSHIP TO PLAYER: {context.player_context.get('relationship', npc.relationship_to_player)}

KNOWLEDGE DOMAINS: {', '.join(npc.knowledge_domains)}

IMPORTANT RULES:
- Stay in character as {npc.name}
- Respond naturally and conversationally
- Provide hints and information relevant to your knowledge domains
- Keep responses concise but helpful
- Don't reveal major plot points unless appropriate
- Show personality through your responses
- If you don't know something, say so rather than making things up

CURRENT CONTEXT:
- Player location: {context.current_location}
- Game state: {json.dumps(context.game_state, indent=2)}
- Conversation history: {len(context.conversation_history)} messages

Respond as {npc.name} to the player's message: "{player_message}"
"""
        
        return system_prompt
    
    def _call_ollama(self, prompt: str, images: Optional[List[str]] = None) -> str:
        """Call Ollama API for response"""
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens
                }
            }
            
            # Add images if provided
            if images:
                payload["images"] = images
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                self.logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return "I'm having trouble thinking right now. Could you repeat that?"
                
        except Exception as e:
            self.logger.error(f"Failed to call Ollama: {e}")
            return "I'm not feeling well today. Maybe we can talk later?"
    
    def interact_with_npc(self, npc_name: str, player_message: str, 
                         context: Optional[Dict[str, Any]] = None,
                         interaction_type: InteractionType = InteractionType.TEXT_ONLY,
                         images: Optional[List[str]] = None) -> NPCResponse:
        """Interact with an NPC"""
        
        # Get NPC profile
        npc_profile = self.get_npc_profile(npc_name)
        if not npc_profile:
            return NPCResponse(
                text=f"I don't know anyone named {npc_name}.",
                emotion="confused"
            )
        
        # Build context
        if context is None:
            context = {}
        
        interaction_context = InteractionContext(
            npc_profile=npc_profile,
            player_context=context.get('player', {}),
            conversation_history=context.get('history', []),
            current_location=context.get('location', 'unknown'),
            game_state=context.get('game_state', {}),
            interaction_type=interaction_type
        )
        
        # Build prompt
        prompt = self._build_prompt(interaction_context, player_message)
        
        # Call Ollama
        response_text = self._call_ollama(prompt, images)
        
        # Determine emotion from response
        emotion = self._analyze_emotion(response_text)
        
        # Generate voice if needed
        voice_file = None
        if interaction_type in [InteractionType.VOICE_AND_TEXT, InteractionType.MULTIMODAL]:
            voice_file = self._generate_voice(response_text, npc_profile.voice_style)
        
        # Generate image if needed
        image_file = None
        if interaction_type in [InteractionType.IMAGE_AND_TEXT, InteractionType.MULTIMODAL]:
            image_file = self._generate_npc_image(npc_profile, emotion)
        
        # Save conversation
        self._save_conversation(npc_name, player_message, response_text, context)
        
        return NPCResponse(
            text=response_text,
            emotion=emotion,
            voice_file=voice_file,
            image_file=image_file,
            metadata={
                "npc_name": npc_name,
                "interaction_type": interaction_type.value,
                "timestamp": time.time()
            }
        )
    
    def _analyze_emotion(self, text: str) -> str:
        """Analyze the emotional tone of the response"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['happy', 'joy', 'excited', 'great', 'wonderful']):
            return "happy"
        elif any(word in text_lower for word in ['sad', 'sorry', 'unfortunate', 'regret']):
            return "sad"
        elif any(word in text_lower for word in ['angry', 'furious', 'mad', 'upset']):
            return "angry"
        elif any(word in text_lower for word in ['afraid', 'scared', 'fear', 'terrified']):
            return "afraid"
        elif any(word in text_lower for word in ['surprised', 'shocked', 'amazed', 'wow']):
            return "surprised"
        else:
            return "neutral"
    
    def _generate_voice(self, text: str, voice_style: str) -> Optional[str]:
        """Generate voice file for NPC response"""
        # This would integrate with a TTS system
        # For now, return None (placeholder)
        return None
    
    def _generate_npc_image(self, npc_profile: NPCProfile, emotion: str) -> Optional[str]:
        """Generate NPC image based on profile and emotion"""
        # This would integrate with the Stable Diffusion system
        # For now, return None (placeholder)
        return None
    
    def _save_conversation(self, npc_name: str, player_message: str, 
                          npc_response: str, context: Dict[str, Any]):
        """Save conversation to history"""
        conversation_file = self.conversations_dir / f"{npc_name.lower().replace(' ', '_')}_history.json"
        
        try:
            if conversation_file.exists():
                with open(conversation_file, 'r') as f:
                    conversations = json.load(f)
            else:
                conversations = []
            
            conversations.append({
                "timestamp": time.time(),
                "player_message": player_message,
                "npc_response": npc_response,
                "context": context
            })
            
            # Keep only last 50 conversations
            if len(conversations) > 50:
                conversations = conversations[-50:]
            
            with open(conversation_file, 'w') as f:
                json.dump(conversations, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to save conversation: {e}")
    
    def get_conversation_history(self, npc_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get conversation history for an NPC"""
        conversation_file = self.conversations_dir / f"{npc_name.lower().replace(' ', '_')}_history.json"
        
        if conversation_file.exists():
            try:
                with open(conversation_file, 'r') as f:
                    conversations = json.load(f)
                return conversations[-limit:]
            except Exception as e:
                self.logger.error(f"Failed to load conversation history: {e}")
        
        return []
    
    def create_sample_npcs(self):
        """Create sample NPCs for testing"""
        sample_npcs = [
            NPCProfile(
                name="Eldric the Blacksmith",
                role="Master Blacksmith",
                personality="Gruff but kind-hearted, takes pride in his craft, loves to share stories about weapons",
                background="Has been forging weapons for 30 years, knows every type of metal and enchantment",
                location="Sunderfall Forge",
                voice_style="deep_rough",
                conversation_style="casual",
                knowledge_domains=["weapons", "armor", "metals", "enchantments", "local gossip"],
                relationship_to_player="friendly"
            ),
            NPCProfile(
                name="Mira the Healer",
                role="Village Healer",
                personality="Gentle and caring, always concerned about others' wellbeing, wise beyond her years",
                background="Learned healing from her grandmother, has saved many lives in the village",
                location="Healing House",
                voice_style="soft_caring",
                conversation_style="formal",
                knowledge_domains=["healing", "herbs", "medicine", "village history", "spirits"],
                relationship_to_player="caring"
            ),
            NPCProfile(
                name="Grim the Guard",
                role="Town Guard",
                personality="Suspicious of strangers, loyal to the town, always on alert for danger",
                background="Former soldier, has seen many battles, protects the town with his life",
                location="Town Gate",
                voice_style="stern_authoritative",
                conversation_style="direct",
                knowledge_domains=["security", "combat", "town defense", "suspicious activity", "military"],
                relationship_to_player="cautious"
            )
        ]
        
        for npc in sample_npcs:
            self._save_npc_profile(npc)
        
        self.logger.info(f"Created {len(sample_npcs)} sample NPCs")

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="NPC AI System for Chronicles of Ruin")
    parser.add_argument("command", choices=[
        "check", "list", "create", "interact", "history", "samples"
    ])
    parser.add_argument("--npc", help="NPC name")
    parser.add_argument("--message", help="Message to NPC")
    parser.add_argument("--role", help="NPC role")
    parser.add_argument("--personality", help="NPC personality")
    parser.add_argument("--background", help="NPC background")
    parser.add_argument("--location", help="NPC location")
    parser.add_argument("--type", choices=["text", "image_text", "voice_text", "multimodal"], 
                       default="text", help="Interaction type")
    
    args = parser.parse_args()
    
    # Initialize system
    base_dir = Path.cwd()
    npc_system = NPCAISystem(base_dir)
    
    if args.command == "check":
        if npc_system.check_ollama_connection():
            print("SUCCESS: Ollama is running and model is available")
        else:
            print("ERROR: Ollama is not available")
            print("Make sure Ollama is running and the model is installed:")
            print("  ollama pull llama3.1:8b")
    
    elif args.command == "list":
        npcs = npc_system.list_npcs()
        if npcs:
            print("Available NPCs:")
            for npc in npcs:
                profile = npc_system.get_npc_profile(npc)
                print(f"  - {npc} ({profile.role}) at {profile.location}")
        else:
            print("No NPCs found. Create some with 'create' command.")
    
    elif args.command == "create":
        if not all([args.npc, args.role, args.personality, args.background, args.location]):
            print("Error: All fields required for NPC creation")
            print("Usage: --npc NAME --role ROLE --personality PERSONALITY --background BACKGROUND --location LOCATION")
            return
        
        profile = npc_system.create_npc_profile(
            name=args.npc,
            role=args.role,
            personality=args.personality,
            background=args.background,
            location=args.location
        )
        print(f"SUCCESS: Created NPC: {profile.name}")
    
    elif args.command == "interact":
        if not all([args.npc, args.message]):
            print("Error: NPC name and message required")
            print("Usage: --npc NAME --message 'Your message'")
            return
        
        interaction_type = InteractionType(args.type)
        response = npc_system.interact_with_npc(
            args.npc, 
            args.message, 
            interaction_type=interaction_type
        )
        
        print(f"\n{args.npc} ({response.emotion}):")
        print(f"  {response.text}")
        
        if response.voice_file:
            print(f"  Voice: {response.voice_file}")
        if response.image_file:
            print(f"  Image: {response.image_file}")
    
    elif args.command == "history":
        if not args.npc:
            print("Error: NPC name required")
            return
        
        history = npc_system.get_conversation_history(args.npc, 5)
        if history:
            print(f"Recent conversations with {args.npc}:")
            for conv in history:
                print(f"  Player: {conv['player_message']}")
                print(f"  {args.npc}: {conv['npc_response']}")
                print()
        else:
            print(f"No conversation history for {args.npc}")
    
    elif args.command == "samples":
        npc_system.create_sample_npcs()
        print("SUCCESS: Created sample NPCs")
        print("  - Eldric the Blacksmith")
        print("  - Mira the Healer")
        print("  - Grim the Guard")

if __name__ == "__main__":
    main()

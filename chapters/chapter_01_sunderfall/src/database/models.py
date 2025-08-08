"""
Chronicles of Ruin: Sunderfall - Database Models
Comprehensive SQLAlchemy models for Discord bot with multiplayer systems
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    BigInteger,
    Boolean,
    DateTime,
    Text,
    Numeric,
    ForeignKey,
    UniqueConstraint,
    Index,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import TypeDecorator, JSON
from datetime import datetime
import enum

Base = declarative_base()

# =====================================================
# CUSTOM TYPES FOR CROSS-DATABASE COMPATIBILITY
# =====================================================


class JSONB(TypeDecorator):
    """Cross-database JSONB type that works with both PostgreSQL and SQLite"""

    impl = JSON

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# =====================================================
# ENUMERATIONS
# =====================================================


class ArenaType(enum.Enum):
    ONE_VS_ONE = "1v1"
    TWO_VS_TWO = "2v2"
    THREE_VS_THREE = "3v3"


class MatchType(enum.Enum):
    DUEL = "duel"
    ARENA = "arena"
    BATTLEGROUND = "battleground"


class TournamentType(enum.Enum):
    SINGLE_ELIMINATION = "single_elimination"
    DOUBLE_ELIMINATION = "double_elimination"
    ROUND_ROBIN = "round_robin"


class ListingType(enum.Enum):
    SALE = "sale"
    AUCTION = "auction"
    TRADE = "trade"


class TransactionType(enum.Enum):
    SALE = "sale"
    PURCHASE = "purchase"
    AUCTION_WIN = "auction_win"
    GUILD_TRANSFER = "guild_transfer"


class SessionType(enum.Enum):
    COMBAT = "combat"
    EXPLORATION = "exploration"
    TRADING = "trading"


class ActionType(enum.Enum):
    ATTACK = "attack"
    SKILL = "skill"
    ITEM = "item"
    STATUS = "status"


class StatType(enum.Enum):
    COMBAT = "combat"
    TRADING = "trading"
    GUILD = "guild"
    PVP = "pvp"


class EventType(enum.Enum):
    SEASONAL = "seasonal"
    TOURNAMENT = "tournament"
    GUILD_WAR = "guild_war"


# =====================================================
# CORE PLAYER & CHARACTER MODELS
# =====================================================


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    discord_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    settings = Column(JSONB, default={})
    is_active = Column(Boolean, default=True)

    # Relationships
    characters = relationship("Character", back_populates="player")


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"))
    name = Column(String(100), nullable=False)
    class_name = Column(String(50), nullable=False)  # 'class' is reserved
    archetype = Column(String(50))
    level = Column(Integer, default=1)
    experience = Column(BigInteger, default=0)
    health = Column(Integer, nullable=False)
    max_health = Column(Integer, nullable=False)
    mana = Column(Integer, nullable=False)
    max_mana = Column(Integer, nullable=False)
    strength = Column(Integer, default=10)
    dexterity = Column(Integer, default=10)
    intelligence = Column(Integer, default=10)
    vitality = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow)
    achievements = Column(JSONB, default=[])
    is_active = Column(Boolean, default=True)

    # Relationships
    player = relationship("Player", back_populates="characters")
    inventory = relationship("Inventory", back_populates="character", uselist=False)
    equipped_items = relationship("EquippedItem", back_populates="character")
    guild_membership = relationship(
        "GuildMember", back_populates="character", uselist=False
    )
    pvp_matches_player1 = relationship("PvPMatch", foreign_keys="PvPMatch.player1_id")
    pvp_matches_player2 = relationship("PvPMatch", foreign_keys="PvPMatch.player2_id")
    arena_rankings = relationship("ArenaRanking", back_populates="character")
    trading_posts = relationship("TradingPost", back_populates="seller")
    auction_listings = relationship("AuctionHouse", back_populates="seller")
    active_sessions = relationship("ActiveSession", back_populates="character")


class Inventory(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"))
    gold = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    character = relationship("Character", back_populates="inventory")
    items = relationship("InventoryItem", back_populates="inventory")


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True)
    inventory_id = Column(Integer, ForeignKey("inventories.id", ondelete="CASCADE"))
    item_id = Column(String(100), nullable=False)
    item_name = Column(String(255), nullable=False)
    item_type = Column(String(50), nullable=False)
    rarity = Column(String(20), nullable=False)
    quantity = Column(Integer, default=1)
    durability = Column(Integer)
    max_durability = Column(Integer)
    enchantments = Column(JSONB, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    inventory = relationship("Inventory", back_populates="items")
    equipped_in = relationship("EquippedItem", back_populates="item")


class EquippedItem(Base):
    __tablename__ = "equipped_items"

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"))
    slot = Column(String(50), nullable=False)
    item_id = Column(Integer, ForeignKey("inventory_items.id", ondelete="SET NULL"))

    # Relationships
    character = relationship("Character", back_populates="equipped_items")
    item = relationship("InventoryItem", back_populates="equipped_in")

    __table_args__ = (UniqueConstraint("character_id", "slot"),)


# =====================================================
# GUILD & ALLIANCE MODELS
# =====================================================


class Guild(Base):
    __tablename__ = "guilds"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    tag = Column(String(10), unique=True, nullable=False)
    description = Column(Text)
    leader_id = Column(Integer, ForeignKey("characters.id"))
    level = Column(Integer, default=1)
    experience = Column(BigInteger, default=0)
    treasury_gold = Column(Integer, default=0)
    max_members = Column(Integer, default=50)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    settings = Column(JSONB, default={})

    # Relationships
    leader = relationship("Character")
    members = relationship("GuildMember", back_populates="guild")
    ranks = relationship("GuildRank", back_populates="guild")
    territories = relationship("Territory", back_populates="guild")
    alliance_membership = relationship("AllianceMember", back_populates="guild")


class GuildMember(Base):
    __tablename__ = "guild_members"

    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer, ForeignKey("guilds.id", ondelete="CASCADE"))
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"))
    rank = Column(String(50), default="Member")
    rank_level = Column(Integer, default=1)
    joined_at = Column(DateTime, default=datetime.utcnow)
    contribution_points = Column(Integer, default=0)
    last_contribution = Column(DateTime, default=datetime.utcnow)

    # Relationships
    guild = relationship("Guild", back_populates="members")
    character = relationship("Character", back_populates="guild_membership")

    __table_args__ = (UniqueConstraint("guild_id", "character_id"),)


class GuildRank(Base):
    __tablename__ = "guild_ranks"

    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer, ForeignKey("guilds.id", ondelete="CASCADE"))
    rank_name = Column(String(50), nullable=False)
    rank_level = Column(Integer, nullable=False)
    permissions = Column(JSONB, default={})
    color = Column(String(7), default="#FFFFFF")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    guild = relationship("Guild", back_populates="ranks")


class Alliance(Base):
    __tablename__ = "alliances"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    leader_guild_id = Column(Integer, ForeignKey("guilds.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    leader_guild = relationship("Guild")
    members = relationship("AllianceMember", back_populates="alliance")


class AllianceMember(Base):
    __tablename__ = "alliance_members"

    id = Column(Integer, primary_key=True)
    alliance_id = Column(Integer, ForeignKey("alliances.id", ondelete="CASCADE"))
    guild_id = Column(Integer, ForeignKey("guilds.id", ondelete="CASCADE"))
    joined_at = Column(DateTime, default=datetime.utcnow)
    contribution_points = Column(Integer, default=0)

    # Relationships
    alliance = relationship("Alliance", back_populates="members")
    guild = relationship("Guild", back_populates="alliance_membership")

    __table_args__ = (UniqueConstraint("alliance_id", "guild_id"),)


class Territory(Base):
    __tablename__ = "territories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    guild_id = Column(Integer, ForeignKey("guilds.id", ondelete="SET NULL"))
    territory_type = Column(String(50), nullable=False)
    level = Column(Integer, default=1)
    benefits = Column(JSONB, default={})
    claimed_at = Column(DateTime)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    guild = relationship("Guild", back_populates="territories")


# =====================================================
# PVP & COMPETITIVE MODELS
# =====================================================


class PvPMatch(Base):
    __tablename__ = "pvp_matches"

    id = Column(Integer, primary_key=True)
    match_type = Column(String(50), nullable=False)
    player1_id = Column(Integer, ForeignKey("characters.id"))
    player2_id = Column(Integer, ForeignKey("characters.id"))
    winner_id = Column(Integer, ForeignKey("characters.id"))
    match_data = Column(JSONB, default={})
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime)
    duration_seconds = Column(Integer)
    is_ranked = Column(Boolean, default=False)

    # Relationships
    player1 = relationship("Character", foreign_keys=[player1_id])
    player2 = relationship("Character", foreign_keys=[player2_id])
    winner = relationship("Character", foreign_keys=[winner_id])


class ArenaRanking(Base):
    __tablename__ = "arena_rankings"

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"))
    arena_type = Column(String(50), nullable=False)
    rating = Column(Integer, default=1000)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    draws = Column(Integer, default=0)
    season = Column(Integer, default=1)
    rank_tier = Column(String(20))
    rank_division = Column(Integer)
    last_match_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    character = relationship("Character", back_populates="arena_rankings")

    __table_args__ = (UniqueConstraint("character_id", "arena_type", "season"),)


class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    tournament_type = Column(String(50), nullable=False)
    max_participants = Column(Integer)
    current_participants = Column(Integer, default=0)
    entry_fee = Column(Integer, default=0)
    prize_pool = Column(JSONB, default={})
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String(20), default="upcoming")
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    participants = relationship("TournamentParticipant", back_populates="tournament")
    brackets = relationship("TournamentBracket", back_populates="tournament")


class TournamentParticipant(Base):
    __tablename__ = "tournament_participants"

    id = Column(Integer, primary_key=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id", ondelete="CASCADE"))
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"))
    registered_at = Column(DateTime, default=datetime.utcnow)
    eliminated_at = Column(DateTime)
    final_rank = Column(Integer)
    prize_earned = Column(Integer, default=0)

    # Relationships
    tournament = relationship("Tournament", back_populates="participants")
    character = relationship("Character")

    __table_args__ = (UniqueConstraint("tournament_id", "character_id"),)


class TournamentBracket(Base):
    __tablename__ = "tournament_brackets"

    id = Column(Integer, primary_key=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id", ondelete="CASCADE"))
    round_number = Column(Integer, nullable=False)
    match_number = Column(Integer, nullable=False)
    player1_id = Column(Integer, ForeignKey("tournament_participants.id"))
    player2_id = Column(Integer, ForeignKey("tournament_participants.id"))
    winner_id = Column(Integer, ForeignKey("tournament_participants.id"))
    match_data = Column(JSONB, default={})
    scheduled_at = Column(DateTime)
    completed_at = Column(DateTime)

    # Relationships
    tournament = relationship("Tournament", back_populates="brackets")
    player1 = relationship("TournamentParticipant", foreign_keys=[player1_id])
    player2 = relationship("TournamentParticipant", foreign_keys=[player2_id])
    winner = relationship("TournamentParticipant", foreign_keys=[winner_id])

    __table_args__ = (
        UniqueConstraint("tournament_id", "round_number", "match_number"),
    )


# =====================================================
# TRADING & ECONOMY MODELS
# =====================================================


class TradingPost(Base):
    __tablename__ = "trading_posts"

    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"))
    item_id = Column(Integer, ForeignKey("inventory_items.id", ondelete="CASCADE"))
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    listing_type = Column(String(20), default="sale")
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)

    # Relationships
    seller = relationship("Character", back_populates="trading_posts")
    item = relationship("InventoryItem")


class AuctionHouse(Base):
    __tablename__ = "auction_house"

    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"))
    item_id = Column(Integer, ForeignKey("inventory_items.id", ondelete="CASCADE"))
    starting_bid = Column(Integer, nullable=False)
    buyout_price = Column(Integer)
    current_bid = Column(Integer)
    current_bidder_id = Column(Integer, ForeignKey("characters.id"))
    quantity = Column(Integer, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    ends_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    seller = relationship("Character", back_populates="auction_listings")
    current_bidder = relationship("Character", foreign_keys=[current_bidder_id])
    item = relationship("InventoryItem")
    bids = relationship("AuctionBid", back_populates="auction")


class AuctionBid(Base):
    __tablename__ = "auction_bids"

    id = Column(Integer, primary_key=True)
    auction_id = Column(Integer, ForeignKey("auction_house.id", ondelete="CASCADE"))
    bidder_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"))
    bid_amount = Column(Integer, nullable=False)
    bid_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    auction = relationship("AuctionHouse", back_populates="bids")
    bidder = relationship("Character")


class TradingTransaction(Base):
    __tablename__ = "trading_transactions"

    id = Column(Integer, primary_key=True)
    transaction_type = Column(String(50), nullable=False)
    buyer_id = Column(Integer, ForeignKey("characters.id"))
    seller_id = Column(Integer, ForeignKey("characters.id"))
    item_id = Column(Integer, ForeignKey("inventory_items.id"))
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    commission = Column(Integer, default=0)
    transaction_data = Column(JSONB, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    buyer = relationship("Character", foreign_keys=[buyer_id])
    seller = relationship("Character", foreign_keys=[seller_id])
    item = relationship("InventoryItem")


# =====================================================
# COMBAT & SESSION MODELS
# =====================================================


class ActiveSession(Base):
    __tablename__ = "active_sessions"

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"))
    session_type = Column(String(50), nullable=False)
    session_data = Column(JSONB, default={})
    started_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    character = relationship("Character", back_populates="active_sessions")
    combat_logs = relationship("CombatLog", back_populates="session")


class CombatLog(Base):
    __tablename__ = "combat_logs"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("active_sessions.id", ondelete="CASCADE"))
    attacker_id = Column(Integer, ForeignKey("characters.id"))
    target_id = Column(Integer, ForeignKey("characters.id"))
    action_type = Column(String(50), nullable=False)
    damage_dealt = Column(Integer, default=0)
    damage_taken = Column(Integer, default=0)
    status_effects = Column(JSONB, default=[])
    combat_data = Column(JSONB, default={})
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    session = relationship("ActiveSession", back_populates="combat_logs")
    attacker = relationship("Character", foreign_keys=[attacker_id])
    target = relationship("Character", foreign_keys=[target_id])


class Party(Base):
    __tablename__ = "parties"

    id = Column(Integer, primary_key=True)
    leader_id = Column(Integer, ForeignKey("characters.id"))
    party_type = Column(String(50), default="exploration")
    max_members = Column(Integer, default=4)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    leader = relationship("Character")
    members = relationship("PartyMember", back_populates="party")


class PartyMember(Base):
    __tablename__ = "party_members"

    id = Column(Integer, primary_key=True)
    party_id = Column(Integer, ForeignKey("parties.id", ondelete="CASCADE"))
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"))
    joined_at = Column(DateTime, default=datetime.utcnow)
    is_leader = Column(Boolean, default=False)

    # Relationships
    party = relationship("Party", back_populates="members")
    character = relationship("Character")

    __table_args__ = (UniqueConstraint("party_id", "character_id"),)


# =====================================================
# ANALYTICS & MONITORING MODELS
# =====================================================


class UserStat(Base):
    __tablename__ = "user_stats"

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"))
    stat_type = Column(String(50), nullable=False)
    stat_name = Column(String(100), nullable=False)
    stat_value = Column(Numeric, default=0)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    character = relationship("Character")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    event_name = Column(String(255), nullable=False)
    event_type = Column(String(50), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    rewards = Column(JSONB, default={})
    participants = Column(JSONB, default=[])
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

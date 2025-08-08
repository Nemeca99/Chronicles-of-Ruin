-- Chronicles of Ruin: Sunderfall - Database Schema
-- Comprehensive schema for Discord bot with multiplayer systems

-- =====================================================
-- CORE PLAYER & CHARACTER TABLES
-- =====================================================

-- Players table (Discord users)
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    discord_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    settings JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE
);

-- Characters table (player characters)
CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    class VARCHAR(50) NOT NULL,
    archetype VARCHAR(50),
    level INTEGER DEFAULT 1,
    experience BIGINT DEFAULT 0,
    health INTEGER NOT NULL,
    max_health INTEGER NOT NULL,
    mana INTEGER NOT NULL,
    max_mana INTEGER NOT NULL,
    strength INTEGER DEFAULT 10,
    dexterity INTEGER DEFAULT 10,
    intelligence INTEGER DEFAULT 10,
    vitality INTEGER DEFAULT 10,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    achievements JSONB DEFAULT '[]',
    is_active BOOLEAN DEFAULT TRUE
);

-- Inventories table
CREATE TABLE inventories (
    id SERIAL PRIMARY KEY,
    character_id INTEGER REFERENCES characters(id) ON DELETE CASCADE,
    gold INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inventory items table
CREATE TABLE inventory_items (
    id SERIAL PRIMARY KEY,
    inventory_id INTEGER REFERENCES inventories(id) ON DELETE CASCADE,
    item_id VARCHAR(100) NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    item_type VARCHAR(50) NOT NULL,
    rarity VARCHAR(20) NOT NULL,
    quantity INTEGER DEFAULT 1,
    durability INTEGER,
    max_durability INTEGER,
    enchantments JSONB DEFAULT '[]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Equipped items table
CREATE TABLE equipped_items (
    id SERIAL PRIMARY KEY,
    character_id INTEGER REFERENCES characters(id) ON DELETE CASCADE,
    slot VARCHAR(50) NOT NULL,
    item_id INTEGER REFERENCES inventory_items(id) ON DELETE SET NULL,
    UNIQUE(character_id, slot)
);

-- =====================================================
-- GUILD & ALLIANCE SYSTEM TABLES
-- =====================================================

-- Guilds table
CREATE TABLE guilds (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    tag VARCHAR(10) UNIQUE NOT NULL,
    description TEXT,
    leader_id INTEGER REFERENCES characters(id),
    level INTEGER DEFAULT 1,
    experience BIGINT DEFAULT 0,
    treasury_gold INTEGER DEFAULT 0,
    max_members INTEGER DEFAULT 50,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    settings JSONB DEFAULT '{}'
);

-- Guild members table
CREATE TABLE guild_members (
    id SERIAL PRIMARY KEY,
    guild_id INTEGER REFERENCES guilds(id) ON DELETE CASCADE,
    character_id INTEGER REFERENCES characters(id) ON DELETE CASCADE,
    rank VARCHAR(50) DEFAULT 'Member',
    rank_level INTEGER DEFAULT 1,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    contribution_points INTEGER DEFAULT 0,
    last_contribution TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(guild_id, character_id)
);

-- Guild ranks table (customizable ranks)
CREATE TABLE guild_ranks (
    id SERIAL PRIMARY KEY,
    guild_id INTEGER REFERENCES guilds(id) ON DELETE CASCADE,
    rank_name VARCHAR(50) NOT NULL,
    rank_level INTEGER NOT NULL,
    permissions JSONB DEFAULT '{}',
    color VARCHAR(7) DEFAULT '#FFFFFF',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alliances table
CREATE TABLE alliances (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    leader_guild_id INTEGER REFERENCES guilds(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Alliance members table
CREATE TABLE alliance_members (
    id SERIAL PRIMARY KEY,
    alliance_id INTEGER REFERENCES alliances(id) ON DELETE CASCADE,
    guild_id INTEGER REFERENCES guilds(id) ON DELETE CASCADE,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    contribution_points INTEGER DEFAULT 0,
    UNIQUE(alliance_id, guild_id)
);

-- Territories table
CREATE TABLE territories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    guild_id INTEGER REFERENCES guilds(id) ON DELETE SET NULL,
    territory_type VARCHAR(50) NOT NULL,
    level INTEGER DEFAULT 1,
    benefits JSONB DEFAULT '{}',
    claimed_at TIMESTAMP,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- PVP & COMPETITIVE SYSTEM TABLES
-- =====================================================

-- PvP matches table
CREATE TABLE pvp_matches (
    id SERIAL PRIMARY KEY,
    match_type VARCHAR(50) NOT NULL, -- 'duel', 'arena', 'battleground'
    player1_id INTEGER REFERENCES characters(id),
    player2_id INTEGER REFERENCES characters(id),
    winner_id INTEGER REFERENCES characters(id),
    match_data JSONB DEFAULT '{}',
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    duration_seconds INTEGER,
    is_ranked BOOLEAN DEFAULT FALSE
);

-- Arena rankings table
CREATE TABLE arena_rankings (
    id SERIAL PRIMARY KEY,
    character_id INTEGER REFERENCES characters(id) ON DELETE CASCADE,
    arena_type VARCHAR(50) NOT NULL, -- '1v1', '2v2', '3v3'
    rating INTEGER DEFAULT 1000,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    draws INTEGER DEFAULT 0,
    season INTEGER DEFAULT 1,
    rank_tier VARCHAR(20),
    rank_division INTEGER,
    last_match_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(character_id, arena_type, season)
);

-- Tournaments table
CREATE TABLE tournaments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    tournament_type VARCHAR(50) NOT NULL, -- 'single_elimination', 'double_elimination', 'round_robin'
    max_participants INTEGER,
    current_participants INTEGER DEFAULT 0,
    entry_fee INTEGER DEFAULT 0,
    prize_pool JSONB DEFAULT '{}',
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    status VARCHAR(20) DEFAULT 'upcoming', -- 'upcoming', 'active', 'completed', 'cancelled'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tournament participants table
CREATE TABLE tournament_participants (
    id SERIAL PRIMARY KEY,
    tournament_id INTEGER REFERENCES tournaments(id) ON DELETE CASCADE,
    character_id INTEGER REFERENCES characters(id) ON DELETE CASCADE,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    eliminated_at TIMESTAMP,
    final_rank INTEGER,
    prize_earned INTEGER DEFAULT 0,
    UNIQUE(tournament_id, character_id)
);

-- Tournament brackets table
CREATE TABLE tournament_brackets (
    id SERIAL PRIMARY KEY,
    tournament_id INTEGER REFERENCES tournaments(id) ON DELETE CASCADE,
    round_number INTEGER NOT NULL,
    match_number INTEGER NOT NULL,
    player1_id INTEGER REFERENCES tournament_participants(id),
    player2_id INTEGER REFERENCES tournament_participants(id),
    winner_id INTEGER REFERENCES tournament_participants(id),
    match_data JSONB DEFAULT '{}',
    scheduled_at TIMESTAMP,
    completed_at TIMESTAMP,
    UNIQUE(tournament_id, round_number, match_number)
);

-- =====================================================
-- TRADING & ECONOMY SYSTEM TABLES
-- =====================================================

-- Trading posts table
CREATE TABLE trading_posts (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER REFERENCES characters(id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES inventory_items(id) ON DELETE CASCADE,
    price INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    listing_type VARCHAR(20) DEFAULT 'sale', -- 'sale', 'auction', 'trade'
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Auction house table
CREATE TABLE auction_house (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER REFERENCES characters(id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES inventory_items(id) ON DELETE CASCADE,
    starting_bid INTEGER NOT NULL,
    buyout_price INTEGER,
    current_bid INTEGER,
    current_bidder_id INTEGER REFERENCES characters(id),
    quantity INTEGER NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ends_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

-- Auction bids table
CREATE TABLE auction_bids (
    id SERIAL PRIMARY KEY,
    auction_id INTEGER REFERENCES auction_house(id) ON DELETE CASCADE,
    bidder_id INTEGER REFERENCES characters(id) ON DELETE CASCADE,
    bid_amount INTEGER NOT NULL,
    bid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trading transactions table
CREATE TABLE trading_transactions (
    id SERIAL PRIMARY KEY,
    transaction_type VARCHAR(50) NOT NULL, -- 'sale', 'purchase', 'auction_win', 'guild_transfer'
    buyer_id INTEGER REFERENCES characters(id),
    seller_id INTEGER REFERENCES characters(id),
    item_id INTEGER REFERENCES inventory_items(id),
    quantity INTEGER NOT NULL,
    price INTEGER NOT NULL,
    commission INTEGER DEFAULT 0,
    transaction_data JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- COMBAT & SESSION TABLES
-- =====================================================

-- Active sessions table
CREATE TABLE active_sessions (
    id SERIAL PRIMARY KEY,
    character_id INTEGER REFERENCES characters(id) ON DELETE CASCADE,
    session_type VARCHAR(50) NOT NULL, -- 'combat', 'exploration', 'trading'
    session_data JSONB DEFAULT '{}',
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Combat logs table
CREATE TABLE combat_logs (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES active_sessions(id) ON DELETE CASCADE,
    attacker_id INTEGER REFERENCES characters(id),
    target_id INTEGER REFERENCES characters(id),
    action_type VARCHAR(50) NOT NULL, -- 'attack', 'skill', 'item', 'status'
    damage_dealt INTEGER DEFAULT 0,
    damage_taken INTEGER DEFAULT 0,
    status_effects JSONB DEFAULT '[]',
    combat_data JSONB DEFAULT '{}',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Party system table
CREATE TABLE parties (
    id SERIAL PRIMARY KEY,
    leader_id INTEGER REFERENCES characters(id),
    party_type VARCHAR(50) DEFAULT 'exploration', -- 'exploration', 'dungeon', 'pvp'
    max_members INTEGER DEFAULT 4,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Party members table
CREATE TABLE party_members (
    id SERIAL PRIMARY KEY,
    party_id INTEGER REFERENCES parties(id) ON DELETE CASCADE,
    character_id INTEGER REFERENCES characters(id) ON DELETE CASCADE,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_leader BOOLEAN DEFAULT FALSE,
    UNIQUE(party_id, character_id)
);

-- =====================================================
-- ANALYTICS & MONITORING TABLES
-- =====================================================

-- User statistics table
CREATE TABLE user_stats (
    id SERIAL PRIMARY KEY,
    character_id INTEGER REFERENCES characters(id) ON DELETE CASCADE,
    stat_type VARCHAR(50) NOT NULL, -- 'combat', 'trading', 'guild', 'pvp'
    stat_name VARCHAR(100) NOT NULL,
    stat_value NUMERIC DEFAULT 0,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Events table
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_name VARCHAR(255) NOT NULL,
    event_type VARCHAR(50) NOT NULL, -- 'seasonal', 'tournament', 'guild_war'
    description TEXT,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    rewards JSONB DEFAULT '{}',
    participants JSONB DEFAULT '[]',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Core indexes
CREATE INDEX idx_players_discord_id ON players(discord_id);
CREATE INDEX idx_characters_player_id ON characters(player_id);
CREATE INDEX idx_characters_name ON characters(name);
CREATE INDEX idx_inventory_items_inventory_id ON inventory_items(inventory_id);
CREATE INDEX idx_equipped_items_character_id ON equipped_items(character_id);

-- Guild indexes
CREATE INDEX idx_guild_members_guild_id ON guild_members(guild_id);
CREATE INDEX idx_guild_members_character_id ON guild_members(character_id);
CREATE INDEX idx_alliance_members_alliance_id ON alliance_members(alliance_id);
CREATE INDEX idx_territories_guild_id ON territories(guild_id);

-- PvP indexes
CREATE INDEX idx_pvp_matches_player1_id ON pvp_matches(player1_id);
CREATE INDEX idx_pvp_matches_player2_id ON pvp_matches(player2_id);
CREATE INDEX idx_arena_rankings_character_id ON arena_rankings(character_id);
CREATE INDEX idx_arena_rankings_season ON arena_rankings(season);
CREATE INDEX idx_tournament_participants_tournament_id ON tournament_participants(tournament_id);

-- Trading indexes
CREATE INDEX idx_trading_posts_seller_id ON trading_posts(seller_id);
CREATE INDEX idx_trading_posts_is_active ON trading_posts(is_active);
CREATE INDEX idx_auction_house_seller_id ON auction_house(seller_id);
CREATE INDEX idx_auction_house_is_active ON auction_house(is_active);
CREATE INDEX idx_trading_transactions_buyer_id ON trading_transactions(buyer_id);
CREATE INDEX idx_trading_transactions_seller_id ON trading_transactions(seller_id);

-- Session indexes
CREATE INDEX idx_active_sessions_character_id ON active_sessions(character_id);
CREATE INDEX idx_active_sessions_is_active ON active_sessions(is_active);
CREATE INDEX idx_combat_logs_session_id ON combat_logs(session_id);
CREATE INDEX idx_party_members_party_id ON party_members(party_id);

-- Analytics indexes
CREATE INDEX idx_user_stats_character_id ON user_stats(character_id);
CREATE INDEX idx_user_stats_stat_type ON user_stats(stat_type);
CREATE INDEX idx_events_start_date ON events(start_date);
CREATE INDEX idx_events_is_active ON events(is_active);

-- =====================================================
-- TRIGGERS FOR DATA INTEGRITY
-- =====================================================

-- Update last_active timestamp on player activity
CREATE OR REPLACE FUNCTION update_player_last_active()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE players SET last_active = CURRENT_TIMESTAMP WHERE id = NEW.player_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_player_last_active
    AFTER INSERT OR UPDATE ON characters
    FOR EACH ROW
    EXECUTE FUNCTION update_player_last_active();

-- Update character last_login on session creation
CREATE OR REPLACE FUNCTION update_character_last_login()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE characters SET last_login = CURRENT_TIMESTAMP WHERE id = NEW.character_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_character_last_login
    AFTER INSERT ON active_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_character_last_login();

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- Character overview view
CREATE VIEW character_overview AS
SELECT 
    c.id,
    c.name,
    p.username as player_name,
    c.class,
    c.archetype,
    c.level,
    c.experience,
    c.health,
    c.max_health,
    c.mana,
    c.max_mana,
    c.strength,
    c.dexterity,
    c.intelligence,
    c.vitality,
    g.name as guild_name,
    g.tag as guild_tag,
    gm.rank as guild_rank
FROM characters c
JOIN players p ON c.player_id = p.id
LEFT JOIN guild_members gm ON c.id = gm.character_id
LEFT JOIN guilds g ON gm.guild_id = g.id
WHERE c.is_active = TRUE;

-- Guild overview view
CREATE VIEW guild_overview AS
SELECT 
    g.id,
    g.name,
    g.tag,
    g.level,
    g.experience,
    g.treasury_gold,
    g.max_members,
    COUNT(gm.id) as current_members,
    c.name as leader_name,
    g.created_at
FROM guilds g
LEFT JOIN guild_members gm ON g.id = gm.guild_id
LEFT JOIN characters c ON g.leader_id = c.id
WHERE g.is_active = TRUE
GROUP BY g.id, c.name;

-- Trading post listings view
CREATE VIEW trading_listings AS
SELECT 
    tp.id,
    tp.price,
    tp.quantity,
    tp.listing_type,
    tp.description,
    tp.created_at,
    tp.expires_at,
    ii.item_name,
    ii.item_type,
    ii.rarity,
    c.name as seller_name,
    g.name as seller_guild
FROM trading_posts tp
JOIN inventory_items ii ON tp.item_id = ii.id
JOIN inventories inv ON ii.inventory_id = inv.id
JOIN characters c ON inv.character_id = c.id
LEFT JOIN guild_members gm ON c.id = gm.character_id
LEFT JOIN guilds g ON gm.guild_id = g.id
WHERE tp.is_active = TRUE;

-- Arena rankings view
CREATE VIEW arena_rankings_view AS
SELECT 
    ar.id,
    ar.arena_type,
    ar.rating,
    ar.wins,
    ar.losses,
    ar.draws,
    ar.season,
    ar.rank_tier,
    ar.rank_division,
    c.name as character_name,
    p.username as player_name,
    g.name as guild_name
FROM arena_rankings ar
JOIN characters c ON ar.character_id = c.id
JOIN players p ON c.player_id = p.id
LEFT JOIN guild_members gm ON c.id = gm.character_id
LEFT JOIN guilds g ON gm.guild_id = g.id
ORDER BY ar.rating DESC;

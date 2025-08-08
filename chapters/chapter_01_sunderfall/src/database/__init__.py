"""
Chronicles of Ruin: Sunderfall - Database Package
Database initialization and connection management
"""

import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager

# Import all models to ensure they're registered
from .models import (
    Base,
    Player,
    Character,
    Inventory,
    InventoryItem,
    EquippedItem,
    Guild,
    GuildMember,
    GuildRank,
    Alliance,
    AllianceMember,
    Territory,
    PvPMatch,
    ArenaRanking,
    Tournament,
    TournamentParticipant,
    TournamentBracket,
    TradingPost,
    AuctionHouse,
    AuctionBid,
    TradingTransaction,
    ActiveSession,
    CombatLog,
    Party,
    PartyMember,
    UserStat,
    Event,
)

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and sessions"""

    def __init__(self, database_url=None):
        self.database_url = database_url or self._get_database_url()
        self.engine = None
        self.SessionLocal = None
        self._setup_engine()

    def _get_database_url(self):
        """Get database URL from environment or use default"""
        # Check for environment variable
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            return db_url

        # Check for local SQLite file
        db_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "data", "sunderfall.db"
        )
        return f"sqlite:///{db_path}"

    def _setup_engine(self):
        """Setup SQLAlchemy engine with appropriate configuration"""
        if self.database_url.startswith("sqlite"):
            # SQLite configuration for development
            self.engine = create_engine(
                self.database_url,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
                echo=False,  # Set to True for SQL debugging
            )
        else:
            # PostgreSQL configuration for production
            self.engine = create_engine(
                self.database_url, pool_pre_ping=True, pool_recycle=300, echo=False
            )

        # Create session factory
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        # Create scoped session for thread safety
        self.Session = scoped_session(self.SessionLocal)

    def create_tables(self):
        """Create all database tables"""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise

    def drop_tables(self):
        """Drop all database tables (use with caution!)"""
        try:
            Base.metadata.drop_all(bind=self.engine)
            logger.info("Database tables dropped successfully")
        except Exception as e:
            logger.error(f"Failed to drop database tables: {e}")
            raise

    @contextmanager
    def get_session(self):
        """Context manager for database sessions"""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()

    def get_session_direct(self):
        """Get a database session directly (caller must close)"""
        return self.SessionLocal()

    def close_session(self, session):
        """Close a database session"""
        if session:
            session.close()

    def health_check(self):
        """Check database connectivity"""
        try:
            from sqlalchemy import text

            with self.get_session() as session:
                session.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False


# Global database manager instance
db_manager = None


def initialize_database(database_url=None):
    """Initialize the global database manager"""
    global db_manager
    db_manager = DatabaseManager(database_url)
    return db_manager


def get_db_manager():
    """Get the global database manager"""
    if db_manager is None:
        raise RuntimeError(
            "Database not initialized. Call initialize_database() first."
        )
    return db_manager


def get_session():
    """Get a database session using the global manager"""
    return get_db_manager().get_session()


# Convenience functions for common operations
def create_tables():
    """Create all database tables"""
    return get_db_manager().create_tables()


def health_check():
    """Check database health"""
    return get_db_manager().health_check()


# Example usage:
# initialize_database()
# create_tables()
#
# with get_session() as session:
#     # Do database operations
#     pass

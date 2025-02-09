import sqlite3
from datetime import datetime
from contextlib import contextmanager
from config import config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseError(Exception):
    """Custom exception for database operations"""
    pass

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = None
    try:
        conn = sqlite3.connect(config['development'].DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise DatabaseError("Failed to connect to database") from e
    finally:
        if conn:
            conn.close()

def init_db():
    """Initialize the database with required tables"""
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            
            # Drop existing table if it exists
            c.execute('DROP TABLE IF EXISTS high_scores')
            
            # Create new table with updated schema
            c.execute('''
                CREATE TABLE high_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            logger.info("Database initialized successfully")
    except DatabaseError as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

def save_score(player_name: str, score: int) -> None:
    """Save a player's score to the database"""
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute(
                'INSERT INTO high_scores (player_name, score) VALUES (?, ?)',
                (player_name, score)
            )
            conn.commit()
            logger.info(f"Score saved: {player_name} - {score}")
    except DatabaseError as e:
        logger.error(f"Failed to save score: {e}")
        raise

def get_top_scores(limit: int = 20) -> list:
    """Get top scores from the database"""
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute('''
                SELECT player_name, score, date 
                FROM high_scores 
                ORDER BY score DESC 
                LIMIT ?
            ''', (limit,))
            scores = [dict(row) for row in c.fetchall()]
            logger.debug(f"Retrieved {len(scores)} top scores")
            return scores
    except DatabaseError as e:
        logger.error(f"Failed to retrieve top scores: {e}")
        raise

def get_total_players() -> int:
    """Get total number of unique players"""
    try:
        with get_db_connection() as conn:
            c = conn.cursor()
            c.execute('SELECT COUNT(DISTINCT player_name) FROM high_scores')
            count = c.fetchone()[0]
            logger.debug(f"Total unique players: {count}")
            return count
    except DatabaseError as e:
        logger.error(f"Failed to get total players count: {e}")
        raise
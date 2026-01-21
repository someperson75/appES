"""Database management for omniGames."""
import sqlite3
import os
from pathlib import Path
from typing import Optional, Dict, List, Any

DB_PATH = Path(__file__).parent.parent.parent / "omnigames.db"


class Database:
    """SQLite database manager for omniGames."""

    def __init__(self):
        """Initialize database connection."""
        self.db_path = DB_PATH
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
        self.init_db()

    def connect(self) -> None:
        """Connect to database."""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def disconnect(self) -> None:
        """Disconnect from database."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def init_db(self) -> None:
        """Initialize database schema."""
        self.connect()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS game_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                game_name TEXT NOT NULL,
                data TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(user_id, game_name)
            )
        """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS game_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                game_name TEXT NOT NULL,
                high_score INTEGER DEFAULT 0,
                times_played INTEGER DEFAULT 0,
                total_playtime INTEGER DEFAULT 0,
                last_played TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(user_id, game_name)
            )
        """
        )

        self.conn.commit()
        self.disconnect()

    def execute(self, query: str, params: tuple = ()) -> Any:
        """Execute a query."""
        if not self.conn:
            self.connect()
        self.cursor.execute(query, params)
        return self.cursor

    def commit(self) -> None:
        """Commit changes."""
        if self.conn:
            self.conn.commit()

    def fetchone(self) -> Optional[sqlite3.Row]:
        """Fetch one result."""
        if self.cursor:
            return self.cursor.fetchone()
        return None

    def fetchall(self) -> List[sqlite3.Row]:
        """Fetch all results."""
        if self.cursor:
            return self.cursor.fetchall()
        return []

    # User management
    def create_user(self, username: str) -> int:
        """Create a new user. Returns user_id."""
        self.execute("INSERT INTO users (username) VALUES (?)", (username,))
        self.commit()
        return self.cursor.lastrowid

    def get_user(self, username: str) -> Optional[sqlite3.Row]:
        """Get user by username."""
        self.execute("SELECT * FROM users WHERE username = ?", (username,))
        return self.fetchone()

    def get_all_users(self) -> List[sqlite3.Row]:
        """Get all users."""
        self.execute("SELECT * FROM users ORDER BY username")
        return self.fetchall()

    def user_exists(self, username: str) -> bool:
        """Check if user exists."""
        self.execute("SELECT id FROM users WHERE username = ?", (username,))
        return self.fetchone() is not None

    # Game data management
    def save_game_data(self, user_id: int, game_name: str, data: str) -> None:
        """Save or update game data for a user."""
        self.execute(
            """
            INSERT INTO game_data (user_id, game_name, data)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, game_name) DO UPDATE SET data = ?, updated_at = CURRENT_TIMESTAMP
        """,
            (user_id, game_name, data, data),
        )
        self.commit()

    def load_game_data(self, user_id: int, game_name: str) -> Optional[str]:
        """Load game data for a user."""
        self.execute(
            "SELECT data FROM game_data WHERE user_id = ? AND game_name = ?",
            (user_id, game_name),
        )
        result = self.fetchone()
        return result[0] if result else None

    # Game statistics
    def update_game_stats(
        self,
        user_id: int,
        game_name: str,
        high_score: int = None,
        playtime: int = 0,
    ) -> None:
        """Update game statistics for a user."""
        self.execute(
            """
            INSERT INTO game_stats (user_id, game_name, high_score, times_played, total_playtime, last_played)
            VALUES (?, ?, ?, 1, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id, game_name) DO UPDATE SET 
                high_score = MAX(high_score, ?),
                times_played = times_played + 1,
                total_playtime = total_playtime + ?,
                last_played = CURRENT_TIMESTAMP
        """,
            (user_id, game_name, high_score or 0, playtime, high_score or 0, playtime),
        )
        self.commit()

    def get_game_stats(self, user_id: int, game_name: str) -> Optional[sqlite3.Row]:
        """Get game statistics for a user."""
        self.execute(
            "SELECT * FROM game_stats WHERE user_id = ? AND game_name = ?",
            (user_id, game_name),
        )
        return self.fetchone()

    def get_user_game_stats(self, user_id: int) -> List[sqlite3.Row]:
        """Get all game statistics for a user."""
        self.execute(
            "SELECT * FROM game_stats WHERE user_id = ? ORDER BY high_score DESC",
            (user_id,),
        )
        return self.fetchall()


# Global database instance
db = Database()

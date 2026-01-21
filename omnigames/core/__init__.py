"""Core module for omniGames."""
from .database import db, Database
from .config import localization, LocalizationManager, GAMES_PATH, ASSETS_PATH
from .game_manager import game_manager, GameManager

__all__ = [
    "db",
    "Database",
    "localization",
    "LocalizationManager",
    "game_manager",
    "GameManager",
    "GAMES_PATH",
    "ASSETS_PATH",
]

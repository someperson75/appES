"""
Initialization module for omniGames package.
"""
__version__ = "1.0.0"
__author__ = "omniGames Team"

from omnigames.core import db, localization, game_manager

__all__ = ["db", "localization", "game_manager"]

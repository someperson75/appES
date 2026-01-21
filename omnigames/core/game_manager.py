"""Game manager for loading and installing games."""
import os
import json
import shutil
import zipfile
from pathlib import Path
from typing import Dict, List, Optional
from .config import GAMES_PATH

GAME_MANIFEST = "game.json"


class GameManager:
    """Manage game installation and discovery."""

    def __init__(self):
        """Initialize game manager."""
        self.games_path = GAMES_PATH
        self.games_path.mkdir(parents=True, exist_ok=True)

    def get_installed_games(self) -> List[Dict[str, any]]:
        """Get list of installed games."""
        games = []
        for game_dir in self.games_path.iterdir():
            if game_dir.is_dir():
                game_data = self._load_game_manifest(game_dir)
                if game_data:
                    game_data["path"] = str(game_dir)
                    games.append(game_data)
        return sorted(games, key=lambda x: x.get("title", ""))

    def _load_game_manifest(self, game_dir: Path) -> Optional[Dict]:
        """Load game manifest from directory."""
        manifest_path = game_dir / GAME_MANIFEST
        if manifest_path.exists():
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading manifest for {game_dir.name}: {e}")
        return None

    def install_game_from_zip(self, zip_path: str, extract_to: Optional[Path] = None) -> tuple[bool, str]:
        """
        Install a game from ZIP file.
        Returns (success: bool, message: str)
        """
        try:
            zip_path = Path(zip_path)
            if not zip_path.exists():
                return False, "ZIP file not found"

            if not zipfile.is_zipfile(zip_path):
                return False, "Invalid ZIP file"

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                # Find the game manifest in the ZIP
                game_manifest_found = False
                for file in zip_ref.namelist():
                    if file.endswith(GAME_MANIFEST):
                        game_manifest_found = True
                        break

                if not game_manifest_found:
                    return False, f"No {GAME_MANIFEST} found in ZIP"

                # Extract to temp location first
                temp_extract = self.games_path / ".temp_extract"
                if temp_extract.exists():
                    shutil.rmtree(temp_extract)
                temp_extract.mkdir(parents=True, exist_ok=True)

                zip_ref.extractall(temp_extract)

                # Find the game directory (may be nested)
                game_dir = self._find_game_directory(temp_extract)
                if not game_dir:
                    shutil.rmtree(temp_extract)
                    return False, "Could not find game directory in ZIP"

                # Load manifest to get game name
                manifest = self._load_game_manifest(game_dir)
                if not manifest or "name" not in manifest:
                    shutil.rmtree(temp_extract)
                    return False, "Invalid game manifest"

                game_name = manifest["name"]
                final_path = self.games_path / game_name

                # Remove existing game if it exists
                if final_path.exists():
                    shutil.rmtree(final_path)

                # Move from temp to final location
                shutil.move(str(game_dir), str(final_path))
                shutil.rmtree(temp_extract)

                return True, f"Game '{game_name}' installed successfully"

        except Exception as e:
            return False, f"Installation error: {str(e)}"

    def _find_game_directory(self, search_path: Path) -> Optional[Path]:
        """Find directory containing game.json."""
        for root, dirs, files in os.walk(search_path):
            if GAME_MANIFEST in files:
                return Path(root)
        return None

    def get_game_thumbnail(self, game_name: str) -> Optional[Path]:
        """Get path to game thumbnail."""
        game_dir = self.games_path / game_name
        thumbnail_path = game_dir / "assets" / "thumbnail.png"
        if thumbnail_path.exists():
            return thumbnail_path
        return None

    def get_game_main_module(self, game_name: str) -> Optional[str]:
        """Get the main module name for a game."""
        manifest = self._load_game_manifest(self.games_path / game_name)
        if manifest:
            return manifest.get("main_module", "main")
        return None

    def is_game_installed(self, game_name: str) -> bool:
        """Check if a game is installed."""
        game_dir = self.games_path / game_name
        return (game_dir / GAME_MANIFEST).exists()


# Global game manager instance
game_manager = GameManager()

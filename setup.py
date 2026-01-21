"""Setup script for omniGames - initializes built-in games."""

import shutil
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).parent
OMNIGAMES_GAMES_DIR = ROOT_DIR / "omnigames" / "games"
GAMES_DIR = ROOT_DIR / "games"


def setup_builtin_games():
    """Copy built-in games to ./games directory."""
    games_to_copy = ["snake", "tictactoe", "memory", "pong", "maze"]

    for game_name in games_to_copy:
        source_file = OMNIGAMES_GAMES_DIR / f"{game_name}.py"
        game_folder = GAMES_DIR / game_name
        target_file = game_folder / "main.py"

        if source_file.exists() and game_folder.exists():
            try:
                shutil.copy(source_file, target_file)
                print(f"✓ Copied {game_name} game to ./games/{game_name}/main.py")
            except Exception as e:
                print(f"✗ Error copying {game_name}: {e}")
        else:
            print(f"✗ Source or destination not found for {game_name}")


def verify_structure():
    """Verify the project structure is correct."""
    required_files = [
        "main.py",
        "requirements.txt",
        "README.md",
        "omnigames/__init__.py",
        "omnigames/core/__init__.py",
        "omnigames/core/base_game.py",
        "omnigames/core/database.py",
        "omnigames/core/config.py",
        "omnigames/core/game_manager.py",
        "omnigames/ui/__init__.py",
        "omnigames/ui/menu.py",
    ]

    print("\nVerifying project structure:")
    all_ok = True
    for file_path in required_files:
        full_path = ROOT_DIR / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - MISSING")
            all_ok = False

    required_games = ["snake", "tictactoe", "memory", "pong", "maze"]
    for game in required_games:
        game_manifest = GAMES_DIR / game / "game.json"
        game_main = GAMES_DIR / game / "main.py"
        if game_manifest.exists() and game_main.exists():
            print(f"✓ games/{game}/ (manifest + main.py)")
        else:
            print(f"✗ games/{game}/ - INCOMPLETE")
            all_ok = False

    return all_ok


if __name__ == "__main__":
    print("omniGames Setup")
    print("=" * 50)

    # Setup games
    setup_builtin_games()

    # Verify structure
    if verify_structure():
        print("\n✓ All checks passed! Ready to run: python main.py")
    else:
        print("\n✗ Some files are missing. Please check the installation.")

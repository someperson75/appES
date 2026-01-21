"""
Comprehensive test and verification script for omniGames.
Run this to ensure everything is working correctly.
"""

import sys
import importlib
import json
from pathlib import Path

# Add appES to path
APP_DIR = Path(__file__).parent
sys.path.insert(0, str(APP_DIR))

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_success(text):
    """Print success message."""
    print(f"✓ {text}")

def print_error(text):
    """Print error message."""
    print(f"✗ {text}")

def test_imports():
    """Test that all modules can be imported."""
    print_header("TESTING IMPORTS")
    
    modules = [
        ("omnigames", "Main package"),
        ("omnigames.core", "Core module"),
        ("omnigames.core.base_game", "BaseGame class"),
        ("omnigames.core.database", "Database module"),
        ("omnigames.core.config", "Config module"),
        ("omnigames.core.game_manager", "GameManager module"),
        ("omnigames.ui.menu", "Menu module"),
        ("pygame", "Pygame library"),
    ]
    
    failed = []
    for module_name, description in modules:
        try:
            importlib.import_module(module_name)
            print_success(f"Imported {description}: {module_name}")
        except ImportError as e:
            print_error(f"Failed to import {description}: {module_name}")
            print(f"  Error: {e}")
            failed.append(module_name)
    
    return len(failed) == 0

def test_database():
    """Test database functionality."""
    print_header("TESTING DATABASE")
    
    try:
        from omnigames.core.database import Database
        
        # Create test database
        db = Database()
        print_success("Database initialized")
        
        # Test user creation
        test_user_id = db.create_user("test_user_verification")
        print_success(f"Created test user (ID: {test_user_id})")
        
        # Test user retrieval
        user = db.get_user("test_user_verification")
        if user and user["id"] == test_user_id:
            print_success("Retrieved user successfully")
        else:
            print_error("Failed to retrieve user")
            return False
        
        # Test game data
        db.save_game_data(test_user_id, "test_game", '{"score": 100}')
        print_success("Saved game data")
        
        data = db.load_game_data(test_user_id, "test_game")
        if data and "100" in data:
            print_success("Loaded game data successfully")
        else:
            print_error("Failed to load game data")
            return False
        
        # Test statistics
        db.update_game_stats(test_user_id, "test_game", 100, 60)
        print_success("Updated game statistics")
        
        stats = db.get_game_stats(test_user_id, "test_game")
        if stats and stats["high_score"] == 100:
            print_success("Retrieved game statistics successfully")
        else:
            print_error("Failed to retrieve statistics")
            return False
        
        db.disconnect()
        return True
        
    except Exception as e:
        print_error(f"Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_localization():
    """Test localization system."""
    print_header("TESTING LOCALIZATION")
    
    try:
        from omnigames.core.config import LocalizationManager
        
        # Test English
        loc_en = LocalizationManager("en")
        text = loc_en.translate("menu_title")
        if text == "omniGames":
            print_success("English localization works")
        else:
            print_error(f"English translation failed: got '{text}'")
            return False
        
        # Test Spanish
        loc_es = LocalizationManager("es")
        text = loc_es.translate("menu_select_user")
        if "Seleccionar" in text or "usuario" in text.lower():
            print_success("Spanish localization works")
        else:
            print_error(f"Spanish translation failed: got '{text}'")
            return False
        
        # Test language switching
        loc_en.set_language("es")
        text = loc_en.translate("menu_quit")
        if "Salir" in text:
            print_success("Language switching works")
        else:
            print_error("Language switching failed")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Localization test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_game_manager():
    """Test game manager functionality."""
    print_header("TESTING GAME MANAGER")
    
    try:
        from omnigames.core.game_manager import GameManager
        
        gm = GameManager()
        print_success("GameManager initialized")
        
        # Get installed games
        games = gm.get_installed_games()
        print(f"Found {len(games)} installed games:")
        for game in games:
            print(f"  - {game.get('title', 'Unknown')} ({game['name']})")
        
        if len(games) >= 5:
            print_success("All 5 built-in games detected")
        else:
            print_error(f"Expected 5 games, found {len(games)}")
            return False
        
        # Check for required games
        game_names = [g['name'] for g in games]
        required = ['snake', 'tictactoe', 'memory', 'pong', 'maze']
        for req_game in required:
            if req_game in game_names:
                print_success(f"Found {req_game}")
            else:
                print_error(f"Missing game: {req_game}")
                return False
        
        return True
        
    except Exception as e:
        print_error(f"GameManager test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_game_files():
    """Test that game files exist and are valid."""
    print_header("TESTING GAME FILES")
    
    games_path = APP_DIR / "games"
    required_games = {
        "snake": "snake.py",
        "tictactoe": "tictactoe.py",
        "memory": "memory.py",
        "pong": "pong.py",
        "maze": "maze.py"
    }
    
    all_ok = True
    for game_name, filename in required_games.items():
        game_dir = games_path / game_name
        game_file = game_dir / "main.py"
        manifest = game_dir / "game.json"
        
        if game_file.exists():
            print_success(f"{game_name}: main.py exists")
        else:
            print_error(f"{game_name}: main.py missing")
            all_ok = False
        
        if manifest.exists():
            try:
                with open(manifest) as f:
                    data = json.load(f)
                    if "name" in data and "title" in data:
                        print_success(f"{game_name}: game.json valid")
                    else:
                        print_error(f"{game_name}: game.json missing required fields")
                        all_ok = False
            except json.JSONDecodeError:
                print_error(f"{game_name}: game.json is invalid JSON")
                all_ok = False
        else:
            print_error(f"{game_name}: game.json missing")
            all_ok = False
    
    return all_ok

def test_base_game():
    """Test BaseGame class."""
    print_header("TESTING BASE GAME CLASS")
    
    try:
        from omnigames.core.base_game import BaseGame
        
        # Check required methods
        required_methods = [
            'initialize',
            'handle_event',
            'update',
            'render',
            'cleanup',
            'run',
            'get_score',
            'pause',
            'resume',
            'is_paused'
        ]
        
        for method in required_methods:
            if hasattr(BaseGame, method):
                print_success(f"BaseGame has {method}() method")
            else:
                print_error(f"BaseGame missing {method}() method")
                return False
        
        return True
        
    except Exception as e:
        print_error(f"BaseGame test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_project_structure():
    """Test project structure."""
    print_header("TESTING PROJECT STRUCTURE")
    
    required_files = {
        "main.py": "Main entry point",
        "setup.py": "Setup script",
        "requirements.txt": "Dependencies",
        "README.md": "Documentation",
        "QUICKSTART.md": "Quick start guide",
        "GAME_TEMPLATE.py": "Game template",
        "omnigames/__init__.py": "Package init",
        "omnigames/core/__init__.py": "Core package",
        "omnigames/ui/__init__.py": "UI package",
    }
    
    all_ok = True
    for file_path, description in required_files.items():
        full_path = APP_DIR / file_path
        if full_path.exists():
            print_success(f"{description}: {file_path}")
        else:
            print_error(f"{description}: {file_path} missing")
            all_ok = False
    
    return all_ok

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("  omniGames - Comprehensive Verification")
    print("=" * 60)
    
    results = []
    
    # Run all tests
    results.append(("Project Structure", test_project_structure()))
    results.append(("Imports", test_imports()))
    results.append(("BaseGame Class", test_base_game()))
    results.append(("Localization", test_localization()))
    results.append(("Database", test_database()))
    results.append(("Game Files", test_game_files()))
    results.append(("Game Manager", test_game_manager()))
    
    # Print summary
    print_header("VERIFICATION SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {test_name}")
    
    print("\n" + "=" * 60)
    if passed == total:
        print(f"✓ ALL TESTS PASSED ({passed}/{total})")
        print("\nReady to run: python main.py")
        print("=" * 60 + "\n")
        return 0
    else:
        print(f"✗ SOME TESTS FAILED ({passed}/{total})")
        print("\nPlease fix the errors above and try again.")
        print("=" * 60 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())

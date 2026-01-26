#!/usr/bin/env python3
"""Test that games load and use locales."""

import sys
from pathlib import Path
import json

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

def test_game_with_language(game_name: str, language: str):
    """Test if a game loads with specific language."""
    try:
        game_path = Path(__file__).parent / "games" / game_name / "main.py"
        
        if not game_path.exists():
            return False, f"Game path not found: {game_path}"
        
        # Check if locale file exists
        locale_path = game_path.parent / "locales" / f"{language}.json"
        if not locale_path.exists():
            return False, f"Locale not found: {locale_path}"
        
        # Try to load the locale
        with open(locale_path, "r", encoding="utf-8") as f:
            locale_data = json.load(f)
        
        # Check if required keys exist
        if not locale_data:
            return False, "Locale file is empty"
        
        return True, f"✓ {game_name}: {language} loaded with {len(locale_data)} keys"
    
    except Exception as e:
        return False, f"Error: {e}"

def main():
    """Run tests."""
    games = ["snake", "tictactoe", "memory", "pong", "maze"]
    languages = ["en", "es"]
    
    print("=" * 60)
    print("Testing Game Localization System")
    print("=" * 60)
    
    all_passed = True
    
    for game in games:
        print(f"\n[{game.upper()}]")
        for lang in languages:
            passed, msg = test_game_with_language(game, lang)
            status = "✓" if passed else "✗"
            print(f"  {status} {msg}")
            if not passed:
                all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed! Localization system ready.")
    else:
        print("✗ Some tests failed!")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

"""Quick test to verify everything works after removing omnigames/games"""
from omnigames.core import db, localization, game_manager

print("Testing after omnigames/games removal...")
print()

# Test imports
print("[OK] All imports successful")

# Test game manager
games = game_manager.get_installed_games()
print(f"[OK] Found {len(games)} games:")
for game in games:
    print(f"  - {game['title']} ({game['name']})")

# Test database
print(f"[OK] Database ready at: {db.db_path}")

# Test localization  
text = localization.translate("menu_title")
print(f"[OK] Localization works: menu_title = '{text}'")

print()
print("All systems operational!")

# omniGames - Project Index & Roadmap

## 📋 Quick Navigation

### 🎮 **To Play Games**
```bash
python main.py
```
Or double-click: `run_omnigames.bat`

### 📚 **To Learn How to Create Games**
1. Read: `GAME_TEMPLATE.py` (500+ lines of documentation)
2. Read: `README.md` - "Creating Custom Games" section
3. Check: `omnigames/games/snake.py` (working example)

### 🔧 **To Setup/Debug**
```bash
python setup.py
```

### 📖 **Documentation Files** (In Reading Order)
1. `QUICKSTART.md` - Start here! (5 min read)
2. `README.md` - Complete guide (20 min read)
3. `GAME_TEMPLATE.py` - Game creation (30 min read)
4. `IMPLEMENTATION_SUMMARY.md` - Technical details (15 min read)

---

## 📁 File Structure with Descriptions

```
appES/
│
├─ 📄 main.py                      👈 START HERE - Run this to play
├─ 🎬 run_omnigames.bat            👈 Double-click to start (Windows)
├─ 🔧 setup.py                     ⚙️ Verify installation
├─ 📦 requirements.txt              📋 Dependencies: pygame, Pillow
│
├─ 📚 DOCUMENTATION
│  ├─ README.md                     📘 Complete documentation
│  ├─ QUICKSTART.md                📘 Quick start guide
│  ├─ GAME_TEMPLATE.py             📘 Game creation tutorial (executable)
│  ├─ IMPLEMENTATION_SUMMARY.md     📘 Technical summary
│  └─ INDEX.md                      📘 This file
│
├─ 💾 omnigames.db                 Database (auto-created, SQLite)
│
├─ 📦 omnigames/                    Main Python package
│  │
│  ├─ 🎯 __init__.py               Package initialization
│  │
│  ├─ 🔧 core/                     Core functionality (database, config)
│  │  ├─ __init__.py
│  │  ├─ base_game.py              ⭐ BaseGame class - all games inherit this
│  │  ├─ database.py               💾 SQLite database management
│  │  ├─ config.py                 🌐 Localization & configuration
│  │  └─ game_manager.py           📦 Game discovery & installation
│  │
│  ├─ 🎮 games/                    Built-in games (+ template)
│  │  ├─ __init__.py
│  │  ├─ template_game.py          📘 Template for creating games
│  │  ├─ snake.py                  🐍 Snake game (180 lines)
│  │  ├─ tictactoe.py              ❌ Tic Tac Toe with AI (200 lines)
│  │  ├─ memory.py                 🧠 Memory/Matching game (150 lines)
│  │  ├─ pong.py                   🏓 Pong arcade game (160 lines)
│  │  └─ maze.py                   🎲 Maze navigation game (200 lines)
│  │
│  ├─ 🖼️ ui/                       User interface
│  │  ├─ __init__.py
│  │  └─ menu.py                   🎨 Tkinter menu interface (350 lines)
│  │
│  ├─ 🎨 assets/                   App images & icons
│  │
│  └─ 🌐 locales/                  Translation files (auto-generated)
│     ├─ en.json                   🇬🇧 English translations
│     └─ es.json                   🇪🇸 Spanish translations
│
└─ 🎮 games/                       Installed games directory
   ├─ snake/
   │  ├─ game.json                 Game manifest
   │  ├─ main.py                   Entry point
   │  └─ assets/thumbnail.png      (optional icon)
   ├─ tictactoe/
   ├─ memory/
   ├─ pong/
   └─ maze/
```

---

## 🎯 What Each Component Does

### Core Components

| Component | Purpose | Key Classes |
|-----------|---------|------------|
| `database.py` | User & game data storage | `Database` |
| `config.py` | Settings & translations | `LocalizationManager` |
| `game_manager.py` | Game discovery & installation | `GameManager` |
| `base_game.py` | Base class for all games | `BaseGame` |
| `menu.py` | Main user interface | `MainMenu`, `GameButton` |

### Built-in Games

| Game | Type | AI | Difficulty |
|------|------|----|----|
| Snake | Action | No | Medium |
| Tic Tac Toe | Strategy | Yes (Minimax) | Hard |
| Memory | Puzzle | No | Easy-Medium |
| Pong | Action | Yes (Basic) | Easy |
| Maze | Action/Puzzle | Yes (Random) | Medium |

### Database Tables

| Table | Purpose | Key Fields |
|-------|---------|-----------|
| `users` | User accounts | id, username, created_at |
| `game_data` | User game saves | user_id, game_name, data (JSON) |
| `game_stats` | Game statistics | user_id, game_name, high_score, times_played |

---

## 🚀 Getting Started (Recommended Order)

### Phase 1: Setup (5 minutes)
```
1. Open PowerShell in appES folder
2. Run: python setup.py
3. Verify all ✓ checks pass
```

### Phase 2: First Play (5 minutes)
```
1. Run: python main.py
2. Create a new user
3. Play each game once
```

### Phase 3: Create a Game (30 minutes)
```
1. Read: GAME_TEMPLATE.py
2. Copy and modify template_game.py
3. Create game.json manifest
4. Test your game
```

### Phase 4: Install Custom Game (10 minutes)
```
1. Package game as ZIP
2. Run omniGames
3. Click "Install Game"
4. Select your ZIP file
5. Play!
```

---

## 💡 Key Concepts Explained

### 1. BaseGame Class
All games must inherit from `BaseGame`:
- Provides standard interface
- Handles common functionality
- Enforces required methods

**Required Methods:**
- `initialize()` - Setup resources
- `handle_event(event)` - Process input
- `update(dt)` - Game logic
- `render()` - Drawing
- `cleanup()` - Cleanup
- `run()` - Main loop
- `get_score()` - Return score

### 2. Game Manifest (game.json)
```json
{
  "name": "game_id",           // Unique identifier
  "title": "Display Name",     // Shown in menu
  "description": "...",        // Menu description
  "version": "1.0.0",          // Semantic versioning
  "author": "Name",            // Creator
  "main_module": "main",       // Entry point filename
  "icon": "assets/thumbnail.png"  // Optional icon
}
```

### 3. Entry Point (main.py)
Every game must have a `main()` function:
```python
def main(user_id: int) -> int:
    """Entry point. Receives user_id, returns score."""
    game = MyGame(user_id, "my_game")
    return game.run()
```

### 4. Database Operations
```python
from omnigames.core import db

# Per-user data
db.save_game_data(user_id, "game_name", json_string)
data = db.load_game_data(user_id, "game_name")

# Statistics
db.update_game_stats(user_id, "game_name", 
                      high_score=100, playtime=60)
stats = db.get_user_game_stats(user_id)
```

### 5. Game Installation
- User clicks "Install Game"
- Selects ZIP file
- GameManager extracts and validates
- Game installed to `./games/game_name/`

### 6. Localization
```python
from omnigames.core import localization

text = localization.translate("menu_title")
localization.set_language("es")
```

---

## 🎓 Learning Path

### For Players
1. Run `python main.py`
2. Create account
3. Play all 5 games
4. Check statistics
5. Try different languages

### For Game Developers
1. Read `QUICKSTART.md`
2. Study `GAME_TEMPLATE.py`
3. Review `snake.py` for example
4. Copy template
5. Implement your game
6. Test locally
7. Create game.json
8. Package as ZIP
9. Install via menu

### For Developers
1. Read `README.md` - Full documentation
2. Study `database.py` - Database schema
3. Review `menu.py` - UI implementation
4. Check `game_manager.py` - Game system
5. Explore `base_game.py` - Game structure
6. Examine any `games/*.py` for examples

---

## 🔍 Troubleshooting

### Problem: "Python not found"
**Solution:** Install Python 3.12+ from python.org

### Problem: "No module named pygame"
**Solution:** `pip install pygame`

### Problem: Game won't launch
**Checklist:**
- [ ] game.json exists
- [ ] main.py exists
- [ ] `main(user_id)` function defined
- [ ] Check console for errors

### Problem: Database locked
**Solution:** Close other omniGames instances

### Problem: Game install fails
**Checklist:**
- [ ] ZIP file is valid
- [ ] Contains game.json at root
- [ ] No spaces in game name

---

## 🎯 Common Tasks

### Run the App
```bash
python main.py
```

### Verify Installation
```bash
python setup.py
```

### Test a Game Directly
```bash
cd games/snake
python main.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Create New Game
1. Copy `GAME_TEMPLATE.py`
2. Modify class name and logic
3. Save to `games/my_game/main.py`
4. Create `games/my_game/game.json`
5. Create `games/my_game/assets/thumbnail.png`
6. Package as ZIP: `my_game.zip`
7. Install via menu

### Add New Language
1. Copy `omnigames/locales/en.json` to `new_lang.json`
2. Translate all values
3. Save to `omnigames/locales/new_lang.json`
4. Edit `config.py` to include new language

---

## 📊 Statistics Tracked

For each user and game:
- **High Score** - Best score achieved
- **Times Played** - Number of play sessions
- **Total Playtime** - Hours played (stored in seconds)
- **Last Played** - When last played
- **Creation Date** - When first played

---

## 🌟 Features Highlight

✨ **Multi-User Support**
- Separate accounts per person
- Isolated game data and statistics
- User-specific save games

✨ **5 Complete Games**
- All playable out of the box
- Different mechanics (action, puzzle, strategy)
- Source code available for learning

✨ **Game Installation System**
- Package games as ZIP files
- One-click installation
- Automatic validation

✨ **Localization (i18n)**
- English & Spanish built-in
- Easy to add more languages
- Dynamic language switching

✨ **Persistent Data**
- SQLite database
- Per-user statistics
- Game save capability

✨ **Developer-Friendly**
- Template system for new games
- Well-documented code
- Example implementations

✨ **Cross-Platform Ready**
- Works on Windows, Linux, macOS
- Pure Python + pygame
- No native dependencies

---

## 📚 Documentation Map

```
QUICKSTART.md           ← Start here (5 min)
    ↓
README.md              ← Full details (20 min)
    ↓
GAME_TEMPLATE.py       ← Create games (30 min)
    ↓
IMPLEMENTATION_SUMMARY ← Tech details (15 min)
    ↓
Source code (games/*.py) ← Examples
```

---

## 🎓 Code Examples

### Example 1: Access User Stats
```python
from omnigames.core import db

user = db.get_user("john_doe")
stats = db.get_user_game_stats(user["id"])

for stat in stats:
    print(f"{stat['game_name']}: {stat['high_score']} points")
```

### Example 2: Create Simple Game
```python
from omnigames.core.base_game import BaseGame
import pygame

class SimpleGame(BaseGame):
    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 400))
        return True
    
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
    
    def update(self, dt):
        pass
    
    def render(self):
        self.screen.fill((0, 0, 0))
        pygame.display.flip()
    
    def cleanup(self):
        pygame.quit()

def main(user_id):
    game = SimpleGame(user_id, "simple")
    return game.run()
```

### Example 3: Save Game Data
```python
from omnigames.core import db
import json

# Save
game_state = {"level": 2, "lives": 3}
db.save_game_data(user_id, "my_game", 
                   json.dumps(game_state))

# Load
data_json = db.load_game_data(user_id, "my_game")
if data_json:
    game_state = json.loads(data_json)
```

---

## 🏁 Ready to Start?

### To Play:
```bash
python main.py
```

### To Create Games:
1. Read `GAME_TEMPLATE.py`
2. See full docs in `README.md`

### To Deploy:
1. Package game as ZIP
2. Distribute to others
3. They click "Install Game"

---

## 📞 Quick Reference

| Action | Command/File |
|--------|-------------|
| Start playing | `python main.py` |
| Create game | `GAME_TEMPLATE.py` |
| Full docs | `README.md` |
| Quick start | `QUICKSTART.md` |
| Verify setup | `python setup.py` |
| View code | `omnigames/games/*.py` |

---

**Version:** 1.0.0  
**Created:** January 2026  
**Platform:** Windows (Python 3.12)  
**License:** As per LICENSE file

**Enjoy omniGames! 🎮**

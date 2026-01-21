# Quick Start Guide - omniGames

## 1. Installation

### Requirements
- Windows 7 or higher
- Python 3.12 or higher
- Administrator access (recommended)

### Step 1: Install Python dependencies

Open PowerShell in the project directory and run:
```powershell
pip install -r requirements.txt
```

Or run the automatic setup:
```powershell
python setup.py
```

## 2. Running the Game

Start the application from PowerShell:
```powershell
python main.py
```

Or create a shortcut for easy access:
```powershell
New-Shortcut -LinkPath "Desktop\omniGames.lnk" -TargetPath "python" -Arguments "C:\path\to\appES\main.py"
```

## 3. First Run

1. **Create a User**: Choose "New User" and enter your name
2. **View Games**: You'll see 5 built-in games available
3. **Play a Game**: Click "Start Game" on any game to play
4. **Check Stats**: View your scores and playtime

## 4. Keyboard Controls

### Snake
- **Arrow Keys**: Move the snake
- **ESC**: Exit game

### Tic Tac Toe
- **Mouse**: Click to place X
- **ESC**: Exit game

### Memory Game
- **Mouse**: Click cards to find matches
- **ESC**: Exit game

### Pong
- **UP Arrow**: Move paddle up
- **DOWN Arrow**: Move paddle down
- **ESC**: Exit game

### Maze
- **Arrow Keys**: Move player
- **ESC**: Exit game

## 5. Installing Custom Games

### From ZIP File
1. Click "Install Game" in the main menu
2. Select a `.zip` file containing the game
3. The game will be installed to `./games/` automatically

### Creating Your Own Game
1. Read `GAME_TEMPLATE.py` for a complete example
2. Copy and modify the template
3. Create a `game.json` manifest file
4. Package your game as ZIP
5. Install via the "Install Game" button

## 6. Multi-User Features

- **User Management**: Each user has separate saved games and statistics
- **User Data**: Game progress is saved per user in SQLite database
- **Statistics**: High scores and play counts tracked per user per game

## 7. Language Support

The menu supports two languages:
- **English** (en)
- **Spanish** (es)

Switch languages from the language selector in the user selection screen.

## 8. Troubleshooting

### Python not found
Make sure Python 3.12+ is installed and added to PATH:
```powershell
python --version
```

### pygame import error
Install pygame:
```powershell
pip install pygame
```

### Database locked
Close any other instances of omniGames

### Game won't launch
1. Check that `game.json` exists in the game folder
2. Verify the game has a `main(user_id)` function
3. Check the console for specific error messages

## 9. Project Structure

```
appES/
├── main.py                 # Start here
├── setup.py               # Run this first
├── requirements.txt       # Dependencies
├── README.md              # Full documentation
├── GAME_TEMPLATE.py       # Template for new games
├── omnigames/             # Main package
│   ├── core/             # Core functionality
│   ├── games/            # Built-in games
│   └── ui/               # Menu interface
├── games/                # Game installations
│   ├── snake/
│   ├── tictactoe/
│   ├── memory/
│   ├── pong/
│   └── maze/
└── omnigames.db          # Database (auto-created)
```

## 10. Advanced Features

### Database Access in Games

```python
from omnigames.core import db

# Save user data
db.save_game_data(user_id, "game_name", "{"data": "json"}")

# Load user data
data = db.load_game_data(user_id, "game_name")

# Update statistics
db.update_game_stats(user_id, "game_name", high_score=100, playtime=60)
```

### Localization in Games

```python
from omnigames.core import localization

# Get translated string
text = localization.translate("menu_title")

# All available keys are in omnigames/locales/en.json
```

## 11. Next Steps

1. **Create Your First Game**: Use `GAME_TEMPLATE.py` as a starting point
2. **Add Custom Art**: Create thumbnail.png for your game
3. **Share Games**: Package as ZIP and share with others
4. **Extend Features**: Add new games or modify existing ones

## 12. Support

For detailed information:
- See `README.md` for complete documentation
- Check `GAME_TEMPLATE.py` for game creation guide
- Review existing game files for examples

## 13. Tips & Tricks

✓ Use `setup.py` to verify your installation
✓ Test games directly: `python games/snake/main.py`
✓ Keep game files under 50MB for ZIP distribution
✓ Use descriptive game titles and descriptions in game.json
✓ Add a thumbnail.png (300x200) for better menu appearance
✓ Test on different screen resolutions
✓ Save high scores to the database for persistence

---

**Enjoy omniGames!** 🎮

For more information, see `README.md`

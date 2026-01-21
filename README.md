# omniGames - Multi-User Game Launcher

A comprehensive game launcher platform for Windows built with Python 3.12. Play multiple games with per-user score tracking, game installation, and multi-language support.

## Features

✅ **Multi-User Support** - Multiple users on the same computer with individual game data and statistics
✅ **5 Built-in Games** - Snake, Tic Tac Toe, Memory, Pong, and Maze games
✅ **Game Installation** - Install new games from ZIP files
✅ **Bilingual Interface** - English and Spanish language support
✅ **User Statistics** - Track high scores, play count, and playtime per user
✅ **Game Template** - Template system for creating custom games
✅ **Database Storage** - SQLite database for persistent user and game data

## Installation

### Prerequisites

- Python 3.12 or higher
- Windows (or Linux/macOS with pygame support)

### Setup

1. Navigate to the project directory:
```bash
cd appES
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the main menu:
```bash
python main.py
```

This launches the omniGames menu where you can:
- Select or create a user
- Play installed games
- Install new games from ZIP files
- View your statistics
- Change language (English/Spanish)

## Game Structure

Games are organized in the `./games` folder:
```
./games/
├── snake/
│   ├── game.json          # Game manifest
│   ├── main.py            # Entry point
│   └── assets/
│       └── thumbnail.png  # Game icon (optional)
├── tictactoe/
├── memory/
├── pong/
└── maze/
```

## Game Manifest (game.json)

Every game requires a `game.json` file:
```json
{
  "name": "game_id",
  "title": "Game Title",
  "description": "Game description",
  "version": "1.0.0",
  "author": "Your Name",
  "main_module": "main",
  "icon": "assets/thumbnail.png"
}
```

## Creating Custom Games

### Using the Template

1. Copy the template from `omnigames/games/template_game.py`
2. Create a new folder in `./games/your_game/`
3. Implement the BaseGame class:

```python
from omnigames.core.base_game import BaseGame
import pygame

class YourGame(BaseGame):
    def initialize(self) -> bool:
        """Initialize game resources"""
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        return True
    
    def handle_event(self, event):
        """Handle input events"""
        pass
    
    def update(self, dt: float):
        """Update game logic"""
        pass
    
    def render(self):
        """Draw the game"""
        pygame.display.flip()
    
    def cleanup(self):
        """Clean up resources"""
        pygame.quit()
    
    def run(self) -> int:
        """Main game loop - returns final score"""
        # Implement your main loop
        pass

def main(user_id: int) -> int:
    """Entry point - must accept user_id and return score"""
    game = YourGame(user_id, "your_game")
    return game.run()
```

4. Create `game.json` manifest in your game folder
5. Package as ZIP: `your_game.zip`
6. Use "Install Game" to add it to omniGames

## Built-in Games

### Snake
- Classic snake gameplay
- Eat food to grow and earn points
- Avoid walls and yourself

### Tic Tac Toe
- Play against AI opponent
- AI uses minimax algorithm
- Win, lose, or draw

### Memory Game
- Match pairs of numbered cards
- 4x4 grid (16 cards, 8 pairs)
- Score based on moves

### Pong
- Classic arcade pong
- Play against AI
- First to 5 wins

### Maze
- Navigate a procedurally generated maze
- Collect pellets for points
- Avoid ghosts (enemies)

## Database Structure

The app uses SQLite with three main tables:

- **users** - Stores username and creation date
- **game_data** - Stores per-user game save data (JSON format)
- **game_stats** - Tracks high scores, play count, and playtime

Data is automatically managed and isolated per user.

## File Structure

```
appES/
├── main.py                    # Entry point
├── requirements.txt           # Python dependencies
├── omnigames.db              # SQLite database (auto-created)
├── omnigames/
│   ├── __init__.py
│   ├── core/
│   │   ├── base_game.py      # Base class for all games
│   │   ├── database.py       # Database management
│   │   ├── config.py         # Configuration & localization
│   │   ├── game_manager.py   # Game installation & discovery
│   │   └── __init__.py
│   ├── games/
│   │   ├── snake.py
│   │   ├── tictactoe.py
│   │   ├── memory.py
│   │   ├── pong.py
│   │   ├── maze.py
│   │   ├── template_game.py  # Game template
│   │   └── __init__.py
│   ├── ui/
│   │   ├── menu.py           # Main menu interface
│   │   └── __init__.py
│   ├── assets/               # App assets
│   └── locales/
│       ├── en.json           # English translations
│       └── es.json           # Spanish translations
└── games/                     # Installed games directory
    ├── snake/
    ├── tictactoe/
    ├── memory/
    ├── pong/
    └── maze/
```

## Installing Games from ZIP

Games can be packaged and installed as ZIP files:

1. Structure your game folder:
```
my_game/
├── game.json
├── main.py
└── assets/
    └── thumbnail.png
```

2. Create ZIP file:
```bash
# Windows PowerShell
Compress-Archive -Path my_game -DestinationPath my_game.zip
```

3. Use "Install Game" in the menu to install

## Localization

The app supports English and Spanish. Translations are stored in `omnigames/locales/`:
- `en.json` - English
- `es.json` - Spanish

To add more languages, create a new JSON file with the same keys.

## Game API Reference

### BaseGame Class

All games must inherit from `BaseGame`:

```python
class BaseGame(ABC):
    def initialize(self) -> bool: ...     # Initialize resources
    def handle_event(self, event): ...    # Handle input
    def update(self, dt: float): ...      # Update logic
    def render(self): ...                 # Draw/render
    def cleanup(self): ...                # Cleanup resources
    def get_score(self) -> int: ...       # Return score
    def pause(self): ...                  # Pause game
    def resume(self): ...                 # Resume game
    def run(self) -> int: ...             # Main loop
```

### Database API

```python
from omnigames.core import db

# User management
db.create_user(username)
db.get_user(username)
db.user_exists(username)
db.get_all_users()

# Game data
db.save_game_data(user_id, game_name, data_json)
db.load_game_data(user_id, game_name)

# Statistics
db.update_game_stats(user_id, game_name, high_score, playtime)
db.get_game_stats(user_id, game_name)
db.get_user_game_stats(user_id)
```

### Localization API

```python
from omnigames.core import localization

# Get translated string
text = localization.translate("menu_title")

# Change language
localization.set_language("es")

# Get available languages
langs = localization.get_available_languages()
```

## Troubleshooting

### ImportError: No module named 'pygame'
Install pygame: `pip install pygame`

### Database locked
Close any other instances of omniGames

### Game won't launch
- Check game.json exists and is valid
- Verify main.py has a `main(user_id)` function
- Check console for specific error messages

## Version History

### v1.0.0
- Initial release
- 5 built-in games
- Multi-user support
- Bilingual interface
- Game installation system

## License

This project is provided as-is for educational and personal use.

## Support

For issues or feature requests, refer to the GitHub repository.

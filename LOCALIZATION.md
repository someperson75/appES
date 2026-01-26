# Game Localization System

## Overview

Each game now has its own localization files supporting English and Spanish. The menu displays a warning icon (⚠) when a selected language is not available for a game.

## Structure

Each game folder now contains:
```
games/
├── snake/
│   ├── locales/
│   │   ├── en.json    # English localization
│   │   └── es.json    # Spanish localization
│   ├── main.py
│   └── game.json
├── tictactoe/
│   ├── locales/
│   │   ├── en.json
│   │   └── es.json
│   ├── main.py
│   └── game.json
├── memory/
│   ├── locales/
│   │   ├── en.json
│   │   └── es.json
│   ├── main.py
│   └── game.json
├── pong/
│   ├── locales/
│   │   ├── en.json
│   │   └── es.json
│   ├── main.py
│   └── game.json
└── maze/
    ├── locales/
    │   ├── en.json
    │   └── es.json
    ├── main.py
    └── game.json
```

## Menu Features

### Language Support Detection
- The menu automatically loads game localization files
- Checks if the current language (set in omniGames menu) is available for each game
- Displays a yellow warning icon (**⚠**) next to game titles when language is not available

### Language Warning Dialog
- If you try to launch a game with an unsupported language:
  - A warning dialog appears: "Warning: This game does not support '[language]' language. It will use English instead."
  - You can click **Yes** to continue (game will default to English)
  - You can click **No** to cancel

### Language Selection
- Language can ONLY be changed in the **omniGames menu** (top-left corner)
- Games cannot change language internally - they run in the language selected from the menu
- If selected language isn't available for a game, it falls back to English

## Localization Keys Per Game

### Snake Game (6 keys)
- `game_title`: "Snake Game" / "Juego Snake"
- `game_description`: "Classic Snake arcade game"
- `score`: "Score" / "Puntuación"
- `game_over`: "GAME OVER" / "JUEGO TERMINADO"
- `restart`: "Press SPACE to restart"
- `escape`: "Press ESC to exit"

### Tic Tac Toe (8 keys)
- `game_title`, `game_description`
- `your_turn`: "Your turn (X)" / "Tu turno (X)"
- `you_won`: "You Won!" / "¡Ganaste!"
- `ai_won`: "AI Won!" / "¡IA Ganó!"
- `draw`: "Draw!" / "¡Empate!"
- `restart`, `escape`

### Memory Game (7 keys)
- `game_title`, `game_description`
- `score`, `moves`: "Score" / "Moves" (Puntuación / Movimientos)
- `you_won`: "YOU WON!" / "¡GANASTE!"
- `restart`, `escape`

### Pong (6 keys)
- `game_title`, `game_description`
- `you_won`: "YOU WON!" / "¡GANASTE!"
- `you_lost`: "YOU LOST!" / "¡PERDISTE!"
- `restart`, `escape`

### Maze Game (7 keys)
- `game_title`, `game_description`
- `score`
- `you_won`: "YOU WON!" / "¡GANASTE!"
- `caught`: "CAUGHT!" / "¡ATRAPADO!"
- `restart`, `escape`

## How It Works

1. **Menu.py GameButton Class**
   - Loads game locales when button is created
   - Calls `_load_game_locales()` to read JSON files from `games/{game}/locales/`
   - Calls `_language_available()` to check if current language exists for game
   - Shows ⚠ icon if language unavailable

2. **Language Fallback**
   - If game doesn't support selected language, user is warned
   - Games default to English if their locale file is missing

3. **No Language Change in Games**
   - Games do NOT have language-switching UI
   - All text is rendered in the language selected in omniGames menu
   - If that language isn't available, it defaults to English

## Adding New Languages

To add a new language (e.g., French):

1. Add new locale files to omnigames/locales/:
   ```
   omnigames/locales/fr.json
   ```

2. Add same language to each game:
   ```
   games/{game}/locales/fr.json
   ```

3. Update menu.py language dropdown to include the new language code

## Testing

Run `test_locales.py` to verify all game locales are correctly loaded:
```bash
python test_locales.py
```

Expected output:
```
[snake] EN:True ES:True FR:False
[tictactoe] EN:True ES:True FR:False
[memory] EN:True ES:True FR:False
[pong] EN:True ES:True FR:False
[maze] EN:True ES:True FR:False
```

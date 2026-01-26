#!/usr/bin/env python3
"""Quick test of game locales system."""

import sys
sys.path.insert(0, '.')

print("Testing menu with game locales...")
from pathlib import Path
import json

# Test loading locales
games = ['snake', 'tictactoe', 'memory', 'pong', 'maze']
for game in games:
    game_path = Path(f'games/{game}')
    locales_path = game_path / 'locales'
    locales = {}

    if locales_path.exists():
        for lang_file in locales_path.glob('*.json'):
            lang = lang_file.stem
            with open(lang_file, 'r', encoding='utf-8') as f:
                locales[lang] = json.load(f)

    en_ok = 'en' in locales
    es_ok = 'es' in locales
    fr_ok = 'fr' in locales
    
    print(f"[{game}] EN:{en_ok} ES:{es_ok} FR:{fr_ok}")

print()
print("=== Menu localization system ready ===")

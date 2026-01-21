"""Configuration and localization for omniGames."""
import json
from pathlib import Path
from typing import Dict, Any

LOCALES_PATH = Path(__file__).parent.parent / "locales"
GAMES_PATH = Path(__file__).parent.parent.parent / "games"  # games/ folder at same level as omnigames/
ASSETS_PATH = Path(__file__).parent.parent / "assets"


class LocalizationManager:
    """Manage game localization."""

    def __init__(self, language: str = "en"):
        """Initialize localization manager."""
        self.language = language
        self.translations: Dict[str, Dict[str, str]] = {}
        self.load_translations()

    def load_translations(self) -> None:
        """Load translation files."""
        # Create locale files if they don't exist
        self._ensure_locale_files()

        locale_file = LOCALES_PATH / f"{self.language}.json"
        if locale_file.exists():
            with open(locale_file, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        else:
            self.translations = {}

    def _ensure_locale_files(self) -> None:
        """Ensure locale files exist."""
        LOCALES_PATH.mkdir(parents=True, exist_ok=True)

        en_translations = {
            "menu_title": "omniGames",
            "menu_select_user": "Select User",
            "menu_new_user": "New User",
            "menu_start_game": "Start Game",
            "menu_install_game": "Install Game",
            "menu_quit": "Quit",
            "menu_user_stats": "User Stats",
            "menu_settings": "Settings",
            "language": "Language",
            "username": "Username",
            "confirm": "Confirm",
            "cancel": "Cancel",
            "back": "Back",
            "close": "Close",
            "error": "Error",
            "success": "Success",
            "loading": "Loading...",
            "please_wait": "Please wait...",
            "user_created": "User created successfully",
            "game_installed": "Game installed successfully",
            "invalid_zip": "Invalid or corrupted ZIP file",
            "game_not_found": "Game not found",
            "high_score": "High Score",
            "times_played": "Times Played",
            "total_playtime": "Total Playtime",
            "exit_game": "Exit Game",
            "game_paused": "Game Paused",
            "resume": "Resume",
            "no_games": "No games installed",
            "install_first": "Install a game to get started",
            "enter_username": "Enter username",
            "select_zip": "Select ZIP file to install",
            "installing": "Installing game...",
        }

        es_translations = {
            "menu_title": "omniGames",
            "menu_select_user": "Seleccionar Usuario",
            "menu_new_user": "Nuevo Usuario",
            "menu_start_game": "Iniciar Juego",
            "menu_install_game": "Instalar Juego",
            "menu_quit": "Salir",
            "menu_user_stats": "Estadísticas",
            "menu_settings": "Configuración",
            "language": "Idioma",
            "username": "Nombre de usuario",
            "confirm": "Confirmar",
            "cancel": "Cancelar",
            "back": "Atrás",
            "close": "Cerrar",
            "error": "Error",
            "success": "Éxito",
            "loading": "Cargando...",
            "please_wait": "Por favor espera...",
            "user_created": "Usuario creado exitosamente",
            "game_installed": "Juego instalado exitosamente",
            "invalid_zip": "Archivo ZIP inválido o corrupto",
            "game_not_found": "Juego no encontrado",
            "high_score": "Puntuación Máxima",
            "times_played": "Veces Jugado",
            "total_playtime": "Tiempo Total de Juego",
            "exit_game": "Salir del Juego",
            "game_paused": "Juego en Pausa",
            "resume": "Reanudar",
            "no_games": "No hay juegos instalados",
            "install_first": "Instala un juego para comenzar",
            "enter_username": "Ingresa nombre de usuario",
            "select_zip": "Selecciona archivo ZIP para instalar",
            "installing": "Instalando juego...",
        }

        for lang, translations in [("en", en_translations), ("es", es_translations)]:
            locale_file = LOCALES_PATH / f"{lang}.json"
            if not locale_file.exists():
                with open(locale_file, "w", encoding="utf-8") as f:
                    json.dump(translations, f, ensure_ascii=False, indent=2)

    def set_language(self, language: str) -> None:
        """Set active language."""
        self.language = language
        self.load_translations()

    def translate(self, key: str, default: str = "") -> str:
        """Get translated string."""
        return self.translations.get(key, default or key)

    def get_available_languages(self) -> list:
        """Get list of available languages."""
        return ["en", "es"]


# Global localization instance
localization = LocalizationManager("en")

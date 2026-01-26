"""Main menu UI for omniGames."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import json
from typing import Optional, Callable
import importlib.util
import sys

from omnigames.core import db, localization, game_manager


class GameButton:
    """Custom button widget for displaying games."""

    def __init__(self, parent, game_data: dict, callback: Callable, current_language: str = "en"):
        """Initialize game button."""
        self.frame = tk.Frame(parent, bg="#2a2a2a", relief=tk.RAISED, bd=1)
        self.frame.pack(fill=tk.X, padx=5, pady=5)

        self.game_data = game_data
        self.callback = callback
        self.current_language = current_language
        self.game_locales = self._load_game_locales()

        # Game info
        info_frame = tk.Frame(self.frame, bg="#2a2a2a")
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Title with language warning icon
        title_frame = tk.Frame(info_frame, bg="#2a2a2a")
        title_frame.pack(anchor=tk.W)

        title = tk.Label(
            title_frame, text=game_data.get("title", "Unknown"), font=("Arial", 14, "bold"), fg="white", bg="#2a2a2a"
        )
        title.pack(side=tk.LEFT)

        # Language warning icon
        if not self._language_available():
            warning = tk.Label(
                title_frame, text="⚠", font=("Arial", 14, "bold"), fg="yellow", bg="#2a2a2a"
            )
            warning.pack(side=tk.LEFT, padx=5)

        desc = tk.Label(
            info_frame,
            text=game_data.get("description", ""),
            font=("Arial", 10),
            fg="#cccccc",
            bg="#2a2a2a",
            wraplength=300,
        )
        desc.pack(anchor=tk.W)

        # Play button
        btn = tk.Button(
            self.frame, text=localization.translate("menu_start_game"), command=self._play, font=("Arial", 12), bg="#0066cc", fg="white"
        )
        btn.pack(side=tk.RIGHT, padx=10, pady=10)

    def _load_game_locales(self) -> dict:
        """Load locales for the game."""
        game_path = Path(self.game_data["path"])
        locales_path = game_path / "locales"
        locales = {}

        if locales_path.exists():
            for lang_file in locales_path.glob("*.json"):
                lang = lang_file.stem
                try:
                    with open(lang_file, "r", encoding="utf-8") as f:
                        locales[lang] = json.load(f)
                except Exception:
                    pass

        return locales

    def _language_available(self) -> bool:
        """Check if current language is available for this game."""
        return self.current_language in self.game_locales

    def _play(self):
        """Callback when play button is clicked."""
        if not self._language_available():
            msg = f"Warning: This game does not support '{self.current_language}' language. It will use English instead."
            if messagebox.askyesno("Language Warning", msg):
                self.callback(self.game_data)
        else:
            self.callback(self.game_data)


class MainMenu:
    """Main menu for omniGames."""

    def __init__(self, root):
        """Initialize main menu."""
        self.root = root
        self.root.title("omniGames")
        self.root.geometry("700x600")
        self.root.configure(bg="#1a1a1a")

        self.current_user = None
        self.current_frame = None

        self.style_menu()
        self.show_user_selection()

    def style_menu(self):
        """Configure window styling."""
        self.root.configure(bg="#1a1a1a")

    def clear_frame(self):
        """Clear current frame."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = None

    def show_user_selection(self):
        """Show user selection screen."""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Title
        title = tk.Label(self.current_frame, text="omniGames", font=("Arial", 28, "bold"), fg="#00ccff", bg="#1a1a1a")
        title.pack(pady=20)

        # User selection
        users_label = tk.Label(
            self.current_frame, text=localization.translate("menu_select_user"), font=("Arial", 14), fg="white", bg="#1a1a1a"
        )
        users_label.pack(pady=10)

        users = db.get_all_users()
        for user in users:
            btn = tk.Button(
                self.current_frame,
                text=user["username"],
                command=lambda u=user: self.select_user(u["id"], u["username"]),
                font=("Arial", 12),
                width=20,
                bg="#0066cc",
                fg="white",
            )
            btn.pack(pady=5)

        # New user
        new_btn = tk.Button(
            self.current_frame,
            text=localization.translate("menu_new_user"),
            command=self.create_new_user,
            font=("Arial", 12),
            width=20,
            bg="#009900",
            fg="white",
        )
        new_btn.pack(pady=5)

        # Settings
        settings_frame = tk.Frame(self.current_frame, bg="#1a1a1a")
        settings_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        lang_label = tk.Label(settings_frame, text=localization.translate("language") + ":", fg="white", bg="#1a1a1a")
        lang_label.pack(side=tk.LEFT, padx=5)

        lang_var = tk.StringVar(value=localization.language)

        def change_language(lang):
            localization.set_language(lang)
            self.show_user_selection()

        lang_menu = ttk.Combobox(settings_frame, textvariable=lang_var, values=["en", "es"], state="readonly", width=5)
        lang_menu.pack(side=tk.LEFT, padx=5)
        lang_menu.bind("<<ComboboxSelected>>", lambda e: change_language(lang_var.get()))

    def select_user(self, user_id: int, username: str):
        """Select a user and show main menu."""
        self.current_user = {"id": user_id, "username": username}
        self.show_main_menu()

    def create_new_user(self):
        """Create a new user."""
        dialog = tk.Toplevel(self.root)
        dialog.title(localization.translate("menu_new_user"))
        dialog.geometry("300x150")
        dialog.configure(bg="#1a1a1a")

        label = tk.Label(dialog, text=localization.translate("enter_username"), fg="white", bg="#1a1a1a")
        label.pack(pady=10)

        entry = tk.Entry(dialog, font=("Arial", 12), width=25)
        entry.pack(pady=10)
        entry.focus()

        def create():
            username = entry.get().strip()
            if not username:
                messagebox.showerror(localization.translate("error"), localization.translate("enter_username"))
                return
            if db.user_exists(username):
                messagebox.showerror(localization.translate("error"), f"User '{username}' already exists")
                return

            user_id = db.create_user(username)
            messagebox.showinfo(
                localization.translate("success"), f"{localization.translate('user_created')}: {username}"
            )
            dialog.destroy()
            self.show_user_selection()

        btn = tk.Button(dialog, text=localization.translate("confirm"), command=create, bg="#0066cc", fg="white")
        btn.pack(pady=10)

    def show_main_menu(self):
        """Show main game menu."""
        self.clear_frame()
        self.current_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # User info
        user_info = tk.Label(
            self.current_frame,
            text=f"{localization.translate('username')}: {self.current_user['username']}",
            font=("Arial", 12),
            fg="#00ccff",
            bg="#1a1a1a",
        )
        user_info.pack(pady=10)

        # Games list
        games_label = tk.Label(
            self.current_frame, text=localization.translate("menu_start_game"), font=("Arial", 14, "bold"), fg="white", bg="#1a1a1a"
        )
        games_label.pack(pady=10)

        games = game_manager.get_installed_games()
        if not games:
            no_games = tk.Label(
                self.current_frame,
                text=localization.translate("no_games"),
                font=("Arial", 12),
                fg="yellow",
                bg="#1a1a1a",
            )
            no_games.pack(pady=20)

        # Create scrollable frame for games
        canvas = tk.Canvas(self.current_frame, bg="#1a1a1a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.current_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1a1a1a")

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for game in games:
            GameButton(scrollable_frame, game, self.launch_game, localization.language)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bottom buttons
        button_frame = tk.Frame(self.current_frame, bg="#1a1a1a")
        button_frame.pack(fill=tk.X, pady=10)

        install_btn = tk.Button(
            button_frame,
            text=localization.translate("menu_install_game"),
            command=self.install_game,
            font=("Arial", 11),
            bg="#009900",
            fg="white",
            width=15,
        )
        install_btn.pack(side=tk.LEFT, padx=5)

        stats_btn = tk.Button(
            button_frame,
            text=localization.translate("menu_user_stats"),
            command=self.show_stats,
            font=("Arial", 11),
            bg="#ff9900",
            fg="white",
            width=15,
        )
        stats_btn.pack(side=tk.LEFT, padx=5)

        back_btn = tk.Button(
            button_frame,
            text=localization.translate("back"),
            command=self.show_user_selection,
            font=("Arial", 11),
            bg="#666666",
            fg="white",
            width=15,
        )
        back_btn.pack(side=tk.RIGHT, padx=5)

    def launch_game(self, game_data: dict):
        """Launch a game."""
        game_name = game_data["name"]
        game_path = Path(game_data["path"])

        try:
            # Import game module - always use main.py as entry point
            module_path = game_path / "main.py"

            if not module_path.exists():
                messagebox.showerror(localization.translate("error"), f"Game entry point not found: {module_path}")
                return

            # Load and execute game
            spec = importlib.util.spec_from_file_location(game_name, module_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[game_name] = module
            spec.loader.exec_module(module)

            # Run game with current language
            if hasattr(module, "main"):
                score = module.main(self.current_user["id"], localization.language)

                # Update statistics
                db.update_game_stats(self.current_user["id"], game_name, score, 0)

                messagebox.showinfo(localization.translate("success"), f"Final Score: {score}")
            else:
                messagebox.showerror(localization.translate("error"), f"Game has no 'main' function")

            # Refresh menu
            self.show_main_menu()

        except Exception as e:
            messagebox.showerror(localization.translate("error"), f"Error launching game:\n{str(e)}")

    def install_game(self):
        """Install a game from ZIP."""
        zip_path = filedialog.askopenfilename(
            title=localization.translate("select_zip"), filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")]
        )

        if not zip_path:
            return

        success, message = game_manager.install_game_from_zip(zip_path)
        if success:
            messagebox.showinfo(localization.translate("success"), message)
            self.show_main_menu()
        else:
            messagebox.showerror(localization.translate("error"), message)

    def show_stats(self):
        """Show user statistics."""
        stats = db.get_user_game_stats(self.current_user["id"])

        if not stats:
            messagebox.showinfo(localization.translate("menu_user_stats"), "No statistics available yet")
            return

        stats_text = f"User: {self.current_user['username']}\n\n"
        for stat in stats:
            stats_text += f"{stat['game_name'].upper()}\n"
            stats_text += f"  {localization.translate('high_score')}: {stat['high_score']}\n"
            stats_text += f"  {localization.translate('times_played')}: {stat['times_played']}\n\n"

        messagebox.showinfo(localization.translate("menu_user_stats"), stats_text)


def main():
    """Main entry point for the menu."""
    root = tk.Tk()
    menu = MainMenu(root)
    root.mainloop()


if __name__ == "__main__":
    main()

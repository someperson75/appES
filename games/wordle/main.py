"""Wordle-style Game for omniGames (console-friendly)."""

import random
import sys
from pathlib import Path
from typing import List, Dict, Any
import tkinter as tk
from tkinter import messagebox

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from omnigames.core.base_game import BaseGame


class WordleGame(BaseGame):
    """Wordle-style game implementation (console).

    This implementation is intentionally console-based so it can be run
    directly with `python games/wordle/main.py` for quick testing.
    """

    def __init__(self, user_id: int, game_name: str, language: str = "en"):
        super().__init__(user_id, game_name)
        self.language = language
        self.word_len = 5
        self.max_attempts = 6
        self.words: List[str] = []
        self.secret: str = ""
        self.attempts: List[str] = []
        self.score_value = 0

    def _words_file_path(self) -> Path:
        return Path(__file__).parent / "assets" / "words.txt"

    def initialize(self) -> bool:
        """Load word list and pick a secret word."""
        path = self._words_file_path()
        if path.exists():
            try:
                with path.open("r", encoding="utf-8") as fh:
                    self.words = [w.strip().lower() for w in fh if w.strip()]
            except Exception:
                self.words = []
        if not self.words:
            # Fallback small list
            self.words = [
                "apple",
                "brick",
                "crane",
                "draft",
                "eagle",
                "flame",
                "grape",
                "house",
                "input",
                "joker",
                "knock",
                "lemon",
                "mango",
                "night",
                "ocean",
                "paper",
                "queen",
                "river",
                "stone",
                "trace",
            ]

        # Filter only correct-length words
        self.words = [w for w in self.words if len(w) == self.word_len]
        if not self.words:
            return False

        self.secret = random.choice(self.words)
        self.attempts = []
        self.score_value = 0
        return True

    def handle_event(self, event: Any) -> None:
        # Console-based game doesn't use events
        pass

    def update(self, dt: float) -> None:
        # Not used for the CLI version
        pass

    def render(self) -> None:
        # Print previous attempts with simple emoji feedback
        for guess in self.attempts:
            print(self._format_feedback(guess))

    def cleanup(self) -> None:
        # Nothing special to clean up for console
        pass

    def get_score(self) -> int:
        return self.score_value

    def _format_feedback(self, guess: str) -> str:
        # Wordle-style marking: 🟩 correct pos, 🟨 wrong pos, ⬛ absent
        secret = list(self.secret)
        result = [""] * self.word_len

        # First pass: greens
        for i, ch in enumerate(guess):
            if secret[i] == ch:
                result[i] = "🟩"
                secret[i] = " "

        # Second pass: yellows or blacks
        for i, ch in enumerate(guess):
            if result[i]:
                continue
            if ch in secret:
                result[i] = "🟨"
                secret[secret.index(ch)] = " "
            else:
                result[i] = "⬛"

        # Return string with guess + feedback
        return f"{guess}  {''.join(result)}"

    def run(self) -> int:
        """Interactive console run. Returns score (attempts used or 0 on fail)."""
        if not self.initialize():
            print("Failed to initialize Wordle (no words available).")
            return 0

        print("Welcome to Wordle (console). Guess the 5-letter word.")
        for attempt_num in range(1, self.max_attempts + 1):
            guess = input(f"Attempt {attempt_num}/{self.max_attempts}: ").strip().lower()
            if guess == "":
                print("Empty input — try again.")
                continue
            if len(guess) != self.word_len:
                print(f"Please enter a {self.word_len}-letter word.")
                continue
            if guess not in self.words:
                print("Word not in list. Try another word.")
                continue

            self.attempts.append(guess)
            print(self._format_feedback(guess))

            if guess == self.secret:
                self.score_value = max(0, self.max_attempts - attempt_num + 1)
                print(f"Correct! You guessed the word in {attempt_num} attempts.")
                break
        else:
            # Ran out of attempts
            print(f"Out of attempts. The word was '{self.secret}'.")
            self.score_value = 0

        self.cleanup()
        return self.get_score()


class WordleGUI:
    """Minimal Tkinter GUI for Wordle to integrate with the main menu."""

    GREEN = "#6aaa64"
    YELLOW = "#c9b458"
    GRAY = "#787c7e"

    def __init__(self, parent, game: WordleGame, user_id: int):
        self.parent = parent
        self.game = game
        self.user_id = user_id
        self.top = tk.Toplevel(parent)
        self.top.title("Wordle")
        self.top.geometry("400x500")
        self.top.protocol("WM_DELETE_WINDOW", self._on_close)

        self.grid_labels:list[list[tk.Label]] = [[tk.Label for _ in range(game.word_len)] for _ in range(game.max_attempts)]
        self.current_row = 0

        self._build_ui()
        self.finished = False
        self.result_score = 0

    def _build_ui(self):
        frame = tk.Frame(self.top)
        frame.pack(pady=10)

        for r in range(self.game.max_attempts):
            for c in range(self.game.word_len):
                lbl = tk.Label(frame, text=" ", width=4, height=2, relief=tk.RIDGE, bg="white", font=("Helvetica", 16, "bold"))
                lbl.grid(row=r, column=c, padx=4, pady=4)
                self.grid_labels[r][c] = lbl

        entry_frame = tk.Frame(self.top)
        entry_frame.pack(pady=10)
        self.entry = tk.Entry(entry_frame, font=("Helvetica", 14), width=10)
        self.entry.pack(side=tk.LEFT, padx=5)
        submit = tk.Button(entry_frame, text="Submit", command=self._on_submit)
        submit.pack(side=tk.LEFT)

    def _on_submit(self):
        guess = self.entry.get().strip().lower()
        if not guess:
            return
        if len(guess) != self.game.word_len:
            messagebox.showinfo("Wordle", f"Please enter a {self.game.word_len}-letter word.")
            return
        if guess not in self.game.words:
            messagebox.showinfo("Wordle", "Word not in list.")
            return

        self.game.attempts.append(guess)
        feedback = self._feedback_list(guess)

        for i, ch in enumerate(guess):
            lbl = self.grid_labels[self.current_row][i]
            lbl.config(text=ch.upper())
            lbl.config(bg=feedback[i])

        self.current_row += 1
        self.entry.delete(0, tk.END)

        if guess == self.game.secret:
            self.result_score = max(0, self.game.max_attempts - self.current_row + 1)
            messagebox.showinfo("Wordle", f"Correct! You guessed the word in {self.current_row} attempts.")
            self.finished = True
            self.top.destroy()
            return

        if self.current_row >= self.game.max_attempts:
            messagebox.showinfo("Wordle", f"Out of attempts. The word was '{self.game.secret}'.")
            self.finished = True
            self.result_score = 0
            self.top.destroy()

    def _feedback_list(self, guess: str) -> List[str]:
        secret = list(self.game.secret)
        colors = [None] * self.game.word_len
        for i, ch in enumerate(guess):
            if secret[i] == ch:
                colors[i] = self.GREEN
                secret[i] = None

        for i, ch in enumerate(guess):
            if colors[i]:
                continue
            if ch in secret:
                colors[i] = self.YELLOW
                secret[secret.index(ch)] = None
            else:
                colors[i] = self.GRAY

        return colors

    def _on_close(self):
        self.finished = True
        self.top.destroy()

    def wait(self) -> int:
        self.top.transient(self.parent)
        self.top.grab_set()
        self.parent.wait_window(self.top)
        return self.result_score


def main(user_id: int = 0, language: str = "en") -> int:
    """Entry point used by the menu launcher.

    When called from the GUI launcher, `user_id` and `language` are passed in.
    When run as a script, defaults are used and interactive play starts.
    Returns the final score as an integer.
    """
    # If running as a script with --test, run initialized test
    if "--test" in sys.argv:
        game = WordleGame(user_id=user_id, game_name="wordle", language=language)
        ok = game.initialize()
        if not ok:
            print("Initialization failed.")
            return 0
        print(f"Loaded {len(game.words)} words. Secret='{game.secret}'")
        return 0

    # Interactive/normal run: use GUI if running under the main Tk root (launched from menu)
    game = WordleGame(user_id=user_id, game_name="wordle", language=language)
    if not game.initialize():
        print("Failed to initialize Wordle (no words available).")
        return 0

    try:
        # If a Tk root exists (menu launched), open a Toplevel GUI
        if tk._default_root is not None:
            gui = WordleGUI(tk._default_root, game, user_id)
            score = gui.wait()
            return score
    except Exception:
        # Fallback to console run if GUI fails
        pass

    # Console fallback
    score = game.run()
    return score


if __name__ == "__main__":
    exit_code = main()
    sys.exit(0 if exit_code >= 0 else 1)

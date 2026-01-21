"""Memory Game for omniGames."""

import pygame
import random
from typing import Dict, Any, List, Tuple
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from omnigames.core.base_game import BaseGame


class MemoryGame(BaseGame):
    """Memory/Matching game implementation."""

    def __init__(self, user_id: int, game_name: str):
        """Initialize Memory game."""
        super().__init__(user_id, game_name)
        self.screen = None
        self.clock = None
        self.score = 0
        self.grid_cols = 4
        self.grid_rows = 4
        self.card_width = 100
        self.card_height = 100
        self.card_spacing = 10
        self.cards = []
        self.revealed = []
        self.matched = []
        self.first_click = None
        self.second_click = None
        self.click_locked = False
        self.moves = 0
        self.matched_count = 0
        self._initialize_cards()

    def _initialize_cards(self) -> None:
        """Initialize card grid."""
        numbers = list(range(1, (self.grid_cols * self.grid_rows) // 2 + 1)) * 2
        random.shuffle(numbers)
        self.cards = numbers
        self.revealed = [False] * len(self.cards)
        self.matched = [False] * len(self.cards)

    def reset_game(self) -> None:
        """Reset game state without reinitializing pygame."""
        self.score = 0
        self.moves = 0
        self.matched_count = 0
        self._initialize_cards()
        self.first_click = None
        self.second_click = None
        self.click_locked = False

    def initialize(self) -> bool:
        """Initialize pygame and game resources."""
        try:
            pygame.init()
            width = self.grid_cols * (self.card_width + self.card_spacing) + self.card_spacing
            height = self.grid_rows * (self.card_height + self.card_spacing) + 100
            self.screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption("Memory Game")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font(None, 36)
            self.card_font = pygame.font.Font(None, 72)
            return True
        except Exception as e:
            print(f"Initialization error: {e}")
            return False

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pygame events."""
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.key == pygame.K_SPACE and self.matched_count == len(self.cards) // 2:
                self.reset_game()
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.click_locked:
            if not self.paused:
                pos = pygame.mouse.get_pos()
                col = pos[0] // (self.card_width + self.card_spacing)
                row = pos[1] // (self.card_height + self.card_spacing)

                if 0 <= row < self.grid_rows and 0 <= col < self.grid_cols:
                    index = row * self.grid_cols + col
                    if index < len(self.cards) and not self.revealed[index] and not self.matched[index]:
                        self.revealed[index] = True
                        if self.first_click is None:
                            self.first_click = index
                        elif self.second_click is None:
                            self.second_click = index
                            self.moves += 1
                            self.click_locked = True

    def update(self, dt: float) -> None:
        """Update game state."""
        if self.paused or not self.click_locked:
            return

        # Wait before checking match
        pygame.time.wait(500)

        if self.first_click is not None and self.second_click is not None:
            if self.cards[self.first_click] == self.cards[self.second_click]:
                # Match found
                self.matched[self.first_click] = True
                self.matched[self.second_click] = True
                self.matched_count += 1
                self.score += 10
            else:
                # No match
                self.revealed[self.first_click] = False
                self.revealed[self.second_click] = False

            self.first_click = None
            self.second_click = None
            self.click_locked = False

    def render(self) -> None:
        """Render the game."""
        self.screen.fill((50, 50, 50))

        # Draw cards
        for i in range(len(self.cards)):
            row = i // self.grid_cols
            col = i % self.grid_cols
            x = col * (self.card_width + self.card_spacing) + self.card_spacing
            y = row * (self.card_height + self.card_spacing) + self.card_spacing

            # Draw card background
            if self.matched[i]:
                color = (100, 200, 100)
            elif self.revealed[i]:
                color = (200, 200, 200)
            else:
                color = (100, 100, 150)

            pygame.draw.rect(self.screen, color, (x, y, self.card_width, self.card_height))
            pygame.draw.rect(self.screen, (200, 200, 200), (x, y, self.card_width, self.card_height), 2)

            # Draw card number
            if self.revealed[i] or self.matched[i]:
                text = self.card_font.render(str(self.cards[i]), True, (0, 0, 0))
                text_rect = text.get_rect(center=(x + self.card_width // 2, y + self.card_height // 2))
                self.screen.blit(text, text_rect)

        # Draw UI
        ui_y = self.grid_rows * (self.card_height + self.card_spacing) + self.card_spacing
        score_text = self.font.render(f"Score: {self.score} | Moves: {self.moves}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, ui_y + 10))

        if self.matched_count == len(self.cards) // 2:
            game_over_text = self.font.render("YOU WON! Press SPACE to restart", True, (0, 255, 0))
            self.screen.blit(game_over_text, (50, ui_y + 50))

        pygame.display.flip()

    def cleanup(self) -> None:
        """Cleanup resources."""
        pygame.quit()

    def run(self) -> int:
        """Main game loop."""
        self.running = True
        if not self.initialize():
            return 0

        try:
            while self.running:
                dt = self.clock.tick(60) / 1000.0

                for event in pygame.event.get():
                    self.handle_event(event)

                if not self.paused:
                    self.update(dt)

                self.render()
        finally:
            self.cleanup()

        return self.get_score()

    def get_score(self) -> int:
        """Return current score."""
        return self.score


def main(user_id: int) -> int:
    """Entry point for Memory game."""
    game = MemoryGame(user_id, "memory")
    return game.run()


if __name__ == "__main__":
    main(1)

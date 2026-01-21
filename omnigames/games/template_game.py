"""
Template for creating a new omniGames game.

To create a new game:
1. Copy this file and rename it appropriately
2. Rename 'TemplateGame' class to your game name
3. Implement the required methods
4. Create a game.json manifest in your game folder
"""

import pygame
from typing import Dict, Any
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from omnigames.core.base_game import BaseGame


class TemplateGame(BaseGame):
    """Template game implementation."""

    def __init__(self, user_id: int, game_name: str):
        """Initialize template game."""
        super().__init__(user_id, game_name)
        self.screen = None
        self.clock = None
        self.score = 0

    def initialize(self) -> bool:
        """Initialize pygame and game resources."""
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((800, 600))
            pygame.display.set_caption("Template Game")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font(None, 36)
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
            elif event.key == pygame.K_SPACE:
                self.score += 10

    def update(self, dt: float) -> None:
        """Update game state."""
        # Add your game logic here
        pass

    def render(self) -> None:
        """Render the game."""
        self.screen.fill((0, 0, 0))  # Black background

        # Render score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        # Render instructions
        instruction_text = self.font.render("Press SPACE to add points, ESC to quit", True, (200, 200, 200))
        self.screen.blit(instruction_text, (50, 250))

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
                dt = self.clock.tick(60) / 1000.0  # 60 FPS

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

    def get_game_state(self) -> Dict[str, Any]:
        """Get game state for saving."""
        return {"score": self.score}

    def load_game_state(self, state: Dict[str, Any]) -> None:
        """Load game state."""
        self.score = state.get("score", 0)


def main(user_id: int) -> int:
    """Entry point for the game. Returns final score."""
    game = TemplateGame(user_id, "template_game")
    return game.run()


if __name__ == "__main__":
    # For testing purposes
    main(1)

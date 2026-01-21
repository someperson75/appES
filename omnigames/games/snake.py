"""Snake Game for omniGames."""

import pygame
import random
from typing import Dict, Any, List, Tuple
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from omnigames.core.base_game import BaseGame


class SnakeGame(BaseGame):
    """Classic Snake game implementation."""

    def __init__(self, user_id: int, game_name: str):
        """Initialize Snake game."""
        super().__init__(user_id, game_name)
        self.screen = None
        self.clock = None
        self.score = 0
        self.grid_size = 20
        self.grid_width = 40
        self.grid_height = 30
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.food = self._spawn_food()
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.game_over = False

    def _spawn_food(self) -> Tuple[int, int]:
        """Spawn food at random location not occupied by snake."""
        while True:
            food = (random.randint(0, self.grid_width - 1), random.randint(0, self.grid_height - 1))
            if food not in self.snake:
                return food

    def reset_game(self) -> None:
        """Reset game state without reinitializing pygame."""
        self.score = 0
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.food = self._spawn_food()
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.game_over = False

    def initialize(self) -> bool:
        """Initialize pygame and game resources."""
        try:
            pygame.init()
            width = self.grid_width * self.grid_size
            height = self.grid_height * self.grid_size + 50
            self.screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption("Snake Game")
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
            elif event.key == pygame.K_UP and self.direction != (0, 1):
                self.next_direction = (0, -1)
            elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                self.next_direction = (0, 1)
            elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                self.next_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                self.next_direction = (1, 0)
            elif event.key == pygame.K_SPACE and self.game_over:
                self.reset_game()

    def update(self, dt: float) -> None:
        """Update game state."""
        if self.game_over or self.paused:
            return

        self.direction = self.next_direction
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        # Check collision with walls
        if (
            new_head[0] < 0
            or new_head[0] >= self.grid_width
            or new_head[1] < 0
            or new_head[1] >= self.grid_height
        ):
            self.game_over = True
            return

        # Check collision with self
        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        # Check if food eaten
        if new_head == self.food:
            self.score += 10
            self.food = self._spawn_food()
        else:
            self.snake.pop()

    def render(self) -> None:
        """Render the game."""
        self.screen.fill((0, 0, 0))

        # Draw grid
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                rect = pygame.Rect(x * self.grid_size, y * self.grid_size, self.grid_size, self.grid_size)
                pygame.draw.rect(self.screen, (30, 30, 30), rect, 1)

        # Draw snake
        for segment in self.snake:
            rect = pygame.Rect(
                segment[0] * self.grid_size + 1,
                segment[1] * self.grid_size + 1,
                self.grid_size - 2,
                self.grid_size - 2,
            )
            pygame.draw.rect(self.screen, (0, 255, 0), rect)

        # Draw food
        food_rect = pygame.Rect(
            self.food[0] * self.grid_size + 1,
            self.food[1] * self.grid_size + 1,
            self.grid_size - 2,
            self.grid_size - 2,
        )
        pygame.draw.rect(self.screen, (255, 0, 0), food_rect)

        # Draw UI
        ui_y = self.grid_height * self.grid_size
        pygame.draw.line(self.screen, (100, 100, 100), (0, ui_y), (self.grid_width * self.grid_size, ui_y))

        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, ui_y + 10))

        if self.game_over:
            game_over_text = self.font.render("GAME OVER! Press SPACE to restart", True, (255, 0, 0))
            self.screen.blit(game_over_text, (100, ui_y + 10))

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
                dt = self.clock.tick(10) / 1000.0  # 10 FPS for snake

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
    """Entry point for Snake game."""
    game = SnakeGame(user_id, "snake")
    return game.run()


if __name__ == "__main__":
    main(1)

"""Pong Game for omniGames."""

import pygame
import random
from typing import Dict, Any
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from omnigames.core.base_game import BaseGame


class PongGame(BaseGame):
    """Pong game implementation."""

    def __init__(self, user_id: int, game_name: str):
        """Initialize Pong game with pygame resources."""
        super().__init__(user_id, game_name)
        
        # Initialize pygame and resources (do not change on restart)
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 36)
        
        # Paddle properties
        self.paddle_width = 15
        self.paddle_height = 90
        self.paddle_speed = 5
        
        # Ball properties
        self.ball_size = 10
        self.ball_speed = 5
        
        # Initialize game state
        self.initialize()
        
    def initialize(self) -> bool:
        """Initialize game variables and state."""
        try:
            self.score = 0
            self.enemy_score = 0
            
            # Player paddle
            self.player_x = 10
            self.player_y = self.height // 2 - self.paddle_height // 2
            self.player_dy = 0
            
            # Enemy paddle
            self.enemy_x = self.width - 25
            self.enemy_y = self.height // 2 - self.paddle_height // 2
            self.enemy_dy = 0
            
            # Ball
            self.ball_x = self.width // 2
            self.ball_y = self.height // 2
            self.ball_dx = 5
            self.ball_dy = 5
            
            self.game_over = False
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
            elif event.key == pygame.K_UP:
                self.player_dy = -self.paddle_speed
            elif event.key == pygame.K_DOWN:
                self.player_dy = self.paddle_speed
            elif event.key == pygame.K_SPACE and self.game_over:
                self.initialize()
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                self.player_dy = 0

    def update(self, dt: float) -> None:
        """Update game state."""
        if self.paused:
            return

        # Update player paddle
        self.player_y += self.player_dy
        self.player_y = max(0, min(self.height - self.paddle_height, self.player_y))

        # AI enemy movement
        enemy_center = self.enemy_y + self.paddle_height // 2
        if enemy_center < self.ball_y - 20:
            self.enemy_y += self.paddle_speed
        elif enemy_center > self.ball_y + 20:
            self.enemy_y -= self.paddle_speed
        self.enemy_y = max(0, min(self.height - self.paddle_height, self.enemy_y))

        # Update ball
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        # Ball collision with top/bottom
        if self.ball_y <= 0 or self.ball_y >= self.height - self.ball_size:
            self.ball_dy = -self.ball_dy
            self.ball_y = max(0, min(self.height - self.ball_size, self.ball_y))

        # Ball collision with paddles
        if (
            self.ball_x <= self.player_x + self.paddle_width
            and self.player_y <= self.ball_y <= self.player_y + self.paddle_height
        ):
            self.ball_dx = abs(self.ball_dx)
            self.ball_x = self.player_x + self.paddle_width

        if (
            self.ball_x >= self.enemy_x - self.ball_size
            and self.enemy_y <= self.ball_y <= self.enemy_y + self.paddle_height
        ):
            self.ball_dx = -abs(self.ball_dx)
            self.ball_x = self.enemy_x - self.ball_size

        # Scoring
        if self.ball_x < 0:
            self.enemy_score += 1
            self.ball_x = self.width // 2
            self.ball_y = self.height // 2

        if self.ball_x > self.width:
            self.score += 1
            self.ball_x = self.width // 2
            self.ball_y = self.height // 2

        # Check if game over (first to 5)
        if self.score >= 5:
            self.game_over = True
        elif self.enemy_score >= 5:
            self.game_over = True

    def render(self) -> None:
        """Render the game."""
        self.screen.fill((0, 0, 0))

        # Draw center line
        for y in range(0, self.height, 10):
            pygame.draw.line(self.screen, (255, 255, 255), (self.width // 2, y), (self.width // 2, y + 5), 2)

        # Draw paddles
        pygame.draw.rect(
            self.screen, (255, 255, 255), (self.player_x, self.player_y, self.paddle_width, self.paddle_height)
        )
        pygame.draw.rect(
            self.screen, (255, 255, 255), (self.enemy_x, self.enemy_y, self.paddle_width, self.paddle_height)
        )

        # Draw ball
        pygame.draw.rect(self.screen, (255, 255, 255), (self.ball_x, self.ball_y, self.ball_size, self.ball_size))

        # Draw scores
        player_text = self.font.render(str(self.score), True, (255, 255, 255))
        enemy_text = self.font.render(str(self.enemy_score), True, (255, 255, 255))
        self.screen.blit(player_text, (self.width // 4, 20))
        self.screen.blit(enemy_text, (3 * self.width // 4, 20))

        if self.game_over:
            if self.score >= 5:
                winner_text = self.small_font.render("YOU WON! Press SPACE to restart", True, (0, 255, 0))
            else:
                winner_text = self.small_font.render("YOU LOST! Press SPACE to restart", True, (255, 0, 0))
            self.screen.blit(winner_text, (150, self.height // 2))

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
    """Entry point for Pong game."""
    game = PongGame(user_id, "pong")
    return game.run()


if __name__ == "__main__":
    main(1)

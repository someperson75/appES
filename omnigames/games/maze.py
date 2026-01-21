"""Pacman-style Maze Game for omniGames."""

import pygame
import random
from typing import Dict, Any, List, Tuple
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from omnigames.core.base_game import BaseGame


class MazeGame(BaseGame):
    """Maze/Pacman-style game implementation."""

    def __init__(self, user_id: int, game_name: str):
        """Initialize Maze game."""
        super().__init__(user_id, game_name)
        self.screen = None
        self.clock = None
        self.score = 0
        self.tile_size = 30
        self.grid_width = 20
        self.grid_height = 18

        # Player
        self.player_x = 1
        self.player_y = 1
        self.player_speed = 0.1

        # Ghosts
        self.ghosts = [
            {"x": 9, "y": 8, "dx": 1, "dy": 0},
            {"x": 8, "y": 9, "dx": 0, "dy": 1},
            {"x": 9, "y": 9, "dx": -1, "dy": 0},
        ]

        # Maze generation
        self.maze = self._generate_maze()
        self.pellets = self._generate_pellets()
        self.game_over = False
        self.won = False

    def _generate_maze(self) -> List[List[int]]:
        """Generate a simple maze. 1 = wall, 0 = path."""
        maze = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]

        # Add walls
        for i in range(self.grid_height):
            maze[i][0] = 1
            maze[i][self.grid_width - 1] = 1
        for j in range(self.grid_width):
            maze[0][j] = 1
            maze[self.grid_height - 1][j] = 1

        # Add some random walls
        for i in range(3, self.grid_height - 3):
            for j in range(3, self.grid_width - 3):
                if random.random() < 0.15:
                    maze[i][j] = 1

        return maze

    def _generate_pellets(self) -> set:
        """Generate pellets in open spaces."""
        pellets = set()
        for i in range(1, self.grid_height - 1):
            for j in range(1, self.grid_width - 1):
                if self.maze[i][j] == 0 and random.random() < 0.3:
                    pellets.add((i, j))
        return pellets

    def reset_game(self) -> None:
        """Reset game state without reinitializing pygame."""
        self.score = 0
        self.player_x = 1
        self.player_y = 1
        self.ghosts = [
            {"x": 9, "y": 8, "dx": 1, "dy": 0},
            {"x": 8, "y": 9, "dx": 0, "dy": 1},
            {"x": 9, "y": 9, "dx": -1, "dy": 0},
        ]
        self.maze = self._generate_maze()
        self.pellets = self._generate_pellets()
        self.game_over = False
        self.won = False

    def initialize(self) -> bool:
        """Initialize pygame and game resources."""
        try:
            pygame.init()
            width = self.grid_width * self.tile_size
            height = self.grid_height * self.tile_size + 50
            self.screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption("Maze Game")
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
            elif event.key == pygame.K_SPACE and self.game_over:
                self.reset_game()

    def update(self, dt: float) -> None:
        """Update game state."""
        if self.game_over or self.paused:
            return

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not self._is_wall(int(self.player_x - self.player_speed), int(self.player_y)):
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT] and not self._is_wall(int(self.player_x + self.player_speed), int(self.player_y)):
            self.player_x += self.player_speed
        if keys[pygame.K_UP] and not self._is_wall(int(self.player_x), int(self.player_y - self.player_speed)):
            self.player_y -= self.player_speed
        if keys[pygame.K_DOWN] and not self._is_wall(int(self.player_x), int(self.player_y + self.player_speed)):
            self.player_y += self.player_speed

        # Collect pellets
        player_grid = (int(self.player_y), int(self.player_x))
        if player_grid in self.pellets:
            self.pellets.remove(player_grid)
            self.score += 10

        # Check win condition
        if not self.pellets:
            self.won = True
            self.game_over = True
            self.score += 100

        # Ghost movement
        for ghost in self.ghosts:
            ghost["x"] += ghost["dx"]
            ghost["y"] += ghost["dy"]

            if self._is_wall(ghost["x"], ghost["y"]):
                ghost["dx"] = random.choice([-1, 0, 1])
                ghost["dy"] = random.choice([-1, 0, 1])

            # Collision with player
            if int(ghost["x"]) == int(self.player_x) and int(ghost["y"]) == int(self.player_y):
                self.game_over = True

    def _is_wall(self, x: int, y: int) -> bool:
        """Check if position is a wall."""
        if 0 <= y < self.grid_height and 0 <= x < self.grid_width:
            return self.maze[y][x] == 1
        return True

    def render(self) -> None:
        """Render the game."""
        self.screen.fill((0, 0, 0))

        # Draw maze
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if self.maze[i][j] == 1:
                    rect = pygame.Rect(j * self.tile_size, i * self.tile_size, self.tile_size, self.tile_size)
                    pygame.draw.rect(self.screen, (50, 150, 255), rect)

        # Draw pellets
        for i, j in self.pellets:
            center_x = j * self.tile_size + self.tile_size // 2
            center_y = i * self.tile_size + self.tile_size // 2
            pygame.draw.circle(self.screen, (255, 255, 150), (center_x, center_y), 3)

        # Draw player
        player_rect = pygame.Rect(
            int(self.player_x) * self.tile_size + 5, int(self.player_y) * self.tile_size + 5, self.tile_size - 10, self.tile_size - 10
        )
        pygame.draw.rect(self.screen, (255, 255, 0), player_rect)

        # Draw ghosts
        colors = [(255, 0, 0), (255, 184, 255), (0, 255, 255)]
        for idx, ghost in enumerate(self.ghosts):
            ghost_rect = pygame.Rect(
                int(ghost["x"]) * self.tile_size + 5, int(ghost["y"]) * self.tile_size + 5, self.tile_size - 10, self.tile_size - 10
            )
            pygame.draw.rect(self.screen, colors[idx], ghost_rect)

        # Draw UI
        ui_y = self.grid_height * self.tile_size
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, ui_y + 10))

        if self.game_over:
            if self.won:
                status_text = self.font.render("YOU WON!", True, (0, 255, 0))
            else:
                status_text = self.font.render("CAUGHT! Press SPACE", True, (255, 0, 0))
            self.screen.blit(status_text, (200, ui_y + 10))

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
                dt = self.clock.tick(10) / 1000.0

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
    """Entry point for Maze game."""
    game = MazeGame(user_id, "maze")
    return game.run()


if __name__ == "__main__":
    main(1)

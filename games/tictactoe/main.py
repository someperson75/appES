"""Tic Tac Toe Game for omniGames."""

import pygame
from typing import Dict, Any, Optional, List, Tuple
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from omnigames.core.base_game import BaseGame


class TicTacToeGame(BaseGame):
    """Tic Tac Toe game implementation with AI opponent."""

    def __init__(self, user_id: int, game_name: str):
        """Initialize Tic Tac Toe game."""
        super().__init__(user_id, game_name)
        self.screen = None
        self.clock = None
        self.score = 0
        self.board: List[List[int]] = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.player = 1  # 1 = human, -1 = AI
        self.game_over = False
        self.winner = None
        self.message = "Your turn (X)"
        self.cell_size = 150

    def initialize(self) -> bool:
        """Initialize pygame and game resources."""
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((600, 700))
            pygame.display.set_caption("Tic Tac Toe")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font(None, 36)
            self.large_font = pygame.font.Font(None, 72)
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
                self.__init__(self.user_id, self.game_name)
        elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
            if not self.paused:
                pos = pygame.mouse.get_pos()
                col = pos[0] // self.cell_size
                row = (pos[1] - 50) // self.cell_size
                if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == 0:
                    self.board[row][col] = 1
                    self.check_game_state()
                    if not self.game_over:
                        self.ai_move()
                        self.check_game_state()

    def ai_move(self) -> None:
        """Make AI move using minimax algorithm."""
        best_score = float("-inf")
        best_move = None

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    self.board[i][j] = -1
                    score = self._minimax(0, False)
                    self.board[i][j] = 0
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        if best_move:
            self.board[best_move[0]][best_move[1]] = -1

    def _minimax(self, depth: int, is_maximizing: bool) -> int:
        """Minimax algorithm for AI."""
        winner = self._check_winner()
        if winner == 1:
            return 10 - depth
        elif winner == -1:
            return depth - 10
        elif self._is_full():
            return 0

        if is_maximizing:
            best_score = float("-inf")
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == 0:
                        self.board[i][j] = 1
                        score = self._minimax(depth + 1, False)
                        self.board[i][j] = 0
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == 0:
                        self.board[i][j] = -1
                        score = self._minimax(depth + 1, True)
                        self.board[i][j] = 0
                        best_score = min(score, best_score)
            return best_score

    def _check_winner(self) -> Optional[int]:
        """Check for winner. Returns 1 for human, -1 for AI, 0 for draw, None for ongoing."""
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != 0:
                return row[0]

        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != 0:
                return self.board[0][col]

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            return self.board[0][2]

        return None

    def _is_full(self) -> bool:
        """Check if board is full."""
        return all(self.board[i][j] != 0 for i in range(3) for j in range(3))

    def check_game_state(self) -> None:
        """Check current game state."""
        winner = self._check_winner()
        if winner == 1:
            self.game_over = True
            self.winner = "You Won!"
            self.score = 100
            self.message = "You Won! Press SPACE to restart"
        elif winner == -1:
            self.game_over = True
            self.winner = "AI Won!"
            self.message = "AI Won! Press SPACE to restart"
        elif self._is_full():
            self.game_over = True
            self.winner = "Draw!"
            self.message = "Draw! Press SPACE to restart"
        else:
            self.message = "Your turn (X)"

    def update(self, dt: float) -> None:
        """Update game state."""
        pass

    def render(self) -> None:
        """Render the game."""
        self.screen.fill((240, 240, 240))

        # Draw title
        title = self.font.render("Tic Tac Toe", True, (0, 0, 0))
        self.screen.blit(title, (200, 10))

        # Draw board
        for i in range(3):
            for j in range(3):
                x = j * self.cell_size
                y = 50 + i * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 2)

                cell_value = self.board[i][j]
                if cell_value == 1:
                    text = self.large_font.render("X", True, (0, 0, 255))
                    self.screen.blit(text, (x + 40, y + 30))
                elif cell_value == -1:
                    text = self.large_font.render("O", True, (255, 0, 0))
                    self.screen.blit(text, (x + 40, y + 30))

        # Draw message
        message_text = self.font.render(self.message, True, (0, 0, 0))
        self.screen.blit(message_text, (50, 600))

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

                self.update(dt)
                self.render()
        finally:
            self.cleanup()

        return self.get_score()

    def get_score(self) -> int:
        """Return current score."""
        return self.score


def main(user_id: int) -> int:
    """Entry point for Tic Tac Toe game."""
    game = TicTacToeGame(user_id, "tictactoe")
    return game.run()


if __name__ == "__main__":
    main(1)

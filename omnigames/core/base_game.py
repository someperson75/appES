"""Base class for all omniGames games."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseGame(ABC):
    """Abstract base class for all games."""

    def __init__(self, user_id: int, game_name: str):
        """
        Initialize the game.

        Args:
            user_id: ID of the current user
            game_name: Name of the game
        """
        self.user_id = user_id
        self.game_name = game_name
        self.running = False
        self.paused = False

    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize game resources.
        Returns True if successful.
        """
        pass

    @abstractmethod
    def handle_event(self, event: Any) -> None:
        """Handle input events."""
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """Update game state. dt is delta time in seconds."""
        pass

    @abstractmethod
    def render(self) -> None:
        """Render/draw the game."""
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Cleanup game resources."""
        pass

    def get_score(self) -> int:
        """Get current game score. Override in subclass if applicable."""
        return 0

    def get_game_state(self) -> Dict[str, Any]:
        """Get game state for saving. Override in subclass if applicable."""
        return {"score": self.get_score()}

    def load_game_state(self, state: Dict[str, Any]) -> None:
        """Load game state. Override in subclass if applicable."""
        pass

    def pause(self) -> None:
        """Pause the game."""
        self.paused = True

    def resume(self) -> None:
        """Resume the game."""
        self.paused = False

    def is_paused(self) -> bool:
        """Check if game is paused."""
        return self.paused

    def run(self) -> int:
        """
        Main game loop. Returns final score.
        Should be called by the game launcher.
        """
        self.running = True
        if not self.initialize():
            return 0

        try:
            # This is a placeholder loop structure
            # Each game implementation should override this
            # or implement their own main loop
            while self.running:
                self.update(0.016)  # Assume 60 FPS
                self.render()
                if not self.running:
                    break
        finally:
            self.cleanup()

        return self.get_score()

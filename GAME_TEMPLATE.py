"""
GAME CREATION GUIDE for omniGames

This template shows you how to create a custom game for omniGames.
Follow these steps:

1. Copy the omnigames/games/template_game.py file
2. Create your own game class inheriting from BaseGame
3. Implement all required methods
4. Create a game.json manifest
5. Test your game
6. Package as ZIP for distribution
"""

import pygame
from typing import Dict, Any
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from omnigames.core.base_game import BaseGame


class MyAwesomeGame(BaseGame):
    """Your custom game implementation."""

    def __init__(self, user_id: int, game_name: str):
        """
        Initialize your game.
        
        Args:
            user_id: The ID of the player (for saving per-user data)
            game_name: The name of your game
        """
        super().__init__(user_id, game_name)
        self.screen = None
        self.clock = None
        self.score = 0
        # Add your game-specific attributes here

    def initialize(self) -> bool:
        """
        Initialize pygame and game resources.
        
        Called once at the start of the game.
        Return True if initialization successful, False otherwise.
        """
        try:
            pygame.init()
            self.screen = pygame.display.set_mode((800, 600))
            pygame.display.set_caption("My Awesome Game")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font(None, 36)
            
            # Initialize your game resources here
            # Load images, sounds, setup game state, etc.
            
            return True
        except Exception as e:
            print(f"Initialization error: {e}")
            return False

    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Handle pygame events (input, window, etc).
        
        This is called for every event in the event queue.
        """
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
            # Handle other keys
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle mouse clicks
            pos = pygame.mouse.get_pos()
            # Do something with the position

    def update(self, dt: float) -> None:
        """
        Update game logic.
        
        Called every frame.
        dt = time elapsed since last frame in seconds
        """
        if self.paused:
            return
        
        # Update game state
        # Move objects, check collisions, update AI, etc.
        # Example: update player position based on input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            pass  # Move left
        if keys[pygame.K_RIGHT]:
            pass  # Move right

    def render(self) -> None:
        """
        Render/draw the game.
        
        This should draw all graphics for the current frame.
        """
        # Clear screen
        self.screen.fill((0, 0, 0))  # Black background
        
        # Draw game elements
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        # Update display
        pygame.display.flip()

    def cleanup(self) -> None:
        """
        Clean up resources.
        
        Called when the game exits.
        Close files, release resources, quit pygame, etc.
        """
        pygame.quit()

    def get_score(self) -> int:
        """
        Return the player's final score.
        
        This is used for high score tracking.
        """
        return self.score

    def get_game_state(self) -> Dict[str, Any]:
        """
        Optional: Return game state for saving.
        
        This allows players to save progress.
        Returns a dictionary that will be stored in the database.
        """
        return {"score": self.score, "level": 1}  # Add your game state

    def load_game_state(self, state: Dict[str, Any]) -> None:
        """
        Optional: Load previously saved game state.
        
        Called to restore a saved game.
        """
        self.score = state.get("score", 0)
        # Load other state variables

    def run(self) -> int:
        """
        Main game loop.
        
        This is called to run your game. Don't override unless needed.
        Returns the final score.
        """
        self.running = True
        if not self.initialize():
            return 0

        try:
            while self.running:
                # Calculate delta time for frame-rate independent movement
                dt = self.clock.tick(60) / 1000.0  # 60 FPS

                # Handle events
                for event in pygame.event.get():
                    self.handle_event(event)

                # Update game logic
                if not self.paused:
                    self.update(dt)

                # Render
                self.render()
        finally:
            self.cleanup()

        return self.get_score()


def main(user_id: int) -> int:
    """
    Entry point for your game.
    
    IMPORTANT: Every game must have a main() function with this signature!
    It receives the user_id and must return the final score.
    
    Args:
        user_id: The ID of the player
        
    Returns:
        The final score
    """
    game = MyAwesomeGame(user_id, "my_awesome_game")
    return game.run()


# For testing your game directly
if __name__ == "__main__":
    # Test with user_id = 1
    final_score = main(1)
    print(f"Game ended. Final score: {final_score}")


# ============================================================================
# CREATING A GAME PACKAGE
# ============================================================================
#
# Once your game is complete, package it for distribution:
#
# 1. Create folder structure:
#    my_awesome_game/
#    ├── game.json
#    ├── main.py (your game code)
#    └── assets/
#        └── thumbnail.png (optional - 300x200 recommended)
#
# 2. game.json should contain:
#    {
#      "name": "my_awesome_game",
#      "title": "My Awesome Game",
#      "description": "A fun and awesome game",
#      "version": "1.0.0",
#      "author": "Your Name",
#      "main_module": "main",
#      "icon": "assets/thumbnail.png"
#    }
#
# 3. Create ZIP file:
#    Windows PowerShell:
#      Compress-Archive -Path my_awesome_game -DestinationPath my_awesome_game.zip
#
#    Linux/macOS:
#      zip -r my_awesome_game.zip my_awesome_game/
#
# 4. Install in omniGames:
#    Run omniGames -> Install Game -> Select ZIP file
#
# ============================================================================
# USING THE DATABASE FOR USER DATA
# ============================================================================
#
# Save and load user-specific game data:
#
#   from omnigames.core import db
#   
#   # Save game data
#   game_state = {"level": 2, "items": ["sword", "shield"]}
#   db.save_game_data(user_id, "my_awesome_game", json.dumps(game_state))
#   
#   # Load game data
#   data_json = db.load_game_data(user_id, "my_awesome_game")
#   if data_json:
#       import json
#       game_state = json.loads(data_json)
#
# ============================================================================
# KEYBOARD CODES
# ============================================================================
#
# Common pygame key codes:
#   pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT
#   pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE
#   pygame.K_a, pygame.K_b, ... pygame.K_z (for letters)
#   pygame.K_0, pygame.K_1, ... pygame.K_9 (for numbers)
#
# ============================================================================
# TIPS
# ============================================================================
#
# 1. Use delta time (dt) for frame-rate independent movement
# 2. Keep the main loop running smoothly - offload heavy work
# 3. Store user data using the database API
# 4. Return a score that reflects game difficulty/performance
# 5. Test on target system before packaging
# 6. Include a thumbnail image for the game menu
# 7. Document your game controls
# 8. Handle window close gracefully
#
# ============================================================================

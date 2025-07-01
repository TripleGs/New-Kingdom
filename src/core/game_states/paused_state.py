import pygame

from core.game_states.game_state import GameState, GameStateType


class PausedState(GameState):
    """Paused game state"""
    
    def enter(self):
        pass
        
    def exit(self):
        pass
        
    def update(self, dt: float):
        pass
        
    def handle_input(self, events: list):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.state_manager.change_state(GameStateType.PLAYING)
                    
    def render(self, screen):
        # Render paused overlay
        pass
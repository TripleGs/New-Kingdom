from core.game_states.game_state import GameState


class PlayingState(GameState):
    """Main gameplay state"""
    
    def enter(self):
        pass
        
    def exit(self):
        pass
        
    def update(self, dt: float):
        # Update game objects
        pass
        
    def handle_input(self, events: list):
        # Handle gameplay input
        pass
        
    def render(self, screen):
        # Render game world
        pass
from typing import Dict
from core.game_states.game_state import GameState, GameStateType


class GameStateManager:
    """Manages game state transitions"""
    
    def __init__(self):
        self.states: Dict[GameStateType, GameState] = {}
        self.current_state: GameState = None
        self.current_state_type: GameStateType = None
        
    def add_state(self, state_type: GameStateType, state: GameState):
        """Add a state to the manager"""
        self.states[state_type] = state
        
    def change_state(self, new_state_type: GameStateType):
        """Change to a new state"""
        if new_state_type not in self.states:
            raise ValueError(f"State {new_state_type} not found")
            
        if self.current_state:
            self.current_state.exit()
            
        self.current_state_type = new_state_type
        self.current_state = self.states[new_state_type]
        self.current_state.enter()
        
    def update(self, dt: float):
        """Update current state"""
        if self.current_state:
            self.current_state.update(dt)
            
    def handle_input(self, events: list):
        """Handle input for current state"""
        if self.current_state:
            self.current_state.handle_input(events)
            
    def render(self, screen):
        """Render current state"""
        if self.current_state:
            self.current_state.render(screen) 
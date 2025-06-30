"""
Game State Management
Handles different game states (menu, playing, paused, game over, etc.)
"""

from enum import Enum
from abc import ABC, abstractmethod
from typing import Dict, Any
import pygame


class GameStateType(Enum):
    """Different game states"""
    MENU = "menu"
    PLAYING = "playing" 
    PAUSED = "paused"
    EXPLODING = "exploding"
    GAME_OVER = "game_over"


class GameState(ABC):
    """Abstract base class for game states"""
    
    def __init__(self, state_manager):
        self.state_manager = state_manager
        
    @abstractmethod
    def enter(self):
        """Called when entering this state"""
        pass
        
    @abstractmethod
    def exit(self):
        """Called when exiting this state"""
        pass
        
    @abstractmethod
    def update(self, dt: float):
        """Update the state"""
        pass
        
    @abstractmethod
    def handle_input(self, events: list):
        """Handle input events"""
        pass
        
    @abstractmethod
    def render(self, screen):
        """Render the state"""
        pass


class MenuState(GameState):
    """Menu/attract mode state"""
    
    def enter(self):
        pass
        
    def exit(self):
        pass
        
    def update(self, dt: float):
        pass
        
    def handle_input(self, events: list):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.state_manager.change_state(GameStateType.PLAYING)
                    
    def render(self, screen):
        # Render menu/attract screen
        pass


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
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
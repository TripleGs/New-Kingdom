#!/usr/bin/env python3

import pygame
import sys
import os

# Add the src directory to the Python path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.game import Game
from src.audio.soundManager import initSoundManager

def main():
    # Check for pygame components
    if not pygame.font:
        print('Warning, fonts disabled')
    if not pygame.mixer:
        print('Warning, sound disabled')
    
    # Initialize sound system
    initSoundManager()
    
    # Create and run the game
    game = Game()
    game.playGame()

if __name__ == "__main__":
    main() 
import pygame
from ..config.config import FONT_PATH, FONT_SIZES

# UI
from ..ui.rescue_ui import RescueUI

class RescueSystem:
    """Handles rescue operations when player runs out of fuel"""
    
    def __init__(self, game):
        self.game = game
        self.rescueCost = 100  # Cost of rescue service
        self.emergencyFuel = 10  # Amount of fuel given after rescue
        
        # UI
        self.ui = RescueUI(self)
        
    def displayRescuePrompt(self):
        """Display rescue prompt when out of fuel"""
        if not self.game.showRescuePrompt:
            return
            
        # Semi-transparent overlay
        overlay = pygame.Surface((self.game.stage.width, self.game.stage.height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.game.stage.screen.blit(overlay, (0, 0))
        
        # Delegate drawing to UI
        self.ui.draw(self.game.stage.screen)
    
    def handleRescueRequest(self):
        """Handle rescue service request"""
        if self.game.money >= self.rescueCost:
            self.game.money -= self.rescueCost
            self.rescueShip()
            return True
        else:
            # Not enough money for rescue
            return False
    
    def rescueShip(self):
        """Rescue the ship and return it to the space station"""
        if self.game.ship and self.game.spaceStation:
            # Move ship to space station
            self.game.ship.position.x = self.game.spaceStation.position.x - 100
            self.game.ship.position.y = self.game.spaceStation.position.y
            self.game.ship.thrustJet.position.x = self.game.ship.position.x
            self.game.ship.thrustJet.position.y = self.game.ship.position.y
            
            # Give some emergency fuel (enough to dock)
            self.game.ship.fuel = self.emergencyFuel
            
            # Reset fuel status
            self.game.outOfFuel = False
            self.game.showRescuePrompt = False
            
            # Focus camera on ship
            self.game.camera.setTarget(self.game.ship)
            
            # Stop all movement
            self.game.ship.heading.x = 0
            self.game.ship.heading.y = 0
            # Also ensure thrust jet not accelerating
            self.game.ship.thrustJet.accelerating = False
    
    def isRescueNeeded(self):
        """Check if rescue is currently needed"""
        return self.game.showRescuePrompt
    
    def canAffordRescue(self):
        """Check if player can afford rescue service"""
        return self.game.money >= self.rescueCost 

    # ------------------------------------------------------------------
    def handle_event(self, event):
        """Pass pygame events to UI for buttons."""
        self.ui.handle_event(event) 
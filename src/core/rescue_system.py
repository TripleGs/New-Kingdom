import pygame
from ..config.config import FONT_PATH, FONT_SIZES

class RescueSystem:
    """Handles rescue operations when player runs out of fuel"""
    
    def __init__(self, game):
        self.game = game
        self.rescueCost = 100  # Cost of rescue service
        self.emergencyFuel = 10  # Amount of fuel given after rescue
        
    def displayRescuePrompt(self):
        """Display rescue prompt when out of fuel"""
        if not self.game.showRescuePrompt:
            return
            
        # Semi-transparent overlay
        overlay = pygame.Surface((self.game.stage.width, self.game.stage.height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.game.stage.screen.blit(overlay, (0, 0))
        
        font_title = pygame.font.Font(FONT_PATH, FONT_SIZES["subtitle"])
        font_text = pygame.font.Font(FONT_PATH, FONT_SIZES["normal"])
        
        title_text = font_title.render("OUT OF FUEL!", True, (255, 0, 0))
        title_rect = title_text.get_rect(centerx=self.game.stage.width//2, centery=self.game.stage.height//2 - 50)
        self.game.stage.screen.blit(title_text, title_rect)
        
        prompt_text = font_text.render("Press R to call for rescue", True, (255, 255, 255))
        prompt_rect = prompt_text.get_rect(centerx=self.game.stage.width//2, centery=self.game.stage.height//2)
        self.game.stage.screen.blit(prompt_text, prompt_rect)
        
        cost_text = font_text.render(f"(Rescue service will cost ${self.rescueCost})", True, (255, 255, 0))
        cost_rect = cost_text.get_rect(centerx=self.game.stage.width//2, centery=self.game.stage.height//2 + 30)
        self.game.stage.screen.blit(cost_text, cost_rect)
        
        # Show current money
        if self.game.money < self.rescueCost:
            money_text = font_text.render(f"Insufficient funds! You have ${self.game.money}", True, (255, 0, 0))
            money_rect = money_text.get_rect(centerx=self.game.stage.width//2, centery=self.game.stage.height//2 + 60)
            self.game.stage.screen.blit(money_text, money_rect)
    
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
    
    def isRescueNeeded(self):
        """Check if rescue is currently needed"""
        return self.game.showRescuePrompt
    
    def canAffordRescue(self):
        """Check if player can afford rescue service"""
        return self.game.money >= self.rescueCost 
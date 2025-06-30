import pygame
from ..config.config import FONT_PATH, FONT_SIZES

class FuelSystem:
    """Handles fuel display and fuel status management"""
    
    def __init__(self, game):
        self.game = game
        
    def displayFuelBar(self):
        """Display the fuel bar on screen"""
        if not self.game.ship:
            return
            
        font = pygame.font.Font(FONT_PATH, FONT_SIZES["small"])
        
        # Fuel bar dimensions and position
        bar_width = 200
        bar_height = 20
        bar_x = self.game.stage.width - bar_width - 20
        bar_y = 20
        
        # Draw fuel bar background
        pygame.draw.rect(self.game.stage.screen, (100, 100, 100), 
                        (bar_x, bar_y, bar_width, bar_height))
        
        # Calculate fuel bar fill
        fuel_percentage = self.game.ship.getFuelPercentage()
        fill_width = int((fuel_percentage / 100) * bar_width)
        
        # Choose color based on fuel level
        if fuel_percentage > 60:
            fuel_color = (0, 255, 0)  # Green
        elif fuel_percentage > 20:
            fuel_color = (255, 255, 0)  # Yellow
        else:
            fuel_color = (255, 0, 0)  # Red
            
        # Draw fuel fill
        if fill_width > 0:
            pygame.draw.rect(self.game.stage.screen, fuel_color,
                           (bar_x, bar_y, fill_width, bar_height))
        
        # Draw fuel bar border
        pygame.draw.rect(self.game.stage.screen, (255, 255, 255),
                        (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Draw fuel text
        fuel_text = font.render(f"FUEL: {int(fuel_percentage)}%", True, (255, 255, 255))
        fuel_text_rect = fuel_text.get_rect()
        fuel_text_rect.right = bar_x - 10
        fuel_text_rect.centery = bar_y + bar_height // 2
        self.game.stage.screen.blit(fuel_text, fuel_text_rect)
        
    def checkFuelStatus(self):
        """Check if player has run out of fuel"""
        if self.game.ship and not self.game.ship.hasFuel() and not self.game.outOfFuel:
            self.game.outOfFuel = True
            self.game.showRescuePrompt = True
            return True
        return False
    
    def getFuelCost(self, fuel_needed):
        """Calculate the cost for a given amount of fuel"""
        return int(fuel_needed * 3)  # $3 per fuel unit 
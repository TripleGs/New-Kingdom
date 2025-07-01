import pygame

# Local imports
from ..config.config import FONT_PATH, FONT_SIZES
from ..entities.crystal import Crystal

# UI
from ..ui.shop.buy_ui import ShopBuyUI
from ..ui.shop.sell_ui import ShopSellUI

class Shop:
    """Handles the space station shop interface and transactions"""
    
    def __init__(self, game):
        self.game = game
        self.fuelCostPerUnit = 3  # $3 per fuel unit
        self.shop_mode = "buy"  # "buy" or "sell"
        
        # Lazy create UI objects (need reference to self)
        self.buy_ui = ShopBuyUI(self)
        self.sell_ui = ShopSellUI(self)
        
    def display(self):
        """Display the shop interface"""
        if not self.game.showShop:
            return
            
        # Semi-transparent overlay
        overlay = pygame.Surface((self.game.stage.width, self.game.stage.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.game.stage.screen.blit(overlay, (0, 0))
        
        # Shop window
        shop_width = 400
        shop_height = 300
        shop_x = (self.game.stage.width - shop_width) // 2
        shop_y = (self.game.stage.height - shop_height) // 2
        
        pygame.draw.rect(self.game.stage.screen, (50, 50, 50),
                        (shop_x, shop_y, shop_width, shop_height))
        pygame.draw.rect(self.game.stage.screen, (0, 255, 255),
                        (shop_x, shop_y, shop_width, shop_height), 3)
        
        # Shop title
        title_font = pygame.font.Font(FONT_PATH, FONT_SIZES["subtitle"])
        mode_text = "BUY" if self.shop_mode == "buy" else "SELL"
        title_text = title_font.render(f"SPACE STATION - {mode_text}", True, (0, 255, 255))
        title_rect = title_text.get_rect(centerx=shop_x + shop_width//2, y=shop_y + 20)
        self.game.stage.screen.blit(title_text, title_rect)
        
        # Display UI for current mode
        if self.shop_mode == "buy":
            self.buy_ui.draw(self.game.stage.screen, shop_x, shop_y, shop_width, shop_height)
        else:
            self.sell_ui.draw(self.game.stage.screen, shop_x, shop_y, shop_width, shop_height)
        
        # Close instruction (ESC still works)
        instruction_font = pygame.font.Font(FONT_PATH, FONT_SIZES["small"])
        close_text = instruction_font.render("Press ESC to close", True, (200, 200, 200))
        self.game.stage.screen.blit(close_text, (shop_x + 40, shop_y + shop_height - 30))
    
    def handleFuelPurchase(self):
        """Handle fuel purchase transaction"""
        if not self.game.ship:
            return False
            
        fuel_needed = self.game.ship.maxFuel - self.game.ship.fuel
        fuel_cost = int(fuel_needed * self.fuelCostPerUnit)
        
        if self.game.money >= fuel_cost:
            self.game.money -= fuel_cost
            self.game.ship.refillFuel()
            return True
        else:
            # Not enough money
            return False
    
    def open(self):
        """Open the shop"""
        self.game.showShop = True
    
    def close(self):
        """Close the shop"""
        self.game.showShop = False
        self.shop_mode = "buy"  # Reset to buy mode when closing
    
    def toggleMode(self):
        """Toggle between buy and sell modes"""
        self.shop_mode = "sell" if self.shop_mode == "buy" else "buy"
    
    def handleCrystalSale(self, option):
        """Handle crystal sale transactions"""
        from ..entities.crystal import Crystal
        
        if option == 1:  # Coal
            money_earned = self.game.crystalSystem.sellCrystalType(Crystal.COAL)
        elif option == 2:  # Iron
            money_earned = self.game.crystalSystem.sellCrystalType(Crystal.IRON)
        elif option == 3:  # Gold
            money_earned = self.game.crystalSystem.sellCrystalType(Crystal.GOLD)
        elif option == 4:  # All crystals
            money_earned = self.game.crystalSystem.sellAllCrystals()
        else:
            return
        
        # Add money to player
        self.game.money += money_earned 

    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------
    def handle_event(self, event):
        """Pass pygame events down to active UI for button handling."""
        if self.shop_mode == "buy":
            self.buy_ui.handle_event(event)
        else:
            self.sell_ui.handle_event(event) 
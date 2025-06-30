import pygame
from ..config.config import FONT_PATH, FONT_SIZES
from ..entities.crystal import Crystal

class Shop:
    """Handles the space station shop interface and transactions"""
    
    def __init__(self, game):
        self.game = game
        self.fuelCostPerUnit = 3  # $3 per fuel unit
        self.shop_mode = "buy"  # "buy" or "sell"
        
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
        
        # Mode toggle instructions
        instruction_font = pygame.font.Font(FONT_PATH, FONT_SIZES["small"])
        toggle_text = instruction_font.render("Press TAB to switch buy/sell mode", True, (200, 200, 200))
        toggle_rect = toggle_text.get_rect(centerx=shop_x + shop_width//2, y=shop_y + 45)
        self.game.stage.screen.blit(toggle_text, toggle_rect)
        
        if self.shop_mode == "buy":
            self.displayBuyMode(shop_x, shop_y, shop_width, shop_height)
        else:
            self.displaySellMode(shop_x, shop_y, shop_width, shop_height)
            
        # Common instructions
        instruction2 = instruction_font.render("Press ESC to close", True, (200, 200, 200))
        instruction2_rect = instruction2.get_rect(x=shop_x + 40, y=shop_y + 250)
        self.game.stage.screen.blit(instruction2, instruction2_rect)
    
    def displayBuyMode(self, shop_x, shop_y, shop_width, shop_height):
        """Display buy mode interface"""
        option_font = pygame.font.Font(FONT_PATH, FONT_SIZES["normal"])
        instruction_font = pygame.font.Font(FONT_PATH, FONT_SIZES["small"])
        
        # Fuel refill option
        if self.game.ship:
            fuel_needed = self.game.ship.maxFuel - self.game.ship.fuel
            fuel_cost = int(fuel_needed * self.fuelCostPerUnit)
            
            fuel_text = option_font.render(f"1. Refill Fuel Tank - ${fuel_cost}", True, (255, 255, 255))
            fuel_rect = fuel_text.get_rect(x=shop_x + 40, y=shop_y + 80)
            self.game.stage.screen.blit(fuel_text, fuel_rect)
        
        # Instructions
        instruction1 = instruction_font.render("Press 1 to refill fuel", True, (200, 200, 200))
        instruction1_rect = instruction1.get_rect(x=shop_x + 40, y=shop_y + 160)
        self.game.stage.screen.blit(instruction1, instruction1_rect)
        
        # Current fuel status and money
        if self.game.ship:
            fuel_status = instruction_font.render(f"Current Fuel: {int(self.game.ship.getFuelPercentage())}%", 
                                                True, (255, 255, 0))
            fuel_status_rect = fuel_status.get_rect(x=shop_x + 40, y=shop_y + 120)
            self.game.stage.screen.blit(fuel_status, fuel_status_rect)
            
            money_status = instruction_font.render(f"Your Money: ${self.game.money}", 
                                                 True, (0, 255, 0))
            money_status_rect = money_status.get_rect(x=shop_x + 40, y=shop_y + 140)
            self.game.stage.screen.blit(money_status, money_status_rect)
    
    def displaySellMode(self, shop_x, shop_y, shop_width, shop_height):
        """Display sell mode interface"""
        option_font = pygame.font.Font(FONT_PATH, FONT_SIZES["normal"])
        instruction_font = pygame.font.Font(FONT_PATH, FONT_SIZES["small"])
        
        # Get actual crystal counts from the bin
        crystal_counts = self.game.crystalSystem.getCrystalCounts()
        
        # Crystal selling options
        y_offset = 80
        crystal_types = [Crystal.COAL, Crystal.IRON, Crystal.GOLD]
        
        for i, crystal_type in enumerate(crystal_types):
            count = crystal_counts[crystal_type]
            name = Crystal.crystal_types[crystal_type]["name"]
            value = Crystal.crystal_types[crystal_type]["value"]
            total_value = count * value
            
            color = Crystal.crystal_types[crystal_type]["color"]
            option_text = option_font.render(f"{i+1}. Sell {name} ({count}) - ${total_value}", True, color)
            option_rect = option_text.get_rect(x=shop_x + 40, y=shop_y + y_offset + (i * 25))
            self.game.stage.screen.blit(option_text, option_rect)
        
        # Sell all option
        total_value = self.game.crystalSystem.getTotalValue()
        sell_all_text = option_font.render(f"4. Sell All Crystals - ${total_value}", True, (255, 255, 255))
        sell_all_rect = sell_all_text.get_rect(x=shop_x + 40, y=shop_y + y_offset + 80)
        self.game.stage.screen.blit(sell_all_text, sell_all_rect)
        
        # Instructions
        instructions = [
            "Press 1-3 to sell crystal type",
            "Press 4 to sell all crystals",
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = instruction_font.render(instruction, True, (200, 200, 200))
            inst_rect = inst_text.get_rect(x=shop_x + 40, y=shop_y + 200 + (i * 15))
            self.game.stage.screen.blit(inst_text, inst_rect)
        
        # Current money
        money_status = instruction_font.render(f"Your Money: ${self.game.money}", 
                                             True, (0, 255, 0))
        money_status_rect = money_status.get_rect(x=shop_x + 40, y=shop_y + 180)
        self.game.stage.screen.blit(money_status, money_status_rect)
    
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
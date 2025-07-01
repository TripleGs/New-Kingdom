import pygame
import math
import random

from core.crystal_system.bin_crystal import BinCrystal
from ...config.config import FONT_PATH, FONT_SIZES
from ...entities.crystal import Crystal

class CrystalSystem:
    """Handles crystal collection, storage, and physics-based bin display"""
    
    def __init__(self, game):
        self.game = game
        
        # Physical crystals in the bin
        self.bin_crystals = []
        
        # Visual bin properties
        self.bin_width = 300
        self.bin_height = 120  # Increased height for crystal physics
        self.bin_x = (game.stage.width - self.bin_width) // 2
        self.bin_y = 10
        
        # Bin physics bounds (inner area where crystals can exist)
        self.bin_inner_x = self.bin_x + 5
        self.bin_inner_y = self.bin_y + 30  # Below the title
        self.bin_inner_width = self.bin_width - 10
        self.bin_inner_height = self.bin_height - 35
        
    def addCrystal(self, crystal_type, amount=1):
        """Add crystals to the bin with physics"""
        for _ in range(amount):
            # Drop crystals from random positions at the top of the bin
            drop_x = self.bin_inner_x + random.randint(20, self.bin_inner_width - 20)
            drop_y = self.bin_inner_y - 10  # Just above the bin
            
            bin_crystal = BinCrystal(crystal_type, drop_x, drop_y)
            self.bin_crystals.append(bin_crystal)
    
    def collectNearbyCrystals(self, ship):
        """Collect crystals near the ship"""
        collected_crystals = []
        
        # Get all crystals from universe
        crystals_in_universe = [obj for obj in self.game.universe.objects if isinstance(obj, Crystal)]
        
        for crystal in crystals_in_universe:
            if crystal.canBeCollectedBy(ship):
                crystal.collect()
                self.addCrystal(crystal.crystal_type)
                collected_crystals.append(crystal)
                # Remove from universe
                self.game.universe.removeObject(crystal)
                
        return collected_crystals
    
    def displayCrystalBin(self):
        """Display the physics-based crystal bin"""
        # Draw bin background
        pygame.draw.rect(self.game.stage.screen, (40, 40, 40),
                        (self.bin_x, self.bin_y, self.bin_width, self.bin_height))
        pygame.draw.rect(self.game.stage.screen, (100, 100, 100),
                        (self.bin_x, self.bin_y, self.bin_width, self.bin_height), 2)
        
        # Draw bin title
        font_small = pygame.font.Font(FONT_PATH, FONT_SIZES["small"])
        title_text = font_small.render("CRYSTAL COLLECTION BIN", True, (255, 255, 255))
        title_rect = title_text.get_rect(centerx=self.bin_x + self.bin_width//2, y=self.bin_y + 5)
        self.game.stage.screen.blit(title_text, title_rect)
        
        # Update and draw all bin crystals
        bin_bounds = (self.bin_inner_x, self.bin_inner_y, self.bin_inner_width, self.bin_inner_height)
        
        for crystal in self.bin_crystals:
            crystal.update(bin_bounds, self.bin_crystals)
            crystal.draw(self.game.stage.screen)
        
        # Draw crystal count summary in corner
        self.drawCrystalCounts()
    
    def drawCrystalCounts(self):
        """Draw a small summary of crystal counts"""
        font_tiny = pygame.font.Font(FONT_PATH, FONT_SIZES["small"])
        
        # Count crystals by type
        counts = {Crystal.COAL: 0, Crystal.IRON: 0, Crystal.GOLD: 0}
        for crystal in self.bin_crystals:
            counts[crystal.crystal_type] += 1
        
        # Draw counts
        y_offset = self.bin_y + self.bin_height + 5
        for i, (crystal_type, count) in enumerate(counts.items()):
            color = Crystal.crystal_types[crystal_type]["color"]
            name = Crystal.crystal_types[crystal_type]["name"]
            
            count_text = font_tiny.render(f"{name}: {count}", True, color)
            count_rect = count_text.get_rect(x=self.bin_x + (i * 80), y=y_offset)
            self.game.stage.screen.blit(count_text, count_rect)
    
    def getTotalValue(self):
        """Get total value of all crystals in the bin"""
        total = 0
        for crystal in self.bin_crystals:
            total += crystal.value
        return total
    
    def sellAllCrystals(self):
        """Sell all crystals and return money earned"""
        money_earned = self.getTotalValue()
        self.bin_crystals.clear()
        return money_earned
    
    def sellCrystalType(self, crystal_type):
        """Sell all crystals of a specific type"""
        money_earned = 0
        crystals_to_remove = []
        
        for crystal in self.bin_crystals:
            if crystal.crystal_type == crystal_type:
                money_earned += crystal.value
                crystals_to_remove.append(crystal)
        
        # Remove sold crystals
        for crystal in crystals_to_remove:
            self.bin_crystals.remove(crystal)
            
        return money_earned
    
    def getCrystalCounts(self):
        """Get count of each crystal type for shop display"""
        counts = {Crystal.COAL: 0, Crystal.IRON: 0, Crystal.GOLD: 0}
        for crystal in self.bin_crystals:
            counts[crystal.crystal_type] += 1
        return counts 
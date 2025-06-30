import pygame
import math
import random
from ..config.config import FONT_PATH, FONT_SIZES
from ..entities.crystal import Crystal

class BinCrystal:
    """A crystal that exists physically in the bin with collision physics"""
    
    def __init__(self, crystal_type, x, y):
        self.crystal_type = crystal_type
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)  # velocity x
        self.vy = random.uniform(-1, 1)  # velocity y
        self.radius = 6  # collision radius
        self.color = Crystal.crystal_types[crystal_type]["color"]
        self.value = Crystal.crystal_types[crystal_type]["value"]
        self.name = Crystal.crystal_types[crystal_type]["name"]
        
        # Physics properties
        self.gravity = 0.2
        self.friction = 0.98
        self.bounce_damping = 0.6
        self.settled = False
        self.settle_timer = 0
        self.total_settling_attempts = 0  # Track total time trying to settle
        self.max_settling_time = 300  # Force settle after 5 seconds (60fps * 5)
        
    def update(self, bin_bounds, other_crystals):
        """Update crystal physics"""
        if self.settled:
            return
        
        # Apply gravity
        self.vy += self.gravity
        
        # Limit velocity to prevent physics instability
        max_velocity = 8.0
        speed = math.sqrt(self.vx*self.vx + self.vy*self.vy)
        if speed > max_velocity:
            self.vx = (self.vx / speed) * max_velocity
            self.vy = (self.vy / speed) * max_velocity
        
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Store bin bounds for easier access
        bin_x, bin_y, bin_width, bin_height = bin_bounds
        
        # Collision with other crystals first
        for other in other_crystals:
            if other is self:
                continue
                
            dx = self.x - other.x
            dy = self.y - other.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Minimum distance to prevent divide by zero
            min_distance = self.radius + other.radius
            
            if distance < min_distance and distance > 0.1:
                # Normalize collision vector
                nx = dx / distance
                ny = dy / distance
                
                # Calculate overlap
                overlap = min_distance - distance
                
                # Check if the other crystal is settled
                if other.settled:
                    # Other crystal is settled and immovable
                    # Only move this crystal away from the settled one
                    self.x += nx * overlap
                    self.y += ny * overlap
                    
                    # Bounce off the settled crystal like a wall
                    # Calculate velocity component in collision normal direction
                    dvn = self.vx * nx + self.vy * ny
                    
                    # Only resolve if moving towards the settled crystal
                    if dvn < 0:
                        self.vx -= 2 * dvn * nx * 0.8  # Bounce with damping
                        self.vy -= 2 * dvn * ny * 0.8
                        
                elif self.settled:
                    # This crystal is settled, don't move it
                    # Move the other crystal away
                    other.x -= nx * overlap
                    other.y -= ny * overlap
                    
                    # Bounce the other crystal off this settled one
                    dvn = other.vx * (-nx) + other.vy * (-ny)
                    if dvn < 0:
                        other.vx -= 2 * dvn * (-nx) * 0.8
                        other.vy -= 2 * dvn * (-ny) * 0.8
                        
                else:
                    # Both crystals are moving - normal collision
                    # Separate crystals more carefully
                    separate_distance = overlap * 0.51  # Slightly more than half to prevent sticking
                    
                    self.x += nx * separate_distance
                    self.y += ny * separate_distance
                    other.x -= nx * separate_distance
                    other.y -= ny * separate_distance
                    
                    # Calculate relative velocity
                    dvx = self.vx - other.vx
                    dvy = self.vy - other.vy
                    
                    # Calculate relative velocity in collision normal direction
                    dvn = dvx * nx + dvy * ny
                    
                    # Do not resolve if velocities are separating
                    if dvn > 0:
                        continue
                    
                    # Calculate impulse scalar
                    impulse = 2 * dvn / 2  # Assuming equal mass
                    impulse *= 0.8  # Damping factor
                    
                    # Apply impulse
                    self.vx -= impulse * nx * 0.5
                    self.vy -= impulse * ny * 0.5
                    other.vx += impulse * nx * 0.5
                    other.vy += impulse * ny * 0.5
        
        # Enforce bin boundaries after all collisions
        # Left wall
        if self.x - self.radius < bin_x:
            self.x = bin_x + self.radius
            if not self.settled:  # Only bounce if not settled
                self.vx = abs(self.vx) * self.bounce_damping
            
        # Right wall  
        if self.x + self.radius > bin_x + bin_width:
            self.x = bin_x + bin_width - self.radius
            if not self.settled:  # Only bounce if not settled
                self.vx = -abs(self.vx) * self.bounce_damping
            
        # Bottom wall
        if self.y + self.radius > bin_y + bin_height:
            self.y = bin_y + bin_height - self.radius
            if not self.settled:  # Only bounce if not settled
                self.vy = -abs(self.vy) * self.bounce_damping
                self.vx *= self.friction
            
        # Top wall (crystals shouldn't go above bin)
        if self.y - self.radius < bin_y:
            self.y = bin_y + self.radius
            if not self.settled:  # Only bounce if not settled
                self.vy = abs(self.vy) * self.bounce_damping
        
        # Safety constraints - hard limits to prevent any escaping (applies to all crystals)
        self.x = max(bin_x + self.radius, min(self.x, bin_x + bin_width - self.radius))
        self.y = max(bin_y + self.radius, min(self.y, bin_y + bin_height - self.radius))
        
        # Check if crystal has settled
        settling_velocity_threshold = 0.15
        
        if abs(self.vx) < settling_velocity_threshold and abs(self.vy) < settling_velocity_threshold:
            self.settle_timer += 1
            self.total_settling_attempts += 1
            
            # Apply extra damping when trying to settle to reduce vibration
            self.vx *= 0.9
            self.vy *= 0.9
            
            # Normal settling condition
            if self.settle_timer > 30:  # 30 frames of minimal movement
                self.settled = True
                self.vx = 0
                self.vy = 0
                
        elif abs(self.vx) < 0.5 and abs(self.vy) < 0.5:
            # Crystal is moving slowly but not slow enough - still count as settling attempt
            self.total_settling_attempts += 1
            self.settle_timer = 0  # Reset precise settling timer
            
            # Apply mild damping to help it settle
            self.vx *= 0.95
            self.vy *= 0.95
            
        else:
            # Crystal is moving too fast to be settling
            self.settle_timer = 0
            # Only reset total attempts if crystal is moving significantly
            if abs(self.vx) > 1.0 or abs(self.vy) > 1.0:
                self.total_settling_attempts = 0
        
        # Force settle if trying to settle for too long (prevents infinite vibration)
        if self.total_settling_attempts > self.max_settling_time:
            self.settled = True
            self.vx = 0
            self.vy = 0
            
    def draw(self, screen):
        """Draw the crystal as a diamond"""
        size = self.radius - 2
        crystal_points = [
            (self.x, self.y - size),      # top
            (self.x + size, self.y),      # right
            (self.x, self.y + size),      # bottom
            (self.x - size, self.y)       # left
        ]
        pygame.draw.polygon(screen, self.color, crystal_points)
        pygame.draw.polygon(screen, (255, 255, 255), crystal_points, 1)

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
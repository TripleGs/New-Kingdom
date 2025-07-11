import math
import random

import pygame

from entities.crystal import Crystal


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

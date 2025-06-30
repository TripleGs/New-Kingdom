#!/usr/bin/env python3

import pygame
import random
from ..util.vector2d import Vector2d
from ..config.config import SCREEN_WIDTH, SCREEN_HEIGHT


class Star:
    """A single star in the starfield"""
    
    def __init__(self, x, y, brightness=255, size=1, layer=0):
        self.x = x
        self.y = y
        self.brightness = brightness
        self.size = size
        self.layer = layer  # Layer determines parallax speed
        self.color = (brightness, brightness, brightness)
        
    def draw(self, surface, camera_offset_x, camera_offset_y, parallax_factor):
        """Draw the star with parallax offset"""
        # Calculate parallax position
        screen_x = self.x - (camera_offset_x * parallax_factor)
        screen_y = self.y - (camera_offset_y * parallax_factor)
        
        # Wrap around screen edges for infinite scrolling
        screen_x = screen_x % SCREEN_WIDTH
        screen_y = screen_y % SCREEN_HEIGHT
        
        if self.size == 1:
            surface.set_at((int(screen_x), int(screen_y)), self.color)
        else:
            pygame.draw.circle(surface, self.color, (int(screen_x), int(screen_y)), self.size)


class StarField:
    """Optimized starfield background with multiple parallax layers"""
    
    def __init__(self, num_layers=3):
        self.num_layers = num_layers
        self.star_layers = []
        self.parallax_factors = []
        
        # Initialize star layers with different densities and parallax speeds
        base_star_count = 150
        
        for layer in range(num_layers):
            stars = []
            layer_factor = (layer + 1) / num_layers
            
            # More distant stars move slower and are dimmer
            parallax_factor = 0.1 + (layer * 0.3)  # 0.1, 0.4, 0.7
            star_count = int(base_star_count * (1.5 - layer_factor))  # Fewer stars in distant layers
            
            self.parallax_factors.append(parallax_factor)
            
            # Generate stars for this layer
            for _ in range(star_count):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                
                # Distant layers have dimmer, smaller stars
                if layer == 0:  # Closest layer
                    brightness = random.randint(180, 255)
                    size = random.choice([1, 1, 1, 2])  # Mostly size 1, some size 2
                elif layer == 1:  # Middle layer
                    brightness = random.randint(120, 200)
                    size = 1
                else:  # Distant layer
                    brightness = random.randint(60, 150)
                    size = 1
                
                star = Star(x, y, brightness, size, layer)
                stars.append(star)
            
            self.star_layers.append(stars)
        
        # Pre-create surface for stars to optimize drawing
        self.star_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.star_surface.set_colorkey((0, 0, 0))  # Black is transparent
        
        # Cache last camera position to avoid unnecessary redraws
        self.last_camera_x = 0
        self.last_camera_y = 0
        self.cache_threshold = 5  # Redraw if camera moved more than this many pixels
        
    def update(self, camera):
        """Update starfield based on camera position"""
        # Only redraw if camera moved significantly
        camera_moved = (abs(camera.x - self.last_camera_x) > self.cache_threshold or
                       abs(camera.y - self.last_camera_y) > self.cache_threshold)
        
        if camera_moved:
            self._redraw_stars(camera.x, camera.y)
            self.last_camera_x = camera.x
            self.last_camera_y = camera.y
    
    def _redraw_stars(self, camera_x, camera_y):
        """Redraw all stars with current camera position"""
        # Clear the star surface
        self.star_surface.fill((0, 0, 0))
        
        # Draw each layer with its parallax factor
        for layer_idx, stars in enumerate(self.star_layers):
            parallax_factor = self.parallax_factors[layer_idx]
            
            for star in stars:
                star.draw(self.star_surface, camera_x, camera_y, parallax_factor)
    
    def draw(self, surface):
        """Draw the starfield to the given surface"""
        surface.blit(self.star_surface, (0, 0))
    
    def regenerate_layer(self, layer_idx):
        """Regenerate stars for a specific layer (useful for dynamic changes)"""
        if 0 <= layer_idx < len(self.star_layers):
            # Force regeneration by clearing cache
            self.last_camera_x = float('inf')
            self.last_camera_y = float('inf')


class BackgroundManager:
    """Main background manager that coordinates all background elements"""
    
    def __init__(self, camera):
        self.camera = camera
        self.starfield = StarField(num_layers=3)
        
        # Force initial draw
        self.starfield.update(camera)
    
    def update(self):
        """Update all background elements"""
        self.starfield.update(self.camera)
    
    def draw(self, surface):
        """Draw all background elements"""
        # Fill with deep space color
        surface.fill((5, 5, 15))  # Very dark blue-black
        
        # Draw starfield
        self.starfield.draw(surface)
    
    def set_star_density(self, density_multiplier):
        """Adjust star density (1.0 = normal, 0.5 = half, 2.0 = double)"""
        # This would require regenerating the starfield
        if 0.1 <= density_multiplier <= 5.0:
            # Regenerate with new density
            base_count = 150
            new_count = int(base_count * density_multiplier)
            # Implementation would regenerate star layers with new counts
            pass 
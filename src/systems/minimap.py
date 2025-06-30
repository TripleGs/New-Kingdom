import pygame
import math
from ..util.vector2d import Vector2d


class MiniMap:
    def __init__(self, universe, screen_width, screen_height):
        self.universe = universe
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Mini map dimensions and position
        self.map_size = 200  # 200x200 pixel mini map
        self.map_x = screen_width - self.map_size - 20  # 20 pixels from right edge
        self.map_y = 20  # 20 pixels from top
        
        # Create mini map surface
        self.surface = pygame.Surface((self.map_size, self.map_size))
        self.surface.set_alpha(180)  # Semi-transparent
        
        # Colors for different objects
        self.colors = {
            'background': (10, 10, 30),
            'border': (100, 100, 100),
            'player': (0, 255, 0),
            'space_station': (0, 100, 255),
            'asteroid_belt': (150, 150, 150),
            'rock': (100, 100, 100),
            'saucer': (255, 0, 0),
            'debris': (80, 80, 80)
        }
        
    def worldToMapCoords(self, world_x, world_y):
        """Convert world coordinates to mini map coordinates"""
        # Scale world coordinates to map coordinates
        map_x = int((world_x / self.universe.width) * self.map_size)
        map_y = int((world_y / self.universe.height) * self.map_size)
        return map_x, map_y
    
    def draw(self, screen):
        """Draw the mini map on the screen"""
        # Clear the mini map surface
        self.surface.fill(self.colors['background'])
        
        # Draw border
        pygame.draw.rect(self.surface, self.colors['border'], 
                        (0, 0, self.map_size, self.map_size), 2)
        
        # Draw individual rocks (make them more prominent)
        self.drawRocks()
        
        # Draw space station
        self.drawSpaceStation()
        
        # Draw saucer if present
        self.drawSaucer()
        
        # Draw debris (small dots)
        self.drawDebris()
        
        # Draw player ship (always on top)
        self.drawPlayer()
        
        # Draw mini map title
        self.drawTitle()
        
        # Blit the mini map to the main screen
        screen.blit(self.surface, (self.map_x, self.map_y))
    
    def drawRocks(self):
        """Draw individual rocks as more noticeable dots"""
        for rock in self.universe.rocks:
            map_x, map_y = self.worldToMapCoords(rock.position.x, rock.position.y)
            # Make sure the rock is within the mini map bounds
            if 0 <= map_x < self.map_size and 0 <= map_y < self.map_size:
                # Different colors and sizes for different rock materials and types
                radius = 2  # Base radius - larger than before
                
                if hasattr(rock, 'materialType'):
                    if rock.materialType == 2:  # Gold
                        color = (255, 215, 0)  # Brighter gold
                        radius = 3  # Make gold rocks more prominent
                    elif rock.materialType == 1:  # Iron
                        color = (180, 180, 180)  # Brighter silver
                        radius = 2
                    else:  # Coal
                        color = (120, 120, 120)  # Brighter gray
                        radius = 2
                else:
                    color = (150, 150, 150)  # Default bright gray
                    radius = 2
                
                # Make large rocks even more visible
                if hasattr(rock, 'rockType'):
                    if rock.rockType == 0:  # Large rock
                        radius += 1
                
                # Draw the rock with a small border for better visibility
                pygame.draw.circle(self.surface, (255, 255, 255), (map_x, map_y), radius + 1)
                pygame.draw.circle(self.surface, color, (map_x, map_y), radius)
    
    def drawPlayer(self):
        """Draw the player ship"""
        if self.universe.ship:
            map_x, map_y = self.worldToMapCoords(self.universe.ship.position.x, 
                                               self.universe.ship.position.y)
            # Make sure the player is within the mini map bounds
            if 0 <= map_x < self.map_size and 0 <= map_y < self.map_size:
                # Draw player as a bright green dot with a direction indicator
                pygame.draw.circle(self.surface, self.colors['player'], (map_x, map_y), 3)
                
                # Draw direction indicator
                if hasattr(self.universe.ship, 'angle'):
                    angle_rad = math.radians(self.universe.ship.angle)
                    end_x = map_x + int(6 * math.sin(angle_rad))
                    end_y = map_y + int(6 * math.cos(angle_rad))
                    pygame.draw.line(self.surface, self.colors['player'], 
                                   (map_x, map_y), (end_x, end_y), 2)
    
    def drawSpaceStation(self):
        """Draw the space station"""
        # Find space station in universe objects
        space_station = None
        for obj in self.universe.objects:
            if hasattr(obj, '__class__') and obj.__class__.__name__ == 'SpaceStation':
                space_station = obj
                break
        
        if space_station:
            map_x, map_y = self.worldToMapCoords(space_station.position.x, 
                                               space_station.position.y)
            # Make sure the station is within the mini map bounds
            if 0 <= map_x < self.map_size and 0 <= map_y < self.map_size:
                # Draw station as a blue square
                pygame.draw.rect(self.surface, self.colors['space_station'], 
                               (map_x - 2, map_y - 2, 4, 4))
    
    def drawSaucer(self):
        """Draw the saucer if present"""
        if self.universe.saucer:
            map_x, map_y = self.worldToMapCoords(self.universe.saucer.position.x, 
                                               self.universe.saucer.position.y)
            # Make sure the saucer is within the mini map bounds
            if 0 <= map_x < self.map_size and 0 <= map_y < self.map_size:
                # Draw saucer as a red triangle
                points = [(map_x, map_y - 3), (map_x - 3, map_y + 2), (map_x + 3, map_y + 2)]
                pygame.draw.polygon(self.surface, self.colors['saucer'], points)
    
    def drawDebris(self):
        """Draw debris as small gray dots"""
        debris_count = 0
        for debris in self.universe.debris:
            if debris_count > 50:  # Limit debris drawing for performance
                break
            map_x, map_y = self.worldToMapCoords(debris.position.x, debris.position.y)
            # Make sure the debris is within the mini map bounds
            if 0 <= map_x < self.map_size and 0 <= map_y < self.map_size:
                pygame.draw.circle(self.surface, self.colors['debris'], (map_x, map_y), 1)
                debris_count += 1
    
    def drawTitle(self):
        """Draw mini map title"""
        try:
            font = pygame.font.Font(None, 16)
            title_text = font.render("Galaxy Map", True, (255, 255, 255))
            self.surface.blit(title_text, (5, 5))
        except:
            # Fallback if font loading fails
            pass
    
    def isPointInMiniMap(self, screen_x, screen_y):
        """Check if a screen coordinate is within the mini map area"""
        return (self.map_x <= screen_x <= self.map_x + self.map_size and 
                self.map_y <= screen_y <= self.map_y + self.map_size)
    
    def screenToWorldCoords(self, screen_x, screen_y):
        """Convert screen coordinates (within mini map) to world coordinates"""
        if not self.isPointInMiniMap(screen_x, screen_y):
            return None
        
        # Convert to mini map local coordinates
        local_x = screen_x - self.map_x
        local_y = screen_y - self.map_y
        
        # Scale to world coordinates
        world_x = (local_x / self.map_size) * self.universe.width
        world_y = (local_y / self.map_size) * self.universe.height
        
        return Vector2d(world_x, world_y) 
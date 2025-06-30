import random
import math
from ..util.vectorsprites import *

class Crystal(VectorSprite):
    """Collectible crystals that drop from destroyed small rocks"""
    
    # Crystal types and their properties
    COAL = 0
    IRON = 1 
    GOLD = 2
    
    crystal_types = {
        COAL: {"color": (64, 64, 64), "name": "Coal", "value": 1},
        IRON: {"color": (169, 169, 169), "name": "Iron", "value": 3}, 
        GOLD: {"color": (255, 215, 0), "name": "Gold", "value": 10}
    }
    
    def __init__(self, position, stage, crystal_type=COAL):
        # Random velocity for crystal scatter (reduced for easier collection)
        velocity = random.uniform(0.5, 1.5)
        angle = random.uniform(0, 2 * math.pi)
        heading = Vector2d(velocity * math.cos(angle), velocity * math.sin(angle))
        
        # Create diamond shape pointlist
        size = 4
        diamond_points = [
            (0, -size),      # top
            (size, 0),       # right
            (0, size),       # bottom
            (-size, 0)       # left
        ]
        
        VectorSprite.__init__(self, position, heading, diamond_points)
        
        self.stage = stage
        self.crystal_type = crystal_type
        self.color = Crystal.crystal_types[crystal_type]["color"]
        self.value = Crystal.crystal_types[crystal_type]["value"]
        self.name = Crystal.crystal_types[crystal_type]["name"]
        
        # Collection properties
        self.collected = False
        self.collection_radius = 40  # Distance within which ship can collect (increased for easier pickup)
        self.ttl = 600  # Crystals disappear after 10 seconds (60fps * 10)
        
        # Visual properties
        self.pulse_counter = 0
        self.base_color = self.color
        
    def move(self):
        VectorSprite.move(self)
        
        # Add some glitter effect
        self.pulse_counter += 1
        pulse = abs(math.sin(self.pulse_counter * 0.1))
        
        # Pulse the brightness
        r, g, b = self.base_color
        brightness = 0.7 + (0.3 * pulse)
        self.color = (int(r * brightness), int(g * brightness), int(b * brightness))
        
        # Apply friction to slow down over time (reduced friction for more movement)
        self.heading.x *= 0.995
        self.heading.y *= 0.995
        
        # Reduce TTL
        self.ttl -= 1
        
    def canBeCollectedBy(self, ship):
        """Check if the ship is close enough to collect this crystal"""
        if ship is None or self.collected:
            return False
            
        distance = ((self.position.x - ship.position.x) ** 2 + 
                   (self.position.y - ship.position.y) ** 2) ** 0.5
        return distance <= self.collection_radius
        
    def collect(self):
        """Mark this crystal as collected"""
        self.collected = True
        self.ttl = 0  # Remove from game
        
 
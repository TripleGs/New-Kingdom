"""
Object Factories
Centralized object creation with proper dependency injection
"""

import random
from ..util.vector2d import Vector2d
from ..entities.ship import Ship, ThrustJet
from ..entities.rock import Rock
from ..entities.saucer import Saucer
from ..entities.debris import Debris
from .config import *


class GameObjectFactory:
    """Base factory for game objects"""
    
    def __init__(self, universe, stage):
        self.universe = universe
        self.stage = stage


class ShipFactory(GameObjectFactory):
    """Factory for creating ships"""
    
    def create_ship(self, position: Vector2d = None) -> Ship:
        """Create a new ship at the specified position"""
        if position is None:
            position = Vector2d(UNIVERSE_WIDTH // 2, UNIVERSE_HEIGHT // 2)
            
        ship = Ship(self.stage)
        ship.position = position
        ship.universe = self.universe
        
        # Configure ship with settings from config
        ship.acceleration = SHIP_ACCELERATION
        ship.decelaration = SHIP_DECELERATION
        ship.maxVelocity = SHIP_MAX_VELOCITY
        ship.turnAngle = SHIP_TURN_ANGLE
        ship.bulletVelocity = SHIP_BULLET_VELOCITY
        ship.maxBullets = SHIP_MAX_BULLETS
        ship.bulletTtl = SHIP_BULLET_TTL
        
        # Create and configure thrust jet
        ship.thrustJet.position = Vector2d(position.x, position.y)
        
        return ship


class RockFactory(GameObjectFactory):
    """Factory for creating rocks"""
    
    def create_rock(self, position: Vector2d, rock_type: int) -> Rock:
        """Create a rock of the specified type at the given position"""
        rock = Rock(self.stage, position, rock_type)
        return rock
        
    def create_rock_field(self, center_position: Vector2d, count: int, 
                         min_distance: float = 200) -> list:
        """Create a field of rocks around a center position"""
        rocks = []
        
        for _ in range(count):
            # Generate position not too close to center
            while True:
                x = random.randrange(int(center_position.x - 1000), 
                                   int(center_position.x + 1000))
                y = random.randrange(int(center_position.y - 1000), 
                                   int(center_position.y + 1000))
                
                # Check distance from center
                distance = ((x - center_position.x) ** 2 + 
                           (y - center_position.y) ** 2) ** 0.5
                if distance >= min_distance:
                    break
                    
            position = Vector2d(x, y)
            rock = self.create_rock(position, ROCK_LARGE_TYPE)
            rocks.append(rock)
            
        return rocks
        
    def create_rock_fragments(self, parent_rock: Rock, count: int = 2) -> list:
        """Create smaller rock fragments from a destroyed rock"""
        if parent_rock.rockType == ROCK_SMALL_TYPE:
            return []  # Small rocks don't fragment
            
        # Determine new rock type
        if parent_rock.rockType == ROCK_LARGE_TYPE:
            new_type = ROCK_MEDIUM_TYPE
        else:  # MEDIUM
            new_type = ROCK_SMALL_TYPE
            
        fragments = []
        for _ in range(count):
            # Position fragments near the parent with some spread
            offset_x = random.randrange(-20, 20)
            offset_y = random.randrange(-20, 20)
            position = Vector2d(parent_rock.position.x + offset_x,
                              parent_rock.position.y + offset_y)
            
            fragment = self.create_rock(position, new_type)
            fragments.append(fragment)
            
        return fragments


class SaucerFactory(GameObjectFactory):
    """Factory for creating saucers"""
    
    def create_saucer(self, saucer_type: int, target_ship, 
                     spawn_position: Vector2d = None) -> Saucer:
        """Create a saucer of the specified type"""
        saucer = Saucer(self.stage, saucer_type, target_ship)
        saucer.universe = self.universe
        
        if spawn_position:
            saucer.position = spawn_position
        elif target_ship:
            # Spawn near the player
            saucer.position.x = target_ship.position.x - 500
            saucer.position.y = target_ship.position.y + random.randrange(-200, 200)
            
        return saucer


class DebrisFactory(GameObjectFactory):
    """Factory for creating debris"""
    
    def create_debris_field(self, center_position: Vector2d, 
                           count: int = DEBRIS_COUNT) -> list:
        """Create a field of debris at the specified position"""
        debris_list = []
        
        for _ in range(count):
            offset_x = random.randrange(-10, 10)
            offset_y = random.randrange(-10, 10)
            position = Vector2d(center_position.x + offset_x,
                              center_position.y + offset_y)
            
            debris = Debris(position, self.stage)
            debris_list.append(debris)
            
        return debris_list


class GameObjectFactoryManager:
    """Manages all object factories"""
    
    def __init__(self, universe, stage):
        self.ship_factory = ShipFactory(universe, stage)
        self.rock_factory = RockFactory(universe, stage)
        self.saucer_factory = SaucerFactory(universe, stage)
        self.debris_factory = DebrisFactory(universe, stage) 
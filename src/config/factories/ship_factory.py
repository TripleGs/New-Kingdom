from config.config import SHIP_ACCELERATION, SHIP_DECELERATION, SHIP_MAX_VELOCITY, SHIP_TURN_ANGLE, SHIP_BULLET_VELOCITY, SHIP_MAX_BULLETS, SHIP_BULLET_TTL
from config.factories.game_object_factory import GameObjectFactory
from entities.ship import Ship
from util.vector2d import Vector2d

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
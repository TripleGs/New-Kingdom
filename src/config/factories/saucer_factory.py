import random

from config.config import SAUCER_LARGE_TYPE, SAUCER_MEDIUM_TYPE, SAUCER_SMALL_TYPE
from config.factories.game_object_factory import GameObjectFactory
from entities.saucer import Saucer
from util.vector2d import Vector2d


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
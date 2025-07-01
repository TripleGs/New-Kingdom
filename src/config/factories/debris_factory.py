import random

from config.config import DEBRIS_COUNT
from config.factories.game_object_factory import GameObjectFactory
from entities.debris import Debris
from util.vector2d import Vector2d


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
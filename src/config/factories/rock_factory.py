import random

from config.config import ROCK_LARGE_TYPE, ROCK_MEDIUM_TYPE, ROCK_SMALL_TYPE
from config.factories.game_object_factory import GameObjectFactory
from entities.rock import Rock
from util.vector2d import Vector2d


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

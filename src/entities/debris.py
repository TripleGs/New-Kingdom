import random
from ..util.vectorsprites import *

class Debris(Point):    
     
    def __init__(self, position, stage):
        heading = Vector2d(random.uniform(-1.5, 1.5), random.uniform(-1.5, 1.5))
        Point.__init__(self, position, heading, stage)
        self.ttl = 50
    
    def move(self):    
        Point.move(self)
        r,g,b = self.color
        r -= 5
        g -= 5
        b -= 5
        self.color = (r,g,b) 
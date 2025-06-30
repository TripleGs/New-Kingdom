import random
from ..util.vectorsprites import *

# Four different shape of rock each of which can be small, medium or large.
# Smaller rocks are faster.
class Rock(VectorSprite):
    
    # indexes into the tuples below
    largeRockType = 0
    mediumRockType = 1
    smallRockType = 2   
    
    # Material types for rocks
    COAL = 0
    IRON = 1
    GOLD = 2
    
    material_types = {
        COAL: {"color": (80, 80, 80), "name": "Coal", "rarity": 0.6},
        IRON: {"color": (140, 140, 140), "name": "Iron", "rarity": 0.3},
        GOLD: {"color": (200, 180, 60), "name": "Gold", "rarity": 0.1}
    }
    
    velocities = (1.5, 3.0, 2.5)  # Reduced small rock speed from 4.5 to 2.5    
    scales = (2.5, 1.5, 0.6)

    # tracks the last rock shape to be generated
    rockShape = 1    
    
    # Create the rock polygon to the given scale
    def __init__(self, stage, position, rockType):
        
        scale = Rock.scales[rockType]
        velocity = Rock.velocities[rockType]                
        heading = Vector2d(random.uniform(-velocity, velocity), random.uniform(-velocity, velocity))
        
        # Ensure that the rocks don't just sit there or move along regular lines
        if heading.x == 0:
            heading.x = 0.1
        
        if heading.y == 0:
            heading.y = 0.1
                        
        self.rockType = rockType
        self.materialType = self.determineMaterialType()
        self.color = Rock.material_types[self.materialType]["color"]
        self.materialName = Rock.material_types[self.materialType]["name"]
        
        pointlist = self.createPointList()
        newPointList = [self.scale(point, scale) for point in pointlist]        
        VectorSprite.__init__(self, position, heading, newPointList)
    
    def determineMaterialType(self):
        """Determine rock material type based on rarity"""
        rand = random.random()
        
        if rand < Rock.material_types[Rock.GOLD]["rarity"]:
            return Rock.GOLD
        elif rand < Rock.material_types[Rock.GOLD]["rarity"] + Rock.material_types[Rock.IRON]["rarity"]:
            return Rock.IRON
        else:
            return Rock.COAL
                
    
    # Create different rock type pointlists    
    def createPointList(self):
        
        if (Rock.rockShape == 1):
            pointlist = [(-4,-12), (6,-12), (13, -4), (13, 5), (6, 13), (0,13), (0,4),\
                     (-8,13), (-15, 4), (-7,1), (-15,-3)]
 
        elif (Rock.rockShape == 2):
            pointlist = [(-6,-12), (1,-5), (8, -12), (15, -5), (12,0), (15,6), (5,13),\
                         (-7,13), (-14,7), (-14,-5)]
            
        elif (Rock.rockShape == 3):
            pointlist = [(-7,-12), (1,-9), (8,-12), (15,-5), (8,-3), (15,4), (8,12),\
                         (-3,10), (-6,12), (-14,7), (-10,0), (-14,-5)]            

        elif (Rock.rockShape == 4):
            pointlist = [(-7,-11), (3,-11), (13,-5), (13,-2), (2,2), (13,8), (6,14),\
                         (2,10), (-7,14), (-15,5), (-15,-5), (-5,-5), (-7,-11)]

        Rock.rockShape += 1
        if (Rock.rockShape == 5):
            Rock.rockShape = 1

        return pointlist
    
    # Spin the rock when it moves
    def move(self):
        VectorSprite.move(self)                        
        
        # Original Asteroid didn't have spinning rocks but they look nicer
        self.angle += 1 
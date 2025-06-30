from ..util.vectorsprites import *

# Space Station - where player can dock and refuel
class SpaceStation(VectorSprite):
    
    # Space station visual design
    pointlist = [
        # Main station body (rectangular)
        (-20, -15), (20, -15), (20, 15), (-20, 15), (-20, -15),
        # Docking ports
        (-20, -5), (-30, -5), (-30, 5), (-20, 5),
        (20, -5), (30, -5), (30, 5), (20, 5),
        # Antenna/solar panels
        (-10, -15), (-10, -25), (10, -25), (10, -15),
        (-15, 15), (-15, 25), (15, 25), (15, 15)
    ]
    
    dockingRange = 80  # Distance within which player can dock
    
    def __init__(self, position, stage):
        heading = Vector2d(0, 0)  # Space station doesn't move
        self.stage = stage
        self.universe = None  # Will be set by the game
        self.color = (0, 255, 255)  # Cyan color for space station
        VectorSprite.__init__(self, position, heading, self.pointlist)
        
    def move(self):
        # Space station doesn't move, but we override to prevent any movement
        pass
        
    def canDockWith(self, ship):
        """Check if the ship is close enough to dock"""
        if ship is None:
            return False
            
        distance = ((self.position.x - ship.position.x) ** 2 + 
                   (self.position.y - ship.position.y) ** 2) ** 0.5
        return distance <= self.dockingRange
        
    def getDistanceToShip(self, ship):
        """Get distance to ship for UI display"""
        if ship is None:
            return float('inf')
            
        return ((self.position.x - ship.position.x) ** 2 + 
                (self.position.y - ship.position.y) ** 2) ** 0.5 
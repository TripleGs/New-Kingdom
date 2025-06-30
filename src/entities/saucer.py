import random
import math
from ..util.vectorsprites import *
from .shooter import *
from ..audio.soundManager import *

# Flying saucer, shoots at player
class Saucer(Shooter):
    
    # indexes into the tuples below
    largeSaucerType = 0
    smallSaucerType = 1

    velocities = (1.5, 2.5)    
    scales = (1.5, 1.0)
    scores = (500, 1000)
    pointlist = [(-9,0), (-3,-3), (-2,-6), (-2,-6), (2,-6), (3,-3), (9,0), (-9,0), (-3,4), (3,4), (9,0)]
    maxBullets = 1
    bulletTtl = [60, 90]
    bulletVelocity = 5  
    
    def __init__(self, stage, saucerType, ship):                
        position = Vector2d(0.0, random.randrange(0, stage.height))
        heading = Vector2d(self.velocities[saucerType], 0.0)
        self.saucerType = saucerType
        self.ship = ship
        self.scoreValue = self.scores[saucerType]
        stopSound("ssaucer")
        stopSound("lsaucer")            
        if saucerType == self.largeSaucerType:            
            playSoundContinuous("lsaucer")            
        else:            
            playSoundContinuous("ssaucer")
        self.laps = 0
        self.lastx = 0
        
        # Scale the shape and create the VectorSprite
        newPointList = [self.scale(point, self.scales[saucerType]) for point in self.pointlist]
        Shooter.__init__(self, position, heading, newPointList, stage)
        
    def move(self):        
        Shooter.move(self)  
        
        if (self.position.x > self.stage.width * 0.33) and (self.position.x < self.stage.width * 0.66):
            self.heading.y = self.heading.x
        else:
            self.heading.y = 0
        
        self.fireBullet()
        
        # have we lapped?        
        if self.lastx > self.position.x:
            self.lastx = 0
            self.laps += 1
        else:
            self.lastx = self.position.x
                
    # Set the bullet velocity and create the bullet
    def fireBullet(self):
        if self.ship is not None:            
            dx = self.ship.position.x - self.position.x
            dy = self.ship.position.y - self.position.y
            mag = math.sqrt(dx*dx + dy*dy);
            heading = Vector2d(self.bulletVelocity * (dx/mag), self.bulletVelocity * (dy/mag))
            position = Vector2d(self.position.x, self.position.y)          
            shotFired = Shooter.fireBullet(self, heading, self.bulletTtl[self.saucerType], self.bulletVelocity)
            if shotFired:
                playSound("sfire") 
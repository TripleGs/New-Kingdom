import random
from ..util.vectorsprites import *
from .shooter import *
from math import *
from ..audio.soundManager import *

class Ship(Shooter):

    # Class attributes
    acceleration = 0.2
    decelaration = -0.005
    maxVelocity = 10
    turnAngle = 6
    bulletVelocity = 13.0
    maxBullets = 4
    bulletTtl = 35
    # Fuel system attributes
    maxFuel = 100
    fuelConsumptionRate = 0.3

    def __init__(self, stage):

        position = Vector2d(stage.width/2, stage.height/2)
        heading = Vector2d(0, 0)
        self.thrustJet = ThrustJet(stage, self)
        self.shipDebrisList = []
        self.visible = True
        self.inHyperSpace = False
        self.universe = None  # Will be set by the game
        # Fuel system initialization
        self.fuel = self.maxFuel
        self.lowFuelWarning = False
        pointlist = [(0, -10), (6, 10), (3, 7), (-3, 7), (-6, 10)]

        Shooter.__init__(self, position, heading, pointlist, stage)

    def draw(self):
        if self.visible:
            if not self.inHyperSpace:
                VectorSprite.draw(self)
            else:
                self.hyperSpaceTtl -= 1
                if self.hyperSpaceTtl == 0:
                    self.inHyperSpace = False
                    self.color = (255, 255, 255)
                    self.thrustJet.color = (255, 255, 255)
                    # Teleport to a random location in the universe
                    if self.universe:
                        self.position.x = random.randrange(100, self.universe.width - 100)
                        self.position.y = random.randrange(100, self.universe.height - 100)
                    else:
                        # Fallback to stage dimensions
                        self.position.x = random.randrange(0, self.stage.width)
                        self.position.y = random.randrange(0, self.stage.height)
                    position = Vector2d(self.position.x, self.position.y)
                    self.thrustJet.position = position

        return self.transformedPointlist

    def rotateLeft(self):
        self.angle += self.turnAngle

    def rotateRight(self):
        self.angle -= self.turnAngle

    def increaseThrust(self):
        # Check if we have fuel before thrusting
        if self.fuel <= 0:
            self.thrustJet.accelerating = False
            return
            
        playSoundContinuous("thrust")
        if math.hypot(self.heading.x, self.heading.y) > self.maxVelocity:
            return

        # Consume fuel when thrusting
        self.fuel -= self.fuelConsumptionRate
        if self.fuel < 0:
            self.fuel = 0
            
        # Set low fuel warning when fuel is below 20%
        self.lowFuelWarning = self.fuel < (self.maxFuel * 0.2)

        dx = self.acceleration * math.sin(radians(self.angle)) * -1
        dy = self.acceleration * math.cos(radians(self.angle)) * -1
        self.changeVelocity(dx, dy)

    def decreaseThrust(self):
        stopSound("thrust")
        if (self.heading.x == 0 and self.heading.y == 0):
            return

        dx = self.heading.x * self.decelaration
        dy = self.heading.y * self.decelaration
        self.changeVelocity(dx, dy)

    def changeVelocity(self, dx, dy):
        self.heading.x += dx
        self.heading.y += dy

    def move(self):
        VectorSprite.move(self)
        self.decreaseThrust()

    # Break the shape of the ship down into several lines
    # Ship shape - [(0, -10), (6, 10), (3, 7), (-3, 7), (-6, 10)]
    def explode(self):
        pointlist = [(0, -10), (6, 10)]
        self.addShipDebris(pointlist)
        pointlist = [(6, 10), (3, 7)]
        self.addShipDebris(pointlist)
        pointlist = [(3, 7), (-3, 7)]
        self.addShipDebris(pointlist)
        pointlist = [(-3, 7), (-6, 10)]
        self.addShipDebris(pointlist)
        pointlist = [(-6, 10), (0, -10)]
        self.addShipDebris(pointlist)

    # Create a peice of ship debris

    def addShipDebris(self, pointlist):
        heading = Vector2d(0, 0)
        position = Vector2d(self.position.x + random.randrange(-5, 5), 
                          self.position.y + random.randrange(-5, 5))
        debris = VectorSprite(position, heading, pointlist, self.angle)

        # Add debris to the universe if available
        if self.universe:
            self.universe.addObject(debris)

        # Calc a velocity moving away from the ship's center
        # Use approximate center since we don't have boundingRect yet
        debris_center_x = position.x
        debris_center_y = position.y

        # Alter the random values below to change the rate of expansion
        debris.heading.x = ((debris_center_x - self.position.x) +
                            0.1) / random.uniform(20, 40)
        debris.heading.y = ((debris_center_y - self.position.y) +
                            0.1) / random.uniform(20, 40)
        self.shipDebrisList.append(debris)

    # Set the bullet velocity and create the bullet

    def fireBullet(self):
        if self.inHyperSpace == False:
            vx = self.bulletVelocity * math.sin(radians(self.angle)) * -1
            vy = self.bulletVelocity * math.cos(radians(self.angle)) * -1
            heading = Vector2d(vx, vy)
            Shooter.fireBullet(self, heading, self.bulletTtl,
                               self.bulletVelocity)
            playSound("fire")

    #
    def enterHyperSpace(self):
        if not self.inHyperSpace:
            self.inHyperSpace = True
            self.hyperSpaceTtl = 100
            self.color = (0, 0, 0)
            self.thrustJet.color = (0, 0, 0)

    def refillFuel(self):
        """Refill the ship's fuel tank"""
        self.fuel = self.maxFuel
        self.lowFuelWarning = False

    def getFuelPercentage(self):
        """Get fuel level as a percentage (0-100)"""
        return (self.fuel / self.maxFuel) * 100

    def hasFuel(self):
        """Check if ship has fuel for thrusting"""
        return self.fuel > 0

# Exhaust jet when ship is accelerating
class ThrustJet(VectorSprite):
    pointlist = [(-3, 7), (0, 13), (3, 7)]

    def __init__(self, stage, ship):
        position = Vector2d(stage.width/2, stage.height/2)
        heading = Vector2d(0, 0)
        self.accelerating = False
        self.ship = ship
        VectorSprite.__init__(self, position, heading, self.pointlist)

    def move(self):
        # Override move to always sync with ship position and angle
        # Don't call VectorSprite.move() as we don't want independent movement
        self.position.x = self.ship.position.x
        self.position.y = self.ship.position.y
        self.angle = self.ship.angle

    def draw(self):
        if self.accelerating and self.ship.inHyperSpace == False:
            self.color = (255, 255, 255)
        else:
            self.color = (0, 0, 0)

        VectorSprite.draw(self)
        return self.transformedPointlist

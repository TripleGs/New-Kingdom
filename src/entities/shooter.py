import random
from ..util.vectorsprites import *
from ..util import *


class Shooter(VectorSprite):

    def __init__(self, position, heading, pointlist, stage):
        VectorSprite.__init__(self, position, heading, pointlist)
        self.bullets = []
        self.stage = stage
        self.universe = None  # Will be set by the game

    def fireBullet(self, heading, ttl, velocity):
        if (len(self.bullets) < self.maxBullets):
            position = Vector2d(self.position.x, self.position.y)
            newBullet = Bullet(position, heading, self,
                               ttl, velocity, self.stage)
            self.bullets.append(newBullet)
            # Add to universe instead of stage
            if self.universe:
                self.universe.addObject(newBullet)
            return True

    def bulletCollision(self, target):
        collisionDetected = False
        for bullet in self.bullets:
            if bullet.ttl > 0 and target.collidesWith(bullet):
                collisionDetected = True
                bullet.ttl = 0

        return collisionDetected

# Bullet class


class Bullet(Point):

    def __init__(self, position, heading, shooter, ttl, velocity, stage):
        Point.__init__(self, position, heading, stage)
        self.shooter = shooter
        self.ttl = ttl
        self.velocity = velocity

    def move(self):
        Point.move(self)
        if (self.ttl <= 0):
            # Only remove if still in the list (collision may have already removed it)
            if self in self.shooter.bullets:
                self.shooter.bullets.remove(self)

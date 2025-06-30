

import pygame
import sys
import os
import math
import random
from math import *
from .vector2d import *
from .geometry import *


class VectorSprite:

    def __init__(self, position, heading, pointlist, angle=0, color=(255, 255, 255)):
        self.position = position
        self.heading = heading
        self.angle = angle
        self.vAngle = 0
        self.pointlist = pointlist  # raw pointlist
        self.color = color
        self.ttl = 25

        #self.color = color = (random.randrange(40,255),random.randrange(40,255),random.randrange(40,255))

    # rotate each x,y coord by the angle, then translate it to the x,y position
    def rotateAndTransform(self):
        newPointList = [self.rotatePoint(point) for point in self.pointlist]
        self.transformedPointlist = [
            self.translatePoint(point) for point in newPointList]

    # draw the sprite
    def draw(self):
        self.rotateAndTransform()
        return self.transformedPointlist

    # translate each point to the current x, y position
    def translatePoint(self, point):
        newPoint = []
        newPoint.append(point[0] + self.position.x)
        newPoint.append(point[1] + self.position.y)
        return newPoint

    # Move the sprite by the velocity
    def move(self):
        # Apply velocity
        self.position.x = self.position.x + self.heading.x
        self.position.y = self.position.y + self.heading.y
        self.angle = self.angle + self.vAngle

        # needed?
        # self.rotateAndTransform()

    # Rotate a point by the given angle
    def rotatePoint(self, point):
        newPoint = []
        cosVal = math.cos(radians(self.angle))
        sinVal = math.sin(radians(self.angle))
        newPoint.append(point[0] * cosVal + point[1] * sinVal)
        newPoint.append(point[1] * cosVal - point[0] * sinVal)

        # Keep points as integers
        newPoint = [int(point) for point in newPoint]
        return newPoint

    # Scale a point
    def scale(self, point, scale):
        newPoint = []
        newPoint.append(point[0] * scale)
        newPoint.append(point[1] * scale)
        # Keep points as integers
        newPoint = [int(point) for point in newPoint]
        return newPoint

    def collidesWith(self, target):
        # Compute bounding rectangles on the fly
        self_rect = self.getBoundingRect()
        target_rect = target.getBoundingRect()
        if self_rect.colliderect(target_rect):
            return True
        else:
            return False
            
    def getBoundingRect(self):
        """Compute and return bounding rectangle for this sprite"""
        if not hasattr(self, 'transformedPointlist') or not self.transformedPointlist:
            # Generate transformed points if they don't exist
            self.rotateAndTransform()
            
        if not self.transformedPointlist:
            # Fallback to a small rectangle around the position
            return pygame.Rect(int(self.position.x - 5), int(self.position.y - 5), 10, 10)
            
        # Find min/max x,y from transformed points
        x_coords = [point[0] for point in self.transformedPointlist]
        y_coords = [point[1] for point in self.transformedPointlist]
        
        min_x = min(x_coords)
        max_x = max(x_coords)
        min_y = min(y_coords)
        max_y = max(y_coords)
        
        width = max_x - min_x
        height = max_y - min_y
        
        return pygame.Rect(int(min_x), int(min_y), int(width) + 1, int(height) + 1)

    # Check each line from pointlist1 for intersection with
    # the lines in pointlist2
    def checkPolygonCollision(self, target):
        for i in range(0, len(self.transformedPointlist)):
            for j in range(0, len(target.transformedPointlist)):
                p1 = self.transformedPointlist[i-1]
                p2 = self.transformedPointlist[i]
                p3 = target.transformedPointlist[j-1]
                p4 = target.transformedPointlist[j]
                p = calculateIntersectPoint(p1, p2, p3, p4)
                if (p != None):
                    return p

        return None

# Used for bullets and debris


class Point(VectorSprite):

    # Class attributes
    pointlist = [(0, 0), (1, 1), (1, 0), (0, 1)]

    def __init__(self, position, heading, stage):
        VectorSprite.__init__(self, position, heading, self.pointlist)
        self.stage = stage
        self.ttl = 30

    def move(self):
        self.ttl -= 1
        # TTL-based removal is now handled by the universe
        VectorSprite.move(self)

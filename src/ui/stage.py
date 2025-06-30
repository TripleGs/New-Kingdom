import pygame
import sys
import os
from pygame.locals import *
from ..util.vector2d import Vector2d


class Stage:

    # Set up the PyGame surface
    def __init__(self, caption, dimensions=None):
        pygame.init()

        # If no screen size is provided pick the first available mode
        if dimensions == None:
            dimensions = pygame.display.list_modes()[0]

        # pygame.display.set_mode(dimensions, FULLSCREEN)
        pygame.mouse.set_visible(True)

        pygame.display.set_mode(dimensions)

        pygame.display.set_caption(caption)
        self.screen = pygame.display.get_surface()
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.showBoundingBoxes = False
        self.camera = None

    def setCamera(self, camera):
        """Set the camera for this stage"""
        self.camera = camera

    def drawSprites(self, visible_sprites):
        """Draw only the visible sprites using camera coordinates"""
        for sprite in visible_sprites:
            if self.camera and self.camera.isVisible(sprite.position):
                # Convert world position to screen position
                screen_pos = self.camera.worldToScreen(sprite.position)
                
                # Temporarily store original position
                original_pos = Vector2d(sprite.position.x, sprite.position.y)
                
                # Set sprite to screen position for drawing
                sprite.position = screen_pos
                
                # Draw the sprite and get its bounding rect
                points = sprite.draw()
                if points and len(points) > 0:
                    drawn_rect = pygame.draw.aalines(
                        self.screen, sprite.color, True, points)
                    # Store the bounding rect for this frame
                    sprite.boundingRect = drawn_rect
                    
                    if self.showBoundingBoxes:
                        pygame.draw.rect(self.screen, (255, 255, 255),
                                       drawn_rect, 1)
                
                # Restore original world position
                sprite.position = original_pos

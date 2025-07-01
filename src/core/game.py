#!/usr/bin/env python3

import pygame
import sys
import os
import random
from pygame.locals import *
from ..util.vectorsprites import *
from ..entities.ship import *
from ..ui.stage import *
from ..entities.rock import Rock
from ..entities.saucer import Saucer
from ..entities.debris import Debris
from ..entities.space_station import SpaceStation
from ..entities.crystal import Crystal
from ..entities.shooter import *
from ..audio.soundManager import *
from ..systems.universe import Universe
from ..systems.camera import Camera
from ..systems.background import BackgroundManager
from ..systems.minimap import MiniMap
from ..config.config import FONT_PATH, FONT_SIZES
from .shop import Shop
from .fuel_system import FuelSystem
from .rescue_system import RescueSystem
from .ui_manager import UIManager
from .crystal_system.crystal_system import CrystalSystem


class Game():

    explodingTtl = 180

    def __init__(self):
        # Screen dimensions
        self.screen_width = 1024
        self.screen_height = 768
        
        # Create universe (much larger than screen)
        self.universe = Universe(width=20000, height=20000)
        
        # Create camera
        self.camera = Camera(self.screen_width, self.screen_height, 
                           self.universe.width, self.universe.height)
        
        # Create stage and link camera
        self.stage = Stage('Atari Asteroids', (self.screen_width, self.screen_height))
        self.stage.setCamera(self.camera)
        
        # Create background manager
        self.background = BackgroundManager(self.camera)
        
        # Create mini map
        self.minimap = MiniMap(self.universe, self.screen_width, self.screen_height)
        
        # Initialize UI and game systems
        self.shop = Shop(self)
        self.fuelSystem = FuelSystem(self)
        self.rescueSystem = RescueSystem(self)
        self.uiManager = UIManager(self)
        self.crystalSystem = CrystalSystem(self)
        
        # Game state
        self.paused = False
        self.showingFPS = False
        self.frameAdvance = False
        self.gameState = "attract_mode"
        self.secondsCount = 1
        self.money = 1000  # Start with $1000 instead of score
        self.nextLife = 10000  # Next life award threshold
        self.ship = None
        self.lives = 0
        self.livesList = []
        # Docking and shop system
        self.spaceStation = None
        self.showShop = False
        self.nearStation = False
        # Fuel rescue system
        self.outOfFuel = False
        self.showRescuePrompt = False
        # Mini map control
        self.showMiniMap = True
        
        # Create initial asteroid belts for the attract mode display
        self.universe.createAsteroidBelts(6, 20)  # 6 belts with 20 rocks each

    def initialiseGame(self):
        self.gameState = 'playing'
        
        # Clear universe
        self.universe = Universe(width=20000, height=20000)
        
        # Recreate mini map with new universe
        self.minimap = MiniMap(self.universe, self.screen_width, self.screen_height)
        
        # Reset game variables
        self.startLives = 5
        self.money = 1000  # Start with $1000
        self.numRocks = 120  # Number of rocks in asteroid belts
        self.nextLife = 10000
        self.secondsCount = 1
        self.outOfFuel = False
        self.showRescuePrompt = False
        
        self.createNewShip()
        self.createLivesList()
        self.createAsteroidBelts()
        self.createSpaceStation()

    def createSpaceStation(self):
        """Create space station near the center of the universe (spawn point)"""
        center_x = self.universe.width // 2
        center_y = self.universe.height // 2
        # Position station slightly offset from ship spawn
        station_x = center_x + 150
        station_y = center_y
        position = Vector2d(station_x, station_y)
        
        self.spaceStation = SpaceStation(position, self.stage)
        self.spaceStation.universe = self.universe
        self.universe.addObject(self.spaceStation)

    def createNewShip(self):
        # Place ship at center of universe
        center_x = self.universe.width // 2
        center_y = self.universe.height // 2
        position = Vector2d(center_x, center_y)
        
        self.ship = Ship(self.stage)
        self.ship.position = position
        self.ship.thrustJet.position = Vector2d(position.x, position.y)
        
        # Link ship to universe for debris and bullet management
        self.ship.universe = self.universe
        
        # Add ship to universe
        self.universe.addObject(self.ship)
        self.universe.addObject(self.ship.thrustJet)
        
        # Set camera to follow ship
        self.camera.setTarget(self.ship)

    def createLivesList(self):
        self.lives = self.startLives
        self.livesList = []
        # Lives display will be handled differently in the new system

    def addLife(self, lifeNumber):
        self.lives += 1

    def createAsteroidBelts(self):
        """Create asteroid belts throughout the universe"""
        # Calculate number of belts and rocks per belt
        num_belts = 8
        rocks_per_belt = self.numRocks // num_belts
        self.universe.createAsteroidBelts(num_belts, rocks_per_belt)

    def playGame(self):

        clock = pygame.time.Clock()

        frameCount = 0.0
        timePassed = 0.0
        self.fps = 0.0
        # Main loop
        while True:

            # calculate fps
            timePassed += clock.tick(60)
            frameCount += 1
            if frameCount % 10 == 0:  # every 10 frames
                # nearest integer
                self.fps = round((frameCount / (timePassed / 1000.0)))
                # reset counter
                timePassed = 0
                frameCount = 0

            self.secondsCount += 1

            self.input(pygame.event.get())

            # pause
            if self.paused and not self.frameAdvance:
                self.uiManager.displayPaused()
                continue

            # Update camera
            self.camera.update()
            
            # Update background
            self.background.update()
            
            # Draw background first
            self.background.draw(self.stage.screen)
            
            # Update universe (all objects move)
            self.universe.updateObjects()
            
            # Get visible objects from universe
            view_x, view_y, view_width, view_height = self.camera.getVisibleRegion()
            visible_objects = self.universe.getObjectsInRegion(view_x, view_y, view_width, view_height)
            
            # Draw visible objects
            self.stage.drawSprites(visible_objects)
            
            self.doSaucerLogic()
            self.uiManager.checkDocking()
            self.crystalSystem.displayCrystalBin()
            self.uiManager.displayMoney()
            self.fuelSystem.displayFuelBar()
            self.uiManager.displayDockingPrompt()
            self.rescueSystem.displayRescuePrompt()
            self.shop.display()
            # Draw mini map (show in all game states)
            if self.showMiniMap:
                self.minimap.draw(self.stage.screen)
            if self.showingFPS:
                self.uiManager.displayFps()  # for debug
            self.checkMoney()

            # Process keys
            if self.gameState == 'playing':
                self.playing()
            elif self.gameState == 'exploding':
                self.exploding()
            else:
                self.uiManager.displayGameText()
                # Also show mini map in attract mode to see the galaxy
                if self.showMiniMap:
                    self.minimap.draw(self.stage.screen)

            # Double buffer draw
            pygame.display.flip()

    def playing(self):
        if self.lives == 0:
            self.gameState = 'attract_mode'
        else:
            self.fuelSystem.checkFuelStatus()
            self.processKeys()
            self.checkCollisions()
            # Collect nearby crystals
            if self.ship:
                self.crystalSystem.collectNearbyCrystals(self.ship)
            if len(self.universe.rocks) == 0:
                self.levelUp()

    def doSaucerLogic(self):
        if self.universe.saucer is not None:
            if self.universe.saucer.laps >= 2:
                self.killSaucer()

        # Create a saucer
        if self.secondsCount % 2000 == 0 and self.universe.saucer is None:
            randVal = random.randrange(0, 10)
            if randVal <= 3:
                saucer = Saucer(self.stage, Saucer.smallSaucerType, self.ship)
            else:
                saucer = Saucer(self.stage, Saucer.largeSaucerType, self.ship)
            
            # Position saucer at edge of universe near player
            if self.ship:
                saucer.position.x = self.ship.position.x - 500
                saucer.position.y = self.ship.position.y + random.randrange(-200, 200)
            
            # Link saucer to universe for bullet management
            saucer.universe = self.universe
            self.universe.addObject(saucer)

    def exploding(self):
        self.explodingCount += 1
        if self.explodingCount > self.explodingTtl:
            self.gameState = 'playing'
            
            # Clean up ship debris
            if self.ship and hasattr(self.ship, 'shipDebrisList'):
                for debris in self.ship.shipDebrisList:
                    self.universe.removeObject(debris)
                self.ship.shipDebrisList = []

            if self.lives == 0:
                if self.ship:
                    self.ship.visible = False
            else:
                self.createNewShip()

    def levelUp(self):
        """Add more rocks throughout the universe for next level"""
        additional_rocks_per_belt = 3  # Add 3 rocks per belt each level
        self.universe.addRocksToExistingBelts(additional_rocks_per_belt)
        # Estimate the number of rocks added (8 belts * rocks per belt)
        self.numRocks += 8 * additional_rocks_per_belt

    # move this kack somewhere else!


    # Should move the ship controls into the ship class
    def input(self, events):
        self.frameAdvance = False
        for event in events:
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if self.showShop:
                        self.shop.close()
                    else:
                        sys.exit(0)
                
                # Rescue controls
                if self.showRescuePrompt:
                    if event.key == K_r:
                        # Call rescue service
                        self.rescueSystem.handleRescueRequest()
                
                # Shop controls
                elif self.showShop:
                    if event.key == K_TAB:
                        # Toggle shop mode
                        self.shop.toggleMode()
                    elif event.key == K_1:
                        if self.shop.shop_mode == "buy":
                            # Refill fuel
                            self.shop.handleFuelPurchase()
                        else:
                            # Sell coal crystals
                            self.shop.handleCrystalSale(1)
                    elif event.key == K_2 and self.shop.shop_mode == "sell":
                        # Sell iron crystals
                        self.shop.handleCrystalSale(2)
                    elif event.key == K_3 and self.shop.shop_mode == "sell":
                        # Sell gold crystals
                        self.shop.handleCrystalSale(3)
                    elif event.key == K_4 and self.shop.shop_mode == "sell":
                        # Sell all crystals
                        self.shop.handleCrystalSale(4)
                elif self.gameState == 'playing':
                    if event.key == K_SPACE:
                        self.ship.fireBullet()
                    elif event.key == K_b:
                        self.ship.fireBullet()
                    elif event.key == K_h:
                        self.ship.enterHyperSpace()
                    elif event.key == K_d:
                        # Docking
                        if self.nearStation and not self.showShop:
                            self.shop.open()
                elif self.gameState == 'attract_mode':
                    # Start a new game
                    if event.key == K_RETURN:
                        self.initialiseGame()

                if event.key == K_p:
                    if self.paused:  # (is True)
                        self.paused = False
                    else:
                        self.paused = True

                if event.key == K_j:
                    if self.showingFPS:  # (is True)
                        self.showingFPS = False
                    else:
                        self.showingFPS = True

                if event.key == K_m:
                    # Toggle mini map
                    self.showMiniMap = not self.showMiniMap

                if event.key == K_f:
                    pygame.display.toggle_fullscreen()

                # if event.key == K_k:
                    # self.killShip()
            elif event.type == KEYUP:
                if event.key == K_o:
                    self.frameAdvance = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Forward mouse click events to active UI components
                if self.showShop:
                    self.shop.handle_event(event)
                elif self.showRescuePrompt:
                    self.rescueSystem.handle_event(event)

    def processKeys(self):
        # Don't process movement keys if out of fuel and showing rescue prompt
        if self.showRescuePrompt:
            return
            
        key = pygame.key.get_pressed()

        if key[K_LEFT] or key[K_z]:
            self.ship.rotateLeft()
        elif key[K_RIGHT] or key[K_x]:
            self.ship.rotateRight()

        if key[K_UP] or key[K_n]:
            # Only show thrust jet if ship has fuel
            if self.ship.hasFuel():
                self.ship.increaseThrust()
                self.ship.thrustJet.accelerating = True
            else:
                self.ship.thrustJet.accelerating = False
        else:
            self.ship.thrustJet.accelerating = False

    def checkCollisions(self):
        """Check for collisions using the universe system"""
        collisions = self.universe.checkCollisions()
        
        for collision_type, obj1, obj2 in collisions:
            if collision_type == 'ship_rock':
                self.handleRockDestroyed(obj2)
                self.killShip()
                
            elif collision_type == 'bullet_rock':
                self.handleRockDestroyed(obj2)
                # Remove bullet
                if hasattr(obj1, 'shooter'):
                    if obj1 in obj1.shooter.bullets:
                        obj1.shooter.bullets.remove(obj1)
                obj1.ttl = 0  # Mark bullet as expired
                
            elif collision_type == 'bullet_ship':
                # Saucer bullet hit ship
                if hasattr(obj1, 'shooter'):
                    if obj1 in obj1.shooter.bullets:
                        obj1.shooter.bullets.remove(obj1)
                obj1.ttl = 0
                self.killShip()
                
            elif collision_type == 'bullet_saucer':
                # Ship bullet hit saucer
                if hasattr(obj1, 'shooter'):
                    if obj1 in obj1.shooter.bullets:
                        obj1.shooter.bullets.remove(obj1)
                obj1.ttl = 0
                self.money += self.universe.saucer.scoreValue
                self.createDebris(obj2)
                self.killSaucer()
                
            elif collision_type == 'saucer_rock':
                self.handleRockDestroyed(obj2)
                self.createDebris(obj1)
                self.killSaucer()
                
            elif collision_type == 'saucer_ship':
                self.createDebris(obj1)
                self.killSaucer()
                self.killShip()
                
    def handleRockDestroyed(self, rock):
        """Handle when a rock is destroyed"""
        self.universe.removeObject(rock)
        
        # Score and sound based on rock size
        if rock.rockType == Rock.largeRockType:
            playSound("explode1")
            newRockType = Rock.mediumRockType
            self.money += 50
        elif rock.rockType == Rock.mediumRockType:
            playSound("explode2")
            newRockType = Rock.smallRockType
            self.money += 100
        else:
            playSound("explode3")
            self.money += 200
            # Create crystals when small rock is destroyed
            self.createCrystals(rock)
            
        # Create smaller rocks
        if rock.rockType != Rock.smallRockType:
            for _ in range(2):
                position = Vector2d(rock.position.x + random.randrange(-20, 20), 
                                  rock.position.y + random.randrange(-20, 20))
                newRock = Rock(self.stage, position, newRockType)
                # Preserve the material type for smaller rocks
                newRock.materialType = rock.materialType
                newRock.color = rock.color
                newRock.materialName = rock.materialName
                self.universe.addObject(newRock)
                
        self.createDebris(rock)

    def killShip(self):
        stopSound("thrust")
        playSound("explode2")
        self.explodingCount = 0
        self.lives -= 1
        
        # Remove ship from universe
        if self.ship:
            self.universe.removeObject(self.ship)
            self.universe.removeObject(self.ship.thrustJet)
            
        self.gameState = 'exploding'
        if self.ship:
            self.ship.explode()

    def killSaucer(self):
        stopSound("lsaucer")
        stopSound("ssaucer")
        playSound("explode2")
        if self.universe.saucer:
            self.universe.removeObject(self.universe.saucer)

    def createDebris(self, sprite):
        for _ in range(25):
            position = Vector2d(sprite.position.x + random.randrange(-10, 10), 
                              sprite.position.y + random.randrange(-10, 10))
            debris = Debris(position, self.stage)
            self.universe.addObject(debris)
    
    def createCrystals(self, rock):
        """Create crystals when a small rock is destroyed"""
        # Create 3-8 crystals based on rock material
        num_crystals = random.randint(3, 8)
        
        for _ in range(num_crystals):
            position = Vector2d(rock.position.x + random.randrange(-15, 15), 
                              rock.position.y + random.randrange(-15, 15))
            crystal = Crystal(position, self.stage, rock.materialType)
            self.universe.addObject(crystal)



    def checkMoney(self):
        if self.money > 0 and self.money > self.nextLife:
            playSound("extralife")
            self.nextLife += 10000
            self.addLife(self.lives)












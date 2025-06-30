import pygame
from ..config.config import FONT_PATH, FONT_SIZES

class UIManager:
    """Handles general UI elements like money display and docking prompts"""
    
    def __init__(self, game):
        self.game = game
        
    def displayMoney(self):
        """Display the money on screen"""
        font1 = pygame.font.Font(FONT_PATH, FONT_SIZES["subtitle"])
        moneyStr = "$" + str(self.game.money)
        moneyText = font1.render(moneyStr, True, (200, 200, 200))
        moneyTextRect = moneyText.get_rect(centerx=100, centery=45)
        self.game.stage.screen.blit(moneyText, moneyTextRect)
        
    def displayDockingPrompt(self):
        """Display docking prompt when near space station"""
        if not self.game.nearStation or self.game.showRescuePrompt:
            return
            
        font = pygame.font.Font(FONT_PATH, FONT_SIZES["normal"])
        prompt_text = font.render("Press D to Dock", True, (0, 255, 255))
        prompt_rect = prompt_text.get_rect(centerx=self.game.stage.width//2, centery=self.game.stage.height//2 + 100)
        self.game.stage.screen.blit(prompt_text, prompt_rect)
        
    def displayGameText(self):
        """Display attract mode text"""
        font1 = pygame.font.Font(FONT_PATH, FONT_SIZES["title"])
        font2 = pygame.font.Font(FONT_PATH, FONT_SIZES["normal"])
        font3 = pygame.font.Font(FONT_PATH, FONT_SIZES["subtitle"])

        titleText = font1.render('Asteroids', True, (180, 180, 180))
        titleTextRect = titleText.get_rect(centerx=self.game.stage.width/2)
        titleTextRect.y = self.game.stage.height/2 - titleTextRect.height*2
        self.game.stage.screen.blit(titleText, titleTextRect)

        keysText = font2.render(
            '(C) 1979 Atari INC.', True, (255, 255, 255))
        keysTextRect = keysText.get_rect(centerx=self.game.stage.width/2)
        keysTextRect.y = self.game.stage.height - keysTextRect.height - 20
        self.game.stage.screen.blit(keysText, keysTextRect)

        instructionText = font3.render(
            'Press start to Play', True, (200, 200, 200))
        instructionTextRect = instructionText.get_rect(
            centerx=self.game.stage.width/2)
        instructionTextRect.y = self.game.stage.height/2 - instructionTextRect.height
        self.game.stage.screen.blit(instructionText, instructionTextRect)
        
    def displayPaused(self):
        """Display paused screen"""
        if self.game.paused:
            font1 = pygame.font.Font(FONT_PATH, FONT_SIZES["subtitle"])
            pausedText = font1.render("Paused", True, (255, 255, 255))
            textRect = pausedText.get_rect(
                centerx=self.game.stage.width/2, centery=self.game.stage.height/2)
            self.game.stage.screen.blit(pausedText, textRect)
            pygame.display.update()
            
    def displayFps(self):
        """Display FPS counter"""
        font2 = pygame.font.Font(FONT_PATH, FONT_SIZES["small"])
        fpsStr = str(self.game.fps)+(' FPS')
        scoreText = font2.render(fpsStr, True, (255, 255, 255))
        scoreTextRect = scoreText.get_rect(
            centerx=(self.game.stage.width/2), centery=15)
        self.game.stage.screen.blit(scoreText, scoreTextRect)
        
    def checkDocking(self):
        """Check if player is near space station for docking"""
        if self.game.ship and self.game.spaceStation:
            self.game.nearStation = self.game.spaceStation.canDockWith(self.game.ship) 
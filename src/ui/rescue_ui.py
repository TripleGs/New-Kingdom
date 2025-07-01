import pygame
from ..config.config import FONT_PATH, FONT_SIZES
from .components.button import Button

class RescueUI:
    """UI prompt shown when player runs out of fuel."""

    def __init__(self, rescue_system):
        self.rescue_system = rescue_system
        self.game = rescue_system.game
        self.button_created = False
        self.button = None

    # ------------------------------------------------------------------
    def _create_button(self):
        # Center button on screen
        screen_w = self.game.stage.width
        screen_h = self.game.stage.height
        rect = pygame.Rect(screen_w//2 - 120, screen_h//2 + 20, 240, 40)
        font = pygame.font.Font(FONT_PATH, FONT_SIZES["normal"])
        cost = self.rescue_system.rescueCost
        self.button = Button(rect, f"Rescue me - ${cost}", font, self.rescue_system.handleRescueRequest)
        self.button_created = True

    # ------------------------------------------------------------------
    def draw(self, surface):
        if not self.button_created:
            self._create_button()

        font_title = pygame.font.Font(FONT_PATH, FONT_SIZES["subtitle"])
        font_text = pygame.font.Font(FONT_PATH, FONT_SIZES["normal"])

        title_text = font_title.render("OUT OF FUEL!", True, (255, 0, 0))
        title_rect = title_text.get_rect(centerx=self.game.stage.width//2, centery=self.game.stage.height//2 - 60)
        surface.blit(title_text, title_rect)

        # Draw button
        self.button.draw(surface)

        # Show money status if insufficient
        if self.game.money < self.rescue_system.rescueCost:
            money_text = font_text.render(f"Insufficient funds! You have ${self.game.money}", True, (255, 0, 0))
            money_rect = money_text.get_rect(centerx=self.game.stage.width//2, centery=self.game.stage.height//2 + 70)
            surface.blit(money_text, money_rect)

    # ------------------------------------------------------------------
    def handle_event(self, event):
        if self.button:
            self.button.handle_event(event) 
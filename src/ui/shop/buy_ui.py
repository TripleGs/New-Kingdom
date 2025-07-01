import pygame
from ...config.config import FONT_PATH, FONT_SIZES
from ..components.button import Button

class ShopBuyUI:
    """UI for the shop BUY mode."""

    def __init__(self, shop):
        self.shop = shop  # reference to Shop instance
        self.game = shop.game
        self.buttons_created = False
        self.buttons = []

    # ------------------------------------------------------------------
    def _create_buttons(self, shop_x, shop_y):
        """Create buttons. Must be called once window dims known."""
        option_font = pygame.font.Font(FONT_PATH, FONT_SIZES["normal"])
        instruction_font = pygame.font.Font(FONT_PATH, FONT_SIZES["small"])

        # Button for refilling fuel
        refill_rect = pygame.Rect(shop_x + 40, shop_y + 90, 320, 35)
        refill_btn = Button(refill_rect, "Refill Fuel Tank", option_font, self.shop.handleFuelPurchase)

        # Button to switch to sell mode
        toggle_rect = pygame.Rect(shop_x + 40, shop_y + 140, 320, 30)
        toggle_btn = Button(toggle_rect, "Switch to SELL", instruction_font, self.shop.toggleMode)

        self.buttons = [refill_btn, toggle_btn]
        self.buttons_created = True

    # ------------------------------------------------------------------
    def draw(self, surface, shop_x, shop_y, shop_width, shop_height):
        """Render the UI, creating buttons if needed."""
        if not self.buttons_created:
            self._create_buttons(shop_x, shop_y)

        # Update text that depends on runtime values (fuel cost)
        if self.game.ship:
            fuel_needed = self.game.ship.maxFuel - self.game.ship.fuel
            fuel_cost = int(fuel_needed * self.shop.fuelCostPerUnit)
            # Update button label
            self.buttons[0].text = f"Refill Fuel Tank - ${fuel_cost}"

        # Draw buttons
        for btn in self.buttons:
            btn.draw(surface)

        # Draw status lines
        instruction_font = pygame.font.Font(FONT_PATH, FONT_SIZES["small"])
        if self.game.ship:
            fuel_pct = int(self.game.ship.getFuelPercentage())
            fuel_status = instruction_font.render(f"Current Fuel: {fuel_pct}%", True, (255, 255, 0))
            surface.blit(fuel_status, (shop_x + 40, shop_y + 180))
        money_status = instruction_font.render(f"Your Money: ${self.game.money}", True, (0, 255, 0))
        surface.blit(money_status, (shop_x + 40, shop_y + 200))

    # ------------------------------------------------------------------
    def handle_event(self, event):
        """Pass event to buttons."""
        for btn in self.buttons:
            btn.handle_event(event) 
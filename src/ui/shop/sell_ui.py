import pygame
from ...config.config import FONT_PATH, FONT_SIZES
from ..components.button import Button
from ...entities.crystal import Crystal

class ShopSellUI:
    """UI for the shop SELL mode."""

    def __init__(self, shop):
        self.shop = shop
        self.game = shop.game
        self.buttons_created = False
        self.buttons = []

    # ------------------------------------------------------------------
    def _create_buttons(self, shop_x, shop_y):
        option_font = pygame.font.Font(FONT_PATH, FONT_SIZES["normal"])
        small_font = pygame.font.Font(FONT_PATH, FONT_SIZES["small"])

        y_offset = 90
        height = 30
        width = 320
        start_x = shop_x + 40
        crystal_types = [Crystal.COAL, Crystal.IRON, Crystal.GOLD]
        for i, c_type in enumerate(crystal_types):
            rect = pygame.Rect(start_x, shop_y + y_offset + i* (height + 5), width, height)
            name = Crystal.crystal_types[c_type]["name"]
            btn = Button(rect, f"Sell {name}", option_font,
                          lambda opt=i+1: self.shop.handleCrystalSale(opt))
            self.buttons.append(btn)

        # Sell All button
        rect_all = pygame.Rect(start_x, shop_y + y_offset + 3*(height+5), width, height)
        sell_all_btn = Button(rect_all, "Sell All Crystals", option_font,
                               lambda: self.shop.handleCrystalSale(4))
        self.buttons.append(sell_all_btn)

        # Toggle back to Buy mode
        rect_toggle = pygame.Rect(start_x, shop_y + y_offset + 4*(height+5), width, height)
        toggle_btn = Button(rect_toggle, "Switch to BUY", small_font, self.shop.toggleMode)
        self.buttons.append(toggle_btn)

        self.buttons_created = True

    # ------------------------------------------------------------------
    def draw(self, surface, shop_x, shop_y, shop_width, shop_height):
        if not self.buttons_created:
            self._create_buttons(shop_x, shop_y)

        # Update dynamic labels with counts and values
        crystal_counts = self.game.crystalSystem.getCrystalCounts()
        for i, btn in enumerate(self.buttons):
            # 0,1,2 correspond to crystals, 3 Sell All, 4 toggle
            if i < 3:
                c_type = [Crystal.COAL, Crystal.IRON, Crystal.GOLD][i]
                count = crystal_counts[c_type]
                name = Crystal.crystal_types[c_type]["name"]
                value = Crystal.crystal_types[c_type]["value"]
                total = count * value
                btn.text = f"Sell {name} ({count}) - ${total}"
            elif i == 3:
                total_value = self.game.crystalSystem.getTotalValue()
                btn.text = f"Sell All Crystals - ${total_value}"

        # Draw buttons
        for btn in self.buttons:
            btn.draw(surface)

        # Money status
        small_font = pygame.font.Font(FONT_PATH, FONT_SIZES["small"])
        money_status = small_font.render(f"Your Money: ${self.game.money}", True, (0, 255, 0))
        surface.blit(money_status, (shop_x + 40, shop_y + shop_height - 60))

    # ------------------------------------------------------------------
    def handle_event(self, event):
        for btn in self.buttons:
            btn.handle_event(event) 
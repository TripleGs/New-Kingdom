class Button:
    """Simple clickable button component for pygame UIs"""
    def __init__(self, rect, text, font, callback,
                 bg_color=(80, 80, 80), hover_color=(120, 120, 120),
                 text_color=(255, 255, 255)):
        """
        Parameters
        ----------
        rect : pygame.Rect | tuple
            Rectangle describing position and size of button
        text : str
            Label displayed on button
        font : pygame.font.Font
            Font object used to render text
        callback : Callable[[], None]
            Function invoked when the button is clicked
        bg_color, hover_color, text_color : Tuple[int, int, int]
            RGB colours for default, hover and text respectively
        """
        import pygame  # Local import to avoid issues if pygame not yet initialised
        if not isinstance(rect, pygame.Rect):
            rect = pygame.Rect(rect)
        self.rect = rect
        self.text = text
        self.font = font
        self.callback = callback
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color

    # ---------------------------------------------------------------------
    # Rendering & events
    # ---------------------------------------------------------------------
    def draw(self, surface):
        """Draw the button on the given surface."""
        import pygame
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)
        colour = self.hover_color if is_hover else self.bg_color
        pygame.draw.rect(surface, colour, self.rect)
        pygame.draw.rect(surface, (0, 255, 255), self.rect, 2)  # border

        # Render text centred
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        """Call in event loop. Executes callback on left click."""
        import pygame
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback() 
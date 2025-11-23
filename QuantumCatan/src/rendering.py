# src/rendering.py
# low-level drawing helpers used by UI and main loop

import pygame
from .constants import TEXT_COLOR

# Note: constants.py does not export fonts; create quick fallback
def draw_text(screen, text, x, y, size=18, color=TEXT_COLOR):
    font = pygame.font.SysFont("Arial", size)
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))

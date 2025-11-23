# src/dice.py
import random
import pygame
from .constants import WHITE, TEXT_COLOR
from .rendering import draw_text

def roll_with_animation(screen):
    # quick animation, returns final roll
    """for _ in range(8):
        fake = random.randint(1,6) + random.randint(1,6)
        pygame.draw.rect(screen, (235,222,200), (160,80,120,40))
        draw_text(screen, f"Dice: {fake}", 160, 80, size=20)
        pygame.display.flip()
        pygame.time.delay(50) """
    roll = random.randint(1,6) + random.randint(1,6)
    return roll

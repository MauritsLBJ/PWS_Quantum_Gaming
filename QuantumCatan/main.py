# main.py
# Run this to start Quantum Catan
import time
import pygame
import sys
from src.game_state import GameState
from src.ui import GameUI
from src.constants import WIN_W, WIN_H

"""
def ask_player_count():
     simple terminal prompt before launching pygame
    while True:
        try:
            val = input("Number of players (2-4) [default 4]: ").strip()
            if val == "":
                return 4
            n = int(val)
            if 2 <= n <= 4:
                return n
        except Exception:
            pass
        print("Please enter 2, 3 or 4.")
"""

def main():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Quantum Catan")
    screen = pygame.display.set_mode((WIN_W, WIN_H), pygame.RESIZABLE)

    num_players =  3 #ask_player_count()
    state = GameState(num_players=num_players, screen=screen)
    ui = GameUI(state, screen)

    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ui.handle_event(event)

        state.update(dt)
        ui.draw()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

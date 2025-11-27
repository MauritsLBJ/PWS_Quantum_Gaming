import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hexagon with Two Colored Halves")

# Colors
COLOR_TOP = (255, 0, 0)     # Red
COLOR_BOTTOM = (0, 0, 255)  # Blue
BG_COLOR = (255, 255, 255)  # White

# Hexagon parameters
center = (WIDTH // 2, HEIGHT // 2)
radius = 100

def hexagon_points(center, radius):
    """Generate the 6 vertices of a regular hexagon."""
    cx, cy = center
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30  # Start flat-top
        angle_rad = math.radians(angle_deg)
        x = cx + radius * math.cos(angle_rad)
        y = cy + radius * math.sin(angle_rad)
        points.append((x, y))
    return points

# Get hexagon vertices
hex_points = hexagon_points(center, radius)

# Split into top and bottom halves
# Top half: vertices 0,1,2 + center
top_half = [center,hex_points[5], hex_points[0], hex_points[1], hex_points[2]]
# Bottom half: vertices 3,4,5 + center
bottom_half = [center,hex_points[2], hex_points[3], hex_points[4], hex_points[5]]

# Main loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG_COLOR)

    # Draw top half
    pygame.draw.polygon(screen, COLOR_TOP, top_half)
    # Draw bottom half
    pygame.draw.polygon(screen, COLOR_BOTTOM, bottom_half)

    # Optional: draw hexagon outline
    pygame.draw.polygon(screen, (0, 0, 0), hex_points, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()


"""How it works:

hexagon_points: Uses math.cos and math.sin to calculate the 6 vertices of a regular hexagon.
Splitting halves: We take the top 3 vertices and the bottom 3 vertices, each connected to the center, to form two polygons.
Drawing: pygame.draw.polygon is called twice with different colors.


✅ This method works for flat-top hexagons.
If you want a pointy-top hexagon, just change the starting angle in hexagon_points.

If you want, I can also show you a version where the two halves are split vertically instead of horizontally.
Do you want me to prepare that?"""

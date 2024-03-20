import sys

import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player image
player_image = pygame.Surface((50, 50))
player_image.fill(RED)  # Fill with red color for demonstration

# Player rect (big)
player_rect_big = player_image.get_rect()
player_rect_big.center = (WIDTH // 2, HEIGHT // 2)
big_rect_alignment_point = (player_rect_big.centerx, player_rect_big.centery + 20)  # Example: 20px below center

# Player rect (small, for collision detection)
small_rect_size = (25, 25)  # Small rect size
player_rect_small = pygame.Rect(big_rect_alignment_point, small_rect_size)

# Offset between the alignment points of big and small rects
offset_x = player_rect_small.centerx - big_rect_alignment_point[0]
offset_y = player_rect_small.centery - big_rect_alignment_point[1]

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    player_rect_big.center = pygame.mouse.get_pos()  # Move big rect with mouse
    # Update small rect position based on the offset
    player_rect_small.centerx = player_rect_big.centerx + offset_x
    player_rect_small.centery = player_rect_big.centery + offset_y

    # Draw
    # Draw big rect
    pygame.draw.rect(screen, (0, 255, 0), player_rect_big, 2)
    # Draw small rect
    pygame.draw.rect(screen, BLUE, player_rect_small, 2)
    # Draw player image
    screen.blit(player_image, player_rect_big.topleft)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

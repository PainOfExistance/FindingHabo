import numpy as np
import pygame
from main_menu import MainMenu
from main_menu import is_menu_visible

pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Finding Habo")
menu=MainMenu(screen)

if __name__ == "__main__":
    print(is_menu_visible)
    while is_menu_visible:
        screen.fill((255, 255, 255))
    
        #menu.handle_input()
        #menu.render()
    
        pygame.display.flip()


"""import pygame
import sys
import numpy as np

# Initialize Pygame
pygame.init()

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Finding Habo")

# Load player image
player = pygame.image.load("desk1.png")
player = pygame.transform.scale(player, (screen_width // 10, screen_height // 10))
player_rect = player.get_rect()
player_rect.center = (screen_width // 2, screen_height // 2)

# Load background image (larger than the screen)
background = pygame.image.load("desk2.png")
bg_rect = background.get_rect()

# Create a collision map using NumPy
# 1's on the borders, 0's elsewhere
collision_map = np.zeros((bg_rect.height, bg_rect.width), dtype=int)
collision_map[0, :] = 1
collision_map[-1, :] = 1
collision_map[:, 0] = 1
collision_map[:, -1] = 1
#collision_map[200:300, 200:300] = 1

#image = pygame.image.load("desk3.png")  # Replace with the path to your image
#image = pygame.transform.scale(image, (100, 100))
#image_rect = image.get_rect()
#image_rect.center = (250, 250)

# Set up clock for controlling frame rate
clock = pygame.time.Clock()
target_fps = 60

# Initialize variables for time-based movement
last_frame_time = pygame.time.get_ticks()
movement_speed = 200  # pixels per second
bg_speed = 200  # pixels per second

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Calculate delta time (time since last frame)
    current_time = pygame.time.get_ticks()
    delta_time = (current_time - last_frame_time) / 1000.0  # Convert to seconds
    last_frame_time = current_time

    relative_player_left = int(player_rect.left - bg_rect.left)
    relative_player_right = int(player_rect.right - bg_rect.left)
    relative_player_top = int(player_rect.top - bg_rect.top)
    relative_player_bottom = int(player_rect.bottom - bg_rect.top)

    print(f"rl: {relative_player_left},   rr: {relative_player_right},   rt: {relative_player_top},   rb: {relative_player_bottom}")

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and np.count_nonzero(collision_map[relative_player_top:relative_player_bottom, relative_player_left-1] == 1) <= 1:
        if player_rect.left > 10:
            player_rect.move_ip(int(-movement_speed * delta_time), 0)
        else:
            bg_rect.move_ip(int(bg_speed * delta_time), 0)
    
    if keys[pygame.K_d] and np.count_nonzero(collision_map[relative_player_top:relative_player_bottom, relative_player_right+1] == 1) <= 1:
        if player_rect.right < screen_width-10:
            player_rect.move_ip(int(movement_speed * delta_time), 0)
        else:
            bg_rect.move_ip(int(-bg_speed * delta_time), 0)
    
    if keys[pygame.K_w] and np.count_nonzero(collision_map[relative_player_top-1, relative_player_left:relative_player_right] == 1) <= 1:
        if player_rect.top > 10:
            player_rect.move_ip(0, int(-movement_speed * delta_time))
        else:
            bg_rect.move_ip(0, int(bg_speed * delta_time))
    
    if keys[pygame.K_s] and np.count_nonzero(collision_map[relative_player_bottom-1, relative_player_left:relative_player_right] == 1) <= 1:
        if player_rect.bottom < screen_height-10:
            player_rect.move_ip(0, int(movement_speed * delta_time))
        else:
            bg_rect.move_ip(0, int(-bg_speed * delta_time))


    # Clear screen
    screen.fill((230, 60, 20))

    # Draw the visible portion of the background based on camera's position
    screen.blit(background, bg_rect.topleft)

    #screen.blit(image, image_rect)

    # Draw player
    screen.blit(player, player_rect.topleft)

    # Update display
    pygame.display.flip()

    # Limit frame rate
    clock.tick(target_fps)
"""

"""
health-health lol
knowlage-to learn abilities, increases/decreases over time and is effected by effects
sanity-ability to learn new shit if its hight enough
power-to use abilities, increases/decreases over time and is effected by effects
"""
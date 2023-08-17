import pygame
import sys
import numpy as np
from asset_loader import AssetLoader

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up display
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Finding Habo")

        # Load player image
        asets=AssetLoader(self.screen_width, self.screen_height)

        self.player, self.player_rect = asets.load_player("desk1.png")
        self.background, self.bg_rect = asets.load_background("bg.png")
        #self.image, self.image_rect = asets.load_images("desk3.png", (100, 100), (250, 250))

        # Create a collision map using NumPy
        self.collision_map =asets.load_collision("bg.png")

        # Set up clock for controlling frame rate
        self.clock = pygame.time.Clock()
        self.target_fps = 60

        # Initialize variables for time-based movement
        self.last_frame_time = pygame.time.get_ticks()
        self.movement_speed = 200

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.target_fps)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Calculate delta time (time since last frame)
        current_time = pygame.time.get_ticks()
        self.delta_time = (current_time - self.last_frame_time) / 1000.0  # Convert to seconds
        self.last_frame_time = current_time
        relative_player_left = int(self.player_rect.left - self.bg_rect.left)
        relative_player_right = int(self.player_rect.right - self.bg_rect.left)
        relative_player_top = int(self.player_rect.top - self.bg_rect.top)
        relative_player_bottom = int(self.player_rect.bottom - self.bg_rect.top)

        print(f"rl: {relative_player_left},   rr: {relative_player_right},   rt: {relative_player_top},   rb: {relative_player_bottom}")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and np.count_nonzero(self.collision_map[relative_player_top:relative_player_bottom, relative_player_left-1] == 1) <= 1:
            if self.player_rect.left > 10:
                self.player_rect.move_ip(int(-self.movement_speed * self.delta_time), 0)
            else:
                self.bg_rect.move_ip(int(self.movement_speed * self.delta_time), 0)
                
        if keys[pygame.K_d] and np.count_nonzero(self.collision_map[relative_player_top:relative_player_bottom, relative_player_right+1] == 1) <= 1:
            if self.player_rect.right < self.screen_width-10:
                self.player_rect.move_ip(int(self.movement_speed * self.delta_time), 0)
            else:
                self.bg_rect.move_ip(int(-self.movement_speed * self.delta_time), 0)

        if keys[pygame.K_w] and np.count_nonzero(self.collision_map[relative_player_top-1, relative_player_left:relative_player_right] == 1) <= 1:
            if self.player_rect.top > 10:
                self.player_rect.move_ip(0, int(-self.movement_speed * self.delta_time))
            else:
                self.bg_rect.move_ip(0, int(self.movement_speed * self.delta_time))

        if keys[pygame.K_s] and np.count_nonzero(self.collision_map[relative_player_bottom-1, relative_player_left:relative_player_right] == 1) <= 1:
            if self.player_rect.bottom < self.screen_height-10:
                self.player_rect.move_ip(0, int(self.movement_speed * self.delta_time))
            else:
                self.bg_rect.move_ip(0, int(-self.movement_speed * self.delta_time))

    def draw(self):
        self.screen.fill((230, 60, 20))
        self.screen.blit(self.background, self.bg_rect.topleft)
        self.screen.blit(self.player, self.player_rect.topleft)
        #self.screen.blit(self.image, self.image_rect.topleft)
        pygame.display.flip()

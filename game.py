import pygame
import sys
import numpy as np
from asset_loader import AssetLoader
from player import Player
from menu import Menu

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up display
        self.screen_width, self.screen_height = 800, 600
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        pygame.display.set_caption("Finding Habo")

        # Load player image
        asets = AssetLoader(self.screen_width, self.screen_height)
        self.menu = Menu(self.screen)

        self.player=Player("desk1.png", self.screen_width, self.screen_height)
        self.background, self.bg_rect = asets.load_background("bg.png")
        # self.image, self.image_rect = asets.load_images("desk3.png", (100, 100), (250, 250))

        # Create a collision map using NumPy
        self.collision_map = asets.load_collision("bg.png")

        # Set up clock for controlling frame rate
        self.clock = pygame.time.Clock()
        self.target_fps = 60

        # Initialize variables for time-based movement
        self.last_frame_time = pygame.time.get_ticks()
        self.movement_speed = 200
        self.rotation_angle = 0

    def run(self):
        while True:
            if not self.menu.visible:
                self.update()
            self.handle_events()
            self.draw()
            self.menu.handle_input()
            self.clock.tick(self.target_fps)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        # Calculate delta time (time since last frame)
        current_time = pygame.time.get_ticks()
        self.delta_time = (current_time - self.last_frame_time) / \
            1000.0  # Convert to seconds
        self.last_frame_time = current_time
        
        relative_player_left = int(self.player.player_rect.left - self.bg_rect.left)
        relative_player_right = int(self.player.player_rect.right - self.bg_rect.left)
        relative_player_top = int(self.player.player_rect.top - self.bg_rect.top)
        relative_player_bottom = int(self.player.player_rect.bottom - self.bg_rect.top)
        movement = int(self.movement_speed * self.delta_time)

        print(f"rl: {relative_player_left},   rr: {relative_player_right},   rt: {relative_player_top},   rb: {relative_player_bottom}")
        #print(self.detect_slope((relative_player_left, relative_player_bottom)))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and np.count_nonzero(self.collision_map[relative_player_top:relative_player_bottom, relative_player_left-movement] == 1) <= 1:
            if self.player.player_rect.left > 10:
                self.player.player_rect.move_ip(
                    int(-self.movement_speed * self.delta_time), 0)
                if self.rotation_angle != 90:
                    self.rotation_angle = 90 - self.rotation_angle
                    self.player.player = pygame.transform.rotate(self.player.player, self.rotation_angle)
                    self.rotation_angle = 90
            else:
                self.bg_rect.move_ip(
                    int(self.movement_speed * self.delta_time), 0)

        if keys[pygame.K_d] and np.count_nonzero(self.collision_map[relative_player_top:relative_player_bottom, relative_player_right+movement] == 1) <= 1:
            if self.player.player_rect.right < self.screen_width-10:
                self.player.player_rect.move_ip(
                    int(self.movement_speed * self.delta_time), 0)
                if self.rotation_angle != 270:
                    self.rotation_angle = 270 - self.rotation_angle
                    self.player.player = pygame.transform.rotate(self.player.player, self.rotation_angle)
                    self.rotation_angle = 270
            else:
                self.bg_rect.move_ip(
                    int(-self.movement_speed * self.delta_time), 0)

        if keys[pygame.K_w] and np.count_nonzero(self.collision_map[relative_player_top-movement, relative_player_left:relative_player_right] == 1) <= 1:
            if self.player.player_rect.top > 10:
                self.player.player_rect.move_ip(
                    0, int(-self.movement_speed * self.delta_time))
                self.player.update_health(10)
                if self.rotation_angle != 0:
                    self.rotation_angle = 0 - self.rotation_angle
                    self.player.player = pygame.transform.rotate(self.player.player, self.rotation_angle)
                    self.rotation_angle = 0
            else:
                self.bg_rect.move_ip(
                    0, int(self.movement_speed * self.delta_time))

        if keys[pygame.K_s] and np.count_nonzero(self.collision_map[relative_player_bottom+movement, relative_player_left:relative_player_right] == 1) <= 1:
            if self.player.player_rect.bottom < self.screen_height-10:
                self.player.player_rect.move_ip(
                    0, int(self.movement_speed * self.delta_time))
                self.player.update_health(-10)
                if self.rotation_angle != 180:
                    self.rotation_angle = 180 - self.rotation_angle
                    self.player.player = pygame.transform.rotate(self.player.player, self.rotation_angle)
                    self.rotation_angle = 180
            else:
                self.bg_rect.move_ip(
                    0, int(-self.movement_speed * self.delta_time))

    #def detect_slope(self, position):
    #    x, y = position
    #    subarray_size = 5  # Size of the subarray (odd number for a centered subarray)
    #    half_size = subarray_size // 2
    #    nearby_points = self.collision_map[y - half_size:y + half_size + 1, x - half_size:x + half_size + 1]
#
    #    gradient_y, gradient_x = np.gradient(nearby_points)
    #    angle_rad = np.arctan2(gradient_y[half_size, half_size], gradient_x[half_size, half_size])
    #    angle_deg = np.degrees(angle_rad)
#
    #    return angle_deg


    def draw(self):
        self.screen.fill((230, 60, 20))
        self.screen.blit(self.background, self.bg_rect.topleft)
        self.player.draw(self.screen)
        self.menu.render()
        # self.screen.blit(self.image, self.image_rect.topleft)
        pygame.display.flip()

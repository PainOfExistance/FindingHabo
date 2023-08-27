import pygame
import sys
import numpy as np


class Game:
    def __init__(
        self, screen, screen_width, screen_height, menu, player_menu, player, assets
    ):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.asets = assets
        self.menu = menu

        self.items = assets.load_items()
        self.player = player
        self.player_menu = player_menu

        self.player.inventory.add_item(self.items["Minor Health Potion"])
        self.player.inventory.add_item(self.items["Knowledge Potion"])
        self.player.inventory.add_item(self.items["Power Elixir"])
        self.player.inventory.add_item(self.items["Steel Sword"])
        self.player.inventory.add_item(self.items["Steel Armor"])
        self.player.inventory.add_item(self.items["Divine Armor"])
        self.worlds=assets.load_worlds()

        self.background, self.bg_rect = self.asets.load_background(self.worlds[self.player.current_world]["collision_set"])
        self.collision_map = self.asets.load_collision(self.worlds[self.player.current_world]["background"])
        self.map_height = self.collision_map.shape[0]
        self.map_width = self.collision_map.shape[1]
        self.world_objects={}
        
        for data in self.worlds[self.player.current_world]["items"]:
            item=self.items[data["type"]]
            img, img_rect=self.asets.load_images(item["image"], (64,64), tuple(data["position"]))
            self.world_objects[img]=img_rect
                    
        self.clock = pygame.time.Clock()
        self.target_fps = 60

        self.last_frame_time = pygame.time.get_ticks()
        self.movement_speed = 200
        self.rotation_angle = 0

        # self.sound_effect = pygame.mixer.Sound("Angelia.mp3")
        # self.sound_effect.play()
        # self.sound_effect.set_volume(0.2)
        # self.sound_effect.play(loops=-1)

    def run(self):
        while True:
            self.update()
            self.handle_events()
            self.draw()

            if not self.player_menu.visible:
                self.menu.handle_input()

            if not self.menu.visible:
                self.player_menu.handle_input()

            self.clock.tick(self.target_fps)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        # Calculate delta time (time since last frame)
        current_time = pygame.time.get_ticks()
        self.delta_time = (
            current_time - self.last_frame_time
        ) / 1000.0  # Convert to seconds
        self.last_frame_time = current_time

        relative_player_left = int(self.player.player_rect.left - self.bg_rect.left)
        relative_player_right = int(self.player.player_rect.right - self.bg_rect.left)
        relative_player_top = int(self.player.player_rect.top - self.bg_rect.top)
        relative_player_bottom = int(self.player.player_rect.bottom - self.bg_rect.top)
        movement = int(self.movement_speed * self.delta_time)

        # print(f"rl: {relative_player_left},   rr: {relative_player_right},   rt: {relative_player_top},   rb: {relative_player_bottom}")
        # print(self.detect_slope((relative_player_left, relative_player_bottom)))

        keys = pygame.key.get_pressed()
        if (
            keys[pygame.K_a]
            and np.count_nonzero(
                self.collision_map[
                    relative_player_top:relative_player_bottom,
                    relative_player_left - movement,
                ]
                == 1
            )
            <= 1
            and not self.menu.visible
            and not self.player_menu.visible
        ):
            if self.player.player_rect.left > 10:
                self.player.player_rect.move_ip(
                    int(-self.movement_speed * self.delta_time), 0
                )
                self.player.level.gain_experience(100)
                # self.player.add_trait("Health Boost")
                if self.rotation_angle != 90:
                    self.rotation_angle = 90 - self.rotation_angle
                    self.player.player = pygame.transform.rotate(
                        self.player.player, self.rotation_angle
                    )
                    self.rotation_angle = 90
            else:
                self.bg_rect.move_ip(int(self.movement_speed * self.delta_time), 0)

        if (
            keys[pygame.K_d]
            and np.count_nonzero(
                self.collision_map[
                    relative_player_top:relative_player_bottom,
                    min(relative_player_right + movement, self.map_width - 1),
                ]
                == 1
            )
            <= 1
            and not self.menu.visible
            and not self.player_menu.visible
        ):
            if self.player.player_rect.right < self.screen_width - 10:
                self.player.player_rect.move_ip(
                    int(self.movement_speed * self.delta_time), 0
                )
                if self.rotation_angle != 270:
                    self.rotation_angle = 270 - self.rotation_angle
                    self.player.player = pygame.transform.rotate(
                        self.player.player, self.rotation_angle
                    )
                    self.rotation_angle = 270
            else:
                self.bg_rect.move_ip(int(-self.movement_speed * self.delta_time), 0)

        if (
            keys[pygame.K_w]
            and np.count_nonzero(
                self.collision_map[
                    relative_player_top - movement,
                    relative_player_left:relative_player_right,
                ]
                == 1
            )
            <= 1
            and not self.menu.visible
            and not self.player_menu.visible
        ):
            if self.player.player_rect.top > 10:
                self.player.player_rect.move_ip(
                    0, int(-self.movement_speed * self.delta_time)
                )
                # self.player.update_health(10)
                if self.rotation_angle != 0:
                    self.rotation_angle = 0 - self.rotation_angle
                    self.player.player = pygame.transform.rotate(
                        self.player.player, self.rotation_angle
                    )
                    self.rotation_angle = 0
            else:
                self.bg_rect.move_ip(0, int(self.movement_speed * self.delta_time))

        if (
            keys[pygame.K_s]
            and np.count_nonzero(
                self.collision_map[
                    min(relative_player_bottom + movement, self.map_height - 1),
                    relative_player_left:relative_player_right,
                ]
                == 1
            )
            <= 1
            and not self.menu.visible
            and not self.player_menu.visible
        ):
            if self.player.player_rect.bottom < self.screen_height - 10:
                self.player.player_rect.move_ip(
                    0, int(self.movement_speed * self.delta_time)
                )
                # self.player.update_health(-10)
                if self.rotation_angle != 180:
                    self.rotation_angle = 180 - self.rotation_angle
                    self.player.player = pygame.transform.rotate(
                        self.player.player, self.rotation_angle
                    )
                    self.rotation_angle = 180
            else:
                self.bg_rect.move_ip(0, int(-self.movement_speed * self.delta_time))

    # def detect_slope(self, position):
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
        for x in self.world_objects:
            relative__left = int(self.bg_rect.left + self.world_objects[x].left)
            relative__top = int(self.bg_rect.top + self.world_objects[x].top)
            if relative__left > - 80 and relative__left < self.screen_width + 80 and relative__top > - 80 and relative__top < self.screen_height + 80:
                self.screen.blit(x, (relative__left, relative__top))
        self.player.draw(self.screen)
        self.menu.render()
        self.player_menu.render()
        pygame.display.flip()

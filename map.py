import numpy as np
import pygame

from game_manager import ClassManager as CM
from game_manager import GameManager as GM


class Map:
    def __init__(self):
        self.map = None
        self.full_map = None
        self.width = 0
        self.height = 0
        self.offset = (
            (GM.relative_player_left + GM.relative_player_right) // 2,
            (GM.relative_player_top + GM.relative_player_bottom) // 2,
        )
        self.border_rect = pygame.Rect(0, GM.screen_height - 20, GM.screen_width, 20)

    def set_map(self, map):
        self.full_map = map
        self.width = map.get_width()
        self.height = map.get_height()
        self.offset = (
            ((GM.relative_player_left + GM.relative_player_right) // 2)
            - self.width // 4,
            ((GM.relative_player_top + GM.relative_player_bottom) // 2)
            - self.height // 4,
        )

        subsurface_rect = pygame.Rect(
            self.offset[0], self.offset[1], self.width // 2, self.height // 2
        )
        subsurface = map.subsurface(subsurface_rect)
        self.map = pygame.transform.scale(
            subsurface,
            (
                max(GM.screen_width - 40, GM.screen_height - 40),
                max(GM.screen_width - 40, GM.screen_height - 40),
            ),
        )

    def handle_input(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        subsurface_rect = pygame.Rect(
            100, 100, GM.screen_width - 200, GM.screen_height - 200
        )

        if not subsurface_rect.collidepoint(mouse_x, mouse_y):
            print("Mouse is within the 20-pixel border.")
            offset_x = mouse_x - GM.screen_width // 2
            offset_y = -1*(mouse_y - GM.screen_height // 2)
            print(offset_x, offset_y)
            # self.offset=(((GM.relative_player_left + GM.relative_player_right) // 2)-self.width // 4, ((GM.relative_player_top + GM.relative_player_bottom) // 2)-self.height // 4)
            # subsurface_rect = pygame.Rect(self.offset[0], self.offset[1], self.width // 2, self.height // 2)
            # subsurface = map.subsurface(subsurface_rect)
            # self.map = pygame.transform.scale(
            #    subsurface, (max(GM.screen_width - 40, GM.screen_height - 40), max(GM.screen_width - 40, GM.screen_height - 40))
            # )

    def draw(self):
        GM.screen.fill((11, 11, 11))
        GM.screen.blit(self.map, (20, 20))
        pygame.draw.rect(GM.screen, (0, 0, 0), self.border_rect)

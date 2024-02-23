import numpy as np
import pygame

from game_manager import ClassManager as CM
from game_manager import GameManager as GM


class Map:
    def __init__(self):
        self.map = None
        self.rect = pygame.Rect(0, 0, GM._scr.get_width(), GM._scr.get_height())
        self.width = 0
        self.height = 0

    def set_map(self, map):
        subsurface_rect = pygame.Rect(0, 0, map.get_width() // 2, map.get_height() // 2)
        self.width = map.get_width()
        self.height = map.get_height()

        subsurface = map.subsurface(subsurface_rect)
        self.map = pygame.transform.scale(
            subsurface, (GM._scr.get_width() - 40, GM._scr.get_height() - 40)
        )

    def handle_input(self):
        pass

    def draw(self):
        pygame.draw.rect(GM.screen, (11, 11, 11), self.rect)
        GM.screen.blit(self.map, (20, 20))
        GM._scr.blit(GM.screen, (0, 0))
        pygame.display.flip()

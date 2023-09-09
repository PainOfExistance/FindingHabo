import pygame
import numpy as np
import random

class Dialougue:
    def __init__(self, assets, ai, screen):
        self.strings = assets.load_dialogue()
        self.ai = ai
        self.screen = screen
    
    def random_line(self, name):
        subtitle_font = pygame.font.Font("game_data/inter.ttf", 24)
        item_render = subtitle_font.render(
            self.strings[name]["random"][random.randint(0, len(self.strings[name]["random"])-1)],
            True,
            (44, 53, 57),
        )
        
        item_rect = item_render.get_rect(
            center=(
                self.screen.get_width() // 2,
                self.screen.get_height()-50
            )
        )
        self.screen.blit(item_render, item_rect)
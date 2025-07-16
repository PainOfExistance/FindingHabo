import numpy as np
import pygame

import asset_loader as assets
from colors import Colors
from game_manager import ClassManager as CM
from game_manager import GameManager as GM


class Effects:
    def __init__(self):
        self.effects = assets.load_effects()
        self.effects_font = pygame.font.Font("./fonts/SovngardeBold.ttf", 28)
    
    def to_dict(self):
        return {
            "effects": self.effects,
        }
    
    def from_dict(self, data):
        self.effects = data["effects"]
import pygame
import numpy as np
from asset_loader import AssetLoader

class Player:
    def __init__(self, path, screen_width, screen_height):
        asets=AssetLoader(screen_width, screen_height)
        self.player, self.player_rect=asets.load_player(path, (asets.screen_width // 2, asets.screen_height // 2))
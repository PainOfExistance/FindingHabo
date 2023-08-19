import pygame
import numpy as np
from asset_loader import AssetLoader

class Player:
    def __init__(self, path, screen_width, screen_height):
        asets=AssetLoader(screen_width, screen_height)
        self.player, self.player_rect=asets.load_player(path, (asets.screen_width // 2, asets.screen_height // 2))
        self.max_sanity=100
        self.sanity=100
        self.depleted_rect = pygame.Rect(10, 10, self.sanity, 15)
        self.border_rect = pygame.Rect(10, 10, self.max_sanity, 15)
        font = pygame.font.Font(None, 20)  # You can adjust the font and size
        self.text = font.render("Sanity", True, (255, 255, 255))  # Adjust color
        self.text_rect = self.text.get_rect(left=(self.max_sanity/2)-8, top=11)

    def update_sanity(self, value):
        self.sanity+=value
        if self.sanity > self.max_sanity:
            self.sanity = self.max_sanity
        elif self.sanity < 0:
            self.sanity = 0
        self.depleted_rect.width = self.sanity
    
    def draw(self, screen):
        screen.blit(self.player, self.player_rect)
        pygame.draw.rect(screen, (0, 0, 0), self.border_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 0, 0), self.depleted_rect, border_radius=10)
        screen.blit(self.text, self.text_rect)
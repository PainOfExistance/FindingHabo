import pygame
import numpy as np
from asset_loader import AssetLoader
from stats import Stats

class Player:
    def __init__(self, path, screen_width, screen_height):
        asets=AssetLoader(screen_width, screen_height)
        self.stats=Stats()
        self.player, self.player_rect=asets.load_player(path, (asets.screen_width // 2, asets.screen_height // 2))
        self.depleted_rect = pygame.Rect(10, 10, self.stats.health, 15)
        self.border_rect = pygame.Rect(10, 10, self.stats.max_health, 15)
        font = pygame.font.Font(None, 20)  # You can adjust the font and size
        self.text = font.render("Health", True, (255, 255, 255))  # Adjust color
        self.text_rect = self.text.get_rect(left=(self.stats.max_health/2)-9, top=11)

    def update_health(self, health):
        self.stats.update_health(health)
        self.depleted_rect.width = self.stats.health
    
    def draw(self, screen):
        screen.blit(self.player, self.player_rect)
        pygame.draw.rect(screen, (0, 0, 0), self.border_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 0, 0), self.depleted_rect, border_radius=10)
        screen.blit(self.text, self.text_rect)
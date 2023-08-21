import pygame
import numpy as np
from stats import Stats

class Player:
    def __init__(self, path, screen_width, screen_height, assets):
        self.asets=assets
        self.stats=Stats()
        self.player, self.player_rect=self.asets.load_player(path, (screen_width // 2, screen_height // 2))
        self.depleted_rect = pygame.Rect(screen_width // 2 - self.stats.max_health // 2, screen_height - 20, self.stats.health, 18)
        self.border_rect = pygame.Rect(screen_width // 2 - self.stats.max_health // 2, screen_height - 20, self.stats.max_health, 18)
        font = pygame.font.Font("inter.ttf", 13)
        self.text = font.render("Health", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(screen_width // 2, screen_height - 12))

    def update_health(self, health):
        self.stats.update_health(health)
        self.depleted_rect.width = self.stats.health
    
    def draw(self, screen):
        screen.blit(self.player, self.player_rect)
        pygame.draw.rect(screen, (0, 0, 0), self.border_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 0, 0), self.depleted_rect, border_radius=10)
        screen.blit(self.text, self.text_rect)
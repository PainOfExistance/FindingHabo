import numpy as np
import pygame

import renderer as R
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
        self.bottom_border_rect = pygame.Rect(0, GM.screen_height - 20, GM.screen_width, 20)
        self.bottom_top_rect = pygame.Rect(0, 0, GM.screen_width, 20)
        self.bottom_left_rect = pygame.Rect(0, 20, 20, GM.screen_height-20)
        self.bottom_right_rect = pygame.Rect(GM.screen_width-20, 20, 20, GM.screen_height-20)
        self.map_rect=None
        self.zoom=1
        
    def set_map(self, map):
        self.full_map = map
        self.width = map.get_width()
        self.height = map.get_height()
    
    def update_offset(self):
        self.offset = (
        (GM.relative_player_left + CM.player.player_rect.width // 2) // 2 - GM.screen.get_width() // 2,
        (GM.relative_player_top + CM.player.player_rect.height // 2) // 2 - GM.screen.get_height() // 2
        )

        self.map = pygame.transform.scale(
            self.full_map,
            (
                self.width // 2,
                self.height // 2,
            ),
        )
        self.map_rect = self.map.get_rect()
        self.map_rect.topleft = (-self.offset[0], -self.offset[1])

    def handle_input(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        top_rect = pygame.Rect(0, 0, GM.screen_width, 100)
        bottom_rect = pygame.Rect(0, GM.screen_height - 100, GM.screen_width, 100)
        left_rect = pygame.Rect(0, 0, 100, GM.screen_height)
        right_rect = pygame.Rect(GM.screen_width - 100, 0, 100, GM.screen_height)

        top_left_rect = pygame.Rect(0, 0, 100, 100)
        top_right_rect = pygame.Rect(GM.screen_width - 100, 0, 100, 100)
        bottom_left_rect = pygame.Rect(0, GM.screen_height - 100, 100, 100)
        bottom_right_rect = pygame.Rect(GM.screen_width - 100, GM.screen_height - 100, 100, 100)

        if top_left_rect.collidepoint(mouse_x, mouse_y):
            self.move_image(1, 1) 
        elif top_right_rect.collidepoint(mouse_x, mouse_y):
            self.move_image(-1, 1)  
        elif bottom_left_rect.collidepoint(mouse_x, mouse_y):
            self.move_image(1, -1)  
        elif bottom_right_rect.collidepoint(mouse_x, mouse_y):
            self.move_image(-1, -1)  
        elif top_rect.collidepoint(mouse_x, mouse_y):
            self.move_image(0, 1)  
        elif bottom_rect.collidepoint(mouse_x, mouse_y):
            self.move_image(0, -1)  
        elif left_rect.collidepoint(mouse_x, mouse_y):
            self.move_image(1, 0)  
        elif right_rect.collidepoint(mouse_x, mouse_y):
            self.move_image(-1, 0)  
        
        if self.map_rect.topleft[0] > 0:
            self.map_rect.topleft = (0, self.map_rect.topleft[1])
        if self.map_rect.topleft[1] > 0:
            self.map_rect.topleft = (self.map_rect.topleft[0], 0)
            
        if -self.map_rect.topleft[0] > self.map.get_width() - GM.screen_width:
            self.map_rect.topleft = (-(self.map.get_width() - GM.screen_width)-20, self.map_rect.topleft[1])
        if -self.map_rect.topleft[1] > self.map.get_height() - GM.screen_height:
            self.map_rect.topleft = (self.map_rect.topleft[0], -(self.map.get_height() - GM.screen_height)-20)
            
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 5:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                old_zoom = self.zoom
                self.zoom = max(0.5, self.zoom - 0.01)
                if abs(old_zoom - self.zoom) >= 0.01:
                    old_center = self.map_rect.center
                    self.map = pygame.transform.scale(
                        self.full_map,
                        (
                            int((self.width // 2) * self.zoom),
                            int((self.height // 2) * self.zoom),
                        )
                    )
                    self.map_rect = self.map.get_rect()
                    self.map_rect.center = old_center
                    offset_x = (self.map_rect.centerx - mouse_x) * (1 - 1 / (old_zoom / self.zoom))
                    offset_y = (self.map_rect.centery - mouse_y) * (1 - 1 / (old_zoom / self.zoom))
                    self.map_rect.move_ip(-offset_x, -offset_y)

            elif event.button == 4:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                old_zoom = self.zoom
                self.zoom = min(1.8, self.zoom + 0.01)
                if abs(old_zoom - self.zoom) >= 0.01:
                    old_center = self.map_rect.center
                    self.map = pygame.transform.scale(
                        self.full_map,
                        (
                            int((self.width // 2) * self.zoom),
                            int((self.height // 2) * self.zoom),
                        )
                    )
                    self.map_rect = self.map.get_rect()
                    self.map_rect.center = old_center
                    offset_x = (self.map_rect.centerx - mouse_x) * (1 - 1 / (old_zoom / self.zoom))
                    offset_y = (self.map_rect.centery - mouse_y) * (1 - 1 / (old_zoom / self.zoom))
                    self.map_rect.move_ip(-offset_x, -offset_y)

    def move_image(self, dx, dy):
        magnitude = (dx ** 2 + dy ** 2) ** 0.5
        if magnitude != 0:
            dx /= magnitude
            dy /= magnitude
        
        self.map_rect.move_ip(dx * 20, dy * 20)

    def draw(self):
        GM.screen.fill((0, 0, 0))
        GM.screen.blit(self.map, self.map_rect.topleft)
        R.draw_notes(self.map_rect)
        pygame.draw.rect(GM.screen, (11, 11, 11), self.bottom_border_rect)
        pygame.draw.rect(GM.screen, (11, 11, 11), self.bottom_top_rect)
        pygame.draw.rect(GM.screen, (11, 11, 11), self.bottom_left_rect)
        pygame.draw.rect(GM.screen, (11, 11, 11), self.bottom_right_rect)
        print(self.zoom)

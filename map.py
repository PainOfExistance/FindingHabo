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

        # Define regions with multiple rectangles
        top_rect = pygame.Rect(0, 0, GM.screen_width, 100)
        bottom_rect = pygame.Rect(0, GM.screen_height - 100, GM.screen_width, 100)
        left_rect = pygame.Rect(0, 0, 100, GM.screen_height)
        right_rect = pygame.Rect(GM.screen_width - 100, 0, 100, GM.screen_height)

        # Define corner quadrants
        top_left_rect = pygame.Rect(0, 0, 100, 100)
        top_right_rect = pygame.Rect(GM.screen_width - 100, 0, 100, 100)
        bottom_left_rect = pygame.Rect(0, GM.screen_height - 100, 100, 100)
        bottom_right_rect = pygame.Rect(GM.screen_width - 100, GM.screen_height - 100, 100, 100)

        # Check if the mouse intersects with any of the rectangles
        if top_left_rect.collidepoint(mouse_x, mouse_y):
            self.move_image(1, 1)  # Move image towards top-left
        elif top_right_rect.collidepoint(mouse_x, mouse_y):
            self.move_image(-1, 1)  # Move image towards top-right
        elif bottom_left_rect.collidepoint(mouse_x, mouse_y):
            self.move_image(1, -1)  # Move image towards bottom-left
        elif bottom_right_rect.collidepoint(mouse_x, mouse_y):
            self.move_image(-1, -1)  # Move image towards bottom-right
        elif top_rect.collidepoint(mouse_x, mouse_y):
            self.move_image(0, 1)  # Move image towards top
        elif bottom_rect.collidepoint(mouse_x, mouse_y):
            self.move_image(0, -1)  # Move image towards bottom
        elif left_rect.collidepoint(mouse_x, mouse_y):
            self.move_image(1, 0)  # Move image towards left
        elif right_rect.collidepoint(mouse_x, mouse_y):
            self.move_image(-1, 0)  # Move image towards right
        
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
                self.zoom = max(0.5, self.zoom - 0.01)
                self.map = pygame.transform.scale(
                self.full_map,
                (
                    (self.width // 2)*self.zoom,
                    (self.height // 2)*self.zoom,
                ))  
        
            elif event.button == 4:
                self.zoom = min(2.0, self.zoom + 0.01)
                self.map = pygame.transform.scale(
                self.full_map,
                (
                    (self.width // 2)*self.zoom,
                    (self.height // 2)*self.zoom,
                ))
                
            tmp = self.map.get_rect()
            self.map_rect = tmp
            #todo fix left adn top relatives
    
    def move_image(self, dx, dy):
        magnitude = (dx ** 2 + dy ** 2) ** 0.5
        if magnitude != 0:
            dx /= magnitude
            dy /= magnitude
        
        self.map_rect.move_ip(dx * 20, dy * 20)
        print(self.map_rect.topleft[0], self.map_rect.topleft[1])
        print(self.map.get_width(), self.map.get_height())


    def draw(self):
        GM.screen.fill((0, 0, 0))
        GM.screen.blit(self.map, self.map_rect.topleft)
        pygame.draw.rect(GM.screen, (11, 11, 11), self.bottom_border_rect)
        pygame.draw.rect(GM.screen, (11, 11, 11), self.bottom_top_rect)
        pygame.draw.rect(GM.screen, (11, 11, 11), self.bottom_left_rect)
        pygame.draw.rect(GM.screen, (11, 11, 11), self.bottom_right_rect)

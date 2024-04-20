import numpy as np
import pygame

import renderer as R
from colors import Colors
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
        self.prompt_font = pygame.font.Font("./fonts/SovngardeBold.ttf", 20)
        
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
        
        top_rect = pygame.Rect(0, 0, GM.screen_width_scr, GM.screen_height_scr//6)
        bottom_rect = pygame.Rect(0, GM.screen_height_scr - GM.screen_height_scr//6, GM.screen_width_scr, GM.screen_height_scr//6)
        left_rect = pygame.Rect(0, 0, GM.screen_width_scr//6, GM.screen_height_scr)
        right_rect = pygame.Rect(GM.screen_width_scr - GM.screen_width_scr//6, 0, GM.screen_width_scr//6, GM.screen_height_scr)
        top_left_rect = pygame.Rect(0, 0, GM.screen_width_scr//6, GM.screen_height_scr//6)
        top_right_rect = pygame.Rect(GM.screen_width_scr - GM.screen_width_scr//6, 0, GM.screen_width_scr//6, GM.screen_height_scr//6)
        bottom_left_rect = pygame.Rect(0, GM.screen_height_scr - GM.screen_height_scr//6, GM.screen_width_scr//6, GM.screen_height_scr//6)
        bottom_right_rect = pygame.Rect(GM.screen_width_scr - GM.screen_width_scr//6, GM.screen_height_scr - GM.screen_height_scr//6, GM.screen_width_scr//6, GM.screen_height_scr//6)

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
    
    def fast_travel(self):
        CM.game.loading()
        offset = (
            GM.location_hovered["x"] - GM.screen.get_width() // 2,
            GM.location_hovered["y"] - GM.screen.get_height() // 2,
        )

        GM.bg_rect.left = -offset[0]
        GM.bg_rect.top = -offset[1]

        CM.player.player_rect.left = GM.location_hovered["x"] - offset[0]
        CM.player.player_rect.top = GM.location_hovered["y"] - offset[1]
        
        GM.map_shown = not GM.map_shown
        pygame.mouse.set_visible(GM.map_shown)
        
    def draw(self):
        GM.screen.fill((0, 0, 0))
        GM.screen.blit(self.map, self.map_rect.topleft)
        R.draw_notes(self.map_rect, self.prompt_font)
        pygame.draw.rect(GM.screen, Colors.dark_black, self.bottom_border_rect)
        pygame.draw.rect(GM.screen, Colors.dark_black, self.bottom_top_rect)
        pygame.draw.rect(GM.screen, Colors.dark_black, self.bottom_left_rect)
        pygame.draw.rect(GM.screen, Colors.dark_black, self.bottom_right_rect)
        if GM.can_fast_travel:
            text = self.prompt_font.render(f"(Hold the icon to fast travel)", True, Colors.active_item)
            text_rect = text.get_rect(center=(GM.screen.get_width()//2, GM.screen.get_height()-11))
            GM.screen.blit(text, text_rect)
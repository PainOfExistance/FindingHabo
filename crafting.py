import numpy as np
import pygame

import asset_loader as assets
from colors import Colors
from game_manager import ClassManager as CM
from game_manager import GameManager as GM


class Crafting:
    def __init__(self):
        self.recepies= assets.load_recepies()
        self.active_recepies=[]
        
    def filter_recepies(self, type):
        self.active_recepies = filter(lambda x: x['type'] == type, self.recepies)
    
    def draw_crafting(self, menu_font):
        pygame.draw.rect(
            GM.bg_surface_menu,
            Colors.bg_color,
            GM.bg_surface_menu.get_rect(),
        )
        GM.screen.blit(GM.bg_surface_menu, GM.bg_menu)
        
        pygame.draw.line(
            GM.screen,
            Colors.edge_color,
            (GM.screen.get_width() // 2, 0),
            (GM.screen.get_width() // 2, GM.screen.get_height()),
            4,
        )
        
        scroll_position = (GM.selected_inventory_item // 10) * 10
        visible_items = self.active_recepies[
            scroll_position : scroll_position + 10
        ]
        
        i = 0
        item_render = menu_font.render(
            CM.player.name,
            True,
            Colors.active_item,
        )
        
        item_rect = item_render.get_rect(
            topleft=(
                GM.screen.get_width() // 2 - GM.screen.get_width() // 3,
                20 + i * 50,
            )
        )
        GM.screen.blit(item_render, item_rect)
        
        i += 1
        pygame.draw.line(
            GM.screen,
            Colors.edge_color,
            (0, 20 + i * 50),
            (GM.screen.get_width(), 20 + i * 50),
            4,
        )
        
        for index, data in enumerate(visible_items):
            color = (
                Colors.active_item
                if index == GM.selected_inventory_item - scroll_position
                else Colors.inactive_item
            )
            
            if (
                index == GM.selected_inventory_item - scroll_position
                and GM.container_menu_selected
            ):
                item_text = "}"+f" {data['name']} ({data['amount']})"
            else:
                item_text = f"    {data['name']} ({data['amount']})"
                
            item_render = menu_font.render(item_text, True, color)
            item_rect = item_render.get_rect(
                topleft=(GM.screen.get_width() // 2 + 20, 20 + (index + 2) * 40)
            )
            GM.screen.blit(item_render, item_rect)
            
            #todo make this work
            
        scroll_position = (GM.selected_inventory_item // 10) * 10
        visible_items = list(CM.inventory.quantity.items())[
            scroll_position : scroll_position + 10
        ]
        for index, (item_name, item_quantity) in enumerate(visible_items):
            color = (
                Colors.active_item
                if index == GM.selected_inventory_item - scroll_position
                else Colors.inactive_item
            )
            if GM.container_menu_selected:
                color = Colors.unselected_item
            if (
                index == GM.selected_inventory_item - scroll_position
                and not GM.container_menu_selected
            ):
                item_text = "}"+f" {item_name}: {item_quantity}"
            else:
                item_text = f"    {item_name}: {item_quantity}"
            item_render = menu_font.render(item_text, True, color)
            item_rect = item_render.get_rect(topleft=(10, 20 + (index + 2) * 40))
            GM.screen.blit(item_render, item_rect)
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
        self.filtered=False
        
    def filter_recepies(self, type):
        if isinstance(self.recepies, dict) and 'recipes' in self.recepies:
            self.active_recepies = list(filter(lambda x: x['type'] == type, self.recepies['recipes']))
            self.filtered = True
    
    def craft(self):
        item = self.active_recepies[GM.selected_inventory_item]
        for j in range(0, len(item["ingredients"]), 2):
            if item["ingredients"][j+1] > CM.inventory.quantity[item["ingredients"][j]]:
                return
                
        for i in range(0, len(item["ingredients"]), 2):
            for j in range(0, len(item["ingredients"][i+1]), 1):
                CM.player.remove_item(item["ingredients"][i])
        
        CM.player.add_item(item["name"])
                
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
            ):
                item_text = "}"+f" {data['name']} ({data['amount']})"
            else:
                item_text = f"    {data['name']} ({data['amount']})"
                
            item_render = menu_font.render(item_text, True, color)
            item_rect = item_render.get_rect(
                topleft=(GM.screen.get_width() // 2 + 20, 20 + (index + 2) * 40)
            )
            GM.screen.blit(item_render, item_rect)
            
            if (index == GM.selected_inventory_item - scroll_position):
                for i in range(0, len(data["ingredients"]), 2):
                    color = (
                        Colors.active_item
                        if (data["ingredients"][i] in CM.inventory.quantity and data["ingredients"][i + 1] >= CM.inventory.quantity[data["ingredients"][i]])
                        else Colors.inactive_item
                    )
                    if data["ingredients"][i] not in CM.inventory.quantity:
                        txt=0
                    else:
                        txt=CM.inventory.quantity[data['ingredients'][i]]
                    item_text = f"{data['ingredients'][i]}: {txt}/{data['ingredients'][i + 1]}"
                    item_render = menu_font.render(item_text, True, color)
                    item_rect = item_render.get_rect(topleft=(10, 53 + (i + 2) * 20))
                    GM.screen.blit(item_render, item_rect)
import copy
from operator import is_
from os import name

import numpy as np
import pygame

import asset_loader as assets
from colors import Colors
from game_manager import ClassManager as CM
from game_manager import GameManager as GM


class Crafting:
    def __init__(self):
        self.recepies = assets.load_recepies()
        self.active_recepies = []
        self.filtered = False
        self.type = ""
        self.tmp_items=[]
        self.held=False
        self.in_sub_menu=False
        self.selected_item={}
        self.if_sure=False
        self.types={"smithing":"Smithing", "upgrade":"Upgrading", "enchanting":"Enchatning", "alchemy": "Alchemy", "cooking": "Cooking"}

    def filter_recepies(self, type):
        if isinstance(self.recepies, dict) and 'recipes' in self.recepies:
            self.active_recepies = list(
                filter(lambda x: x['type'] == type, self.recepies['recipes']))
            self.filtered = True
            self.type = type

    def craft(self):
        if not self.if_sure:
            self.if_sure=True
            return
        elif self.if_sure:
            self.if_sure=False

        if self.type == "upgrade":
            item = copy.deepcopy(self.tmp_items[GM.selected_inventory_item])
            recepie = list(filter(lambda y: y['name'] == item['base_name'], self.active_recepies))[0]
            for j in range(0, len(recepie["ingredients"]), 2):
                if recepie["ingredients"][j] not in CM.inventory.quantity or recepie["ingredients"][j+1] > CM.inventory.quantity[recepie["ingredients"][j]]:
                    return
                
            damage, name = self.set_upgrade_level(item["name"], item["base_name"])
            if damage <= item["stats"]["damage"]:
                return
            
            for i in range(0, len(recepie["ingredients"]), 2):
                for j in range(0, recepie["ingredients"][i+1], 1):
                    CM.player.remove_item(recepie["ingredients"][i])

            CM.player.remove_item(item["name"])
            item["stats"]["damage"], item["name"] = damage, name
            CM.player.add_item(item)
            
        elif self.type == "smithing" or self.type == "alchemy" or self.type == "cooking":
            item = self.active_recepies[GM.selected_inventory_item]
            for j in range(0, len(item["ingredients"]), 2):
                if item["ingredients"][j] not in CM.inventory.quantity or item["ingredients"][j+1] > CM.inventory.quantity[item["ingredients"][j]]:
                    return

            for i in range(0, len(item["ingredients"]), 2):
                for j in range(0, item["ingredients"][i+1], 1):
                    CM.player.remove_item(item["ingredients"][i])
            
            for i in range(0, item["amount"], 1):
                CM.player.add_item(item["name"])
    
    def set_upgrade_level(self, name, base_name):
        if "weak" in name:
            return GM.items[base_name]["stats"]["damage"], name.replace(" (weak)", "")
        elif "elegant" in name:
            return GM.items[base_name]["stats"]["damage"]*1.25, name.replace(" (elegant)", " (superior)")
        elif "superior" in name:
            return GM.items[base_name]["stats"]["damage"]*1.4, name.replace(" (superior)", " (immaculate)")
        elif "immaculate" in name:
            return GM.items[base_name]["stats"]["damage"]*1.55, name.replace(" (immaculate)", " (epic)")
        elif "epic" in name:
            return GM.items[base_name]["stats"]["damage"]*1.75, name.replace(" (epic)", " (legendary)")
        else:
            return GM.items[base_name]["stats"]["damage"]*1.12, name+" (elegant)"         

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
            scroll_position: scroll_position + 10
        ]

        i = 0
        item_render = menu_font.render(
            self.types[self.type],
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
                topleft=(GM.screen.get_width() // 2 +
                         20, 20 + (index + 2) * 40)
            )
            GM.screen.blit(item_render, item_rect)

            if (index == GM.selected_inventory_item - scroll_position):
                for i in range(0, len(data["ingredients"]), 2):
                    color = (
                        Colors.active_item
                        if (data["ingredients"][i] in CM.inventory.quantity and data["ingredients"][i + 1] <= CM.inventory.quantity[data["ingredients"][i]])
                        else Colors.inactive_item
                    )
                    
                    if (data["ingredients"][i] not in CM.inventory.quantity or data["ingredients"][i + 1] > CM.inventory.quantity[data["ingredients"][i]]):
                        self.if_sure=False
                        
                    if data["ingredients"][i] not in CM.inventory.quantity:
                        txt = 0
                    else:
                        txt = CM.inventory.quantity[data['ingredients'][i]]
                    item_text = f"{data['ingredients'][i]}: {
                        txt}/{data['ingredients'][i + 1]}"
                    item_render = menu_font.render(item_text, True, color)
                    item_rect = item_render.get_rect(
                        topleft=(10, 53 + (i + 2) * 20))
                    GM.screen.blit(item_render, item_rect)
            
            if self.if_sure:
                item_render = menu_font.render(
                    "Are you sure?",
                    True,
                    Colors.active_item
                )
                item_rect = item_render.get_rect(
                    topleft=(
                        GM.screen.get_width() // 2 + GM.screen.get_width() // 9,
                        20
                    )
                )
                GM.screen.blit(item_render, item_rect)

    def draw_upgrade(self, menu_font):
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
        self.tmp_items = [CM.inventory.items[x] for x in CM.inventory.items if CM.inventory.items[x]['type'] in ['weapon', 'armor']]
            
        visible_items = self.tmp_items[
            scroll_position: scroll_position + 10
        ]

        i = 0
        item_render = menu_font.render(
            self.types[self.type],
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
                item_text = "}"+f" {data['name']
                                    } ({CM.inventory.quantity[data['name']]})"
            else:
                item_text = f"    {
                    data['name']} ({CM.inventory.quantity[data['name']]})"

            item_render = menu_font.render(item_text, True, color)
            item_rect = item_render.get_rect(
                topleft=(GM.screen.get_width() // 2 +
                         20, 20 + (index + 2) * 40)
            )
            GM.screen.blit(item_render, item_rect)

            if (index == GM.selected_inventory_item - scroll_position):
                recepie = list(filter(lambda y: y['name'] == data['base_name'], self.active_recepies))[0]
                for i in range(0, len(recepie["ingredients"]), 2):
                    color = (
                        Colors.active_item
                        if (recepie["ingredients"][i] in CM.inventory.quantity and recepie["ingredients"][i + 1] <= CM.inventory.quantity[recepie["ingredients"][i]])
                        else Colors.inactive_item
                    )
                    if (recepie["ingredients"][i] not in CM.inventory.quantity or recepie["ingredients"][i + 1] > CM.inventory.quantity[recepie["ingredients"][i]]):
                        self.if_sure=False
                        
                    if recepie["ingredients"][i] not in CM.inventory.quantity:
                        txt = 0
                    else:
                        txt = CM.inventory.quantity[recepie['ingredients'][i]]
                        
                    item_text = f"{recepie['ingredients'][i]}: {txt}/{recepie['ingredients'][i + 1]}"
                    item_render = menu_font.render(item_text, True, color)
                    item_rect = item_render.get_rect(
                        topleft=(10, 53 + (i + 2) * 20))
                    GM.screen.blit(item_render, item_rect)
                    
            if self.if_sure:
                item_render = menu_font.render(
                    "Are you sure?",
                    True,
                    Colors.active_item
                )
                item_rect = item_render.get_rect(
                    topleft=(
                        GM.screen.get_width() // 2 + GM.screen.get_width() // 9,
                        20
                    )
                )
                GM.screen.blit(item_render, item_rect)
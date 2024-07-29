import random
import string

import numpy as np
import pygame

import asset_loader as assets
from colors import Colors
from game_manager import ClassManager as CM
from game_manager import GameManager as GM


class Inventory:
    def __init__(self):
        self.items = {}
        self.quantity = {}
        self.images = {}
        self.inventory_font = pygame.font.Font("./fonts/SovngardeBold.ttf", 28)
        
    def add_item(self, item):
        name = item["name"]
        if name in self.items:
            self.quantity[name] += 1
        else:
            self.quantity[name] = 1
            self.items[name] = item
            img, rect= assets.load_images(item["image"], (0, 0), (0, 0))
            self.images[name] = {"img": img, "rect": rect}

    def remove_item(self, name):
        if name in self.items and self.quantity[name] > 1:
            self.quantity[name] -= 1
        elif name in self.items:
            del self.items[name]
            del self.quantity[name]
            del self.images[name]
    
    def to_dict(self):
        return {
            "items": self.items,
            "quantity": self.quantity,
        }

    def from_dict(self, data):
        self.items = data["items"]
        self.quantity = data["quantity"]
            
    def draw(self, selected_sub_item, sub_items, left=220, ofset=0):
        scroll_position = (selected_sub_item // 6) * 6
        visible_items = list(self.quantity.items())[scroll_position : scroll_position + 6]
        index=0
        for i, (item_name, item_quantity) in enumerate(visible_items):
            color = (
                Colors.active_item
                if i == selected_sub_item - scroll_position
                else Colors.inactive_item
                if sub_items
                else Colors.unselected_item
            )
            if i == selected_sub_item - scroll_position:
                item_text = "}"+f" {item_name}: {item_quantity} Value: {self.items[item_name]['price']}"
                if "stats" in self.items[item_name] and self.items[item_name]['stats']["equiped"]:
                    item_text = "}"+f" {item_name}: {item_quantity} Value: {self.items[item_name]['price']} <"
            else:
                item_text = f"    {item_name}: {item_quantity} Value: {self.items[item_name]['price']}"
                if "stats" in self.items[item_name] and self.items[item_name]['stats']["equiped"]:
                    item_text = f"    {item_name}: {item_quantity} Value: {self.items[item_name]['price']} <"
                    
            
            item_render = self.inventory_font.render(item_text, True, color)
            item_rect = item_render.get_rect(topleft=(left, ofset + 20 + index * 40))
            GM.screen.blit(item_render, item_rect)

            self.images[item_name]["rect"].topleft=(GM.screen.get_width()-64, ofset + 40 + index * 40)
            GM.screen.blit(self.images[item_name]["img"], self.images[item_name]["rect"])
            index += 1
            
            item_render = self.inventory_font.render(self.items[item_name]['description'], True, color)
            item_rect = item_render.get_rect(topleft=(left+100, ofset + 20 + index * 40))
            index += 1
            GM.screen.blit(item_render, item_rect)
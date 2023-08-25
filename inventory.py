import pygame
import numpy as np
import random
import string

class Inventory:
    def __init__(self):
        self.items = {}
        self.quantity = {}
    
    def add_item(self, item):
        name = item["name"]
        if name in self.items:
            self.quantity[name] += 1
        else:
            self.quantity[name] = 1
            self.items[name] = item

    def remove_item(self, name):
        if name in self.items and self.quantity[name] > 1:
            self.quantity[name] -= 1
        elif name in self.items:
            del self.items[name]
            del self.quantity[name]
            
    def draw(self, screen, selected_sub_item, sub_items):
        inventory_font = pygame.font.Font("inter.ttf", 24)
        item_spacing = 40
        text_y = 20
        max_visible_items = 4  # Change this to the desired number of visible items at a time

        scroll_position = selected_sub_item  # Use selected_sub_item as the scroll position
        visible_items = list(self.quantity.items())[scroll_position : scroll_position + max_visible_items]
        if selected_sub_item > len(visible_items):
            pass

        for index, (item_name, item_quantity) in enumerate(visible_items):
            color = (
                (157, 157, 210)
                if index == selected_sub_item - scroll_position
                else (237, 106, 94)
                if sub_items
                else (120, 120, 120)
            )
            if index == selected_sub_item - scroll_position:
                item_text = f"> {item_name}: {item_quantity} desc: {self.items[item_name]['description']}"
                if "stats" in self.items[item_name] and self.items[item_name]['stats']["equiped"]:
                    item_text = f"> {item_name}: {item_quantity} desc: {self.items[item_name]['description']} ◄"
            else:
                item_text = f"    {item_name}: {item_quantity} desc: {self.items[item_name]['description']}"
                if "stats" in self.items[item_name] and self.items[item_name]['stats']["equiped"]:
                    item_text = f"    {item_name}: {item_quantity} desc: {self.items[item_name]['description']} ◄"

            item_render = inventory_font.render(item_text, True, color)
            item_rect = item_render.get_rect(topleft=(220, 20 + index * 40))
            screen.blit(item_render, item_rect)
            text_y += item_spacing

        
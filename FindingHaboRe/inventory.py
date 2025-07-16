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
import pygame
import numpy as np
import random
import string

class Inventory:
    def __init__(self):
        self.items = {}
        self.quantity = {}
    
    def add_item(self, name, item):
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
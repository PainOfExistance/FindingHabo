import random

import numpy as np

import asset_loader as assets
from game_manager import ClassManager as CM
from game_manager import GameManager as GM


class LevelList:
    def __init__(self):
        pass
        
    def generate_level_list(self, type):
        match(type):
            case "weapon":
                return self.generate_weapon_level_list()
            case "armor":
                return self.generate_armor_level_list()
            case _:
                return self.generate_weapon_level_list()
    
    def generate_weapon_level_list(self):
        #todo all of thsi shit
        level_list = []
        for i in range(1, 6):
            level_list.append(f"level_{i}")
        return level_list
    
    def generate_armor_level_list(self):
        level_list = []
        level_list.append("level_1")
        return level_list
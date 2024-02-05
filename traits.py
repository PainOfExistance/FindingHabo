import json

import numpy as np
import pygame

from game_manager import ClassManager as CM


class Traits:
    def __init__(self):
        self.unused_trait_points = 0
        self.traits = CM.assets.load_traits()
        
    def add_trait(self, name, lvl):
        for level in self.traits[name]["levels"]:
            if not level["taken"] and self.unused_trait_points > 0 and level["level"] <= lvl:
                level["taken"] = True
                self.unused_trait_points -= 1
                return (level["effect"], self.traits[name]["stat"])
        return (None, None)
    
    def check_trait_conditions(self, name, lvl):
        for level in self.traits[name]["levels"]:
            if not level["taken"] and self.unused_trait_points > 0 and level["level"] <= lvl:
                return True
        return False       
    
    def to_dict(self):
        return {
            "unused_trait_points": self.unused_trait_points,
            "traits": self.traits
        }
    
    def from_dict(self, data):
        self.unused_trait_points = data["unused_trait_points"]
        self.traits = data["traits"] 
        
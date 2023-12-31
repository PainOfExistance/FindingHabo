import pygame
import json
import numpy as np

class Traits:
    def __init__(self, assets):
        self.unused_trait_points = 0
        self.traits = assets.load_traits()
        
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
        
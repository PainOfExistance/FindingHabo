import pygame
import numpy as np
from traits import Traits

class LevelingSystem:
    def __init__(self, assets):
        self.level = 1
        self.experience = 0
        self.required_experience = 100
        self.traits = Traits(assets)

    def gain_experience(self, amount):
        self.experience += amount
        while self.experience >= self.required_experience:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.traits.unused_trait_points =+ 2
        self.experience -= self.required_experience
        self.required_experience = self.calculate_next_required_experience(self.level)
        
    def calculate_next_required_experience(self, current_level):
        base_experience = 100
        experience_increment = 50
        increment_multiplier = 1.1 
        return int(base_experience + (experience_increment * (increment_multiplier ** (current_level - 2))))
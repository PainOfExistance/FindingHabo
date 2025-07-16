import numpy as np
import pygame

from colors import Colors
from game_manager import ClassManager as CM
from game_manager import GameManager as GM
from traits import Traits


class LevelingSystem:
    def __init__(self):
        self.level = 1
        self.experience = 0
        self.required_experience = 100
        self.traits = Traits()
        self.trait_font = pygame.font.Font("./fonts/SovngardeBold.ttf", 28)

    def gain_experience(self, amount):
        self.experience += amount
        while self.experience >= self.required_experience:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.traits.unused_trait_points += 2
        self.experience -= self.required_experience
        self.required_experience = self.calculate_next_required_experience(self.level)

    def calculate_next_required_experience(self, current_level):
        base_experience = 100
        experience_increment = 50
        increment_multiplier = 1.1
        return int(
            base_experience
            + (experience_increment * (increment_multiplier ** (current_level - 2)))
        )
        #(75 x (Next Level - 1))+200 
    
    def to_dict(self):
        return {
            "level": self.level,
            "experience": self.experience,
            "required_experience": self.required_experience,
            "traits": self.traits.to_dict(),
        }

    def from_dict(self, data):
        self.level = data["level"]
        self.experience = data["experience"]
        self.required_experience = data["required_experience"]
        self.traits.from_dict(data["traits"])
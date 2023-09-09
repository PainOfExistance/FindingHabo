import pygame
import numpy as np
import random


class Dialougue:
    def __init__(self, assets, ai, screen):
        self.strings = assets.load_dialogue()
        self.ai = ai
        self.screen = screen

    def random_line(self, name):
        current_string = {"text": "", "dialogue": False}
        
        current_string["text"] = (
            name
            + ": "
            + self.strings[name]["random"][
                random.randint(0, len(self.strings[name]["random"]) - 1)
            ]
        )
        
        return current_string

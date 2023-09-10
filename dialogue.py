import pygame
import numpy as np
import random


class Dialougue:
    def __init__(self, assets, ai, screen):
        self.strings = assets.load_dialogue()
        self.ai = ai
        self.screen = screen

    def random_line(self, name):
        current_string = {"text": "", "dialogue": False, "file": ""}
        index = random.randint(0, len(self.strings[name]["random"]) - 1)
        line = self.strings[name]["random"][index]
        line_file = self.strings[name]["random_file"][index]
        current_string["text"] = name + ": " + line
        current_string["file"] = line_file

        return current_string

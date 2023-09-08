import pygame
import numpy as np

class Dialougue:
    def __init__(self, assets):
        self.strings=assets.load_dialogue()
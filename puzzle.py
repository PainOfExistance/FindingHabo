import numpy as np
import pygame


class Puzzle:
    def __init__(self, puzzle_data):
        self.type = puzzle_data['type']
        self.x = puzzle_data['x']
        self.y = puzzle_data['y']
        self.width = puzzle_data['width']
        self.height = puzzle_data['height']
        self.buttons = puzzle_data.get('buttons', [])
        self.solution = puzzle_data.get('solution', [])

    def check_solution(self, pressed_buttons):
        return sorted(pressed_buttons) == sorted(self.solution)
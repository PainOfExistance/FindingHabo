import math
import random
from turtle import speed

import numpy as np
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from game_manager import GameManager as GM


class PathFinder:
    def __init__(self):
        self.path = Grid(matrix=GM.collision_map)
        self.finder = AStarFinder()
    
    def update(self):
        self.path = Grid(matrix=GM.collision_map)  
          
    def find_path(self, start, end):
        start_node = Grid.node(*start)
        end_node = Grid.node(*end)
        return self.finder.find_path(start_node, end_node, self.path)
    
    def fix_path(self, path):
        #todo make this work
        return [(int(node[0]), int(node[1])) for node in path]
    
    def check_collision(self, dx, dy, rect):
        new_center = (rect.centerx + dx, rect.centery + dy)
        # Calculate the boundaries of the collision area
        top = int(rect.top + dy)
        bottom = int(rect.bottom + dy)
        left = int(rect.left + dx)
        right = int(rect.right + dx)
        collision_area = GM.collision_map[top: bottom, left: right]
        if np.count_nonzero(collision_area) <= 30:
            return new_center
        return rect.center

    def move(self, npc, target):
        x, y = npc["rect"].center
        target_x, target_y = target
        dx = target_x - x
        dy = target_y - y

        magnitude = math.sqrt(dx ** 2 + dy ** 2)
        if magnitude != 0:
            dx /= magnitude
            dy /= magnitude

        speed = npc["name"]["movement_behavior"]["movement_speed"] * GM.delta_time
        dx *= speed
        dy *= speed

        new_center_x, new_center_y = self.check_collision(dx, dy, npc["rect"])
        npc["rect"].centerx = new_center_x
        npc["rect"].centery = new_center_y
        return npc
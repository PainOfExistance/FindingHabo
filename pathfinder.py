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
    
    def fix_path(self, path):
        return [(int(node[0]), int(node[1])) for node in path]
    
    def find_path(self, start, end):
        start_node = Grid.node(*start)
        end_node = Grid.node(*end)
        return self.finder.find_path(start_node, end_node, self.path)
    
    def check_collision(self, collision_map, x, y, rect):
        prev_center = rect.center
        rect.center = (x, y)

        collision_area = collision_map[rect.top: rect.top +
                                       rect.height, rect.left: rect.left + rect.width]
        if np.count_nonzero(collision_area) <= 30:
            return x, y

        rect.center = prev_center
        return rect.center
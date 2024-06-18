import copy
import math
import random
from os import close
from tokenize import group
from turtle import speed

import numpy as np
from pathfinding.core.grid import Grid
from pathfinding.core.node import Node
from pathfinding.finder.a_star import AStarFinder

from astar import AStar
from game_manager import GameManager as GM


class PathFinder:
    def __init__(self):
        #self.finder = AStar(GM.collision_map)
        self.movement_vectors = {
         (0, -1): 1,
         (-1, -1): 1,
         (1, -1): 1,
         (-1, 1):  2,
         (0, 1):  2,
         (1, 1):  2,
         (1, 0):  3,
         (1, 1):  3,
         (1, -1):  3,
         (-1, -1): 4,
         (-1, 0): 4,
         (-1, 1): 4,
        }

    
    #def update(self):
    #    self.finder = AStar(GM.collision_map)
          
    def find_path(self, start, end, size=(1, 1)):
        return self.finder.find_path(start, end, size)
    
    def fix_path(self, path):
        #todo make this work
        return [(int(node[0]), int(node[1])) for node in path]
    
    def find_global_nav_points(self, action, npc):
        if "name" in npc:
            npc_group = npc["name"]["stats"]["group"]
            npc_center=npc["rect"]["center"]
            world=npc["name"]["world"].replace(" ","_")
        elif npc is type(tuple):
            npc_group = npc[0]["stats"]["group"]
            npc_center = npc[-1]
            world=npc[0]["world"].replace(" ","_")
        else:
            npc_group = npc["customFields"]["enemy_Type"]
            npc_center=(npc["x"],npc["y"])
            world=npc["world"].replace(" ","_")
            
        #npc_group = npc["name"]["stats"]["group"]
        min_distance = float('inf')
        closest_column_index = None
        closest_object_index = None
        nav_tiles=GM.global_nav_tiles[world]
        for i, column in enumerate(nav_tiles):
            if np.any([obj[0]['action'] == action for obj in column]):
                for j, obj in enumerate(column):
                    obj_group = obj[0]['group']
                    obj_action = obj[0]['action']
                    if npc_group in obj_group or 'All' in obj_group:
                        distance = math.dist(npc_center, obj[1])
                        if distance < min_distance:
                            min_distance = distance
                            closest_column_index = i
                            closest_object_index = j

        for i, column in enumerate(nav_tiles[closest_column_index]):
            obj_group = column[0]['group']
            obj_action = column[0]['action']
            if action==obj_action:
                return closest_object_index, i, closest_column_index
    
    def find_nav_points(self, action, npc):
        npc_group = npc["name"]["stats"]["group"]
        min_distance = float('inf')
        closest_column_index = None
        closest_object_index = None
        
        for i, column in enumerate(GM.nav_tiles):
            if np.any([obj['name']['action'] == action for obj in column]):
                for j, obj in enumerate(column):
                    obj_group = obj['name']['group']
                    obj_action = obj['name']['action']
                    if npc_group in obj_group or 'All' in obj_group:
                        distance = math.dist(npc["rect"].center, obj['rect'].center)
                        if distance < min_distance:
                            min_distance = distance
                            closest_column_index = i
                            closest_object_index = j

        for i, column in enumerate(GM.nav_tiles[closest_column_index]):
            obj_group = column['name']['group']
            obj_action = column['name']['action']
            if action==obj_action:
                return closest_object_index, i, closest_column_index
    
    def check_collision(self, dx, dy, rect):
        new_center = (rect["centerx"] + dx, rect["centery"] + dy)
        # Calculate the boundaries of the collision area
        top = int(rect["top"] + dy)
        bottom = int(rect["bottom"] + dy)
        left = int(rect["left"] + dx)
        right = int(rect["right"] + dx)
        collision_area = GM.collision_map[top: bottom, left: right]
        if np.count_nonzero(collision_area) <= 30:
            return new_center
        return rect["center"]

    def move(self, npc, target):
        x, y = npc["rect"]["center"]
        target_x, target_y = target
        dx = target_x - x
        dy = target_y - y
        
        tdx=int(dx/abs(dx))
        tdy=int(dy/abs(dy))
        
        magnitude = math.sqrt(dx ** 2 + dy ** 2)
        if magnitude != 0:
            dx /= magnitude
            dy /= magnitude

        speed = npc["name"]["movement_behavior"]["movement_speed"] * GM.delta_time
        dx *= speed
        dy *= speed

        new_center_x, new_center_y = self.check_collision(dx, dy, npc["rect"])
        npc["rect"]["centerx"] = new_center_x
        npc["rect"]["centery"] = new_center_y
        
        npc["name"]["movement_behavior"]["dirrection"]=copy.deepcopy(self.movement_vectors[(tdx, tdy)])
        return npc
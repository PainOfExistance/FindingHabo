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
        self.finder = AStar(GM.collision_map)
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

    
    def update(self):
        self.finder = AStar(GM.collision_map)
          
    def find_path(self, start, end, size=(1, 1)):
        return self.finder.find_path(start, end, size)
    
    def fix_path(self, path):
        #todo make this work
        return [(int(node[0]), int(node[1])) for node in path]
    
    def find_nav_points(self, action, npc):
        npc_group = npc["name"]["stats"]["group"]
        min_distance = float('inf')
        closest_column_index = None
        closest_object_index = None

        # Iterate over all columns and objects to find the closest one with the specified action
        for i, column in enumerate(GM.nav_tiles):
            #print()
            #print(column, action, np.any([obj['name']['action'] == action for obj in column]))
            #print()
            if np.any([obj['name']['action'] == action for obj in column]):
                for j, obj in enumerate(column):
                    obj_group = obj['name']['group']
                    obj_action = obj['name']['action']
                    # Check if the object's group matches NPC group or 'All'
                    if npc_group in obj_group or 'All' in obj_group:
                        # Calculate the distance between specified point and object's center
                        distance = math.dist(npc["rect"].center, obj['rect'].center)
                        # Update closest indexes if this object is closer
                        if distance < min_distance:
                            min_distance = distance
                            closest_column_index = i
                            closest_object_index = j

        for i, column in enumerate(GM.nav_tiles[closest_column_index]):
            obj_group = column['name']['group']
            obj_action = column['name']['action']
            if action==obj_action:
                return closest_object_index, i, closest_column_index
                        

        ## Now find the object with action 'market' in the closest column
        #if closest_column_index is not None:
        #    closest_column = filtered_columns[closest_column_index]
        #    min_distance_to_market = float('inf')
        #    closest_market_index = None
        #    for k, obj in enumerate(closest_column):
        #        obj_group = obj['name']['group']
        #        obj_action = obj['name']['action']
        #        if 'All' in obj_group or npc_group in obj_group:
        #            if obj_action == action:
        #                # Calculate the distance between the closest object and 'market' object
        #                obj_center_x, obj_center_y = obj['rect'].center
        #                distance_to_market = np.sqrt((obj_center_x - closest_column[closest_object_index]['rect'].center[0]) ** 2 + (obj_center_y - closest_column[closest_object_index]['rect'].center[1]) ** 2)
        #                # Update closest market object index if this 'market' object is closer
        #                if distance_to_market < min_distance_to_market:
        #                    min_distance_to_market = distance_to_market
        #                    closest_market_index = k
    
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
        npc["rect"].centerx = new_center_x
        npc["rect"].centery = new_center_y
        
        npc["name"]["movement_behavior"]["dirrection"]=copy.deepcopy(self.movement_vectors[(tdx, tdy)])
        return npc
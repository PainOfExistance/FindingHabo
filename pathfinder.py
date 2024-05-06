import math

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
        #todo make this work
        return [(int(node[0]), int(node[1])) for node in path]
    
    def find_path(self, start, end):
        start_node = Grid.node(*start)
        end_node = Grid.node(*end)
        return self.finder.find_path(start_node, end_node, self.path)
    
    def check_collision(self, x, y, rect):
        prev_center = rect.center
        rect.center = (x, y)

        collision_area = GM.collision_map[rect.top: rect.top +
                                       rect.height, rect.left: rect.left + rect.width]
        if np.count_nonzero(collision_area) <= 30:
            return x, y

        rect.center = prev_center
        return rect.center
    
   # def find_closest_rect(self, group, coordinate, action):
        min_distance = float('inf')  # Initialize with infinity
        closest_column_index = 0
        closest_index_in_column = 0

        for col_index, column in enumerate(GM.nav_tiles):
            for row_index, rect_info in enumerate(column):
                rect = rect_info['rect']
                rect_group = rect_info['name']['group']

                # Check if the group matches the specified group and action matches the specified action
                if (group in rect_group or "All" in group) and (column[-1]["name"]["action"] == action):
                    # Calculate the center coordinates of the rect
                    center_x = rect.x + rect.width / 2
                    center_y = rect.y + rect.height / 2

                    # Calculate the distance between the rect's center and the coordinate
                    distance = np.sqrt((center_x - coordinate[0]) ** 2 + (center_y - coordinate[1]) ** 2)

                    # Update if current rect is closest
                    if distance < min_distance:
                        min_distance = distance
                        closest_column_index = col_index
                        closest_index_in_column = row_index

        return closest_column_index, closest_index_in_column

   # def get_path(self, group, coordiante, action):
        column, index = self.find_closest_rect(group, coordiante, action)
        path=[x["rect"].center for x in GM.nav_tiles[column][index:-1]]
        print()
        print(path)
        print()
        return path
 
   # def determine_direction(self, npc_position, target_position):
        # Calculate the horizontal and vertical distances between the points
        dx = target_position[0] - npc_position[0]
        dy = target_position[1] - npc_position[1]    
        dirrection=0
        # Determine the direction based on the sign of horizontal and vertical distances
        if abs(dx) > abs(dy):
            # Horizontal distance is greater than vertical distance
            if dx > 0:
                dirrection=1  # Right
            else:
                dirrection=3  # Left
        else:
            # Vertical distance is greater than or equal to horizontal distance
            if dy > 0:
                dirrection=2  # Down
            else:
                dirrection=0  # Up     
        return dirrection, dx/abs(dx), dy/abs(dy)
   #        
   # def move(self, npc):
        name=npc["name"]["name"]
        if len(npc["name"]["path"])>0 and npc["rect"].colliderect(npc["name"]["path"][0]):
            npc["name"]["path"].pop(0)
            
        if len(npc["name"]["path"])>0 and not npc["rect"].colliderect(npc["name"]["path"][0]):
            speed = GM.ai_package[name]["movement_behavior"]["movement_speed"]*GM.delta_time
            dirrection, dx, dy=self.determine_direction(npc["rect"].center, npc["name"]["path"][0].center)
            self.check_collision(npc["rect"].centerx+speed*dx, npc["rect"].centery+speed*dy, npc["rect"])
            npc["name"]["movement_behavior"]["dirrection"]=dirrection
        else:
            npc["name"]["path"]=self.pathfiner.get_path(npc["name"]["stats"]["group"], npc["rect"].center, npc["name"]["routine"][3])     
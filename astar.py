import heapq

import numpy as np


class AStar:
    def __init__(self, grid):
        self.grid = np.array(grid)
        self.width, self.height = self.grid.shape

    def heuristic(self, a, b):
        # Manhattan distance heuristic
        return np.abs(b[0] - a[0]) + np.abs(b[1] - a[1])

    def find_path(self, start, end, npc_size):
        # Check if start or end points are obstructed
        if self.grid[start[0], start[1]] == 1 or self.grid[end[0], end[1]] == 1:
            return None
        
        # Initialize priority queue and set for efficient lookup
        open_set = []
        heapq.heappush(open_set, (0, start))
        visited = set()
        
        # Initialize arrays for storing costs and previous nodes
        g_cost = np.full((self.width, self.height), np.inf)
        parent = {}
        
        g_cost[start] = 0
        
        while open_set:
            _, current = heapq.heappop(open_set)
            
            if current == end:
                path = []
                while current:
                    path.append(current)
                    current = parent.get(current)
                path.reverse()
                return path
            
            visited.add(current)
            
            for dx in range(-npc_size[0] + 1, npc_size[0]):
                for dy in range(-npc_size[1] + 1, npc_size[1]):
                    x, y = current[0] + dx, current[1] + dy
                    
                    # Check if next position is within bounds and not obstructed
                    if 0 <= x < self.width and 0 <= y < self.height and self.grid[x, y] == 0 and (x, y) not in visited:
                        new_g_cost = g_cost[current] + 1
                        if new_g_cost < g_cost[x, y]:
                            g_cost[x, y] = new_g_cost
                            parent[(x, y)] = current
                            heapq.heappush(open_set, (new_g_cost + self.heuristic((x, y), end), (x, y)))
        
        # If no path found
        return None

    
    #https://media.discordapp.net/attachments/462552907267702804/1237814820867145841/y2mate.com_-_Remastered_Soviet_Victory_Day_Parade_1985_1985__360p_3.gif?ex=663e55e2&is=663d0462&hm=34e09684709ffca010c5d541b625b39b100dc76c162ce868554dadeccceec430&
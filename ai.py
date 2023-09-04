import pygame
import random

class Ai:
    def __init__(self, npcs, assets):
        self.npcs = npcs
        self.ai_package=assets.load_ai_package()
        self.dt = 0

    def update_npcs(self, npcs):
        self.npcs = npcs

    def update(self, name, dt, collision):
        self.dt = dt
        print(collision)
        if self.ai_package[name]["movement_behavior"]["type"] == "patrol" and not collision:
            # Implement random movement within a patrol area
            return self.random_patrol(name)
        if self.ai_package[name]["movement_behavior"]["type"] == "stand" and not collision:
            return self.npcs[name]["position"]
        elif self.ai_package[name]["movement_behavior"]["type"] == "patrol" and collision:
            return 200, 300 

    def random_patrol(self, name):
        # Simulate random movement within a patrol area
        patrol_speed = self.ai_package[name]["movement_behavior"]["movement_speed"]
        position = self.npcs[name]["position"]
        y = position[0]
        x = position[1]

        # Generate a random movement direction
        dx, dy= 0, 0
        rng=random.randint(0, 3)
        if rng == 0:
            dx = -1
        elif rng == 1:
            dx = 1
        elif rng == 2:
            dy = -1
        elif rng == 3:
            dy = 1

        # Update NPC's position based on the direction and speed
        x += dx * patrol_speed * self.dt
        y += dy * patrol_speed * self.dt

        # Update the NPC's position within the patrol area
        # You can add logic to ensure the NPC stays within bounds
        
        return x, y
    
    def attack(self, name, dt):
        pass

import pygame
import random

class Ai:
    def __init__(self, npcs, assets):
        self.npcs = npcs
        self.ai_package=assets.load_ai_package()
        self.dt = 0

    def update_npcs(self, npcs):
        self.npcs = npcs

    def update(self, name, dt):
        print(name)
        self.dt = dt
        if self.ai_package[name]["movement_behavior"]["type"] == "patrol":
            # Implement random movement within a patrol area
            return self.random_patrol(name)
        elif self.ai_package[name]["movement_behavior"]["type"] == "stand":
            return self.npcs[name]["position"]

    def random_patrol(self, name):
        # Simulate random movement within a patrol area
        patrol_speed = self.ai_package[name]["movement_behavior"]["movement_speed"]
        position = self.npcs[name]["position"]
        y = position[0]
        x = position[1]

        # Generate a random movement direction
        dx, dy= 0, 0
        if random.uniform(-1, 1)>0:
            dx = random.uniform(-10, 10)
        else:
            dy = random.uniform(-10, 10)

        # Update NPC's position based on the direction and speed
        x += dx * patrol_speed * self.dt
        y += dy * patrol_speed * self.dt

        # Update the NPC's position within the patrol area
        # You can add logic to ensure the NPC stays within bounds
        
        return x, y

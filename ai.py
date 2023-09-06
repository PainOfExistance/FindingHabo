import pygame
import random
import numpy as np
import math


class Ai:
    def __init__(self, npcs, assets):
        self.npcs = npcs
        self.ai_package = assets.load_ai_package()
        self.dt = 0
        self.npc_movement = {}

    def update_npcs(self, npcs):
        self.npcs = npcs

    def update(self, name, dt, collision_map, relative__left, relative__top, rect):
        self.dt = dt
        if self.ai_package[name]["movement_behavior"]["type"] == "patrol":
            # Implement random movement within a patrol area
            return self.random_patrol(
                name, collision_map, relative__left, relative__top, rect
            )
        elif self.ai_package[name]["movement_behavior"]["type"] == "stand":
            return self.npcs[name]["npc"]

    def random_patrol(self, name, collision_map, relative__left, relative__top, rect):
        # Simulate random movement within a patrol area
        speed = self.ai_package[name]["movement_behavior"]["movement_speed"]
        npc = self.npcs[name]["npc"]
        y = npc[0]
        x = npc[1]

        if self.ai_package[name]["movement_behavior"]["dirrection"] == False:
            return self.rng(name, speed, x, y)

        elif self.ai_package[name]["movement_behavior"]["dirrection"] == 0:
            x += -1 * speed * self.dt
            if (
                np.count_nonzero(
                    collision_map[
                        relative__top : relative__top + rect.bottom,
                        relative__left + x : relative__left + x + rect.right,
                    ]
                    == 1
                )
                > 1
            ):
                self.rng(name, speed, x, y)
            else:
                return x, y

        elif self.ai_package[name]["movement_behavior"]["dirrection"] == 1:
            x += 1 * speed * self.dt
            if (
                np.count_nonzero(
                    collision_map[
                        relative__top : relative__top + rect.bottom,
                        relative__left + x : relative__left + x + rect.right,
                    ]
                    == 1
                )
                > 1
            ):
                self.rng(name, speed, x, y)
            else:
                return x, y

        elif self.ai_package[name]["movement_behavior"]["dirrection"] == 2:
            y += -1 * speed * self.dt
            print(y)
            if (
                np.count_nonzero(
                    collision_map[
                        relative__top + y : relative__top + y + rect.bottom,
                        relative__left : relative__left + rect.right,
                    ]
                    == 1
                )
                > 1
            ):
                self.rng(name, speed, x, y)
            else:
                return x, y

        elif self.ai_package[name]["movement_behavior"]["dirrection"] == 3:
            y += 1 * speed * self.dt
            if (
                np.count_nonzero(
                    collision_map[
                        relative__top + y : relative__top + y + rect.bottom,
                        relative__left : relative__left + rect.right,
                    ]
                    == 1
                )
                > 1
            ):
                self.rng(name, speed, x, y)
            else:
                return x, y

    def attack(self, name, dt, npc, player_possition):
        speed = self.ai_package[name]["movement_behavior"]["movement_speed"]
        distance = math.dist((npc), player_possition)
        
        if distance < self.ai_package[name]["detection_range"]:
            dx, dy = 0, 0
            if player_possition[0] > npc[0]:
                dx = npc[0] + speed * dt
            else:
                dx = npc[0] - speed * dt

            if player_possition[1] > npc[1]:
                dy = npc[1] + speed * dt
            else:
                dy = npc[1] - speed * dt

            return dx, dy

        else:
            return npc[0], npc[1]

    def rng(self, name, speed, x, y):
        rng = random.randint(0, 3)
        dx, dy = 0, 0

        if rng == 0:
            dx = -1
            self.ai_package[name]["movement_behavior"]["dirrection"] = rng
        elif rng == 1:
            dx = 1
            self.ai_package[name]["movement_behavior"]["dirrection"] = rng
        elif rng == 2:
            dy = -1
            self.ai_package[name]["movement_behavior"]["dirrection"] = rng
        elif rng == 3:
            dy = 1
            self.ai_package[name]["movement_behavior"]["dirrection"] = rng

        x += dx * speed * self.dt
        y += dy * speed * self.dt

        return x, y

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
            return self.npcs[name]["position"]

    def random_patrol(self, name, collision_map, relative__left, relative__top, rect):
        # Simulate random movement within a patrol area
        speed = self.ai_package[name]["movement_behavior"]["movement_speed"]
        
        if self.ai_package[name]["movement_behavior"]["dirrection"] == False:
            self.rng(name)
            return rect.centerx, rect.centery

        elif self.ai_package[name]["movement_behavior"]["dirrection"] == 0:
            dy = int(-speed * self.dt)
            if (
                np.count_nonzero(
                    collision_map[
                        relative__top + dy : relative__top + rect.height + dy,
                        relative__left : relative__left + rect.width,
                    ]
                    == 1
                )
                > 1
            ):
                self.rng(name)
            else:
                rect.centery += dy
                return rect.centerx, rect.centery

        elif self.ai_package[name]["movement_behavior"]["dirrection"] == 1:
            dx = int(speed * self.dt)
            if (
                np.count_nonzero(
                    collision_map[
                        relative__top : relative__top + rect.height,
                        relative__left + dx : relative__left + dx + rect.width,
                    ]
                    == 1
                )
                > 1
            ):
                self.rng(name)
            else:
                rect.centerx += dx
                return rect.centerx, rect.centery

        elif self.ai_package[name]["movement_behavior"]["dirrection"] == 2:
            dy = int(speed * self.dt)
            print(relative__top + dy)
            if (
                np.count_nonzero(
                    collision_map[
                        relative__top + dy : relative__top + rect.height + dy,
                        relative__left : relative__left + rect.width,
                    ]
                    == 1
                )
                > 1
            ):
                self.rng(name)
            else:
                rect.centery += dy
                return rect.centerx, rect.centery

        elif self.ai_package[name]["movement_behavior"]["dirrection"] == 3:
            dx = int(-speed * self.dt)
            if (
                np.count_nonzero(
                    collision_map[
                        relative__top : relative__top + rect.height,
                        relative__left + dx : relative__left + dx + rect.width,
                    ]
                    == 1
                )
                > 1
            ):
                self.rng(name)
            else:
                rect.centerx += dx
                return rect.centerx, rect.centery
            
        return rect.centerx, rect.centery
        

    def rng(self, name):
        rng = random.randint(0, 3)
        if rng == 0:
            self.ai_package[name]["movement_behavior"]["dirrection"] = rng

        elif rng == 1:
            self.ai_package[name]["movement_behavior"]["dirrection"] = rng

        elif rng == 2:
            self.ai_package[name]["movement_behavior"]["dirrection"] = rng

        elif rng == 3:
            self.ai_package[name]["movement_behavior"]["dirrection"] = rng

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

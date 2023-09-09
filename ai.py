import pygame
import random
import numpy as np
import math
from dialogue import Dialougue

class Ai:
    def __init__(self, npcs, assets, screen):
        self.npcs = npcs
        self.ai_package = assets.load_ai_package()
        self.dt = 0
        self.npc_movement = {}
        self.strings = Dialougue(assets, self.ai_package, screen)

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
            return (rect.centerx, rect.centery)

    def random_patrol(self, name, collision_map, relative__left, relative__top, rect):
        # Simulate random movement within a patrol area
        speed = self.ai_package[name]["movement_behavior"]["movement_speed"]

        if self.ai_package[name]["movement_behavior"]["dirrection"] == False:
            self.rng(name)
            return rect.centerx, rect.centery

        elif self.ai_package[name]["movement_behavior"]["dirrection"] == 1:
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

        elif self.ai_package[name]["movement_behavior"]["dirrection"] == 2:
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

        elif self.ai_package[name]["movement_behavior"]["dirrection"] == 3:
            dy = int(speed * self.dt)
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

        elif self.ai_package[name]["movement_behavior"]["dirrection"] == 4:
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
        rng = random.randint(1, 4)
        if rng == 1:
            self.ai_package[name]["movement_behavior"]["dirrection"] = rng

        elif rng == 2:
            self.ai_package[name]["movement_behavior"]["dirrection"] = rng

        elif rng == 3:
            self.ai_package[name]["movement_behavior"]["dirrection"] = rng

        elif rng == 4:
            self.ai_package[name]["movement_behavior"]["dirrection"] = rng

    def check_collision(self, collision_map, x, y, rect, move, name, dirrection):
        prev_center = rect.center
        rect.center = (x, y)

        if (
            np.count_nonzero(
                collision_map[
                    rect.top : rect.top + rect.height,
                    rect.left : rect.left + rect.width,
                ]
            )
            == 0
        ):
            return x, y

        self.ai_package[name]["movement_behavior"]["dirrection"] == dirrection
        rect.center = prev_center
        return self.random_patrol(name, collision_map, rect.left, rect.top, rect)

    def attack(self, name, dt, npc, player_possition, collision_map, rect):
        speed = self.ai_package[name]["movement_behavior"]["movement_speed"]
        distance = math.dist((npc), player_possition)

        if distance < self.ai_package[name]["detection_range"]:
            dx, dy = 0, 0
            move = 0
            direction = 0
            if player_possition[0] > npc[0]:
                move = int(speed * dt)
                dx = npc[0] + move
                direction = 4
            else:
                move = int(-speed * dt)
                dx = npc[0] + move
                direction = 2

            if player_possition[1] - 10 > npc[1]:
                move = int(speed * dt)
                dy = npc[1] + move
                direction = 1
            else:
                move = int(-speed * dt)
                dy = npc[1] + move
                direction = 3

            dx, dy = self.check_collision(
                collision_map, int(dx), int(dy), rect, move, name, direction
            )
            print(dy, dy)
            return dx, dy

        else:
            return npc[0], npc[1]
        
    def random_line(self, npc, player_possition, name):
        distance = math.dist((npc), player_possition)
        if distance < self.ai_package[name]["talk_range"] and not self.ai_package[name]["talking"] and self.dt*5 < pygame.time.get_ticks():
            self.strings.random_line(name)

import math
import random

import numpy as np
import pygame

from dialogue import Dialougue
from game_manager import ClassManager as CM
from game_manager import GameManager as GM


class Ai:
    def __init__(self):
        self.npc_movement = {}
        self.strings = Dialougue()

    def update(self, name, collision_map, relative__left, relative__top, rect):
        if GM.ai_package[name]["movement_behavior"]["type"] == "patrol":
            # Implement random movement within a patrol area
            return self.random_patrol(
                name, collision_map, relative__left, relative__top, rect
            )
        elif GM.ai_package[name]["movement_behavior"]["type"] == "stand":
            return (rect.centerx, rect.centery)

    def random_patrol(self, name, collision_map, relative__left, relative__top, rect):
        # Simulate random movement within a patrol area
        speed = GM.ai_package[name]["movement_behavior"]["movement_speed"]

        if GM.ai_package[name]["movement_behavior"]["dirrection"] == False:
            self.rng(name)
            return rect.centerx, rect.centery

        elif GM.ai_package[name]["movement_behavior"]["dirrection"] == 1:
            dy = int(-speed * GM.delta_time)
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

        elif GM.ai_package[name]["movement_behavior"]["dirrection"] == 2:
            dx = int(speed * GM.delta_time)
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

        elif GM.ai_package[name]["movement_behavior"]["dirrection"] == 3:
            dy = int(speed * GM.delta_time)
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

        elif GM.ai_package[name]["movement_behavior"]["dirrection"] == 4:
            dx = int(-speed * GM.delta_time)
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
            GM.ai_package[name]["movement_behavior"]["dirrection"] = rng

        elif rng == 2:
            GM.ai_package[name]["movement_behavior"]["dirrection"] = rng

        elif rng == 3:
            GM.ai_package[name]["movement_behavior"]["dirrection"] = rng

        elif rng == 4:
            GM.ai_package[name]["movement_behavior"]["dirrection"] = rng

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
            <= 30
        ):
            return x, y

        GM.ai_package[name]["movement_behavior"]["dirrection"] == dirrection
        rect.center = prev_center
        return self.random_patrol(name, collision_map, rect.left, rect.top, rect)

    def attack(self, name, npc, player_possition, collision_map, rect):
        speed = GM.ai_package[name]["movement_behavior"]["movement_speed"]
        distance = math.dist((npc), player_possition)

        if distance < GM.ai_package[name]["detection_range"]:
            dx, dy = 0, 0
            move = 0
            direction = 0
            if player_possition[0] > npc[0]:
                move = int(speed * GM.delta_time)
                dx = npc[0] + move
                direction = 4
            else:
                move = int(-speed * GM.delta_time)
                dx = npc[0] + move
                direction = 2

            if player_possition[1] - 10 > npc[1]:
                move = int(speed * GM.delta_time)
                dy = npc[1] + move
                direction = 1
            else:
                move = int(-speed * GM.delta_time)
                dy = npc[1] + move
                direction = 3

            dx, dy = self.check_collision(
                collision_map, int(dx), int(dy), rect, move, name, direction
            )
            return dx, dy, True

        else:
            return npc[0], npc[1], False

    def random_line(self, npc, player_possition, name):
        distance = math.dist((npc), player_possition)
        rng = random.randint(1, 100)
        if distance < GM.ai_package[name]["talk_range"] and rng == 5:
            return self.strings.random_line(name)
        
        return None

    def to_dict(self):
        return {
            "npc_movement": self.npc_movement,
            "strings": self.strings.to_dict()
        }

    def from_dict(self, data):
        self.npc_movement = data.get("npc_movement", {})
        self.strings=Dialougue()
        self.strings.from_dict(data.get("strings", {})) if data.get("strings") else None

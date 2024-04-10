import copy
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
            return rect.centerx, rect.centery, GM.ai_package[name]["movement_behavior"]["dirrection"]

    def random_patrol(self, name, collision_map, relative__left, relative__top, rect):
        # Simulate random movement within a patrol area
        speed = GM.ai_package[name]["movement_behavior"]["movement_speed"]

        if GM.ai_package[name]["movement_behavior"]["dirrection"] == False:
            self.rng(name)
            return rect.centerx, rect.centery, GM.ai_package[name]["movement_behavior"]["dirrection"]

        elif GM.ai_package[name]["movement_behavior"]["dirrection"] == 1:
            dy = int(-speed * GM.delta_time)
            if (
                np.count_nonzero(
                    collision_map[
                        relative__top + dy: relative__top + rect.height + dy,
                        relative__left: relative__left + rect.width,
                    ]
                    == 1
                )
                > 1
            ):
                self.rng(name)
            else:
                rect.centery += dy
                return rect.centerx, rect.centery, GM.ai_package[name]["movement_behavior"]["dirrection"]

        elif GM.ai_package[name]["movement_behavior"]["dirrection"] == 2:
            dx = int(speed * GM.delta_time)
            if (
                np.count_nonzero(
                    collision_map[
                        relative__top: relative__top + rect.height,
                        relative__left + dx: relative__left + dx + rect.width,
                    ]
                    == 1
                )
                > 1
            ):
                self.rng(name)
            else:
                rect.centerx += dx
                return rect.centerx, rect.centery, GM.ai_package[name]["movement_behavior"]["dirrection"]

        elif GM.ai_package[name]["movement_behavior"]["dirrection"] == 3:
            dy = int(speed * GM.delta_time)
            if (
                np.count_nonzero(
                    collision_map[
                        relative__top + dy: relative__top + rect.height + dy,
                        relative__left: relative__left + rect.width,
                    ]
                    == 1
                )
                > 1
            ):
                self.rng(name)
            else:
                rect.centery += dy
                return rect.centerx, rect.centery, GM.ai_package[name]["movement_behavior"]["dirrection"]

        elif GM.ai_package[name]["movement_behavior"]["dirrection"] == 4:
            dx = int(-speed * GM.delta_time)
            if (
                np.count_nonzero(
                    collision_map[
                        relative__top: relative__top + rect.height,
                        relative__left + dx: relative__left + dx + rect.width,
                    ]
                    == 1
                )
                > 1
            ):
                self.rng(name)
            else:
                rect.centerx += dx
                return rect.centerx, rect.centery, GM.ai_package[name]["movement_behavior"]["dirrection"]

        return rect.centerx, rect.centery, GM.ai_package[name]["movement_behavior"]["dirrection"]

    def rng(self, name):
        GM.ai_package[name]["movement_behavior"]["dirrection"] = random.randint(
            1, 4)

    def check_collision(self, collision_map, x, y, rect):
        prev_center = rect.center
        rect.center = (x, y)

        collision_area = collision_map[rect.top: rect.top +
                                       rect.height, rect.left: rect.left + rect.width]
        if np.count_nonzero(collision_area) <= 30:
            return x, y

        rect.center = prev_center
        return rect.center

    def attack(self, name, npc, player_possition, collision_map, rect):
        # CM.script_loader.run_script(script["script_name"], script["function"], script["args"])
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
                collision_map, int(dx), int(dy), rect
            )
            GM.ai_package[name]["movement_behavior"]["dirrection"] = direction
            return dx, dy, True, direction

        else:
            return npc[0], npc[1], False, GM.ai_package[name]["movement_behavior"]["dirrection"]

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
        self.strings = Dialougue()
        self.strings.from_dict(data.get("strings", {})
                               ) if data.get("strings") else None

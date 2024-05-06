import copy
import math
import random

import numpy as np

import asset_loader as assets
from dialogue import Dialougue
from game_manager import ClassManager as CM
from game_manager import GameManager as GM
from pathfinder import PathFinder


class Ai:
    def __init__(self):
        self.strings = Dialougue()
        self.pathfiner = PathFinder()

    def update(self, npc):
        if GM.ai_package[npc["name"]["name"]]["movement_behavior"]["type"] == "patrol":
            return self.random_patrol(npc)

        elif GM.ai_package[npc["name"]["name"]]["movement_behavior"]["type"] == "stand" or "Idle" in GM.ai_package[npc["name"]["name"]]["movement_behavior"]["type"]:
            return npc["rect"].centerx, npc["rect"].centery, GM.ai_package[npc["name"]["name"]]["movement_behavior"]["dirrection"]

        elif GM.ai_package[npc["name"]["name"]]["movement_behavior"]["type"] == "move":
            return self.pathfinder_move(npc)

    def random_patrol(self, npc):
        name = npc["name"]["name"]
        rect = npc["rect"]
        speed = GM.ai_package[name]["movement_behavior"]["movement_speed"]
        direction = GM.ai_package[name]["movement_behavior"]["dirrection"]

        if direction == 1:
            dy = int(-speed * GM.delta_time)
            if self.check_collision(rect.left, rect.top + dy, rect):
                self.rng(name)
            else:
                rect.centery += dy

        elif direction == 2:
            dx = int(speed * GM.delta_time)
            if self.check_collision(rect.left + dx, rect.top, rect):
                self.rng(name)
            else:
                rect.centerx += dx

        elif direction == 3:
            dy = int(speed * GM.delta_time)
            if self.check_collision(rect.left, rect.top + dy, rect):
                self.rng(name)
            else:
                rect.centery += dy

        elif direction == 4:
            dx = int(-speed * GM.delta_time)
            if self.check_collision(rect.left + dx, rect.top, rect):
                self.rng(name)
            else:
                rect.centerx += dx

        return rect.centerx, rect.centery, direction

    def pathfinder_move(self, npc):
        path = npc["path"]
        if path:
            next_point = path.pop(0)
            return next_point[0], next_point[1], None
        else:
            return npc["rect"].centerx, npc["rect"].centery, None

    def rng(self, name):
        GM.ai_package[name]["movement_behavior"]["dirrection"] = random.randint(1, 4)

    def check_collision(self, x, y, rect):
        prev_center = rect.center
        rect.center = (x, y)

        collision_area = GM.collision_map[rect.top: rect.top + rect.height, rect.left: rect.left + rect.width]
        if np.count_nonzero(collision_area) <= 30:
            return True

        rect.center = prev_center
        return False

    def attack(self, name, npc, player_position, rect):
        speed = GM.ai_package[name]["movement_behavior"]["movement_speed"]
        distance = math.dist(npc, player_position)

        if distance < GM.ai_package[name]["detection_range"]:
            dx, dy = 0, 0
            move = 0
            direction = 0

            if player_position[0] > npc[0]:
                move = int(speed * GM.delta_time)
                dx = npc[0] + move
                direction = 4
            else:
                move = int(-speed * GM.delta_time)
                dx = npc[0] + move
                direction = 2

            if player_position[1] - 10 > npc[1]:
                move = int(speed * GM.delta_time)
                dy = npc[1] + move
                direction = 1
            else:
                move = int(-speed * GM.delta_time)
                dy = npc[1] + move
                direction = 3

            if self.check_collision(dx, dy, rect):
                direction = 0

            return dx, dy, True, direction
        else:
            return npc[0], npc[1], False, GM.ai_package[name]["movement_behavior"]["dirrection"]

    def random_line(self, npc, player_position, name):
        distance = math.dist(npc, player_position)
        rng = random.randint(1, 100)
        if distance < GM.ai_package[name]["talk_range"] and rng == 5:
            return self.strings.random_line(name)
        return None

    def find_path(self, start_point, end_point):
        path, _ = self.pathfinder.find_path(start_point, end_point)
        return path

    def set_action(self, npc):
        week_day = GM.game_date.current_date.weekday()
        hour = f"{GM.game_date.current_date.hour}.{GM.game_date.current_date.minute:02d}"
        routine = assets.get_actions(week_day, hour, copy.deepcopy(npc["name"]["routine"]))
        if len(npc["name"]["current_routine"]) == 0 or npc["name"]["current_routine"][-1] != routine[-1]:
            npc["name"]["current_routine"] = copy.deepcopy(routine)
            npc["name"]["path"] = self.pathfiner.get_path(npc["name"]["stats"]["group"], npc["rect"].center, routine[2])

    def to_dict(self):
        return {
            "strings": self.strings.to_dict()
        }

    def from_dict(self, data):
        self.strings = Dialougue()
        self.strings.from_dict(data.get("strings", {})) if data.get("strings") else None

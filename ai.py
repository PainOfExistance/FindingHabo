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
        self.pathfinder = PathFinder()
        self.movement_vectors = {
        0: (0, -1),
        1: (0, -1),
        2: (-1, 0),
        3: (1, 0),
        4: (0, 1),
        }

    def update(self, npc):
        if npc["name"]["movement_behavior"]["type"] == "patrol":
            return self.random_patrol(npc)

        elif "stand" in npc["name"]["movement_behavior"]["type"] or "Idle" in npc["name"]["movement_behavior"]["type"]:
            return npc

        elif npc["name"]["movement_behavior"]["type"] == "move":
            return self.pathfinder.move(npc)

    def attack(self, npc):
        if math.dist(npc["rect"].center, GM.player_relative_center) < npc["name"]["detection_range"]:
            npc["agroved"]=True
            return self.pathfinder.move(npc, GM.player_relative_center)
        npc["agroved"]=False
        return npc

    def random_patrol(self, npc):
        rect = copy.deepcopy(npc["rect"])
        direction=npc["name"]["movement_behavior"]["dirrection"]
        movement_vector = self.movement_vectors.get(direction, (0, 0))

        target_x = rect.centerx + movement_vector[0]
        target_y = rect.centery + movement_vector[1]
        tmp = self.pathfinder.move(npc, (target_x, target_y))

        if tmp["rect"].center == rect.center:
            direction = self.rng()
            npc["name"]["movement_behavior"]["dirrection"] = direction

        return tmp

    def rng(self):
        return random.randint(1, 4)

    def random_line(self, npc, player_position, name):
        try:
            distance = math.dist(npc, player_position)
            rng = random.randint(1, 100)
            if distance < GM.ai_package[name]["talk_range"] and rng == 5:
                return self.strings.random_line(name)
            return None
        except:
            return None

    def to_dict(self):
        return {
            "strings": self.strings.to_dict()
        }

    def from_dict(self, data):
        self.strings = Dialougue()
        self.strings.from_dict(data.get("strings", {})) if data.get("strings") else None

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
        if npc["name"]["movement_behavior"]["type"] == "random_patrol":
            return self.random_patrol(npc)
        elif npc["name"]["target"]!=None:
            return self.pathfinder.move(npc, npc["name"]["target"])
        else:
            return npc
        
    def attack(self, npc):
        if math.dist(npc["rect"].center, GM.player_relative_center) < npc["name"]["detection_range"]:
            npc["agroved"]=True
            return self.pathfinder.move(npc, GM.player_relative_center)
        npc["agroved"]=False
        return npc

    def follow(self, npc):
        pass
    
    def update_state(self, npc):
        day=GM.game_date.current_date.weekday()
        time=f"{GM.game_date.current_date.hour}:{GM.game_date.current_date.minute:02d}"
        actions=assets.get_actions(day, time, npc["name"]["routine"])
        if len(npc["name"]["current_routine"])==0 or npc["name"]["current_routine"][-1]!=actions[-1]:
            npc["name"]["current_routine"]=copy.deepcopy(actions)
            npc=self.__get_state_action(npc)
            #npc["name"]["current_routine"].pop(0)
            #npc["name"]["movement_behavior"]["type"]=copy.deepcopy(actions[0])
            
    def __get_state_action(self, npc):
        routine=npc["name"]["current_routine"]
        if "move" in routine[0]:
            if "||" in routine[0]:
                split_by_=routine[0].split("_")
                split_by_vertical=split_by_[-1].split("||")
                npc["name"]["movement_behavior"]["type"]="".join(split_by_[:-1])
                target=random.choice(split_by_vertical)
                index=self.pathfinder.find_nav_points(target, npc)
                npc["name"]["routine"]=copy.deepcopy(GM.nav_tiles["index"])
                npc["name"]["target"]=copy.deepcopy(GM.nav_tiles["index"][0])
                #fix this line
                


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

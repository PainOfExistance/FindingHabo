import copy
import math
import random
import sys
from tkinter import N

import numpy as np
import pygame

import asset_loader as assets
from dialogue import Dialougue
from game_manager import ClassManager as CM
from game_manager import GameManager as GM
from pathfinder import PathFinder


class Ai:
    def __init__(self):
        self.strings = Dialougue()
        self.pathfinder = None
        self.movement_vectors = {
        0: (0, -1),
        1: (0, -1),
        2: (-1, 0),
        3: (1, 0),
        4: (0, 1),
        }

    def update(self, npc):
        #if npc["name"]["stats"]["group"]=="Merchant":
        #    print()
        #    print()
        #    print(npc["name"]["target"])
        #    print(npc["rect"])
        #    print()
        #    print()

        if npc["name"]["movement_behavior"]["type"] == "random_patrol":
            return self.random_patrol(npc)
        elif npc["name"]["target"]!=None:
            if(math.dist(npc["rect"]["center"], npc["name"]["target"])<10):
                if len(npc["name"]["path"])>0:
                    npc["name"]["target"]=copy.deepcopy(npc["name"]["path"][0])
                    npc["name"]["path"].pop(0)
                else:
                    npc["name"]["target"]=None
                    npc=self.update_state(npc)
                    return npc
            return self.pathfinder.move(npc, npc["name"]["target"])
        else:
            return self.update_state(npc)
        
    def attack(self, npc):
        if math.dist(npc["rect"]["center"], GM.player_relative_center) < npc["name"]["detection_range"]:
            npc["agroved"]=True
            return self.pathfinder.move(npc, GM.player_relative_center)
        npc["agroved"]=False
        return npc

    def follow(self, npc):
        #todo
        pass
    
    def update_state(self, npc):
        day=GM.game_date.current_date.weekday()
        time=f"{GM.game_date.current_date.hour}.{GM.game_date.current_date.minute:02d}"
        actions, npc["name"]["world"], npc["name"]["portal"]=assets.get_actions(day, time, npc["name"]["routine"])
            
        if len(npc["name"]["current_routine"])==0 or npc["name"]["current_routine"][-1]!=actions[-1]:
            npc["name"]["to_face"]=0
            npc["name"]["current_routine"]=copy.deepcopy(actions)
            npc=self.__get_state_action(npc)
        
        elif len(npc["name"]["current_routine"])==1 and npc["name"]["to_face"]!=0 and len(npc["name"]["path"])==0:
            npc["name"]["movement_behavior"]["dirrection"]=copy.deepcopy(npc["name"]["to_face"])
            npc["name"]["to_face"]=0      
            
        elif npc["name"]["target"]==None and not len(npc["name"]["current_routine"])==1:
            npc["name"]["to_face"]=0
            npc["name"]["current_routine"].pop(0)
            npc=self.__get_state_action(npc)
            
        if npc["name"]["stats"]["group"]=="Merchant":
            print()
            print()
            print(npc["name"]["target"])
            print(npc["rect"])
            print(npc["name"]["current_routine"])
            print(npc["name"]["to_face"])
            print(npc["name"]["path"])
            print()
            print()
            
        return npc
            
    def __get_state_action(self, npc):
        routine=npc["name"]["current_routine"]
        world=npc["name"]["world"]
        if "move" in routine[0]:
            split_by_=routine[0].split("_")
            npc["name"]["movement_behavior"]["type"]="".join(split_by_[:-1])
            if "||" in routine[0]:
                split_by_vertical=split_by_[-1].split("||")
                target=random.choice(split_by_vertical)
            else:
                target=split_by_[-1]
            
            if "||" in world:
                world=world.split("||")
                if CM.player.current_world==world[0]:
                    npc["name"]["portal_to_be"]=""
                    world=world[0]
                else:
                    npc["name"]["portal_to_be"]=world[0]
                    world=world[1]
                    
            npc["name"]["world"]=world
            
            index1, index2, column_index=self.pathfinder.find_global_nav_points(target, npc)
            if index1==None:
                return npc
            
            if index1>index2:
                index1, index2=index2, index1
                
            npc["name"]["path"]=copy.deepcopy([x[1] for x in GM.global_nav_tiles[world][column_index][index1:index2+1]])
            npc["name"]["target"]=copy.deepcopy(npc["name"]["path"][0])
            npc["name"]["path"].pop(0)
            npc["name"]["index_points"]=[i for i in range(index1, index2+1)]
            npc["name"]["column_index"]=column_index
            
        else:
            target=routine[0]
            if "||" in routine[0]:
                split_by_vertical=routine[0].split("||")
                target=random.choice(split_by_vertical)
            target=target.split("_")
            
            if "||" in world:
                world=world.split("||")
                if CM.player.current_world==world[0]:
                    npc["name"]["portal_to_be"]=world[1]
                    world=world[0]
                else:
                    npc["name"]["portal_to_be"]=world[0]
                    world=world[1]
                    
            npc["name"]["world"]=world
            
            index1, index2, column_index=self.pathfinder.find_global_nav_points(target[0], npc)
            if index1==None:
                return npc
            #npc["name"]["path"]=self.pathfinder.find_path(npc["rect"]["center"], GM.nav_tiles[column_index][index1]["rect"]["center"], (npc["rect"].width, npc["rect"].height))
            #todo speed test
            
            npc["name"]["path"]=copy.deepcopy([x[1] for x in GM.global_nav_tiles[world][column_index][index1:index2+1]])
            npc["name"]["target"]=copy.deepcopy(npc["name"]["path"][0])
            npc["name"]["path"].pop(0)
            npc["name"]["index_points"]=[i for i in range(index1, index2+1)]
            npc["name"]["column_index"]=column_index
            npc["name"]["to_face"]=target[1]

        return npc
                
    def random_patrol(self, npc):
        rect = copy.deepcopy(npc["rect"])
        direction=npc["name"]["movement_behavior"]["dirrection"]
        movement_vector = self.movement_vectors.get(direction, (0, 0))

        target_x = rect["centerx"] + movement_vector[0]
        target_y = rect["centery"] + movement_vector[1]
        tmp = self.pathfinder.move(npc, (target_x, target_y))

        if tmp["rect"]["center"] == rect["center"]:
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

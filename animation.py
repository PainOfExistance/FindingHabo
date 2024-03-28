import copy

import pygame

import asset_loader as assets
from colors import Colors
from game_manager import ClassManager as CM
from game_manager import GameManager as GM


class Animation:
    def __init__(self):
        self.action_images = assets.load_player_sprites()
        self.anim_counter=1
        self.prev_frame=0
        self.attacking=False
        self.enemy_anims={}
        self.prev_action="player_idle_up"
        self.in_attack=False
        self.data=assets.load_animations()
        
    def load_anims(self, data):
        self.enemy_anims[f"{data["name"]["name"].lower()}"]={"anim_counter": 0, "prev_action": f""}
    
    def init_player(self):
        return self.action_images["player_walk_up"]["image"][0]
    
    def to_dict(self):
        return {
            "anim_counter": self.anim_counter,
            "prev_frame": self.prev_frame,
            "attacking": self.attacking,
            "in_attack": self.in_attack,
            "prev_action": self.prev_action,
            "anim_counter": self.anim_counter,
            "enemy_anims": self.enemy_anims
        }
    
    def from_dict(self, data):
        self.anim_counter = data["anim_counter"]
        self.prev_frame = data["prev_frame"]
        self.attacking = data["attacking"]
        self.in_attack = data["in_attack"]
        self.prev_action = data["prev_action"]
        self.anim_counter = data["anim_counter"]
        self.enemy_anims = data["enemy_anims"]
    
    def animate_npc(self, data):
        if data["name"]["movement_behavior"]["moving"]:
            action="move"
        else:
            action="idle"
        if data["agroved"]:
            action="attack"
        match data["name"]["movement_behavior"]["dirrection"]:
            case 1:
                dirrection="up"
                
            case 4:
                dirrection="left"

            case 3:
                dirrection="down"

            case 2:
                dirrection="right"
                
            case _:
                dirrection="up"
                
        if self.enemy_anims[f"{data["name"]["name"].lower()}"]["prev_action"]!=f"{data["name"]["name"].lower()}_{action}_{dirrection}":
            self.enemy_anims[f"{data["name"]["name"].lower()}"]["anim_counter"]=0
            self.enemy_anims[f"{data["name"]["name"].lower()}"]["prev_action"]=f"{data["name"]["name"].lower()}_{action}_{dirrection}"
        
        self.enemy_anims[f"{data["name"]["name"].lower()}"]["anim_counter"] += GM.delta_time*(data["image"][f"{data["name"]["name"].lower()}_{action}_{dirrection}"]["fps"]/1.5)
        if int(self.enemy_anims[f"{data["name"]["name"].lower()}"]["anim_counter"])>=len(data["image"][f"{data["name"]["name"].lower()}_{action}_{dirrection}"]["frames"]):
            self.enemy_anims[f"{data["name"]["name"].lower()}"]["anim_counter"]=0
        
        tmp=int(self.enemy_anims[f"{data["name"]["name"].lower()}"]["anim_counter"])
        
        return data["image"][f"{data["name"]["name"].lower()}_{action}_{dirrection}"]["frames"][tmp], data["image"][f"{data["name"]["name"].lower()}_{action}_{dirrection}"]["rects"][tmp]
    #https://fixupx.com/francenews24/status/1768349762946838655/en
    
    def player_anim(self, weapon_equiped, speed=200):
        if GM.moving:
            action="walk"
        else:
            action="idle"
        if GM.attacking or self.in_attack:
            self.in_attack=True
            action="attack"
        
        match GM.rotation_angle:
            case 0:
                dirrection="up"
                
            case 90:
                dirrection="left"

            case 180:
                dirrection="down"

            case 270:
                dirrection="right"
                
            case _:
                dirrection="up"
        
        if self.prev_action!=f"player_{action}_{dirrection}":
            self.anim_counter=0
            self.prev_action=f"player_{action}_{dirrection}"
            
        neke=self.action_images[f"player_{action}_{dirrection}"]
        self.anim_counter += GM.delta_time*(neke["fps"]/1.5)

        if int(self.anim_counter)>=len(neke["image"]):
            self.anim_counter=0
            if action=="attack":
                self.in_attack=False
        
        return self.action_images[f"player_{action}_{dirrection}"]["image"][int(self.anim_counter)], self.action_images[f"player_{action}_{dirrection}"]["rect"][int(self.anim_counter)]

    def animate_static(self, coordinates):
        rect=pygame.Rect(0, 0, 8, 8)
        for x in coordinates:
            self.data[x["value"]] += GM.delta_time*(self.data[x["value"]]["fps"]/1.5)
            if int(self.data[x["value"]]["counter"])>=len(self.data[x["value"]]["frames"]):
                self.data[x["value"]]["counter"]=0
            
            tmp=int(self.data[x["value"]]["counter"])
            
            rect.x=x["x"]
            rect.y=x["y"]
            GM.screen.blit(self.data[x["value"]]["frames"][tmp], rect.topleft)
import copy
from re import X

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
    
    def animate_npc(self, data, index, agrov):
        name=data["name"]["name"].lower()
        if data["name"]["movement_behavior"]["moving"]:
            action="move"
        else:
            action="idle"
        if agrov:
            action="attack"
            
        match data["name"]["movement_behavior"]["dirrection"]:
            case 1:
                dirrection="up"
                
            case 2:
                dirrection="right"

            case 3:
                dirrection="down"
            
            case 4:
                dirrection="left"
                
        if GM.npc_list[index]["name"]["movement_behavior"]["prev_action"]!=f"{name}_{action}_{dirrection}":
            GM.npc_list[index]["name"]["movement_behavior"]["counter"]=0
            GM.npc_list[index]["name"]["movement_behavior"]["prev_action"]=f"{name}_{action}_{dirrection}"
        
        tmp=int(GM.npc_list[index]["name"]["movement_behavior"]["counter"])
        if (not CM.menu.visible and not CM.player_menu.visible):
            GM.npc_list[index]["name"]["movement_behavior"]["counter"]+= GM.delta_time*(self.enemy_anims[name]["images"][f"{name}_{action}_{dirrection}"]["fps"]/1.5)
            tmp=int(GM.npc_list[index]["name"]["movement_behavior"]["counter"])
            if tmp>=len(self.enemy_anims[name]["images"][f"{name}_{action}_{dirrection}"]["frames"]):
                GM.npc_list[index]["name"]["movement_behavior"]["counter"], tmp = 0, 0
        
        return self.enemy_anims[name]["images"][f"{name}_{action}_{dirrection}"]["frames"][tmp], self.enemy_anims[name]["images"][f"{name}_{action}_{dirrection}"]["rects"][tmp]
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

    def animate_static(self):
        removing=[]
        for i, x in enumerate(GM.anim_tiles):
            relative_left = int(GM.bg_rect.left + x["col"])
            relative_top = int(GM.bg_rect.top + x["row"])
            if (
            relative_left > -80
            and relative_left < GM.screen_width + 80
            and relative_top > -80
            and relative_top < GM.screen_height + 80
            and "special" not in x
            ):   
                value_data = self.data[x["value"]]
                x["counter"] += GM.delta_time * (value_data["fps"] / 1.5)
                
                tmp = int(x["counter"])
                if tmp >= len(value_data["frames"]):
                    x["counter"] = 0
                    tmp = 0
                    
                GM.screen.blit(value_data["frames"][tmp], (relative_left, relative_top))
                
            elif "special" in x:
                value_data = self.data[x["value"]]
                if "hold" in x["special"]:
                    tmp = int(x["counter"])
                    if tmp >= len(value_data["frames"])-1:
                        x["counter"]=len(value_data["frames"])-1
                        tmp=len(value_data["frames"])-1
                    else:
                        x["counter"] += GM.delta_time * (value_data["fps"] / 1.5)
                    GM.screen.blit(value_data["frames"][tmp], (relative_left, relative_top))
                
                elif "once" in x["special"]:
                    x["counter"] += GM.delta_time * (value_data["fps"] / 1.5)
                    tmp = int(x["counter"])
                    if tmp >= len(value_data["frames"]):
                        removing.append(i)
                        continue
                    GM.screen.blit(value_data["frames"][tmp], (relative_left, relative_top))
        
        for i in removing:
            GM.anim_tiles.pop(i)
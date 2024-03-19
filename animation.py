import pygame

import asset_loader as assets
from game_manager import ClassManager as CM
from game_manager import GameManager as GM


class Animation:
    def __init__(self):
        self.action_images = assets.load_player_sprites()
        self.anim_counter=1
        self.prev_frame=0
        self.attacking=False
        self.enemy_anims={}
    
    def load_anims(self, paths, data):
        self.enemy_anims.clear()
        for path in paths:
            images, rects, fps = assets.load_enemy_sprites(path)
            self.enemy_anims[f"{data["name"]["name"]}_{data["name"]["movement_behavior"]["dirrection"]}_{data["name"]["movement_behavior"]["moving"]}"]={"npc": f"{data["name"]["name"]}_{data["name"]["movement_behavior"]["dirrection"]}_{data["name"]["movement_behavior"]["moving"]}","images": images, "rects": rects, "anim_counter": 0, "fps": fps}
    
    def init_player(self):
        return self.action_images["player_walk_up"]["image"][0], self.action_images["player_walk_up"]["rect"][0]
    
    def to_dict(self):
        return {
            "anim_counter": self.anim_counter,
            "prev_frame": self.prev_frame,
            "attacking": self.attacking
        }
    
    def from_dict(self, data):
        self.anim_counter = data["anim_counter"]
        self.prev_frame = data["prev_frame"]
        self.attacking = data["attacking"]
    
    def animate_npc(self, data):
        neke=self.enemy_anims[f"{data["name"]["name"]}_{data["name"]["movement_behavior"]["dirrection"]}_{data["name"]["movement_behavior"]["moving"]}"]
        frame_index = int(neke["anim_counter"] * neke["fps"] / 60) % len(neke["images"])
        neke["anim_counter"]+=1
        if neke["anim_counter"]>len(neke["images"]):
            neke["anim_counter"]=0
        return neke["images"][frame_index], neke["rects"][frame_index]
    #https://fixupx.com/francenews24/status/1768349762946838655/en
    
    def player_anim(self, weapon_equiped, speed=200):
        if GM.moving:
            action="walk"
        if GM.attacking:
            action="attack"
        else:
            action="idle"
        
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
                
        neke=self.action_images[f"player_{action}_{dirrection}"]
        frame_index = int((self.anim_counter * (neke["fps"] / 60)) * speed) % len(neke["image"])

        #todo fix
        
        self.anim_counter+=1
        if self.anim_counter>len(neke["image"]):
            self.anim_counter=0
        return self.action_images[f"player_{action}_{dirrection}"]["image"][frame_index], self.action_images[f"player_{action}_{dirrection}"]["rect"][frame_index]
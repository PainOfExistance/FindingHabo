import pygame

import asset_loader as assets
from game_manager import ClassManager as CM
from game_manager import GameManager as GM


class Animation:
    def __init__(self):
        images = assets.load_player_sprites()
        self.action_images = self.slice_image(images)
        self.anim_counter=1
        self.prev_frame=0
        self.attacking=False

    def slice_image(self, images):
        frames = {}
        for key in images.keys():
            img = pygame.transform.scale(images[key], (images[key].get_width()*2,images[key].get_height()*3))
            rect=img.get_rect()
            frames[key] = {"image": img, "rect": rect}
        return frames
    
    def init_player(self):
        return self.action_images["Player_Walk_Up_1"]["image"], self.action_images["Player_Walk_Up_1"]["rect"]
    
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
    
    def player_anim(self, weapon_equiped, speed=200):
        #print(self.prev_frame)
        move=(speed*GM.delta_time)/28
        anim_speed=(speed*GM.delta_time)/100
        
        if GM.attacking:
            self.attacking=True
            
        if GM.rotation_angle == 0:
            if not GM.moving and not self.attacking:
                if weapon_equiped==None:
                    return self.action_images["Player_Walk_Up_1"]["image"], self.action_images["Player_Walk_Up_1"]["rect"]
                else:
                    return self.action_images["Player_Walk_Up_Weapon_1"]["image"], self.action_images["Player_Walk_Up_1"]["rect"]
            
            elif self.attacking:
                if self.prev_frame>anim_speed:
                    self.anim_counter+=1
                    self.prev_frame=0
                    if self.anim_counter==5:
                        self.anim_counter=1
                        self.attacking=False
                        if weapon_equiped==None:
                            return self.action_images["Player_Walk_Up_1"]["image"], self.action_images["Player_Walk_Up_1"]["rect"]
                        else:
                            return self.action_images["Player_Walk_Up_Weapon_1"]["image"], self.action_images["Player_Walk_Up_1"]["rect"]
                else:
                    self.prev_frame+=GM.delta_time
                if weapon_equiped==None:
                    return self.action_images["Player_Attack_Up_"+str(self.anim_counter)]["image"], self.action_images["Player_Attack_Up_"+str(self.anim_counter)]["rect"]
                else:
                    return self.action_images["Player_Attack_Up_"+str(self.anim_counter)]["image"], self.action_images["Player_Attack_Up_"+str(self.anim_counter)]["rect"]
            
            elif GM.moving:
                if self.prev_frame>move:
                    self.anim_counter+=1
                    self.prev_frame=0
                    if self.anim_counter==5:
                        self.anim_counter=1
                else:
                    self.prev_frame+=GM.delta_time
                if weapon_equiped==None:
                    return self.action_images["Player_Walk_Up_"+str(self.anim_counter)]["image"], self.action_images["Player_Walk_Up_"+str(self.anim_counter)]["rect"]
                else:
                    return self.action_images["Player_Walk_Up_Weapon_"+str(self.anim_counter)]["image"], self.action_images["Player_Walk_Up_Weapon_"+str(self.anim_counter)]["rect"]
                
        elif GM.rotation_angle == 90:
            if not GM.moving and not self.attacking:
                if weapon_equiped==None:
                    return self.action_images["Player_Walk_Left_1"]["image"], self.action_images["Player_Walk_Left_1"]["rect"]
                else:
                    return self.action_images["Player_Walk_Left_Weapon_1"]["image"], self.action_images["Player_Walk_Left_1"]["rect"]
            
            elif self.attacking:
                if self.prev_frame>anim_speed:
                    self.anim_counter+=1
                    self.prev_frame=0
                    if self.anim_counter==5:
                        self.anim_counter=1
                        self.attacking=False
                        if weapon_equiped==None:
                            return self.action_images["Player_Walk_Left_1"]["image"], self.action_images["Player_Walk_Left_1"]["rect"]
                        else:
                            return self.action_images["Player_Walk_Left_Weapon_1"]["image"], self.action_images["Player_Walk_Left_1"]["rect"]
                else:
                    self.prev_frame+=GM.delta_time
                if weapon_equiped==None:
                    return self.action_images["Player_Attack_Left_"+str(self.anim_counter)]["image"], self.action_images["Player_Attack_Left_"+str(self.anim_counter)]["rect"]
                else:
                    return self.action_images["Player_Attack_Left_"+str(self.anim_counter)]["image"], self.action_images["Player_Attack_Left_"+str(self.anim_counter)]["rect"]
            
            elif GM.moving:
                if self.prev_frame>move:
                    self.anim_counter+=1
                    self.prev_frame=0
                    if self.anim_counter==5:
                        self.anim_counter=1
                else:
                    self.prev_frame+=GM.delta_time
                if weapon_equiped==None:
                    return self.action_images["Player_Walk_Left_"+str(self.anim_counter)]["image"], self.action_images["Player_Walk_Left_"+str(self.anim_counter)]["rect"]
                else:
                    return self.action_images["Player_Walk_Left_Weapon_"+str(self.anim_counter)]["image"], self.action_images["Player_Walk_Left_Weapon_"+str(self.anim_counter)]["rect"]
                
        elif GM.rotation_angle == 180:
            if not GM.moving and not self.attacking:
                if weapon_equiped==None:
                    return self.action_images["Player_Walk_Down_1"]["image"], self.action_images["Player_Walk_Down_1"]["rect"]
                else:
                    return self.action_images["Player_Walk_Down_Weapon_1"]["image"], self.action_images["Player_Walk_Down_1"]["rect"]
            
            elif self.attacking:
                if self.prev_frame>anim_speed:
                    self.anim_counter+=1
                    self.prev_frame=0
                    if self.anim_counter==5:
                        self.anim_counter=1
                        self.attacking=False
                        if weapon_equiped==None:
                            return self.action_images["Player_Walk_Down_1"]["image"], self.action_images["Player_Walk_Down_1"]["rect"]
                        else:
                            return self.action_images["Player_Walk_Down_Weapon_1"]["image"], self.action_images["Player_Walk_Down_1"]["rect"]
                else:
                    self.prev_frame+=GM.delta_time
                if weapon_equiped==None:
                    return self.action_images["Player_Attack_Down_"+str(self.anim_counter)]["image"], self.action_images["Player_Attack_Down_"+str(self.anim_counter)]["rect"]
                else:
                    return self.action_images["Player_Attack_Down_"+str(self.anim_counter)]["image"], self.action_images["Player_Attack_Down_"+str(self.anim_counter)]["rect"]
            
            elif GM.moving:
                if self.prev_frame>move:
                    self.anim_counter+=1
                    self.prev_frame=0
                    if self.anim_counter==5:
                        self.anim_counter=1
                else:
                    self.prev_frame+=GM.delta_time
                if weapon_equiped==None:
                    return self.action_images["Player_Walk_Down_"+str(self.anim_counter)]["image"], self.action_images["Player_Walk_Down_"+str(self.anim_counter)]["rect"]
                else:
                    return self.action_images["Player_Walk_Down_Weapon_"+str(self.anim_counter)]["image"], self.action_images["Player_Walk_Down_Weapon_"+str(self.anim_counter)]["rect"]
                
        elif GM.rotation_angle == 270:
            if not GM.moving and not self.attacking:
                if weapon_equiped==None:
                    return self.action_images["Player_Walk_Right_1"]["image"], self.action_images["Player_Walk_Right_1"]["rect"]
                else:
                    return self.action_images["Player_Walk_Right_Weapon_1"]["image"], self.action_images["Player_Walk_Right_1"]["rect"]
            
            elif self.attacking:
                if self.prev_frame>anim_speed:
                    self.anim_counter+=1
                    self.prev_frame=0
                    if self.anim_counter==5:
                        self.anim_counter=1
                        self.attacking=False
                        if weapon_equiped==None:
                            return self.action_images["Player_Walk_Right_1"]["image"], self.action_images["Player_Walk_Right_1"]["rect"]
                        else:
                            return self.action_images["Player_Walk_Right_Weapon_1"]["image"], self.action_images["Player_Walk_Right_1"]["rect"]
                else:
                    self.prev_frame+=GM.delta_time
                if weapon_equiped==None:
                    return self.action_images["Player_Attack_Right_"+str(self.anim_counter)]["image"], self.action_images["Player_Attack_Right_"+str(self.anim_counter)]["rect"]
                else:
                    return self.action_images["Player_Attack_Right_"+str(self.anim_counter)]["image"], self.action_images["Player_Attack_Right_"+str(self.anim_counter)]["rect"]
            
            elif GM.moving:
                if self.prev_frame>move:
                    self.anim_counter+=1
                    self.prev_frame=0
                    if self.anim_counter==5:
                        self.anim_counter=1
                else:
                    self.prev_frame+=GM.delta_time
                if weapon_equiped==None:
                    return self.action_images["Player_Walk_Right_"+str(self.anim_counter)]["image"], self.action_images["Player_Walk_Right_"+str(self.anim_counter)]["rect"]
                else:
                    return self.action_images["Player_Walk_Right_Weapon_"+str(self.anim_counter)]["image"], self.action_images["Player_Walk_Right_Weapon_"+str(self.anim_counter)]["rect"]
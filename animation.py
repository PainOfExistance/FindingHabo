import pygame


class Animation:
    def __init__(self, assets):
        images =assets.load_player_sprites()
        self.action_images = self.slice_image(images)
        self.anim_counter=1
        self.prev_frame=0

    def slice_image(self, images):
        frames = {}
        for key in images.keys():
            if "Attack" not in key:
                for i in range(4):
                    img=images[key].subsurface((i * 16, 0, 16, 16))
                    img = pygame.transform.scale(img, (img.get_width()*2,img.get_height()*3))
                    rect=img.get_rect()
                    frames[key+"_"+str(i+1)] = {"image": img, "rect": rect}
            else:
                img = pygame.transform.scale(images[key], (images[key].get_width()*2,images[key].get_height()*3))
                rect=img.get_rect()
                frames[key] = {"image": img, "rect": rect}
        return frames
    
    def init_player(self):
        return self.action_images["Player_Walk_Up_1"]["image"], self.action_images["Player_Walk_Up_1"]["rect"]
    
    def player_anim(self, delta_time, moving, attacking, rotation, weapon_equiped, speed=200):
        print(self.prev_frame)
        move=(speed*delta_time)/35
        if weapon_equiped==None:
            if rotation == 0 and not moving:
                return self.action_images["Player_Walk_Up_1"]["image"], self.action_images["Player_Walk_Up_1"]["rect"]
            elif rotation == 90 and not moving:
                return self.action_images["Player_Walk_Left_1"]["image"], self.action_images["Player_Walk_Left_1"]["rect"]
            elif rotation == 180 and not moving:
                return self.action_images["Player_Walk_Down_1"]["image"], self.action_images["Player_Walk_Down_1"]["rect"]
            elif rotation == 270 and not moving:
                return self.action_images["Player_Walk_Right_1"]["image"], self.action_images["Player_Walk_Right_1"]["rect"]
            
            elif rotation == 0 and moving:
                    if self.prev_frame>move:
                        self.anim_counter+=1
                        self.prev_frame=0
                        if self.anim_counter==5:
                            self.anim_counter=1
                    else:
                        self.prev_frame+=delta_time
                    return self.action_images["Player_Walk_Up_"+str(self.anim_counter)]["image"], self.action_images["Player_Walk_Up_"+str(self.anim_counter)]["rect"]
                    
            elif rotation == 90 and moving:
                    if self.prev_frame>move:
                        self.anim_counter+=1
                        self.prev_frame=0
                        if self.anim_counter==5:
                            self.anim_counter=1
                    else:
                        self.prev_frame+=delta_time
                    return self.action_images["Player_Walk_Left_"+str(self.anim_counter)]["image"], self.action_images["Player_Walk_Left_"+str(self.anim_counter)]["rect"]

            elif rotation == 180 and moving:
                    if self.prev_frame>move:
                        self.anim_counter+=1
                        self.prev_frame=0
                        if self.anim_counter==5:
                            self.anim_counter=1
                    else:
                        self.prev_frame+=delta_time
                    return self.action_images["Player_Walk_Down_"+str(self.anim_counter)]["image"], self.action_images["Player_Walk_Down_"+str(self.anim_counter)]["rect"]
                    
            elif rotation == 270 and moving:
                    if self.prev_frame>move:
                        self.anim_counter+=1
                        self.prev_frame=0
                        if self.anim_counter==5:
                            self.anim_counter=1
                    else:
                        self.prev_frame+=delta_time
                    return self.action_images["Player_Walk_Right_"+str(self.anim_counter)]["image"], self.action_images["Player_Walk_Right_"+str(self.anim_counter)]["rect"]
        
        else:
            if rotation == 0 and attacking:
                if self.prev_frame>move:
                    self.anim_counter+=1
                    self.prev_frame=0
                    if self.anim_counter==5:
                        self.anim_counter=1
                else:
                    self.prev_frame+=delta_time
                return self.action_images["Player_Attack_Up_"+str(self.anim_counter)]["image"], self.action_images["Player_Attack_Up_"+str(self.anim_counter)]["rect"]
            elif rotation == 0 and not attacking:
                return self.action_images["Player_Attack_Up_1"]["image"], self.action_images["Player_Attack_Up_1"]["rect"]
            
            elif rotation == 90 and attacking:
                if self.prev_frame>move:
                    self.anim_counter+=1
                    self.prev_frame=0
                    if self.anim_counter==5:
                        self.anim_counter=1
                else:
                    self.prev_frame+=delta_time
                return self.action_images["Player_Attack_Left_"+str(self.anim_counter)]["image"], self.action_images["Player_Attack_Left_"+str(self.anim_counter)]["rect"]
            elif rotation == 90 and not attacking:
                return self.action_images["Player_Attack_Left_1"]["image"], self.action_images["Player_Attack_Up_1"]["rect"]
            
            elif rotation == 180 and attacking:
                if self.prev_frame>move:
                    self.anim_counter+=1
                    self.prev_frame=0
                    if self.anim_counter==5:
                        self.anim_counter=1
                else:
                    self.prev_frame+=delta_time
                return self.action_images["Player_Attack_Down_"+str(self.anim_counter)]["image"], self.action_images["Player_Attack_Down_"+str(self.anim_counter)]["rect"]
            elif rotation == 180 and not attacking:
                return self.action_images["Player_Attack_Down_1"]["image"], self.action_images["Player_Attack_Up_1"]["rect"]
            
            elif rotation == 270 and attacking:
                if self.prev_frame>move:
                    self.anim_counter+=1
                    self.prev_frame=0
                    if self.anim_counter==5:
                        self.anim_counter=1
                else:
                    self.prev_frame+=delta_time
                return self.action_images["Player_Attack_Right_"+str(self.anim_counter)]["image"], self.action_images["Player_Attack_Right_"+str(self.anim_counter)]["rect"]
            elif rotation == 270 and not attacking:
                return self.action_images["Player_Attack_Right_1"]["image"], self.action_images["Player_Attack_Up_1"]["rect"]
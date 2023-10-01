import json

import cv2
import numpy as np
import pygame


class AssetLoader:
    def __init__(self, screen_width, screen_height):
        self.screen_width=screen_width
        self.screen_height=screen_height

    def load_images(self, path, size, center):
        # Load and return images as needed
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, size)
        img_rect = img.get_rect()
        img_rect.center = center
        return img, img_rect
    
    def load_player(self, path, center):
        # Load player image
        player = pygame.image.load(path)
        player = pygame.transform.scale(player, (32, 64))
        player_rect = player.get_rect()
        player_rect.center = center
        return player, player_rect
    
    def load_background(self, path):
        # Load bg image
        bg = pygame.image.load(path)
        bg_rect = bg.get_rect()
        return bg, bg_rect
    
    def load_collision(self, path):
        #collision_map = np.zeros((self.bg_rect.height, self.bg_rect.width), dtype=int)
        #collision_map[0, :] = 1
        #collision_map[-1, :] = 1
        #collision_map[:, 0] = 1
        #collision_map[:, -1] = 1
        #collision_map[200:300, 200:300] = 1
        #print(collision_map)
        #return collision_map
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        binary_image = 1 - (image // 255)
        print(binary_image)
        #np.savetxt('map.txt', binary_image, fmt='%d')
        return binary_image
    
    def load_items(self):
        item_list=np.array({})
        with open("game_data/items.json", "r") as items:
            item_list = json.load(items)
            item_list = {item["name"]: item for item in item_list["items"]}
        return item_list
    
    def load_traits(self):
        traits=np.array({})
        with open("game_data/traits.json", "r") as traits_file:
            traits_data = json.load(traits_file)
            traits = {trait["name"]: trait for trait in traits_data["traits"]}
        return traits
    
    def load_effects(self):
        effects=np.array({})
        with open("game_data/effects.json", "r") as effect_file:
            effects_data = json.load(effect_file)
            effects = {effect["stat"]: effect for effect in effects_data["effects"]}
        return effects
    
    def load_worlds(self):
        worlds=np.array({})
        with open("game_data/leveldata.json", "r") as world_file:
            world_data = json.load(world_file)
            worlds = {world["name"]: world for world in world_data["worlds"]}
        return worlds
    
    def load_ai_package(self):
        ai_package=np.array({})
        with open("game_data/ai.json", "r") as ai_file:
            ai_data = json.load(ai_file)
            ai_package = {ai["name"]: ai for ai in ai_data["npcs"]}
        return ai_package
    
    def load_dialogue(self):
        dialogue_lines=np.array({})
        with open("game_data/dialogue.json", "r") as dialogue_file:
            dialogue_data = json.load(dialogue_file)
            dialogue_lines = {dialogue["name"]: dialogue for dialogue in dialogue_data["dialoge"]}
        return dialogue_lines
    
    def load_quests(self):
        quests=np.array({})
        with open("game_data/quests.json", "r") as quest_file:
            quest_data = json.load(quest_file)
            quests = {quest["id"]: quest for quest in quest_data["quests"]}
        return quests
    
    #https://www.youtube.com/watch?v=vOn0z0IRVN8&list=PLI2unizewPmmLdFX9kTGPSnXJJCiasCw5&index=64&ab_channel=Nazareth-Topic
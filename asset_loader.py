import json
import os

import bson
import cv2
import numpy as np
import pygame

from game_manager import ClassManager as CM
from game_manager import GameManager as GM


class AssetLoader:
    def __init__(self):
        pass

    def load_images(self, path, size, center):
        # Load and return images as needed
        img = pygame.image.load(path)
        if size!=(0,0):
            img = pygame.transform.scale(img, size)
        img_rect = img.get_rect()
        img_rect.center = center
        return img, img_rect

    def load_player(self, path):
        # Load player image
        player = pygame.image.load(path)
        player = pygame.transform.scale(player, (32, 64))
        player_rect = player.get_rect()
        return player, player_rect

    def load_player_sprites(self):
        image_list = {}
        for filename in os.listdir("textures/npc/player"):
            if filename.endswith(".png"):
                path = os.path.join("textures/npc/player", filename)
                key = filename[:-4]
                image_list[key] = pygame.image.load(path)
        return image_list

    def load_background(self, path):
        # Load bg image
        bg = pygame.image.load(path)
        bg_rect = bg.get_rect()
        return bg, bg_rect
    
    def load_level_data(self, path="terrain/worlds/simplified/Dream_World/data.json"):
        level_data = np.array({})
        with open(path, "r") as ai_file:
            level_data = json.load(ai_file)
        return level_data

    def load_collision(self, path):
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (image.shape[0]*8, image.shape[1]*8), interpolation = cv2.INTER_AREA)
        binary_image = 1 - (image // 255)
        print(binary_image)
        # np.savetxt('map.txt', binary_image, fmt='%d')
        return binary_image

    def load_items(self):
        item_list = np.array({})
        with open("game_data/items.json", "r") as items:
            item_list = json.load(items)
            item_list = {item["name"]: item for item in item_list["items"]}
        return item_list

    def load_traits(self):
        traits = np.array({})
        with open("game_data/traits.json", "r") as traits_file:
            traits_data = json.load(traits_file)
            traits = {trait["name"]: trait for trait in traits_data["traits"]}
        return traits

    def load_effects(self):
        effects = np.array({})
        with open("game_data/effects.json", "r") as effect_file:
            effects_data = json.load(effect_file)
            effects = {effect["stat"]: effect for effect in effects_data["effects"]}
        return effects

    def load_worlds(self):
        worlds = np.array({})
        with open("game_data/leveldata.json", "r") as world_file:
            world_data = json.load(world_file)
            worlds = {world["name"]: world for world in world_data["worlds"]}
        return worlds

    def load_ai_package(self):
        ai_package = np.array({})
        with open("game_data/ai.json", "r") as ai_file:
            ai_data = json.load(ai_file)
            ai_package = {ai["name"]: ai for ai in ai_data["npcs"]}
        return ai_package

    def load_dialogue(self):
        dialogue_lines = np.array({})
        with open("game_data/dialogue.json", "r") as dialogue_file:
            dialogue_data = json.load(dialogue_file)
            dialogue_lines = {
                dialogue["name"]: dialogue for dialogue in dialogue_data["dialoge"]
            }
        return dialogue_lines

    def load_quests(self):
        quests = np.array({})
        with open("game_data/quests.json", "r") as quest_file:
            quest_data = json.load(quest_file)
            quests = {quest["id"]: quest for quest in quest_data["quests"]}
        return quests

    def save(self):
        filename=f"{CM.player.name}_{CM.player.current_world}_{GM.game_date.print_date()}".replace(" ", "_")
        data=CM.player.to_dict()
        with open(f"saves/{filename}.habo", "w") as file:
            json_data=json.dumps(data, indent=2)
            file.write(json_data)
            return True

    def load(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)
            return data
        
    def world_save(self, world):
        path = os.path.dirname(world[0]["name"]["background"])
        path = os.path.join(path, CM.player.hash)
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(path, "data_modified.json")
        transformed_data = []
        for entry in world:
            if entry["type"] == "metadata":
                entry["name"]["time_passed"]=GM.game_date.get_date()
                transformed_entry = {"name": entry["name"], "type": entry["type"]}
            else:
                transformed_entry = {"name": entry["name"], "type": entry["type"], "x": entry["rect"].centerx, "y": entry["rect"].centery}
            transformed_data.append(transformed_entry)
        
        with open(path, "w") as file:
            json_data=json.dumps(transformed_data, indent=2)
            file.write(json_data)
        

    def get_stored_data(self, path):
        path = os.path.dirname(path)
        path = os.path.join(path, CM.player.hash)
        path = os.path.join(path, "data_modified.json")
        
        if not os.path.isfile(path):
            return None
        with open(path, "r") as file:
            data = json.load(file)
            return data
        

    # https://www.youtube.com/watch?v=vOn0z0IRVN8&list=PLI2unizewPmmLdFX9kTGPSnXJJCiasCw5&index=64&ab_channel=Nazareth-Topic

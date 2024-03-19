import glob
import json
import os

import cv2
import numpy as np
import pygame
from PIL import Image, ImageSequence

from game_manager import ClassManager as CM
from game_manager import GameManager as GM


def load_images(path, size, center):
    if path==None:
        path = "textures/Emblema_KGB.svg.png"
    # Load and return images as needed
    img = pygame.image.load(path)
    if size!=(0,0):
        img = pygame.transform.scale(img, size)
    img_rect = img.get_rect()
    img_rect.center = center
    return img, img_rect

def load_player(path):
    # Load player image
    player = pygame.image.load(path)
    player = pygame.transform.scale(player, (32, 64))
    player_rect = player.get_rect()
    return player, player_rect

def load_player_sprites():
    image_list = {}
    for filename in os.listdir("textures/npc/player"):
        if filename.endswith(".gif"):
            path = os.path.join("textures/npc/player", filename)
            key = filename[:-4]
            img, rect, fps=load_enemy_sprites(path)
            rect.clear()
            for i in range(len(img)):
                img[i] = pygame.transform.scale(img[i], (img[i].get_width()*2, img[i].get_height()*3))
                rect.append(img[i].get_rect())
            image_list[key] = {"image": img, "rect": rect, "fps": fps}
    return image_list

def load_background(path):
    # Load bg image
    bg = pygame.image.load(path)
    bg_rect = bg.get_rect()
    return bg, bg_rect

def load_level_data(path="terrain/worlds/simplified/Dream_World/data.json"):
    level_data = np.array({})
    with open(path, "r") as ai_file:
        level_data = json.load(ai_file)
    return level_data

def load_collision(path):
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (image.shape[0]*8, image.shape[1]*8), interpolation = cv2.INTER_AREA)
    binary_image = 1 - (image // 255)
    print(binary_image)
    # np.savetxt('map.txt', binary_image, fmt='%d')
    return binary_image

def load_items():
    item_list = np.array({})
    with open("game_data/items.json", "r") as items:
        item_list = json.load(items)
        item_list = {item["name"]: item for item in item_list["items"]}
    return item_list

def load_traits():
    traits = np.array({})
    with open("game_data/traits.json", "r") as traits_file:
        traits_data = json.load(traits_file)
        traits = {trait["name"]: trait for trait in traits_data["traits"]}
    return traits

def load_effects():
    effects = np.array({})
    with open("game_data/effects.json", "r") as effect_file:
        effects_data = json.load(effect_file)
        effects = {effect["stat"]: effect for effect in effects_data["effects"]}
    return effects

def load_worlds():
    worlds = np.array({})
    with open("game_data/leveldata.json", "r") as world_file:
        world_data = json.load(world_file)
        worlds = {world["name"]: world for world in world_data["worlds"]}
    return worlds

def load_ai_package():
    ai_package = np.array({})
    with open("game_data/ai.json", "r") as ai_file:
        ai_data = json.load(ai_file)
        ai_package = {ai["name"]: ai for ai in ai_data["npcs"]}
    return ai_package

def load_dialogue():
    dialogue_lines = np.array({})
    with open("game_data/dialogue.json", "r") as dialogue_file:
        dialogue_data = json.load(dialogue_file)
        dialogue_lines = {
            dialogue["name"]: dialogue for dialogue in dialogue_data["dialoge"]
        }
    return dialogue_lines

def load_quests():
    quests = np.array({})
    with open("game_data/quests.json", "r") as quest_file:
        quest_data = json.load(quest_file)
        quests = {quest["id"]: quest for quest in quest_data["quests"]}
    return quests

def find_substring_index_in_list(new_path, substr):
    renamed=False
    for index, string in enumerate(GM.save_world_names):
        if substr in string:
            renamed=True
            GM.save_world_names[index]=new_path
            
    if not renamed:
        GM.save_world_names.append(new_path)

def rename_index_worlds(save_name):
    for item in os.listdir("terrain\worlds\simplified"):
        item_path=f"terrain\worlds\simplified\{item}\{CM.player.hash}\data_modified.world"
        if os.path.isfile(item_path):
            new_path=os.path.join(os.path.dirname(item_path), save_name+".world")
            os.rename(item_path, os.path.join(os.path.dirname(item_path), save_name+".world"))
            find_substring_index_in_list(new_path, item)
            
def save():
    world_save()
    save_name =f"{CM.player.name}_{GM.game_date.print_date()}".replace(" ", "_").replace(",", "")
    rename_index_worlds(save_name)
    data=CM.player.to_dict()
    data["save_world_names"]=GM.save_world_names
    GM.save_name=save_name
    #print("---------SAVING DATA---------")
    #print(data)
    #print("-----------------------------")
    if not os.path.exists("saves"):
        os.makedirs("saves")
    with open(f"saves/{GM.save_name}.habo", "w") as file:
        json_data=json.dumps(data, indent=2)
        file.write(json_data)
        return True
    
def load(filename):
    with open(filename, "r") as file:
        data = json.load(file)
        return data
    
def world_save(file_name="data_modified.world"):
    world=GM.world_objects+GM.npc_list+GM.notes
    path = os.path.dirname(world[0]["name"]["background"])
    path = os.path.join(path, CM.player.hash)
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path, file_name)
    transformed_data = []
    for entry in world:
        if entry["type"] == "metadata":
            entry["name"]["time_passed"]=GM.game_date.get_date()
            transformed_entry = {"name": entry["name"], "type": entry["type"]}
        elif entry["type"]=="activator" or entry["type"]=="walk_in_portal":
            transformed_entry = {"name": entry["name"], "type": entry["type"], "x": entry["rect"].centerx, "y": entry["rect"].centery, "width": entry["rect"].width, "height": entry["rect"].height, "iid": entry["iid"]}
        elif entry["type"]=="container":
            transformed_entry = {"name": entry["name"], "type": entry["type"], "x": entry["rect"].centerx, "y": entry["rect"].centery, "pedistal": entry["pedistal"], "iid": entry["iid"]}
        else:
            transformed_entry = {"name": entry["name"], "type": entry["type"], "x": entry["rect"].centerx, "y": entry["rect"].centery, "iid": entry["iid"]}
        transformed_data.append(transformed_entry)
    
    with open(path, "w") as file:
        json_data=json.dumps(transformed_data, indent=2)
        file.write(json_data)
        
def get_stored_data(path, file_name="data_modified.world"):
    path = os.path.dirname(path)
    path = os.path.join(path, CM.player.hash)
    path = os.path.join(path, file_name)
    
    if not os.path.exists(os.path.dirname(path)):
        return None
    
    found_file=None
    if not os.path.isfile(path):
        files_in_folder = os.listdir(os.path.dirname(path))
        print(os.path.dirname(path))
        for file in files_in_folder:
            for meow in GM.save_world_names:
                if os.path.basename(file) in os.path.basename(meow):
                    found_file=os.path.join(os.path.dirname(path), file)
                    path=found_file
                    #print("bemti path", path)
                    break
        if found_file==None:
            return found_file
        
    with open(path, "r") as file:
        data = json.load(file)
        return data

def pilImageToSurface(pilImage):
    mode, size, data = pilImage.mode, pilImage.size, pilImage.tobytes()
    return pygame.image.fromstring(data, size, mode).convert_alpha()

def load_enemy_sprites(gif_path):
    pilImage = Image.open(gif_path)
    frames = []
    rects = []
    fps = pilImage.info.get('duration', 100) # Default to 100ms if duration is not available
    print(fps)
    if pilImage.format == 'GIF' and pilImage.is_animated:
        for frame in ImageSequence.Iterator(pilImage):
            pygameImage = pilImageToSurface(frame.convert('RGBA'))
            frames.append(pygameImage)
            rects.append(pygameImage.get_rect())
    else:
        pygameImage = pilImageToSurface(pilImage)
        frames.append(pygameImage)
        rects.append(pygameImage.get_rect())
    return frames, rects, fps




    
# https://www.youtube.com/watch?v=vOn0z0IRVN8&list=PLI2unizewPmmLdFX9kTGPSnXJJCiasCw5&index=64&ab_channel=Nazareth-Topic

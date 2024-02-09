import copy
import json
import os
import random

from asset_loader import AssetLoader
from game_manager import ClassManager as CM
from game_manager import GameManager as GM

assets = AssetLoader()
items = assets.load_items()
ai = assets.load_ai_package()


def setEnemies(enemy):
    for x in ai:
        if (
            ai[x]["stats"]["group"] == enemy["enemy_Type"]
            and enemy["chance"] >= random.random()
            and enemy["rarity"] == ai[x]["stats"]["rarity"]
        ):
            return x


def setItems(item):
    if (
        item["name"][0] == "common"
        or item["name"][0] == "uncommon"
        or item["name"][0] == "rare"
        or item["name"][0] == "epic"
        or item["name"][0] == "legendary"
    ):
        for x in items:
            if (
                items[x]["type"] == item["type"][0]
                and item["chance"][0] >= random.random()
                and item["name"][0] == items[x]["rarity"]
            ):
                return x
    else:
        for x in items:
            if item["chance"][0] >= random.random() and item["name"][0] == x:
                return x


def setContainer(item):
    tmp = []
    num_of_items = []
    for i, x in enumerate(item["items"]):
        if (
            x == "common"
            or x == "uncommon"
            or x == "rare"
            or x == "epic"
            or x == "legendary"
        ):
            if item["number_of_items"][i] == 0:
                for j in range(0, random.randint(2, 4)):
                    for y in items:
                        if (
                            items[y]["type"] == item["type"][i]
                            and item["chance"][i] >= random.random()
                            and item["items"][i] == items[y]["rarity"]
                        ):
                            if y in tmp:
                                index = tmp.index(y)
                                num_of_items[index] += random.randint(1, 3)
                            else:
                                num_of_items.append(random.randint(1, 3))
                                tmp.append(y)
            else:
                for y in items:
                    if (
                        items[y]["type"] == item["type"][i]
                        and item["chance"][i] >= random.random()
                        and item["items"][i] == items[y]["rarity"]
                    ):
                        if y in tmp:
                            index = tmp.index(y)
                            num_of_items[index] += item["number_of_items"][i]
                        else:
                            num_of_items.append(item["number_of_items"][i])
                            tmp.append(y)
        else:
            for y in items:
                if item["chance"][i] >= random.random() and item["items"][i] == y:
                    tmp.append(y)
                    num_of_items.append(item["number_of_items"][i])

    return tmp, num_of_items


def parser(world):
    spawn = (0, 0)
    portals = []
    enemies = []
    final_items = []
    containers = []
    metadata = []

    for x in world["entities"]:
        if x == "Player_spawn":
            for y in world["entities"][x]:
                if y["customFields"]["type"] == "default":
                    spawn = (y["x"], y["y"])
                else:
                    portals.append((y["customFields"], y["x"], y["y"]))

        elif x == "Enemy_Random_Spawn":
            for y in world["entities"][x]:
                tmp = setEnemies(y["customFields"])
                if tmp:
                    enemies.append((GM.ai_package[tmp], y["x"], y["y"]))

        elif x == "Item_field":
            for y in world["entities"][x]:
                tmp = setItems(y["customFields"])
                if tmp:
                    final_items.append((tmp, y["x"], y["y"]))

        elif x == "Container_field":
            for y in world["entities"][x]:
                tmp, nums = setContainer(y["customFields"])
                neke=[]
                for i, _ in enumerate(tmp):
                    neke.append({"type":tmp[i], "quantity":nums[i]})
                file_name = os.path.basename(y["customFields"]["image"]).split("/")[-1]
                containers.append(
                    (
                        neke,
                        y["x"],
                        y["y"],
                        y["customFields"]["name"],
                        "textures/static/" + file_name,
                        nums,
                    )
                )

        elif x == "Metadata":
            for i, _ in enumerate(world["entities"][x][0]["customFields"]["music"]):
                world["entities"][x][0]["customFields"]["music"][i] = world["entities"][
                    x
                ][0]["customFields"]["music"][i][3:]
            metadata = world["entities"][x][0]["customFields"]

    #print("-------------------")
    #print(spawn)
    #print("-------------------")
    #print(portals)
    #print("-------------------")
    #print(enemies)
    #print("-------------------")
    #print(final_items)
    #print("-------------------")
    #print(containers)
    #print("-------------------")
    #print(metadata)
    #print("-------------------")

    return spawn, portals, enemies, final_items, containers, metadata

def parse_visited(world):
    spawn = (0, 0)
    portals = []
    enemies = []
    final_items = []
    containers = []
    metadata = []
    for i in world:
        if i["type"]=="metadata":
            metadata=i["name"]
        elif i["type"]=="item":
            final_items.append((i["name"], i["x"], i["y"]))
        elif i["type"]=="container":
            i["name"][1]=i["x"]
            i["name"][2]=i["y"]
            containers.append(i["name"])
        elif i["type"]=="npc":
            enemies.append((i["name"], i["x"], i["y"]))
        elif i["type"]=="portal":
            portals.append((i["name"], i["x"], i["y"]))
            
    
    #print("-------------------")
    #print(spawn)
    #print("-------------------")
    #print(portals)
    #print("-------------------")
    #print(enemies)
    #print("-------------------")
    #print(final_items)
    #print("-------------------")
    #print(containers)
    #print("-------------------")
    #print(metadata)
    #print("-------------------")
            
        
    return spawn, portals, enemies, final_items, containers, metadata


def remove_uniques(original, modified):
    orig_spawn, orig_portals, orig_enemies, orig_final_items, orig_containers, orig_metadata = parser(copy.deepcopy(original))
    mod_spawn, mod_portals, mod_enemies, mod_final_items, mod_containers, mod_metadata = parse_visited(copy.deepcopy(modified))

    #print()
    #print("orig_spawn", orig_spawn)
    #print()
    #print("orig_portals", orig_portals)
    #print()
    #print("orig_enemies", orig_enemies)
    #print()
    #print("orig_final_items", orig_final_items)
    #print()
    #print("orig_containers", orig_containers)
    #print()
    #print("orig_metadata", orig_metadata)
    #print()
    #print()
    #print()
    #print("mod_spawn", mod_spawn)
    #print()
    #print("mod_portals", mod_portals)
    #print()
    #print("mod_enemies", mod_enemies)
    #print()
    #print("mod_final_items", mod_final_items)
    #print()
    #print("mod_containers", mod_containers)
    #print()
    #print("mod_metadata", mod_metadata)
    #print()
    
    
    for i, _ in enumerate(orig_enemies):
        if orig_enemies[i][0]["stats"]["rarity"]=="unique":
            in_mod=False
            for j in mod_enemies:
                if orig_enemies[i][0]["name"]==j[0]["name"]:
                    in_mod=True
                    
            if not in_mod and orig_enemies[i][0]["stats"]["rarity"]=="unique":
                orig_enemies.pop(i)
            
    for i, _ in enumerate(orig_final_items):
        if GM.items[orig_final_items[i][0]]["rarity"]=="unique":
            in_mod=False
            for j in mod_final_items:
                if orig_final_items[i][0]==j[0]:
                    in_mod=True
                    
            if not in_mod and GM.items[orig_final_items[i][0]]["rarity"]=="unique":
                orig_final_items.pop(i)
                    
    for i, _ in enumerate(orig_containers):
        for index, j in enumerate(orig_containers[i][0]):
            in_mod=False
            if GM.items[j["type"]]["rarity"]=="unique":
                for k in mod_containers[i][0]:
                    if j["type"]==k["type"]:
                        in_mod=True
                    
            if not in_mod and GM.items[j["type"]]["rarity"]=="unique":
                print(j)
                orig_containers[i][0].pop(index)
    
    return orig_spawn, orig_portals, orig_enemies, orig_final_items, orig_containers, orig_metadata
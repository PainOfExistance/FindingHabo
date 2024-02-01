import os
import random

from asset_loader import AssetLoader

assets = AssetLoader()
world = assets.load_level_data()
items = assets.load_items()
ai = assets.load_ai_package()

spawn = (0, 0)
portals = []
enemies = []
final_items = []
containers = []
metadata = []


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
    for i, x in enumerate(item["items"]):
        if (
            x == "common"
            or x == "uncommon"
            or x == "rare"
            or x == "epic"
            or x == "legendary"
        ):
            for y in items:
                if (
                    items[y]["type"] == item["type"][i]
                    and item["chance"][i] >= random.random()
                    and item["items"][i] == items[y]["rarity"]
                ):
                    tmp.append(y)
        else:
            for y in items:
                if (
                    item["chance"][i] >= random.random()
                    and item["items"][i] == y
                    ):
                        tmp.append(y)

    return tmp


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
                enemies.append((tmp, y["x"], y["y"]))

    elif x == "Item_field":
        for y in world["entities"][x]:
            tmp = setItems(y["customFields"])
            if tmp:
                final_items.append((tmp, y["x"], y["y"]))

    elif x == "Container_field":
        for y in world["entities"][x]:
            tmp = setContainer(y["customFields"])
            file_name=os.path.basename(y["customFields"]["image"]).split('/')[-1]
            
            if tmp:
                containers.append(
                    (
                        tmp,
                        y["x"],
                        y["y"],
                        y["customFields"]["name"],
                        "textures/static/"+file_name,
                    )
                )
                
    elif x=="Metadata":
        for i, _ in enumerate(world["entities"][x][0]["customFields"]["music"]):
            world["entities"][x][0]["customFields"]["music"][i]=world["entities"][x][0]["customFields"]["music"][i][3:]       
        metadata=world["entities"][x][0]["customFields"]

print("-------------------")
print(spawn)
print("-------------------")
print(portals)
print("-------------------")
print(enemies)
print("-------------------")
print(final_items)
print("-------------------")
print(containers)
print("-------------------")
print(metadata)
print("-------------------")

import copy
import multiprocessing
import sys
import threading

import pygame

import asset_loader as assets
import world_parser as wp
from colors import Colors
from game_manager import ClassManager as CM
from game_manager import GameManager as GM


def manage_global_npc():
    rm_list=[]
    for i, x in enumerate(GM.global_enemy_list):
        npc=shorten_tuple_npc(x)
        tmp=CM.ai.update(npc)
        x=lengthen_tuple_npc(x, tmp)
        #if tmp["name"]["stats"]["group"]=="Merchant":
        #    print(x)
        #    print()
        GM.global_enemy_list[i]=x
        if CM.player.current_world in x[0]["world"]:
            if x[0]["name"]=="TBP" or x[0]["stats"]["status"]=="dead":
                    tmp=wp.setEnemies(x[0]["customFields"])
                    print()
                    print(tmp)
                    print(CM.player.current_world)
                    print(x[0]["world"])
                    print()
                    if tmp:
                        x[0]["name"]=copy.deepcopy(GM.ai_package[tmp]["name"])
                        x[0]["movement_behavior"]=copy.deepcopy(GM.ai_package[tmp]["movement_behavior"])
                        x[0]["stats"]=copy.deepcopy(GM.ai_package[tmp]["stats"])
                        x[0]["items"]=copy.deepcopy(GM.ai_package[tmp]["items"])
                        x[0]["faction_data"]=copy.deepcopy(GM.ai_package[tmp]["faction_data"])
                        znj=((copy.deepcopy(x[0]), x[0]["portal"], x[0]["world"], x[-2], x[-1]))
                        znj[0]["package"]=(x[0]["customFields"]["package"] if x[0]["customFields"]["package"] != "" else "dream_city_merchant_misc")
                        znj[0]["routine"] = assets.load_routine(znj[0]["package"])
                        znj[0]["customFields"]=x[0]["customFields"]
                        day=GM.game_date.current_date.weekday()
                        time=f"{GM.game_date.current_date.hour}.{GM.game_date.current_date.minute:02d}"
                        znj[0]["current_routine"], znj[0]["world"], znj[0]["portal"]=copy.deepcopy(assets.get_actions(day, time, znj[0]["routine"]))
                        GM.transfer_list.append(copy.deepcopy(znj))
                        rm_list.append(i)
                        print()
                        print(znj)
                        print()
                    
            elif x[0]["stats"]["status"]!="dead" and x[0]["stats"]["status"]!="" and x[0]["name"]!="TBP":
                znj=(x[0], x[0]["portal"], x[0]["world"], x[3], x[4])
                #znj[0]["package"]==(x[0]["customFields"]["package"] if x[0]["customFields"]["package"] != "" else "dream_city_merchant_misc")
                znj[0]["routine"] = assets.load_routine(znj[0]["package"])
                day=GM.game_date.current_date.weekday()
                time=f"{GM.game_date.current_date.hour}.{GM.game_date.current_date.minute:02d}"
                znj[0]["current_routine"], znj[0]["world"], znj[0]["portal"]=copy.deepcopy(assets.get_actions(day, time, znj[0]["routine"]))
                GM.transfer_list.append(copy.deepcopy(znj))
                rm_list.append(i)
          
    for index in sorted(rm_list, reverse=True):
         GM.global_enemy_list.pop(index)
    
    #GM.global_enemy_list = [x for i, x in enumerate(GM.global_enemy_list) if i not in rm_list]
            
def update_npc(subtitle_font, prompt_font):
    rm_list=[]
    for index, x in enumerate(GM.npc_list):
        if GM.npc_list[index]["name"]["stats"]["status"] == "dead" and "death_anim" in x["name"]["stats"]:
            GM.anim_tiles.append({'row': x["rect"].top, 'col': x["rect"].left,
                                 'value': x["name"]["stats"]["death_anim"], "special": "hold", "counter": 0})
            img = CM.animation.data[x["name"]
                                    ["stats"]["death_anim"]]["frames"][-1]
            rect = img.get_rect()
            rect.left = x["rect"].left
            rect.top = x["rect"].top
            itm = copy.deepcopy(GM.npc_list[index]["name"]["items"])
            itm_nums = [x["quantity"] for x in itm]
            data = (itm, x["rect"].left, x["rect"].top, GM.npc_list[index]["name"]
                    ["name"], 'textures/static/chest.jpg', itm_nums, None, "", False)
            GM.world_objects.append({"image": img, "rect": rect, "type": "container",
                                    "name": data, "pedistal": data[6], "iid": data[7]})
            GM.global_enemy_list.append((copy.deepcopy(GM.npc_list[index]["name"]), GM.npc_list[index]["name"]["world"], None, GM.npc_list[index]["iid"], GM.npc_list[index]["rect"].center))
            rm_list.append(index)   
        elif GM.npc_list[index]["name"]["stats"]["status"]=="transfer":
            rm_list.append(index)
        elif GM.npc_list[index]["name"]["stats"]["status"] == "dead":
            rm_list.append(index)
    
    for index in sorted(rm_list, reverse=True):
        #? meow
        #GM.global_enemy_list.append((copy.deepcopy(GM.npc_list[index]["name"]), GM.npc_list[index]["name"]["world"], GM.npc_list[index]["name"]["portal"], GM.npc_list[index]["iid"], GM.npc_list[index]["rect"].center))
        GM.npc_list.pop(index)
    #GM.npc_list = [x for i, x in enumerate(GM.npc_list) if i not in rm_list] 

    for index, x in enumerate(GM.npc_list):
            if x["name"]["stats"]["status"] == "":
                # Add your indented block here
                continue
            
            if (
                not CM.menu.visible
                and not CM.player_menu.visible
                and not GM.is_in_dialogue
            ):
                lenghten_active_npc(x, CM.ai.update(shorten_active_npc(x)))
                        
            relative__left = int(GM.bg_rect.left + x["rect"].left)
            relative__top = int(GM.bg_rect.top + x["rect"].top)
            x["name"]["movement_behavior"]["moving"] = False
            agrov = False
            counter = 0
            for other in GM.npc_list:
                if other is not x:
                    counter += 1
                    dx = x["rect"].centerx - other["rect"].centerx
                    dy = x["rect"].centery - other["rect"].centery
                    distance = (dx**2 + dy**2)**0.5
                    if distance < x["name"]["talk_range"] and other["name"]["faction_data"]["faction"] not in x["name"]["faction_data"]["enemy_factions"]:
                        other_obj_rect = pygame.Rect(
                            relative__left,
                            relative__top,
                            x["rect"].width,
                            x["rect"].height,
                        )

                        GM.line = CM.ai.random_line(
                            (
                                (x["rect"].centerx),
                                (x["rect"].centery),
                            ),
                            (
                                (other["rect"].centerx),
                                (other["rect"].centery),
                            ),
                            x["name"]["name"],
                        )

                        x["agroved"] = False
                        other["agroved"] = False

                    elif distance < x["name"]["detection_range"] and other["name"]["faction_data"]["faction"] in x["name"]["faction_data"]["enemy_factions"]:
                        x["name"]["movement_behavior"]["target"] = other["rect"].center
                        other["name"]["movement_behavior"]["target"] = x["rect"].center
                        x["name"]["movement_behavior"]["moving"] = True
                        other["name"]["movement_behavior"]["moving"] = True
                        x["agroved"] = True
                        other["agroved"] = True

                        if other["rect"].colliderect(x["rect"]):
                            agrov = True
                            if x["attack_diff"] > x["name"]["attack_speed"]:
                                res = other["name"]["stats"]["defence"] - x["name"]["stats"]["damage"]
                                if res > 0:
                                    res = 0

                                other["name"]["stats"]["health"] += res
                                x["attack_diff"] = 0

                                if other["name"]["stats"]["health"] <= 0:
                                    other["name"]["stats"]["status"] = "dead"
                                    other["name"]["movement_behavior"]["moving"] = False
                                    other["name"]["movement_behavior"]["target"] = None

                            if x["attack_diff"] < 5:
                                x["attack_diff"] += GM.delta_time

                            if other["attack_diff"] > other["name"]["attack_speed"]:
                                res = x["name"]["stats"]["defence"] - \
                                    other["name"]["stats"]["damage"]
                                if res > 0:
                                    res = 0

                                x["name"]["stats"]["health"] += res
                                other["attack_diff"] = 0

                                if x["name"]["stats"]["health"] <= 0:
                                    x["name"]["stats"]["status"] = "dead"
                                    x["name"]["movement_behavior"]["moving"] = False
                                    x["name"]["movement_behavior"]["target"] = None

                            if other["attack_diff"] < 5:
                                other["attack_diff"] += GM.delta_time

                            break

            if counter == len(GM.npc_list)-2:
                x["agroved"] = False

            other_obj_rect = pygame.Rect(
                    relative__left,
                    relative__top,
                    x["rect"].width,
                    x["rect"].height,
                )
            
            for object in GM.world_objects:
                if (object["type"] == "portal" or object["type"]=="walk_in_portal") and object["name"]["type"]!="default" and "rect" in object and x["rect"].colliderect(object["rect"]):
                    print("meow when colliding portal")
                    x["name"]["path"]=[]
                    x["name"]["target"]=None
                    x["name"]["current_routine"]=[]
                    x["name"]["index_points"]=[]
                    x["name"]["column_index"]=0
                    x["name"]["column_index"]=0
                    x["name"]["to_face"]=0
                    #? meow
                    GM.global_enemy_list.append((copy.deepcopy(x["name"]), object["name"]["world_name"], object['name']['type'], x["iid"], x["rect"].center))
                    GM.npc_list[index]["name"]["stats"]["status"] = "transfer"

            if (
                "stats" in x["name"]
                and "status" in x["name"]["stats"]
                and x["name"]["stats"]["status"] == "alive"
                and x["name"]["stats"]["type"] == "enemy"
                and not GM.container_open
                and not CM.menu.visible
                and not CM.player_menu.visible
                and not GM.is_in_dialogue
                and not GM.crafting
            ):
                if not CM.player.player_rect.colliderect(other_obj_rect):
                    lenghten_active_npc(x, CM.ai.attack(shorten_active_npc(x)))
                    x["name"]["movement_behavior"]["moving"] = True

                if counter < len(GM.npc_list)-2:
                    x["agroved"] = True

                if CM.player.player_rect.colliderect(other_obj_rect):
                    agrov = True
                    if x["attack_diff"] > x["name"]["attack_speed"]:
                        res = CM.player.stats.defense - x["name"]["stats"]["damage"]

                        if res > 0:
                            res = 0

                        CM.player.update_health(res)
                        GM.npc_list[index]["attack_diff"] = 0

                if GM.npc_list[index]["attack_diff"] < 5:
                    GM.npc_list[index]["attack_diff"] += GM.delta_time

            if (
                "stats" in x["name"]
                and "status" in x["name"]["stats"]
                and x["name"]["stats"]["status"] == "alive"
                and not x["agroved"]
                and not GM.container_open
                and not CM.menu.visible
                and not CM.player_menu.visible
                and not GM.is_in_dialogue
                and not GM.crafting
            ):
                x["name"]["movement_behavior"]["moving"] = True
                GM.line = CM.ai.random_line(
                    (
                        (x["rect"].centerx),
                        (x["rect"].centery),
                    ),
                    (
                        (GM.relative_player_left + GM.relative_player_right) // 2,
                        (GM.relative_player_top + GM.relative_player_bottom) // 2,
                    ),
                    x["name"]["name"],
                )

            #if x["name"]["name"]=="Merchant":
            #    print()
            #    print()
            #    print(x)
            #    print()
            #    print()
                
            if (
                relative__left > -80
                and relative__left < GM.screen_width + 80
                and relative__top > -80
                and relative__top < GM.screen_height + 80
            ):
                if x["name"]["name"] == "Slime":
                    img, _ = CM.animation.animate_npc(x, index, agrov)
                    GM.screen.blit(img, (relative__left, relative__top))
                else:
                    GM.screen.blit(x["image"], (relative__left, relative__top))

                if other_obj_rect.colliderect(GM.weapon_rect) and x["type"] == "npc":
                    if GM.attacking:
                        if x["name"]["stats"]["type"] != "enemy":
                            GM.npc_list[index]["name"]["stats"]["type"] = "enemy"
                            GM.npc_list[index]["agroved"] = True
                        special_damage=(int(CM.player.stats.power)/int(CM.player.stats.max_power))*15
                        damage = special_damage+(int(CM.player.stats.weapon_damage)*min(0.98, ((0.2*int(CM.player.stats.weapon_damage))/int(x["name"]["stats"]["defence"]))**0.365))
                        GM.npc_list[index]["name"]["stats"][
                            "health"
                        ] -= damage

                        if GM.npc_list[index]["name"]["stats"]["health"] <= 0:
                            CM.player.level.gain_experience(
                                GM.npc_list[index]["name"]["stats"]["xp"]
                            )
                            GM.npc_list[index]["name"]["stats"]["status"] = "dead"
                            GM.npc_list[index]["agroved"] = False

                    if (
                        "stats" in GM.npc_list[index]["name"]
                        and GM.npc_list[index]["name"]["stats"]["type"] != "enemy"
                        and GM.npc_list[index]["name"]["stats"]["status"] != "dead"
                    ):
                        GM.talk_to_name = x["name"]["name"]
                        GM.propmt_pos = (relative__left + x["rect"].width // 2, relative__top - 10)
                        GM.is_ready_to_talk = True

                    if (
                        "stats" in GM.npc_list[index]["name"]
                        and GM.npc_list[index]["name"]["stats"]["health"] > 0
                        and GM.npc_list[index]["name"]["stats"]["type"] == "enemy"
                    ):
                        text = prompt_font.render(
                            str(GM.npc_list[index]["name"]["stats"]["health"]),
                            True,
                            Colors.red,
                        )
                        text_rect = text.get_rect(
                            center=(
                                relative__left + x["rect"].width // 2,
                                relative__top + x["rect"].height + 10,
                            )
                        )
                        GM.screen.blit(text, text_rect)
                elif (
                    not other_obj_rect.colliderect(GM.weapon_rect)
                    and x["type"] == "npc"
                    and "stats" in GM.npc_list[index]["name"]
                    and GM.npc_list[index]["name"]["stats"]["type"] != "enemy"
                    and GM.npc_list[index]["name"]["stats"]["status"] != "dead"
                ):
                    GM.is_ready_to_talk = False
                    GM.talk_to_name = ""

def play_line(subtitle_font, prompt_font):
    if GM.talk_to_name != "":
        text = prompt_font.render(
            f"E) {GM.talk_to_name}",
            True,
            Colors.chroma_blue,
        )
        text_rect = text.get_rect(
            center=(
                GM.propmt_pos[0],
                GM.propmt_pos[1],
            )
        )
        GM.screen.blit(text, text_rect)
    
    if GM.line != None and GM.line_time < GM.counter:
        GM.current_line = GM.line
        GM.line_time = (
            CM.music_player.play_line(
                GM.current_line["file"]) + GM.counter
        )
    if GM.current_line != None and GM.line_time >= GM.counter:
        text = subtitle_font.render(
            GM.current_line["text"], True, Colors.chroma_blue
        )
        text_rect = text.get_rect(
            center=(
                GM.screen.get_width() // 2,
                GM.screen.get_height() - 50,
            )
        )
        GM.screen.blit(text, text_rect)
    else:
        GM.current_line = None

def transfer_npc(tmp, inline=False):
    rm_list=[]
    for i, npc in enumerate(GM.transfer_list):
        portal=copy.deepcopy(tmp)
        if portal==None or portal=="default":
            portal={}
            portal["type"]="default"
            portal["spawn_point"]={}
            portal["spawn_point"]["cx"]=npc[-1][0]//16
            portal["spawn_point"]["cy"]=npc[-1][1]//16
        
        if npc[0]["name"]=="Merchant":
            print()
            print(npc[0]["name"])
            print(npc[2])
            print(CM.player.current_world)
            print()
        if (npc[1] == portal["type"] or portal["type"]=="default") and CM.player.current_world in npc[2]:
            try:
                if "inventory_type" in npc[0]["stats"]:
                    inventory_type = npc[0]["stats"]["inventory_type"].split("_")
                    inventory, item_list = CM.level_list.generate_inventory(inventory_type, int(inventory_type[-1]), inventory_type[0])
                    if len(npc[0]["items"]) > 0:
                        item_list = []
                        for item in npc[0]["items"]:
                            if item["type"] in inventory:
                                item["quantity"] = inventory[item["type"]] + item["quantity"]
                                inventory.pop(item["type"])
                        for item in inventory:
                            item_list.append({"type": item, "quantity": inventory[item]})
                    npc[0]["items"] = item_list

                if "package" in npc[0]:
                    npc[0]["routine"] = assets.load_routine(npc[0]["package"])

                if "png" in npc[0]["stats"]["image"]:
                    img, img_rect = assets.load_images(npc[0]["stats"]["image"], (64, 64), (portal["spawn_point"]["cx"]*16, portal["spawn_point"]["cy"]*16))
                    GM.npc_list.append({
                        "image": img,
                        "rect": img_rect,
                        "type": "npc",
                        "name": copy.deepcopy(npc[0]),
                        "attack_diff": 0,
                        "agroved": False,
                        "iid": npc[3]
                    })
                else:
                    images, rect=assets.load_enemy_sprites(f"./textures/npc/{npc[0]["stats"]["image"]}/")
                    rect.center=(portal["spawn_point"]["cx"]*16, portal["spawn_point"]["cy"]*16)
                    CM.animation.enemy_anims[npc[0]["name"].lower()]={"images": images, "rect": rect, "prev_action": ""}
                    GM.npc_list.append({
                        "image": images[list(images.keys())[0]]["frames"][0],
                        "rect": rect,
                        "type": "npc",
                        "name": copy.deepcopy(npc[0]),
                        "attack_diff": 0,
                        "agroved": False,
                        "iid": npc[3]
                    })
                    if GM.npc_list[-1]["name"]["name"].lower() not in CM.animation.enemy_anims:
                        CM.animation.load_anims(GM.npc_list[-1])
                rm_list.append(i)
                try:
                    GM.npc_list[-1]["name"]["world"]=CM.player.current_world
                    #lenghten_active_npc(GM.npc_list[-1], CM.ai.update(shorten_active_npc(GM.npc_list[-1])))
                    #if not inline:
                    #    GM.npc_list[-1]["rect"].center=copy.deepcopy(GM.npc_list[-1]["name"]["target"])
                except Exception as e:
                    print()
                    print(e)
                    print()
                    pass
                    
            except Exception as e:
                print()
                print(e)
                print()
                pass
    
    for index in sorted(rm_list, reverse=True):
         GM.transfer_list.pop(index)         
               
def set_npc():
    rm_list=[]
    for i, x in enumerate(GM.global_enemy_list):
        y=x[0]
        print()
        print("set_npc", x)
        print()
        day=GM.game_date.current_date.weekday()
        time=f"{GM.game_date.current_date.hour}.{GM.game_date.current_date.minute:02d}"
        current_routine, world, portal=copy.deepcopy(assets.get_actions(day, time, y["routine"]))
        if y["current_routine"]!=current_routine or CM.player.current_world in world:
            y["current_routine"]=copy.deepcopy(current_routine)
            y["world"]=copy.deepcopy(world)
            y["portal"]=copy.deepcopy(portal)
            if CM.player.current_world in world:
                #if "stats" not in y:
                #    tmp=wp.setEnemies(y["customFields"])
                #    if tmp:
                #        GM.transfer_list.append((copy.deepcopy(GM.ai_package[tmp]), y["portal"], y["world"], y["iid"], (y["x"], y["y"])))
                #        GM.transfer_list[-1][0]["package"]=y["customFields"]["package"]
                #        rm_list.append(i)
                if y["name"]=="TBP" or y["stats"]["status"]=="dead":
                    tmp=wp.setEnemies(y["customFields"])
                    if tmp:
                        znj=((copy.deepcopy(GM.ai_package[tmp]), y["portal"], y["world"], x[-2], x[-1]))
                        GM.transfer_list.append(copy.deepcopy(znj))
                        GM.transfer_list[-1][0]["package"]=y["customFields"]["package"]
                        rm_list.append(i)
                    
                elif y["stats"]["status"]!="dead" and y["stats"]["status"]!="" and y["name"]!="TBP":
                    znj=(y, y["portal"], y["world"], x[3], x[4])
                    GM.transfer_list.append(copy.deepcopy(znj))
                    GM.transfer_list[-1][0]["package"]=y["customFields"]["package"]
                    rm_list.append(i)
          
    GM.global_enemy_list = [x for i, x in enumerate(GM.global_enemy_list) if i not in rm_list]

def shorten_active_npc(x):
    return {
            "name": {
                "name": x["name"]["name"],
                "movement_behavior": {
                    "type": x["name"]["movement_behavior"]["type"],
                    "dirrection": x["name"]["movement_behavior"]["dirrection"],
                    "movement_speed": x["name"]["movement_behavior"]["movement_speed"]
                },
                "target": x["name"]["target"],
                "path": x["name"]["path"],
                "current_routine": x["name"]["current_routine"],
                "routine": x["name"]["routine"],
                "world": x["name"]["world"],
                "index_points": x["name"]["index_points"],
                "column_index": x["name"]["column_index"],
                "to_face":  x["name"]["to_face"],
                "detection_range": x["name"]["detection_range"],
                "portal": x["name"]["portal"] if "portal" in x["name"] else None,
                "stats": {
                    "group": x["name"]["stats"]["group"]
                }
            },
            "rect": {
                "center": x["rect"].center,
                "width": x["rect"].width,
                "height": x["rect"].height,
                "left": x["rect"].left,
                "top": x["rect"].top,
                "bottom": x["rect"].bottom,
                "right": x["rect"].right,
                "centerx": x["rect"].centerx,
                "centery": x["rect"].centery
            },
            "agroved": x["agroved"],
            "active": True
        }

def shorten_tuple_npc(x):
    y=copy.deepcopy(x[-1])
    x=copy.deepcopy(x[0])
    return {
            "name": {
                "name": x["name"],
                "movement_behavior": {
                    "type": x["movement_behavior"]["type"],
                    "dirrection": x["movement_behavior"]["dirrection"],
                    "movement_speed": x["movement_behavior"]["movement_speed"]
                },
                "target": x["target"],
                "path": x["path"],
                "current_routine": x["current_routine"],
                "routine": x["routine"],
                "world": x["world"],
                "index_points": x["index_points"],
                "column_index": x["column_index"],
                "to_face":  x["to_face"],
                "detection_range": x["detection_range"],
                "portal": x["portal"] if "portal" in x else None,
                "stats": {
                    "group": x["stats"]["group"]
                }
            },
            "rect": {
                "center": (y[0], y[1]),
                "width": 1,
                "height": 1,
                "left": y[0],
                "top": y[1],
                "bottom": y[1],
                "right": y[0],
                "centerx": y[0],
                "centery": y[1]
            },
            "agroved": False,
            "active": False
        }
    
def lenghten_active_npc(x, npc):
    x["name"]["movement_behavior"]["type"]=npc["name"]["movement_behavior"]["type"]
    x["name"]["movement_behavior"]["dirrection"]=npc["name"]["movement_behavior"]["dirrection"]
    x["name"]["movement_behavior"]["movement_speed"]=npc["name"]["movement_behavior"]["movement_speed"]
    x["name"]["target"]=npc["name"]["target"]
    x["name"]["path"]=npc["name"]["path"]
    x["name"]["current_routine"]=npc["name"]["current_routine"]
    x["name"]["routine"]=npc["name"]["routine"]
    x["name"]["world"]=npc["name"]["world"]
    x["name"]["index_points"]=npc["name"]["index_points"]
    x["name"]["column_index"]=npc["name"]["column_index"]
    x["name"]["to_face"]=npc["name"]["to_face"]
    x["name"]["detection_range"]=npc["name"]["detection_range"]
    x["agroved"]=npc["agroved"]
    x["name"]["stats"]["group"]=npc["name"]["stats"]["group"]
    x["rect"].center=npc["rect"]["center"]
    x["rect"].width=npc["rect"]["width"]
    x["rect"].height=npc["rect"]["height"]
    x["rect"].left=npc["rect"]["left"]
    x["rect"].top=npc["rect"]["top"]
    x["rect"].bottom=npc["rect"]["bottom"]
    x["rect"].right=npc["rect"]["right"]
    x["rect"].centerx=npc["rect"]["centerx"]
    x["rect"].centery=npc["rect"]["centery"]
    x["name"]["name"]=npc["name"]["name"]
    x["name"]["active"]=True
    x["name"]["portal"]=npc["name"]["portal"]
    x["name"]["portal_to_be"]=npc.get("name").get("portal_to_be", "")

def lengthen_tuple_npc(x, npc):
    x=list(x)
    x[0]["movement_behavior"]["type"]=npc["name"]["movement_behavior"]["type"]
    x[0]["movement_behavior"]["dirrection"]=npc["name"]["movement_behavior"]["dirrection"]
    x[0]["movement_behavior"]["movement_speed"]=npc["name"]["movement_behavior"]["movement_speed"]
    x[0]["target"]=npc["name"]["target"]
    x[0]["path"]=npc["name"]["path"]
    x[0]["current_routine"]=npc["name"]["current_routine"]
    x[0]["routine"]=npc["name"]["routine"]
    x[0]["world"]=npc["name"]["world"]
    x[0]["index_points"]=npc["name"]["index_points"]
    x[0]["column_index"]=npc["name"]["column_index"]
    x[0]["to_face"]=npc["name"]["to_face"]
    x[0]["detection_range"]=npc["name"]["detection_range"]
    x[0]["stats"]["group"]=npc["name"]["stats"]["group"]
    x[-1]=npc["rect"]["center"]
    x[0]["name"]=npc["name"]["name"]
    x[0]["active"]=False
    x[0]["portal"]=npc["name"]["portal"]
    x[0]["portal_to_be"]=npc.get("name").get("portal_to_be", "")
    x=tuple(x)
    return x
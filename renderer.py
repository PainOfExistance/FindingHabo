import copy
import math

import numpy as np
import pygame

import puzzle
from colors import Colors
from game_manager import ClassManager as CM
from game_manager import GameManager as GM


def draw_container(menu_font):
    if GM.container_open and GM.container_hovered != None:
        if GM.world_objects[GM.container_hovered]["pedistal"] != None:
            _, ref=puzzle.find_ref(GM.world_objects[GM.container_hovered]["pedistal"]["entityIid"], "pedistal")
            index, _=puzzle.find_ref(ref["name"]["ref"]["entityIid"], "trap")
            GM.world_objects[index]["name"]["trap"]="ref"
            
            if puzzle.check_pedistal(GM.world_objects[GM.container_hovered]["name"][0], ref["name"]["pedistal"]):
                GM.container_open=False
                GM.container_hovered=None
                for i, x in enumerate(GM.world_objects):
                    if x["type"]=="walk_in_portal" and x["iid"]==ref["name"]["door_ref"]["entityIid"]:
                        GM.world_objects[i]["name"]["locked"]=False
                        break
                return
            elif puzzle.check_pedistal(GM.world_objects[GM.container_hovered]["name"][0], ref["name"]["pedistal"])==False:
                index, ref=puzzle.find_ref(ref["name"]["ref"]["entityIid"], "trap")
                GM.world_objects[index]["name"]["trap"]="spikes"
                      
        CM.ai.strings.bartering = False
        pygame.draw.rect(
            GM.bg_surface_menu,
            Colors.bg_color,
            GM.bg_surface_menu.get_rect(),
        )
        GM.screen.blit(GM.bg_surface_menu, GM.bg_menu)
        
        pygame.draw.line(
            GM.screen,
            Colors.edge_color,
            (GM.screen.get_width() // 2, 0),
            (GM.screen.get_width() // 2, GM.screen.get_height()),
            4,
        )
        
        scroll_position = (GM.selected_inventory_item // 10) * 10
        visible_items = GM.world_objects[GM.container_hovered]["name"][0][
            scroll_position : scroll_position + 10
        ]
        
        i = 0
        item_render = menu_font.render(
            CM.player.name,
            True,
            Colors.active_item,
        )
        item_rect = item_render.get_rect(
            topleft=(
                GM.screen.get_width() // 2 - GM.screen.get_width() // 3,
                20 + i * 50,
            )
        )
        GM.screen.blit(item_render, item_rect)
        
        item_render = menu_font.render(
            GM.world_objects[GM.container_hovered]["name"][3],
            True,
            Colors.active_item,
        )
        item_rect = item_render.get_rect(
            topleft=(
                GM.screen.get_width() // 2 + GM.screen.get_width() // 5,
                20 + i * 50,
            )
        )
        GM.screen.blit(item_render, item_rect)
        
        i += 1
        pygame.draw.line(
            GM.screen,
            Colors.edge_color,
            (0, 20 + i * 50),
            (GM.screen.get_width(), 20 + i * 50),
            4,
        )
        
        for index, (data) in enumerate(visible_items):
            color = (
                Colors.active_item
                if index == GM.selected_inventory_item - scroll_position
                else Colors.inactive_item
            )
            if not GM.container_menu_selected:
                color = Colors.unselected_item
            if (
                index == GM.selected_inventory_item - scroll_position
                and GM.container_menu_selected
            ):
                item_text = "}"+f" {data['type']}: {data['quantity']}"
            else:
                item_text = f"    {data['type']}: {data['quantity']}"
            item_render = menu_font.render(item_text, True, color)
            item_rect = item_render.get_rect(
                topleft=(GM.screen.get_width() // 2 + 20, 20 + (index + 2) * 40)
            )
            GM.screen.blit(item_render, item_rect)
            
        scroll_position = (GM.selected_inventory_item // 10) * 10
        visible_items = list(CM.inventory.quantity.items())[
            scroll_position : scroll_position + 10
        ]
        for index, (item_name, item_quantity) in enumerate(visible_items):
            color = (
                Colors.active_item
                if index == GM.selected_inventory_item - scroll_position
                else Colors.inactive_item
            )
            if GM.container_menu_selected:
                color = Colors.unselected_item
            if (
                index == GM.selected_inventory_item - scroll_position
                and not GM.container_menu_selected
            ):
                item_text = "}"+f" {item_name}: {item_quantity}"
            else:
                item_text = f"    {item_name}: {item_quantity}"
                
            item_render = menu_font.render(item_text, True, color)
            item_rect = item_render.get_rect(topleft=(10, 20 + (index + 2) * 40))
            GM.screen.blit(item_render, item_rect)
            
    elif not CM.ai.strings.bartering:
        GM.enter_held = False
        
def draw_barter(menu_font):
    if CM.ai.strings.bartering:
        GM.container_open = False
        pygame.draw.rect(
            GM.bg_surface_menu,
            Colors.bg_color,
            GM.bg_surface_menu.get_rect(),
        )
        GM.screen.blit(GM.bg_surface_menu, GM.bg_menu)
        pygame.draw.line(
            GM.screen,
            Colors.edge_color,
            (GM.screen.get_width() // 2, 0),
            (GM.screen.get_width() // 2, GM.screen.get_height()),
            4,
        )
        scroll_position = (GM.selected_inventory_item // 10) * 10
        visible_items = list(GM.ai_package[GM.talk_to_name]["items"])[
            scroll_position : scroll_position + 10
        ]
        i = 0
        item_render = menu_font.render(
            CM.player.name + "  Gold: " + str(CM.player.gold),
            True,
            Colors.active_item
        )
        item_rect = item_render.get_rect(
            topleft=(
                GM.screen.get_width() // 2 - GM.screen.get_width() // 2.5,
                20 + i * 50,
            )
        )
        GM.screen.blit(item_render, item_rect)
        item_render = menu_font.render(
            GM.talk_to_name
            + "  Gold: "
            + str(GM.ai_package[GM.talk_to_name]["gold"]),
            True,
            Colors.active_item
        )
        item_rect = item_render.get_rect(
            topleft=(
                GM.screen.get_width() // 2 + GM.screen.get_width() // 9,
                20 + i * 50,
            )
        )
        GM.screen.blit(item_render, item_rect)
        i += 1
        pygame.draw.line(
            GM.screen,
            Colors.edge_color,
            (0, 20 + i * 50),
            (GM.screen.get_width(), 20 + i * 50),
            4,
        )
        for index, (data) in enumerate(visible_items):
            color = (
                Colors.active_item
                if index == GM.selected_inventory_item - scroll_position
                else Colors.inactive_item
            )
            if not GM.container_menu_selected:
                color = Colors.unselected_item
            if (
                index == GM.selected_inventory_item - scroll_position
                and GM.container_menu_selected
            ):
                item_text = "}"+f" {data['type']}: {data['quantity']}  {GM.items[GM.ai_package[GM.talk_to_name]['items'][index+scroll_position]['type']]['price']}"
            else:
                item_text = f"    {data['type']}: {data['quantity']}  {GM.items[GM.ai_package[GM.talk_to_name]['items'][index+scroll_position]['type']]['price']}"
            item_render = menu_font.render(item_text, True, color)
            item_rect = item_render.get_rect(
                topleft=(GM.screen.get_width() // 2 + 20, 20 + (index + 2) * 40)
            )
            GM.screen.blit(item_render, item_rect)
        scroll_position = (GM.selected_inventory_item // 10) * 10
        visible_items = list(CM.inventory.quantity.items())[
            scroll_position : scroll_position + 10
        ]
        for index, (item_name, item_quantity) in enumerate(visible_items):
            color = (
                Colors.active_item
                if index == GM.selected_inventory_item - scroll_position
                else Colors.inactive_item
            )
            if GM.container_menu_selected:
                color = Colors.unselected_item
            if (
                index == GM.selected_inventory_item - scroll_position
                and not GM.container_menu_selected
            ):
                item_text = "}"+f" {item_name}: {item_quantity}  {GM.items[item_name]['price']}"
            else:
                item_text = f"    {item_name}: {item_quantity}  {GM.items[item_name]['price']}"
            item_render = menu_font.render(item_text, True, color)
            item_rect = item_render.get_rect(topleft=(10, 20 + (index + 2) * 40))
            GM.screen.blit(item_render, item_rect)
    elif not GM.container_open:
        GM.enter_held = False

def draw_objects(prompt_font):
    can_travel = False
    for index, x in enumerate(GM.world_objects):
        if index == 0:
            continue

        relative__left = int(GM.bg_rect.left + x["rect"].left)
        relative__top = int(GM.bg_rect.top + x["rect"].top)

        if (
            relative__left > -80
            and relative__left < GM.screen_width + 80
            and relative__top > -80
            and relative__top < GM.screen_height + 80
        ):
            if (
                x["type"] == "walk_in_portal"
            ):
                if x["name"]["locked"]:
                    GM.collision_map[
                        x["rect"].top : x["rect"].bottom,
                        x["rect"].left : x["rect"].right,
                    ] = 1
                    GM.screen.blit(x["image"], (relative__left, relative__top))
                else:
                    GM.collision_map[
                        x["rect"].top : x["rect"].bottom,
                        x["rect"].left : x["rect"].right,
                    ] = 0

            elif "stats" not in x["name"] and "image" in x:
                GM.screen.blit(x["image"], (relative__left, relative__top))

            if x["type"] == "container":
                GM.collision_map[
                    x["rect"].top + 10 : x["rect"].bottom - 10,
                    x["rect"].left + 10 : x["rect"].right - 10,
                ] = 1

            other_obj_rect = pygame.Rect(
                relative__left,
                relative__top,
                x["rect"].width,
                x["rect"].height,
            )

            if (
                other_obj_rect.colliderect(CM.player.player_rect)
                and x["type"] == "item"
            ):
                GM.item_hovered = index
                text = prompt_font.render(f"E) Pick up", True, Colors.mid_black)
                text_rect = text.get_rect(
                    center=(
                        relative__left + x["rect"].width // 2,
                        relative__top + x["rect"].height + 10,
                    )
                )
                GM.screen.blit(text, text_rect)

                text = prompt_font.render(x["name"], True, Colors.mid_black)
                text_rect = text.get_rect(
                    center=(
                        relative__left + x["rect"].width // 2,
                        relative__top + x["rect"].height + 25,
                    )
                )
                GM.screen.blit(text, text_rect)

            elif (
                not other_obj_rect.colliderect(CM.player.player_rect)
                and x["type"] == "item"
                and index == GM.item_hovered
            ):
                GM.item_hovered = None

            if (
                other_obj_rect.colliderect(CM.player.player_rect)
                and x["type"] == "container"
            ):
                GM.container_hovered = index
                text = prompt_font.render(f"E) Access", True, Colors.mid_black)
                text_rect = text.get_rect(
                    center=(
                        relative__left + x["rect"].width // 2,
                        relative__top + x["rect"].height + 10,
                    )
                )
                GM.screen.blit(text, text_rect)
            elif (
                not other_obj_rect.colliderect(CM.player.player_rect)
                and x["type"] == "container"
                and index == GM.container_hovered
            ):
                GM.container_hovered = None

            if (
                x["type"] == "portal"
                and not GM.container_open
                and not CM.menu.visible
                and not CM.player_menu.visible
                and not GM.is_in_dialogue
                and other_obj_rect.colliderect(CM.player.player_rect)
            ):
                if x["name"]["locked"]:
                    text = prompt_font.render(
                        f"Key required) {x['name']['world_name']} ",
                        True,
                        Colors.mid_black
                    )
                else:
                    text = prompt_font.render(
                        f"E) {x['name']['world_name']} ", True, Colors.mid_black
                    )
                text_rect = text.get_rect(
                    center=(
                        relative__left + x["rect"].width // 2,
                        relative__top + x["rect"].height + 10,
                    )
                )
                GM.world_to_travel_to = x["name"]
                GM.world_to_travel_to["index"] = index
                GM.screen.blit(text, text_rect)

            elif (
                not other_obj_rect.colliderect(CM.player.player_rect)
                and x["type"] == "portal"
            ):
                GM.world_to_travel_to = None
        
            if (other_obj_rect.colliderect(CM.player.player_rect) and x["type"]=="activator" and x["name"]["type"]=="quest"):
                if CM.player.quests.check_quest_state(x["name"]["quest"])=="not started":
                    CM.player.quests.start_quest(x["name"]["quest"])
                    CM.ai.strings.starts = 0
            if x["type"]=="activator" and x["name"]["type"]=="trap" and not GM.container_open and x["name"]["trap"]!="ref" and "activated" not in x["name"]["trap"]:
                #todo play anim depending on trap type
                for ti, tx in enumerate(GM.npc_list):
                    relative__left = int(GM.bg_rect.left + tx["rect"].left)
                    relative__top = int(GM.bg_rect.top + tx["rect"].top)
                    rect = pygame.Rect(relative__left, relative__top, tx["rect"].width, tx["rect"].height)
                    
                    if other_obj_rect.colliderect(rect):
                        GM.npc_list[ti]["name"]["stats"]["health"]-=50
                        if GM.npc_list[ti]["name"]["stats"]["health"]<=0:
                            GM.npc_list[ti]["name"]["stats"]["status"] = "dead"
                            GM.npc_list[ti]["agroved"] = False
                        GM.world_objects[index]["name"]["trap"]+=" activated"
                            
                if other_obj_rect.colliderect(CM.player.player_rect):
                    CM.player.update_health(-50)
                    GM.world_objects[index]["name"]["trap"]+=" activated"
                    
            if (other_obj_rect.colliderect(CM.player.player_rect) and x["type"]=="activator" and x["name"]["type"]=="board"):
                can_travel = True
            else:
                GM.can_fast_travel = False
                
            if (other_obj_rect.colliderect(CM.player.player_rect) and x["type"]=="activator" and x["name"]["type"]=="script_runner"):
                for index, script in enumerate(x["name"]["script_runner"]):
                    if not script["used"]:
                        CM.script_loader.run_script(script["script_name"], script["function"], script["args"])
                        x["name"]["script_runner"][index]["used"]=True   
                    
            other_rect = pygame.Rect(
                relative__left-50,
                relative__top-50,
                x["rect"].width+100,
                x["rect"].height+100,
            )
            
            if (
                x["type"] == "walk_in_portal"
                and not GM.container_open
                and not CM.menu.visible
                and not CM.player_menu.visible
                and not GM.is_in_dialogue
                and other_rect.colliderect(CM.player.player_rect)
            ):
                if not x["name"]["locked"]:
                    GM.collision_map[
                        x["rect"].top : x["rect"].bottom,
                        x["rect"].left : x["rect"].right,
                    ] = 0
                    
                    text = prompt_font.render(
                        f"{x['name']['world_name']} ", True, Colors.mid_black
                    )
                    text_rect = text.get_rect(
                        center=(
                        relative__left + x["rect"].width // 2,
                        relative__top + x["rect"].height + 10,
                        )
                    )
                    
                    GM.screen.blit(text, text_rect)
                    
                    if other_obj_rect.colliderect(CM.player.player_rect):
                        GM.world_to_travel_to = x["name"]
                        GM.world_to_travel_to["index"] = index
                        GM.load = True
                            
            elif (
                not other_obj_rect.colliderect(CM.player.player_rect)
                and x["type"] == "walk_in_portal"
            ):
                GM.world_to_travel_to = None
            
            if can_travel:
                GM.can_fast_travel = True
                
def check_notes():
    for index, x in enumerate(GM.notes):
        if not GM.notes[index]["name"]["discovered"] and math.dist((x["x"], x["y"]), (GM.relative_player_left+CM.player.player_rect.width//2, GM.relative_player_top+CM.player.player_rect.height//2))<x["name"]["radius"]:
            GM.notes[index]["name"]["discovered"]=True
            CM.player.quests.text_to_draw.clear()
            CM.player.quests.text_to_draw.append("Discovered: " + x["name"]["name"])
            CM.player.quests.tics = pygame.time.get_ticks()
            CM.player.level.gain_experience(x["name"]["xp"])
            return

def draw_notes(rect, prompt_font):
    hover={"name":None,"x":None,"y":None, "index":None}
    for i, note in enumerate(GM.notes):
        if note["name"]["discovered"]:
            relative_left = int(rect.left + (note["rect"].left//2)*CM.map.zoom)
            relative_top = int(rect.top + (note["rect"].top//2)*CM.map.zoom)
            GM.screen.blit(note["image"], (relative_left, relative_top))
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rect = pygame.Rect(relative_left, relative_top, note["rect"].width, note["rect"].height)
            if rect.collidepoint(np.round(mouse_x*GM.ratio[0]), np.round(mouse_y*GM.ratio[1])):
                text = prompt_font.render(f"{note['name']['name']}", True, Colors.mid_black)
                text_rect = text.get_rect(
                    center=(relative_left+note["rect"].width//2, relative_top-8)
                )
                GM.screen.blit(text, text_rect)
                
                hover={"name":note["name"]["name"],"x":note["x"],"y":note["y"], "index":i}
                if not note["moved"]:
                    note["rect"].left -= 16
                    note["rect"].top -= 16
                    note["rect"].width += 16
                    note["rect"].height += 16
                    note["image"]=pygame.transform.scale(note["image"], (32,32))
                note["moved"]=True
                
            mouse_buttons = pygame.mouse.get_pressed()
            if rect.collidepoint(np.round(mouse_x*GM.ratio[0]), np.round(mouse_y*GM.ratio[1])) and mouse_buttons[0] and GM.prev_mouse>=20 and GM.can_fast_travel:
                CM.map.fast_travel()
            elif rect.collidepoint(np.round(mouse_x*GM.ratio[0]), np.round(mouse_y*GM.ratio[1])) and mouse_buttons[0] and GM.prev_mouse<=20 and GM.can_fast_travel:
                GM.prev_mouse+=1
            else:
                GM.prev_mouse=0
                
    if GM.location_hovered["name"] != hover["name"]:
        if GM.location_hovered["name"] != None and GM.notes[GM.location_hovered["index"]]["moved"]:
            GM.notes[GM.location_hovered["index"]]["rect"].left += 16
            GM.notes[GM.location_hovered["index"]]["rect"].top += 16
            GM.notes[GM.location_hovered["index"]]["rect"].width -= 16
            GM.notes[GM.location_hovered["index"]]["rect"].height -= 16
            GM.notes[GM.location_hovered["index"]]["image"]=pygame.transform.scale(note["image"], (16,16))
            GM.notes[GM.location_hovered["index"]]["moved"]=False
        GM.location_hovered={"name":hover["name"],"x":hover["x"],"y":hover["y"], "index":hover["index"]}
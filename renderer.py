import pygame

import puzzle
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
            (200, 210, 200, 180),
            GM.bg_surface_menu.get_rect(),
        )
        GM.screen.blit(GM.bg_surface_menu, GM.bg_menu)
        
        pygame.draw.line(
            GM.screen,
            (22, 22, 22),
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
            (44, 53, 57),
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
            (44, 53, 57),
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
            (22, 22, 22),
            (0, 20 + i * 50),
            (GM.screen.get_width(), 20 + i * 50),
            4,
        )
        
        for index, (data) in enumerate(visible_items):
            color = (
                (157, 157, 210)
                if index == GM.selected_inventory_item - scroll_position
                else (237, 106, 94)
            )
            if not GM.container_menu_selected:
                color = (44, 53, 57)
            if (
                index == GM.selected_inventory_item - scroll_position
                and GM.container_menu_selected
            ):
                item_text = f"> {data['type']}: {data['quantity']}"
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
                (157, 157, 210)
                if index == GM.selected_inventory_item - scroll_position
                else (237, 106, 94)
            )
            if GM.container_menu_selected:
                color = (44, 53, 57)
            if (
                index == GM.selected_inventory_item - scroll_position
                and not GM.container_menu_selected
            ):
                item_text = f"> {item_name}: {item_quantity}"
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
            (200, 210, 200, 180),
            GM.bg_surface_menu.get_rect(),
        )
        GM.screen.blit(GM.bg_surface_menu, GM.bg_menu)
        pygame.draw.line(
            GM.screen,
            (22, 22, 22),
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
            (44, 53, 57),
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
            (44, 53, 57),
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
            (22, 22, 22),
            (0, 20 + i * 50),
            (GM.screen.get_width(), 20 + i * 50),
            4,
        )
        for index, (data) in enumerate(visible_items):
            color = (
                (157, 157, 210)
                if index == GM.selected_inventory_item - scroll_position
                else (237, 106, 94)
            )
            if not GM.container_menu_selected:
                color = (44, 53, 57)
            if (
                index == GM.selected_inventory_item - scroll_position
                and GM.container_menu_selected
            ):
                item_text = f"> {data['type']}: {data['quantity']}  {GM.items[GM.ai_package[GM.talk_to_name]['items'][index+scroll_position]['type']]['price']}"
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
                (157, 157, 210)
                if index == GM.selected_inventory_item - scroll_position
                else (237, 106, 94)
            )
            if GM.container_menu_selected:
                color = (44, 53, 57)
            if (
                index == GM.selected_inventory_item - scroll_position
                and not GM.container_menu_selected
            ):
                item_text = f"> {item_name}: {item_quantity}  {GM.items[item_name]['price']}"
            else:
                item_text = f"    {item_name}: {item_quantity}  {GM.items[item_name]['price']}"
            item_render = menu_font.render(item_text, True, color)
            item_rect = item_render.get_rect(topleft=(10, 20 + (index + 2) * 40))
            GM.screen.blit(item_render, item_rect)
    elif not GM.container_open:
        GM.enter_held = False

def draw_objects(prompt_font):
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
                text = prompt_font.render(f"E) Pick up", True, (0, 0, 0))
                text_rect = text.get_rect(
                    center=(
                        relative__left + x["rect"].width // 2,
                        relative__top + x["rect"].height + 10,
                    )
                )
                GM.screen.blit(text, text_rect)

                text = prompt_font.render(x["name"], True, (0, 0, 0))
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
                text = prompt_font.render(f"E) Access", True, (0, 0, 0))
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
                        (44, 53, 57),
                    )
                else:
                    text = prompt_font.render(
                        f"E) {x['name']['world_name']} ", True, (44, 53, 57)
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
            
            if (
                x["type"] == "walk_in_portal"
                and not GM.container_open
                and not CM.menu.visible
                and not CM.player_menu.visible
                and not GM.is_in_dialogue
                and other_obj_rect.colliderect(CM.player.player_rect)
            ):
                if not x["name"]["locked"]:
                    GM.collision_map[
                        x["rect"].top : x["rect"].bottom,
                        x["rect"].left : x["rect"].right,
                    ] = 0
                    
                    text = prompt_font.render(
                        f"E) {x['name']['world_name']} ", True, (44, 53, 57)
                    )
                    text_rect = text.get_rect(
                        center=(
                        relative__left + x["rect"].width // 2,
                        relative__top + x["rect"].height + 10,
                        )
                    )
                    
                    GM.screen.blit(text, text_rect)
                
                    GM.world_to_travel_to = x["name"]
                    GM.world_to_travel_to["index"] = index
                            
            elif (
                not other_obj_rect.colliderect(CM.player.player_rect)
                and x["type"] == "walk_in_portal"
            ):
                GM.world_to_travel_to = None
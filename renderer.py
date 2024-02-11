import pygame

from game_manager import ClassManager as CM
from game_manager import GameManager as GM


def draw_container(menu_font):
    if GM.container_open:
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


def draw_objects(subtitle_font, prompt_font):
    for index, x in enumerate(GM.world_objects):
        if index == 0:
            continue
        if (
            "stats" in x["name"]
            and "status" in x["name"]["stats"]
            and x["name"]["stats"]["status"] == "alive"
            and x["name"]["stats"]["type"] == "enemy"
            and not GM.container_open
            and not CM.menu.visible
            and not CM.player_menu.visible
            and not GM.is_in_dialogue
        ):
            # print(x)
            dx, dy, agroved = CM.ai.attack(
                x["name"]["name"],
                (
                    (x["rect"].centerx),
                    (x["rect"].centery),
                ),
                (
                    (GM.relative_player_left + GM.relative_player_right) // 2,
                    (GM.relative_player_top + GM.relative_player_bottom) // 2,
                ),
                GM.collision_map,
                x["rect"],
            )

            GM.world_objects[index]["agroved"] = agroved
            x["rect"].centerx = dx
            x["rect"].centery = dy
            relative__left = int(GM.bg_rect.left + x["rect"].left)
            relative__top = int(GM.bg_rect.top + x["rect"].top)

            other_obj_rect = pygame.Rect(
                relative__left,
                relative__top,
                x["rect"].width,
                x["rect"].height,
            )

            if CM.player.player_rect.colliderect(other_obj_rect):
                if x["attack_diff"] > x["name"]["attack_speed"]:
                    res = CM.player.stats.defense - x["name"]["stats"]["damage"]

                    if res > 0:
                        res = 0

                    CM.player.update_health(res)
                    GM.world_objects[index]["attack_diff"] = 0

            if GM.world_objects[index]["attack_diff"] < 5:
                GM.world_objects[index]["attack_diff"] += GM.delta_time

        else:
            relative__left = int(GM.bg_rect.left + x["rect"].left)
            relative__top = int(GM.bg_rect.top + x["rect"].top)

        if (
            "stats" in x["name"]
            and "status" in x["name"]["stats"]
            and x["name"]["stats"]["status"] == "alive"
            and not x["agroved"]
            and not GM.container_open
            and not CM.menu.visible
            and not CM.player_menu.visible
            and not GM.is_in_dialogue
        ):
            dx, dy = CM.ai.update(
                x["name"]["name"],
                GM.collision_map,
                x["rect"].left,
                x["rect"].top,
                x["rect"],
            )
            x["rect"].centerx = dx
            x["rect"].centery = dy
            relative__left = int(GM.bg_rect.left + x["rect"].left)
            relative__top = int(GM.bg_rect.top + x["rect"].top)

            line = CM.ai.random_line(
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

            if line != None and GM.line_time < GM.counter:
                GM.current_line = line
                GM.line_time = (
                    CM.music_player.play_line(GM.current_line["file"]) + GM.counter
                )

            if GM.current_line != None and GM.line_time >= GM.counter:
                text = subtitle_font.render(
                    GM.current_line["text"], True, (44, 53, 57)
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

        if (
            relative__left > -80
            and relative__left < GM.screen_width + 80
            and relative__top > -80
            and relative__top < GM.screen_height + 80
        ):
            if (
                "stats" in x["name"]
                and "status" in x["name"]["stats"]
                and x["name"]["stats"]["status"] == "alive"
            ):
                GM.screen.blit(x["image"], (relative__left, relative__top))
            elif "stats" not in x["name"]:
                GM.screen.blit(x["image"], (relative__left, relative__top))

            if x["type"] == "container":
                GM.collision_map[
                    x["rect"].top + 10 : x["rect"].bottom - 9,
                    x["rect"].left + 10 : x["rect"].right - 9,
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

            if other_obj_rect.colliderect(GM.weapon_rect) and x["type"] == "npc":
                if GM.attacking:
                    if x["name"]["stats"]["type"] != "enemy":
                        GM.world_objects[index]["name"]["stats"]["type"] = "enemy"
                        GM.world_objects[index]["agroved"] = True

                    enemy_index = index
                    GM.world_objects[enemy_index]["name"]["stats"][
                        "health"
                    ] -= CM.player.stats.weapon_damage

                    if GM.world_objects[index]["name"]["stats"]["health"] <= 0:
                        CM.player.level.gain_experience(
                            GM.world_objects[index]["name"]["stats"]["xp"]
                        )
                        GM.world_objects[index]["name"]["stats"]["status"] = "dead"
                        GM.world_objects[index]["agroved"] = False
                        GM.world_objects.pop(index)

                if (
                    "stats" in GM.world_objects[index]["name"]
                    and GM.world_objects[index]["name"]["stats"]["type"] != "enemy"
                    and GM.world_objects[index]["name"]["stats"]["status"] != "dead"
                ):
                    text = prompt_font.render(
                        f"E) {GM.world_objects[index]['name']['name']}",
                        True,
                        (44, 53, 57),
                    )

                    text_rect = text.get_rect(
                        center=(
                            relative__left + x["rect"].width // 2,
                            relative__top - 10,
                        )
                    )
                    GM.talk_to_name = x["name"]["name"]
                    GM.screen.blit(text, text_rect)
                    GM.is_ready_to_talk = True

                elif (
                    not other_obj_rect.colliderect(GM.weapon_rect)
                    and x["type"] == "npc"
                ):
                    GM.talk_to_name = ""
                    GM.is_ready_to_talk = False

                if (
                    "stats" in GM.world_objects[index]["name"]
                    and GM.world_objects[index]["name"]["stats"]["health"] > 0
                    and GM.world_objects[index]["name"]["stats"]["type"] == "enemy"
                ):
                    text = prompt_font.render(
                        str(GM.world_objects[index]["name"]["stats"]["health"]),
                        True,
                        (200, 0, 0),
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
                and "stats" in GM.world_objects[index]["name"]
                and GM.world_objects[index]["name"]["stats"]["type"] != "enemy"
                and GM.world_objects[index]["name"]["stats"]["status"] != "dead"
            ):
                GM.is_ready_to_talk = False

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
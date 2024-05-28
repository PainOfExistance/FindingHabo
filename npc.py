import copy
import multiprocessing
import threading

import pygame

from colors import Colors
from game_manager import ClassManager as CM
from game_manager import GameManager as GM


def update_npc(subtitle_font, prompt_font):
    for index, x in enumerate(GM.npc_list):
        if GM.npc_list[index]["name"]["stats"]["status"] == "dead":
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
            GM.npc_list.pop(index)

    for index, x in enumerate(GM.npc_list):
        def worker(x, subtitle_font, prompt_font):
            if (
                not CM.menu.visible
                and not CM.player_menu.visible
            ):
                x = CM.ai.update(x)

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

                        GM.line=CM.ai.random_line(
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
                                res = other["name"]["stats"]["defense"] - \
                                    x["name"]["stats"]["damage"]
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
                                res = x["name"]["stats"]["defense"] - \
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
                other_obj_rect = pygame.Rect(
                    relative__left,
                    relative__top,
                    x["rect"].width,
                    x["rect"].height,
                )

                if not CM.player.player_rect.colliderect(other_obj_rect):
                    x = CM.ai.attack(x)
                    x["name"]["movement_behavior"]["moving"] = True

                if counter < len(GM.npc_list)-2:
                    x["agroved"] = True

                relative__left = int(GM.bg_rect.left + x["rect"].left)
                relative__top = int(GM.bg_rect.top + x["rect"].top)

                if CM.player.player_rect.colliderect(other_obj_rect):
                    agrov = True
                    if x["attack_diff"] > x["name"]["attack_speed"]:
                        res = CM.player.stats.defense - \
                            x["name"]["stats"]["damage"]

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
                relative__left = int(GM.bg_rect.left + x["rect"].left)
                relative__top = int(GM.bg_rect.top + x["rect"].top)
                x["name"]["movement_behavior"]["moving"] = True

                other_obj_rect = pygame.Rect(
                    relative__left,
                    relative__top,
                    x["rect"].width,
                    x["rect"].height,
                )

                GM.line=CM.ai.random_line(
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

                other_obj_rect = pygame.Rect(
                    relative__left,
                    relative__top,
                    x["rect"].width,
                    x["rect"].height,
                )

                if other_obj_rect.colliderect(GM.weapon_rect) and x["type"] == "npc":
                    if GM.attacking:
                        if x["name"]["stats"]["type"] != "enemy":
                            GM.npc_list[index]["name"]["stats"]["type"] = "enemy"
                            GM.npc_list[index]["agroved"] = True

                        GM.npc_list[index]["name"]["stats"][
                            "health"
                        ] -= (int(CM.player.stats.weapon_damage)-int(x["name"]["stats"]["defense"]))

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
                        text = prompt_font.render(
                            f"E) {GM.npc_list[index]['name']['name']}",
                            True,
                            Colors.mid_black,
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
        threads = []
        for npc in GM.npc_list:
            thread = threading.Thread(target=worker, args=(
                npc, subtitle_font, prompt_font))
            thread.start()
            threads.append(thread)

        # Wait for all threads to complete
        for thread in threads:
            thread.join()


def play_line(subtitle_font):
    if GM.line != None and GM.line_time < GM.counter:
        GM.current_line = GM.line
        GM.line_time = (
            CM.music_player.play_line(
                GM.current_line["file"]) + GM.counter
        )
    if GM.current_line != None and GM.line_time >= GM.counter:
        text = subtitle_font.render(
            GM.current_line["text"], True, Colors.mid_black
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
import pygame

import puzzle
from game_manager import ClassManager as CM
from game_manager import GameManager as GM


def update_npc(subtitle_font, prompt_font):
    for index, x in enumerate(GM.npc_list):
        if GM.npc_list[index]["name"]["stats"]["status"] == "dead":
            GM.npc_list.pop(index)
        
    for index, x in enumerate(GM.npc_list):
        relative__left = int(GM.bg_rect.left + x["rect"].left)
        relative__top = int(GM.bg_rect.top + x["rect"].top)
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

            GM.npc_list[index]["agroved"] = agroved
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
            
            other_obj_rect = pygame.Rect(
                relative__left,
                relative__top,
                x["rect"].width,
                x["rect"].height,
            )

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

                    enemy_index = index
                    GM.npc_list[enemy_index]["name"]["stats"][
                        "health"
                    ] -= CM.player.stats.weapon_damage

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
                    "stats" in GM.npc_list[index]["name"]
                    and GM.npc_list[index]["name"]["stats"]["health"] > 0
                    and GM.npc_list[index]["name"]["stats"]["type"] == "enemy"
                ):
                    text = prompt_font.render(
                        str(GM.npc_list[index]["name"]["stats"]["health"]),
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
                and "stats" in GM.npc_list[index]["name"]
                and GM.npc_list[index]["name"]["stats"]["type"] != "enemy"
                and GM.npc_list[index]["name"]["stats"]["status"] != "dead"
            ):
                GM.is_ready_to_talk = False
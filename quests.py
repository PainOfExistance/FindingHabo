import math

import numpy as np
import pygame


class Quests:
    def __init__(self, assets, inventory):
        self.quests = assets.load_quests()
        self.tics = 0
        self.text_to_draw = []
        self.items=inventory

    def advance_quest(self, id):
        for index, stages in enumerate(self.quests[id]["stages"]):
            if stages["objectives"]["state"] == 1:
                self.quests[id]["stages"][index]["objectives"]["state"] = 2
                if index < len(self.quests[id]["stages"]) - 1:
                    self.quests[id]["stages"][index + 1]["objectives"]["state"] = 1
                    self.text_to_draw.clear()
                    self.text_to_draw.append(self.quests[id]["name"])
                    self.text_to_draw.append(
                        "◇" + self.quests[id]["stages"][index + 1]["description"]
                    )
                    self.tics = pygame.time.get_ticks()
                    return
                elif index == len(self.quests[id]["stages"]) - 1:
                    self.end_quest(id)
                    self.tics = pygame.time.get_ticks()
                    return


    def start_quest(self, id):
        self.quests[id]["started"] = True
        self.quests[id]["stages"][0]["objectives"]["state"] = 1
        self.text_to_draw.clear()
        self.text_to_draw.append("Started: " + self.quests[id]["name"])
        self.text_to_draw.append("◇" + self.quests[id]["stages"][0]["description"])
        self.tics = pygame.time.get_ticks()

    def end_quest(self, id):
        self.quests[id]["started"] = "finished"
        self.text_to_draw.clear()
        self.text_to_draw.append("Completed: " + self.quests[id]["name"])
        self.tics = pygame.time.get_ticks()

    def draw_quest_info(self, screen):
        if pygame.time.get_ticks() - self.tics <= 5000:
            quest_start_font = pygame.font.Font("game_data/inter.ttf", 32)
            for index, v in enumerate(self.text_to_draw):
                item_render = quest_start_font.render(v, True, (44, 53, 57))
                item_rect = item_render.get_rect(
                    center=(screen.get_width() // 2, 200 + index * 40)
                )
                screen.blit(item_render, item_rect)

    def check_quest_advancement(self, quest_objective, world="default"):
        for index, (kv, quest) in enumerate(self.quests.items()):
            if quest["started"]:
                for stage in quest["stages"]:
                    if "radius" in stage["objectives"] and stage["objectives"]["state"] == 1:
                        if stage["objectives"]["world"] == world:
                            distance = math.dist(
                                tuple(stage["objectives"]["possition"]), quest_objective
                            )
                            if (
                                distance <= stage["objectives"]["radius"]
                                and stage["objectives"]["state"] == 1
                            ):
                                self.advance_quest(kv)
                                
                    elif "inventory" in stage["objectives"] and stage["objectives"]["state"] == 1 and stage["objectives"]["inventory"]:
                        self.advance_quest(kv)
                            
                    elif "items" in stage["objectives"] and stage["objectives"]["state"] == 1:
                        for items in stage["objectives"]["items"]:
                            
                            self.advance_quest(kv)     
                        

    def draw(self, screen, selected_sub_item, sub_items):
        quests_font = pygame.font.Font("game_data/inter.ttf", 24)
        item_spacing = 30
        i = 0
        coords = (screen.get_width() + screen.get_width() // 4) / 2

        scroll_position = (selected_sub_item // 5) * 5
        visible_quests = list(self.quests.items())[
            scroll_position : scroll_position + 5
        ]
        for index, (quest_index, quest_data) in enumerate(visible_quests):
            if quest_data["started"]:
                color = (
                    (157, 157, 210)
                    if index == selected_sub_item - scroll_position
                    else (237, 106, 94)
                    if sub_items
                    else (120, 120, 120)
                )

                quest_text = f"{quest_data['name']}"
                item_render = quests_font.render(quest_text, True, color)
                item_rect = item_render.get_rect(center=(coords, 20 + index * 40 + i))
                screen.blit(item_render, item_rect)

                if index == selected_sub_item - scroll_position:
                    i += item_spacing
                    line_render = quests_font.render(
                        quest_data["description"], True, color
                    )
                    line_rect = line_render.get_rect(
                        center=(coords, 20 + index * 40 + i)
                    )
                    screen.blit(line_render, line_rect)
                    i += item_spacing

                    for stage in quest_data["stages"]:
                        if (
                            stage["objectives"]["state"] in (1, 2)
                            and quest_data["active"]
                        ):
                            if stage["objectives"]["state"] == 2:
                                stage_text = f"◆{stage['description']}"
                            elif stage["objectives"]["state"] == 1:
                                stage_text = f"◇{stage['description']}"

                            stage_render = quests_font.render(stage_text, True, color)
                            stage_rect = stage_render.get_rect(
                                center=(coords, 20 + index * 40 + i)
                            )
                            screen.blit(stage_render, stage_rect)
                            i += item_spacing

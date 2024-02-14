import math

import numpy as np
import pygame

from game_manager import ClassManager as CM
from game_manager import GameManager as GM


class Quests:
    def __init__(self):
        self.quests = CM.assets.load_quests()
        self.tics = 0
        self.text_to_draw = []
        self.dialogue=None
        self.quests_font = pygame.font.Font("fonts/SovngardeBold.ttf", 28)
        self.quest_start_font = pygame.font.Font("fonts/SovngardeBold.ttf", 36)

    def advance_quest(self, id):
        for index, stages in enumerate(self.quests[id]["stages"]):
            if stages["objectives"]["state"] == 1:
                if "rmitems" in stages["objectives"]:
                    for items in stages["objectives"]["rmitems"]:
                        CM.inventory.items[items["name"]]["dropable"]=True
                        for x in range(items["quantity"]):
                            CM.inventory.remove_item(items["name"])
                            
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
        
    def check_quest_state(self, id):
        if self.quests[id]["started"] == "finished":
            return "finished"
        elif self.quests[id]["started"]:
            return "started"
        else:
            return "not started"

    def draw_quest_info(self):
        if pygame.time.get_ticks() - self.tics <= 5000:
            for index, v in enumerate(self.text_to_draw):
                item_render = self.quest_start_font.render(v, True, (44, 53, 57))
                item_rect = item_render.get_rect(
                    center=(GM.screen.get_width() // 2, 200 + index * 40)
                )
                GM.screen.blit(item_render, item_rect)

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
                        tmp=list()
                        for items in stage["objectives"]["items"]:
                            for key in CM.inventory.quantity:
                                if key == items["name"] and CM.inventory.quantity[key] >= items["quantity"]:
                                    tmp.append(key)
                        
                        if len(tmp) == len(stage["objectives"]["items"]):
                            for key in tmp:
                                CM.inventory.items[key]["dropable"]=False
                            self.advance_quest(kv)     
                    
                    elif "npc" in stage["objectives"] and stage["objectives"]["state"] == 1:
                        self.dialogue.strings[stage["objectives"]["npc"]]["options"][stage["objectives"]["option"]]["used"] = True
    
    def to_dict(self):
        return {
            "quests": self.quests,
            "tics": self.tics,
            "text_to_draw": self.text_to_draw,
        }

    def from_dict(self, data):
        fixed={int(key): value for key, value in data["quests"].items()}
        self.quests = fixed
        self.tics = -5000#data["tics"]
        self.text_to_draw = data["text_to_draw"]
                        
    def draw(self, selected_sub_item, sub_items):
        item_spacing = 30
        i = 0
        coords = (GM.screen.get_width() + GM.screen.get_width() // 4) / 2

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
                item_render = self.quests_font.render(quest_text, True, color)
                item_rect = item_render.get_rect(center=(coords, 20 + index * 40 + i))
                GM.screen.blit(item_render, item_rect)

                if index == selected_sub_item - scroll_position:
                    i += item_spacing
                    line_render = self.quests_font.render(
                        quest_data["description"], True, color
                    )
                    line_rect = line_render.get_rect(
                        center=(coords, 20 + index * 40 + i)
                    )
                    GM.screen.blit(line_render, line_rect)
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

                            stage_render = self.quests_font.render(stage_text, True, color)
                            stage_rect = stage_render.get_rect(
                                center=(coords, 20 + index * 40 + i)
                            )
                            GM.screen.blit(stage_render, stage_rect)
                            i += item_spacing

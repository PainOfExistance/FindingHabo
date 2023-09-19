import numpy as np
import pygame


class Quests:
    def __init__(self, assets):
        self.quests=assets.load_quests()

    def advance_quest(self, id):
        pass

    def start_quest(self, id):
        pass

    def end_quest(self, id):
        pass
    
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
                        if stage["objectives"]["state"] in (1,2):
                            if stage["objectives"]["state"]==2:
                                stage_text = f"◆{stage['description']}"
                            elif stage["objectives"]["state"]==1:
                                stage_text = f"◇{stage['description']}"
                                
                            stage_render = quests_font.render(stage_text, True, color)
                            stage_rect = stage_render.get_rect(
                                center=(coords, 20 + index * 40 + i)
                            )
                            screen.blit(stage_render, stage_rect)
                            i += item_spacing

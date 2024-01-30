import numpy as np
import pygame

from game_manager import ClassManager as CM
from game_manager import GameManager as GM


class Effects:
    def __init__(self):
        self.effects = CM.assets.load_effects()
        self.effects_font = pygame.font.Font("fonts/SovngardeBold.ttf", 28)

    def draw(self, selected_sub_item, sub_items):
        item_spacing = 30
        i = 0
        coords = (GM.screen.get_width() + GM.screen.get_width() // 4) / 2

        scroll_position = (selected_sub_item // 5) * 5
        visible_effects = list(self.effects.items())[
            scroll_position : scroll_position + 5
        ]
        for index, (effect_name, effect_data) in enumerate(visible_effects):
            if effect_data["amount"] >= 0:
                color = (
                    (157, 157, 210)
                    if index == selected_sub_item - scroll_position
                    else (237, 106, 94)
                    if sub_items
                    else (120, 120, 120)
                )
                
                effect_text = f"{effect_data['name']}"
                item_render = self.effects_font.render(effect_text, True, color)
                item_rect = item_render.get_rect(center=(coords, 20 + index * 40 + i))
                GM.screen.blit(item_render, item_rect)
                
                if index == selected_sub_item - scroll_position:
                    i += item_spacing
                    line_render = self.effects_font.render(
                        effect_data["description"], True, color
                    )
                    line_rect = line_render.get_rect(
                        center=(coords, 20 + index * 40 + i)
                    )
                    GM.screen.blit(line_render, line_rect)
                i += item_spacing
                
                amount_text = f"Effect amount: {effect_data['amount']}"
                amount_render = self.effects_font.render(amount_text, True, color)
                amount_rect = amount_render.get_rect(
                    center=(coords, 20 + index * 40 + i)
                )
                GM.screen.blit(amount_render, amount_rect)
                i += item_spacing

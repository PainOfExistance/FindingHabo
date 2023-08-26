import numpy as np
import pygame

class Effects:
    def __init__(self, assets):
        self.effects = assets.load_effects()

    def draw(self, screen, selected_sub_item, sub_items):
        effects_font = pygame.font.Font("game_data/inter.ttf", 24)
        scroll_position = (selected_sub_item // 15) * 15
        visible_items = list(self.effects.items())[
            scroll_position : scroll_position + 15
        ]
        for index, (effect_name, effect_data) in enumerate(visible_items):
            color = (
                (157, 157, 210)
                if index == selected_sub_item - scroll_position
                else (237, 106, 94)
                if sub_items
                else (120, 120, 120)
            )
            if index == selected_sub_item - scroll_position:
                item_text = f"> {effect_name}  desc: {effect_data['description']}  Current effect amount: {effect_data['amount']}"
            else:
                item_text = f"    {effect_name}  desc: {effect_data['description']}  Current effect amount: {effect_data['amount']}"
            item_render = effects_font.render(item_text, True, color)
            item_rect = item_render.get_rect(topleft=(220, 20 + index * 40))
            screen.blit(item_render, item_rect)

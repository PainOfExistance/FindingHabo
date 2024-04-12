import numpy as np
import pygame

from colors import Colors
from game_manager import ClassManager as CM
from game_manager import GameManager as GM
from traits import Traits


class LevelingSystem:
    def __init__(self):
        self.level = 1
        self.experience = 0
        self.required_experience = 100
        self.traits = Traits()
        self.trait_font = pygame.font.Font("fonts/SovngardeBold.ttf", 28)

    def gain_experience(self, amount):
        self.experience += amount
        while self.experience >= self.required_experience:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.traits.unused_trait_points += 2
        self.experience -= self.required_experience
        self.required_experience = self.calculate_next_required_experience(self.level)

    def calculate_next_required_experience(self, current_level):
        base_experience = 100
        experience_increment = 50
        increment_multiplier = 1.1
        return int(
            base_experience
            + (experience_increment * (increment_multiplier ** (current_level - 2)))
        )
        #(75 x (Next Level - 1))+200 
    
    def to_dict(self):
        return {
            "level": self.level,
            "experience": self.experience,
            "required_experience": self.required_experience,
            "traits": self.traits.to_dict(),
        }

    def from_dict(self, data):
        self.level = data["level"]
        self.experience = data["experience"]
        self.required_experience = data["required_experience"]
        self.traits.from_dict(data["traits"])

    def draw(self, selected_sub_item, sub_items, trait_selection):
        item_spacing = 30
        i = 0
        coords = (GM.screen.get_width() + GM.screen.get_width() // 4) / 2

        scroll_position = (selected_sub_item // 4) * 4
        selected = (trait_selection // 4) * 4
        visible_traits = list(self.traits.traits.items())[
            scroll_position : scroll_position + 4
        ]
        for index, (trait_name, trait_data) in enumerate(visible_traits):
            color = (
                Colors.active_item
                if index == selected_sub_item - scroll_position
                else Colors.inactive_item
                if sub_items
                else Colors.unselected_item
            )

            trait_text = f"{trait_name}"
            item_render = self.trait_font.render(trait_text, True, color)
            item_rect = item_render.get_rect(center=(coords, 20 + index * 40 + i))
            GM.screen.blit(item_render, item_rect)

            if index == selected_sub_item - scroll_position:
                i += item_spacing
                line_render = self.trait_font.render(trait_data["description"], True, color)
                line_rect = line_render.get_rect(center=(coords, 20 + index * 40 + i))
                GM.screen.blit(line_render, line_rect)
            i += item_spacing

            level_text = f""
            clr = (157, 157, 210)

            for level_info in trait_data["levels"]:
                if not level_info["taken"]:
                    if level_info["level"] <= self.level:
                        clr = Colors.green
                    else:
                        clr = Colors.red

                    if trait_selection - selected == index and trait_selection != -1:
                        level_text = f"Unlock this level?"
                    else:
                        level_text = f"Next unlock at: {level_info['level']}  Gain: {level_info['effect']}"
                    break

                clr = Colors.active_item#(120, 120, 200)
                level_text = f"Next unlock at: MAX  Value amount: MAX"

            taken_text = "Taken:"
            for level_info in trait_data["levels"]:
                taken_text += f" {'O' if not level_info['taken'] else 'Ø':<2}"

            level_render = self.trait_font.render(level_text, True, clr)
            taken_render = self.trait_font.render(taken_text, True, color)

            level_rect = level_render.get_rect(
                center=(coords, 20 + index * 40 + i + item_spacing)
            )
            taken_rect = taken_render.get_rect(center=(coords, 20 + index * 40 + i))
            GM.screen.blit(taken_render, taken_rect)
            GM.screen.blit(level_render, level_rect)
            i += 2.5 * item_spacing

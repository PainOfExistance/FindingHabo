import pygame
import numpy as np
import random


class Dialougue:
    def __init__(self, assets, ai, screen):
        self.strings = assets.load_dialogue()
        self.ai = ai
        self.screen = screen
        self.subtitle_font = pygame.font.Font("game_data/inter.ttf", 24)
        self.option_font = pygame.font.Font("game_data/inter.ttf", 20)
        self.index = -1
        self.selection_held = False

    def random_line(self, name):
        current_string = {"text": "", "dialogue": False, "file": ""}
        index = random.randint(0, len(self.strings[name]["random"]) - 1)
        line = self.strings[name]["random"][index]
        line_file = self.strings[name]["random_file"][index]
        current_string["text"] = name + ": " + line
        current_string["file"] = line_file

        return current_string

    def draw(self, name):
        if self.index == -1:
            enabled = self.strings[name]["options"][self.strings[name]["enables"][0]:self.strings[name]["enables"][1]+1]
            for i, value in enumerate(enabled):
                text = self.option_font.render(
                    value["text"], True, (44, 53, 57)
                )
                text_rect = text.get_rect(
                    center=(
                        self.screen.get_width() // 2,
                        self.screen.get_height() - 140 + i * 35,
                    )
                )
                self.screen.blit(text, text_rect)

            text = self.subtitle_font.render(
                f"{name}: {self.strings[name]['greeting']}", True, (44, 53, 57)
            )
            text_rect = text.get_rect(
                center=(
                    self.screen.get_width() // 2,
                    self.screen.get_height() - 200,
                )
            )
            self.screen.blit(text, text_rect)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if not self.selection_held:
            if (
                keys[pygame.K_UP]
                and not self.selection_held
            ):
                if not self.sub_items:
                    self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                elif len(self.player.inventory.items) > 0 and self.selected_item == 0:
                    self.selected_sub_item = (self.selected_sub_item - 1) % len(
                        self.player.inventory.items
                    )
                elif self.selected_item == 1:
                    self.selected_sub_item = (self.selected_sub_item - 1) % len(
                        self.player.level.traits.traits
                    )
                elif self.selected_item == 2:
                    self.selected_sub_item = (self.selected_sub_item - 1) % len(
                        self.player.effects.effects
                    )
                self.selection_held = True

            elif (
                keys[pygame.K_DOWN]
                and not self.selection_held
            ):
                if not self.sub_items:
                    self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                elif len(self.player.inventory.items) > 0 and self.selected_item == 0:
                    self.selected_sub_item = (self.selected_sub_item + 1) % len(
                        self.player.inventory.items
                    )
                elif self.selected_item == 1:
                    self.selected_sub_item = (self.selected_sub_item + 1) % len(
                        self.player.level.traits.traits
                    )
                elif self.selected_item == 2:
                    self.selected_sub_item = (self.selected_sub_item + 1) % len(
                        self.player.effects.effects
                    )
                self.selection_held = True

        elif (
            not keys[pygame.K_UP]
            and not keys[pygame.K_DOWN]
            and not keys[pygame.K_RIGHT]
            and not keys[pygame.K_LEFT]
            and not keys[pygame.K_RETURN]
        ):
            self.selection_held = False
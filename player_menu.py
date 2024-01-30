import re
import sys

import pygame

from game_manager import ClassManager as CM
from game_manager import GameManager as GM


class PlayerMenu:
    def __init__(self):
        self.visible = False
        self.menu_items = ["Items", "Traits", "Effects", "Quests"]
        self.selected_item = 0
        self.selected_sub_item = 0
        self.sub_items = False
        self.tab_held = False
        self.selection_held = False
        self.inventory_visible = False
        self.trait_selection = -1
        
        self.menu_font = pygame.font.Font("fonts/SovngardeBold.ttf", 34)
        self.stats_font = pygame.font.Font("fonts/SovngardeBold.ttf", 22)

        self.bg = pygame.Rect(
            0, 0, GM.screen.get_width() // 4, GM.screen.get_height()
        )
        self.bg_surface = pygame.Surface(
            (self.bg.width, self.bg.height), pygame.SRCALPHA
        )

        self.bg_menu = pygame.Rect(
            GM.screen.get_width() // 4,
            0,
            GM.screen.get_width() - (GM.screen.get_width() // 4),
            GM.screen.get_height(),
        )
        self.bg_surface_menu = pygame.Surface(
            (self.bg_menu.width, self.bg_menu.height), pygame.SRCALPHA
        )

        self.stats = [
            f"Health: {CM.player.stats.health}/{CM.player.stats.max_health}",
            f"Power: {CM.player.stats.power}/{CM.player.stats.max_power}",
            f"Knowledge: {CM.player.stats.knowlage}/{CM.player.stats.max_knowlage}",
        ]

    def toggle_visibility(self):
        self.visible = not self.visible

    def handle_input(self):
        
        num_started_quests = sum(1 for quest in CM.player.quests.quests
                        if CM.player.quests.quests[quest]["started"]
                    )
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_TAB]:
            if self.trait_selection != -1 and not self.tab_held:
                self.trait_selection = -1
            elif not self.tab_held:
                self.toggle_visibility()
                self.stats = [
                    f"Health: {CM.player.stats.health}/{CM.player.stats.max_health}",
                    f"Power: {CM.player.stats.power}/{CM.player.stats.max_power}",
                    f"Knowledge: {CM.player.stats.knowlage}/{CM.player.stats.max_knowlage}",
                ]
            self.tab_held = True
        else:
            self.tab_held = False

        if self.visible and not self.selection_held:
            if (
                keys[pygame.K_UP]
                and not self.selection_held
                and self.trait_selection == -1
            ):
                if not self.sub_items:
                    self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                elif len(CM.inventory.items) > 0 and self.selected_item == 0:
                    self.selected_sub_item = (self.selected_sub_item - 1) % len(
                        CM.inventory.items
                    )
                elif self.selected_item == 1:
                    self.selected_sub_item = (self.selected_sub_item - 1) % len(
                        CM.player.level.traits.traits
                    )
                elif self.selected_item == 2:
                    self.selected_sub_item = (self.selected_sub_item - 1) % len(
                        CM.player.effects.effects
                    )
                elif num_started_quests>0 and self.selected_item == 3:
                    self.selected_sub_item = (
                        self.selected_sub_item - 1
                    ) % num_started_quests

                if self.selected_sub_item < 0:
                    self.selected_sub_item = 0
                self.selection_held = True

            elif (
                keys[pygame.K_DOWN]
                and not self.selection_held
                and self.trait_selection == -1
            ):
                if not self.sub_items:
                    self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                elif len(CM.inventory.items) > 0 and self.selected_item == 0:
                    self.selected_sub_item = (self.selected_sub_item + 1) % len(
                        CM.inventory.items
                    )
                elif self.selected_item == 1:
                    self.selected_sub_item = (self.selected_sub_item + 1) % len(
                        CM.player.level.traits.traits
                    )
                elif self.selected_item == 2:
                    self.selected_sub_item = (self.selected_sub_item + 1) % len(
                        CM.player.effects.effects
                    )
                elif num_started_quests>0 and self.selected_item == 3:
                    self.selected_sub_item = (
                        self.selected_sub_item + 1
                    ) % num_started_quests

                if self.selected_sub_item < 0:
                    self.selected_sub_item = 0
                self.selection_held = True

            elif (
                (keys[pygame.K_RIGHT] or keys[pygame.K_RETURN])
                and not self.sub_items
                and self.trait_selection == -1
            ):
                self.sub_items = True
                self.selection_held = True

            elif keys[pygame.K_LEFT] and self.sub_items and self.trait_selection == -1:
                self.sub_items = False
                self.selected_sub_item = 0
                self.selection_held = True

            elif keys[pygame.K_RETURN] and self.sub_items:
                if self.selected_item == 0 and len(CM.inventory.items) > 0:
                    CM.player.use_item(self.selected_sub_item)
                    self.stats = [
                        f"Health: {CM.player.stats.health}/{CM.player.stats.max_health}",
                        f"Power: {CM.player.stats.power}/{CM.player.stats.max_power}",
                        f"Knowledge: {CM.player.stats.knowlage}/{CM.player.stats.max_knowlage}",
                    ]
                elif self.selected_item == 1:
                    if (
                        self.trait_selection != -1
                        and CM.player.level.traits.unused_trait_points > 0
                        and CM.player.check_trait_conditions(self.selected_sub_item)
                    ):
                        CM.player.add_trait(self.selected_sub_item)
                        self.trait_selection = -1
                        self.stats = [
                            f"Health: {CM.player.stats.health}/{CM.player.stats.max_health}",
                            f"Power: {CM.player.stats.power}/{CM.player.stats.max_power}",
                            f"Knowledge: {CM.player.stats.knowlage}/{CM.player.stats.max_knowlage}",
                        ]
                    elif (
                        CM.player.level.traits.unused_trait_points > 0
                        and CM.player.check_trait_conditions(self.selected_sub_item)
                        and self.trait_selection == -1
                    ):
                        self.trait_selection = self.selected_sub_item
                elif self.selected_item == 3 and num_started_quests>0:
                    keys_list = list(CM.player.quests.quests.keys())
                    CM.player.quests.quests[keys_list[self.selected_sub_item]]["active"] = not CM.player.quests.quests[keys_list[self.selected_sub_item]]["active"]
                    
                self.selection_held = True

        elif (
            not keys[pygame.K_UP]
            and not keys[pygame.K_DOWN]
            and not keys[pygame.K_RIGHT]
            and not keys[pygame.K_LEFT]
            and not keys[pygame.K_RETURN]
        ):
            self.selection_held = False

    def render(self):
        if self.visible:
            pygame.draw.rect(
                self.bg_surface, (200, 210, 200, 180), self.bg_surface.get_rect()
            )
            GM.screen.blit(self.bg_surface, self.bg)

            pygame.draw.rect(
                self.bg_surface_menu, (44, 44, 44, 200), self.bg_surface_menu.get_rect()
            )
            GM.screen.blit(self.bg_surface_menu, self.bg_menu)

            pygame.draw.line(
                GM.screen,
                (22, 22, 22),
                (GM.screen.get_width() // 4, 0),
                (GM.screen.get_width() // 4, GM.screen.get_height()),
                4,
            )

            for index, item in enumerate(self.menu_items):
                color = (
                    (44, 53, 57)
                    if index == self.selected_item
                    else (237, 106, 94)
                    if not self.sub_items
                    else (160, 160, 160)
                )

                text = self.menu_font.render(item, True, color)
                text_rect = text.get_rect(topleft=(20, 20 + index * 40))
                GM.screen.blit(text, text_rect)
                text_y = GM.screen.get_height() - 140

                for stat in self.stats:
                    stat_render = self.stats_font.render(stat, True, (44, 53, 57))
                    stat_rect = stat_render.get_rect(bottomleft=(20, text_y))
                    GM.screen.blit(stat_render, stat_rect)
                    text_y += stat_rect.height + 5

                level = self.stats_font.render(
                    f"Level: {str(CM.player.level.level)}", True, (44, 53, 57)
                )
                level_rect = level.get_rect(bottomleft=(20, text_y))
                GM.screen.blit(level, level_rect)
                text_y += level_rect.height + 5

                level = self.stats_font.render(
                    f"Unused points: {str(CM.player.level.traits.unused_trait_points)}",
                    True,
                    (44, 53, 57),
                )
                level_rect = level.get_rect(bottomleft=(20, text_y))
                GM.screen.blit(level, level_rect)
                text_y += level_rect.height + 5

                level = self.stats_font.render(
                    f"Gold: {str(CM.player.gold)}",
                    True,
                    (44, 53, 57),
                )
                level_rect = level.get_rect(bottomleft=(20, text_y))
                GM.screen.blit(level, level_rect)

            if self.selected_item == 0:
                CM.inventory.draw(
                    self.selected_sub_item, self.sub_items, GM.screen.get_width() // 4 + 20
                )
                if self.selected_sub_item > len(CM.inventory.items) - 1:
                    self.selected_sub_item -= 1
                elif self.selected_sub_item < 0:
                    self.selected_sub_item = 0

            elif self.selected_item == 1:
                CM.player.level.draw(
                    self.selected_sub_item,
                    self.sub_items,
                    self.trait_selection,
                )

            elif self.selected_item == 2:
                CM.player.effects.draw(
                    self.selected_sub_item, self.sub_items
                )

            elif self.selected_item == 3:
                CM.player.quests.draw(
                    self.selected_sub_item, self.sub_items
                )

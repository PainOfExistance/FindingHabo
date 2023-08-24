import pygame
import sys


class PlayerMenu:
    def __init__(self, screen, player):
        self.screen = screen
        self.visible = False
        self.menu_items = ["Weapons", "Items", "Effects", "Data"]
        self.selected_item = 0
        self.selected_sub_item = 0
        self.sub_items = False
        self.tab_held = False
        self.selection_held = False
        self.inventory_visible = False
        self.player = player

        self.bg = pygame.Rect(
            0, 0, self.screen.get_width() // 4, self.screen.get_height()
        )
        self.bg_surface = pygame.Surface(
            (self.bg.width, self.bg.height), pygame.SRCALPHA
        )

        self.bg_menu = pygame.Rect(
            self.screen.get_width() // 4,
            0,
            self.screen.get_width() - (self.screen.get_width() // 4),
            self.screen.get_height(),
        )
        self.bg_surface_menu = pygame.Surface(
            (self.bg_menu.width, self.bg_menu.height), pygame.SRCALPHA
        )

        self.stats = [
            f"Health: {self.player.stats.health}",
            f"Power: {self.player.stats.power}",
            f"Knowledge: {self.player.stats.knowlage}",
        ]

    def toggle_visibility(self):
        self.visible = not self.visible

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_TAB]:
            if not self.tab_held:
                self.toggle_visibility()
                self.tab_held = True
                self.stats = [
                    f"Health: {self.player.stats.health}",
                    f"Power: {self.player.stats.power}",
                    f"Knowledge: {self.player.stats.knowlage}",
                ]
        else:
            self.tab_held = False

        if self.visible and not self.selection_held:
            if keys[pygame.K_UP] and not self.selection_held:
                if not self.sub_items:
                    self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                else:
                    self.selected_sub_item = (self.selected_sub_item - 1) % len(
                        self.player.inventory.items
                    )
                self.selection_held = True

            elif keys[pygame.K_DOWN] and not self.selection_held:
                if not self.sub_items:
                    self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                else:
                    self.selected_sub_item = (self.selected_sub_item + 1) % len(
                        self.player.inventory.items
                    )
                self.selection_held = True

            elif keys[pygame.K_RIGHT] and not self.sub_items:
                self.sub_items = True
                self.selection_held = True

            elif keys[pygame.K_LEFT] and self.sub_items:
                self.sub_items = False
                self.selection_held = True

            elif keys[pygame.K_RETURN] and self.sub_items:
                self.player.use_item()
                self.selection_held = True

        elif (
            not keys[pygame.K_UP]
            and not keys[pygame.K_DOWN]
            and not keys[pygame.K_RIGHT]
            and not keys[pygame.K_LEFT]
            and not keys[pygame.K_RETURN]
        ):
            self.selection_held = False

    def render_inventory(self):
        inventory_font = pygame.font.Font("inter.ttf", 24)
        item_spacing = 40
        text_y = 20

        for index, (item_name, item_quantity) in enumerate(
            self.player.inventory.quantity.items()
        ):
            color = (
                (157, 157, 210)
                if index == self.selected_sub_item
                else (237, 106, 94)
                if self.sub_items
                else (120, 120, 120)
            )
            if index == self.selected_sub_item:
                item_text = f"> {item_name}: {item_quantity} desc: {self.player.inventory.items[item_name]['description']}"
            else:
                item_text = f"    {item_name}: {item_quantity} desc: {self.player.inventory.items[item_name]['description']}"

            item_render = inventory_font.render(item_text, True, color)
            item_rect = item_render.get_rect(topleft=(220, 20 + index * 40))
            self.screen.blit(item_render, item_rect)
            text_y += item_spacing

    def render(self):
        if self.visible:
            pygame.draw.rect(
                self.bg_surface, (200, 210, 200, 180), self.bg_surface.get_rect()
            )
            self.screen.blit(self.bg_surface, self.bg)

            pygame.draw.rect(
                self.bg_surface_menu, (44, 44, 44, 200), self.bg_surface_menu.get_rect()
            )
            self.screen.blit(self.bg_surface_menu, self.bg_menu)

            pygame.draw.line(
                self.screen,
                (22, 22, 22),
                (self.screen.get_width() // 4, 0),
                (self.screen.get_width() // 4, self.screen.get_height()),
                4,
            )

            menu_font = pygame.font.Font("inter.ttf", 30)
            stats_font = pygame.font.Font("inter.ttf", 18)

            for index, item in enumerate(self.menu_items):
                color = (
                    (44, 53, 57)
                    if index == self.selected_item
                    else (237, 106, 94)
                    if not self.sub_items
                    else (160, 160, 160)
                )

                text = menu_font.render(item, True, color)
                text_rect = text.get_rect(topleft=(20, 20 + index * 40))
                self.screen.blit(text, text_rect)
                text_y = self.screen.get_height() - 70

                for stat in self.stats:
                    stat_render = stats_font.render(stat, True, (44, 53, 57))
                    stat_rect = stat_render.get_rect(bottomleft=(20, text_y))
                    self.screen.blit(stat_render, stat_rect)
                    text_y += stat_rect.height + 5

            if self.selected_item == 1:
                self.render_inventory()

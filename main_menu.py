import glob
import os
import sys

import pygame

from asset_loader import AssetLoader
from game import Game
from menu import Menu
from player import Player
from player_menu import PlayerMenu


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.menu_items = ["Start", "Load", "Options", "Exit"]
        self.selected_item = 0
        self.selection_held = False
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.is_menu_visible = True
        self.in_sub_menu = 0
        saves = glob.glob(os.path.join("saves", "*.habo"))
        self.saves = [os.path.splitext(os.path.basename(filename))[0] for filename in saves]
        self.font = pygame.font.Font("fonts/SovngardeBold.ttf", 40)  

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and not self.selection_held:
            if self.in_sub_menu == 0:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif self.in_sub_menu == 1:
                self.selected_item = (self.selected_item - 1) % len(self.saves)
            self.selection_held = True

        elif keys[pygame.K_DOWN] and not self.selection_held:
            if self.in_sub_menu == 0:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif self.in_sub_menu == 1:
                self.selected_item = (self.selected_item + 1) % len(self.saves)
            self.selection_held = True

        elif keys[pygame.K_RETURN] and not self.selection_held:
            self.select_option()
            self.selection_held = True

        elif keys[pygame.K_TAB] and not self.selection_held:
            self.in_sub_menu = 0
            self.selection_held = True

        elif (
            not keys[pygame.K_UP]
            and not keys[pygame.K_DOWN]
            and not keys[pygame.K_RETURN]
            and not keys[pygame.K_TAB]
        ):
            self.selection_held = False

    def select_option(self):
        if self.in_sub_menu == 0:
            selected_option = self.menu_items[self.selected_item]
        elif self.in_sub_menu == 1:
            selected_option = self.saves[self.selected_item]

        if selected_option == "Start":
            print("Starting the game...")
            self.loading()

            surface = pygame.Surface((1080, 720))
            self.screen.blit(surface, (0, 0))
            surface.get_width()
            surface.get_height()
            #pygame.display.update()
            assets = AssetLoader(surface.get_width(), surface.get_height())
            player = Player(
                "textures/npc/desk1.png", surface.get_width(), surface.get_height(), assets
            )
            menu = Menu(surface, assets, player)
            player_menu = PlayerMenu(surface, player)
            game = Game(
                self.screen,
                surface,
                surface.get_width(),
                surface.get_height(),
                menu,
                player_menu,
                player,
                assets,
            )
            
            self.is_menu_visible = False
            game.run()
        elif selected_option == "Load" and len(self.saves) > 0:
            print("Opening load menu...")
            self.in_sub_menu = 1
            # Add your options menu logic here
        elif selected_option == "Options":
            print("Opening options menu...")
            self.in_sub_menu = 2
            # Add your options menu logic here
        elif selected_option == "Exit":
            pygame.quit()
            sys.exit()
        elif self.in_sub_menu == 1:
            assets = AssetLoader(self.screen_width, self.screen_height)
            game=assets.load(f"saves/{selected_option}.habo")
            self.is_menu_visible = False
            game.run()

    def render(self):
        if self.in_sub_menu == 0:
            for index, item in enumerate(self.menu_items):
                color = (0, 0, 0) if index == self.selected_item else (180, 180, 180)
                
                if (
                    self.selected_item == 1
                    and len(self.saves) == 0
                    and index == self.selected_item
                ):
                    color = (100, 100, 100)
                    
                text = self.font.render(item, True, color)
                text_rect = text.get_rect(
                    center=(
                        self.screen.get_width() // 2,
                        self.screen.get_height() // 2.5 + index * 50,
                    )
                )
                self.screen.blit(text, text_rect)

        elif self.in_sub_menu == 1:
            scroll_position = (self.selected_item // 6) * 6
            visible_saves = list(self.saves)[scroll_position : scroll_position + 6]
            
            for index, save in enumerate(visible_saves):
                color = (
                    (0, 0, 0)
                    if index == self.selected_item - scroll_position
                    else (180, 180, 180)
                )

                if index == self.selected_item - scroll_position:
                    save_text = f"> {save}"
                else:
                    save_text = f"  {save}"
                item_render = self.font.render(save_text, True, color)
                item_rect = item_render.get_rect(
                    center=(
                        self.screen.get_width() // 2,
                        self.screen.get_height() // 4 + index * 50,
                    )
                )
                self.screen.blit(item_render, item_rect)

    def loading(self):
        text = self.font.render("Loading...", True, (180, 180, 180))
        text_rect = text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2.5)
        )
        self.screen.blit(text, text_rect)

    def run(self):
        while self.is_menu_visible:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_menu_visible = False

            self.screen.fill((255, 255, 255))
            self.handle_input()
            self.render()
            pygame.display.flip()

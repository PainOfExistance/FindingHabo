import glob
import os
import sys

import pygame

import asset_loader as assets
from ai import Ai
from colors import Colors
from game import Game
from game_manager import ClassManager as CM
from game_manager import GameManager as GM
from level_list import LevelList
from menu import Menu
from music_player import MusicPlayer
from player import Player
from player_menu import PlayerMenu


class MainMenu:
    def __init__(self):
        self.menu_items = ["Start", "Load", "Options", "Exit"]
        self.selected_item = 0
        self.selection_held = False
        GM.screen_width = GM._scr.get_width()
        GM.screen_height = GM._scr.get_height()
        self.is_menu_visible = True
        self.in_sub_menu = 0
        saves = glob.glob(os.path.join("./saves", "*.habo"))
        self.saves = [os.path.splitext(os.path.basename(filename))[0] for filename in saves[::-1]]
        self.font = pygame.font.Font("./fonts/SovngardeBold.ttf", 40)  
        CM.music_player = MusicPlayer("./sounds/bgm/DOVAHKIIN.mp3")
        CM.music_player.play_random_track()
        self.logo, self.logo_rect = assets.load_images("./textures/logo.png", (int((GM.screen_height)*0.8), GM.screen_height), (GM.screen_width // 3, (GM.screen_height // 2)-25))

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and not self.selection_held:
            CM.music_player.play_effect("hover")
            if self.in_sub_menu == 0:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif self.in_sub_menu == 1:
                self.selected_item = (self.selected_item - 1) % len(self.saves)
            self.selection_held = True

        elif keys[pygame.K_DOWN] and not self.selection_held:
            CM.music_player.play_effect("hover")
            if self.in_sub_menu == 0:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif self.in_sub_menu == 1:
                self.selected_item = (self.selected_item + 1) % len(self.saves)
            self.selection_held = True

        elif keys[pygame.K_RETURN] and not self.selection_held:
            CM.music_player.play_effect("select")
            self.select_option()
            self.selection_held = True

        elif keys[pygame.K_TAB] and not self.selection_held:
            CM.music_player.play_effect("back")
            self.in_sub_menu = 0
            self.selection_held = True
        
        elif keys[pygame.K_r] and not self.selection_held and len(self.saves) > 0:
            CM.music_player.play_effect("select")
            selected_option = self.saves[self.selected_item]
            os.remove(f"./saves/{selected_option}.habo")
            saves = glob.glob(os.path.join("./saves", "*.habo"))
            self.saves = [os.path.splitext(os.path.basename(filename))[0] for filename in saves[::-1]]
            self.selection_held = True

        elif (
            not keys[pygame.K_UP]
            and not keys[pygame.K_DOWN]
            and not keys[pygame.K_RETURN]
            and not keys[pygame.K_TAB]
            and not keys[pygame.K_r]
        ):
            self.selection_held = False

    def select_option(self):
        if self.in_sub_menu == 0:
            selected_option = self.menu_items[self.selected_item]
        elif self.in_sub_menu == 1 and len(self.saves) > 0:
            selected_option = self.saves[self.selected_item]

        if selected_option == "Start":
            print("Starting the game...")
            self.loading()

            GM._scr.blit(GM.screen, (0, 0))
            GM.screen_width = GM.screen.get_width()
            GM.screen_height = GM.screen.get_height()
            #pygame.display.update()
            
            CM.player = Player()
            CM.level_list=LevelList()
            CM.menu = Menu()
            CM.player_menu = PlayerMenu()
            CM.ai = Ai()
            CM.game = Game()
            
            self.is_menu_visible = False
            CM.game.run()
        elif selected_option == "Load" and len(self.saves) > 0:
            print("Opening load menu...")
            self.in_sub_menu = 1
            self.selected_item = 0
        elif selected_option == "Options":
            print("Opening options menu...")
            self.in_sub_menu = 2
            self.selected_item = 0
            # Add your options menu logic here
        elif selected_option == "Exit":
            pygame.quit()
            sys.exit()
        elif self.in_sub_menu == 1:
            self.loading()
            
            GM._scr.blit(GM.screen, (0, 0))
            GM.screen_width = GM.screen.get_width()
            GM.screen_height = GM.screen.get_height()
            #pygame.display.update()
            
            CM.player = Player()
            CM.level_list=LevelList()
            CM.ai = Ai()
            GM.save_name=f"{selected_option}.habo"
            CM.player.from_dict(assets.load(f"saves/{selected_option}.habo"))
            CM.menu = Menu()
            CM.player_menu = PlayerMenu()
            CM.game = Game()
            
            self.is_menu_visible = False
            CM.game.run()

    def render(self):
        if self.in_sub_menu == 0:
            for index, item in enumerate(self.menu_items):
                color = Colors.active_item if index == self.selected_item else Colors.inactive_item
                
                if (
                    self.selected_item == 1
                    and len(self.saves) == 0
                    and index == self.selected_item
                ):
                    color = Colors.unselected_item
                    
                text = self.font.render(item, True, color)
                text_rect = text.get_rect(
                    center=(
                        (GM._scr.get_width() // 2)+(GM._scr.get_width() // 4),
                        GM._scr.get_height() // 2.5 + index * 50,
                    )
                )
                GM._scr.blit(text, text_rect)
                GM._scr.blit(self.logo, self.logo_rect)

        elif self.in_sub_menu == 1:
            
            item_render = self.font.render(f"ENTER) Load     R) Delete", True, Colors.active_item)
            item_rect = item_render.get_rect(
                    center=(
                        GM.screen.get_width() // 2,
                        50,
                    )
                )
            GM._scr.blit(item_render, item_rect)
        
            scroll_position = (self.selected_item // 6) * 6
            visible_saves = list(self.saves)[scroll_position : scroll_position + 6]
            
            for index, save in enumerate(visible_saves):
                color = (
                    Colors.active_item
                    if index == self.selected_item - scroll_position
                    else Colors.inactive_item
                )

                if index == self.selected_item - scroll_position:
                    save_text = f"> {save}"
                else:
                    save_text = f"  {save}"
                item_render = self.font.render(save_text, True, color)
                item_rect = item_render.get_rect(
                    center=(
                        GM._scr.get_width() // 2,
                        GM._scr.get_height() // 4 + index * 50,
                    )
                )
                GM._scr.blit(item_render, item_rect)

    def loading(self):
        text = self.font.render("Loading...", True, Colors.edge_color)
        text_rect = text.get_rect(
            center=(GM._scr.get_width() // 2, GM._scr.get_height() // 2.5)
        )
        GM._scr.blit(text, text_rect)
        pygame.display.flip()

    def run(self):
        while self.is_menu_visible:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_menu_visible = False
                                
                if event.type == pygame.USEREVENT:
                    CM.music_player.update()

            GM._scr.fill(Colors.dark_black)
            self.handle_input()
            self.render()
            pygame.display.flip()

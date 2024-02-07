import glob
import os
import sys
from datetime import datetime

import pygame

from game_manager import ClassManager as CM
from game_manager import GameManager as GM


class Menu:
    def __init__(self):
        self.visible = False
        self.menu_items = ["Continue", "Save and Load", "Options", "Exit"]
        self.selected_item = 0
        self.m_key_held = False
        self.selection_held = False
        self.in_sub_menu = 0
        saves = glob.glob(os.path.join("saves", "*.habo"))
        self.saves = [os.path.splitext(os.path.basename(filename))[0] for filename in saves]
        self.action="Save"
        self.game=None
        self.menu_font = pygame.font.Font("fonts/SovngardeBold.ttf", 40)   
        self.bg_menu = pygame.Rect(
            0,
            0,
            GM.screen.get_width(),
            GM.screen.get_height(),
        )

        self.bg_surface_menu = pygame.Surface(
            (self.bg_menu.width, self.bg_menu.height), pygame.SRCALPHA
        )

    def toggle_visibility(self):
        self.visible = not self.visible
        saves = glob.glob(os.path.join("saves", "*.habo"))
        self.saves = [os.path.splitext(os.path.basename(filename))[0] for filename in saves]

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            if not self.m_key_held:
                self.toggle_visibility()
                self.m_key_held = True
        else:
            self.m_key_held = False

        if self.visible and not self.selection_held:
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
                if self.in_sub_menu==1:
                    self.action="Save"
                self.selection_held = True
                self.select_option()

            elif keys[pygame.K_TAB] and not self.selection_held:
                self.action=""
                self.in_sub_menu = 0
                self.selection_held = True
            
            elif keys[pygame.K_e] and not self.selection_held and self.in_sub_menu==1:
                self.action="Load"
                self.selection_held = True
                self.select_option()
            
            elif keys[pygame.K_t] and not self.selection_held and self.in_sub_menu==1:
                self.action="Overwrite"
                self.selection_held = True
                self.select_option()

        elif not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_RETURN] and not keys[pygame.K_TAB] and not keys[pygame.K_e] and not keys[pygame.K_t]:
            self.selection_held = False

    def select_option(self):
        if self.in_sub_menu == 0:
            selected_option = self.menu_items[self.selected_item]
        elif self.in_sub_menu == 1:
            selected_option = self.saves[self.selected_item]
            
        if selected_option == "Continue":
            self.visible = False
        elif selected_option == "Save and Load":
            self.in_sub_menu=1
        elif selected_option == "Options":
            self.in_sub_menu=2
        elif selected_option == "Exit":
            for item in os.listdir("terrain\worlds\simplified"):
                item_path=f"terrain\worlds\simplified\{item}\{CM.player.hash}\data_modified.world"
                if os.path.isfile(item_path):
                    os.remove(item_path)
            pygame.quit()
            sys.exit()
        elif self.in_sub_menu==1:
            if self.action=="Save":
                tmp=CM.assets.save()
                if tmp:
                    saves = glob.glob(os.path.join("saves", "*.habo"))
                    self.saves = [os.path.splitext(os.path.basename(filename))[0] for filename in saves]

    def render(self):
        if self.visible:
            
            pygame.draw.rect(
                self.bg_surface_menu,
                (100, 100, 100, 180),
                self.bg_surface_menu.get_rect(),
            )
            GM.screen.blit(self.bg_surface_menu, self.bg_menu)
            
            item_render = self.menu_font.render(GM.game_date.print_date(), True, (180, 180, 180))
            item_rect = item_render.get_rect(
                        center=(
                            GM.screen.get_width() // 2,
                            GM.screen.get_height()-50,
                        )
                    )
            GM.screen.blit(item_render, item_rect)
            
            if self.in_sub_menu == 0:
                for index, item in enumerate(self.menu_items):
                    color = (0, 0, 0) if index == self.selected_item else (180, 180, 180)
                    text = self.menu_font.render(item, True, color)
                    text_rect = text.get_rect(center=(GM.screen.get_width() // 2, GM.screen.get_height() // 2.5 + index * 50))
                    GM.screen.blit(text, text_rect)
            
            if self.in_sub_menu==1:
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
                    item_render = self.menu_font.render(save_text, True, color)
                    item_rect = item_render.get_rect(
                        center=(
                            GM.screen.get_width() // 2,
                            GM.screen.get_height() // 4 + index * 50,
                        )
                    )
                    GM.screen.blit(item_render, item_rect)
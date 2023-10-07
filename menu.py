import glob
import os
import sys
from datetime import datetime

import pygame


class Menu:
    def __init__(self, screen, assets, player):
        self.screen = screen
        self.visible = False
        self.menu_items = ["Continue", "Save and Load", "Options", "Exit"]
        self.selected_item = 0
        self.m_key_held = False
        self.selection_held = False
        self.in_sub_menu = 0
        saves = glob.glob(os.path.join("saves", "*.habo"))
        self.saves = [os.path.splitext(os.path.basename(filename))[0] for filename in saves]
        self.action="Save"
        self.assets=assets
        self.player=player
        self.game=None

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
            pygame.quit()
            sys.exit()
        elif self.in_sub_menu==1:
            if self.action=="Save":
                save_name=f"{self.player.name}_{self.player.current_world}_{datetime.now().strftime('%d-%m-%Y %H-%M-%S')}"
                tmp=self.assets.save(save_name, self.game)
                if tmp:
                    saves = glob.glob(os.path.join("saves", "*.habo"))
                    self.saves = [os.path.splitext(os.path.basename(filename))[0] for filename in saves]

    def render(self, game):
        self.game=game
        if self.visible:
            menu_font = pygame.font.Font("game_data/inter.ttf", 36)
            if self.in_sub_menu == 0:
                for index, item in enumerate(self.menu_items):
                    color = (0, 0, 0) if index == self.selected_item else (180, 180, 180)
                    text = menu_font.render(item, True, color)
                    text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2.5 + index * 50))
                    self.screen.blit(text, text_rect)
            
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
                    item_render = menu_font.render(save_text, True, color)
                    item_rect = item_render.get_rect(
                        center=(
                            self.screen.get_width() // 2,
                            self.screen.get_height() // 4 + index * 50,
                        )
                    )
                    self.screen.blit(item_render, item_rect)
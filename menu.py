import pygame
import sys

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.visible = False
        self.menu_items = ["Continue", "Save", "Options", "Exit"]
        self.selected_item = 0
        self.m_key_held = False
        self.selection_held = False

    def toggle_visibility(self):
        self.visible = not self.visible

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
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                self.selection_held = True

            elif keys[pygame.K_DOWN] and not self.selection_held:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                self.selection_held = True

            elif keys[pygame.K_RETURN] and not self.selection_held:
                self.select_option()
                self.selection_held = True

        elif not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_RETURN]:
            self.selection_held = False

    def select_option(self):
        selected_option = self.menu_items[self.selected_item]
        if selected_option == "Continue":
            self.visible = False
        elif selected_option == "Save":
            # Open options menu
            pass
        elif selected_option == "Options":
            # Open options menu
            pass
        elif selected_option == "Exit":
            pygame.quit()
            sys.exit()

    def render(self):
        if self.visible:
            menu_font = pygame.font.Font("game_data/inter.ttf", 36)
            for index, item in enumerate(self.menu_items):
                color = (0, 0, 0) if index == self.selected_item else (180, 180, 180)
                text = menu_font.render(item, True, color)
                text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2.5 + index * 50))
                self.screen.blit(text, text_rect)
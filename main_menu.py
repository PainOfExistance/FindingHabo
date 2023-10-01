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
        self.screen_width=screen.get_width()
        self.screen_height=screen.get_height()
        self.is_menu_visible=True
        self.font = pygame.font.Font("game_data/inter.ttf", 36)

    def handle_input(self):
        keys = pygame.key.get_pressed()

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
        if selected_option == "Start":
            print("Starting the game...")
            self.loading()
            assets=AssetLoader(self.screen_width, self.screen_height)
            player = Player("game_data/desk1.png", self.screen_width, self.screen_height, assets)
            menu = Menu(self.screen)
            player_menu = PlayerMenu(self.screen, player)
            game = Game(self.screen, self.screen_width, self.screen_height, menu, player_menu, player, assets)
            self.is_menu_visible = False
            game.run()
        elif selected_option == "Load":
            print("Opening load menu...")
            # Add your options menu logic here
        elif selected_option == "Options":
            print("Opening options menu...")
            # Add your options menu logic here
        elif selected_option == "Exit":
            pygame.quit()
            sys.exit()

    def render(self):
        for index, item in enumerate(self.menu_items):
            color = (0, 0, 0) if index == self.selected_item else (180, 180, 180)
            text = self.font.render(item, True, color)
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2.5 + index * 50))
            self.screen.blit(text, text_rect)
        pygame.display.flip()

    def loading(self):
        text = self.font.render("Loading...", True, (180, 180, 180))
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2.5))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def run(self):
        while self.is_menu_visible:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_menu_visible = False

            self.screen.fill((255, 255, 255))
            self.handle_input()
            self.render()


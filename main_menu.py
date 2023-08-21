import pygame
import sys
from player import Player
from menu import Menu
from player_menu import PlayerMenu
from asset_loader import AssetLoader
from game import Game

is_menu_visible=True

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.menu_items = ["Start", "Options", "Exit"]
        self.selected_item = 0
        self.selection_held = False
        self.screen_width=screen.get_width()
        self.screen_height=screen.get_height()

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
            assets=AssetLoader(self.screen_width, self.screen_height)
            menu = Menu(self.screen)
            player = Player("desk1.png", self.screen_width, self.screen_height, assets)
            player_menu = PlayerMenu(self.screen, player)
            game = Game(self.screen, self.screen_width, self.screen_height, menu, player_menu, player, assets)
            game.run()
            is_menu_visible=False
        elif selected_option == "Options":
            print("Opening options menu...")
            # Add your options menu logic here
        elif selected_option == "Exit":
            pygame.quit()
            sys.exit()

    def render(self):
        font = pygame.font.Font("inter.ttf", 36)
        for index, item in enumerate(self.menu_items):
            color = (0, 0, 0) if index == self.selected_item else (180, 180, 180)
            text = font.render(item, True, color)
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2.5 + index * 40))
            self.screen.blit(text, text_rect)

"""
    assets=AssetLoader(screen_width, screen_height)
    menu = Menu(screen)
    player = Player("desk1.png", screen_width, screen_height, assets)
    player_menu = PlayerMenu(screen, player)
    game = Game(screen, screen_width, screen_height, menu, player_menu, player, assets)
    game.run()
"""
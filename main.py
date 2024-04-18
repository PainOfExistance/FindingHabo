import os
import sys

import numpy as np
import pygame

from game_manager import GameManager as GM
from main_menu import MainMenu

pygame.init()
display=pygame.display.get_desktop_sizes()

pygame.display.set_icon(pygame.image.load("./textures/logo.png"))
pygame.mouse.set_visible(False) 
pygame.event.set_grab(True)
screen_width, screen_height = display[0][0], display[0][1]
screen = pygame.display.set_mode((1280, 720), vsync=0, flags= pygame.SCALED | pygame.RESIZABLE)
GM._scr=screen
GM.screen=pygame.Surface((1280, 720))
pygame.display.set_caption("Finding Habo")
if __name__ == "__main__":
    menu=MainMenu()
    menu.run()


"""
health-health lol
knowlage-to learn abilities, increases/decreases over time and is effected by effects
sanity-ability to learn new shit if its hight enough
power-to use abilities, increases/decreases over time and is effected by effects
"""
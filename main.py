import sys

import numpy as np
import pygame
import screeninfo

from game_manager import GameManager as GM
from main_menu import MainMenu

m=screeninfo.get_monitors()

display=[x for x in m if x.is_primary==True]
pygame.init()
screen_width, screen_height = display[0].width, display[0].height
screen = pygame.display.set_mode((1080, 720), pygame.RESIZABLE)
GM._scr=screen
GM.screen=pygame.Surface((1080, 720))
pygame.display.set_caption("Finding Habo")
if __name__ == "__main__":
    menu=MainMenu()
    menu.run()
    pygame.quit()
    sys.exit()


"""
health-health lol
knowlage-to learn abilities, increases/decreases over time and is effected by effects
sanity-ability to learn new shit if its hight enough
power-to use abilities, increases/decreases over time and is effected by effects
"""
import random

import numpy as np
import pygame

from game_manager import GameManager as GM


def check_pedistal(current_items, required_items):
    list=[x["type"] for x in current_items]
    current_items=list
    if len(current_items) == len(required_items) and set(current_items) == set(required_items):
        return True
    elif len(current_items) == len(required_items):
        return False

def find_ref(iid, type):
    for i, x in enumerate(GM.world_objects):
        if (x["type"]=="activator" or x["type"]=="walk_in_portal") and x["name"]["type"]==type and x["iid"]==iid:
            return i, x
    return -1
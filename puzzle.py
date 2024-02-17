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

def find_ref(iid):
    for x in GM.world_objects:
        if x["type"]=="activator" and x["name"]["type"]=="pedistal":
            if x["iid"]==iid:
                return x
    return -1
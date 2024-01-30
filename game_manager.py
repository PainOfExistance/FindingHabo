import numpy as np


class GameManager:
    item_hovered = None
    selection_held = False
    container_hovered = None
    container_open = False
    tab_pressed = False
    r_pressed = False
    container_menu_selected = True
    selected_inventory_item = 0
    prev_index = 0
    time_diff = 0
    attacking = False
    attack_button_held = False
    delta_time = 0
    current_line = None
    line_time = 0.0
    is_in_dialogue = False
    is_ready_to_talk = False
    world_to_travel_to = None
    talk_to_name = ""
    moving = False
    rotation_angle = 0
    counter = 0
    screen=None
    _scr=None
    screen_width=None
    screen_height=None


import numpy as np

from script_loader import ScriptLoader


class GameManager:
    enter_held=False
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
    worlds=None
    ai_package=None
    items=None
    game_date=None
    world_objects=[]
    relative_player_top = 0
    relative_player_left = 0
    relative_player_right = 0
    relative_player_bottom = 0
    save_name="in the beginning"
    save_world_names=[]
    bg_surface_menu=None
    bg_menu=None
    weapon_rect=None
    collision_map=None
    map_height=None
    map_width=None
    bg_rect=None
    background=None
    npc_list=[]
    load=False
    map_shown=False
    map_m_held=False
    notes=[]
    location_hovered={"name":None,"x":None,"y":None, "index":None}
    screen_width_scr=0
    screen_height_scr=0
    ratio=(0,0)
    can_fast_travel=True
    prev_mouse=0
    can_move=True

class ClassManager:
    ai=None
    animation=None
    dialogue=None
    effects=None
    game=None
    inventory=None
    level=None
    menu=None
    music_player=None
    player_menu=None
    player=None
    puzzle=None
    quests=None
    stats=None
    traits=None
    map=None
    script_loader=ScriptLoader()
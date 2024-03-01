import copy
import os
import re
import sys
from datetime import datetime

import numpy as np
import pygame
from pygame.locals import *

import npc as N
import renderer as R
import world_parser as wp
from ai import Ai
from game_manager import ClassManager as CM
from game_manager import GameManager as GM
from map import Map
from music_player import MusicPlayer


class Game:
    def __init__(self):
        for item in os.listdir("terrain\worlds\simplified"):
            item_path=f"terrain\worlds\simplified\{item}\{CM.player.hash}\data_modified.world"
            if os.path.isfile(item_path):
                os.remove(item_path)
        
        GM.items = CM.assets.load_items()
        GM.ai_package = CM.assets.load_ai_package()

        self.prompt_font = pygame.font.Font("fonts/SovngardeBold.ttf", 20)
        self.subtitle_font = pygame.font.Font("fonts/SovngardeBold.ttf", 28)
        self.menu_font = pygame.font.Font("fonts/SovngardeBold.ttf", 34)

        CM.inventory.add_item(GM.items["Minor Health Potion"])
        CM.inventory.add_item(GM.items["Steel Sword"])
        CM.inventory.add_item(GM.items["Minor Health Potion"])
        # CM.inventory.add_item(GM.items["Knowledge Potion"])
        # CM.inventory.add_item(GM.items["Power Elixir"])
        # CM.inventory.add_item(GM.items["Steel Armor"])
        # CM.inventory.add_item(GM.items["Divine Armor"])
        CM.inventory.add_item(GM.items["Key to the Land of the Free"])
        GM.world_objects = list()

        self.setup(f"terrain/worlds/simplified/{CM.player.current_world.replace(' ', '_')}/data.json")
        CM.player.quests.dialogue = CM.ai.strings
        self.clock = pygame.time.Clock()
        self.target_fps = 60
        self.last_frame_time = pygame.time.get_ticks()
        self.on_a_diagonal = False
        CM.map=Map()

        GM.weapon_rect = pygame.Rect(
            CM.player.player_rect.left + CM.player.player_rect.width // 4,
            CM.player.player_rect.top - CM.player.range // 2,
            16,
            CM.player.range,
        )

        GM.bg_menu = pygame.Rect(
            0,
            0,
            GM.screen.get_width(),
            GM.screen.get_height(),
        )

        GM.bg_surface_menu = pygame.Surface(
            (GM.bg_menu.width, GM.bg_menu.height), pygame.SRCALPHA
        )
        
        self.prev=(0,0)

    def setup_loaded(self, portals, npcs, final_items, containers, metadata, activators, nav_tiles, notes):
        metadata["collision_set"] = re.sub(r'\\+', r'\\', metadata["collision_set"])
        metadata["background"] = re.sub(r'\\+', r'\\', metadata["background"])
        GM.world_objects.append(
            {
                "name": metadata,
                "type": "metadata",
            }
        )

        for data in final_items:
            item = GM.items[data[0]]
            img, img_rect = CM.assets.load_images(
                item["image"], (0, 0), (data[1], data[2])
            )
            GM.world_objects.append(
                {
                    "name": item["name"],
                    "image": img,
                    "rect": img_rect,
                    "type": "item",
                    "iid": data[3]
                }
            )

        for data in containers:
            tmp = data
            img, img_rect = CM.assets.load_images(data[4], (64, 64), (data[1], data[2]))
            GM.world_objects.append(
                {"image": img, "rect": img_rect, "type": "container", "name": tmp, "pedistal": data[6], "iid": data[7]}
            )

        for data in npcs:
            img, img_rect = CM.assets.load_images(
                data[0]["stats"]["image"], (64, 64), (data[1], data[2])
            )
            GM.npc_list.append(
                {
                    "image": img,
                    "rect": img_rect,
                    "type": "npc",
                    "name": copy.deepcopy(data[0]),
                    "attack_diff": 0,
                    "agroved": False,
                    "iid": data[3]
                }
            )

        for data in portals:
            if "unlocked_by" in data[0]:
                img, img_rect = CM.assets.load_images(
                    "textures\static\door.png", (64, 64), (data[1], data[2])
                )
                GM.world_objects.append(
                    {
                        "image": img,
                        "rect": img_rect,
                        "type": "portal",
                        "name": data[0],
                        "iid": data[3],
                    }
                )
            else:
                img, img_rect = CM.assets.load_images(
                    "textures\\static\\barrier.png", (data[4], data[5]), (data[1], data[2])
                )
                GM.world_objects.append(
                    {
                        "image": img,
                        "rect": img_rect,
                        "type": "walk_in_portal",
                        "name": data[0],
                        "iid": data[3],
                    }
                )
            
        for data in activators:
            img_rect = pygame.Rect(
                0,0, data[3], data[4]
            )
            img_rect.center=(data[1], data[2])
            
            GM.world_objects.append(
                {
                    "rect": img_rect,
                    "type": "activator",
                    "name": data[0],
                    "iid": data[5],
                }
            )

        for data in nav_tiles:
            img_rect = pygame.Rect(
                0, 0, 16, 16
            )
            img_rect.center=(data[1], data[2])
            
            GM.world_objects.append(
                {
                    "rect": img_rect,
                    "type": "nav_tile",
                    "name": data[0],
                    "iid": data[3]
                }
            )
        
        for data in notes:
            img, img_rect = CM.assets.load_images(
                data[0]["marker_file"][3:], (16, 16), (data[1], data[2])
            )
            GM.notes.append(
                {
                    "image": img,
                    "rect": img_rect,
                    "type": "note",
                    "name": data[0],
                    "iid": data[3],
                    "x": data[1],
                    "y": data[2],
                    "moved": False
                }
            )
        
        #print(GM.world_objects)

    def setup(
        self, path="terrain/worlds/simplified/Dream_World/data.json", type="default"
    ):
        GM.world_objects.clear()
        GM.npc_list.clear()
        
        level_data = CM.assets.load_level_data(path)
        modified_data = CM.assets.get_stored_data(path)
        if modified_data != None:
            date1 = datetime.strptime(GM.game_date.get_date(), "%Y-%m-%dT%H:%M:%S")
            date2 = datetime.strptime(
                modified_data[0]["name"]["time_passed"], "%Y-%m-%dT%H:%M:%S"
            )
            delta = date1 - date2
            if modified_data[0]["name"]["respawn_timer"] > delta.days:
                print("respawned")
                spawn_point, portals, npcs, final_items, containers, metadata, activators, nav_tiles, notes = wp.parse_visited(modified_data)
                self.setup_loaded(portals, npcs, final_items, containers, metadata, activators, nav_tiles, notes)
            else:
                print("basic in")
                spawn_point, portals, npcs, final_items, containers, metadata, activators, nav_tiles, notes = wp.remove_uniques(level_data, modified_data)
                self.setup_loaded(portals, npcs, final_items, containers, metadata, activators, nav_tiles, notes)
        else:
            print("basic out")
            spawn_point, portals, npcs, final_items, containers, metadata, activators, nav_tiles, notes = wp.parser(level_data)
            self.setup_loaded(portals, npcs, final_items, containers, metadata, activators, nav_tiles, notes)
        
        CM.music_player = MusicPlayer(metadata["music"])
        GM.background, GM.bg_rect = CM.assets.load_background(
            metadata["background"],
        )
        GM.collision_map = CM.assets.load_collision(metadata["collision_set"])
        GM.map_height = GM.collision_map.shape[0]
        GM.map_width = GM.collision_map.shape[1]

        if type != "default":
            for i, _ in enumerate(portals):
                if portals[i][0]["type"] == type:
                    spawn_point = (portals[i][0]["spawn_point"]["cx"]*16, portals[i][0]["spawn_point"]["cy"]*16)

        if spawn_point == (0, 0):
            spawn_point = (GM.relative_player_left, GM.relative_player_top)

        offset = (
            spawn_point[0] - GM.screen.get_width() // 2,
            spawn_point[1] - GM.screen.get_height() // 2,
        )

        GM.bg_rect.left = -offset[0]
        GM.bg_rect.top = -offset[1]

        CM.player.player_rect.left = spawn_point[0] - offset[0]
        CM.player.player_rect.top = spawn_point[1] - offset[1]

    def travel(self):
        self.loading()
        CM.player.current_world = GM.world_to_travel_to["world_name"]
        GM.world_objects[GM.world_to_travel_to["index"]]["name"]["locked"] = False
        CM.assets.world_save(GM.world_objects)
        self.setup(
                    "terrain/" + GM.world_to_travel_to["world_to_load"],
                    GM.world_to_travel_to["type"],
                )
        GM.world_to_travel_to = None
        CM.player.quests.dialogue = CM.ai.strings
    
    def run(self):
        while True:
            # Calculate delta time (time since last frame)
            current_time = pygame.time.get_ticks()
            GM.delta_time = (
                current_time - self.last_frame_time
            ) / 1000.0  # Convert to seconds
            self.last_frame_time = current_time
            GM.time_diff += GM.delta_time
            GM.counter += GM.delta_time
            
            if GM.load:
                GM.load = False
                self.travel()
                
            self.handle_input()
            self.handle_events()
            self.draw()
            GM.game_date.increment_seconds()
            CM.player.check_experation(GM.delta_time)
            if (
                not CM.player_menu.visible
                and not GM.tab_pressed
                and not GM.container_open
                and not GM.is_in_dialogue
                and not GM.map_shown
            ):
                CM.menu.handle_input()

            if (
                not CM.menu.visible
                and not GM.tab_pressed
                and not GM.container_open
                and not GM.is_in_dialogue
                and not GM.map_shown
            ):
                CM.player_menu.handle_input()

            if (
                GM.is_in_dialogue
                and not GM.tab_pressed
                and not GM.container_open
                and not CM.player_menu.visible
                and not CM.menu.visible
                and not GM.map_shown
            ):
                CM.ai.strings.handle_input()
                if CM.ai.strings.starts != 0:
                    CM.player.quests.start_quest(CM.ai.strings.starts)
                    CM.ai.strings.starts = 0

                if CM.ai.strings.advances != 0:
                    CM.player.quests.advance_quest(CM.ai.strings.advances)
                    CM.ai.strings.advances = 0
            
            if GM.map_shown:
                CM.map.handle_input()
            else:
                R.check_notes()

            self.clock.tick(self.target_fps)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.USEREVENT:  # Track ended event
                CM.music_player.update()
            
            if GM.map_shown:
                CM.map.handle_events(event)

    def handle_input(self):
        # na lestvici 1-10 kako bi ocenili Saro Dugi iz ITK?
        if GM.time_diff >= 20:
            GM.time_diff = 5

        GM.relative_player_left = int(CM.player.player_rect.left - GM.bg_rect.left)
        GM.relative_player_right = int(CM.player.player_rect.right - GM.bg_rect.left)
        GM.relative_player_top = int(CM.player.player_rect.top - GM.bg_rect.top)
        GM.relative_player_bottom = int(CM.player.player_rect.bottom - GM.bg_rect.top)
        movement = int(CM.player.movement_speed * GM.delta_time)

        CM.player.quests.check_quest_advancement(
            (
                GM.relative_player_top + CM.player.player_rect.height // 2,
                GM.relative_player_left + CM.player.player_rect.width // 2,
            ),
            CM.player.current_world,
        )
        
        self.prev=CM.player.player_rect.center
        
        keys = pygame.key.get_pressed()

        if CM.player.player_rect.left <= 10:
            GM.bg_rect.move_ip(movement, 0)
            CM.player.player_rect.move_ip(movement, 0)

        if CM.player.player_rect.right >= GM.screen_width - 10:
            GM.bg_rect.move_ip(-movement, 0)
            CM.player.player_rect.move_ip(-movement, 0)
            
        if CM.player.player_rect.top <= 10:
            GM.bg_rect.move_ip(0, movement)
            CM.player.player_rect.move_ip(0, movement)
            
        if CM.player.player_rect.bottom >= GM.screen_height - 10:
            GM.bg_rect.move_ip(0, -movement)
            CM.player.player_rect.move_ip(0, -movement)

        GM.moving = False
        if (
            keys[pygame.K_a]
            and np.count_nonzero(
                GM.collision_map[
                    GM.relative_player_top : GM.relative_player_bottom,
                    GM.relative_player_left - movement,
                ]
                == 1
            )
            <= 1
            and not CM.menu.visible
            and not CM.player_menu.visible
            and not GM.container_open
            and not GM.is_in_dialogue
            and not GM.map_shown
        ):
            if CM.player.player_rect.left > 10:
                CM.player.player_rect.move_ip(-movement, 0)
                if GM.rotation_angle != 90:
                    GM.rotation_angle = 90 - GM.rotation_angle
                    # CM.player.player = pygame.transform.rotate(CM.player.player, GM.rotation_angle)
                    GM.rotation_angle = 90
                GM.moving = True

        elif (
            keys[pygame.K_a]
            and not CM.menu.visible
            and not CM.player_menu.visible
            and not GM.container_open
            and not GM.is_in_dialogue
            and not GM.map_shown
        ):
            dx = np.count_nonzero(
                GM.collision_map[
                    GM.relative_player_bottom,
                    GM.relative_player_left - movement * 2 : GM.relative_player_left,
                ]
            )
            dt = np.count_nonzero(
                GM.collision_map[
                    GM.relative_player_top,
                    GM.relative_player_left - movement * 2 : GM.relative_player_left,
                ]
            )
            dy = np.count_nonzero(
                GM.collision_map[
                    GM.relative_player_top : GM.relative_player_bottom,
                    GM.relative_player_left - movement * 2,
                ]
            )

            angle = np.arctan2(dy, dt if dt > dx else dx)

            # print(np.rad2deg(angle))
            if (
                np.rad2deg(angle) < 70
                and np.count_nonzero(
                    GM.collision_map[
                        GM.relative_player_left : GM.relative_player_right,
                        GM.relative_player_top : GM.relative_player_bottom,
                    ]
                )
                <= 5
            ):
                move_direction = -1 if dt < dx else 1
                CM.player.player_rect.move_ip(
                    int(-movement * np.cos(angle)),
                    int(move_direction * movement * np.sin(angle)),
                )
                self.on_a_diagonal = True
                if GM.rotation_angle != 90:
                    GM.rotation_angle = 90 - GM.rotation_angle
                    # CM.player.player = pygame.transform.rotate(CM.player.player, GM.rotation_angle)
                    GM.rotation_angle = 90
                self.on_a_diagonal = True
                GM.moving = True

        if (
            keys[pygame.K_d]
            and np.count_nonzero(
                GM.collision_map[
                    GM.relative_player_top : GM.relative_player_bottom,
                    min(GM.relative_player_right + movement, GM.map_width - 1),
                ]
                == 1
            )
            <= 1
            and not CM.menu.visible
            and not CM.player_menu.visible
            and not GM.container_open
            and not GM.is_in_dialogue
            and not GM.map_shown
        ):
            if CM.player.player_rect.right < GM.screen_width - 10:
                CM.player.player_rect.move_ip(movement, 0)
                if GM.rotation_angle != 270:
                    GM.rotation_angle = 270 - GM.rotation_angle
                    # CM.player.player = pygame.transform.rotate(CM.player.player, GM.rotation_angle)
                    GM.rotation_angle = 270
                GM.moving = True

        elif (
            keys[pygame.K_d]
            and not CM.menu.visible
            and not CM.player_menu.visible
            and not GM.container_open
            and not GM.is_in_dialogue
            and not GM.map_shown
        ):
            dx = np.count_nonzero(
                GM.collision_map[
                    GM.relative_player_bottom,
                    GM.relative_player_right : GM.relative_player_right + movement * 2,
                ]
            )
            dt = np.count_nonzero(
                GM.collision_map[
                    GM.relative_player_top,
                    GM.relative_player_right : GM.relative_player_right + movement * 2,
                ]
            )
            dy = np.count_nonzero(
                GM.collision_map[
                    GM.relative_player_top : GM.relative_player_bottom,
                    GM.relative_player_right + movement * 2,
                ]
            )

            angle = np.arctan2(dy, dt if dt > dx else dx)

            # print(np.rad2deg(angle))
            if (
                np.rad2deg(angle) < 70
                and np.count_nonzero(
                    GM.collision_map[
                        GM.relative_player_left : GM.relative_player_right,
                        GM.relative_player_top : GM.relative_player_bottom,
                    ]
                )
                <= 5
            ):
                move_direction = -1 if dt < dx else 1
                CM.player.player_rect.move_ip(
                    int(movement * np.cos(angle)),
                    int(move_direction * movement * np.sin(angle)),
                )
                if GM.rotation_angle != 270:
                    GM.rotation_angle = 270 - GM.rotation_angle
                    # CM.player.player = pygame.transform.rotate(CM.player.player, GM.rotation_angle)
                    GM.rotation_angle = 270
                self.on_a_diagonal = True
                GM.moving = True

        if (
            keys[pygame.K_w]
            and np.count_nonzero(
                GM.collision_map[
                    GM.relative_player_top - movement,
                    GM.relative_player_left : GM.relative_player_right,
                ]
                == 1
            )
            <= 1
            and not CM.menu.visible
            and not CM.player_menu.visible
            and not GM.container_open
            and not GM.is_in_dialogue
            and not GM.map_shown
        ):
            if CM.player.player_rect.top > 10:
                CM.player.player_rect.move_ip(0, -movement)
                if GM.rotation_angle != 0:
                    GM.rotation_angle = 0 - GM.rotation_angle
                    # CM.player.player = pygame.transform.rotate(CM.player.player, GM.rotation_angle)
                    GM.rotation_angle = 0
                GM.moving = True

        elif (
            keys[pygame.K_w]
            and not CM.menu.visible
            and not CM.player_menu.visible
            and not GM.container_open
            and not GM.is_in_dialogue
            and not GM.map_shown
        ):
            dx = np.count_nonzero(
                GM.collision_map[
                    GM.relative_player_top - movement * 2 : GM.relative_player_top,
                    GM.relative_player_right,
                ]
            )
            dt = np.count_nonzero(
                GM.collision_map[
                    GM.relative_player_top - movement * 2 : GM.relative_player_top,
                    GM.relative_player_left,
                ]
            )
            dy = np.count_nonzero(
                GM.collision_map[
                    GM.relative_player_top - movement * 2,
                    GM.relative_player_left : GM.relative_player_right,
                ]
            )

            angle = np.arctan2(dy, dt if dt > dx else dx)

            if (
                np.rad2deg(angle) < 70
                and np.count_nonzero(
                    GM.collision_map[
                        GM.relative_player_left : GM.relative_player_right,
                        GM.relative_player_top : GM.relative_player_bottom,
                    ]
                )
                <= 5
            ):
                move_direction_X = -1 if dt < dx else 1
                move_direction_Y = -1 if dt > dx else 1
                CM.player.player_rect.move_ip(
                    int(movement * np.cos(angle) * move_direction_X),
                    int(movement * move_direction_Y * np.sin(angle)),
                )
                if GM.rotation_angle != 0:
                    GM.rotation_angle = 0 - GM.rotation_angle
                    # CM.player.player = pygame.transform.rotate(CM.player.player, GM.rotation_angle)
                    GM.rotation_angle = 0
                self.on_a_diagonal = True
                GM.moving = True

        if (
            keys[pygame.K_s]
            and np.count_nonzero(
                GM.collision_map[
                    min(GM.relative_player_bottom + movement, GM.map_height - 1),
                    GM.relative_player_left : GM.relative_player_right,
                ]
                == 1
            )
            <= 1
            and not CM.menu.visible
            and not CM.player_menu.visible
            and not GM.container_open
            and not GM.is_in_dialogue
            and not GM.map_shown
        ):
            if CM.player.player_rect.bottom < GM.screen_height - 10:
                CM.player.player_rect.move_ip(0, movement)
                if GM.rotation_angle != 180:
                    GM.rotation_angle = 180 - GM.rotation_angle
                    # CM.player.player = pygame.transform.rotate(CM.player.player, GM.rotation_angle)
                    GM.rotation_angle = 180
                GM.moving = True

        elif (
            keys[pygame.K_s]
            and not CM.menu.visible
            and not CM.player_menu.visible
            and not GM.container_open
            and not GM.is_in_dialogue
            and not GM.map_shown
        ):
            dx = np.count_nonzero(
                GM.collision_map[
                    GM.relative_player_bottom : GM.relative_player_bottom
                    + movement * 2,
                    GM.relative_player_right,
                ]
            )
            dt = np.count_nonzero(
                GM.collision_map[
                    GM.relative_player_bottom : GM.relative_player_bottom
                    + movement * 2,
                    GM.relative_player_left,
                ]
            )
            dy = np.count_nonzero(
                GM.collision_map[
                    GM.relative_player_bottom + movement * 2,
                    GM.relative_player_left : GM.relative_player_right,
                ]
            )

            angle = np.arctan2(dy, dt if dt > dx else dx)

            if (
                np.rad2deg(angle) < 70
                and np.count_nonzero(
                    GM.collision_map[
                        GM.relative_player_left : GM.relative_player_right,
                        GM.relative_player_top : GM.relative_player_bottom,
                    ]
                )
                <= 5
            ):
                move_direction_X = -1 if dt < dx else 1
                move_direction_Y = -1 if dt > dx else 1
                CM.player.player_rect.move_ip(
                    int(movement * np.cos(angle) * move_direction_X),
                    int(movement * move_direction_Y * np.sin(angle)),
                )
                if GM.rotation_angle != 180:
                    GM.rotation_angle = 180 - GM.rotation_angle
                    # CM.player.player = pygame.transform.rotate(CM.player.player, GM.rotation_angle)
                    GM.rotation_angle = 180
                self.on_a_diagonal = True
                GM.moving = True

        if (
            keys[pygame.K_e]
            and not CM.menu.visible
            and not CM.player_menu.visible
            and not GM.selection_held
            and not GM.map_shown
        ):
            if GM.item_hovered != None:
                GM.selection_held = True
                if GM.item_hovered < len(GM.world_objects) and GM.item_hovered >= 0:
                    CM.player.add_item(
                        GM.items[GM.world_objects[GM.item_hovered]["name"]]
                    )
                    del GM.world_objects[GM.item_hovered]
                    GM.item_hovered = None

            elif GM.container_hovered != None and not GM.container_open:
                GM.selection_held = True
                if (
                    GM.container_hovered < len(GM.world_objects)
                    and GM.container_hovered >= 0
                ):
                    GM.container_open = True

            elif GM.is_ready_to_talk:
                GM.selection_held = True
                GM.is_ready_to_talk = False
                GM.is_in_dialogue = True

            elif GM.world_to_travel_to != None and (
                not GM.world_to_travel_to["locked"]
                or CM.inventory.items.get(GM.world_to_travel_to["unlocked_by"], "None")
                != "None"
                and not GM.selection_held
            ):
                GM.selection_held = True
                self.travel()

        elif (
            not keys[pygame.K_e]
            and not GM.container_open
            and not CM.ai.strings.bartering
        ):
            GM.selection_held = False

        if (
            keys[pygame.K_TAB]
            and not CM.menu.visible
            and not CM.player_menu.visible
            and not GM.tab_pressed
            and not GM.map_shown
        ):
            GM.tab_pressed = True
            GM.container_open = False
            GM.is_ready_to_talk = False

            if CM.ai.strings.bartering:
                CM.ai.strings.bartering = False
                return

            if GM.is_in_dialogue:
                GM.is_in_dialogue = False
                CM.ai.strings.index = -1
                CM.ai.strings.greeting_played = False
                CM.ai.strings.talking = False
                CM.music_player.skip_current_line()

        elif not keys[pygame.K_TAB] and not GM.container_open and GM.tab_pressed:
            GM.tab_pressed = False
            GM.prev_index = 0
            GM.selected_inventory_item = 0

        if (
            keys[pygame.K_UP]
            and not GM.selection_held
            and (GM.container_open or CM.ai.strings.bartering)
            and not CM.menu.visible
            and not CM.player_menu.visible
            and not GM.map_shown
        ):
            if (
                GM.container_menu_selected
                and CM.ai.strings.bartering
                and len(GM.ai_package[GM.talk_to_name]["items"])
            ):
                GM.selected_inventory_item = (GM.selected_inventory_item - 1) % len(
                    GM.ai_package[GM.talk_to_name]["items"]
                )
                GM.selection_held = True
                return

            elif len(CM.inventory.items) and CM.ai.strings.bartering:
                GM.selected_inventory_item = (GM.selected_inventory_item - 1) % len(
                    CM.inventory.items
                )
                GM.selection_held = True
                return

            if (
                GM.container_menu_selected
                and GM.container_open
                and len(GM.world_objects[GM.container_hovered]["name"][0])
            ):
                GM.selected_inventory_item = (GM.selected_inventory_item - 1) % len(
                    GM.world_objects[GM.container_hovered]["name"][0]
                )
                GM.selection_held = True

            elif len(CM.inventory.items) and GM.container_open:
                GM.selected_inventory_item = (GM.selected_inventory_item - 1) % len(
                    CM.inventory.items
                )
                GM.selection_held = True

        elif (
            keys[pygame.K_DOWN]
            and not GM.selection_held
            and (GM.container_open or CM.ai.strings.bartering)
            and not CM.menu.visible
            and not CM.player_menu.visible
            and not GM.map_shown
        ):
            if (
                GM.container_menu_selected
                and CM.ai.strings.bartering
                and len(GM.ai_package[GM.talk_to_name]["items"])
            ):
                GM.selected_inventory_item = (GM.selected_inventory_item + 1) % len(
                    GM.ai_package[GM.talk_to_name]["items"]
                )
                GM.selection_held = True
                return

            elif len(CM.inventory.items) and CM.ai.strings.bartering:
                GM.selected_inventory_item = (GM.selected_inventory_item + 1) % len(
                    CM.inventory.items
                )
                GM.selection_held = True
                return

            if GM.container_menu_selected and len(
                GM.world_objects[GM.container_hovered]["name"][0]
            ):
                GM.selected_inventory_item = (GM.selected_inventory_item + 1) % len(
                    GM.world_objects[GM.container_hovered]["name"][0]
                )
                GM.selection_held = True
            elif len(CM.inventory.items):
                GM.selected_inventory_item = (GM.selected_inventory_item + 1) % len(
                    CM.inventory.items
                )
                GM.selection_held = True

        if (
            keys[pygame.K_LEFT]
            and not GM.selection_held
            and (GM.container_open or CM.ai.strings.bartering)
            and not CM.menu.visible
            and not CM.player_menu.visible
            and GM.container_menu_selected
            and not GM.map_shown
        ):
            GM.container_menu_selected = False
            GM.selection_held = True
            GM.selected_inventory_item, GM.prev_index = (
                GM.prev_index,
                GM.selected_inventory_item,
            )

        elif (
            keys[pygame.K_RIGHT]
            and not GM.selection_held
            and (GM.container_open or CM.ai.strings.bartering)
            and not CM.menu.visible
            and not CM.player_menu.visible
            and not GM.container_menu_selected
            and not GM.map_shown
        ):
            GM.container_menu_selected = True
            GM.selection_held = True
            GM.selected_inventory_item, GM.prev_index = (
                GM.prev_index,
                GM.selected_inventory_item,
            )

        elif (
            not keys[pygame.K_RETURN]
            and not keys[pygame.K_UP]
            and not keys[pygame.K_DOWN]
            and not keys[pygame.K_RIGHT]
            and not keys[pygame.K_LEFT]
            and (GM.container_open or CM.ai.strings.bartering)
        ):
            GM.selection_held = False
            GM.enter_held = True

        if (
            keys[pygame.K_RETURN]
            and not CM.menu.visible
            and not CM.player_menu.visible
            and not GM.selection_held
            and (GM.container_open or CM.ai.strings.bartering)
            and GM.enter_held
            and not GM.map_shown
        ):
            GM.selection_held = True
            GM.enter_held = False

            if CM.ai.strings.bartering:
                if (
                    GM.container_menu_selected
                    and len(GM.ai_package[GM.talk_to_name]["items"]) > 0
                ):
                    if (
                        GM.ai_package[GM.talk_to_name]["items"][
                            GM.selected_inventory_item
                        ]["quantity"]
                        > 0
                        and CM.player.gold
                        >= GM.items[
                            GM.ai_package[GM.talk_to_name]["items"][
                                GM.selected_inventory_item
                            ]["type"]
                        ]["price"]
                    ):
                        CM.player.gold -= GM.items[
                            GM.ai_package[GM.talk_to_name]["items"][
                                GM.selected_inventory_item
                            ]["type"]
                        ]["price"]
                        GM.ai_package[GM.talk_to_name]["gold"] += GM.items[
                            GM.ai_package[GM.talk_to_name]["items"][
                                GM.selected_inventory_item
                            ]["type"]
                        ]["price"]
                        GM.ai_package[GM.talk_to_name]["items"][
                            GM.selected_inventory_item
                        ]["quantity"] -= 1
                        CM.inventory.add_item(
                            GM.items[
                                GM.ai_package[GM.talk_to_name]["items"][
                                    GM.selected_inventory_item
                                ]["type"]
                            ]
                        )
                        if (
                            GM.ai_package[GM.talk_to_name]["items"][
                                GM.selected_inventory_item
                            ]["quantity"]
                            == 0
                        ):
                            del GM.ai_package[GM.talk_to_name]["items"][
                                GM.selected_inventory_item
                            ]

                elif not GM.container_menu_selected and len(CM.inventory.items) > 0:
                    if GM.ai_package[GM.talk_to_name]["gold"] <= 0:
                        GM.ai_package[GM.talk_to_name]["gold"] = 0
                    key = list(CM.inventory.quantity.keys())[GM.selected_inventory_item]
                    item_index = next(
                        (
                            index
                            for index, item in enumerate(
                                GM.ai_package[GM.talk_to_name]["items"]
                            )
                            if item["type"] == key
                        ),
                        None,
                    )

                    if item_index != None:
                        GM.ai_package[GM.talk_to_name]["items"][item_index][
                            "quantity"
                        ] += 1

                    else:
                        GM.ai_package[GM.talk_to_name]["items"].append(
                            {"type": key, "quantity": 1}
                        )
                    CM.inventory.remove_item(key)
                    CM.player.gold += GM.items[key]["price"]
                    GM.ai_package[GM.talk_to_name]["gold"] -= GM.items[key]["price"]

                if (
                    GM.selected_inventory_item > len(CM.inventory.items) - 1
                    and not GM.container_menu_selected
                ):
                    GM.selected_inventory_item = len(CM.inventory.items) - 1

                elif (
                    GM.selected_inventory_item
                    > len(GM.ai_package[GM.talk_to_name]["items"]) - 1
                    and GM.container_menu_selected
                ):
                    GM.selected_inventory_item = (
                        len(GM.ai_package[GM.talk_to_name]["items"]) - 1
                    )
                    if GM.selected_inventory_item < 0:
                        GM.selected_inventory_item = 0

                if GM.selected_inventory_item < 0:
                    GM.selected_inventory_item = 0
                return

            if (
                GM.container_menu_selected
                and len(GM.world_objects[GM.container_hovered]["name"][0]) > 0
            ):
                if (
                    GM.world_objects[GM.container_hovered]["name"][0][
                        GM.selected_inventory_item
                    ]["type"]
                    == "Gold"
                ):
                    CM.player.gold += GM.world_objects[GM.container_hovered]["name"][0][
                        GM.selected_inventory_item
                    ]["quantity"]
                    del GM.world_objects[GM.container_hovered]["name"][0][
                        GM.selected_inventory_item
                    ]

                elif (
                    GM.world_objects[GM.container_hovered]["name"][0][
                        GM.selected_inventory_item
                    ]["quantity"]
                    > 0
                ):
                    GM.world_objects[GM.container_hovered]["name"][0][
                        GM.selected_inventory_item
                    ]["quantity"] -= 1
                    CM.player.add_item(
                        GM.items[
                            GM.world_objects[GM.container_hovered]["name"][0][
                                GM.selected_inventory_item
                            ]["type"]
                        ]
                    )
                    if (
                        GM.world_objects[GM.container_hovered]["name"][0][
                            GM.selected_inventory_item
                        ]["quantity"]
                        == 0
                    ):
                        del GM.world_objects[GM.container_hovered]["name"][0][
                            GM.selected_inventory_item
                        ]

            elif not GM.container_menu_selected and len(CM.inventory.items) > 0:
                key = list(CM.inventory.quantity.keys())[GM.selected_inventory_item]
                item_index = next(
                    (
                        index
                        for index, item in enumerate(
                            GM.world_objects[GM.container_hovered]["name"][0]
                        )
                        if item["type"] == key
                    ),
                    None,
                )

                if item_index != None:
                    GM.world_objects[GM.container_hovered]["name"][0][item_index][
                        "quantity"
                    ] += 1
                else:
                    GM.world_objects[GM.container_hovered]["name"][0].append(
                        {"type": key, "quantity": 1}
                    )
                CM.inventory.remove_item(key)

            if (
                GM.selected_inventory_item > len(CM.inventory.items) - 1
                and not GM.container_menu_selected
            ):
                GM.selected_inventory_item = len(CM.inventory.items) - 1

            elif (
                GM.selected_inventory_item
                > len(GM.world_objects[GM.container_hovered]["name"][0]) - 1
                and GM.container_menu_selected
            ):
                GM.selected_inventory_item = (
                    len(GM.world_objects[GM.container_hovered]["name"][0]) - 1
                )

            if GM.selected_inventory_item < 0:
                GM.selected_inventory_item = 0

        if (
            keys[pygame.K_r]
            and CM.player_menu.selected_item == 0
            and not GM.r_pressed
            and not GM.selection_held
            and CM.player_menu.visible
            and not GM.map_shown
        ):
            GM.r_pressed = True
            key = list(CM.inventory.quantity.keys())[CM.player_menu.selected_sub_item]
            CM.player.unequip_item(key)
            ret = CM.player.remove_item(key)
            if ret:
                img, img_rect = CM.assets.load_images(
                    GM.items[key]["image"],
                    (0, 0),
                    (
                        GM.relative_player_left + CM.player.player_rect.width // 2,
                        GM.relative_player_top + CM.player.player_rect.height // 2,
                    ),
                )
                GM.world_objects.append(
                    {
                        "name": key,
                        "image": img,
                        "rect": img_rect,
                        "type": "item",
                    }
                )

        elif not keys[pygame.K_r] and GM.r_pressed:
            GM.r_pressed = False

        mouse_buttons = pygame.mouse.get_pressed()
        if (
            (mouse_buttons[0] or keys[pygame.K_SPACE])
            and not CM.menu.visible
            and not CM.player_menu.visible
            and not GM.attacking
            and not GM.attack_button_held
            and not GM.is_in_dialogue
            and not GM.container_open
            and not GM.map_shown
        ):
            timedif = 0
            if CM.player.equipped_items["hand"] != None:
                weapon = CM.inventory.items[CM.player.equipped_items["hand"]]
                timedif = weapon["stats"]["speed"]
            else:
                timedif = 0.3

            if GM.time_diff >= timedif and not GM.attacking:
                GM.attacking = True
                GM.attack_button_held = True
                print(f"attacked with a: {CM.player.equipped_items['hand']}")
                GM.time_diff = 0
                self.diff = pygame.time.get_ticks()
                
        elif GM.attacking:
            print("no longer attacking")
            GM.attacking = False
        
        if (
            keys[pygame.K_m]
            and not GM.map_m_held
            and not GM.container_open
            and not CM.ai.strings.bartering
            and not CM.menu.visible
            and not CM.player_menu.visible
        ):
            GM.screen_width_scr = GM._scr.get_width()
            GM.screen_height_scr = GM._scr.get_height()
            GM.ratio=((GM.screen_width/GM.screen_width_scr),(GM.screen_height/GM.screen_height_scr))
            GM.map_m_held = True
            GM.map_shown = not GM.map_shown
            pygame.mouse.set_visible(GM.map_shown) 
            CM.map.update_offset()
            CM.map.zoom=1
        elif not keys[pygame.K_m] and GM.map_m_held:
            GM.map_m_held = False
            
        if not mouse_buttons[0] and not keys[pygame.K_SPACE] and GM.attack_button_held:
            GM.attack_button_held = False

        if keys[pygame.K_o]:
            print()
            print("----------------")
            print(GM.world_objects)
            print("----------------")
            print()

        if GM.rotation_angle == 90:
            GM.weapon_rect = pygame.Rect(
                CM.player.player_rect.left - CM.player.range // 2,
                CM.player.player_rect.top + CM.player.player_rect.height // 2,
                CM.player.range,
                CM.player.player_rect.height // 4,
            )
        elif GM.rotation_angle == 0:
            GM.weapon_rect = pygame.Rect(
                CM.player.player_rect.left + CM.player.player_rect.width // 4,
                CM.player.player_rect.top - CM.player.range // 2,
                16,
                CM.player.range,
            )
        elif GM.rotation_angle == 180:
            GM.weapon_rect = pygame.Rect(
                CM.player.player_rect.left + CM.player.player_rect.width // 4,
                CM.player.player_rect.bottom - CM.player.range // 2,
                16,
                CM.player.range,
            )
        elif GM.rotation_angle == 270:
            GM.weapon_rect = pygame.Rect(
                CM.player.player_rect.right - CM.player.range // 2,
                CM.player.player_rect.top + CM.player.player_rect.height // 2,
                CM.player.range,
                CM.player.player_rect.height // 4,
            )  

    def loading(self):
        GM._scr.fill((255,255,255))
        font = pygame.font.Font("fonts/SovngardeBold.ttf", 34)
        text = font.render("Loading...", True, (180, 180, 180))
        text_rect = text.get_rect(
            center=(GM.screen.get_width() // 2, GM.screen.get_height() // 2.5)
        )
        GM._scr.blit(text, text_rect)
        pygame.display.flip()

    def draw(self):
        GM.screen.fill((230, 60, 20))
        GM.screen.blit(GM.background, GM.bg_rect.topleft)
        R.draw_objects(self.prompt_font)
        
        if not GM.map_shown:
            CM.map.set_map(GM.background)
            N.update_npc(self.subtitle_font, self.prompt_font)
            CM.player.draw()  # .lulekSprulek.123.fafajMi)
            CM.player.quests.draw_quest_info()
            R.draw_container(self.menu_font)
            R.draw_barter(self.menu_font)
            CM.menu.render()
            CM.player_menu.render()

            if GM.is_in_dialogue:
                CM.ai.strings.draw(GM.talk_to_name)
                # todo fix

        else:
            CM.map.draw()
        
        # https://www.youtube.com/watch?v=RXkeWnbJlOE&list=RD_u8CpQdZLMA&index=3
        # pygame.draw.rect(GM.screen, (0, 0, 0), GM.weapon_rect)
        
        subsurface_rect = pygame.Rect(
            0, 0, GM.screen.get_width(), GM.screen.get_height()
        )
        subsurface = GM.screen.subsurface(subsurface_rect)
        
        streched = pygame.transform.scale(
            subsurface, (GM._scr.get_width(), GM._scr.get_height())
        )
        GM._scr.blit(streched, (0, 0))
        pygame.display.flip()
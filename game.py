import copy
import sys

import numpy as np
import pygame
from pygame.locals import *

from ai import Ai
from game_manager import GameManager as GM
from music_player import MusicPlayer


class Game:
    def __init__(
        self,
        menu,
        player_menu,
        player,
        assets,
    ):
        self.asets = assets
        self.menu = menu
        
        self.player = player
        self.items = assets.load_items()
        self.player_menu = player_menu

        self.relative_player_top = 0
        self.relative_player_left = 0
        self.relative_player_right = 0
        self.relative_player_bottom = 0

        self.prompt_font = pygame.font.Font("fonts/SovngardeBold.ttf", 20)
        self.subtitle_font = pygame.font.Font("fonts/SovngardeBold.ttf", 28)
        self.menu_font = pygame.font.Font("fonts/SovngardeBold.ttf", 34)

        self.player.inventory.add_item(self.items["Minor Health Potion"])
        self.player.inventory.add_item(self.items["Knowledge Potion"])
        self.player.inventory.add_item(self.items["Power Elixir"])
        self.player.inventory.add_item(self.items["Steel Sword"])
        self.player.inventory.add_item(self.items["Steel Armor"])
        self.player.inventory.add_item(self.items["Divine Armor"])
        self.worlds = assets.load_worlds()
        self.music_player = MusicPlayer(self.worlds[self.player.current_world]["music"])
        self.world_objects = list()

        temp = self.setup()
        self.ai = Ai(temp, assets, self.music_player)
        self.player.quests.dialogue = self.ai.strings
        self.clock = pygame.time.Clock()
        self.target_fps = 60
        self.last_frame_time = pygame.time.get_ticks()
        self.on_a_diagonal = False
        self.weapon_rect = pygame.Rect(
            self.player.player_rect.left + self.player.player_rect.width // 4,
            self.player.player_rect.top - self.player.range // 2,
            16,
            self.player.range,
        )

        self.bg_menu = pygame.Rect(
            0,
            0,
            GM.screen.get_width(),
            GM.screen.get_height(),
        )

        self.bg_surface_menu = pygame.Surface(
            (self.bg_menu.width, self.bg_menu.height), pygame.SRCALPHA
        )

    def setup(self):
        self.world_objects.clear()
        self.background, self.bg_rect = self.asets.load_background(
            self.worlds[self.player.current_world]["background"]
        )
        self.collision_map = self.asets.load_collision(
            self.worlds[self.player.current_world]["collision_set"]
        )

        self.map_height = self.collision_map.shape[0]
        self.map_width = self.collision_map.shape[1]

        level_data = self.asets.load_level_data(
            self.worlds[self.player.current_world]["data"]
        )
        
        spawn_point = (0, 0)
        for i in level_data["entities"]["Player_spawn"]:
            if i["customFields"]["type"] == "default":
                spawn_point = (i["x"], i["y"])
                break

        offset = (
            spawn_point[0] - GM.screen.get_width() // 2,
            spawn_point[1] - GM.screen.get_height() // 2,
        )
        
        self.bg_rect.left = -offset[0]
        self.bg_rect.top = -offset[1]
        
        self.player.player_rect.left = spawn_point[0]-offset[0]
        self.player.player_rect.top = spawn_point[1]-offset[1]

        for data in self.worlds[self.player.current_world]["items"]:
            item = self.items[data["type"]]
            img, img_rect = self.asets.load_images(
                item["image"], (64, 64), tuple(data["position"])
            )
            self.world_objects.append(
                {
                    "name": item["name"],
                    "image": img,
                    "rect": img_rect,
                    "type": "item",
                }
            )

        for data in self.worlds[self.player.current_world]["containers"]:
            img, img_rect = self.asets.load_images(
                data["image"], (64, 64), tuple(data["position"])
            )
            self.world_objects.append(
                {
                    "image": img,
                    "rect": img_rect,
                    "type": "container",
                    "name": copy.deepcopy(data),
                }
            )

        for data in self.worlds[self.player.current_world]["npcs"]:
            img, img_rect = self.asets.load_images(
                data["image"], (64, 64), tuple(data["position"])
            )
            self.world_objects.append(
                {
                    "image": img,
                    "rect": img_rect,
                    "type": "npc",
                    "name": copy.deepcopy(data),
                    "attack_diff": 0,
                    "agroved": False,
                }
            )

        for data in self.worlds[self.player.current_world]["portals"]:
            img, img_rect = self.asets.load_images(
                data["image"], (64, 64), tuple(data["position"])
            )
            self.world_objects.append(
                {
                    "image": img,
                    "rect": img_rect,
                    "type": "portal",
                    "name": copy.deepcopy(data),
                }
            )

        temp = {}
        for x in self.world_objects:
            if x["type"] == "npc":
                temp[x["name"]["name"]] = copy.deepcopy(x["name"])

        return temp

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

            self.update()
            self.handle_events()
            self.draw()
            self.music_player.update()
            self.player.check_experation(GM.delta_time)
            if (
                not self.player_menu.visible
                and not GM.tab_pressed
                and not GM.container_open
                and not GM.is_in_dialogue
            ):
                self.menu.handle_input()

            if (
                not self.menu.visible
                and not GM.tab_pressed
                and not GM.container_open
                and not GM.is_in_dialogue
            ):
                self.player_menu.handle_input()

            if (
                GM.is_in_dialogue
                and not GM.tab_pressed
                and not GM.container_open
                and not self.player_menu.visible
                and not self.menu.visible
            ):
                self.ai.strings.handle_input()
                if self.ai.strings.starts != 0:
                    self.player.quests.start_quest(self.ai.strings.starts)
                    self.ai.strings.starts = 0

                if self.ai.strings.advances != 0:
                    self.player.quests.advance_quest(self.ai.strings.advances)
                    self.ai.strings.advances = 0

            self.clock.tick(self.target_fps)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def update(self):
        # na lestvici 1-10 kako bi ocenili Saro Dugi iz ITK?
        if GM.time_diff >= 20:
            GM.time_diff = 5

        self.relative_player_left = int(
            self.player.player_rect.left - self.bg_rect.left
        )

        self.relative_player_right = int(
            self.player.player_rect.right - self.bg_rect.left
        )

        self.relative_player_top = int(self.player.player_rect.top - self.bg_rect.top)

        self.relative_player_bottom = int(
            self.player.player_rect.bottom - self.bg_rect.top
        )
        movement = int(self.player.movement_speed * GM.delta_time)

        self.player.quests.check_quest_advancement(
            (
                self.relative_player_top + self.player.player_rect.height // 2,
                self.relative_player_left + self.player.player_rect.width // 2,
            ),
            self.player.current_world,
        )

        keys = pygame.key.get_pressed()
        if self.player.player_rect.left <= 10:
            self.bg_rect.move_ip(movement, 0)
            self.player.player_rect.move_ip(movement, 0)

        if self.player.player_rect.right >= GM.screen_width - 10:
            self.bg_rect.move_ip(-movement, 0)
            self.player.player_rect.move_ip(-movement, 0)
        if self.player.player_rect.top <= 10:
            self.bg_rect.move_ip(0, movement)
            self.player.player_rect.move_ip(0, movement)
        if self.player.player_rect.bottom >= GM.screen_height - 10:
            self.bg_rect.move_ip(0, -movement)
            self.player.player_rect.move_ip(0, -movement)

        GM.moving = False
        if (
            keys[pygame.K_a]
            and np.count_nonzero(
                self.collision_map[
                    self.relative_player_top : self.relative_player_bottom,
                    self.relative_player_left - movement,
                ]
                == 1
            )
            <= 1
            and not self.menu.visible
            and not self.player_menu.visible
            and not GM.container_open
            and not GM.is_in_dialogue
        ):
            if self.player.player_rect.left > 10:
                self.player.player_rect.move_ip(-movement, 0)
                if GM.rotation_angle != 90:
                    GM.rotation_angle = 90 - GM.rotation_angle
                    # self.player.player = pygame.transform.rotate(self.player.player, GM.rotation_angle)
                    GM.rotation_angle = 90
                GM.moving = True

        elif (
            keys[pygame.K_a]
            and not self.menu.visible
            and not self.player_menu.visible
            and not GM.container_open
            and not GM.is_in_dialogue
        ):
            dx = np.count_nonzero(
                self.collision_map[
                    self.relative_player_bottom,
                    self.relative_player_left
                    - movement * 2 : self.relative_player_left,
                ]
            )
            dt = np.count_nonzero(
                self.collision_map[
                    self.relative_player_top,
                    self.relative_player_left
                    - movement * 2 : self.relative_player_left,
                ]
            )
            dy = np.count_nonzero(
                self.collision_map[
                    self.relative_player_top : self.relative_player_bottom,
                    self.relative_player_left - movement * 2,
                ]
            )

            angle = np.arctan2(dy, dt if dt > dx else dx)

            # print(np.rad2deg(angle))
            if (
                np.rad2deg(angle) < 70
                and np.count_nonzero(
                    self.collision_map[
                        self.relative_player_left : self.relative_player_right,
                        self.relative_player_top : self.relative_player_bottom,
                    ]
                )
                <= 5
            ):
                move_direction = -1 if dt < dx else 1
                self.player.player_rect.move_ip(
                    int(-movement * np.cos(angle)),
                    int(move_direction * movement * np.sin(angle)),
                )
                self.on_a_diagonal = True
                if GM.rotation_angle != 90:
                    GM.rotation_angle = 90 - GM.rotation_angle
                    # self.player.player = pygame.transform.rotate(self.player.player, GM.rotation_angle)
                    GM.rotation_angle = 90
                self.on_a_diagonal = True
                GM.moving = True

        if (
            keys[pygame.K_d]
            and np.count_nonzero(
                self.collision_map[
                    self.relative_player_top : self.relative_player_bottom,
                    min(self.relative_player_right + movement, self.map_width - 1),
                ]
                == 1
            )
            <= 1
            and not self.menu.visible
            and not self.player_menu.visible
            and not GM.container_open
            and not GM.is_in_dialogue
        ):
            if self.player.player_rect.right < GM.screen_width - 10:
                self.player.player_rect.move_ip(movement, 0)
                if GM.rotation_angle != 270:
                    GM.rotation_angle = 270 - GM.rotation_angle
                    # self.player.player = pygame.transform.rotate(self.player.player, GM.rotation_angle)
                    GM.rotation_angle = 270
                GM.moving = True

        elif (
            keys[pygame.K_d]
            and not self.menu.visible
            and not self.player_menu.visible
            and not GM.container_open
            and not GM.is_in_dialogue
        ):
            dx = np.count_nonzero(
                self.collision_map[
                    self.relative_player_bottom,
                    self.relative_player_right : self.relative_player_right
                    + movement * 2,
                ]
            )
            dt = np.count_nonzero(
                self.collision_map[
                    self.relative_player_top,
                    self.relative_player_right : self.relative_player_right
                    + movement * 2,
                ]
            )
            dy = np.count_nonzero(
                self.collision_map[
                    self.relative_player_top : self.relative_player_bottom,
                    self.relative_player_right + movement * 2,
                ]
            )

            angle = np.arctan2(dy, dt if dt > dx else dx)

            # print(np.rad2deg(angle))
            if (
                np.rad2deg(angle) < 70
                and np.count_nonzero(
                    self.collision_map[
                        self.relative_player_left : self.relative_player_right,
                        self.relative_player_top : self.relative_player_bottom,
                    ]
                )
                <= 5
            ):
                move_direction = -1 if dt < dx else 1
                self.player.player_rect.move_ip(
                    int(movement * np.cos(angle)),
                    int(move_direction * movement * np.sin(angle)),
                )
                if GM.rotation_angle != 270:
                    GM.rotation_angle = 270 - GM.rotation_angle
                    # self.player.player = pygame.transform.rotate(self.player.player, GM.rotation_angle)
                    GM.rotation_angle = 270
                self.on_a_diagonal = True
                GM.moving = True

        if (
            keys[pygame.K_w]
            and np.count_nonzero(
                self.collision_map[
                    self.relative_player_top - movement,
                    self.relative_player_left : self.relative_player_right,
                ]
                == 1
            )
            <= 1
            and not self.menu.visible
            and not self.player_menu.visible
            and not GM.container_open
            and not GM.is_in_dialogue
        ):
            if self.player.player_rect.top > 10:
                self.player.player_rect.move_ip(0, -movement)
                if GM.rotation_angle != 0:
                    GM.rotation_angle = 0 - GM.rotation_angle
                    # self.player.player = pygame.transform.rotate(self.player.player, GM.rotation_angle)
                    GM.rotation_angle = 0
                GM.moving = True

        elif (
            keys[pygame.K_w]
            and not self.menu.visible
            and not self.player_menu.visible
            and not GM.container_open
            and not GM.is_in_dialogue
        ):
            dx = np.count_nonzero(
                self.collision_map[
                    self.relative_player_top - movement * 2 : self.relative_player_top,
                    self.relative_player_right,
                ]
            )
            dt = np.count_nonzero(
                self.collision_map[
                    self.relative_player_top - movement * 2 : self.relative_player_top,
                    self.relative_player_left,
                ]
            )
            dy = np.count_nonzero(
                self.collision_map[
                    self.relative_player_top - movement * 2,
                    self.relative_player_left : self.relative_player_right,
                ]
            )

            angle = np.arctan2(dy, dt if dt > dx else dx)

            if (
                np.rad2deg(angle) < 70
                and np.count_nonzero(
                    self.collision_map[
                        self.relative_player_left : self.relative_player_right,
                        self.relative_player_top : self.relative_player_bottom,
                    ]
                )
                <= 5
            ):
                move_direction_X = -1 if dt < dx else 1
                move_direction_Y = -1 if dt > dx else 1
                self.player.player_rect.move_ip(
                    int(movement * np.cos(angle) * move_direction_X),
                    int(movement * move_direction_Y * np.sin(angle)),
                )
                if GM.rotation_angle != 0:
                    GM.rotation_angle = 0 - GM.rotation_angle
                    # self.player.player = pygame.transform.rotate(self.player.player, GM.rotation_angle)
                    GM.rotation_angle = 0
                self.on_a_diagonal = True
                GM.moving = True

        if (
            keys[pygame.K_s]
            and np.count_nonzero(
                self.collision_map[
                    min(self.relative_player_bottom + movement, self.map_height - 1),
                    self.relative_player_left : self.relative_player_right,
                ]
                == 1
            )
            <= 1
            and not self.menu.visible
            and not self.player_menu.visible
            and not GM.container_open
            and not GM.is_in_dialogue
        ):
            if self.player.player_rect.bottom < GM.screen_height - 10:
                self.player.player_rect.move_ip(0, movement)
                if GM.rotation_angle != 180:
                    GM.rotation_angle = 180 - GM.rotation_angle
                    # self.player.player = pygame.transform.rotate(self.player.player, GM.rotation_angle)
                    GM.rotation_angle = 180
                GM.moving = True

        elif (
            keys[pygame.K_s]
            and not self.menu.visible
            and not self.player_menu.visible
            and not GM.container_open
            and not GM.is_in_dialogue
        ):
            dx = np.count_nonzero(
                self.collision_map[
                    self.relative_player_bottom : self.relative_player_bottom
                    + movement * 2,
                    self.relative_player_right,
                ]
            )
            dt = np.count_nonzero(
                self.collision_map[
                    self.relative_player_bottom : self.relative_player_bottom
                    + movement * 2,
                    self.relative_player_left,
                ]
            )
            dy = np.count_nonzero(
                self.collision_map[
                    self.relative_player_bottom + movement * 2,
                    self.relative_player_left : self.relative_player_right,
                ]
            )

            angle = np.arctan2(dy, dt if dt > dx else dx)

            if (
                np.rad2deg(angle) < 70
                and np.count_nonzero(
                    self.collision_map[
                        self.relative_player_left : self.relative_player_right,
                        self.relative_player_top : self.relative_player_bottom,
                    ]
                )
                <= 5
            ):
                move_direction_X = -1 if dt < dx else 1
                move_direction_Y = -1 if dt > dx else 1
                self.player.player_rect.move_ip(
                    int(movement * np.cos(angle) * move_direction_X),
                    int(movement * move_direction_Y * np.sin(angle)),
                )
                if GM.rotation_angle != 180:
                    GM.rotation_angle = 180 - GM.rotation_angle
                    # self.player.player = pygame.transform.rotate(self.player.player, GM.rotation_angle)
                    GM.rotation_angle = 180
                self.on_a_diagonal = True
                GM.moving = True

        if (
            keys[pygame.K_e]
            and not self.menu.visible
            and not self.player_menu.visible
            and not GM.selection_held
        ):
            if GM.item_hovered != None:
                GM.selection_held = True
                if (
                    GM.item_hovered < len(self.world_objects)
                    and GM.item_hovered >= 0
                ):
                    self.player.add_item(
                        self.items[self.world_objects[GM.item_hovered]["name"]]
                    )
                    del self.world_objects[GM.item_hovered]
                    GM.item_hovered = None

            elif GM.container_hovered != None and not GM.container_open:
                GM.selection_held = True
                if (
                    GM.container_hovered < len(self.world_objects)
                    and GM.container_hovered >= 0
                ):
                    GM.container_open = True

            elif GM.is_ready_to_talk:
                GM.selection_held = True
                GM.is_ready_to_talk = False
                GM.is_in_dialogue = True

            elif GM.world_to_travel_to != None and (
                not GM.world_to_travel_to["locked"]
                or self.player.inventory.items.get(
                    GM.world_to_travel_to["unlocked_by"], "None"
                )
                != "None"
            ):
                self.loading()
                self.player.current_world = GM.world_to_travel_to["world"]
                self.world_objects[GM.world_to_travel_to["index"]]["name"][
                    "locked"
                ] = False

                self.worlds[self.player.current_world]["offset"][
                    0
                ] = GM.world_to_travel_to["offset"][0]
                self.worlds[self.player.current_world]["offset"][
                    1
                ] = GM.world_to_travel_to["offset"][1]

                self.worlds[self.player.current_world]["spawn_point"][
                    0
                ] = GM.world_to_travel_to["spawn_point"][0]
                self.worlds[self.player.current_world]["spawn_point"][
                    1
                ] = GM.world_to_travel_to["spawn_point"][1]

                GM.world_to_travel_to = None
                temp = self.setup()
                self.ai.update_npcs(temp)
                self.player.quests.dialogue = self.ai.strings
                self.music_player.set_tracks(
                    self.worlds[self.player.current_world]["music"]
                )

        elif (
            not keys[pygame.K_e]
            and not GM.container_open
            and not self.ai.strings.bartering
        ):
            GM.selection_held = False

        if (
            keys[pygame.K_TAB]
            and not self.menu.visible
            and not self.player_menu.visible
            and not GM.tab_pressed
        ):
            GM.tab_pressed = True
            GM.container_open = False

            if self.ai.strings.bartering:
                self.ai.strings.bartering = False
                return

            if GM.is_in_dialogue:
                GM.is_in_dialogue = False
                self.ai.strings.index = -1
                self.ai.strings.greeting_played = False
                self.ai.strings.talking = False
                self.ai.strings.music_player.skip_current_line()

        elif not keys[pygame.K_TAB] and not GM.container_open and GM.tab_pressed:
            GM.tab_pressed = False
            GM.prev_index = 0
            GM.selected_inventory_item = 0

        if (
            keys[pygame.K_UP]
            and not GM.selection_held
            and (GM.container_open or self.ai.strings.bartering)
            and not self.menu.visible
            and not self.player_menu.visible
        ):
            if (
                GM.container_menu_selected
                and self.ai.strings.bartering
                and len(self.ai.ai_package[GM.talk_to_name]["items"])
            ):
                GM.selected_inventory_item = (GM.selected_inventory_item - 1) % len(
                    self.ai.ai_package[GM.talk_to_name]["items"]
                )
                GM.selection_held = True
                return

            elif len(self.player.inventory.items) and self.ai.strings.bartering:
                GM.selected_inventory_item = (GM.selected_inventory_item - 1) % len(
                    self.player.inventory.items
                )
                GM.selection_held = True
                return

            if (
                GM.container_menu_selected
                and GM.container_open
                and len(self.world_objects[GM.container_hovered]["name"]["items"])
            ):
                GM.selected_inventory_item = (GM.selected_inventory_item - 1) % len(
                    self.world_objects[GM.container_hovered]["name"]["items"]
                )
                GM.selection_held = True

            elif len(self.player.inventory.items) and GM.container_open:
                GM.selected_inventory_item = (GM.selected_inventory_item - 1) % len(
                    self.player.inventory.items
                )
                GM.selection_held = True

        elif (
            keys[pygame.K_DOWN]
            and not GM.selection_held
            and (GM.container_open or self.ai.strings.bartering)
            and not self.menu.visible
            and not self.player_menu.visible
        ):
            if (
                GM.container_menu_selected
                and self.ai.strings.bartering
                and len(self.ai.ai_package[GM.talk_to_name]["items"])
            ):
                GM.selected_inventory_item = (GM.selected_inventory_item + 1) % len(
                    self.ai.ai_package[GM.talk_to_name]["items"]
                )
                GM.selection_held = True
                return

            elif len(self.player.inventory.items) and self.ai.strings.bartering:
                GM.selected_inventory_item = (GM.selected_inventory_item + 1) % len(
                    self.player.inventory.items
                )
                GM.selection_held = True
                return

            if GM.container_menu_selected and len(
                self.world_objects[GM.container_hovered]["name"]["items"]
            ):
                GM.selected_inventory_item = (GM.selected_inventory_item + 1) % len(
                    self.world_objects[GM.container_hovered]["name"]["items"]
                )
                GM.selection_held = True
            elif len(self.player.inventory.items):
                GM.selected_inventory_item = (GM.selected_inventory_item + 1) % len(
                    self.player.inventory.items
                )
                GM.selection_held = True

        if (
            keys[pygame.K_LEFT]
            and not GM.selection_held
            and (GM.container_open or self.ai.strings.bartering)
            and not self.menu.visible
            and not self.player_menu.visible
            and GM.container_menu_selected
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
            and (GM.container_open or self.ai.strings.bartering)
            and not self.menu.visible
            and not self.player_menu.visible
            and not GM.container_menu_selected
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
            and (GM.container_open or self.ai.strings.bartering)
        ):
            GM.selection_held = False

        if (
            keys[pygame.K_RETURN]
            and not self.menu.visible
            and not self.player_menu.visible
            and not GM.selection_held
            and (GM.container_open or self.ai.strings.bartering)
        ):
            GM.selection_held = True

            if self.ai.strings.bartering:
                if (
                    GM.container_menu_selected
                    and len(self.ai.ai_package[GM.talk_to_name]["items"]) > 0
                ):
                    if (
                        self.ai.ai_package[GM.talk_to_name]["items"][
                            GM.selected_inventory_item
                        ]["quantity"]
                        > 0
                        and self.player.gold
                        >= self.items[
                            self.ai.ai_package[GM.talk_to_name]["items"][
                                GM.selected_inventory_item
                            ]["type"]
                        ]["price"]
                    ):
                        self.player.gold -= self.items[
                            self.ai.ai_package[GM.talk_to_name]["items"][
                                GM.selected_inventory_item
                            ]["type"]
                        ]["price"]
                        self.ai.ai_package[GM.talk_to_name]["gold"] += self.items[
                            self.ai.ai_package[GM.talk_to_name]["items"][
                                GM.selected_inventory_item
                            ]["type"]
                        ]["price"]
                        self.ai.ai_package[GM.talk_to_name]["items"][
                            GM.selected_inventory_item
                        ]["quantity"] -= 1
                        self.player.inventory.add_item(
                            self.items[
                                self.ai.ai_package[GM.talk_to_name]["items"][
                                    GM.selected_inventory_item
                                ]["type"]
                            ]
                        )
                        if (
                            self.ai.ai_package[GM.talk_to_name]["items"][
                                GM.selected_inventory_item
                            ]["quantity"]
                            == 0
                        ):
                            del self.ai.ai_package[GM.talk_to_name]["items"][
                                GM.selected_inventory_item
                            ]

                elif (
                    not GM.container_menu_selected
                    and len(self.player.inventory.items) > 0
                ):
                    if self.ai.ai_package[GM.talk_to_name]["gold"] <= 0:
                        self.ai.ai_package[GM.talk_to_name]["gold"] = 0
                    key = list(self.player.inventory.quantity.keys())[
                        GM.selected_inventory_item
                    ]
                    item_index = next(
                        (
                            index
                            for index, item in enumerate(
                                self.ai.ai_package[GM.talk_to_name]["items"]
                            )
                            if item["type"] == key
                        ),
                        None,
                    )

                    if item_index != None:
                        self.ai.ai_package[GM.talk_to_name]["items"][item_index][
                            "quantity"
                        ] += 1

                    else:
                        self.ai.ai_package[GM.talk_to_name]["items"].append(
                            {"type": key, "quantity": 1}
                        )
                    self.player.inventory.remove_item(key)
                    self.player.gold += self.items[key]["price"]
                    self.ai.ai_package[GM.talk_to_name]["gold"] -= self.items[key][
                        "price"
                    ]

                if (
                    GM.selected_inventory_item > len(self.player.inventory.items) - 1
                    and not GM.container_menu_selected
                ):
                    GM.selected_inventory_item = len(self.player.inventory.items) - 1

                elif (
                    GM.selected_inventory_item
                    > len(self.ai.ai_package[GM.talk_to_name]["items"]) - 1
                    and GM.container_menu_selected
                ):
                    GM.selected_inventory_item = (
                        len(self.ai.ai_package[GM.talk_to_name]["items"]) - 1
                    )
                    if GM.selected_inventory_item < 0:
                        GM.selected_inventory_item = 0

                if GM.selected_inventory_item < 0:
                    GM.selected_inventory_item = 0
                return

            if (
                GM.container_menu_selected
                and len(self.world_objects[GM.container_hovered]["name"]["items"]) > 0
            ):
                if (
                    self.world_objects[GM.container_hovered]["name"]["items"][
                        GM.selected_inventory_item
                    ]["type"]
                    == "Gold"
                ):
                    self.player.gold += self.world_objects[GM.container_hovered][
                        "name"
                    ]["items"][GM.selected_inventory_item]["quantity"]
                    del self.world_objects[GM.container_hovered]["name"]["items"][
                        GM.selected_inventory_item
                    ]

                elif (
                    self.world_objects[GM.container_hovered]["name"]["items"][
                        GM.selected_inventory_item
                    ]["quantity"]
                    > 0
                ):
                    self.world_objects[GM.container_hovered]["name"]["items"][
                        GM.selected_inventory_item
                    ]["quantity"] -= 1
                    self.player.add_item(
                        self.items[
                            self.world_objects[GM.container_hovered]["name"]["items"][
                                GM.selected_inventory_item
                            ]["type"]
                        ]
                    )
                    if (
                        self.world_objects[GM.container_hovered]["name"]["items"][
                            GM.selected_inventory_item
                        ]["quantity"]
                        == 0
                    ):
                        del self.world_objects[GM.container_hovered]["name"]["items"][
                            GM.selected_inventory_item
                        ]

            elif (
                not GM.container_menu_selected
                and len(self.player.inventory.items) > 0
            ):
                key = list(self.player.inventory.quantity.keys())[
                    GM.selected_inventory_item
                ]
                item_index = next(
                    (
                        index
                        for index, item in enumerate(
                            self.world_objects[GM.container_hovered]["name"]["items"]
                        )
                        if item["type"] == key
                    ),
                    None,
                )

                if item_index != None:
                    self.world_objects[GM.container_hovered]["name"]["items"][
                        item_index
                    ]["quantity"] += 1
                else:
                    self.world_objects[GM.container_hovered]["name"]["items"].append(
                        {"type": key, "quantity": 1}
                    )
                self.player.inventory.remove_item(key)

            if (
                GM.selected_inventory_item > len(self.player.inventory.items) - 1
                and not GM.container_menu_selected
            ):
                GM.selected_inventory_item = len(self.player.inventory.items) - 1

            elif (
                GM.selected_inventory_item
                > len(self.world_objects[GM.container_hovered]["name"]["items"]) - 1
                and GM.container_menu_selected
            ):
                GM.selected_inventory_item = (
                    len(self.world_objects[GM.container_hovered]["name"]["items"]) - 1
                )

            if GM.selected_inventory_item < 0:
                GM.selected_inventory_item = 0

        if (
            keys[pygame.K_r]
            and self.player_menu.selected_item == 0
            and not GM.r_pressed
            and not GM.selection_held
            and self.player_menu.visible
        ):
            GM.r_pressed = True
            key = list(self.player.inventory.quantity.keys())[
                self.player_menu.selected_sub_item
            ]
            self.player.unequip_item(key)
            ret = self.player.remove_item(key)
            if ret:
                img, img_rect = self.asets.load_images(
                    self.items[key]["image"],
                    (64, 64),
                    (
                        self.relative_player_left + self.player.player_rect.width // 2,
                        self.relative_player_top + self.player.player_rect.height // 2,
                    ),
                )
                self.world_objects.append(
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
            and not self.menu.visible
            and not self.player_menu.visible
            and not GM.attacking
            and not GM.attack_button_held
            and not GM.is_in_dialogue
        ):
            timedif = 0
            if self.player.equipped_items["hand"] != None:
                weapon = self.player.inventory.items[self.player.equipped_items["hand"]]
                timedif = weapon["stats"]["speed"]
            else:
                timedif = 0.3

            if GM.time_diff >= timedif and not GM.attacking:
                GM.attacking = True
                GM.attack_button_held = True
                print(f"attacked with a: {self.player.equipped_items['hand']}")
                GM.time_diff = 0
                self.diff = pygame.time.get_ticks()

        elif GM.attacking:
            print("no longer attacking")
            GM.attacking = False

        if (
            not mouse_buttons[0]
            and not keys[pygame.K_SPACE]
            and GM.attack_button_held
        ):
            GM.attack_button_held = False

        if keys[pygame.K_o]:
            print(self.worlds)

        if GM.rotation_angle == 90:
            self.weapon_rect = pygame.Rect(
                self.player.player_rect.left - self.player.range // 2,
                self.player.player_rect.top + self.player.player_rect.height // 2,
                self.player.range,
                self.player.player_rect.height // 4,
            )
        elif GM.rotation_angle == 0:
            self.weapon_rect = pygame.Rect(
                self.player.player_rect.left + self.player.player_rect.width // 4,
                self.player.player_rect.top - self.player.range // 2,
                16,
                self.player.range,
            )
        elif GM.rotation_angle == 180:
            self.weapon_rect = pygame.Rect(
                self.player.player_rect.left + self.player.player_rect.width // 4,
                self.player.player_rect.bottom - self.player.range // 2,
                16,
                self.player.range,
            )
        elif GM.rotation_angle == 270:
            self.weapon_rect = pygame.Rect(
                self.player.player_rect.right - self.player.range // 2,
                self.player.player_rect.top + self.player.player_rect.height // 2,
                self.player.range,
                self.player.player_rect.height // 4,
            )

    def draw_container(self):
        if GM.container_open:
            pygame.draw.rect(
                self.bg_surface_menu,
                (200, 210, 200, 180),
                self.bg_surface_menu.get_rect(),
            )
            GM.screen.blit(self.bg_surface_menu, self.bg_menu)

            pygame.draw.line(
                GM.screen,
                (22, 22, 22),
                (GM.screen.get_width() // 2, 0),
                (GM.screen.get_width() // 2, GM.screen.get_height()),
                4,
            )

            scroll_position = (GM.selected_inventory_item // 10) * 10
            visible_items = list(
                self.world_objects[GM.container_hovered]["name"]["items"]
            )[scroll_position : scroll_position + 10]
            i = 0

            item_render = self.menu_font.render(
                self.player.name,
                True,
                (44, 53, 57),
            )
            item_rect = item_render.get_rect(
                topleft=(
                    GM.screen.get_width() // 2 - GM.screen.get_width() // 3,
                    20 + i * 50,
                )
            )
            GM.screen.blit(item_render, item_rect)

            item_render = self.menu_font.render(
                self.world_objects[GM.container_hovered]["name"]["name"],
                True,
                (44, 53, 57),
            )
            item_rect = item_render.get_rect(
                topleft=(
                    GM.screen.get_width() // 2 + GM.screen.get_width() // 5,
                    20 + i * 50,
                )
            )
            GM.screen.blit(item_render, item_rect)
            i += 1

            pygame.draw.line(
                GM.screen,
                (22, 22, 22),
                (0, 20 + i * 50),
                (GM.screen.get_width(), 20 + i * 50),
                4,
            )

            for index, (data) in enumerate(visible_items):
                color = (
                    (157, 157, 210)
                    if index == GM.selected_inventory_item - scroll_position
                    else (237, 106, 94)
                )

                if not GM.container_menu_selected:
                    color = (44, 53, 57)

                if (
                    index == GM.selected_inventory_item - scroll_position
                    and GM.container_menu_selected
                ):
                    item_text = f"> {data['type']}: {data['quantity']}"
                else:
                    item_text = f"    {data['type']}: {data['quantity']}"
                item_render = self.menu_font.render(item_text, True, color)
                item_rect = item_render.get_rect(
                    topleft=(GM.screen.get_width() // 2 + 20, 20 + (index + 2) * 40)
                )
                GM.screen.blit(item_render, item_rect)

            scroll_position = (GM.selected_inventory_item // 10) * 10
            visible_items = list(self.player.inventory.quantity.items())[
                scroll_position : scroll_position + 10
            ]

            for index, (item_name, item_quantity) in enumerate(visible_items):
                color = (
                    (157, 157, 210)
                    if index == GM.selected_inventory_item - scroll_position
                    else (237, 106, 94)
                )

                if GM.container_menu_selected:
                    color = (44, 53, 57)

                if (
                    index == GM.selected_inventory_item - scroll_position
                    and not GM.container_menu_selected
                ):
                    item_text = f"> {item_name}: {item_quantity}"
                else:
                    item_text = f"    {item_name}: {item_quantity}"

                item_render = self.menu_font.render(item_text, True, color)
                item_rect = item_render.get_rect(topleft=(10, 20 + (index + 2) * 40))
                GM.screen.blit(item_render, item_rect)

    def draw_barter(self):
        if self.ai.strings.bartering:
            pygame.draw.rect(
                self.bg_surface_menu,
                (200, 210, 200, 180),
                self.bg_surface_menu.get_rect(),
            )
            GM.screen.blit(self.bg_surface_menu, self.bg_menu)

            pygame.draw.line(
                GM.screen,
                (22, 22, 22),
                (GM.screen.get_width() // 2, 0),
                (GM.screen.get_width() // 2, GM.screen.get_height()),
                4,
            )

            scroll_position = (GM.selected_inventory_item // 10) * 10
            visible_items = list(self.ai.ai_package[GM.talk_to_name]["items"])[
                scroll_position : scroll_position + 10
            ]
            i = 0

            item_render = self.menu_font.render(
                self.player.name + "  Gold: " + str(self.player.gold),
                True,
                (44, 53, 57),
            )
            item_rect = item_render.get_rect(
                topleft=(
                    GM.screen.get_width() // 2 - GM.screen.get_width() // 2.5,
                    20 + i * 50,
                )
            )
            GM.screen.blit(item_render, item_rect)

            item_render = self.menu_font.render(
                GM.talk_to_name
                + "  Gold: "
                + str(self.ai.ai_package[GM.talk_to_name]["gold"]),
                True,
                (44, 53, 57),
            )
            item_rect = item_render.get_rect(
                topleft=(
                    GM.screen.get_width() // 2 + GM.screen.get_width() // 9,
                    20 + i * 50,
                )
            )
            GM.screen.blit(item_render, item_rect)
            i += 1

            pygame.draw.line(
                GM.screen,
                (22, 22, 22),
                (0, 20 + i * 50),
                (GM.screen.get_width(), 20 + i * 50),
                4,
            )

            for index, (data) in enumerate(visible_items):
                color = (
                    (157, 157, 210)
                    if index == GM.selected_inventory_item - scroll_position
                    else (237, 106, 94)
                )

                if not GM.container_menu_selected:
                    color = (44, 53, 57)

                if (
                    index == GM.selected_inventory_item - scroll_position
                    and GM.container_menu_selected
                ):
                    item_text = f"> {data['type']}: {data['quantity']}  {self.items[self.ai.ai_package[GM.talk_to_name]['items'][index+scroll_position]['type']]['price']}"
                else:
                    item_text = f"    {data['type']}: {data['quantity']}  {self.items[self.ai.ai_package[GM.talk_to_name]['items'][index+scroll_position]['type']]['price']}"
                item_render = self.menu_font.render(item_text, True, color)
                item_rect = item_render.get_rect(
                    topleft=(GM.screen.get_width() // 2 + 20, 20 + (index + 2) * 40)
                )
                GM.screen.blit(item_render, item_rect)

            scroll_position = (GM.selected_inventory_item // 10) * 10
            visible_items = list(self.player.inventory.quantity.items())[
                scroll_position : scroll_position + 10
            ]

            for index, (item_name, item_quantity) in enumerate(visible_items):
                color = (
                    (157, 157, 210)
                    if index == GM.selected_inventory_item - scroll_position
                    else (237, 106, 94)
                )

                if GM.container_menu_selected:
                    color = (44, 53, 57)

                if (
                    index == GM.selected_inventory_item - scroll_position
                    and not GM.container_menu_selected
                ):
                    item_text = f"> {item_name}: {item_quantity}  {self.items[item_name]['price']}"
                else:
                    item_text = f"    {item_name}: {item_quantity}  {self.items[item_name]['price']}"

                item_render = self.menu_font.render(item_text, True, color)
                item_rect = item_render.get_rect(topleft=(10, 20 + (index + 2) * 40))
                GM.screen.blit(item_render, item_rect)

    def draw_objects(self):
        for index, x in enumerate(self.world_objects):
            if (
                "status" in x["name"]
                and x["name"]["status"] == "alive"
                and x["name"]["type"] == "enemy"
                and not GM.container_open
                and not self.menu.visible
                and not self.player_menu.visible
                and not GM.is_in_dialogue
            ):
                dx, dy, agroved = self.ai.attack(
                    x["name"]["name"],
                    GM.delta_time,
                    (
                        (x["rect"].centerx),
                        (x["rect"].centery),
                    ),
                    (
                        (self.relative_player_left + self.relative_player_right) // 2,
                        (self.relative_player_top + self.relative_player_bottom) // 2,
                    ),
                    self.collision_map,
                    x["rect"],
                )

                self.world_objects[index]["agroved"] = agroved
                x["rect"].centerx = dx
                x["rect"].centery = dy
                relative__left = int(self.bg_rect.left + x["rect"].left)
                relative__top = int(self.bg_rect.top + x["rect"].top)

                other_obj_rect = pygame.Rect(
                    relative__left,
                    relative__top,
                    x["rect"].width,
                    x["rect"].height,
                )

                if self.player.player_rect.colliderect(other_obj_rect):
                    if x["attack_diff"] > x["name"]["attack_speed"]:
                        res = self.player.stats.defense - x["name"]["damage"]

                        if res > 0:
                            res = 0

                        self.player.update_health(res)
                        self.world_objects[index]["attack_diff"] = 0

                if self.world_objects[index]["attack_diff"] < 5:
                    self.world_objects[index]["attack_diff"] += GM.delta_time

            else:
                relative__left = int(self.bg_rect.left + x["rect"].left)
                relative__top = int(self.bg_rect.top + x["rect"].top)

            if (
                "status" in x["name"]
                and x["name"]["status"] == "alive"
                and not x["agroved"]
                and not GM.container_open
                and not self.menu.visible
                and not self.player_menu.visible
                and not GM.is_in_dialogue
            ):
                dx, dy = self.ai.update(
                    x["name"]["name"],
                    GM.delta_time,
                    self.collision_map,
                    x["rect"].left,
                    x["rect"].top,
                    x["rect"],
                )
                x["rect"].centerx = dx
                x["rect"].centery = dy
                relative__left = int(self.bg_rect.left + x["rect"].left)
                relative__top = int(self.bg_rect.top + x["rect"].top)

                line = self.ai.random_line(
                    (
                        (x["rect"].centerx),
                        (x["rect"].centery),
                    ),
                    (
                        (self.relative_player_left + self.relative_player_right) // 2,
                        (self.relative_player_top + self.relative_player_bottom) // 2,
                    ),
                    x["name"]["name"],
                )

                if line != None and GM.line_time < GM.counter:
                    GM.current_line = line
                    GM.line_time = (
                        self.music_player.play_line(GM.current_line["file"])
                        + GM.counter
                    )

                if GM.current_line != None and GM.line_time >= GM.counter:
                    text = self.subtitle_font.render(
                        GM.current_line["text"], True, (44, 53, 57)
                    )

                    text_rect = text.get_rect(
                        center=(
                            GM.screen.get_width() // 2,
                            GM.screen.get_height() - 50,
                        )
                    )

                    GM.screen.blit(text, text_rect)

                else:
                    GM.current_line = None

            if (
                relative__left > -80
                and relative__left < GM.screen_width + 80
                and relative__top > -80
                and relative__top < GM.screen_height + 80
            ):
                if "status" in x["name"] and x["name"]["status"] == "alive":
                    GM.screen.blit(x["image"], (relative__left, relative__top))
                elif "status" not in x["name"]:
                    GM.screen.blit(x["image"], (relative__left, relative__top))

                if x["type"] == "container":
                    self.collision_map[
                        x["rect"].top + 10 : x["rect"].bottom - 9,
                        x["rect"].left + 10 : x["rect"].right - 9,
                    ] = 1

                other_obj_rect = pygame.Rect(
                    relative__left,
                    relative__top,
                    x["rect"].width,
                    x["rect"].height,
                )

                if (
                    other_obj_rect.colliderect(self.player.player_rect)
                    and x["type"] == "item"
                ):
                    GM.item_hovered = index
                    self.text = self.prompt_font.render(f"E) Pick up", True, (0, 0, 0))
                    self.text_rect = self.text.get_rect(
                        center=(
                            relative__left + x["rect"].width // 2,
                            relative__top + x["rect"].height + 10,
                        )
                    )
                    GM.screen.blit(self.text, self.text_rect)
                elif (
                    not other_obj_rect.colliderect(self.player.player_rect)
                    and x["type"] == "item"
                    and index == GM.item_hovered
                ):
                    GM.item_hovered = None

                if (
                    other_obj_rect.colliderect(self.player.player_rect)
                    and x["type"] == "container"
                ):
                    GM.container_hovered = index
                    self.text = self.prompt_font.render(f"E) Access", True, (0, 0, 0))
                    self.text_rect = self.text.get_rect(
                        center=(
                            relative__left + x["rect"].width // 2,
                            relative__top + x["rect"].height + 10,
                        )
                    )
                    GM.screen.blit(self.text, self.text_rect)
                elif (
                    not other_obj_rect.colliderect(self.player.player_rect)
                    and x["type"] == "container"
                    and index == GM.container_hovered
                ):
                    GM.container_hovered = None

                if other_obj_rect.colliderect(self.weapon_rect) and x["type"] == "npc":
                    if GM.attacking:
                        if x["name"]["type"] != "enemy":
                            self.world_objects[index]["name"]["type"] = "enemy"
                            self.world_objects[index]["agroved"] = True

                        x["name"]["health"] = (
                            x["name"]["health"] - self.player.stats.weapon_damage
                        )

                        if x["name"]["health"] <= 0:
                            self.player.level.gain_experience(x["name"]["xp"])
                            x["name"]["status"] = "dead"
                            self.world_objects[index]["agroved"] = False
                            # del self.world_objects[index]

                    if x["name"]["type"] != "enemy" and x["name"]["status"] != "dead":
                        text = self.prompt_font.render(
                            f"E) {x['name']['name']}", True, (44, 53, 57)
                        )

                        text_rect = text.get_rect(
                            center=(
                                relative__left + x["rect"].width // 2,
                                relative__top - 10,
                            )
                        )
                        GM.talk_to_name = x["name"]["name"]
                        GM.screen.blit(text, text_rect)
                        GM.is_ready_to_talk = True

                    if x["name"]["health"] > 0 and x["name"]["type"] == "enemy":
                        text = self.prompt_font.render(
                            str(x["name"]["health"]), True, (200, 0, 0)
                        )
                        text_rect = text.get_rect(
                            center=(
                                relative__left + x["rect"].width // 2,
                                relative__top + x["rect"].height + 10,
                            )
                        )
                        GM.screen.blit(text, text_rect)

                elif (
                    not other_obj_rect.colliderect(self.weapon_rect)
                    and x["type"] == "npc"
                ):
                    GM.talk_to_name = ""
                    GM.is_ready_to_talk = False

                if (
                    x["type"] == "portal"
                    and not GM.container_open
                    and not self.menu.visible
                    and not self.player_menu.visible
                    and not GM.is_in_dialogue
                    and other_obj_rect.colliderect(self.player.player_rect)
                ):
                    if x["name"]["locked"]:
                        text = self.prompt_font.render(
                            f"Key required) {x['name']['world']} ", True, (44, 53, 57)
                        )
                    else:
                        text = self.prompt_font.render(
                            f"E) {x['name']['world']} ", True, (44, 53, 57)
                        )
                    text_rect = text.get_rect(
                        center=(
                            relative__left + x["rect"].width // 2,
                            relative__top + x["rect"].height + 10,
                        )
                    )
                    GM.world_to_travel_to = x["name"]
                    GM.world_to_travel_to["index"] = index
                    GM.screen.blit(text, text_rect)

                elif (
                    not other_obj_rect.colliderect(self.player.player_rect)
                    and x["type"] == "portal"
                ):
                    GM.world_to_travel_to = None

    def loading(self):
        font = pygame.font.Font("fonts/SovngardeBold.ttf", 34)
        text = font.render("Loading...", True, (180, 180, 180))
        text_rect = text.get_rect(
            center=(GM.screen.get_width() // 2, GM.screen.get_height() // 2.5)
        )
        GM.screen.blit(text, text_rect)
        pygame.display.flip()

    def draw(self):
        GM.screen.fill((230, 60, 20))
        GM.screen.blit(self.background, self.bg_rect.topleft)
        self.draw_objects()
        self.player.draw()  # .lulekSprulek.123.fafajMi)
        self.menu.render(self)
        self.player_menu.render()
        self.draw_container()
        self.player.quests.draw_quest_info()

        if GM.is_in_dialogue:
            self.ai.strings.draw(GM.talk_to_name)

        if self.ai.strings.bartering:
            self.draw_barter()

        #pygame.draw.rect(GM.screen, (0, 0, 0), self.weapon_rect)

        subsurface_rect = pygame.Rect(
            0, 0, GM.screen.get_width(), GM.screen.get_height()
        )

        subsurface = GM.screen.subsurface(subsurface_rect)

        streched = pygame.transform.scale(
            subsurface, (GM._scr.get_width(), GM._scr.get_height())
        )

        GM._scr.blit(streched, (0, 0))
        pygame.display.flip()

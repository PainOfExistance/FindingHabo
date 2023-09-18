import sys

import numpy as np
import pygame

from ai import Ai
from music_player import MusicPlayer


class Game:
    def __init__(
        self, screen, screen_width, screen_height, menu, player_menu, player, assets
    ):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.asets = assets
        self.menu = menu
        self.item_hovered = None
        self.selection_held = False
        self.container_hovered = None
        self.container_open = False
        self.tab_pressed = False
        self.r_pressed = False
        self.container_menu_selected = True
        self.selected_inventory_item = 0
        self.prev_index = 0
        self.time_diff = 0
        self.attacking = False
        self.attack_button_held = False
        self.delta_time = 0
        self.items = assets.load_items()
        self.player = player
        self.player_menu = player_menu
        self.current_line = None
        self.line_time = 0.0
        self.is_in_dialogue = False
        self.is_ready_to_talk = False
        self.talk_to_name = ""
        self.prompt_font = pygame.font.Font("game_data/inter.ttf", 16)
        self.subtitle_font = pygame.font.Font("game_data/inter.ttf", 24)

        self.relative_player_top = 0
        self.relative_player_left = 0
        self.relative_player_right = 0
        self.relative_player_bottom = 0

        self.player.inventory.add_item(self.items["Minor Health Potion"])
        self.player.inventory.add_item(self.items["Knowledge Potion"])
        self.player.inventory.add_item(self.items["Power Elixir"])
        self.player.inventory.add_item(self.items["Steel Sword"])
        self.player.inventory.add_item(self.items["Steel Armor"])
        self.player.inventory.add_item(self.items["Divine Armor"])
        self.worlds = assets.load_worlds()
        self.music_player = MusicPlayer(self.worlds[self.player.current_world]["music"])

        self.background, self.bg_rect = self.asets.load_background(
            self.worlds[self.player.current_world]["collision_set"]
        )
        self.collision_map = self.asets.load_collision(
            self.worlds[self.player.current_world]["background"]
        )
        self.map_height = self.collision_map.shape[0]
        self.map_width = self.collision_map.shape[1]
        self.world_objects = list()

        # self.bg_rect.topleft = (
        #    -(self.bg_rect.centerx - self.screen_width // 3),
        #    -(self.bg_rect.centery - self.screen_height // 2),
        # )
        # print(self.bg_rect.center)

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
                    "name": data,
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
                    "name": data,
                    "attack_diff": 0,
                    "agroved": False,
                }
            )

        temp = {}
        for x in self.world_objects:
            if x["type"] == "npc":
                temp[x["name"]["name"]] = x["name"]
        self.ai = Ai(temp, assets, screen, self.music_player)

        self.clock = pygame.time.Clock()
        self.target_fps = 60
        self.counter = 0
        self.last_frame_time = pygame.time.get_ticks()
        self.movement_speed = 200
        self.rotation_angle = 0
        self.weapon_rect = pygame.Rect(
            self.player.player_rect.left + self.player.player_rect.width // 3,
            self.player.player_rect.top - self.player.range,
            self.player.player_rect.width // 3,
            self.player.range,
        )

        self.bg_menu = pygame.Rect(
            0,
            0,
            self.screen.get_width(),
            self.screen.get_height(),
        )
        self.bg_surface_menu = pygame.Surface(
            (self.bg_menu.width, self.bg_menu.height), pygame.SRCALPHA
        )

    def run(self):
        while True:
            self.update()
            self.handle_events()
            self.draw()
            self.music_player.update()
            self.player.check_experation(self.delta_time)
            if (
                not self.player_menu.visible
                and not self.tab_pressed
                and not self.container_open
                and not self.is_in_dialogue
            ):
                self.menu.handle_input()

            if (
                not self.menu.visible
                and not self.tab_pressed
                and not self.container_open
                and not self.is_in_dialogue
            ):
                self.player_menu.handle_input()

            if (
                self.is_in_dialogue
                and not self.tab_pressed
                and not self.container_open
                and not self.player_menu.visible
                and not self.menu.visible
            ):
                self.ai.strings.handle_input()

            self.clock.tick(self.target_fps)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        # Calculate delta time (time since last frame)
        current_time = pygame.time.get_ticks()
        self.delta_time = (
            current_time - self.last_frame_time
        ) / 1000.0  # Convert to seconds
        self.last_frame_time = current_time
        self.time_diff += self.delta_time
        self.counter += self.delta_time
        # na lestvici 1-10 kako bi ocenili Saro Dugi iz ITK?

        if self.time_diff >= 20:
            self.time_diff = 5

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
        movement = int(self.movement_speed * self.delta_time)

        keys = pygame.key.get_pressed()
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
            and not self.container_open
            and not self.is_in_dialogue
        ):
            if self.player.player_rect.left > 10:
                self.player.player_rect.move_ip(
                    int(-self.movement_speed * self.delta_time), 0
                )
                # self.player.add_trait("Health Boost")
                if self.rotation_angle != 90:
                    self.rotation_angle = 90 - self.rotation_angle
                    self.player.player = pygame.transform.rotate(
                        self.player.player, self.rotation_angle
                    )
                    self.rotation_angle = 90
            else:
                self.bg_rect.move_ip(int(self.movement_speed * self.delta_time), 0)

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
            and not self.container_open
            and not self.is_in_dialogue
        ):
            if self.player.player_rect.right < self.screen_width - 10:
                self.player.player_rect.move_ip(
                    int(self.movement_speed * self.delta_time), 0
                )
                if self.rotation_angle != 270:
                    self.rotation_angle = 270 - self.rotation_angle
                    self.player.player = pygame.transform.rotate(
                        self.player.player, self.rotation_angle
                    )
                    self.rotation_angle = 270
            else:
                self.bg_rect.move_ip(int(-self.movement_speed * self.delta_time), 0)

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
            and not self.container_open
            and not self.is_in_dialogue
        ):
            if self.player.player_rect.top > 10:
                self.player.player_rect.move_ip(
                    0, int(-self.movement_speed * self.delta_time)
                )
                # self.player.update_health(10)
                if self.rotation_angle != 0:
                    self.rotation_angle = 0 - self.rotation_angle
                    self.player.player = pygame.transform.rotate(
                        self.player.player, self.rotation_angle
                    )
                    self.rotation_angle = 0

            else:
                self.bg_rect.move_ip(0, int(self.movement_speed * self.delta_time))

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
            and not self.container_open
            and not self.is_in_dialogue
        ):
            if self.player.player_rect.bottom < self.screen_height - 10:
                self.player.player_rect.move_ip(
                    0, int(self.movement_speed * self.delta_time)
                )
                # self.player.update_health(-10)
                if self.rotation_angle != 180:
                    self.rotation_angle = 180 - self.rotation_angle
                    self.player.player = pygame.transform.rotate(
                        self.player.player, self.rotation_angle
                    )
                    self.rotation_angle = 180
            else:
                self.bg_rect.move_ip(0, int(-self.movement_speed * self.delta_time))

        if (
            keys[pygame.K_e]
            and not self.menu.visible
            and not self.player_menu.visible
            and not self.selection_held
        ):
            if self.item_hovered != None:
                self.selection_held = True
                if (
                    self.item_hovered < len(self.world_objects)
                    and self.item_hovered >= 0
                ):
                    self.player.inventory.add_item(
                        self.items[self.world_objects[self.item_hovered]["name"]]
                    )
                    del self.world_objects[self.item_hovered]
                    self.item_hovered = None
            elif self.container_hovered != None and not self.container_open:
                self.selection_held = True
                if (
                    self.container_hovered < len(self.world_objects)
                    and self.container_hovered >= 0
                ):
                    self.container_open = True

            elif self.is_ready_to_talk:
                self.is_ready_to_talk = False
                self.is_in_dialogue = True

        elif (
            not keys[pygame.K_e]
            and not self.container_open
            and not self.ai.strings.bartering
        ):
            self.selection_held = False

        if (
            keys[pygame.K_TAB]
            and not self.menu.visible
            and not self.player_menu.visible
            and not self.tab_pressed
        ):
            self.tab_pressed = True
            self.container_open = False

            if self.ai.strings.bartering:
                self.ai.strings.bartering = False
                return

            if self.is_in_dialogue:
                self.is_in_dialogue = False
                self.ai.strings.index = -1
                self.ai.strings.greeting_played = False
                self.ai.strings.talking = False
                self.ai.strings.music_player.skip_current_line()

        elif not keys[pygame.K_TAB] and not self.container_open and self.tab_pressed:
            self.tab_pressed = False
            self.prev_index = 0
            self.selected_inventory_item = 0

        if (
            keys[pygame.K_UP]
            and not self.selection_held
            and (self.container_open or self.ai.strings.bartering)
            and not self.menu.visible
            and not self.player_menu.visible
        ):
            if (
                self.container_menu_selected
                and self.ai.strings.bartering
                and len(self.ai.ai_package[self.talk_to_name]["items"])
            ):
                self.selected_inventory_item = (self.selected_inventory_item - 1) % len(
                    self.ai.ai_package[self.talk_to_name]["items"]
                )
                self.selection_held = True
                return

            elif len(self.player.inventory.items) and self.ai.strings.bartering:
                self.selected_inventory_item = (self.selected_inventory_item - 1) % len(
                    self.player.inventory.items
                )
                self.selection_held = True
                return

            if (
                self.container_menu_selected
                and self.container_open
                and len(self.world_objects[self.container_hovered]["name"]["items"])
            ):
                self.selected_inventory_item = (self.selected_inventory_item - 1) % len(
                    self.world_objects[self.container_hovered]["name"]["items"]
                )
                self.selection_held = True

            elif len(self.player.inventory.items) and self.container_open:
                self.selected_inventory_item = (self.selected_inventory_item - 1) % len(
                    self.player.inventory.items
                )
                self.selection_held = True

        elif (
            keys[pygame.K_DOWN]
            and not self.selection_held
            and (self.container_open or self.ai.strings.bartering)
            and not self.menu.visible
            and not self.player_menu.visible
        ):
            if (
                self.container_menu_selected
                and self.ai.strings.bartering
                and len(self.ai.ai_package[self.talk_to_name]["items"])
            ):
                self.selected_inventory_item = (self.selected_inventory_item + 1) % len(
                    self.ai.ai_package[self.talk_to_name]["items"]
                )
                self.selection_held = True
                return

            elif len(self.player.inventory.items) and self.ai.strings.bartering:
                self.selected_inventory_item = (self.selected_inventory_item + 1) % len(
                    self.player.inventory.items
                )
                self.selection_held = True
                return

            if self.container_menu_selected and len(
                self.world_objects[self.container_hovered]["name"]["items"]
            ):
                self.selected_inventory_item = (self.selected_inventory_item + 1) % len(
                    self.world_objects[self.container_hovered]["name"]["items"]
                )
                self.selection_held = True
            elif len(self.player.inventory.items):
                self.selected_inventory_item = (self.selected_inventory_item + 1) % len(
                    self.player.inventory.items
                )
                self.selection_held = True

        if (
            keys[pygame.K_LEFT]
            and not self.selection_held
            and (self.container_open or self.ai.strings.bartering)
            and not self.menu.visible
            and not self.player_menu.visible
            and self.container_menu_selected
        ):
            self.container_menu_selected = False
            self.selection_held = True
            self.selected_inventory_item, self.prev_index = (
                self.prev_index,
                self.selected_inventory_item,
            )

        elif (
            keys[pygame.K_RIGHT]
            and not self.selection_held
            and (self.container_open or self.ai.strings.bartering)
            and not self.menu.visible
            and not self.player_menu.visible
            and not self.container_menu_selected
        ):
            self.container_menu_selected = True
            self.selection_held = True
            self.selected_inventory_item, self.prev_index = (
                self.prev_index,
                self.selected_inventory_item,
            )

        elif (
            not keys[pygame.K_RETURN]
            and not keys[pygame.K_UP]
            and not keys[pygame.K_DOWN]
            and not keys[pygame.K_RIGHT]
            and not keys[pygame.K_LEFT]
            and (self.container_open or self.ai.strings.bartering)
        ):
            self.selection_held = False

        if (
            keys[pygame.K_RETURN]
            and not self.menu.visible
            and not self.player_menu.visible
            and not self.selection_held
            and (self.container_open or self.ai.strings.bartering)
        ):
            self.selection_held = True

            if self.ai.strings.bartering:
                if (
                    self.container_menu_selected
                    and len(self.ai.ai_package[self.talk_to_name]["items"]) > 0
                ):
                    if (
                        self.ai.ai_package[self.talk_to_name]["items"][
                            self.selected_inventory_item
                        ]["quantity"]
                        > 0
                        and self.player.gold
                        >= self.items[
                            self.ai.ai_package[self.talk_to_name]["items"][
                                self.selected_inventory_item
                            ]["type"]
                        ]["price"]
                    ):
                        self.player.gold -= self.items[
                            self.ai.ai_package[self.talk_to_name]["items"][
                                self.selected_inventory_item
                            ]["type"]
                        ]["price"]
                        self.ai.ai_package[self.talk_to_name]["gold"] += self.items[
                            self.ai.ai_package[self.talk_to_name]["items"][
                                self.selected_inventory_item
                            ]["type"]
                        ]["price"]
                        self.ai.ai_package[self.talk_to_name]["items"][
                            self.selected_inventory_item
                        ]["quantity"] -= 1
                        self.player.inventory.add_item(
                            self.items[
                                self.ai.ai_package[self.talk_to_name]["items"][
                                    self.selected_inventory_item
                                ]["type"]
                            ]
                        )
                        if (
                            self.ai.ai_package[self.talk_to_name]["items"][
                                self.selected_inventory_item
                            ]["quantity"]
                            == 0
                        ):
                            del self.ai.ai_package[self.talk_to_name]["items"][
                                self.selected_inventory_item
                            ]

                elif (
                    not self.container_menu_selected
                    and len(self.player.inventory.items) > 0
                ):
                    if self.ai.ai_package[self.talk_to_name]["gold"] <= 0:
                        self.ai.ai_package[self.talk_to_name]["gold"] = 0
                    key = list(self.player.inventory.quantity.keys())[
                        self.selected_inventory_item
                    ]
                    item_index = next(
                        (
                            index
                            for index, item in enumerate(
                                self.ai.ai_package[self.talk_to_name]["items"]
                            )
                            if item["type"] == key
                        ),
                        None,
                    )

                    if item_index != None:
                        self.ai.ai_package[self.talk_to_name]["items"][item_index][
                            "quantity"
                        ] += 1

                    else:
                        self.ai.ai_package[self.talk_to_name]["items"].append(
                            {"type": key, "quantity": 1}
                        )
                    self.player.inventory.remove_item(key)
                    self.player.gold += self.items[key]["price"]
                    self.ai.ai_package[self.talk_to_name]["gold"] -= self.items[key][
                        "price"
                    ]

                if (
                    self.selected_inventory_item > len(self.player.inventory.items) - 1
                    and not self.container_menu_selected
                ):
                    self.selected_inventory_item = len(self.player.inventory.items) - 1

                elif (
                    self.selected_inventory_item
                    > len(self.ai.ai_package[self.talk_to_name]["items"]) - 1
                    and self.container_menu_selected
                ):
                    self.selected_inventory_item = (
                        len(self.ai.ai_package[self.talk_to_name]["items"]) - 1
                    )
                    if self.selected_inventory_item < 0:
                        self.selected_inventory_item = 0

                if self.selected_inventory_item < 0:
                    self.selected_inventory_item = 0
                return

            if (
                self.container_menu_selected
                and len(self.world_objects[self.container_hovered]["name"]["items"]) > 0
            ):
                if (
                    self.world_objects[self.container_hovered]["name"]["items"][
                        self.selected_inventory_item
                    ]["type"]
                    == "Gold"
                ):
                    self.player.gold += self.world_objects[self.container_hovered][
                        "name"
                    ]["items"][self.selected_inventory_item]["quantity"]
                    del self.world_objects[self.container_hovered]["name"]["items"][
                        self.selected_inventory_item
                    ]

                elif (
                    self.world_objects[self.container_hovered]["name"]["items"][
                        self.selected_inventory_item
                    ]["quantity"]
                    > 0
                ):
                    self.world_objects[self.container_hovered]["name"]["items"][
                        self.selected_inventory_item
                    ]["quantity"] -= 1
                    self.player.inventory.add_item(
                        self.items[
                            self.world_objects[self.container_hovered]["name"]["items"][
                                self.selected_inventory_item
                            ]["type"]
                        ]
                    )
                    if (
                        self.world_objects[self.container_hovered]["name"]["items"][
                            self.selected_inventory_item
                        ]["quantity"]
                        == 0
                    ):
                        del self.world_objects[self.container_hovered]["name"]["items"][
                            self.selected_inventory_item
                        ]

            elif (
                not self.container_menu_selected
                and len(self.player.inventory.items) > 0
            ):
                key = list(self.player.inventory.quantity.keys())[
                    self.selected_inventory_item
                ]
                item_index = next(
                    (
                        index
                        for index, item in enumerate(
                            self.world_objects[self.container_hovered]["name"]["items"]
                        )
                        if item["type"] == key
                    ),
                    None,
                )

                if item_index != None:
                    self.world_objects[self.container_hovered]["name"]["items"][
                        item_index
                    ]["quantity"] += 1
                else:
                    self.world_objects[self.container_hovered]["name"]["items"].append(
                        {"type": key, "quantity": 1}
                    )
                self.player.inventory.remove_item(key)

            if (
                self.selected_inventory_item > len(self.player.inventory.items) - 1
                and not self.container_menu_selected
            ):
                self.selected_inventory_item = len(self.player.inventory.items) - 1

            elif (
                self.selected_inventory_item
                > len(self.world_objects[self.container_hovered]["name"]["items"]) - 1
                and self.container_menu_selected
            ):
                self.selected_inventory_item = (
                    len(self.world_objects[self.container_hovered]["name"]["items"]) - 1
                )

            if self.selected_inventory_item < 0:
                self.selected_inventory_item = 0

        if (
            keys[pygame.K_r]
            and self.player_menu.selected_item == 0
            and not self.r_pressed
            and not self.selection_held
            and self.player_menu.visible
        ):
            self.r_pressed = True
            key = list(self.player.inventory.quantity.keys())[
                self.player_menu.selected_sub_item
            ]
            self.player.unequip_item(key)
            self.player.inventory.remove_item(key)
            img, img_rect = self.asets.load_images(
                self.items[key]["image"],
                (64, 64),
                (self.player.player_rect.centerx, self.player.player_rect.centery),
            )
            self.world_objects.append(
                {
                    "name": key,
                    "image": img,
                    "rect": img_rect,
                    "type": "item",
                }
            )

        elif not keys[pygame.K_r] and self.r_pressed:
            self.r_pressed = False

        mouse_buttons = pygame.mouse.get_pressed()
        if (
            (mouse_buttons[0] or keys[pygame.K_SPACE])
            and not self.menu.visible
            and not self.player_menu.visible
            and not self.attacking
            and not self.attack_button_held
            and not self.is_in_dialogue
        ):
            timedif = 0
            if self.player.equipped_items["hand"] != None:
                weapon = self.player.inventory.items[self.player.equipped_items["hand"]]
                timedif = weapon["stats"]["speed"]
            else:
                timedif = 0.3

            if self.time_diff >= timedif and not self.attacking:
                self.attacking = True
                self.attack_button_held = True
                print(f"attacked with a: {self.player.equipped_items['hand']}")
                self.time_diff = 0
                self.diff = pygame.time.get_ticks()

        elif self.attacking:
            print("no longer attacking")
            self.attacking = False

        if (
            not mouse_buttons[0]
            and not keys[pygame.K_SPACE]
            and self.attack_button_held
        ):
            self.attack_button_held = False

        if self.rotation_angle == 90:
            self.weapon_rect = pygame.Rect(
                self.player.player_rect.left - self.player.range,
                self.player.player_rect.top + self.player.player_rect.width // 3,
                self.player.range,
                self.player.player_rect.height // 3,
            )
        elif self.rotation_angle == 0:
            self.weapon_rect = pygame.Rect(
                self.player.player_rect.left + self.player.player_rect.width // 3,
                self.player.player_rect.top - self.player.range,
                self.player.player_rect.width // 3,
                self.player.range,
            )
        elif self.rotation_angle == 180:
            self.weapon_rect = pygame.Rect(
                self.player.player_rect.left + self.player.player_rect.width // 3,
                self.player.player_rect.bottom,
                self.player.player_rect.width // 3,
                self.player.range,
            )
        elif self.rotation_angle == 270:
            self.weapon_rect = pygame.Rect(
                self.player.player_rect.right,
                self.player.player_rect.top + self.player.player_rect.width // 3,
                self.player.range,
                self.player.player_rect.height // 3,
            )

    def draw_container(self):
        if self.container_open:
            pygame.draw.rect(
                self.bg_surface_menu,
                (200, 210, 200, 180),
                self.bg_surface_menu.get_rect(),
            )
            self.screen.blit(self.bg_surface_menu, self.bg_menu)

            pygame.draw.line(
                self.screen,
                (22, 22, 22),
                (self.screen.get_width() // 2, 0),
                (self.screen.get_width() // 2, self.screen.get_height()),
                4,
            )

            menu_font = pygame.font.Font("game_data/inter.ttf", 30)
            scroll_position = (self.selected_inventory_item // 10) * 10
            visible_items = list(
                self.world_objects[self.container_hovered]["name"]["items"]
            )[scroll_position : scroll_position + 10]
            i = 0

            item_render = menu_font.render(
                self.player.name,
                True,
                (44, 53, 57),
            )
            item_rect = item_render.get_rect(
                topleft=(
                    self.screen.get_width() // 2 - self.screen.get_width() // 3,
                    20 + i * 50,
                )
            )
            self.screen.blit(item_render, item_rect)

            item_render = menu_font.render(
                self.world_objects[self.container_hovered]["name"]["name"],
                True,
                (44, 53, 57),
            )
            item_rect = item_render.get_rect(
                topleft=(
                    self.screen.get_width() // 2 + self.screen.get_width() // 5,
                    20 + i * 50,
                )
            )
            self.screen.blit(item_render, item_rect)
            i += 1

            pygame.draw.line(
                self.screen,
                (22, 22, 22),
                (0, 20 + i * 50),
                (self.screen.get_width(), 20 + i * 50),
                4,
            )

            for index, (data) in enumerate(visible_items):
                color = (
                    (157, 157, 210)
                    if index == self.selected_inventory_item - scroll_position
                    else (237, 106, 94)
                )

                if not self.container_menu_selected:
                    color = (44, 53, 57)

                if (
                    index == self.selected_inventory_item - scroll_position
                    and self.container_menu_selected
                ):
                    item_text = f"> {data['type']}: {data['quantity']}"
                else:
                    item_text = f"    {data['type']}: {data['quantity']}"
                item_render = menu_font.render(item_text, True, color)
                item_rect = item_render.get_rect(
                    topleft=(self.screen.get_width() // 2 + 20, 20 + (index + 2) * 40)
                )
                self.screen.blit(item_render, item_rect)

            scroll_position = (self.selected_inventory_item // 10) * 10
            visible_items = list(self.player.inventory.quantity.items())[
                scroll_position : scroll_position + 10
            ]

            for index, (item_name, item_quantity) in enumerate(visible_items):
                color = (
                    (157, 157, 210)
                    if index == self.selected_inventory_item - scroll_position
                    else (237, 106, 94)
                )

                if self.container_menu_selected:
                    color = (44, 53, 57)

                if (
                    index == self.selected_inventory_item - scroll_position
                    and not self.container_menu_selected
                ):
                    item_text = f"> {item_name}: {item_quantity}"
                else:
                    item_text = f"    {item_name}: {item_quantity}"

                item_render = menu_font.render(item_text, True, color)
                item_rect = item_render.get_rect(topleft=(10, 20 + (index + 2) * 40))
                self.screen.blit(item_render, item_rect)

    def draw_barter(self):
        if self.ai.strings.bartering:
            pygame.draw.rect(
                self.bg_surface_menu,
                (200, 210, 200, 180),
                self.bg_surface_menu.get_rect(),
            )
            self.screen.blit(self.bg_surface_menu, self.bg_menu)

            pygame.draw.line(
                self.screen,
                (22, 22, 22),
                (self.screen.get_width() // 2, 0),
                (self.screen.get_width() // 2, self.screen.get_height()),
                4,
            )

            menu_font = pygame.font.Font("game_data/inter.ttf", 30)

            scroll_position = (self.selected_inventory_item // 10) * 10
            visible_items = list(self.ai.ai_package[self.talk_to_name]["items"])[
                scroll_position : scroll_position + 10
            ]
            i = 0

            item_render = menu_font.render(
                self.player.name + "  Gold: " + str(self.player.gold),
                True,
                (44, 53, 57),
            )
            item_rect = item_render.get_rect(
                topleft=(
                    self.screen.get_width() // 2 - self.screen.get_width() // 2.5,
                    20 + i * 50,
                )
            )
            self.screen.blit(item_render, item_rect)

            item_render = menu_font.render(
                self.talk_to_name
                + "  Gold: "
                + str(self.ai.ai_package[self.talk_to_name]["gold"]),
                True,
                (44, 53, 57),
            )
            item_rect = item_render.get_rect(
                topleft=(
                    self.screen.get_width() // 2 + self.screen.get_width() // 9,
                    20 + i * 50,
                )
            )
            self.screen.blit(item_render, item_rect)
            i += 1

            pygame.draw.line(
                self.screen,
                (22, 22, 22),
                (0, 20 + i * 50),
                (self.screen.get_width(), 20 + i * 50),
                4,
            )

            for index, (data) in enumerate(visible_items):
                color = (
                    (157, 157, 210)
                    if index == self.selected_inventory_item - scroll_position
                    else (237, 106, 94)
                )

                if not self.container_menu_selected:
                    color = (44, 53, 57)

                if (
                    index == self.selected_inventory_item - scroll_position
                    and self.container_menu_selected
                ):
                    item_text = f"> {data['type']}: {data['quantity']}  {self.items[self.ai.ai_package[self.talk_to_name]['items'][index+scroll_position]['type']]['price']}"
                else:
                    item_text = f"    {data['type']}: {data['quantity']}  {self.items[self.ai.ai_package[self.talk_to_name]['items'][index+scroll_position]['type']]['price']}"
                item_render = menu_font.render(item_text, True, color)
                item_rect = item_render.get_rect(
                    topleft=(self.screen.get_width() // 2 + 20, 20 + (index + 2) * 40)
                )
                self.screen.blit(item_render, item_rect)

            scroll_position = (self.selected_inventory_item // 10) * 10
            visible_items = list(self.player.inventory.quantity.items())[
                scroll_position : scroll_position + 10
            ]

            for index, (item_name, item_quantity) in enumerate(visible_items):
                color = (
                    (157, 157, 210)
                    if index == self.selected_inventory_item - scroll_position
                    else (237, 106, 94)
                )

                if self.container_menu_selected:
                    color = (44, 53, 57)

                if (
                    index == self.selected_inventory_item - scroll_position
                    and not self.container_menu_selected
                ):
                    item_text = f"> {item_name}: {item_quantity}  {self.items[item_name]['price']}"
                else:
                    item_text = f"    {item_name}: {item_quantity}  {self.items[item_name]['price']}"

                item_render = menu_font.render(item_text, True, color)
                item_rect = item_render.get_rect(topleft=(10, 20 + (index + 2) * 40))
                self.screen.blit(item_render, item_rect)

    def draw_objects(self):
        for index, x in enumerate(self.world_objects):
            if (
                "status" in x["name"]
                and x["name"]["status"] == "alive"
                and x["name"]["type"] == "enemy"
                and not self.container_open
                and not self.menu.visible
                and not self.player_menu.visible
                and not self.is_in_dialogue
            ):
                dx, dy, agroved = self.ai.attack(
                    x["name"]["name"],
                    self.delta_time,
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
                    self.world_objects[index]["attack_diff"] += self.delta_time

            else:
                relative__left = int(self.bg_rect.left + x["rect"].left)
                relative__top = int(self.bg_rect.top + x["rect"].top)

            if (
                "status" in x["name"]
                and x["name"]["status"] == "alive"
                and not x["agroved"]
                and not self.container_open
                and not self.menu.visible
                and not self.player_menu.visible
                and not self.is_in_dialogue
            ):
                dx, dy = self.ai.update(
                    x["name"]["name"],
                    self.delta_time,
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

                if line != None and self.line_time < self.counter:
                    self.current_line = line
                    self.line_time = (
                        self.music_player.play_line(self.current_line["file"])
                        + self.counter
                    )

                if self.current_line != None and self.line_time >= self.counter:
                    text = self.subtitle_font.render(
                        self.current_line["text"], True, (44, 53, 57)
                    )

                    text_rect = text.get_rect(
                        center=(
                            self.screen.get_width() // 2,
                            self.screen.get_height() - 50,
                        )
                    )

                    self.screen.blit(text, text_rect)

                else:
                    self.current_line = None

            if (
                relative__left > -80
                and relative__left < self.screen_width + 80
                and relative__top > -80
                and relative__top < self.screen_height + 80
            ):
                if "status" in x["name"] and x["name"]["status"] == "alive":
                    self.screen.blit(x["image"], (relative__left, relative__top))
                elif "status" not in x["name"]:
                    self.screen.blit(x["image"], (relative__left, relative__top))

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
                    self.item_hovered = index
                    self.text = self.prompt_font.render(f"E) Pick up", True, (0, 0, 0))
                    self.text_rect = self.text.get_rect(
                        center=(
                            relative__left + x["rect"].width // 2,
                            relative__top + x["rect"].height + 10,
                        )
                    )
                    self.screen.blit(self.text, self.text_rect)
                elif (
                    not other_obj_rect.colliderect(self.player.player_rect)
                    and x["type"] == "item"
                    and index == self.item_hovered
                ):
                    self.item_hovered = None

                if (
                    other_obj_rect.colliderect(self.player.player_rect)
                    and x["type"] == "container"
                ):
                    self.container_hovered = index
                    self.text = self.prompt_font.render(f"E) Access", True, (0, 0, 0))
                    self.text_rect = self.text.get_rect(
                        center=(
                            relative__left + x["rect"].width // 2,
                            relative__top + x["rect"].height + 10,
                        )
                    )
                    self.screen.blit(self.text, self.text_rect)
                elif (
                    not other_obj_rect.colliderect(self.player.player_rect)
                    and x["type"] == "container"
                    and index == self.container_hovered
                ):
                    self.container_hovered = None

                if other_obj_rect.colliderect(self.weapon_rect) and x["type"] == "npc":
                    if self.attacking:
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
                        self.talk_to_name = x["name"]["name"]
                        self.screen.blit(text, text_rect)
                        self.is_ready_to_talk = True

                    else:
                        self.talk_to_name = ""
                        self.is_ready_to_talk = False

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
                        self.screen.blit(text, text_rect)

    def draw(self):
        self.screen.fill((230, 60, 20))
        self.screen.blit(self.background, self.bg_rect.topleft)
        self.draw_objects()
        self.player.draw(self.screen)
        self.menu.render()
        self.player_menu.render()
        self.draw_container()

        if self.is_in_dialogue:
            self.ai.strings.draw(self.talk_to_name)

        if self.ai.strings.bartering:
            self.draw_barter()

        pygame.draw.rect(self.screen, (0, 0, 0), self.weapon_rect)
        pygame.display.flip()

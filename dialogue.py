import random

import numpy as np
import pygame

import asset_loader as assets
from game_manager import ClassManager as CM
from game_manager import GameManager as GM


class Dialougue:
    def __init__(self):
        self.strings = assets.load_dialogue()
        self.index = -1
        self.selected_item = 0
        self.selection_held = False
        self.name = ""
        self.current_talk = -1
        self.current_lines = -1
        self.talk = -1
        self.line = -1
        self.prev_talk = -1
        self.enabled = []
        self.indexed = []
        self.talking = False
        self.length = 0
        self.greeting_played = False
        self.bartering = False
        self.will_bartering = False
        self.starts = 0
        self.advances = 0
        
        self.subtitle_font = pygame.font.Font("fonts/SovngardeBold.ttf", 28)
        self.option_font = pygame.font.Font("fonts/SovngardeBold.ttf", 24)
        
        self.bg_menu = pygame.Rect(
            25,
            GM.screen.get_height() - 170,
            GM.screen.get_width() - 50,
            170,
        )

        self.bg_surface_menu = pygame.Surface(
            (self.bg_menu.width, self.bg_menu.height), pygame.SRCALPHA
        )

    def random_line(self, name):
        current_string = {"text": "", "dialogue": False, "file": ""}
        index = random.randint(0, len(self.strings[name]["random"]) - 1)
        line = self.strings[name]["random"][index]
        line_file = self.strings[name]["random_file"][index]
        current_string["text"] = name + ": " + line
        current_string["file"] = line_file
        return current_string

    def to_dict(self):
            
        return {
            "strings": self.strings,
            "index": self.index,
            "selected_item": self.selected_item,
            "selection_held": self.selection_held,
            "name": self.name,
            "current_talk": [-1],#list(self.current_talk),
            "current_lines": [-1],#list(self.current_lines),
            "talk": self.talk,
            "line": self.line,
            "prev_talk": self.prev_talk,
            "enabled": self.enabled,
            "talking": self.talking,
            "length": self.length,
            "greeting_played": self.greeting_played,
            "bartering": self.bartering,
            "will_bartering": self.will_bartering,
            "starts": self.starts,
            "advances": self.advances,
            "indexed": self.indexed
        }
    
    def from_dict(self, data):
        self.strings = data.get("strings")
        self.index = data.get("index", -1)
        self.selected_item = data.get("selected_item", 0)
        self.selection_held = data.get("selection_held", False)
        self.name = data.get("name", "")
        self.current_talk = iter(data.get("current_talk", -1))
        self.current_lines = iter(data.get("current_lines", -1))
        self.talk = data.get("talk", -1)
        self.line = data.get("line", -1)
        self.prev_talk = data.get("prev_talk", -1)
        self.enabled = data.get("enabled")
        self.talking = data.get("talking", False)
        self.length = data.get("length", 0)
        self.greeting_played = data.get("greeting_played", False)
        self.bartering = data.get("bartering", False)
        self.will_bartering = data.get("will_bartering", False)
        self.starts = data.get("starts", 0)
        self.advances = data.get("advances", 0)
        self.indexed = data.get("indexed", [])

    def draw(self, name):
        self.name = name

        if not self.bartering:
            pygame.draw.rect(
                self.bg_surface_menu,
                (44, 53, 57),
                (0, 0, self.bg_menu.width, self.bg_menu.height),
                border_radius=15,
            )

            pygame.draw.rect(
                self.bg_surface_menu,
                (200, 210, 200, 150),
                (5, 5, self.bg_menu.width - 10, self.bg_menu.height - 10),
                border_radius=10,
            )

            GM.screen.blit(self.bg_surface_menu, self.bg_menu)

        if self.index == -1 and not self.bartering:
            scroll_position = (self.selected_item // 4) * 4
            self.enabled.clear()
            self.indexed.clear()
            for value in self.strings[name]["enables"]:
                if(self.strings[name]["options"][value]["used"]):
                    self.enabled.append(self.strings[name]["options"][value])
                    self.indexed.append(value)

            visible_options = list(self.enabled)[scroll_position : scroll_position + 4]

            for i, value in enumerate(visible_options):
                color = (
                    (237, 106, 94)
                    if i != self.selected_item - scroll_position
                    else (44, 53, 57)
                    if self.talking == False
                    else (237, 106, 94)
                )

                if i == self.selected_item - scroll_position:
                    txt = f"> {value['text']}"
                else:
                    txt = f"    {value['text']}"

                text = self.option_font.render(txt, True, color)
                text_rect = text.get_rect(
                    center=(
                        GM.screen.get_width() // 2,
                        GM.screen.get_height() - 140 + i * 35,
                    )
                )

                GM.screen.blit(text, text_rect)

            if not self.greeting_played:
                CM.music_player.play_greeting(self.strings[name]["file"])
                self.greeting_played = True

            text = self.subtitle_font.render(
                f"{name}: {self.strings[name]['greeting']}", True, (44, 53, 57)
            )

            text_rect = text.get_rect(
                center=(
                    GM.screen.get_width() // 2,
                    GM.screen.get_height() - 200,
                )
            )

            GM.screen.blit(text, text_rect)

        elif not self.bartering:
            scroll_position = (self.selected_item // 3) * 3
            visible_options = list(self.enabled)[scroll_position : scroll_position + 3]

            for i, value in enumerate(visible_options):
                color = (
                    (237, 106, 94)
                    if i != self.selected_item - scroll_position
                    else (44, 53, 57)
                    if self.talking == False
                    else (237, 106, 94)
                )

                if not value["used"]:
                    color = (237, 106, 94)

                if i == self.selected_item - scroll_position:
                    txt = f"> {value['text']}"
                else:
                    txt = f"    {value['text']}"

                text = self.option_font.render(txt, True, color)

                text_rect = text.get_rect(
                    center=(
                        GM.screen.get_width() // 2,
                        GM.screen.get_height() - 140 + i * 35,
                    )
                )

                GM.screen.blit(text, text_rect)

            max_line_width = GM.screen.get_width()
            words = self.prev_talk.split()
            lines = []
            current_line = ""

            for word in words:
                max_chars_per_line = max_line_width // self.subtitle_font.size("J")[0]
                if len(current_line) + len(word) <= max_chars_per_line:
                    current_line += word + " "
                else:
                    lines.append(current_line)
                    current_line = word + " "

            if current_line:
                lines.append(current_line)
            lenght = len(lines) * 30 + 160

            for y, line in enumerate(lines):
                if y == 0:
                    text = self.subtitle_font.render(
                        f"{name}: {line}", True, (44, 53, 57)
                    )
                else:
                    text = self.subtitle_font.render(f"{line}", True, (44, 53, 57))

                text_rect = text.get_rect(
                    center=(
                        GM.screen.get_width() // 2,
                        GM.screen.get_height() - lenght + y * 30,
                    )
                )

                GM.screen.blit(text, text_rect)

            if not CM.music_player.get_player_status() and self.talk != -1:
                CM.music_player.play_current_line(self.line)

                if self.talk != -1 and self.talk != self.prev_talk:
                    self.prev_talk = self.talk

                self.talk = next(self.current_talk, -1)
                self.line = next(self.current_lines, -1)

            elif not CM.music_player.get_player_status() and self.talk == -1:
                self.talking = False
                if self.will_bartering:
                    self.bartering = True
                    self.will_bartering = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if not self.selection_held:
            if keys[pygame.K_l]:
                print(self.strings[self.name])
                
            if (
                keys[pygame.K_UP]
                and not self.selection_held
                and not self.talking
                and not self.bartering
            ):
                self.selected_item = (self.selected_item - 1) % len(self.enabled)
                self.selection_held = True

            elif (
                keys[pygame.K_DOWN]
                and not self.selection_held
                and not self.talking
                and not self.bartering
            ):
                self.selected_item = (self.selected_item + 1) % len(self.enabled)
                self.selection_held = True

            elif (
                keys[pygame.K_RETURN] and not self.selection_held and not self.bartering
            ):
                if self.index == -1:
                    CM.music_player.skip_current_line()
                    self.index += 1

                self.selection_held = True

                if self.talk != self.prev_talk and self.talk != -1:
                    CM.music_player.skip_current_line()
                    self.prev_talk = self.talk
                    CM.music_player.play_current_line(self.line)
                    return

                if self.talking:
                    self.talk = next(self.current_talk, -1)
                    self.line = next(self.current_lines, -1)

                if self.talking and self.talk != -1:
                    CM.music_player.skip_current_line()

                elif self.talking and self.talk == -1:
                    CM.music_player.skip_current_line()
                    self.talking = False

                elif (
                    not self.talking
                    and self.talk == -1
                    and self.strings[self.name]["options"][
                        self.indexed[self.selected_item]
                    ]["used"]
                ):
                    responce_id = self.strings[self.name]["options"][
                        self.indexed[self.selected_item]
                    ]
                    selected=self.indexed[self.selected_item]

                    if (
                        "starts"
                        in self.strings[self.name]["responses"][responce_id["res"]]
                    ):
                        self.starts = self.strings[self.name]["responses"][
                            responce_id["res"]
                        ]["starts"]
                        self.strings[self.name]["options"][
                            self.indexed[self.selected_item]
                        ]["used"] = False

                    if (
                        "advances"
                        in self.strings[self.name]["responses"][responce_id["res"]]
                    ):
                        self.advances = self.strings[self.name]["responses"][
                            responce_id["res"]
                        ]["advances"]
                        self.strings[self.name]["options"][
                            self.indexed[self.selected_item]
                        ]["used"] = False

                    self.current_talk = iter(
                        self.strings[self.name]["responses"][responce_id["res"]]["text"]
                    )
                    
                    self.current_lines = iter(
                        self.strings[self.name]["responses"][responce_id["res"]]["file"]
                    )

                    self.talk = next(self.current_talk, -1)
                    self.prev_talk = self.talk
                    self.line = next(self.current_lines, -1)

                    if (
                        "enables"
                        in self.strings[self.name]["responses"][responce_id["res"]]
                        and len(
                            self.strings[self.name]["responses"][responce_id["res"]][
                                "enables"
                            ]
                        )
                        >= 1
                    ):
                        self.enabled.clear()
                        self.indexed.clear()
                        for value in self.strings[self.name]["responses"][responce_id["res"]]["enables"]:
                            if(self.strings[self.name]["options"][value]["used"]):
                                self.enabled.append(self.strings[self.name]["options"][value])
                                self.indexed.append(value)

                    elif (
                        "barter"
                        in self.strings[self.name]["responses"][responce_id["res"]]
                    ):
                        self.will_bartering = True

                    if (
                        "enables"
                        in self.strings[self.name]["options"][
                            selected
                        ] 
                    ):
                        for value in self.strings[self.name]["options"][selected]["enables"]:
                            self.strings[self.name]["options"][value]["used"] = True
                        
                    if "disables" in self.strings[self.name]["options"][
                            selected
                        ]:
                            for value in self.strings[self.name]["options"][selected]["disables"]:
                                self.strings[self.name]["options"][value]["used"] = False
                           
                    if "script" in self.strings[self.name]["options"][selected] and not self.strings[self.name]["options"][selected]["func_used"]:
                        CM.script_loader.run_script(self.strings[self.name]["options"][selected]["script"], self.strings[self.name]["options"][selected]["function"], self.strings[self.name]["options"][selected]["args"])
                        self.strings[self.name]["options"][selected]["func_used"] = True
                    self.talking = True
                self.selected_item = 0

        elif (
            not keys[pygame.K_UP]
            and not keys[pygame.K_DOWN]
            and not keys[pygame.K_RIGHT]
            and not keys[pygame.K_LEFT]
            and not keys[pygame.K_RETURN]
        ):
            self.selection_held = False

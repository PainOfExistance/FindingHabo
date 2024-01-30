import random

import numpy as np
import pygame

from game_manager import ClassManager as CM
from game_manager import GameManager as GM


class Dialougue:
    def __init__(self,ai):
        self.strings = CM.assets.load_dialogue()
        self.ai = ai
        self.index = -1
        self.selected_item = 0
        self.selection_held = False
        self.name = ""
        self.current_talk = -1
        self.current_lines = -1
        self.talk = -1
        self.line = -1
        self.prev_talk = -1
        self.enabled = None
        self.offset = 0
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
            self.enabled = self.strings[name]["options"][
                self.strings[name]["enables"][0] : self.strings[name]["enables"][1] + 1
            ]
            self.offset = self.strings[name]["enables"][0]
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
                        self.selected_item + self.offset
                    ]["used"]
                ):
                    responce_id = self.strings[self.name]["options"][
                        self.selected_item + self.offset
                    ]
                    
                    selected=self.selected_item + self.offset

                    if (
                        "starts"
                        in self.strings[self.name]["responses"][responce_id["res"]]
                    ):
                        self.starts = self.strings[self.name]["responses"][
                            responce_id["res"]
                        ]["starts"]
                        self.strings[self.name]["options"][
                            self.selected_item + self.offset
                        ]["used"] = False

                    if (
                        "advances"
                        in self.strings[self.name]["responses"][responce_id["res"]]
                    ):
                        self.advances = self.strings[self.name]["responses"][
                            responce_id["res"]
                        ]["advances"]
                        self.strings[self.name]["options"][
                            self.selected_item + self.offset
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
                        > 1
                    ):
                        self.enabled = self.strings[self.name]["options"][
                            self.strings[self.name]["responses"][responce_id["res"]][
                                "enables"
                            ][0] : self.strings[self.name]["responses"][
                                responce_id["res"]
                            ][
                                "enables"
                            ][
                                1
                            ]
                            + 1
                        ]
                        self.offset = self.strings[self.name]["responses"][
                            responce_id["res"]
                        ]["enables"][0]

                    elif (
                        "enables"
                        in self.strings[self.name]["responses"][responce_id["res"]]
                        and len(
                            self.strings[self.name]["responses"][responce_id["res"]][
                                "enables"
                            ]
                        )
                        == 1
                    ):
                        self.enabled = [
                            self.strings[self.name]["options"][
                                self.strings[self.name]["responses"][
                                    responce_id["res"]
                                ]["enables"][0]
                            ]
                        ]

                        self.offset = self.strings[self.name]["responses"][
                            responce_id["res"]
                        ]["enables"][0]

                    elif (
                        "barter"
                        in self.strings[self.name]["responses"][responce_id["res"]]
                    ):
                        self.will_bartering = True

                    if (
                        "res_after"
                        in self.strings[self.name]["options"][
                            selected
                        ]
                        and self.strings[self.name]["options"][
                            selected
                        ]["res"]
                        != self.strings[self.name]["options"][
                            selected
                        ]["res_after"]
                    ):
                        self.strings[self.name]["options"][
                            selected
                        ]["res"] = self.strings[self.name]["options"][
                            selected
                        ][
                            "res_after"
                        ]
                        self.strings[self.name]["options"][
                            selected
                        ]["text"] = self.strings[self.name]["options"][
                            selected
                        ][
                            "text_after"
                        ]
                        

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

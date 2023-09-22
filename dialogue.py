import random

import numpy as np
import pygame


class Dialougue:
    def __init__(self, assets, ai, screen, music_player):
        self.strings = assets.load_dialogue()
        self.ai = ai
        self.screen = screen
        self.music_player = music_player
        self.subtitle_font = pygame.font.Font("game_data/inter.ttf", 24)
        self.option_font = pygame.font.Font("game_data/inter.ttf", 20)
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

        self.bg_menu = pygame.Rect(
            25,
            self.screen.get_height() - 170,
            self.screen.get_width() - 50,
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

            self.screen.blit(self.bg_surface_menu, self.bg_menu)

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
                        self.screen.get_width() // 2,
                        self.screen.get_height() - 140 + i * 35,
                    )
                )

                self.screen.blit(text, text_rect)

            if not self.greeting_played:
                self.music_player.play_greeting(self.strings[name]["file"])
                self.greeting_played = True

            text = self.subtitle_font.render(
                f"{name}: {self.strings[name]['greeting']}", True, (44, 53, 57)
            )

            text_rect = text.get_rect(
                center=(
                    self.screen.get_width() // 2,
                    self.screen.get_height() - 200,
                )
            )

            self.screen.blit(text, text_rect)

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
                        self.screen.get_width() // 2,
                        self.screen.get_height() - 140 + i * 35,
                    )
                )

                self.screen.blit(text, text_rect)

            max_line_width = self.screen.get_width()
            words = self.prev_talk.split()
            lines = []
            current_line = ""

            for word in words:
                # Calculate the maximum number of characters that can fit in the line
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
                        self.screen.get_width() // 2,
                        self.screen.get_height() - lenght + y * 30,
                    )
                )

                self.screen.blit(text, text_rect)

            if not self.music_player.get_player_status() and self.talk != -1:
                self.music_player.play_current_line(self.line)

                if self.talk != -1 and self.talk != self.prev_talk:
                    self.prev_talk = self.talk

                self.talk = next(self.current_talk, -1)
                self.line = next(self.current_lines, -1)

            elif not self.music_player.get_player_status() and self.talk == -1:
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
                    self.music_player.skip_current_line()
                    self.index += 1

                self.selection_held = True

                if self.talk != self.prev_talk and self.talk != -1:
                    self.music_player.skip_current_line()
                    self.prev_talk = self.talk
                    self.music_player.play_current_line(self.line)
                    return

                if self.talking:
                    self.talk = next(self.current_talk, -1)
                    self.line = next(self.current_lines, -1)

                if self.talking and self.talk != -1:
                    self.music_player.skip_current_line()

                elif self.talking and self.talk == -1:
                    self.music_player.skip_current_line()
                    self.talking = False

                elif not self.talking and self.talk == -1 and self.strings[self.name]["options"][self.selected_item + self.offset]["used"]:
                    responce_id = self.strings[self.name]["options"][
                        self.selected_item + self.offset
                    ]
                    
                    if ("starts" in self.strings[self.name]["responses"][responce_id["res"]]):
                        self.starts = self.strings[self.name]["responses"][responce_id["res"]]["starts"]
                        self.strings[self.name]["options"][self.selected_item + self.offset]["used"]=False

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

import pygame
import numpy as np
import random


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
        self.current_talk = ""
        self.enabled = None
        self.offset = 0

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
        if self.index == -1:
            scroll_position = (self.selected_item // 3) * 3
            self.enabled = self.strings[name]["options"][
                self.strings[name]["enables"][0] : self.strings[name]["enables"][1] + 1
            ]
            self.offset = self.strings[name]["enables"][0]
            visible_options = list(self.enabled)[scroll_position : scroll_position + 3]

            for i, value in enumerate(visible_options):
                color = (
                    (44, 53, 57)
                    if i == self.selected_item - scroll_position
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

        else:
            scroll_position = (self.selected_item // 3) * 3

            visible_options = list(self.enabled)[scroll_position : scroll_position + 3]

            for i, value in enumerate(visible_options):
                color = (
                    (44, 53, 57)
                    if i == self.selected_item - scroll_position
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

            text = self.subtitle_font.render(
                f"{name}: {self.current_talk}", True, (44, 53, 57)
            )

            text_rect = text.get_rect(
                center=(
                    self.screen.get_width() // 2,
                    self.screen.get_height() - 200,
                )
            )

            self.screen.blit(text, text_rect)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if not self.selection_held:
            if keys[pygame.K_UP] and not self.selection_held:
                self.selected_item = (self.selected_item - 1) % len(self.enabled)
                self.selection_held = True

            elif keys[pygame.K_DOWN] and not self.selection_held:
                self.selected_item = (self.selected_item + 1) % len(self.enabled)
                self.selection_held = True

            elif keys[pygame.K_RETURN] and not self.selection_held:
                self.index = 0
                self.selection_held = True

                responce_id = self.strings[self.name]["options"][
                    self.selected_item + self.offset
                ]

                self.current_talk = self.strings[self.name]["responses"][
                    responce_id["res"]
                ]["text"]

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
                        ][0] : self.strings[self.name]["responses"][responce_id["res"]][
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
                            self.strings[self.name]["responses"][responce_id["res"]][
                                "enables"
                            ][0]
                        ]
                    ]

                    self.offset = self.strings[self.name]["responses"][
                        responce_id["res"]
                    ]["enables"][0]

                self.selected_item = 0

        elif (
            not keys[pygame.K_UP]
            and not keys[pygame.K_DOWN]
            and not keys[pygame.K_RIGHT]
            and not keys[pygame.K_LEFT]
            and not keys[pygame.K_RETURN]
        ):
            self.selection_held = False

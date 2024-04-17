import copy
import random
import string

import numpy as np
import pygame

import asset_loader as assets
from animation import Animation
from colors import Colors
from effects import Effects
from game_date import GameDate
from game_manager import ClassManager as CM
from game_manager import GameManager as GM
from inventory import Inventory
from leveling_system import LevelingSystem
from quests import Quests
from stats import Stats


class Player:
    def __init__(self):
        self.stats = Stats()
        CM.inventory = Inventory()
        self.level = LevelingSystem()
        self.effects = Effects()
        self.quests = Quests()
        self.name = f"Player"
        self.gold = 1000
        self.current_world = f"Dream World"
        self.range = 5
        self.active_effects = []
        self.font = pygame.font.Font("fonts/SovngardeBold.ttf", 18)
        self.title_font = pygame.font.Font("fonts/SovngardeBold.ttf", 30)
        self.book_font = pygame.font.Font("fonts/SovngardeBold.ttf", 26)
        CM.animation = Animation()
        self.movement_speed = 125
        GM.game_date = GameDate()
        self.hash = "".join(
            random.choices(
                string.ascii_uppercase + string.digits + string.ascii_lowercase, k=32
            )
        )
        # self.hash = "Player"

        self.player = CM.animation.init_player()
        self.player_rect = pygame.Rect(600, 500, 32, 53)

        self.depleted_rect = pygame.Rect(
            GM.screen_width // 2 - 150 // 2,
            GM.screen_height - 19,
            min(self.stats.health / self.stats.max_health * 150, 150),
            18,
        )
        self.border_rect = pygame.Rect(
            (GM.screen_width // 2 - 150 // 2) - 2,
            GM.screen_height - 20,
            154,
            20,
        )
        self.depleted_rect.center = (80, GM.screen_height - 60)
        self.border_rect.center = (80, GM.screen_height - 60)
        
        self.depleted_rect2 = pygame.Rect(
            GM.screen_width // 2 - 150 // 2,
            GM.screen_height - 19,
            min(self.stats.power / self.stats.max_power * 150, 150),
            18,
        )
        self.border_rect2 = pygame.Rect(
            (GM.screen_width // 2 - 150 // 2) - 2,
            GM.screen_height - 20,
            154,
            20,
        )
        self.depleted_rect2.center = (80, GM.screen_height - 37)
        self.border_rect2.center = (80, GM.screen_height - 37)
        
        self.depleted_rect3 = pygame.Rect(
            GM.screen_width // 2 - 150 // 2,
            GM.screen_height - 19,
            min(self.stats.knowlage / self.stats.max_knowlage * 150, 150),
            18,
        )
        self.border_rect3 = pygame.Rect(
            (GM.screen_width // 2 - 150 // 2) - 2,
            GM.screen_height - 20,
            154,
            20,
        )
        self.depleted_rect3.center = (80, GM.screen_height - 14)
        self.border_rect3.center = (80, GM.screen_height - 14)

        self.equipped_items = {
            "hand": None,
            "back": None,
            "chest": None,
            "helmet": None,
            "gloves": None,
            "legs": None,
        }

        self.words = []
        self.title = ""
        self.current_line=0
        self.scrolling = False

    def update_health(self, health):
        self.stats.update_health(health)

        self.depleted_rect.width = min(
            self.stats.health / self.stats.max_health * 150, 150
        )
        self.depleted_rect.center = (GM.screen_width // 2, GM.screen_height - 60)
    
    def update_power(self, power):
        self.stats.update_power(power)

        self.depleted_rect2.width = min(
            self.stats.power / self.stats.max_power * 150, 150
        )
        self.depleted_rect2.center = (80, GM.screen_height - 37)
    
    def update_knowlage(self, knowlage):
        self.stats.update_knowlage(knowlage)

        self.depleted_rect3.width = min(
            self.stats.knowlage / self.stats.max_knowlage * 150, 150
        )
        self.depleted_rect3.center = (80, GM.screen_height - 14)

    def add_trait(self, index):
        amount, stat = self.level.traits.add_trait(
            list(self.level.traits.traits.keys())[index], self.level.level
        )
        if amount != None:
            self.effects.effects[stat]["amount"] += amount
            self.update_stats(stat, amount)
            self.update_health(self.stats.max_health)
            self.update_power(self.stats.max_power)
            self.update_knowlage(self.stats.max_knowlage)
            
    def check_trait_conditions(self, index):
        return self.level.traits.check_trait_conditions(
            list(self.level.traits.traits.keys())[index], self.level.level
        )

    def update_stats(self, stat, amount):
        if stat == "max_health":
            self.effects.effects[stat]["amount"] += amount
            self.stats.update_max_health(amount)
        elif stat == "health":
            self.update_health(amount)
        elif stat == "max_power":
            self.effects.effects[stat]["amount"] += amount
            self.stats.update_max_power(amount)
        elif stat == "power":
            self.stats.update_power(amount)
        elif stat == "max_knowledge":
            self.effects.effects[stat]["amount"] += amount
            self.stats.update_max_knowlage(amount)
        elif stat == "knowledge":
            self.stats.update_knowlage(amount)
        elif stat == "weapon_damage":
            self.effects.effects[stat]["amount"] += amount
            self.stats.update_weapon_damage(amount)

    def add_item(self, item):
        if "script" in item and item["script"]["time"] == "on_pickup":
            CM.script_loader.run_script(
                item["script"]["script_name"],
                item["script"]["function"],
                item["script"]["args"],
            )
            CM.inventory.items[item["name"]]["script"]["used"] = True

        if "quest" in item:
            self.quests.quests[item["quest"][0]]["stages"][item["quest"][1]][
                "objectives"
            ]["inventory"] = True

        if "starts_quest" in item:
            self.quests.start_quest(item["starts_quest"])

        if item["name"] == "Gold":
            self.gold += 1
        elif item["name"] == "Gold Sack":
            self.gold += 10
        else:
            CM.inventory.add_item(item)

    def remove_item(self, key):
        if (
            "script" in CM.inventory.items[key]
            and CM.inventory.items[key]["script"]["time"] == "on_drop"
        ):
            CM.script_loader.run_script(
                CM.inventory.items[key]["script"]["script_name"],
                CM.inventory.items[key]["script"]["function"],
                CM.inventory.items[key]["script"]["args"],
            )
            CM.inventory.items[key]["script"]["used"] = True

        if key in CM.inventory.items and CM.inventory.items[key]["dropable"]:
            CM.inventory.remove_item(key)
            return True
        return False

    def use_item(self, index):
        keys = list(CM.inventory.items.keys())
        item = CM.inventory.items[keys[index]]

        if (
            "script" in CM.inventory.items[keys[index]]
            and CM.inventory.items[keys[index]]["script"]["time"] == "on_use"
        ):
            CM.script_loader.run_script(
                CM.inventory.items[keys[index]]["script"]["script_name"],
                CM.inventory.items[keys[index]]["script"]["function"],
                CM.inventory.items[keys[index]]["script"]["args"],
            )
            CM.inventory.items[keys[index]]["script"]["used"] = True

        if "stats" in item and "effect" in item:
            if (
                item["name"]
                == self.equipped_items[
                    CM.inventory.items[item["name"]]["stats"]["slot"]
                ]
            ):
                self.unequip_item(keys[index])
            else:
                self.unequip_item(
                    self.equipped_items[
                        CM.inventory.items[item["name"]]["stats"]["slot"]
                    ]
                )
                self.equip_item(keys[index])

        elif "effect" in item:
            CM.inventory.remove_item(keys[index])
            if item["effect"]["duration"] > 0:
                self.active_effects.append(item["effect"])
            self.update_stats(item["effect"]["stat"], item["effect"]["value"])

        elif item["type"] == "book":
            CM.player_menu.book_open = True
            self.title = item["text"]["title"]
            self.words = assets.load_text(item["text"]["content"]).split()

    def check_experation(self, dt):
        indexes = []
        for index in range(len(self.active_effects)):
            self.active_effects[index]["duration"] -= dt
            if self.active_effects[index]["duration"] <= 0:
                indexes.append(index)

        for i in indexes:
            self.update_stats(
                self.active_effects[i]["stat"], -self.active_effects[i]["value"]
            )
            self.active_effects.remove(self.active_effects[i])

    def equip_item(self, item):
        slot = CM.inventory.items[item]["stats"]["slot"]
        if slot in self.equipped_items:
            self.equipped_items[slot] = item
            CM.inventory.items[item]["stats"]["equiped"] = True
            print(f"Equipped {item} in {slot}")
        else:
            print(f"Cannot equip {item} in {slot}")
        if slot == "hand":
            self.range = CM.inventory.items[item]["stats"]["range"]
            self.stats.update_weapon_damage(CM.inventory.items[item]["stats"]["damage"])
        else:
            self.stats.update_defense(CM.inventory.items[item]["stats"]["defense"])

    def unequip_item(self, item):
        if item != None and "stats" in CM.inventory.items[item]:
            slot = CM.inventory.items[item]["stats"]["slot"]
            if slot in self.equipped_items and self.equipped_items[slot] is not None:
                unequipped_item = self.equipped_items[slot]
                self.equipped_items[slot] = None
                CM.inventory.items[item]["stats"]["equiped"] = False
                print(f"Unequipped {unequipped_item} from {slot}")
            else:
                print(f"No item equipped in {slot}")
            if slot == "hand":
                self.range = 5
                self.stats.update_weapon_damage(-CM.inventory.items[item]["stats"]["damage"])
            else:
                self.stats.update_weapon_damage(-CM.inventory.items[item]["stats"]["defense"])

    def to_dict(self):
        return {
            "stats": self.stats.to_dict(),
            "level": self.level.to_dict(),
            "inventory": CM.inventory.to_dict(),
            "quests": self.quests.to_dict(),
            "animation": CM.animation.to_dict(),
            "game_date": GM.game_date.to_dict(),
            "name": self.name,
            "gold": self.gold,
            "current_world": self.current_world,
            "range": self.range,
            "active_effects": self.active_effects,
            "movement_speed": self.movement_speed,
            "equipped_items": self.equipped_items,
            "xy": [
                GM.relative_player_left,
                GM.relative_player_top,
                GM.relative_player_right,
                GM.relative_player_bottom,
            ],
            "hash": self.hash,
            "rectxy": [self.player_rect.centerx, self.player_rect.centery],
            "ai": CM.ai.to_dict(),
            "words": self.words,
            "title": self.title,
            "current_line": self.current_line,
            "scrolling": self.scrolling
        }

    def from_dict(self, data):
        self.stats.from_dict(data["stats"])
        self.level.from_dict(data["level"])
        CM.inventory.from_dict(data["inventory"])
        self.quests.from_dict(data["quests"])
        CM.animation.from_dict(data["animation"])
        self.name = data["name"]
        self.gold = data["gold"]
        self.current_world = data["current_world"]
        self.range = data["range"]
        self.active_effects = data["active_effects"]
        self.movement_speed = data["movement_speed"]
        self.equipped_items = data["equipped_items"]
        self.player_rect.centerx = data["rectxy"][0]
        self.player_rect.centery = data["rectxy"][1]
        GM.relative_player_left = data["xy"][0]
        GM.relative_player_top = data["xy"][1]
        GM.relative_player_right = data["xy"][2]
        GM.relative_player_bottom = data["xy"][3]
        self.hash = data["hash"]
        GM.game_date.from_dict(data["game_date"])
        CM.ai.from_dict(data["ai"])
        GM.save_world_names = data["save_world_names"]  
        self.words = data["words"]
        self.title = data["title"]
        self.current_line = data["current_line"]
        self.scrolling = data["scrolling"]
    
    def handle_input(self):
        keys = pygame.key.get_pressed()

        # Calculate the maximum number of lines that can fit on the screen
        max_lines_on_screen = (GM.screen.get_height() * 3 // 4) // self.book_font.size("J")[1]
        max_line_width = (GM.screen.get_width() // 4) * 3
        lines = []
        current_line = ""
        
        for word in self.words:
            max_chars_per_line = max_line_width // self.book_font.size("J")[0]
            if len(current_line) + len(word) <= max_chars_per_line:
                current_line += word + " "
            else:
                lines.append(current_line)
                current_line = word + " "

        if current_line:
            lines.append(current_line)

        # Scroll up
        if keys[pygame.K_UP] and not self.scrolling:
            if self.current_line > 0:
                self.current_line -= max_lines_on_screen
                self.current_line = max(0, self.current_line)
                self.scrolling = True

        # Scroll down
        elif keys[pygame.K_DOWN] and not self.scrolling:
            total_lines = len(self.words)
            max_displayable_lines = total_lines - (total_lines % max_lines_on_screen or max_lines_on_screen)
            if self.current_line < max_displayable_lines:
                self.current_line += max_lines_on_screen
                self.current_line = min(self.current_line, max_displayable_lines)
                self.scrolling = True
        
        if len(lines[self.current_line:self.current_line + max_lines_on_screen])<=0:
            if self.current_line > 0:
                self.current_line -= max_lines_on_screen
                self.current_line = max(0, self.current_line)

        # Reset scrolling flag if no keys are pressed
        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.scrolling = False
        
        return lines
    
    def draw(self):
        self.player, new_rect = CM.animation.player_anim(
            self.equipped_items["hand"], self.movement_speed
        )
        new_rect.center = self.player_rect.center
        new_rect.bottom = self.player_rect.bottom + 11

        GM.screen.blit(self.player, new_rect.topleft)
        
        pygame.draw.rect(
            GM.screen, Colors.dark_black, self.border_rect, border_radius=10
        )
        pygame.draw.rect(
            GM.screen, Colors.communist_red, self.depleted_rect, border_radius=10
        )     
        
        pygame.draw.rect(
            GM.screen, Colors.dark_black, self.border_rect2, border_radius=10
        )
        pygame.draw.rect(
            GM.screen, Colors.green, self.depleted_rect2, border_radius=10
        )
        
        pygame.draw.rect(
            GM.screen, Colors.dark_black, self.border_rect3, border_radius=10
        )
        pygame.draw.rect(
            GM.screen, Colors.blue, self.depleted_rect3, border_radius=10
        )

    def draw_book(self):
        lines=self.handle_input()
        left = (GM.screen.get_width() + GM.screen.get_width() // 4) / 2

        # Calculate the maximum number of lines that can fit on the screen
        max_lines_on_screen = (GM.screen.get_height() * 3 // 4) // self.book_font.size("J")[1]

        # Render the title
        text = self.title_font.render(f"{self.title}", True, Colors.active_item)
        text_rect = text.get_rect(center=(int((GM.screen.get_width() // 3) * 1.9), 50))
        GM.screen.blit(text, text_rect)

        # Render only the visible lines
        for y, line in enumerate(lines[self.current_line:self.current_line + max_lines_on_screen]):
            text = self.book_font.render(f"{line}", True, Colors.active_item)
            text_rect = text.get_rect(centerx=left, y=80 + y * 30)
            GM.screen.blit(text, text_rect)

import copy
import random
import string

import numpy as np
import pygame

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
        self.animation = Animation()
        self.movement_speed = 125
        GM.game_date = GameDate()
        self.hash=''.join(random.choices(string.ascii_uppercase + string.digits+string.ascii_lowercase, k=32))
        #self.hash = "Player"

        self.player= self.animation.init_player()
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
        self.depleted_rect.center = (GM.screen_width // 2, GM.screen_height - 10)
        self.border_rect.center = (GM.screen_width // 2, GM.screen_height - 10)

        self.text = self.font.render("Health", True, Colors.active_item)
        self.text_rect = self.text.get_rect(
            center=(GM.screen_width // 2, GM.screen_height - 12)
        )

        self.equipped_items = {
            "hand": None,
            "back": None,
            "chest": None,
            "helmet": None,
            "gloves": None,
            "legs": None,
        }

    def update_health(self, health):
        self.stats.update_health(health)

        self.depleted_rect.width = min(
            self.stats.health / self.stats.max_health * 150, 150
        )
        self.depleted_rect.center = (GM.screen_width // 2, GM.screen_height - 10)

    def update_max_health(self, health):
        self.stats.update_max_health(health)
        self.update_health(self.stats.max_health)

    def add_trait(self, index):
        amount, stat = self.level.traits.add_trait(
            list(self.level.traits.traits.keys())[index], self.level.level
        )
        if amount != None:
            self.effects.effects[stat]["amount"] += amount
            self.update_stats(stat, amount)

    def check_trait_conditions(self, index):
        return self.level.traits.check_trait_conditions(
            list(self.level.traits.traits.keys())[index], self.level.level
        )

    def update_stats(self, stat, amount):
        if stat == "max_health":
            self.effects.effects[stat]["amount"] += amount
            self.update_max_health(amount)
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
        if key in CM.inventory.items and CM.inventory.items[key]["dropable"]:
            CM.inventory.remove_item(key)
            return True
        return False

    def use_item(self, index):
        keys = list(CM.inventory.items.keys())
        item = CM.inventory.items[keys[index]]
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
            self.stats.weapon_damage = (
                self.stats.weapon_damage + CM.inventory.items[item]["stats"]["damage"]
            )
        else:
            self.stats.defense = (
                self.stats.defense + CM.inventory.items[item]["stats"]["damage"]
            )

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
                self.stats.weapon_damage = (
                    self.stats.weapon_damage
                    - CM.inventory.items[item]["stats"]["damage"]
                )
            else:
                self.stats.defense = (
                    self.stats.defense - CM.inventory.items[item]["stats"]["damage"]
                )

    def to_dict(self):
        return {
            "stats": self.stats.to_dict(),
            "level": self.level.to_dict(),
            "inventory": CM.inventory.to_dict(),
            "quests": self.quests.to_dict(),
            "animation": self.animation.to_dict(),
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
        }

    def from_dict(self, data):
        self.stats.from_dict(data["stats"])
        self.level.from_dict(data["level"])
        CM.inventory.from_dict(data["inventory"])
        self.quests.from_dict(data["quests"])
        self.animation.from_dict(data["animation"])
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

    def draw(self):
        self.player, new_rect = self.animation.player_anim(self.equipped_items["hand"], self.movement_speed)
        new_rect.center=self.player_rect.center
        new_rect.bottom=self.player_rect.bottom+11
        
        GM.screen.blit(self.player, new_rect.topleft)
        pygame.draw.rect(GM.screen, Colors.dark_black, self.border_rect, border_radius=10)
        pygame.draw.rect(GM.screen, Colors.communist_red, self.depleted_rect, border_radius=10)
        GM.screen.blit(self.text, self.text_rect)

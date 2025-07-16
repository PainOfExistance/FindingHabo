import copy
import random
import string
from hmac import new

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
    def __init__(self, world: str):
        self.name = f"Player"
        self.current_world = world
        self.range = 5
        self.active_effects = []
        self.hash = "".join(
            random.choices(
                string.ascii_uppercase + string.digits + string.ascii_lowercase, k=32
            )
        )

        """
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
        """

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
        self.depleted_rect.center = (80, GM.screen_height - 60)
    
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
            self.update_power(amount)
        elif stat == "max_knowledge":
            self.effects.effects[stat]["amount"] += amount
            self.stats.update_max_knowlage(amount)
        elif stat == "knowledge":
            self.update_knowlage(amount)
        elif stat == "weapon_damage":
            self.effects.effects[stat]["amount"] += amount
            self.stats.update_weapon_damage(amount)

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
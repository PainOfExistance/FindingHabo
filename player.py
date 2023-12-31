import numpy as np
import pygame

from animation import Animation
from effects import Effects
from inventory import Inventory
from leveling_system import LevelingSystem
from quests import Quests
from stats import Stats


class Player:
    def __init__(self, path, screen_width, screen_height, assets):
        self.stats = Stats()
        self.inventory = Inventory()
        self.level = LevelingSystem(assets)
        self.effects = Effects(assets)
        self.quests=Quests(assets, self.inventory)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.name = f"Player"
        self.gold = 1000
        self.current_world=f"Dream World"
        self.screen_width = screen_width
        self.range=5
        self.active_effects=[]
        self.assets = assets
        self.font = pygame.font.Font("fonts/SovngardeBold.ttf", 18)
        self.animation = Animation(assets)
        self.movement_speed = 200

        self.player, self.player_rect = self.animation.init_player()
        self.player_rect.center=(600, 500)
        
        self.depleted_rect = pygame.Rect(
            screen_width // 2 - self.stats.max_health // 2,
            screen_height - 19,
            self.stats.health,
            18,
        )
        
        self.border_rect = pygame.Rect(
            (screen_width // 2 - self.stats.max_health // 2)-2,
            screen_height - 20,
            self.stats.max_health+4,
            20,
        )
        
        self.text = self.font.render("Health", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(
            center=(screen_width // 2, screen_height - 12)
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
        self.depleted_rect.width = self.stats.health
        self.depleted_rect.center=(self.screen_width // 2, self.screen_height - 10)
        
    def update_max_health(self, health):
        self.stats.update_max_health(health)
        self.border_rect.width = self.stats.max_health+4
        self.border_rect.left = (self.screen_width // 2 - self.stats.max_health // 2)-2
        self.update_health(self.stats.max_health)

    def add_trait(self, index):
        amount, stat=self.level.traits.add_trait(
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
        if stat=="max_health":
            self.effects.effects[stat]["amount"] += amount
            self.update_max_health(amount)
        elif stat=="health":
            self.update_health(amount)
        elif stat=="max_power":
            self.effects.effects[stat]["amount"] += amount
            self.stats.update_max_power(amount)
        elif stat=="power":
            self.stats.update_power(amount)
        elif stat=="max_knowledge":
            self.effects.effects[stat]["amount"] += amount
            self.stats.update_max_knowlage(amount)
        elif stat=="knowledge":
            self.stats.update_knowlage(amount)
        elif stat=="weapon_damage":
            self.effects.effects[stat]["amount"] += amount
            self.stats.update_weapon_damage(amount)
            
    def add_item(self, item):
        if "quest" in item:
            self.quests.quests[item["quest"][0]]["stages"][item["quest"][1]]["objectives"]["inventory"]=True
        self.inventory.add_item(item)
    
    def remove_item(self, key):
        if key in self.inventory.items and self.inventory.items[key]["dropable"]:
            self.inventory.remove_item(key)
            return True
        return False

    def use_item(self, index):
        keys = list(self.inventory.items.keys())
        item = self.inventory.items[keys[index]]
        if "stats" in item and "effect" in item:
            if (
                item["name"]
                == self.equipped_items[
                    self.inventory.items[item["name"]]["stats"]["slot"]
                ]
            ):
                self.unequip_item(keys[index])
            else:
                self.unequip_item(
                    self.equipped_items[
                        self.inventory.items[item["name"]]["stats"]["slot"]
                    ]
                )
                self.equip_item(keys[index])
        elif "effect" in item:
            self.inventory.remove_item(keys[index])
            if item["effect"]["duration"]>0:
                self.active_effects.append(item["effect"])
            self.update_stats(item["effect"]["stat"], item["effect"]["value"])
            
    def check_experation(self, dt):
        indexes=[]
        for index in range(len(self.active_effects)):
            self.active_effects[index]["duration"]-=dt
            if self.active_effects[index]["duration"]<=0:
                indexes.append(index)

        for i in indexes:
            self.update_stats(self.active_effects[i]["stat"], -self.active_effects[i]["value"])
            self.active_effects.remove(self.active_effects[i])

    def equip_item(self, item):
        slot = self.inventory.items[item]["stats"]["slot"]
        if slot in self.equipped_items:
            self.equipped_items[slot] = item
            self.inventory.items[item]["stats"]["equiped"] = True
            print(f"Equipped {item} in {slot}")
        else:
            print(f"Cannot equip {item} in {slot}")
        if slot == "hand":
            self.range = self.inventory.items[item]["stats"]["range"]
            self.stats.weapon_damage = self.stats.weapon_damage + self.inventory.items[item]["stats"]["damage"]
        else:
            self.stats.defense = self.stats.defense + self.inventory.items[item]["stats"]["damage"]

    def unequip_item(self, item):
        if item != None and "stats" in self.inventory.items[item]:
            slot = self.inventory.items[item]["stats"]["slot"]
            if slot in self.equipped_items and self.equipped_items[slot] is not None:
                unequipped_item = self.equipped_items[slot]
                self.equipped_items[slot] = None
                self.inventory.items[item]["stats"]["equiped"] = False
                print(f"Unequipped {unequipped_item} from {slot}")
            else:
                print(f"No item equipped in {slot}")
            if slot == "hand":
                self.range = 5
                self.stats.weapon_damage = self.stats.weapon_damage - self.inventory.items[item]["stats"]["damage"]
            else:
                self.stats.defense = self.stats.defense - self.inventory.items[item]["stats"]["damage"]             
                           
    def draw(self, screen, delta_time, moving, attacking, rotation):
        self.player, new_rect= self.animation.player_anim(delta_time, moving, attacking, rotation, self.equipped_items["hand"], self.movement_speed)
        new_rect.center= self.player_rect.center
        screen.blit(self.player, new_rect.topleft)
        pygame.draw.rect(screen, (0, 0, 0), self.border_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 0, 0), self.depleted_rect, border_radius=10)
        screen.blit(self.text, self.text_rect)

import pygame
import numpy as np
from stats import Stats
from inventory  import Inventory
from leveling_system  import LevelingSystem
from effects  import Effects

class Player:
    def __init__(self, path, screen_width, screen_height, assets):
        self.stats=Stats()
        self.inventory=Inventory()
        self.level=LevelingSystem(assets)
        self.effects=Effects(assets)
        
        self.player, self.player_rect=assets.load_player(path, (screen_width // 2, screen_height // 2))
        self.depleted_rect = pygame.Rect(screen_width // 2 - self.stats.max_health // 2, screen_height - 20, self.stats.health, 18)
        self.border_rect = pygame.Rect(screen_width // 2 - self.stats.max_health // 2, screen_height - 20, self.stats.max_health, 18)
        font = pygame.font.Font("game_data/inter.ttf", 13)
        self.text = font.render("Health", True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(screen_width // 2, screen_height - 12))
        
        self.equipped_items = {
            "hand": None,
            "back": None,
            "chest": None,
            "helmet": None,
            "gloves": None,
            "legs": None
        }

    def update_health(self, health):
        self.stats.update_health(health)
        self.depleted_rect.width = self.stats.health
    
    def add_trait(self, index):
        self.level.traits.add_trait(list(self.level.traits.traits.keys())[index], self.level.level)
        
    def check_trait_conditions(self, index):
        return self.level.traits.check_trait_conditions(list(self.level.traits.traits.keys())[index], self.level.level)
    
    def use_item(self, index):
        keys = list(self.inventory.items.keys())
        item = self.inventory.items[keys[index]]
        if "stats" in item:
            if item["name"]==self.equipped_items[self.inventory.items[item["name"]]["stats"]["slot"]]:
                self.unequip_item(keys[index])
            else:
                self.unequip_item(self.equipped_items[self.inventory.items[item["name"]]["stats"]["slot"]])
                self.equip_item(keys[index])
        else:
            self.inventory.remove_item(keys[index])
            self.update_health(item["effect"]["value"])
    
    def draw(self, screen):
        screen.blit(self.player, self.player_rect)
        pygame.draw.rect(screen, (0, 0, 0), self.border_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 0, 0), self.depleted_rect, border_radius=10)
        screen.blit(self.text, self.text_rect)

    def equip_item(self, item):
        slot=self.inventory.items[item]["stats"]["slot"]
        if slot in self.equipped_items:
            self.equipped_items[slot] = item
            self.inventory.items[item]["stats"]["equiped"]=True
            print(f"Equipped {item} in {slot}")
        else:
            print(f"Cannot equip {item} in {slot}")

    def unequip_item(self, item):
        if item != None:
            slot=self.inventory.items[item]["stats"]["slot"]
            if slot in self.equipped_items and self.equipped_items[slot] is not None:
                unequipped_item = self.equipped_items[slot]
                self.equipped_items[slot] = None
                self.inventory.items[item]["stats"]["equiped"]=False
                print(f"Unequipped {unequipped_item} from {slot}")
            else:
                print(f"No item equipped in {slot}")
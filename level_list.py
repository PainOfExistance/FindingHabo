import random

import numpy as np

import asset_loader as assets
from game_manager import ClassManager as CM
from game_manager import GameManager as GM


class LevelList:
    def __init__(self):
        self.common=["common"]
        self.uncommon=["common", "uncommon"]
        self.rare=["common", "uncommon", "rare"]
        self.very_rare=["common", "uncommon", "rare", "very rare"]
        self.epic=["common", "uncommon", "rare", "very rare", "epic"]
        self.rarity_table={"common": 0.85, "uncommon": 0.7, "rare": 0.55, "very rare": 0.4, "epic": 0.25}
        
    def generate_level_list(self, item_type, amount):
        max_items=random.randint(max(1, amount-5), amount)
        item_level_list = {}
        filtered_items, weight=self.__set_item_rarity_list(item_type)
        items=random.choices(filtered_items, weights=weight, k=max_items)
        for x in items:
            if x["name"] in item_level_list:
                item_level_list[x["name"]]+=1
            else:
                item_level_list[x["name"]]=1
        return item_level_list

    def __set_item_rarity_list(self, item_type):
        if(CM.player.level.level<9):
            items = [GM.items[x] for x in GM.items if (GM.items[x]['type'] in item_type and GM.items[x]["rarity"] in self.common)]
        elif(CM.player.level.level<19):
            items = [GM.items[x] for x in GM.items if (GM.items[x]['type'] in item_type and GM.items[x]["rarity"] in self.uncommon)]
        elif(CM.player.level.level<29):
            items = [GM.items[x] for x in GM.items if (GM.items[x]['type'] in item_type and GM.items[x]["rarity"] in self.rare)]
        elif(CM.player.level.level<39):
            items = [GM.items[x] for x in GM.items if (GM.items[x]['type'] in item_type and GM.items[x]["rarity"] in self.very_rare)]
        else:
            items = [GM.items[x] for x in GM.items if (GM.items[x]['type'] in item_type and GM.items[x]["rarity"] in self.epic)]
        weights=[self.rarity_table[x["rarity"]] for x in items]
        return items, weights
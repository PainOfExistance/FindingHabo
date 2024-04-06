import math

import numpy as np


class Stats:
    def __init__(self):
        self.max_health = 100
        self.health = 100

        self.max_power = 100
        self.power = 100

        self.max_knowlage = 100
        self.knowlage = 100
        
        self.weapon_damage = 5
        self.defense = 5
        
    def update_max_health(self, value):
        self.max_health+=value
        
    def update_health(self, value):
        self.health+=value
        if self.health > self.max_health:
            self.health = self.max_health
        elif self.health < 0:
            self.health = 0
            
    def update_max_power(self, value):
        self.max_power+=value      
        self.weapon_damage = self.weapon_damage + math.ceil(math.log(self.max_power))

    def update_power(self, value):
        self.power+=value
        if self.power > self.max_power:
            self.power = self.max_power
        elif self.power < 0:
            self.power = 0
           
    def update_max_knowlage(self, value):
        self.max_knowlage+=value

    def update_knowlage(self, value):
        self.knowlage+=value
        if self.knowlage > self.max_knowlage:
            self.knowlage = self.max_knowlage
        elif self.knowlage < 0:
            self.knowlage = 0
    
    def update_weapon_damage(self, value):
        self.weapon_damage+=value
    
    def update_defense(self, value):
        self.defense+=value
        
    def to_dict(self):
        return {
            "max_health": self.max_health,
            "health": self.health,
            "max_power": self.max_power,
            "power": self.power,
            "max_knowledge": self.max_knowlage,
            "knowledge": self.knowlage,
            "weapon_damage": self.weapon_damage,
            "defense": self.defense
        }
        
    def from_dict(self, data):
        self.max_health = data["max_health"]
        self.health = data["health"]
        self.max_power = data["max_power"]
        self.power = data["power"]
        self.max_knowlage = data["max_knowledge"]
        self.knowlage = data["knowledge"]
        self.weapon_damage = data["weapon_damage"]
        self.defense = data["defense"]
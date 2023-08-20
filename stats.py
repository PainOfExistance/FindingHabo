import numpy as np

class Stats:
    def __init__(self):
        self.max_sanity=100
        self.sanity=100

        self.max_health=100
        self.health=100

        self.max_power=100
        self.power=100

        self.max_knowlage=100
        self.knowlage=100

    def update_sanity(self, value):
        self.sanity+=value
        if self.sanity > self.max_sanity:
            self.sanity = self.max_sanity
        elif self.sanity < 0:
            self.sanity = 0

    def update_health(self, value):
        self.health+=value
        if self.health > self.max_health:
            self.health = self.max_health
        elif self.health < 0:
            self.health = 0

    def update_power(self, value):
        self.power+=value
        if self.power > self.max_power:
            self.power = self.max_power
        elif self.power < 0:
            self.power = 0

    def update_knowlage(self, value):
        self.knowlage+=value
        if self.knowlage > self.max_knowlage:
            self.knowlage = self.max_knowlage
        elif self.knowlage < 0:
            self.knowlage = 0
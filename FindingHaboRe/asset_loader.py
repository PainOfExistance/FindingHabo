import os
import sys


class AssetLoader:
    def __init__(self, terrain_path, sounds_path, textures_path):
        self.terrain_path = terrain_path
        self.sounds_path = sounds_path
        self.textures_path = textures_path

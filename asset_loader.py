import pygame
import numpy as np
import cv2

class AssetLoader:
    def __init__(self, screen_width, screen_height):
        self.screen_width=screen_width
        self.screen_height=screen_height

    def load_collision_map(self):
        # Create and return the collision map using NumPy
        bg_rect = pygame.Rect(0, 0, 1920, 1080)  # Replace with your background dimensions
        collision_map = np.zeros((bg_rect.height, bg_rect.width), dtype=int)
        collision_map[0, :] = 1
        collision_map[-1, :] = 1
        collision_map[:, 0] = 1
        collision_map[:, -1] = 1
        collision_map[200:300, 200:300] = 1
        return collision_map

    def load_images(self, path, size, center):
        # Load and return images as needed
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, size)
        img_rect = img.get_rect()
        img_rect.center = center
        return img, img_rect
    
    def load_player(self, path):
        # Load player image
        player = pygame.image.load(path)
        player = pygame.transform.scale(player, (self.screen_width // 10, self.screen_height // 10))
        player_rect = player.get_rect()
        player_rect.center = (self.screen_width // 2, self.screen_height // 2)
        return player, player_rect
    
    def load_background(self, path):
        # Load bg image
        bg = pygame.image.load(path)
        self.bg_rect = bg.get_rect()
        return bg, self.bg_rect
    
    def load_collision(self, path):
        #collision_map = np.zeros((self.bg_rect.height, self.bg_rect.width), dtype=int)
        #collision_map[0, :] = 1
        #collision_map[-1, :] = 1
        #collision_map[:, 0] = 1
        #collision_map[:, -1] = 1
        #collision_map[200:300, 200:300] = 1
        #print(collision_map)
        #return collision_map
        image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        binary_image = 1 - (image // 255)
        print(binary_image)
        return binary_image
    
    #https://www.youtube.com/watch?v=vOn0z0IRVN8&list=PLI2unizewPmmLdFX9kTGPSnXJJCiasCw5&index=64&ab_channel=Nazareth-Topic
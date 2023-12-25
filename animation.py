import pygame


class Animation:
    def __init__(self, assets):
        images =assets.load_player_sprites()
        self.action_images = self.slice_image(images)

    def slice_image(self, images):
        frames = {}
        for key in images.keys():
            if "Attack" not in key:
                for i in range(4):
                    img=images[key].subsurface((i * 16, 0, 16, 16))
                    img = pygame.transform.scale(img, (img.get_width(),img.get_height()))
                    rect=img.get_rect()
                    frames[key+"_"+str(i+1)] = {"image": img, "rect": rect}
            else:
                img = pygame.transform.scale(img, (img.get_width(),img.get_height()))
                rect=img.get_rect()
                frames[key] = {"image": img, "rect": rect}
        return frames
    
    

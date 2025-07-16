import os
import random

import pygame


class MusicPlayer:
    def __init__(self, music_tracks=""):
        self.music_tracks = [music_tracks]
        self.current_track_index = 0
        self.sfx = {}
        self.__load_sounds()

        pygame.mixer.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.mixer.music.set_volume(0.3)
        
    def __load_sounds(self, folder="sounds/sfx"):
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(('.mp3', '.wav')):
                    file_path = os.path.join(root, file)
                    sound_name = os.path.splitext(file)[0]
                    self.sfx[sound_name] = pygame.mixer.Sound(file_path)

    def play_next_track(self):
        self.current_track_index = (self.current_track_index + 1) % len(self.music_tracks)
        pygame.mixer.music.load(self.music_tracks[self.current_track_index])
        pygame.mixer.music.play()

    def play_random_track(self):
        random.shuffle(self.music_tracks)
        pygame.mixer.music.load(self.music_tracks[self.current_track_index])
        pygame.mixer.music.play()

    def update(self):
        self.play_next_track()

    def set_tracks(self, music_tracks):
        self.music_tracks = music_tracks
        random.shuffle(self.music_tracks)
        pygame.mixer.music.fadeout(1000)
        self.current_track_index = 0
        self.play_random_track()

    def stop(self):
        pygame.mixer.music.stop()
    
    def play_sfx(self, name):
        self.sfx[name].play()
        self.sfx[name].set_volume(0.1)
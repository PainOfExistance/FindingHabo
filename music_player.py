import pygame
import random

class MusicPlayer:
    def __init__(self, music_tracks):
        self.music_tracks = music_tracks
        self.current_track_index = 0

        pygame.mixer.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.mixer.music.set_volume(0.2)
        self.play_random_track()

    def play_next_track(self):
        self.current_track_index = (self.current_track_index + 1) % len(self.music_tracks)
        pygame.mixer.music.load(self.music_tracks[self.current_track_index])
        pygame.mixer.music.play()

    def play_random_track(self):
        random.shuffle(self.music_tracks)
        pygame.mixer.music.load(self.music_tracks[self.current_track_index])
        pygame.mixer.music.play()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:  # Track ended event
                self.play_next_track()
                
    def set_tracks(self, music_tracks):
        self.music_tracks = music_tracks
        self.current_track_index = 0
        
    def stop(self):
        pygame.mixer.music.stop()
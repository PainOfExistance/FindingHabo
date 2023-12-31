import random

import pygame


class MusicPlayer:
    def __init__(self, music_tracks):
        self.music_tracks = music_tracks
        self.current_track_index = 0

        pygame.mixer.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.mixer.music.set_volume(0.3)
        self.play_random_track()
        self.sound=None
        self.channel=None

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
        random.shuffle(self.music_tracks)
        pygame.mixer.music.fadeout(1000)
        self.current_track_index = 0
        self.play_random_track()
        
    def stop(self):
        pygame.mixer.music.stop()
    
    def play_line(self, line):
        sound = pygame.mixer.Sound(f"sounds/dialogue/{line}.mp3")
        sound.play()
        sound.set_volume(0.2)
        return sound.get_length()
    
    def play_current_line(self, line):
        self.sound = pygame.mixer.Sound(f"sounds/dialogue/{line}.mp3")
        self.channel = self.sound.play()
        self.sound.set_volume(0.3)
    
    def skip_current_line(self):
        if self.sound != None:
            self.sound.stop()
        self.sound=None
        self.channel=None
    
    def play_greeting(self, line):
        self.sound = pygame.mixer.Sound(f"sounds/dialogue/{line}.mp3")
        self.sound.set_volume(0.3)
        self.sound.get_length()
        self.sound.play()
    
    def get_player_status(self):
        if self.channel==None:
            return False
        return self.channel.get_busy()
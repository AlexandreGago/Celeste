import pygame
from constants.dictionaries import sounds

class SoundManager:

    def __init__(self):
        self.mixer = pygame.mixer
        self.mixer.init()

        self.sounds = {k: self.mixer.Sound(v) for k, v in sounds.items()}

    def play(self, sound, loop=False):
        #find an unused channel
        channel = self.mixer.find_channel()
        if loop:
            channel.play(self.sounds[sound], -1)
        channel.play(self.sounds[sound])
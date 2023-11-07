import pygame
from constants.dictionaries import sounds

class SoundManager:

    def __init__(self):
        self.mixer = pygame.mixer
        self.mixer.init()
        self.mixer.set_num_channels(15)
         

        self.sounds = {k: self.mixer.Sound(v) for k, v in sounds.items()}

    def play(self, sound, loop=False, volume=1.0):
        #find an unused channel
        channel = self.mixer.find_channel()
        if channel:
            sd = self.sounds[sound].set_volume(volume)
            if loop:
                channel.play(sd, -1)

            else:
                channel.play(sd)        
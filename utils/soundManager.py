import pygame
from constants.dictionaries import sounds

class SoundManager:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SoundManager, cls).__new__(cls)
            cls._instance.mixer = pygame.mixer
            cls._instance.mixer.init()
            cls._instance.mixer.set_num_channels(15)
            cls._instance.sounds = {k: cls._instance.mixer.Sound(v) for k, v in sounds.items()}
        return cls._instance

    def play(self, sound: str, loop: bool = False, volume: float = 0.1) -> None:
        channel = self.mixer.find_channel()
        if channel:
            self.sounds[sound].set_volume(volume)
            if loop:
                channel.play(self.sounds[sound], -1)
            else:
                channel.play(self.sounds[sound])


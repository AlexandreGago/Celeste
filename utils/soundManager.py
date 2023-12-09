import pygame
from constants.dictionaries import sounds

class SoundManager:

    _instance = None

    def __new__(cls):
        if cls._instance is not None:
            raise ValueError("An instance of SoundManager already exists")
        cls._instance = super(SoundManager, cls).__new__(cls)
        return cls._instance

    
    def __init__(self) -> None:
        self.mixer = pygame.mixer
        self.mixer.init()
        self.mixer.set_num_channels(15)
        self.sounds = {k: self.mixer.Sound(v) for k, v in sounds.items()}
        
    def play(self, sound: str, loop: bool = False, volume: float = 0.1) -> None:
        channel = self.mixer.find_channel()
        if channel:
            self.sounds[sound].set_volume(volume)
            if loop:
                channel.play(self.sounds[sound], -1)
            else:
                channel.play(self.sounds[sound])

    def stop(self) -> None:
        self.mixer.stop()


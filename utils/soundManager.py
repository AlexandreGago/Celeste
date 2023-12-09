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
        self.mixer.set_num_channels(15)# create 15 channels
        self.sounds = {k: self.mixer.Sound(v) for k, v in sounds.items()}# load all sounds
        
    def play(self, sound: str, loop: bool = False, volume: float = 0.1) -> None:
        """ 
        Play a sound
        
        Args:
            sound (str): sound name
            loop (bool, optional): loop sound. Defaults to False.
            volume (float, optional): volume. Defaults to 0.1.
            
        Returns:
            None
        """
        
        channel = self.mixer.find_channel()# find an available channel
        if channel: # if a channel is available
            self.sounds[sound].set_volume(volume)# set volume
            if loop:
                channel.play(self.sounds[sound], -1)# play sound on channel on loop
            else:
                channel.play(self.sounds[sound])# play sound on channel

    def stop(self) -> None:
        """ 
        Stop all sounds
        
        Args:
            None
            
        Returns:
            None
        """
        self.mixer.stop()


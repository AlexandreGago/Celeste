import pygame
import random
import math


class Particle:
    """
    Base class for particles

    Args:
        None

    Returns:
        None
    """
    def update(self, dt, time):
        raise NotImplementedError

    def draw(self, screen):
        raise NotImplementedError

class SnowParticle(Particle):
    def __init__(self,pos: list[int],radius: int,speed: int,time_offset: int,wave_speed: float,height,width) -> None:
        """
        Class for snow particles
        Args:
            pos (list[int]): position of the particle
            radius (int): radius of the particle
            speed (int): speed of the particle
            time_offset (int): time offset of the particle
            wave_speed (float): wave speed of the particle
            height (int): height of the screen
            width (int): width of the screen

        Returns:
            None
        """
        super().__init__()
        self.pos = pos
        self.radius = radius
        self.speed = speed
        self.time_offset = time_offset
        self.wave_speed = wave_speed
        self.width = width
        self.height = height

    def update(self, time):
        """
        Updates the particle position

        Args:
            time (int): time

        Returns:
            None
        """
        # make the particle go left
        self.pos[0] -= self.speed

        if self.pos[0] < -100:  # particle is out of screen
            # reset the particle to the right side of the screen
            self.pos[0] = self.width + 100

            # if the particle is also too up or down
            if self.pos[1] < -100 or self.pos[1] > self.height + 100:
                self.pos[1] = random.randint(100, self.height - 100)

        # Change the Y value of the particle to make it move in a wave
        self.pos[1] += math.sin(0.001*(time + self.time_offset)) * self.wave_speed

    def updateMapSize(self,width:int,height:int):
        """
        Updates the particle map size

        Args:
            width (int): width of the map
            height (int): height of the map

        Returns:
            None
        """
        self.width = width
        self.height = height

    def draw(self, screen):
        """
        Draws the particle

        Args:
            screen (pygame.display): display where the particle is drawn

        Returns:
            None
        """
        pygame.draw.circle(screen, "white", self.pos, self.radius)

class CloudParticle(Particle):
    #has  width, height and speed
    def __init__(self, pos: list[int], size: list[int], speed: int,height,width:int) -> None:
        """
        Class for cloud particles

        Args:
            pos (list[int]): position of the particle
            size (list[int]): size of the particle
            speed (int): speed of the particle
            height (int): height of the screen
            width (int): width of the screen

        Returns:
            None
        """
        super().__init__()
        self.pos = pos
        self.size = size
        self.speed = speed
        self.height = height
        self.width = width
        self.color = (29,43,83)

    def updateMapSize(self,width:int,height:int):
        """
        Updates the particle map size

        Args:
            width (int): width of the map
            height (int): height of the map

        Returns:
            None
        """
        self.width = width
        self.height = height

    def update(self,time):
        """
        Updates the particle position

        Args:
            time (int): time

        Returns:
            None
        """
        # make the particle go left
        self.pos[0] -= self.speed

        if self.pos[0] < -self.size[0] - 100:
            self.pos[0] = self.width + 100
            self.pos[1] = random.randint(100, self.height - 100)

    def draw(self, screen:pygame.display):
        """
        Draws the particle

        Args:
            screen (pygame.display): display where the particle is drawn

        Returns:
            None
        """
        pygame.draw.rect(screen, self.color, (*self.pos, *self.size))



class ParticleManager:
    """
    Class for managing particles
    """
    _instance = None
    def __new__(cls, *args, **kwargs):
        """
        Singleton implementation
        """
        if cls._instance is not None:
            raise ValueError("An instance of ParticleManager already exists")
        cls._instance = super(ParticleManager, cls).__new__(cls)
        return cls._instance
    def __init__(self,width:int,height:int) -> None:
        """
        Create a particle manager

        Args:
            width (int): width of the screen
            height (int): height of the screen

        Returns:
            None
        """
        self.particles: list[Particle] = []
        self.width = width
        self.height = height

    def update(self, time):
        """
        Updates the particles
        """
        for particle in self.particles:
            particle.update(time)

    def setMapSize(self,width,height):
        """
        Sets the map size of the particles in the particle manager

        Args:
            width (int): width of the map
            height (int): height of the map

        Returns:
            None
        """
        self.width = width
        self.height = height
        for particle in self.particles:
            particle.updateMapSize(self.width,self.height)


    def add_particles(self, type: str, number: int):
        """
        Adds particles to the particle manager

        Args:
            type (str): type of the particle
            number (int): number of particles to add

        Returns:
            None
        """
        if type == "snow":   
            for _ in range(number):
                particle = SnowParticle(
                    pos=[
                        random.randint(-100, self.width + 100),
                        random.randint(-100, self.height + 100),
                    ],
                    radius=random.randint(2, 5),
                    speed=random.randint(3,7),
                    time_offset=random.randint(-10, 10),
                    wave_speed=1 + (random.randint(-15, 15) / 10),
                    height=self.height,
                    width=self.width
                )
                self.particles.append(particle)
        elif type == "cloud":
            for _ in range(number):
                particle = CloudParticle(
                    pos=[
                        random.randint(-100, self.width + 100),
                        random.randint(0, self.height),
                    ],
                    size=[
                        random.randint(100, 600),
                        random.randint(25, 75),
                    ],
                    speed=random.randint(2, 10),
                    height = self.height,
                    width = self.width
                )
                self.particles.append(particle)
    
    def setCloudColor(self,color:str):
        """
        Sets the color of the cloud particles

        Args:
            color (tuple): color of the cloud particles (RGB)

        Returns:
            None
        """
        for particle in self.particles:
            if isinstance(particle,CloudParticle):
                particle.color = color
    def draw(self, type: str, screen:pygame.display):
        """
        Draws the particles

        Args:
            type (str): type of the particle
            screen (pygame.display): display where the particles are drawn

        Returns:
            None
        """
        for particle in self.particles:
            if isinstance(particle, SnowParticle) and type == "snow":
                particle.draw(screen)
            elif isinstance(particle, CloudParticle) and type == "cloud":
                particle.draw(screen)
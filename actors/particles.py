import pygame
import random
import math
from constants.dictionaries import WIDTH, HEIGHT



class Particle:
    def update(self, dt, time):
        pass

    def draw(self, screen):
        pass

class SnowParticle(Particle):
    def __init__(self,pos: list[int],radius: int,speed: int,time_offset: int,wave_speed: float) -> None:
        super().__init__()
        self.pos = pos
        self.radius = radius
        self.speed = speed
        self.time_offset = time_offset
        self.wave_speed = wave_speed

    def update(self, time):

        # make the particle go left
        self.pos[0] -= self.speed

        if self.pos[0] < -100:  # particle is out of screen
            # reset the particle to the right side of the screen
            self.pos[0] = WIDTH + 100

            # if the particle is also too up or down
            if self.pos[1] < -100 or self.pos[1] > HEIGHT + 100:
                self.pos[1] = random.randint(100, HEIGHT - 100)

        # Change the Y value of the particle to make it move in a wave
        self.pos[1] += math.sin(0.001*(time + self.time_offset)) * self.wave_speed

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.pos, self.radius)

class CloudParticle(Particle):
    #has  width, height and speed
    def __init__(self, pos: list[int], size: list[int], speed: int) -> None:
        super().__init__()
        self.pos = pos
        self.size = size
        self.speed = speed

    def update(self, time):
        # make the particle go left
        self.pos[0] -= self.speed

        if self.pos[0] < -self.size[0] - 100:
            self.pos[0] = WIDTH + 100
            self.pos[1] = random.randint(100, HEIGHT - 100)

    def draw(self, screen):
        pygame.draw.rect(screen, "#1D2B53", (*self.pos, *self.size))


class ParticleManager:
    def __init__(self) -> None:
        self.particles: list[Particle] = []

    def update(self, time):
        for particle in self.particles:
            particle.update(time)

    def add_particles(self, type: str, number: int):
        if type == "snow":   
            for _ in range(number):
                particle = SnowParticle(
                    pos=[
                        random.randint(-100, WIDTH + 100),
                        random.randint(-100, HEIGHT + 100),
                    ],
                    radius=random.randint(2, 5),
                    speed=random.randint(3,7),
                    time_offset=random.randint(-10, 10),
                    wave_speed=1 + (random.randint(-15, 15) / 10),
                )
                self.particles.append(particle)
        elif type == "cloud":
            for _ in range(number):
                particle = CloudParticle(
                    pos=[
                        random.randint(-100, WIDTH + 100),
                        random.randint(0, HEIGHT),
                    ],
                    size=[
                        random.randint(100, 600),
                        random.randint(25, 75),
                    ],
                    speed=random.randint(2, 10),
                )
                self.particles.append(particle)

    def draw(self, type: str, screen):
        for particle in self.particles:
            if isinstance(particle, SnowParticle) and type == "snow":
                particle.draw(screen)
            elif isinstance(particle, CloudParticle) and type == "cloud":
                particle.draw(screen)
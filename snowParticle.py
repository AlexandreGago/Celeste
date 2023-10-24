import pygame
import random
import math
WIDTH, HEIGHT = 800, 800


class Particle:
    def __init__(self,pos: list[int],radius: int,speed: int,time_offset: int,wave_speed: float) -> None:
        self.pos = pos
        self.radius = radius
        self.speed = speed
        self.time_offset = time_offset
        self.wave_speed = wave_speed

    def update(self, dt, time):
        # make the particle go left
        self.pos[0] -= self.speed * dt/2

        if self.pos[0] < -100:  # particle is out of screen
            # reset the particle to the right side of the screen
            self.pos[0] = WIDTH + 100

            # if the particle is also too up or down
            if self.pos[1] < -100 or self.pos[1] > HEIGHT + 100:
                self.pos[1] = random.randint(100, HEIGHT - 100)

        # Change the Y value of the particle to make it move in a wave
        self.pos[1] += math.sin(0.1*(time + self.time_offset)) * self.wave_speed * dt

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.pos, self.radius)


class ParticleManager:
    def __init__(self) -> None:
        self.particles: list[Particle] = []

    def update(self, dt, time):
        for particle in self.particles:
            particle.update(dt, time)

    def add_particles(self, number):
        for _ in range(number):
            particle = Particle(
                pos=[
                    random.randint(-100, WIDTH + 100),
                    random.randint(-100, HEIGHT + 100),
                ],
                radius=random.randint(2, 5),
                speed=random.randint(6, 12),
                time_offset=random.randint(-10, 10),
                wave_speed=1 + (random.randint(-15, 15) / 10),
            )
            self.particles.append(particle)

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
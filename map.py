#this has a class that will load a map from the maps.json and determine the sprites to be drawn
#it will also determine the collision map for the map
import pygame.sprite
import json
levels = json.load(open("maps.json"))
spritesheet = pygame.image.load("atlas.png")

spritelocations = {
    "wall"   : (0, 16, 8, 8),
    "flower" : (114, 25, 5, 7),
    "spikes" : (9, 11, 7, 5)
}

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image =  image
        self.rect  =  self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Map:

    def __init__(self, level):
        self.level = level
        self.collision_map = self.load_collision_map(level)
        self.sprites = self.load_sprites(level)
        self.spawn = self.load_spawn(level)

    
    def load_sprites(self, level):
        sprites = pygame.sprite.Group()
        for idx,row in enumerate(levels[level]):
            for idy,cell in enumerate(row):
                if cell == "c":
                    image = spritesheet.subsurface(*spritelocations["wall"])
                    #50*16=800
                    image = pygame.transform.scale(image, (50, 50))
                    sprites.add(Tile(image, idy*50, idx*50))

                if cell == "f":
                    image = spritesheet.subsurface(*spritelocations["flower"])
                    image = pygame.transform.scale(image, (50, 50))
                    sprites.add(Tile(image, idy*50, idx*50))
                if cell == "x":
                    image = spritesheet.subsurface(*spritelocations["spikes"])
                    image = pygame.transform.scale(image, (50, 50))
                    sprites.add(Tile(image, idy*50, idx*50))

        return sprites
    
    def load_spawn(self, level):
        for idx,row in enumerate(levels[level]):
            for idy,cell in enumerate(row):
                if cell == "p":
                    return (idy*50, idx*50)


    def load_collision_map(self, level):
        collision_map = set()
        for idx,row in enumerate(levels[level]):
            for idy,cell in enumerate(row):
                #! -100 is the offset for the player
                if cell == "c":
                    collision_map.add((idy*50-50, idx*50-100))
                if cell == "x":
                    collision_map.add((idy*50-50, idx*50-100))
        return collision_map
    def draw(self, screen):
        self.sprites.draw(screen)


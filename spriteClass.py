import pygame
from enums import ActorTypes
from dictionaries import PlayerStuff,DashResetEntityStuff,StawberryStuff


class SpriteClass(pygame.sprite.Sprite):

    # img= pygame.image.load("zelda.png")

    def __init__(self,height,width,type,spriteID="idle"):
        super().__init__()
        self.type = type
        self.height = height
        self.width = width

        self.spriteID = None

        #set rect to red color
        if self.type == ActorTypes.PLAYER:
            self.spriteID = spriteID
            img = pygame.image.load(PlayerStuff.spritesLocation[self.spriteID])
            self.image = img.subsurface((0,0,16,16))
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

        if self.type == ActorTypes.DASH_RESET:
            self.spriteID = spriteID
            print(self.spriteID)
            img = pygame.image.load(DashResetEntityStuff.spritesLocation[self.spriteID])
            self.image = img.subsurface((0,0,16,16))
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

        if self.type == ActorTypes.STRAWBERRY:
            self.spriteID = spriteID
            img = pygame.image.load(StawberryStuff.spritesLocation[self.spriteID])
            self.image = img.subsurface((0,0,16,16))
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()


    def update(self,x,y,height,width,spriteID,flip=None):
        self.rect.x = x
        self.rect.y = y
        self.height = height
        self.width = width

        self.spriteID = spriteID
        # print(self.spriteID)

        if self.type == ActorTypes.PLAYER:
            #update image
            img = pygame.image.load(PlayerStuff.spritesLocation[spriteID])

            self.image = img.subsurface((9,19,12,13))

        if self.type == ActorTypes.DASH_RESET:
            #update image
            img = pygame.image.load(DashResetEntityStuff.spritesLocation[spriteID])
            self.image = img.subsurface((0,0,16,16))
        if self.type == ActorTypes.STRAWBERRY:
            #update image
            img = pygame.image.load(StawberryStuff.spritesLocation[spriteID])
            self.image = img.subsurface((0,0,16,16))

        if flip:
            self.image = pygame.transform.flip(self.image,True,False)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self,screen):
        screen.blit(self.image,self.rect)

        


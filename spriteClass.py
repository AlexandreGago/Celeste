import pygame
from constants.enums import ActorTypes,ParticleTypes
from constants.dictionaries import PlayerStuff,DashResetEntityStuff,StawberryStuff,SpringStuff,SpikeStuff, cloudStuff, dashUpgradeStuff,jumpParticles,fallingBlockStuff,doubleDashResetStuff


# atlasIMG = pygame.image.load("atlas.png")
class SpriteClass(pygame.sprite.Sprite):
    def __init__(self,x,y,height,width,type,spriteID,flipVertical=None,flipHorizontal=None,rotate=None,playerName = None):
        super().__init__()
        self.type = type
        self.height = height
        self.width = width

        self.spriteID = None
        self.atlasIMG = None

        if self.type == ActorTypes.PLAYER:
            self.spriteID = spriteID
            if playerName == "Badeline":
                img = pygame.image.load(PlayerStuff.spritesLocationBadeline[self.spriteID])
            else:
                img = pygame.image.load(PlayerStuff.spritesLocation[self.spriteID])
            self.image = img.subsurface((0,0,16,16))
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

        if self.type == ActorTypes.DASH_RESET:
            self.spriteID = spriteID
            img = pygame.image.load(DashResetEntityStuff.spritesLocation[self.spriteID])
            self.image = img.subsurface((3,3,10,10))
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

        if self.type == ActorTypes.STRAWBERRY:
            self.spriteID = spriteID
            img = pygame.image.load(StawberryStuff.spritesLocation[self.spriteID])
            self.image = img.subsurface((0,0,16,16))
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        if self.type == ActorTypes.SPRING:
            self.spriteID = spriteID
            img = pygame.image.load(SpringStuff.spritesLocation[self.spriteID])
            self.image = img.subsurface(SpringStuff.spritesImageCrop[self.spriteID])
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            
        if self.type == ActorTypes.SPIKE:
            self.spriteID = spriteID
            # self.image = atlasIMG.subsurface((9,11, 7,5))
            img = pygame.image.load(SpikeStuff.spritesLocation[self.spriteID])
            self.image = img.subsurface((0,0,8,8))
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            
        if self.type == ParticleTypes.JUMP:
            self.atlasIMG = pygame.image.load("atlas.png")
            self.image = self.atlasIMG.subsurface((9,11, 7,5))
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        if self.type == ActorTypes.FALLINGBLOCK:
            self.spriteID = spriteID
            img = pygame.image.load(fallingBlockStuff.spritesLocation[self.spriteID])
            self.image = img.subsurface((0,0,32,8))
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            
        if self.type == ActorTypes.CLOUD:
            self.spriteID = spriteID
            img = pygame.image.load(cloudStuff.spritesLocation[self.spriteID])
            self.image = img.subsurface((6,4,32,14))
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            
        if self.type == ActorTypes.DASH_UPGRADE:
            self.atlasIMG = pygame.image.load("atlas.png")
            self.image = self.atlasIMG.subsurface((48,48,8,8))
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        if self.type == ActorTypes.DOUBLE_DASH_RESET:
            self.spriteID = spriteID
            self.image = pygame.image.load(doubleDashResetStuff.spritesLocation[self.spriteID])
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

        if flipVertical:
            self.image = pygame.transform.flip(self.image,True,False)
        if flipHorizontal:
            self.image = pygame.transform.flip(self.image,False,True)


        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.height = height
        self.rect.width = width


    def update(self,x,y,height,width,spriteID,flipVertical=None,flipHorizontal=None,rotate = None,playerName = None):
        self.rect.x = x
        self.rect.y = y
        self.rect.height = height
        self.rect.width = width
        self.height = height
        self.width = width

        self.spriteID = spriteID
        # print(self.spriteID)

        if self.type == ActorTypes.PLAYER:
            #update image
            if playerName == "Badeline":
                img = pygame.image.load(PlayerStuff.spritesLocationBadeline[self.spriteID])
            else:
                img = pygame.image.load(PlayerStuff.spritesLocation[self.spriteID])

            self.image = img.subsurface((9,19,12,13))

        if self.type == ActorTypes.DASH_RESET:
            #update image
            img = pygame.image.load(DashResetEntityStuff.spritesLocation[spriteID])
            self.image = img.subsurface((2,2,11,11))

        if self.type == ActorTypes.STRAWBERRY:
            #update image
            img = pygame.image.load(StawberryStuff.spritesLocation[spriteID])
            self.image = img.subsurface((0,0,16,16))

        if self.type == ActorTypes.SPRING:
            img = pygame.image.load(SpringStuff.spritesLocation[spriteID])
            self.image = img.subsurface(SpringStuff.spritesImageCrop[spriteID])
            
        if self.type == ActorTypes.SPIKE:
            # self.image = atlasIMG.subsurface((9,11, 7,5))
            img = pygame.image.load(SpikeStuff.spritesLocation[self.spriteID])
            self.image = img.subsurface((1,2,7,6))
        if self.type == ParticleTypes.JUMP:
            self.image = self.atlasIMG.subsurface(jumpParticles.spritesImageCrop[self.spriteID])

        if self.type == ActorTypes.FALLINGBLOCK:
            img = pygame.image.load(fallingBlockStuff.spritesLocation[self.spriteID])
            self.image = img.subsurface((0,0,23,8))
            
        if self.type == ActorTypes.CLOUD:
            self.spriteID = spriteID
            img = pygame.image.load(cloudStuff.spritesLocation[self.spriteID])
            self.image = img.subsurface((6,4,32,14))
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

        if self.type == ActorTypes.DASH_UPGRADE:
            self.atlasIMG = pygame.image.load("atlas.png")
            self.image = self.atlasIMG.subsurface((48,48,8,8))
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

        if self.type == ActorTypes.DOUBLE_DASH_RESET:
            self.image = pygame.image.load(doubleDashResetStuff.spritesLocation[self.spriteID])
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

        if flipVertical:
            self.image = pygame.transform.flip(self.image,True,False)
        if flipHorizontal:
            self.image = pygame.transform.flip(self.image,False,True)
        if rotate:
            self.image =pygame.transform.rotate(self.image, rotate)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        

    def draw(self,screen):
        screen.blit(self.image,self.rect)

        


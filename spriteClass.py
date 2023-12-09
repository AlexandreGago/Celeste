import pygame
from constants.enums import ActorTypes,ParticleTypes
from constants.dictionaries import PlayerDicts,DashResetDicts,StawberryDicts,SpringDicts,SpikeDicts, cloudDicts,jumpParticles,fallingBlockDicts,doubleDashResetDicts,FlagDicts


# atlasIMG = pygame.image.load("atlas.png")
class SpriteClass(pygame.sprite.Sprite):
    def __init__(self,x,y,height,width,type,spriteID,flipVertical=None,flipHorizontal=None,rotate=None,playerName = None):
        super().__init__()
        self.type = type
        self.height = height
        self.width = width

        self.spriteID = spriteID
        self.atlasIMG = pygame.image.load("atlas.png")#!Change to global

        self.loadImage(playerName,spriteID)

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

        self.loadImage(playerName,spriteID)

        if flipVertical:
            self.image = pygame.transform.flip(self.image,True,False)
        if flipHorizontal:
            self.image = pygame.transform.flip(self.image,False,True)
        if rotate:
            self.image =pygame.transform.rotate(self.image, rotate)

        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        

    def draw(self,screen):
        screen.blit(self.image,self.rect)
    
    def loadImage(self,playerName,spriteID):
        if self.type == ActorTypes.PLAYER:
            #update image
            if playerName == "Badeline":
                img = pygame.image.load(PlayerDicts.spritesLocationBadeline[self.spriteID])
            else:
                img = pygame.image.load(PlayerDicts.spritesLocation[self.spriteID])

            self.image = img.subsurface((9,19,12,13))

        if self.type == ActorTypes.DASH_RESET:
            #update image
            img = pygame.image.load(DashResetDicts.spritesLocation[spriteID])
            self.image = img.subsurface((2,2,11,11))

        if self.type == ActorTypes.STRAWBERRY:
            #update image
            img = pygame.image.load(StawberryDicts.spritesLocation[spriteID])
            self.image = img.subsurface((0,0,16,16))

        if self.type == ActorTypes.SPRING:
            img = pygame.image.load(SpringDicts.spritesLocation[spriteID])
            self.image = img.subsurface(SpringDicts.spritesImageCrop[spriteID])
            
        if self.type == ActorTypes.SPIKE:
            # self.image = atlasIMG.subsurface((9,11, 7,5))
            img = pygame.image.load(SpikeDicts.spritesLocation[self.spriteID])
            self.image = img.subsurface((1,2,7,6))
        if self.type == ParticleTypes.JUMP:
            self.image = self.atlasIMG.subsurface(jumpParticles.spritesImageCrop[self.spriteID])

        if self.type == ActorTypes.FALLINGBLOCK:
            img = pygame.image.load(fallingBlockDicts.spritesLocation[self.spriteID])
            self.image = img.subsurface((0,0,23,8))
            
        if self.type == ActorTypes.CLOUD:
            self.spriteID = spriteID
            img = pygame.image.load(cloudDicts.spritesLocation[self.spriteID])
            self.image = img.subsurface((6,4,32,14))
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

        if self.type == ActorTypes.DASH_UPGRADE:
            self.image = self.atlasIMG.subsurface((48,48,8,8))
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

        if self.type == ActorTypes.DOUBLE_DASH_RESET:
            self.image = pygame.image.load(doubleDashResetDicts.spritesLocation[self.spriteID])
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        if self.type == ActorTypes.FLAG:
            self.image = self.atlasIMG.subsurface(FlagDicts.spritesImageCrop[self.spriteID])
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        


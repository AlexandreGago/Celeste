import pygame
from actors.actor import Actor
from spriteClass import SpriteClass
from constants.dictionaries import FlagDicts
from constants.enums import ActorTypes,EventType,States



class Flag(Actor):
    def __init__(self, x:int, y:int, serviceLocator) -> None:
        super().__init__(x,y,50,50,serviceLocator)

        self.name = id(self)
        self.type = ActorTypes.FLAG

        #sprite e state
        self.state = States.IDLE
        self.spriteID = "idle1"
        self.sprite = SpriteClass(self.x,self.y,self.height,self.width,self.type,self.spriteID)
        self.animationCounter = 1


    def update(self) -> None:
        if self.animationCounter % 20 == 0:
            self.spriteID = FlagDicts.sprites[self.spriteID]
            self.animationCounter = 1
        self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)
        self.animationCounter += 1

    def draw(self, display:pygame.display) -> None:
        self.sprite.draw(display)
        if self.state == States.COLLECTED:
            #draw "YOU WIN" on top
            text_font = pygame.font.Font('freesansbold.ttf', 100 )
            text_text = text_font.render("YOU WIN", True, "black")
            text_rect = text_text.get_rect()
            text_rect.center = (self.serviceLocator.map.width/2,self.serviceLocator.map.height/8)
            
            display.blit(text_text,text_rect)
            
            text_font = pygame.font.Font('freesansbold.ttf', 64 )
            text_text = text_font.render("Score: "+str(int(self.serviceLocator.score/1000))+"/30", True, "black")
            text_rect = text_text.get_rect()
            text_rect.center = (self.serviceLocator.map.width/2,self.serviceLocator.map.height/4)
            
            display.blit(text_text,text_rect)
            

    def notify(self, entityName:str, event:EventType) -> None:
        if event == EventType.FLAG_COLLISION and self.state == States.IDLE:
            self.state = States.COLLECTED
            self.serviceLocator.soundManager.stop()
            self.serviceLocator.soundManager.play("flag",volume=1)
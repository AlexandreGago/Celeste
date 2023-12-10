import pygame
from actors.actor import Actor
from spriteClass import SpriteClass
from constants.enums import ActorTypes,EventType,States

class FallingBlock(Actor):
    def __init__(self, x:int, y:int,serviceLocator) -> None:
        """
        Creates a falling block

        Args:
            x (int): x position of the falling block
            y (int): y position of the falling block
            serviceLocator (ServiceLocator): ServiceLocator object

        Returns:
            None
        """

        super().__init__(x+5,y+35,15,45,serviceLocator)

        self.name = id(self)
        self.type = ActorTypes.FALLINGBLOCK
        self.state = States.IDLE

        self.spriteID = "idle1"
        self.sprite = SpriteClass(self.x,self.y,self.height,self.width,self.type,self.spriteID)
        self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)
        self.rect = self.sprite.rect

        self.shake = 0
        self.shakeDir = "left"
        self.animationFrameCounter = 0

    def update(self):
        """
        Updates the falling block's position ,sprite and state

        Args:
            None

        Returns:
            None
        """
        if self.state == States.FALLING:# falling state
            if self.animationFrameCounter % 5 == 0: # shake animation every 5 frames
                self.shake += -2 if self.shakeDir == "left" else 2
                self.shakeDir = "left" if self.shake >= 2 else "right" if self.shake <= -2 else self.shakeDir
                self.sprite.update(self.x+self.shake,self.y,self.height,self.width,self.spriteID)
                self.rect = self.sprite.rect

            if self.animationFrameCounter == 30: # falling animation finished , go to outline state
                self.state = States.OUTLINE
                self.spriteID = "outline1"
                self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)
                self.animationFrameCounter = 0
                self.serviceLocator.soundManager.play("fallBlockOutline")

        if self.state == States.OUTLINE:# outline state
            if self.animationFrameCounter == 120:# outline animation finished, go to idle state
                self.state = States.IDLE
                self.spriteID = "idle1"
                self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)
                self.animationFrameCounter = 0
                self.serviceLocator.soundManager.play("fallBlockReset")
                

        self.animationFrameCounter += 1
        

    def draw(self, display:pygame.display):
        """
        Draws the falling block

        Args:
            display (pygame.display): display where the falling block is drawn

        Returns:
            None
        """
        self.sprite.draw(display)

    def notify(self, entityName:str, event:EventType):
        """
        Notifies the falling block of an event

        Args:
            entityName (str): name of the entity that triggered the event
            event (EventType): type of event

        Returns:
            None
        """
        if event == EventType.FALLINGBLOCK_COLLISION and entityName == self.name:# if player collides with it
            if self.state == States.IDLE:# if idle, go to falling state
                self.state = States.FALLING
                self.spriteID = "falling1"
                self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)
                self.animationFrameCounter = 0
                self.serviceLocator.soundManager.play("fallBlockShake")
            if self.state == States.OUTLINE:
                self.animationFrameCounter = 0
        if event == EventType.PLAYER_DEATH :
            self.state = States.IDLE
            self.spriteID = "idle1"
            self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID)
            self.animationFrameCounter = 0
            self.shake = 0
            self.shakeDir = "left"

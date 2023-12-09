import pygame
from actors.actor import Actor
from spriteClass import SpriteClass
from constants.dictionaries import SpikeDicts
from constants.enums import ActorTypes,SpikeOrientations,States



class Spike(Actor):
    def __init__(self, x:int, y:int,orientation:SpikeOrientations) -> None:
        """
        Creates a spike

        Args:
            x (int): x position of the spike
            y (int): y position of the spike
            orientation (SpikeOrientations): orientation of the spike

        Returns:
            None

        """
        xOffset = None
        yOffset = None
        rotateSprite = 0
        self.hitbox = None
        if orientation == SpikeOrientations.UP:# set the hitbox and sprite position based on the orientation
            xOffset = x + 5
            yOffset = y + 30
            self.width = 40
            self.height = 20
            
            self.hitbox = pygame.Rect(xOffset,y+49,self.width,1)

        if orientation == SpikeOrientations.LEFT:# set the hitbox and sprite position based on the orientation
            xOffset = x + 30
            yOffset = y + 5
            self.width = 20
            self.height = 40
            rotateSprite = 90
            
            self.hitbox = pygame.Rect(x+49,yOffset,1,self.height)

        if orientation == SpikeOrientations.DOWN:# set the hitbox and sprite position based on the orientation
            xOffset = x + 5
            yOffset = y
            self.width = 40
            self.height = 20
            rotateSprite = 180
            
            self.hitbox = pygame.Rect(xOffset,y,self.width,1)
        
        if orientation == SpikeOrientations.RIGHT:# set the hitbox and sprite position based on the orientation
            xOffset = x
            yOffset = y + 5
            self.width = 20
            self.height = 40
            rotateSprite = -90
            
            self.hitbox = pygame.Rect(x,yOffset,1,self.height)# set the hitbox and sprite position based on the orientation
            
        super().__init__(xOffset,yOffset,self.height,self.width,None)# create the actor

        self.name = id(self)
        self.type = ActorTypes.SPIKE

        #sprite e state
        self.state = States.IDLE
        self.spriteID = "idle1"
        self.sprite = SpriteClass(self.x,self.y,self.height,self.width,self.type,self.spriteID)
        self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID,rotate = rotateSprite)


    def update(self):
        pass

    def draw(self, display:pygame.display) -> None:
        """
        Draws the spike on the display

        Args:
            display (pygame.display): display to draw the spike on

        Returns:
            None
        """
        self.sprite.draw(display)

    def notify(self, entityName, event) -> None:
        if event == "touchSpike" and entityName == self.name:
            pass
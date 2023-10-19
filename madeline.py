from actor import Actor
import pygame
from enums import ActorTypes
from dictionaries import PlayerStuff
from spriteClass import SpriteClass

GRAVITY = 5

class Player(Actor):
    def __init__(self,x,y,name,ServiceLocator) -> None:
        super().__init__()
        self.name = name
        self.type = ActorTypes.PLAYER
        self.x = x
        self.y = y
        self.state = PlayerStuff.states[0]
        self.ServiceLocator = ServiceLocator
        self.spriteID = PlayerStuff.statesInit[self.state]
        self.jumpPower = 0
        self.orientation = "right"

        self.spriteGroup = pygame.sprite.Group()
        sprite = SpriteClass(100,100,self.type,self.ServiceLocator,self.spriteID)
        self.spriteGroup.add(sprite)
    
    def move(self,newState):
        # print(newState)
        if newState in PlayerStuff.states:
            #change animation
            if self.state != newState and not(newState == "walkLeft" and self.state == "turningLeft") and not(newState == "walkRight" and self.state == "turningRight") and self.state != "jump":
                if (self.state == "walkRight" and newState == "turningLeft") or (self.state == "walkRight" and newState == "walkLeft") or (self.state == "turningRight" and newState == "walkLeft") and self.state != "turningRight":
                    newState = "turningLeft"
                elif (self.state == "walkLeft" and newState == "turningRight") or (self.state == "walkLeft" and newState == "walkRight") or (self.state == "turningLeft" and newState == "walkRight") and self.state != "turningLeft":
                    newState = "turningRight"
                self.state = newState
                self.spriteID = PlayerStuff.statesInit[newState]
                if self.state == "jump":
                    self.jumpPower = 40


            elif self.state == "jump":
                self.y -= self.jumpPower
                self.x += 3*PlayerStuff.statesMovement[newState][0]
                self.jumpPower -= GRAVITY if self.jumpPower > 0 else 0
                if self.ServiceLocator.frameCount % 10 == 0:
                    if self.jumpPower != 0:
                        if self.spriteID == "jump1":
                            self.spriteID = PlayerStuff.sprites[self.spriteID]
                        else:
                            self.spriteID = "jump1"
                    else:
                        if self.spriteID == "jump2":
                            self.spriteID = PlayerStuff.sprites[self.spriteID]
                        if self.ServiceLocator.frameCount % 10== 0:
                            print(self.spriteID)
                            if self.spriteID == "jump3":
                                self.spriteID = PlayerStuff.sprites[self.spriteID]
                            else:
                                self.spriteID = "jump3"

            #move animation every 10 frames
            elif self.ServiceLocator.frameCount % 10 == 0 or ((self.state == "turningLeft" or self.state == "turningRight")and self.ServiceLocator.frameCount % 2 == 0):
                self.spriteID = PlayerStuff.sprites[self.spriteID]

            #move player
            # print(self.y)
            # print(self.state)
            # print(self.x//50*50,self.y // 50 * 50)
            self.x += 3*PlayerStuff.statesMovement[self.state][0]
            if (self.x//50*50,self.y // 50 * 50) not in self.ServiceLocator.map.collision_map:
                self.y += GRAVITY
            else:
                if self.state == "jump":
                    self.state = newState
                    self.spriteID = PlayerStuff.statesInit[newState]
            # if self.y <600:

            #end turning animation
            if self.spriteID == "walkRight2":
                self.state = "walkRight"
            if self.spriteID == "walkLeft2":
                self.state = "walkLeft"

        else:
            print("invalid direction")

        #update sprite
        flip = False
        if self.state == "walkLeft" or self.state == "turningLeft" or (self.state == "jump" and self.orientation == "left"):
            flip = True
            self.orientation = "left"
        else:
            self.orientation = "right"
        self.spriteGroup.update(self.x,self.y,self.spriteID,flip)


     
    def draw(self,display):
        self.spriteGroup.draw(display)
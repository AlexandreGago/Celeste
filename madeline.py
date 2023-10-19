from actor import Actor
import pygame
from enums import ActorTypes
from dictionaries import PlayerStuff
from spriteClass import SpriteClass

GRAVITY = 1
MOVEMENT_X = 3
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
        self.jumpAux = "init"

        self.spriteGroup = pygame.sprite.Group()
        sprite = SpriteClass(100,100,self.type,self.ServiceLocator,self.spriteID)
        self.spriteGroup.add(sprite)
    
    def move(self,newState):
        if newState in PlayerStuff.states:
            if self.state == "jump":
                if self.jumpAux == "init":
                    self.jumpAux = "up"
                    self.jumpPower = 40
                if self.jumpAux == "up":
                    self.y -= 2
                    self.x += MOVEMENT_X*PlayerStuff.statesMovement[newState][0]
                    self.jumpPower -= GRAVITY if self.jumpPower > 0 else 0
                    #update sprite every 10 frames
                    if self.ServiceLocator.frameCount % 10 == 0:
                        if self.spriteID == "jump1":
                            self.spriteID = PlayerStuff.sprites[self.spriteID]
                        else:
                            self.spriteID = "jump1"
                    if self.jumpPower == 0:
                        self.jumpAux = "down"
                        self.spriteID == PlayerStuff.sprites["jump2"]

                elif self.jumpAux == "down":
                    self.y += self.jumpPower
                    self.x += MOVEMENT_X*PlayerStuff.statesMovement[newState][0]
                    if self.ServiceLocator.frameCount % 10 == 0:
                        if self.spriteID == "jump2":
                            self.spriteID = PlayerStuff.sprites[self.spriteID]
                        else:
                            self.spriteID = "jump2"

                    #ground
                    if (self.x//50*50,self.y // 50 * 50) in self.ServiceLocator.map.collision_map:
                        self.jumpAux = "init"
                        self.state = newState
                        self.spriteID = PlayerStuff.statesInit[newState]

            elif self.state == "turningLeft":
                #if the newstate is not the walk left, change the state
                if newState != self.state and newState != "walkLeft":
                    self.state = newState
                    self.spriteID = PlayerStuff.statesInit[newState]    
                #if the animation still didnt end, keep playing it
                elif self.spriteID != "turningLeft8":
                    if self.ServiceLocator.frameCount % 3 == 0:
                        self.spriteID = PlayerStuff.sprites[self.spriteID]
                else: # if the aniamtion ended, change the state to walking
                    self.state = "walkLeft"
                    self.spriteID = PlayerStuff.statesInit[self.state]

            elif self.state == "turningRight":
                if newState != self.state and newState != "walkRight":
                    self.state = newState
                    self.spriteID = PlayerStuff.statesInit[newState]
                elif self.spriteID != "turningRight8":
                    if self.ServiceLocator.frameCount % 3 == 0:
                        self.spriteID = PlayerStuff.sprites[self.spriteID]
                else:
                    self.state = "walkRight"
                    self.spriteID = PlayerStuff.statesInit[self.state]

            elif self.state == "walkRight" or self.state == "walkLeft" or self.state == "crouch" or self.state == "idle":
                if newState != self.state:
                    #turn left
                    if self.orientation == "right" and newState == "walkLeft":
                        newState = "turningLeft"
                    elif self.orientation == "left" and newState == "walkRight":
                        newState = "turningRight"
                    self.state = newState
                    self.spriteID = PlayerStuff.statesInit[newState]
                else:
                    if self.ServiceLocator.frameCount % 10 == 0:
                        self.spriteID = PlayerStuff.sprites[self.spriteID]

            self.x += MOVEMENT_X*PlayerStuff.statesMovement[self.state][0]
            if (self.x//50*50,self.y // 50 * 50) not in self.ServiceLocator.map.collision_map:
                self.y += GRAVITY
            #we don't have the mirrored sprites, so we just flip the sprite
            if self.state == "walkLeft" or self.state == "turningLeft":
                self.orientation = "left"
            elif self.state == "turningRight" or self.state == "walkRight":
                self.orientation = "right"
            print(self.orientation)
            #update sprite
            self.spriteGroup.update(self.x,self.y,self.spriteID,self.orientation=="left")
        else:
            print("invalid direction")
                


     
    def draw(self,display):
        self.spriteGroup.draw(display)
from actor import Actor
import pygame
from enums import ActorTypes
from dictionaries import PlayerStuff
from spriteClass import SpriteClass

Y_GRAVITY = 5
MOVEMENT_X = 5
points = [
    [pygame.Vector2(0,0),0,pygame.Vector2(0,0),25], #first point is the center of the head
    [pygame.Vector2(-6,4),12,pygame.Vector2(0,0),23],
    [pygame.Vector2(-4,4),11,pygame.Vector2(0,0),22],
    [pygame.Vector2(-2,2),10.5,pygame.Vector2(0,0),21], 
    [pygame.Vector2(-2,2),10,pygame.Vector2(0,0),20],
    [pygame.Vector2(-2,2),9.5,pygame.Vector2(0,0),19],
    [pygame.Vector2(-2,2),9,pygame.Vector2(0,0),18],
    [pygame.Vector2(-2,2),8.5,pygame.Vector2(0,0),17],
    [pygame.Vector2(-2,2),8,pygame.Vector2(0,0),16],
]
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

        self.height = 80
        self.width = 80

        self.spriteGroup = pygame.sprite.Group()
        sprite = SpriteClass(self.height,self.width,self.type,self.ServiceLocator,self.spriteID)
        self.spriteGroup.add(sprite)
    
    def move(self,newState):
        if newState in PlayerStuff.states:
            if self.state == "jump":
                if self.jumpAux == "init":
                    self.jumpAux = "up"
                    self.jumpPower = 100
                    # self.height = 80
                    # self.width = 80
                    self.ServiceLocator.frameCount = 0
                if self.jumpAux == "up":
                    self.y -= 10
                    self.x += MOVEMENT_X*PlayerStuff.statesMovement[newState][0]
                    self.jumpPower -= Y_GRAVITY if self.jumpPower > 0 else 0
                    #update sprite every 10 frames
                    if self.ServiceLocator.frameCount % 10 == 0:
                        if self.spriteID == "jump1":
                            self.spriteID = PlayerStuff.sprites[self.spriteID]
                        else:
                            # self.height= 100
                            # self.width = 100
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
                        self.ServiceLocator.frameCount = 0


            elif self.state == "turningLeft":
                #if the newstate is not the walk left, change the state
                if newState != self.state and newState != "walkLeft":
                    self.state = newState
                    self.spriteID = PlayerStuff.statesInit[newState]   
                    self.ServiceLocator.frameCount = 0

                #if the animation still didnt end, keep playing it
                elif self.spriteID != "turningLeft8":
                    if self.ServiceLocator.frameCount % 3 == 0:
                        self.spriteID = PlayerStuff.sprites[self.spriteID]
                else: # if the aniamtion ended, change the state to walking
                    self.state = "walkLeft"
                    self.spriteID = PlayerStuff.statesInit[self.state]
                    self.ServiceLocator.frameCount = 0

            elif self.state == "turningRight":
                if newState != self.state and newState != "walkRight":
                    self.state = newState
                    self.spriteID = PlayerStuff.statesInit[newState]
                    self.ServiceLocator.frameCount = 0

                elif self.spriteID != "turningRight8":
                    if self.ServiceLocator.frameCount % 3 == 0:
                        self.spriteID = PlayerStuff.sprites[self.spriteID]
                else:
                    self.state = "walkRight"
                    self.spriteID = PlayerStuff.statesInit[self.state]
                    self.ServiceLocator.frameCount = 0

            elif self.state == "walkRight" or self.state == "walkLeft" or self.state == "crouch" or self.state == "idle":
                if newState != self.state:
                    #turn left
                    if self.orientation == "right" and newState == "walkLeft":
                        newState = "turningLeft"
                    elif self.orientation == "left" and newState == "walkRight":
                        newState = "turningRight"
                    self.state = newState
                    self.spriteID = PlayerStuff.statesInit[newState]
                    self.ServiceLocator.frameCount = 0

                else:
                    if self.ServiceLocator.frameCount % 10 == 0:
                        self.spriteID = PlayerStuff.sprites[self.spriteID]

            self.x += MOVEMENT_X*PlayerStuff.statesMovement[self.state][0]
            if (self.x//50*50,self.y // 50 * 50) not in self.ServiceLocator.map.collision_map:
                self.y += Y_GRAVITY
                
            #we don't have the mirrored sprites, so we just flip the sprite
            if self.state == "walkLeft" or self.state == "turningLeft":
                self.orientation = "left"
            elif self.state == "turningRight" or self.state == "walkRight":
                self.orientation = "right"
            #update sprite
            self.spriteGroup.update(self.x,self.y,self.height,self.width,self.spriteID,self.orientation=="left")
            self.drawHair(self.ServiceLocator.getDisplay())
        else:
            print("invalid direction")

    def drawHair(self, display):
        # Hair circle around the head
        for i in range (len(points)-1,-1,-1):
            if i == 0:
                points[i][2] = pygame.Vector2(int(self.x + self.width / 2), int(self.y + self.height / 2-10))
                continue
            if self.orientation == "right":
                points[i][2] = points[i][0] + points[i-1][2]
            else:
                points[i][2] =  points[i-1][2]+(points[i][0][0]*-1,points[i][0][1])
        for i in range(len(points)):
            if i == 0:
                continue
            if points[i][2].distance_to(points[i][0]+points[i-1][2]) > points[i][1]:
                dir = (points[i][2]-(points[i-1][2]+points[i][0])).normalize()
                offset = dir * points[i][1]
                points[i][2] = points[i-1][2] + points[i][0]+ offset
                
        
        for i in range (len(points)):
            pygame.draw.circle(display, (128, 0, 0), points[i][2], points[i][3])

    
    def draw(self,display):
        self.drawHair(display)
        self.spriteGroup.draw(display)
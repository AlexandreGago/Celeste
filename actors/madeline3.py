from actors.actor import Actor
import pygame
import pygame.gfxdraw
from constants.enums import ActorTypes,PlayerStates,PlayerOrientation
from constants.dictionaries import PlayerStuff, physicsValues
from spriteClass import SpriteClass
from states import *
import utils.utils as utils
import math
from actors.spriteParticle import SpriteParticle
from utils.physics import Physics
import time

HEIGHT = 800
MAX_DASHES = 1
DASH_COOLDOWN = 5

ANIMATION_SPEEDS = {
    "jump": 10,
    "turn": 2,
    "dash" : 1
}

#(offset_x,offset_y),max_dist,(pos_x,pos_y),radius
points = [
    [pygame.Vector2(0,0),0,pygame.Vector2(0,0),15], #first point is the center of the head
    [pygame.Vector2(-6,4),9,pygame.Vector2(0,0),14],
    [pygame.Vector2(-2,4),8.5,pygame.Vector2(0,0),13],
    [pygame.Vector2(-4,4),8,pygame.Vector2(0,0),12], 
    [pygame.Vector2(-4,2),7.5,pygame.Vector2(0,0),11],
    [pygame.Vector2(-2,2),7,pygame.Vector2(0,0),10],
]


class Player(Actor):
    def __init__(self,x,y,name,serviceLocator) -> None:
        """
        Player class
        
        Args:
            x (int): spawn x position
            y (int): spawn y position
            name (string): name of the player
            serviceLocator (ServiceLocator): service locator

        Returns:
            None

        """
        #player localizations
        self.spawnX = x
        self.spawnY = y
        self.x = x
        self.y = 800
        
        #play type
        self.type = ActorTypes.PLAYER
        
        #physics
        self.physics = Physics()
        
        #call the parent constructor (Actor)
        super().__init__(x,800,50,50,serviceLocator)
        self.name = name
        self.serviceLocator = serviceLocator

        #collisions
        self.collisions = [0,0,0,0]
        
        #player size and state
        self.height = 50
        self.width = 50
        self.orientation = PlayerOrientation.RIGHT
        self.state = PlayerStates.RESPAWN
        self.alive = False
        
        #sprite
        self.spriteID = f"{self.state.value}1"
        self.sprite = SpriteClass(self.x,self.y,self.height,self.width,self.type,self.spriteID)
        self.animationFrameCounter = 0
        
        #dash
        self.dashCount = 1
        #Particles
        self.particles = []
        
        self.springCollided = False

        self.airborne = 0
        self.dashCooldown = 0
        
        return
    
    def spawn(self):
        if self.y > self.spawnY:    
            self.y -= 8
        else:
            return True
        return False
             
    def respawn(self):
        self.alive = self.spawn()
        if self.alive:
            self.state = PlayerStates.IDLE
            self.spriteID = f"{self.state.value}1"
            self.animationFrameCounter = 0
            self.physics.reset()

    def jump(self):
        if self.animationFrameCounter % 10 == 0:
            self.spriteID = PlayerStuff.sprites[self.spriteID]
        pass
    
    def dash(self):
        if self.animationFrameCounter % 10 == 0:
            self.spriteID = PlayerStuff.sprites[self.spriteID]

    def turn(self):
        if self.animationFrameCounter % ANIMATION_SPEEDS["turn"] == 0:
            self.spriteID = PlayerStuff.sprites[self.spriteID]
            
    def idle(self):
        if self.animationFrameCounter % 10 == 0:
            self.spriteID = PlayerStuff.sprites[self.spriteID]

    def walk(self):
        if self.animationFrameCounter % 10 == 0:
            self.spriteID = PlayerStuff.sprites[self.spriteID]

    def crouch(self):
        if self.animationFrameCounter % 10 == 0:
            self.spriteID = PlayerStuff.sprites[self.spriteID]
            
    def lookup(self):
        if self.animationFrameCounter % 10 == 0:
            self.spriteID = PlayerStuff.sprites[self.spriteID]
    def falling(self):
        if self.animationFrameCounter % 10 == 0:
            self.spriteID = PlayerStuff.sprites[self.spriteID]
    
    def updateState(self,xInput,yInput,dashInput,jumpInput):
        """"
        This is done to decide if the current state is changed or kept,
        it is done after the move function so that the collisions are updated
        """
        newState = self.vectorToState(xInput,yInput,dashInput,jumpInput)
        
        #reduce the dash cooldown
        if self.state != PlayerStates.DASH : # dash cooldown
            self.dashCooldown -= 1 if self.dashCooldown > 0 else 0
                        #spring collision
        #reset dash count if we collide with a spring
        if self.springCollided:
            # self.physics.speed[1] = -physicsValues.spring["power"]
            self.dashCount = MAX_DASHES
            newState = PlayerStates.JUMP
        #if we are dead, respawn
        if not self.alive :
            newState = PlayerStates.RESPAWN
        #we are alive
        else:
            #if we are jumping, keep jumping unless we are dashing
            if self.state == PlayerStates.JUMP:
                if newState != PlayerStates.DASH and self.airborne == -1:
                    newState = PlayerStates.JUMP
                    
            elif self.state == PlayerStates.DASH:
                if self.orientation == PlayerOrientation.RIGHT:
                    if self.physics.speed[0] > physicsValues.air["maxSpeed"] or self.physics.speed[1] < -physicsValues.air["maxSpeed"]:
                        newState = PlayerStates.DASH
                else:
                    if self.physics.speed[0] < -physicsValues.air["maxSpeed"] or self.physics.speed[1] < -physicsValues.air["maxSpeed"]: # of the speed is greater than the max speed, keep dashing
                        newState = PlayerStates.DASH

            elif self.state in [PlayerStates.TURN]:
                if newState in [PlayerStates.JUMP,PlayerStates.DASH]:  #!this can be removed for a smoother animation
                    pass
                elif self.spriteID != "turn8":
                    newState = PlayerStates.TURN
                
            elif self.state in [PlayerStates.WALK]:
                # if the nes state is jump or dash, exit walk and enter them
                if newState == PlayerStates.JUMP or newState == PlayerStates.DASH:  
                    pass
                elif ((self.orientation == PlayerOrientation.RIGHT) and (xInput == -1)) or (self.orientation == PlayerOrientation.LEFT and xInput > 0):
                    newState = PlayerStates.TURN
                elif xInput < 0 and self.collisions[0] and not self.collisions[3] and self.physics.speed[1]>=0 : # change to wallhug
                    newState = PlayerStates.WALLHUG
                elif xInput > 0 and self.collisions[1] and not self.collisions[3] and self.physics.speed[1]>=0: # change to wallhug
                    newState =  PlayerStates.WALLHUG

            elif self.state in [PlayerStates.WALLHUG]:
                if not self.collisions[3]:
                    if xInput < 0 and self.collisions[0]:
                        newState = PlayerStates.WALLHUG
                    if xInput > 0 and self.collisions[1]:
                        newState =  PlayerStates.WALLHUG

                
            elif self.state in [PlayerStates.CROUCH]:
                pass 
                
            elif self.state in [PlayerStates.IDLE]:

                if newState == PlayerStates.JUMP or newState == PlayerStates.DASH:  
                    pass
                elif ((self.orientation == PlayerOrientation.RIGHT) and (xInput == -1)) or (self.orientation == PlayerOrientation.LEFT and xInput > 0):
                    newState = PlayerStates.TURN

                elif self.airborne == 1:
                    newState = PlayerStates.FALLING
                
            elif self.state in [PlayerStates.RESPAWN]:
                if self.alive: #if the player is alive, change the state else maintain the state
                    pass
                else:
                    newState = PlayerStates.RESPAWN
                
            elif self.state in [PlayerStates.LOOKUP]:#TODO
                pass

            elif self.state in [PlayerStates.FALLING]:
                print(self.airborne)
                if newState == PlayerStates.DASH :  
                    pass
                elif self.airborne != 0:
                    newState = PlayerStates.FALLING

            elif self.state in [PlayerStates.LOOKUP]:
                pass
        
        return newState
    
    def move(self,vector) -> None:
        #process inputs
        xInput,yInput,dashInput,jumpInput = vector
        dashInput, jumpInput = bool(dashInput), bool(jumpInput)
        dashInput = dashInput and self.dashCount >=1 and self.dashCooldown <= 0
        print(self.state)
        if self.alive:
            #update the position
            temp_x,temp_y = self.physics.move(self.x,self.y,xInput,yInput,dashInput,jumpInput,self.collisions,self.orientation,self.springCollided)
            #!change place?
            if self.state == PlayerStates.WALLHUG:
                diff = self.y - temp_y
                temp_y = temp_y + diff/2
                
            #check for collisions with terrain, update the position if there is a collision
            self.checkCorrectCollisions(temp_x,temp_y) 

            #check for collisions with the rest of the actors
            self.actorCollision()

            #!check if we are in the air after the movement
            if self.physics.speed[1] < 0:
                self.airborne = -1
            elif self.physics.speed[1] > 0:
                self.airborne = 1
            else:
                if self.collisions[3]:
                    self.airborne = 0
                else:
                    self.airborne = 1

            #update the state
            newState = self.updateState(xInput,yInput,dashInput,jumpInput)
             # if the state changed, reset the animation frame counter and the spriteID
            if self.state != newState:
                self.animationFrameCounter = 1
                self.spriteID = f"{newState.value}1"
                if newState == PlayerStates.DASH:
                    self.dashCount -= 1 if self.dashCount > 0 else 0 
                    self.dashCooldown = DASH_COOLDOWN
                    self.serviceLocator.soundManager.play("dash")
                if newState == PlayerStates.JUMP:
                    self.serviceLocator.soundManager.play("jump") 
            self.state = newState
        
        #update orientation (cannot be moved up because it is used by updateState)
        self.orientation = self.updateOrientation(xInput)
        
        
        #update the sprite corresponding to the state
        match self.state:
            case PlayerStates.JUMP:
                self.jump()
            case PlayerStates.DASH:
                self.dash()
            case PlayerStates.TURN:
                self.turn()
            case PlayerStates.WALK:
                self.walk()
            case PlayerStates.CROUCH:
                self.crouch()
            case PlayerStates.IDLE:
                self.idle()
            case PlayerStates.LOOKUP: 
                self.lookup()
            case PlayerStates.RESPAWN:
                self.respawn()
            case PlayerStates.FALLING:
                self.falling()
            case PlayerStates.LOOKUP:
                self.lookup()
            case _:
                pass

            
        #update particles and remove the ones that are done
        for particle in self.particles:
            if particle.update():
                self.particles.remove(particle)
        
        self.animationFrameCounter += 1
        self.sprite.update(self.x,self.y,self.height,self.width,self.spriteID,self.orientation == PlayerOrientation.LEFT)
        pygame.draw.rect(self.serviceLocator.display,(0,0,255),self.sprite.rect,1)

    #draws the hair
    def drawHair(self, display):
        #offset for the orientation of the character
        if PlayerStuff.spritesHairOffset[self.state][self.spriteID]:
            offsetDirX = PlayerStuff.spritesHairOffset[self.state][self.spriteID][0] + 8 if self.orientation == PlayerOrientation.RIGHT else PlayerStuff.spritesHairOffset[self.state][self.spriteID][0]*-1 - 8
            offsetDirY = PlayerStuff.spritesHairOffset[self.state][self.spriteID][1] + 12
        for i in range (len(points)-1,-1,-1):
            if i == 0:
                points[i][2] = pygame.Vector2(int(self.x + self.width / 2 +offsetDirX), int(self.y + self.height / 2-offsetDirY))
                continue
            if self.orientation == PlayerOrientation.RIGHT:
                points[i][2] = points[i][0] + points[i-1][2] 
            else:
                points[i][2] =  points[i-1][2]+(points[i][0][0]*-1,points[i][0][1])

        for i in range(len(points)):
            if i == 0:
                continue
            if self.orientation == PlayerOrientation.RIGHT:
                if points[i][2].distance_to(points[i][0]+points[i-1][2]) > points[i][1]:
                    dir = (points[i][2]-(points[i-1][2]+points[i][0])).normalize()
                    offset = dir * points[i][1]
                    points[i][2] = points[i-1][2] + points[i][0]+ offset
            else:
                if points[i][2].distance_to((points[i][0][0]*-1,points[i][0][1])+points[i-1][2]) > points[i][1]:
                    dir = (points[i][2]-(points[i-1][2]+(points[i][0][0]*-1,points[i][0][1]))).normalize()
                    offset = dir * points[i][1]
                    points[i][2] = points[i-1][2] + (points[i][0][0]*-1,points[i][0][1])+ offset
            
                
        
        for i in range (len(points)-1,-1,-1):
            if self.airborne == 0:
                if self.dashCooldown > 0:
                    pygame.draw.circle(display, (255, 255, 255), points[i][2], points[i][3]) # white
                else:
                    pygame.draw.circle(display, (172, 50, 49), points[i][2], points[i][3]) # brown
            else:
                if self.dashCount <= 0:
                    pygame.draw.circle(display, (69, 194, 255), points[i][2], points[i][3]) # blue
                else:
                    pygame.draw.circle(display, (172, 50, 49), points[i][2], points[i][3]) # brown

            # pygame.draw.circle(display, (172, 50, 49), points[i][2], points[i][3],width = 3) # brown
                    


    
    def draw(self,display: pygame.display) -> None:
        """
        Draw the player	and its hair

        Args:   
            display (pygame.display): display to draw the player
        
        Returns:
            None
        """
        #draw hair first to be behind the player
        self.drawHair(display)
        self.sprite.draw(display)
        for particle in self.particles:
            particle.draw(display)



    def update(self) -> None:
        pass
    def notify(self,actor,event):
        pass
    
    def levelComplete(self):
        if self.y < 0:
            return True
        else:
            return False
    
    #TODO
    def checkCorrectCollisions(self,x,y):
    #left, right, top, bottom
        self.collisions = [0,0,0,0]

        self.sprite.rect.y = y
        for tile in self.serviceLocator.map.walls:
            if self.sprite.rect.colliderect(tile):
                #ceiling
                if tile.rect.bottom - self.sprite.rect.top <= physicsValues.dash["power"]:
                    self.collisions[2] = 1
                    self.physics.speed[1] = 0
                    self.sprite.rect.y = tile.rect.bottom
                    self.serviceLocator.display.fill((255,0,0),tile.rect)

                #floor
                elif tile.rect.top - self.sprite.rect.bottom >= - physicsValues.dash["power"]:
                    self.collisions[3] = 1
                    self.physics.speed[1] = 0
                    self.dashCount = MAX_DASHES
                    self.sprite.rect.y = tile.rect.top - self.height
                    self.serviceLocator.display.fill((255,0,0),tile.rect)

        self.sprite.rect.x = x
     
        for tile in self.serviceLocator.map.walls:
            # if tile.rect.right == 250:
            if self.sprite.rect.colliderect(tile):
                #left
                if tile.rect.right - self.sprite.rect.left <= physicsValues.dash["power"]:
                    self.collisions[0] = 1
                    self.physics.speed[0] = 0
                    self.sprite.rect.x = tile.rect.right


                    self.serviceLocator.display.fill((255,0,0),tile.rect)
                #right
                elif tile.rect.left - self.sprite.rect.right >= - physicsValues.dash["power"]:
                    self.collisions[1] = 1
                    self.physics.speed[0] = 0
                    x = tile.rect.left - self.width
                    self.sprite.rect.x = x

                    self.serviceLocator.display.fill((255,0,0),tile.rect)

        self.x = self.sprite.rect.x
        self.y = self.sprite.rect.y

    def updateOrientation(self,xInput):
        return PlayerOrientation.RIGHT if xInput > 0 else PlayerOrientation.LEFT if xInput < 0 else self.orientation
    
    def vectorToState(self,xInput,yInput,dashInput,jumpInput):
        if dashInput == 1:
            return PlayerStates.DASH
        if yInput == -1:# crouch
            return PlayerStates.CROUCH
        if jumpInput == 1:
            return PlayerStates.JUMP
        if xInput != 0:
            return PlayerStates.WALK
        if yInput == 1:
            return PlayerStates.LOOKUP
        
        return PlayerStates.IDLE
        
    def actorCollision(self):
            #check collisions for the rest of the actors
            self.springCollided = False
            for actor in self.serviceLocator.actorList:
                if actor.type == ActorTypes.DASH_RESET: 
                    #if the dash reset is on and the player ha sno dashes, after collision, reset the dash and notify the dash reset entity
                    if self.dashCount <= 0 and actor.state =="idle" and self.sprite.rect.colliderect(actor.sprite.rect):
                        self.dashCount = MAX_DASHES
                        self.dashCooldown = DASH_COOLDOWN
                        #notify observers
                        for obs in self.observers:
                            obs.notify(actor.name,"dashReset")
                            
                if actor.type == ActorTypes.SPRING:
                    if self.sprite.rect.colliderect(actor.sprite.rect) :#and self.springCollsionCooldown == 0:
                        for obs in self.observers:
                            obs.notify(actor.name,"springCollision")
                        self.springCollided = True
                        # self.springCollsionCooldown = SPRING_COLLISION_COOLDOWN

                if actor.type == ActorTypes.STRAWBERRY:
                    if self.sprite.rect.colliderect(actor.sprite.rect) and actor.state == "idle":
                        #notify observers
                        for obs in self.observers:
                            obs.notify(actor.name,"strawberryCollected")
                        #self.playSound("strawberry",1)
                            
                if actor.type == ActorTypes.SPIKE or self.y > HEIGHT:
                    if self.sprite.rect.colliderect(actor.sprite.rect):
                        self.alive = False
                        self.x = self.spawnX
                        self.y = 800
                        #self.playSound("death",1)
                        self.serviceLocator.soundManager.play("death")
                        
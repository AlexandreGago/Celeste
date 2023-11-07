from actors.actor import Actor
import pygame
import pygame.gfxdraw
from constants.enums import ActorTypes,PlayerStates,PlayerOrientation
from constants.dictionaries import PlayerStuff
from spriteClass import SpriteClass
from states import *
import utils.utils as utils
import math
from actors.spriteParticle import SpriteParticle
from utils.physics import Physics
import time


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
        self.y = y
        
        #play type
        self.type = ActorTypes.PLAYER
        
        #physics
        self.physics = Physics(x,y)
        
        #call the parent constructor (Actor)
        super().__init__(x,800,50,50,serviceLocator)
        self.name = name
        self.serviceLocator = serviceLocator

        #collisions
        self.collisions = [0,0]
        
        #player size and state
        self.height = 50
        self.width = 50
        self.orientation = PlayerOrientation.RIGHT
        self.state = PlayerStates.IDLE
        
        #sprite
        self.spriteID = f"{self.state.value}1"
        self.sprite = SpriteClass(self.x,self.y,self.height,self.width,self.type,self.spriteID)
        self.animationFrameCounter = 0
        
        #dash
        self.dashCount = 1
        #Particles
        self.particles = []
        
        
        return
    
    def spawn(self):
        if self.y > self.spawnHeight:    
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
            self.enableCollision = True
            self.physics.reset(self.x,self.y)

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
   
    
    def updateState(self,newState):
        """"
        This is done to decide if the current state is changed or kept,
        it is done after the move function so that the collisions are updated
        """
        state = self.state
        if self.state == PlayerStates.JUMP:
            state = newState 
            
        elif self.state == PlayerStates.DASH:
            state = newState 
            
        elif self.state in [PlayerStates.TURN]:
            state = newState 
            
        elif self.state in [PlayerStates.WALK]:
            state = newState   
            
        elif self.state in [PlayerStates.CROUCH]:
            state = newState   
            
        elif self.state in [PlayerStates.IDLE]:
            state = newState   
            
        elif self.state in [PlayerStates.RESPAWN]:
            state = newState 
            
        return state
    
    def move(self,vector) -> None:
        print("vector",vector)
        #process inputs
        xInput,yInput,dashInput,jumpInput = vector
        dashInput, jumpInput = bool(dashInput), bool(jumpInput)
        
        #update collisions
        self.collisions = self.checkCollisions()
        
        #update orientation
        self.orientation = self.updateOrientation(xInput)
        
        #update the position
        self.x,self.y = self.physics.move(xInput,yInput,dashInput,jumpInput,self.collisions,self.orientation)
        
        #update the state
        newState = PlayerStuff.vectorToState[(xInput,yInput)]
        self.state = self.updateState(newState)
        
        # if the state changed, reset the animation frame counter and the spriteID
        if self.state != newState:
            self.animationFrameCounter = 1
            #initialize the spriteID
            self.spriteID = f"{self.state.value}1"

        #update the sprite corresponding to the state
        if self.state == PlayerStates.JUMP:
            self.jump()
        elif self.state == PlayerStates.DASH:
            self.dash()
        elif self.state in [PlayerStates.TURN]:
            self.turn()
        elif self.state in [PlayerStates.WALK]:
            self.walk()
        elif self.state in [PlayerStates.CROUCH]:
            self.crouch()
        elif self.state in [PlayerStates.IDLE]:
            self.idle()
        elif self.state in [PlayerStates.RESPAWN]:
            self.respawn()
            
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
            if self.collisions[1]:
                if self.dashRefreshTimer <= 0:
                    pygame.draw.circle(display, (172, 50, 49), points[i][2], points[i][3]) # brown
                else:
                    pygame.draw.circle(display, (255, 255, 255), points[i][2], points[i][3]) # white
            else:
                if self.dashCount <= 0:
                    pygame.draw.circle(display, (69, 194, 255), points[i][2], points[i][3]) # blue
                else:
                    pygame.draw.circle(display, (172, 50, 49), points[i][2], points[i][3]) # brown
            # pygame.draw.circle(display, (0, 0, 0), points[i][2], points[i][3],width = 3) # brown
                    


    
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
    def checkCollisions(self):
        return self.collisions
    #TODO
    def updateOrientation(self,xInput):
        self.orientation
        
    def actorCollision(self,actor):
            #check collisions for the rest of the actors
            for actor in self.serviceLocator.actorList:
                if actor.type == ActorTypes.DASH_RESET:
                    #if the dash reset is on and the player ha sno dashes, after collision, reset the dash and notify the dash reset entity
                    if self.dashCount == 0 and actor.state =="idle" and self.sprite.rect.colliderect(actor.sprite.rect):
                        self.dashCount = 1
                        #notify observers
                        for obs in self.observers:
                            obs.notify(actor.name,"dashReset")
                            
                if actor.type == ActorTypes.SPRING:
                    if self.sprite.rect.colliderect(actor.sprite.rect) and self.springCollsionCooldown == 0:
                        for obs in self.observers:
                            obs.notify(actor.name,"springCollision")
                            self.springCollided = True
                            self.springCollsionCooldown = SPRING_COLLISION_COOLDOWN
                        #self.playSound("spring",1)

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
                        

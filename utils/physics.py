import pygame
# import utils.utils as utils
import utils
from constants.enums import ActorTypes,PlayerStates,PlayerOrientation

ground = {
    "maxSpeed": 5,
    "acceleration": 0.5,
    "deceleration": 0.5,
}

air = {
    "maxSpeed": 5,
    "gravity": 0.5,
    
}

dash = {
    "power": 12,
}

jump = {
    "power": 10,
}

def calculateSpeed(val:int, target:int, amount:int) -> int:
    """
    Accelerate or decelerate but don't overshoot the target

    Args:
        val (int): current value
        target (int): target value
        amount (int): amount to change by

    Returns:
        int: new value
    """
    #if the value is greater than the target, decelerate
    if val > target:
        #decelerate val by amount but don't go below the target
        return max(val-amount, target)
    else:
        #accelerate val by amount but don't go above the target
        return min(val+amount, target)

class Physics():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.speed = [0,0]
    
    def move(self,xInput,yInput,dashInput,jumpInput,collisions,orientation):
        """

        Args:
            xInput (int): -1 for left, 1 for right, 0 for no input
            yInput (int): 1 for up, -1 for down, 0 for no input
            dashInput (bool) : True if dash button is pressed
            jumpInput (bool) : True if jump button is pressed
            collisions (list): list of collisions [wallCollision,groundCollision] -> 1 for collision, 0 for no collision
            orientation (int): orientation -> PlayerOrientation.RIGHT/LEFT
        """
        #collisions = [wallCollision,groundCollision]

        
        #if over the speed limit, decelerate
        if abs(self.speed[0]) > ground["maxSpeed"]:
            #get the sign of the speed to determine which way to decelerate
            sign = 1 if self.speed[0] > 0 else -1
            self.speed[0] = calculateSpeed(self.speed[0], ground["maxSpeed"] * sign , ground["deceleration"])
        #if under the speed limit, accelerate, but don't overshoot the limit
        #movement[0] is the direction the player is trying to move
        else:
            self.speed[0] = calculateSpeed(self.speed[0], xInput * ground["maxSpeed"], ground["acceleration"])

        #!COYOTE
        #if player pressed jump and is grounded, jump
        if jumpInput and collisions[1]:
            self.speed[1] = -jump["power"]
        
        else:
            #if not grounded, apply gravity
            sign = 1 if self.speed[1] < 0 else -1
            print(self.speed[1])
            print(sign)
            self.speed[1] += calculateSpeed(self.speed[1], air["maxSpeed"]*sign, air["gravity"])
        

        if dashInput: #Dash
            self.speed[0] = dash["power"] * xInput
            self.speed[1] = dash["power"] * yInput

        
        #!here or in update?
        self.x += self.speed[0]
        self.y += self.speed[1]
        return self.x, self.y

    def update(self):
        self.x += self.speed[0]
        self.y += self.speed[1]

    def reset(self):
        self.speed = [0,0]
        self.grounded = False
        self.orientation = PlayerOrientation.RIGHT
        
class Player(Physics):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = 50
        self.height = 50
        self.color = (255,0,0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, self.rect)

# WIDTH, HEIGHT = 800, 800

# player = Player(400,400)
# screen = pygame.display.set_mode((WIDTH,HEIGHT))
# clock = pygame.time.Clock()

# pygame.init()
# while True:
#     keys = pygame.key.get_pressed()
#     keys = utils.parsePressedKeys(keys)   
#     if pygame.K_c in keys:
#         keys.remove(pygame.K_c)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN:
#             if event.key==pygame.K_c:
#                 keys.append(pygame.K_c)
    
#     movement = [0,0,0]
#     for key in keys:
#         if key == pygame.K_LEFT:
#             movement[0] -= 1
#         if key == pygame.K_RIGHT:
#             movement[0] += 1
#         if key == pygame.K_UP:
#             movement[1] -= 1
#         if key == pygame.K_DOWN:
#             movement[1] += 1
#         if key == pygame.K_c:
#             movement[2] += 1

#     player.move(movement)
#     player.update()
#     screen.fill((0,0,0))
#     player.draw(screen)
#     pygame.display.update()
#     clock.tick(60)

        
        
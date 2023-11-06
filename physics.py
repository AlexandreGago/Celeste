import pygame
import utils.utils as utils

ground = {
    "maxSpeed": 5,
    "acceleration": 0.5,
    "deceleration": 0.5,
}
air = {
    "maxSpeed": 5,
    "acceleration": 0.5,
    "deceleration": 0.5,
}

dash = {
    "power": 12,
}
jump = {
    "power": 10,
}
class Physics():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.speed = [0,0]
        self.grounded = False
        
        self.orientation = 1 # 1 = right, -1 = left
    
    def move(self, movement):
       
        print(self.speed,movement)
        
        if self.y > 400: #Decide if the player is touching ground
            self.grounded = True
            self.speed[1] = 0
        else:
            self.grounded = False
            
        self.orientation = 1 if movement[0] > 0 else -1 if movement[0] < 0 else self.orientation
        #movement -> [x, y, dash]
        if movement[0] < 0: #left
            if self.speed[0] < -ground["maxSpeed"]: # decelerate
                self.speed[0] = self.speed[0] + ground["deceleration"] if self.speed[0] < ground["maxSpeed"] - ground["deceleration"] else -ground["maxSpeed"]
            else:
                self.speed[0] = max(self.speed[0] - ground["acceleration"], -ground["maxSpeed"])

        elif movement[0] > 0:#right
            if self.speed[0] > ground["maxSpeed"]:
                self.speed[0] = self.speed[0] - ground["deceleration"] if self.speed[0] > ground["maxSpeed"] + ground["deceleration"] else ground["maxSpeed"]
            else:
                self.speed[0] = min(self.speed[0] + ground["acceleration"], ground["maxSpeed"])
        else:#decelerate with no input
            self.speed[0] = max(self.speed[0]-ground["deceleration"],0) if self.speed[0] > 0 else min(self.speed[0]+ground["deceleration"],0)
            
        if movement[1] < 0 and self.grounded: # jump
            self.speed[1] -= jump["power"] # jump power
        
        if movement[2] > 0: #Dash
            if movement[0] > 0:#right
                self.speed[0] = dash["power"]
            if movement[0] < 0:#left
                self.speed[0] = -dash["power"]
            if movement[1] < 0:#up
                self.speed[1] = -dash["power"]                
            if movement[1] > 0:#down
                self.speed[1] = dash["power"]
            
        if not self.grounded:
            self.speed[1] += air["deceleration"]

    def update(self):
        self.x += self.speed[0]
        self.y += self.speed[1]

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

WIDTH, HEIGHT = 800, 800

player = Player(400,400)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

pygame.init()
while True:
    keys = pygame.key.get_pressed()
    keys = utils.parsePressedKeys(keys)   
    if pygame.K_c in keys:
        keys.remove(pygame.K_c)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_c:
                keys.append(pygame.K_c)
    
    movement = [0,0,0]
    for key in keys:
        if key == pygame.K_LEFT:
            movement[0] -= 1
        if key == pygame.K_RIGHT:
            movement[0] += 1
        if key == pygame.K_UP:
            movement[1] -= 1
        if key == pygame.K_DOWN:
            movement[1] += 1
        if key == pygame.K_c:
            movement[2] += 1

    player.move(movement)
    player.update()
    screen.fill((0,0,0))
    player.draw(screen)
    pygame.display.update()
    clock.tick(60)

        
        
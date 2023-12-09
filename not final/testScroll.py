import pygame
import sys
from map.map import Map
from serviceLocator import ServiceLocator

pygame.init()

# Set up display
screen_width, screen_height = 800, 800
map_width, map_height = 1200, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Scrolling Map Example")

# Load background image
background_image = pygame.image.load("dummy.png")  # Replace "background.jpg" with your image file
background_rect = background_image.get_rect()

# Set up player
player_width, player_height = 50, 50
player_color = (255, 0, 0)
player_x, player_y = screen_width // 2, screen_height // 2

# Set up camera
camera = pygame.Rect(0, 0, screen_width, screen_height)

clock = pygame.time.Clock()
serviceLocator = ServiceLocator()

map = Map("1",serviceLocator)
mapCanvas = pygame.Surface((map_width,map_height))

while True:
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    player_speed = 5

    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < map_width - player_width:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < map_height - player_height:
        player_y += player_speed

    # Update the camera's position based on the player's position
    camera.x = player_x - screen_width // 2
    camera.y = player_y - screen_height // 2

    # Ensure the camera stays within the bounds of the map
    camera.x = max(0, min(camera.x, map_width - screen_width))
    camera.y = max(0, min(camera.y, map_height - screen_height))

    # Draw the background image
    screen.blit(background_image, (0 - camera.x, 0 - camera.y))
    map.draw(mapCanvas)
    screen.blit(mapCanvas,(0 - camera.x, 0 - camera.y))

    # Draw the portion of the map based on the camera's position
    pygame.draw.rect(screen, player_color, (player_x - camera.x, player_y - camera.y, player_width, player_height))

    pygame.display.flip()
    clock.tick(60)
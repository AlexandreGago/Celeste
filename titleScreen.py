
import pygame


def drawTitleScreen(display,display_shake,clock,particlemanager):
    width = display.get_width()
    height = display.get_height()

    pygame.font.init()
    #background image
    bgImage = pygame.image.load("atlas.png")
    bgImage = bgImage.subsurface((72,32,55,31))
    bgImage = pygame.transform.scale(bgImage, (width-50, height/2))
    #"press start" text
    text_font = pygame.font.Font('freesansbold.ttf', 32 )
    text_text = text_font.render("Press Space to Start", True, "white")
    text_rect = text_text.get_rect()
    text_rect.center = (width/2,height/7*5)
    #wait for player to press space
    running = True
    animationFrameCounter = 0
    time = 0

    while running:
        display.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False

        #update and draw particles
        particlemanager.update(time)
        particlemanager.draw("cloud", display)
        particlemanager.draw("snow", display)

        # show image
        display.blit(bgImage,(25,height/4))
        display_shake.blit(display, (0,0))
        
        if animationFrameCounter % 120  <60:
            # show text
            display.blit(text_text,text_rect)
            display_shake.blit(display, (0,0))
        



        display_shake.blit(display, (0,0))
        pygame.display.flip()
        animationFrameCounter += 1
        time += clock.tick(60)
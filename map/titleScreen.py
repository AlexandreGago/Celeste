
import pygame

def drawTitleScreen(display:pygame.display,display_shake:pygame.display,clock:pygame.time.Clock,particlemanager) -> None:
    """
    Draw the Title Screen and holds it until a space key is pressed

    Args:   
        display (pygame.display): display where objects are drawn
        display_shake (pygame.display): display where "display" is drawn with an offset to simulate screen shake
        clock (pygame.time.Clock): clock to keep track of time
        particlemanager (ParticleManager): manager to keep track of particles
    
    Returns:
        None
    """
    width = display.get_width() # get the width of the display
    height = display.get_height() # get the height of the display

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
        
        #update display
        display_shake.blit(display, (0,0))
        pygame.display.flip()

        #
        animationFrameCounter += 1
        time += clock.tick(60)
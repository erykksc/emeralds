import pygame

pygame.init()

resolution = (800, 800)

dispSurf = pygame.display.set_mode(resolution)

#mode 0 - graphical chooser
#mode 1 - 
mode = 0


clock.tick(FPS)
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
        quit()

import pygame
import time
import sys
pygame.init()

displaySurface = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Learning pygame")

# # gemSurf= pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Gem.png")
# gemSurf = gemSurf.convert()
# gemSurf.set_alpha(0)

# xPos=0
# yPos=0

ts=time.time()

clock = pygame.time.Clock()

myfont=pygame.font.SysFont("Comic Sans MS", 40)
textSurface = myfont.render("1", True, (255,255,255),(0,0,0,0))
height = textSurface.get_height()


alpha=255
change = -1

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    displaySurface.fill((0,0,0))
    #
    # xPos+=20
    # if xPos>280:
    #     xPos=0
    #     yPos+=20
    # if yPos>280:
    #     yPos=0

    # pygame.draw.rect(displaySurface, (0,255,0), (xPos, yPos, 20, 20))
    # for x in range(5):
    displaySurface.blit(textSurface, (0,0))

    # if alpha==0:
    #     change=1
    # if alpha==255:
    #     change=-1
    # textSurface.set_alpha(alpha)
    # alpha+=change
    pygame.display.update()

import pygame
import time
import sys
pygame.init()

displaySurface = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Learning pygame")

ts=time.time()

clock = pygame.time.Clock()

def getOnlyLetters(text, maxHeight):
    tStart = time.time()
    size = maxHeight
    myfont=pygame.font.SysFont("Comic Sans MS", size)

    while myfont.get_ascent() > maxHeight:
        size -= myfont.get_ascent() - maxHeight
        myfont=pygame.font.SysFont("Comic Sans MS", size)
    textSurf = myfont.render(text, True, (0,255,0), (0,0,255))
    rSurface = pygame.Surface((myfont.size(text)[0], myfont.get_ascent()))
    rSurface.blit(textSurf, (0,0))
    tStop = time.time()
    print("Time needed for calculation:", tStop-tStart)
    return rSurface


while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    displaySurface.fill((0,0,0))
    numSurf = getOnlyLetters("1", round(600*0.75))
    roundSurf = getOnlyLetters("round", round(600*0.15))


    displaySurface.blit(numSurf, (0, 0))
    displaySurface.blit(roundSurf, (0, numSurf.get_height()))


    pygame.display.update()

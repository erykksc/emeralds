import pygame
import time
pygame.init()

displaySurface = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Learning pygame")

xPos=0
yPos=0

ts=time.time()

clock = pygame.time.Clock()

clock.tick(2)

pygame.draw.rect(displaySurface, (0,255,0), (xPos, yPos, 20, 20))

pygame.display.update()
time.sleep(10)
#
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#     displaySurface.fill((0,0,0))
#
#     if time.time()-ts>=1:
#         ts=time.time()
#         xPos+=20
#         if xPos>280:
#             xPos=0
#             yPos+=20
#
#     pygame.draw.rect(displaySurface, (0,255,0), (xPos, yPos, 20, 20))
#
#     pygame.display.update()

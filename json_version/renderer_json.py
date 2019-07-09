import pygame
import time
from math import floor
import random
import json_loader

class Renderer():
    def __init__(self, mode=0, displayRes=(800, 600)): # mode: 0-load settings from arguments, mode 1 - load from file
        self.displayRes = displayRes
        self.currentState=0
        pygame.init()
        self.dispSurf = pygame.display.set_mode(self.displayRes)
        self.tiles={
            "Gem":pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Gem.png"),
            "Trap":pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Trap.png"),
            "Relict_Full":pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Relict_Full.png"),
            "Relict_Empty":pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Relict_Empty.png"),
            "Jungle":pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Jungle.png"),
            "Base":pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Base.png")
        }
        self.resetTileMap()

    def isGameReady(self):
        return not json_loader.readValue("ready2Continue")

    def isGameWaiting4Answers(self):
        return json_loader.readValue("waiting4Answers")

    #should be later deleted
    def setWaiting4AnswersFalse(self):
        json_loader.updatePair("waiting4Answers", False)

    def setGameState2Ready(self):
        json_loader.updatePair("ready2Continue", True)

    def update(self):
        pygame.display.update()

    def setCurrentState(self):
        self.currentState = json_loader.readValue("state")

    def performGameState(self):

        #If gameState is decisions
        if self.currentState==0:
            dispTileMap=[["Trap" for _ in range(8)] for _ in range(6)]
            self.dispTileMap(dispTileMap)
        #if gameState is goingBack
        elif self.currentState==1:
            self.dispTileMap(self.tileMap)
        #if gameState is reveal
        elif self.currentState==2:
            try:
                lastTile = json_loader.readValue("tilePath")[-1]

                #should be changed when real graphics will come
                if lastTile["type"]=="gem":
                    self.dispTileMap([["Gem"]])
                elif lastTile["type"]=="relict":
                    self.dispTileMap([["Relict_Full"]])
                elif lastTile["type"]=="trap":
                    self.dispTileMap([["Trap"]])

                self.updateTilePath()
            except:
                print("No Path")

        #if gameState is relict or trap
        elif self.currentState==3:
            self.dispTileMap(self.tileMap)
        # if gameState is gem splitting
        elif self.currentState==4:
            self.dispTileMap(self.tileMap)
        #if gameState is a kill
        elif self.currentState==5:
            self.resetTileMap()
            self.dispTileMap(self.tileMap)

    def updateTilePath(self):
        tilePath = json_loader.readValue("tilePath")

        BASE_WIDTH=2

        posX = 0
        posY = 0
        for tile in tilePath:
            if posY+BASE_WIDTH>len(self.tileMap[0])-1:
                posX+=1
                posY=0
            #change for real graphics
            name=""
            if tile["type"]=="gem":
                name="Gem"
            elif tile["type"]=="relict":
                if tile["containsRelict"]:
                    name="Relict_Full"
                else:
                    name = "Relict_Empty"
            elif tile["type"]=="trap":
                name="Trap"
            self.tileMap[posX][posY+BASE_WIDTH] = name
            posY+=1

    def dispTileMap(self, tileMap):
        #displays a tile map from an 2d array Arr of string names of the tiles
        #tileSize=floor(self.displayRes[0]/self.tilesPerRow) #OG version
        lenX = len(tileMap[0]) #length of tiles array that are going to be displayed horizontally
        lenY = len(tileMap) #length of tiles array that are going to be displayed vertically
        if (lenY >= lenX) or (lenX/lenY<(self.displayRes[0]/self.displayRes[1])): # check if tile map has more tiles in y
            tileSize=floor(self.displayRes[1]/len(tileMap))
        else:
            tileSize=floor(self.displayRes[0]/len(tileMap[0]))

        #calculates the starting position at x and y coordinates
        xGap = self.displayRes[0] - tileSize*len(tileMap[0])
        yGap = self.displayRes[1] - tileSize*len(tileMap)

        # print("tileSize: " + str(tileSize))
        # print("xGap: " + str(xGap))
        # print("yGap: " + str(yGap))

        #refreshes dispSurf
        self.dispSurf.fill((0,0,0))
        xPos = xGap/2
        yPos = yGap/2
        for x in range(len(tileMap)):
            for y in range(len(tileMap[x])):
                tileToPlace = pygame.transform.scale(self.tiles[tileMap[x][y]], (tileSize, tileSize))
                self.dispSurf.blit(tileToPlace , (xPos, yPos))
                xPos+=tileSize
            yPos += tileSize
            xPos = xGap/2
        pygame.display.update()

    def resetTileMap(self):
        self.tileMap = [["Base", "Base", "Jungle", "Jungle", "Jungle", "Jungle", "Jungle", "Jungle"] for _ in range(6) ]

    def render(self):
        while(True):
            if self.isGameReady:
                self.setGameState2Ready()
                self.setCurrentState()
                time.sleep(2)
            if self.isGameWaiting4Answers():
                self.setWaiting4AnswersFalse()
            self.performGameState()
            time.sleep(0.1)

if __name__=="__main__":
    renderer = Renderer(displayRes=(800, 600))
    renderer.render()
    # while True:
    #     #tileMap = [[random.choice(["Gem", "Relict_Full", "Relict_Empty", "Trap", "Jungle", "Base"]) for _ in range(1)] for _ in range(1) ]
    #     tileMap=[["Base", "Base", "Jungle", "Jungle", "Jungle", "Jungle", "Jungle", "Jungle"] for _ in range(6) ]
    #     renderer.dispTileMap(tileMap)
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             quit()
    #     time.sleep(0.1)

realTileMap=[["Base", "Base", "Jungle", "Jungle", "Jungle", "Jungle", "Jungle", "Jungle"] for _ in range(6) ]

# dispSurf.blit(tile, (xPos, yPos))
#
# pygame.display.update()
# infoObj = pygame.display.Info()
# input(infoObj.current_h)

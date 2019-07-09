import pygame
import time
from math import floor
import random
import threading

baseTilesNamesGlobal = [["Base", "Base"], ["Base", "Base"], ["Base", "Base"], ["Base", "Base"], ["Base", "Base"]]
widthWholeMapGlobal = 6
heightWholeMapGlobal = 5


class Renderer():
    def __init__(self, mode=0, resolution=(800, 600), fullscreen=False, fontStyle="Comic Sans MS", fontSize=30, fontColor = (255,255,255)): # mode: 0-load settings from arguments, mode 1 - load from file
        self.currentState=0
        pygame.init()
        self.clock = pygame.time.Clock()
        if fullscreen:
            self.displaySurface = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
        else:
            self.displaySurface = pygame.display.set_mode(resolution)
        self.myFont = pygame.font.SysFont(fontStyle, fontSize)
        self.myFontColor = fontColor
        self.playerNicknamesSurfaces=[]
        self.rules= "Rules:\nRule 1\nRule 2\nRule 3"
        self.renderingArr = [False, False, False, False] #indexes 0- askPlayersToJoin, 1-showRules, 2-waitForDecisions, 3-showEndOfGameScreen
        self.textures={
            "gem":pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Gem.png"),
            "trap":pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Trap.png"),
            "relict_Full":pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Relict_Full.png"),
            "relict_Empty":pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Relict_Empty.png"),
            "jungle":pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Jungle.png"),
            "base":pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Base.png"),

            "menu_placeholder":pygame.image.load("D:\GIT\Emeralds\Graphics\menu_placeholder.png"),
        }
        self.resetTileMap()

    def checkIfPygameExit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def getTileTexture(self, tile):
        #temporary
        name= tile.getName()
        if name[:3]=="gem":
            name="gem"
        elif name[:6]=="relict":
            if name[-4:]=="Full":
                name="relict_Full"
            else:
                name="relict_Empty"
        elif name[:4]=="trap":
            name="trap"
        return self.textures[name]

        #final version should be:
        #return self.textures[tile.getName()]

    def menu(self):
        placeholder = self.myFont,render("Press left mouse button to continue")
        self.displaySurface.fill(0,0,0)
        self.displaySurface.blit(placeholder, (0,0))
        self.update()

    def getSurfacesFromString(self, text):
        surfaces=[]
        for line in text.split("\n"):
            surfaces.append(self.myFont.render(line, True, (self.myFontColor)))

        return surfaces

    def startAskPlayersToJoin(self):
        self.updatePlayersJoined([])
        wBannerSurface = self.myFont.render("Waiting for Players", True, (255,255,255))
        askPlayersToJoinThread = threading.Thread(name="AskPlayersToJoinThread", target=self.askPlayersToJoin, args=(wBannerSurface,))
        self.renderingArr[0]=True
        askPlayersToJoinThread.start()

    def askPlayersToJoin(self, waitingBanner):
        wBannerPosX = self.calculateCenterX(waitingBanner)

        wBannerHeight = waitingBanner.get_height()

        while self.renderingArr[0]:
            self.clock.tick(60)
            self.checkIfPygameExit()
            self.update()
            self.displaySurface.fill((0,0,0))
            self.displaySurface.blit(waitingBanner, (wBannerPosX,0))
            for surfaceIndex in range(len(self.playerNicknamesSurfaces)):
                self.displaySurface.blit(self.playerNicknamesSurfaces[surfaceIndex], (0, surfaceIndex*self.myFont.get_height() + wBannerHeight))

    def stopAskPlayersToJoin(self):
        self.renderingArr[0]=False

    def updatePlayersJoined(self, playerNicknames):

        surfaces=[]
        for nickname in playerNicknames:
            surfaces.append(self.myFont.render(nickname, True, (self.myFontColor)))

        self.playerNicknamesSurfaces = surfaces

    def startShowingRules(self):
        self.renderingArr[1]=True
        showRulesThread = threading.Thread(name="showRulesThread", target=self.showRules)
        showRulesThread.start()

    def showRules(self):
        while self.renderingArr[1]:
            self.clock.tick(60)
            self.checkIfPygameExit()
            self.update()
            self.displaySurface.fill((0,0,0))
            rulesSurfaces = self.getSurfacesFromString(self.rules)

            #display banner Rules:
            bannerHeight = rulesSurfaces[0].get_height()
            self.displaySurface.blit(rulesSurfaces[0], (self.calculateCenterX(rulesSurfaces.pop(0)), 0))

            for surfaceIndex in range(len(rulesSurfaces)):
                self.displaySurface.blit(rulesSurfaces[surfaceIndex], (0,bannerHeight + (surfaceIndex)*self.myFont.get_height()))

    def stopShowingRules(self):
        self.renderingArr[1]=False

    def showRoundNum(self, roundNum):
        numFont = pygame.font.SysFont("Comic Sans MS", 300)
        bannerFont = pygame.font.SysFont("Comic Sans MS", 100)

        roundNum = numFont.render(str(roundNum), True, (255,255,255), (0,0,0,0))
        banner = bannerFont.render("round", True, (255,255,255), (0,0,0,0))

        alpha=0
        while(alpha<255):
            self.clock.tick(60)
            self.checkIfPygameExit()
            self.displaySurface.fill((0,0,0))
            self.displaySurface.blit(roundNum, (self.calculateCenterX(roundNum),0))
            self.displaySurface.blit(banner, (self.calculateCenterX(banner),roundNum.get_height()))
            alpha+=1
            roundNum.set_alpha(alpha)
            banner.set_alpha(alpha)
            self.update()

    def showGoingBack(self, tilePath, currentPlayers, pastPlayers):
        global baseTilesNamesGlobal
        global widthWholeMapGlobal
        global heightWholeMapGlobal
        tilePathRenderReady = getTilePathRenderReady(tilePath, baseTilesNamesGlobal, widthWholeMapGlobal, heightWholeMapGlobal)
        tileMapSurface = getTileMapSurface(tilePathRenderReady, (self.displaySurface.get_width() ,self.displaySurface.get_height() - self.myFont.get_height()))

        while i<190:
            self.displaySurface.fill((0,0,0))
            self.displaySurface.blit(tilePathSurface, (0, self.myFont.get_height()))
            self.update()

    def showRevealedTile(self, revealedTile):
        #temporary
        #background=pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Gem.png"
        background = pygame.Surface((10,10))
        background.fill((0,0,255,255))
        BACKGROUND_DISAPPEARING_SPEED = 10

        background=pygame.transform.scale(background, (self.displaySurface.get_size()))
        alpha=255
        while(alpha>0):
            background.set_alpha(alpha)

            self.clock.tick(60)
            self.checkIfPygameExit()
            self.displaySurface.fill((0,0,0))
            self.displaySurface.blit(background, (0,0))
            self.update()

            alpha-=BACKGROUND_DISAPPEARING_SPEED

    def update(self):
        pygame.display.update()

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

    def convertTilePathToNames(self, tilePath):
        #here it is possible to change which pngs are being used
        tilePathNames = []
        for tile in tilePath:
            #change for real graphics
            name=""
            if tile.getType()=="gem":
                name = "gem_" + str(tile.getGemsLeft())
            elif tile.getType()=="relict":
                name = tile.getName()
            elif tile.getType()=="trap":
                name = tile.getName()
            tilePathNames.append(name)
        return tilePathNames

    def convertTilePathNamesTo2dMap(self, tilePathNames, baseTilesNames, widthWholeMap, heightWholeMap):
        tilePathIndex=0
        row = 0
        column = 0
        columnChange = 1 #direction where the column goes
        map2d=[[None for _ in range(widthWholeMap)] for _ in range(heightWholeMap)]

        while row < heightWholeMap:
            if (row < len(baseTilesNames)) and (column<len(baseTilesNames[row])):
                map2d[row][column] = baseTilesNames[row][column]
            elif tilePathIndex < len(tilePathNames):
                map2d[row][column] = tilePathNames[tilePathIndex]
                tilePathIndex+=1
            else:
                map2d[row][column] = "jungle"


            column+=columnChange

            if column>widthWholeMap-1:
                row+=1
                columnChange = -columnChange
                column += columnChange

            if column<0:
                row+=1
                columnChange = -columnChange
                column += columnChange

        return map2d

    def getTilePathRenderReady(self, tilePath, baseTilesNames, widthWholeMap=6, heightWholeMap=5):
        tilePathNames = self.convertTilePathToNames(tilePath)
        return self.convertTilePathNamesTo2dMap(tilePathNames, baseTilesNames, widthWholeMap, heightWholeMap)

    def getTileMapSurface(self, tileMap, resolution = None, background="fill_black"):
        #returns a tile map surface from an 2d array Arr of string names of the tiles

        if not resolution:
            resolution = (self.displaySurface.get_width() ,self.displaySurface.get_height())

        #tileSize=floor(self.displayRes[0]/self.tilesPerRow) #OG version
        lenX = len(tileMap[0]) #length of tiles array that are going to be displayed horizontally
        lenY = len(tileMap) #length of tiles array that are going to be displayed vertically
        if (lenY >= lenX) or (lenX/lenY<(resolution[0]/resolution[1])): #check if tile map has more tiles in y
            tileSize=floor(resolution[1]/len(tileMap))
        else:
            tileSize=floor(resolution[0]/len(tileMap[0]))

        #calculates the starting position at x and y coordinates
        xGap = resolution[0] - tileSize*len(tileMap[0])
        yGap = resolution[1] - tileSize*len(tileMap)

        tileMapSurface = pygame.Surface((resolution))

        if background=="fill_black":
            tileMapSurface.fill((0,0,0))
        else:
            resizedBackground = pygame.transform.scale(background, (resolution))
            tileMapSurface.blit(resizedBackground, (0,0))

        xPos = xGap/2
        yPos = yGap/2
        for x in range(len(tileMap)):
            for y in range(len(tileMap[x])):
                tileToPlace = pygame.transform.scale(self.tiles[tileMap[x][y]], (tileSize, tileSize))
                tileMapSurface.blit(tileToPlace , (xPos, yPos))
                xPos += tileSize
            yPos += tileSize
            xPos = xGap/2

        return tileMapSurface

    def calculateCenterX(self, surface):
        return floor((self.displaySurface.get_width()-surface.get_width())/2)


if __name__=="__main__":
    renderer = Renderer(displayRes=(800, 600))
    renderer.showRoundNum(1)
    #renderer.updatePlayersJoined(["Nickname0", "Nickname1", "Nickname2", "Nickname3", "Nickname4"])
    #renderer.stopAskPlayersToJoin()

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



# infoObj = pygame.display.Info()

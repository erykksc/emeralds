import pygame
import time
import math
import random
import threading

import game_Module
from pprint import pprint
from ctypes import windll
windll.user32.SetProcessDPIAware()


BASE_TILES_NAMES_GLOBAL = [["base", "base"] for _ in range(6)]
WIDTH_WHOLE_MAP_GLOBAL = 8
HEIGHT_WHOLE_MAP_GLOBAL = 6
RULES_GLOBAL = "Rules:\nRule 1\nRule 2\nRule 3"
FPS=60
NUM_OF_PLAYER_SKINS = 8


class Renderer():
    def __init__(self, mode=0, resolution=(800, 600), fullscreen=False, fontStyle="Comic Sans MS", fontSize=30, fontColor = (255,255,255)): # mode: 0-load settings from arguments, mode 1 - load from file
        global BASE_TILES_NAMES_GLOBAL
        global WIDTH_WHOLE_MAP_GLOBAL
        global HEIGHT_WHOLE_MAP_GLOBAL
        global RULES_GLOBAL

        self.widthWholeMap = WIDTH_WHOLE_MAP_GLOBAL
        self.heightWholeMap = HEIGHT_WHOLE_MAP_GLOBAL
        self.baseTilesNames = BASE_TILES_NAMES_GLOBAL
        self.tilePath=[]
        self.rules = RULES_GLOBAL
        self.tileMap=[]
        self.playersInfo={
            "playerCount":0,
            "availablePlayerColors":self.playerSurfacesGen(),
            "nicknames":[],
            "players":{
            # "nickname1":{
            #     "playerNicknameSurface": nickname surface made with a font module
            #     "playerSurface": playerSurface taken from playerSurfaces,
            #     "unsecuredGems":0,
            #     "inCamp":True,
            #     "explores":False
            # }
            }
        }

        pygame.init()
        self.clock = pygame.time.Clock()

        if fullscreen:
            self.displaySurface = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
        else:
            self.displaySurface = pygame.display.set_mode(resolution)

        self.myFont = pygame.font.SysFont(fontStyle, fontSize)
        self.fontStyle = fontStyle
        self.myFontColor = fontColor


        self.renderingArr = [False, False, False, False] #indexes 0- askPlayersToJoin, 1-showRules, 2-waitForDecisions, 3-showEndOfGameScreen
        self.textures={
            "gem":pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Gem.png").convert(),
            "trap":pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Trap.png").convert(),
            "relict_Full":pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Relict_Full.png").convert(),
            "relict_Empty":pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Relict_Empty.png").convert(),
            "jungle":pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Jungle.png").convert(),
            "base":pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Base.png").convert(),

            "menu_placeholder":pygame.image.load("D:\GIT\Emeralds\Graphics\menu_placeholder.png").convert(),
        }
        self.positions_config={
            1:[
            [0,0,0],
            [0,1,0],
            [0,0,0]
            ],
            2:[
            [1,0,0],
            [0,0,0],
            [0,0,1]
            ],
            3:[
            [1,0,0],
            [0,1,0],
            [0,0,1]
            ],
            4:[
            [1,0,1],
            [0,0,0],
            [1,0,1]
            ],
            5:[
            [1,0,1],
            [0,1,0],
            [1,0,1]
            ],
            6:[
            [1,0,1],
            [1,0,1],
            [1,0,1]
            ],
            7:[
            [1,0,1],
            [1,1,1],
            [1,0,1]
            ],
            8:[
            [1,1,1],
            [1,0,1],
            [1,1,1]
            ],
            9:[
            [1,1,1],
            [1,1,1],
            [1,1,1]
            ]
        }

    def playerSurfacesGen(self):
        global NUM_OF_PLAYER_SKINS
        #temporary
        surf = pygame.Surface((100,100))

        surf.fill((255,0,0))
        yield(surf.copy())
        surf.fill((255,128,0))
        yield(surf.copy())
        surf.fill((255,255,0))
        yield(surf.copy())
        surf.fill((0,255,0))
        yield(surf.copy())
        surf.fill((0,255,255))
        yield(surf.copy())
        surf.fill((0,0,255))
        yield(surf.copy())
        surf.fill((127,0,255))
        yield(surf.copy())
        surf.fill((255,51,255))
        yield(surf.copy())
        surf.fill((255,255,254))
        yield(surf.copy())
        #final
        # for i in range(1, NUM_OF_PLAYER_SKINS+1):
        #     yield(pygame.image.load("D:\GIT\Emeralds\Graphics\Player_Skin_" + str(i) ".png"))
        #close()

    def checkIfPygameExit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def getTileTexture(self, tileName):
        #final version should be:
        #return self.textures[tileName]
        #temporary
        if tileName[:3]=="gem":
            tileName="gem"
        elif tileName[:6]=="relict":
            if tileName[-4:]=="Full":
                tileName="relict_Full"
            else:
                tileName="relict_Empty"
        elif tileName[:4]=="trap":
            tileName="trap"
        return self.textures[tileName]

    def updateTileMap(self, tilePath):
        self.tilePath = tilePath
        self.tileMap=self.getTileMapFromTilePath(tilePath)

    # def menu(self):
    #     placeholder = self.myFont,render("Press left mouse button to continue")
    #     self.displaySurface.fill(0,0,0)
    #     self.displaySurface.blit(placeholder, (0,0))
    #     self.update()

    def getFontSurfacesFromString(self, text):
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
            self.displaySurface.fill((0,0,0))
            self.displaySurface.blit(waitingBanner, (wBannerPosX,0))

            index = 0
            for nickname in self.playersInfo["players"]:
                nicknameSurface = self.playersInfo["players"][nickname]["playerNicknameSurface"]
                self.displaySurface.blit(nicknameSurface, (0, index*self.myFont.get_height() + wBannerHeight))
                index+=1

            self.clock.tick(FPS)
            self.checkIfPygameExit()
            self.update()

    def stopAskPlayersToJoin(self):
        self.renderingArr[0]=False

    def updatePlayersJoined(self, playerNicknames):
        #temporary have to add a way to limit adding players

        self.playersInfo["nicknames"]=playerNicknames
        self.playersInfo["playerCount"]= len(playerNicknames)

        for nickname in playerNicknames:
            if nickname not in self.playersInfo["players"]:
                self.playersInfo["players"][nickname]={}
                self.playersInfo["players"][nickname]["unsecuredGems"]=0
                self.playersInfo["players"][nickname]["inCamp"] = True
                self.playersInfo["players"][nickname]["explores"] = False
                self.playersInfo["players"][nickname]["decides"] = False
                self.playersInfo["players"][nickname]["playerNicknameSurface"] = self.myFont.render(nickname, True, (self.myFontColor))
                self.playersInfo["players"][nickname]["playerSurface"]=next(self.playersInfo["availablePlayerColors"])

    def startShowingRules(self):
        self.renderingArr[1]=True
        showRulesThread = threading.Thread(name="showRulesThread", target=self.showRules)
        showRulesThread.start()

    def showRules(self):
        while self.renderingArr[1]:
            self.clock.tick(FPS)
            self.checkIfPygameExit()
            self.update()
            self.displaySurface.fill((0,0,0))
            rulesSurfaces = self.getFontSurfacesFromString(self.rules)

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

        animationTime=3
        alpha=0
        timeS=time.time()
        self.clock.tick()
        while(alpha<255):
            roundNum.set_alpha(alpha)
            banner.set_alpha(alpha)
            self.displaySurface.fill((0,0,0))
            self.displaySurface.blit(roundNum, (self.calculateCenterX(roundNum),0))
            self.displaySurface.blit(banner, (self.calculateCenterX(banner),roundNum.get_height()))

            self.checkIfPygameExit()
            self.update()

            framerate=1000/self.clock.tick(FPS)
            alphaChange=round(255/(animationTime*framerate))
            alpha+=alphaChange
        print("Animation time", time.time() - timeS)
        print("framerate:",framerate)

    def startWaitingForDecisions(self, nicknamesThatMakeDecisions):
        self.renderingArr[2]=True
        for nickname in self.playersInfo["players"]:
            if nickname not in nicknamesThatMakeDecisions:
                self.playersInfo["players"][nickname]["decides"]=False
            else:
                self.playersInfo["players"][nickname]["decides"]=True

        waitingForDecisionsThread = threading.Thread(name="waitForDecisionsThread", target=self.waitForDecisions)
        waitingForDecisionsThread.start()

    def waitForDecisions(self):
        while self.renderingArr[2]:
            #temporary should add graphics
            self.displaySurface.fill((0,0,0))

            nicknamesDeciding=["Waiting for decisions of:"]
            for nickname in self.playersInfo["players"]:
                if self.playersInfo["players"][nickname]["decides"]:
                    nicknamesDeciding.append(nickname)

            nicknamesSurfaces = self.getFontSurfacesFromString("\n".join(nicknamesDeciding))

            y=0
            for surf in nicknamesSurfaces:
                self.displaySurface.blit(surf,(self.calculateCenterX(surf), y))
                y+=surf.get_height()
            self.clock.tick(FPS)
            self.checkIfPygameExit()
            self.update()

    def updateDecisions(self, decisionsDict):
        #decisionsDict should be dictionary with "playersNickname":decision pairs
        for nickname in decisionsDict:
            self.playersInfo["players"][nickname]["explores"] = decisionsDict[nickname]
            self.playersInfo["players"][nickname]["decides"] = False

    def stopWaitingForDecisions(self):
        self.renderingArr[2]=False

    # def showGoingBack(self, tilePath, currentPlayers, pastPlayers):
    #     global BASE_TILES_NAMES_GLOBAL
    #     global WIDTH_WHOLE_MAP_GLOBAL
    #     global HEIGHT_WHOLE_MAP_GLOBAL
    #     tilePathRenderReady = getTilePathRenderReady(tilePath, BASE_TILES_NAMES_GLOBAL, WIDTH_WHOLE_MAP_GLOBAL, HEIGHT_WHOLE_MAP_GLOBAL)
    #     tileMapSurface = getTileMapSurface(tilePathRenderReady, (self.displaySurface.get_width() ,self.displaySurface.get_height() - self.myFont.get_height()))
    #
    #     while i<190:
    #         self.displaySurface.fill((0,0,0))
    #         self.displaySurface.blit(tilePathSurface, (0, self.myFont.get_height()))
    #         self.update()

    def showRevealedTile(self, revealedTile):
        #temporary, the whole module should be based on times rather than fps
        #temporary, final should be:
        #background=pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Gem.png"
        caveSurf = pygame.Surface((10,10))
        caveSurf.fill((255,255,0,255))

        tileMapBackground = pygame.Surface((10,10))
        tileMapBackground.fill((0,0,0,255))
        tileMapBackground = pygame.transform.scale(tileMapBackground, (self.displaySurface.get_size()))

        caveSurf=pygame.transform.scale(caveSurf, (self.displaySurface.get_size()))

        tileMapResolution = (self.displaySurface.get_width(), self.displaySurface.get_height()-self.myFont.get_height())
        tileMapSurf = self.getTileMapSurface(self.tileMap, resolution = tileMapResolution)
        playersSurf = self.getPlayersSurface(tileMapResolution)

        revealedTileSurf = self.getTileTexture(revealedTile)
        currentSize = 1

        maxTileSize = int(self.displaySurface.get_height()*0.8)
        currentTileSurf = pygame.transform.scale(revealedTileSurf, (currentSize, currentSize))

        animationTime=2
        self.displaySurface.fill((0,0,0))
        self.displaySurface.blit(caveSurf, (0, 0))
        self.clock.tick()
        tStart=time.time()
        #scales up the tile
        while(currentSize<maxTileSize):

            currentTileSurf = pygame.transform.scale(revealedTileSurf, (currentSize, currentSize))
            self.displaySurface.blit(currentTileSurf, self.calculateCenter(currentTileSurf))

            self.checkIfPygameExit()
            self.update()

            framerate = 1000/self.clock.tick(FPS)
            TILE_SCALING_SPEED = round((maxTileSize-1)/(animationTime*framerate))

            if currentSize+TILE_SCALING_SPEED>maxTileSize:
                TILE_SCALING_SPEED = maxTileSize-currentSize

            currentSize += TILE_SCALING_SPEED

        print("Scaling Time:", time.time()-tStart)
        print("Framerate:", framerate)
        # whitespaceSize = self.myFont.size(" ")
        # widthOfNicknames = len(self.playerNicknames)-1
        # for surface in self.playersNicknamesSurfaces:
        #     widthOfNicknames += surface.get_width()

        #displays the image for 1.5 seconds
        pygame.time.wait(1000)

        alpha=255
        self.clock.tick()
        tStart = time.time()
        animationTime=2
        #dissapeares the background and the tile
        disapearingSurf = pygame.Surface(self.displaySurface.get_size())
        disapearingSurf.blit(caveSurf, (0,0))
        disapearingSurf.blit(currentTileSurf, self.calculateCenter(currentTileSurf))

        while(alpha>0):
            disapearingSurf.set_alpha(alpha)
            self.displaySurface.blit(tileMapBackground, (0,0))
            self.displaySurface.blit(tileMapSurf, (0, self.myFont.get_height()))
            self.displaySurface.blit(playersSurf, (0, self.myFont.get_height()))

            #blit player nicknames
            self.displaySurface.blit(disapearingSurf, (0,0))

            self.checkIfPygameExit()
            self.update()
            framerate= 1000/self.clock.tick(FPS)
            DISAPPEARING_SPEED = round(255/(animationTime * framerate))
            alpha-= DISAPPEARING_SPEED
        print("Disappearing time:", time.time()-tStart)
        print("Framerate:", framerate)

    def update(self):
        pygame.display.update()

    def getTileMapFromTilePath(self, tilePath):
        tilePathIndex=0
        row = 0
        column = 0
        columnChange = 1 #direction where the column goes
        map2d=[[None for _ in range(self.widthWholeMap)] for _ in range(self.heightWholeMap)]

        while row < self.heightWholeMap:
            if (row < len(self.baseTilesNames)) and (column<len(self.baseTilesNames[row])):
                map2d[row][column] = self.baseTilesNames[row][column]
            elif tilePathIndex < len(tilePath):
                map2d[row][column] = tilePath[tilePathIndex]
                tilePathIndex+=1
            else:
                map2d[row][column] = "jungle"

            column+=columnChange

            if column>self.widthWholeMap-1:
                row+=1
                columnChange = -columnChange
                column += columnChange

            if column<0:
                row+=1
                columnChange = -columnChange
                column += columnChange

        return map2d

    def getTileMapSurface(self, tileMap, resolution = "AUTO", background="fill_black"):
        #returns a tile map surface from an 2d array Arr of string names of the tiles

        if resolution=="AUTO":
            resolution = self.displaySurface.get_size()

        #tileSize=math.floor(self.displayRes[0]/self.tilesPerRow) #OG version
        if (self.heightWholeMap >= self.widthWholeMap) or (self.widthWholeMap/self.heightWholeMap<(resolution[0]/resolution[1])): #check if tile map has more tiles in y
            tileSize=math.floor(resolution[1]/self.heightWholeMap)
        else:
            tileSize=math.floor(resolution[0]/self.widthWholeMap)
        #calculates the starting position at x and y coordinates
        xGap = (resolution[0] - tileSize*self.widthWholeMap)/2
        yGap = (resolution[1] - tileSize*self.heightWholeMap)/2

        tileMapSurface = pygame.Surface((resolution))

        if background=="fill_black":
            tileMapSurface.fill((0,0,0))
        else:
            resizedBackground = pygame.transform.scale(background, (resolution))
            tileMapSurface.blit(resizedBackground, (0,0))

        xPos = xGap
        yPos = yGap
        tileToPlace = pygame.Surface((tileSize, tileSize))
        for x in range(self.heightWholeMap):
            for y in range(len(tileMap[x])):
                tileTexture = self.getTileTexture(tileMap[x][y])
                tileToPlace = pygame.transform.scale(tileTexture, (tileSize, tileSize))
                tileMapSurface.blit(tileToPlace , (xPos, yPos))
                xPos += tileSize
            yPos += tileSize
            xPos = xGap

        return tileMapSurface

    def getPlayersSurface(self, resolution):
        surf = pygame.Surface(resolution)
        surf.fill((255,255,255))
        surf.set_colorkey((255, 255, 255))

        baseTileCords = (0,2)

        playersInBase=[]
        playersExploring=[]

        for nickname in self.playersInfo["players"]:
            if self.playersInfo["players"][nickname]["inCamp"]:
                playersInBase.append(nickname)
            else:
                playersExploring.append(nickname)


        if (self.heightWholeMap >= self.widthWholeMap) or (self.widthWholeMap/self.heightWholeMap<(resolution[0]/resolution[1])): #check if tile map has more tiles in y
            tileSize=math.floor(resolution[1]/self.heightWholeMap)
        else:
            tileSize=math.floor(resolution[0]/self.widthWholeMap)

        playersInBaseSurf = self.getPlayersTileSurf(tileSize, playersInBase)
        playersExploringSurf = self.getPlayersTileSurf(tileSize, playersExploring)

        #calculates the starting position at x and y coordinates
        xGap = (resolution[0] - tileSize*self.widthWholeMap)/2
        yGap = (resolution[1] - tileSize*self.heightWholeMap)/2

        tilePathIndex=0
        row = 0
        column = 0
        columnChange = 1 #direction where the column goes

        xPos=xGap
        yPos=yGap

        while row < self.heightWholeMap:
            if (row,column)==baseTileCords:
                surf.blit(playersInBaseSurf, (xPos, yPos))

            if column >= len(self.baseTilesNames[0]):
                if tilePathIndex==len(self.tilePath)-1:
                    surf.blit(playersExploringSurf, (xPos, yPos))
                tilePathIndex+=1


            column += columnChange
            xPos += tileSize*columnChange

            if column>self.widthWholeMap-1:
                row+=1
                columnChange = -columnChange
                column += columnChange
                yPos+=tileSize
                xPos += tileSize*columnChange

            if column<0:
                row+=1
                columnChange = -columnChange
                column += columnChange
                yPos+=tileSize
                xPos += tileSize*columnChange

        return surf

    def getPlayersTileSurf(self, tileSize, nicknames):
        surf = pygame.Surface((tileSize,tileSize))
        surf.fill((255,255,255))
        surf.set_colorkey((255,255,255))
        if len(nicknames):
            config = self.positions_config[len(nicknames)]

            nicknamesIndex = 0
            row=0
            multiPl = [0.25, 0.5, 0.75]


            while row<3:
                column=0
                while column<3:

                    if config[row][column]:
                        playerSurf = self.playersInfo["players"][nicknames[nicknamesIndex]]["playerSurface"]
                        playerSurf = pygame.transform.scale(playerSurf, (round(tileSize/5), round(tileSize/5)))
                        nicknamesIndex += 1
                        surf.blit(playerSurf, (tileSize*multiPl[row]-math.floor(playerSurf.get_width()/2), tileSize*multiPl[column]-math.floor(playerSurf.get_height()/2)))
                    column += 1
                row+=1
            return surf
        else:
            return surf

    def calculateCenterX(self, surface):
        return math.floor((self.displaySurface.get_width()-surface.get_width())/2)

    def calculateCenter(self, surface):
        return (math.floor((self.displaySurface.get_width()-surface.get_width())/2), math.floor((self.displaySurface.get_height()-surface.get_height())/2))



if __name__=="__main__":
    resolution=(1000, 700)
    renderer=Renderer(resolution=resolution, fullscreen=False)


    renderer.updatePlayersJoined([str(i) for i in range(8)])

    deck = game_Module.Deck()
    tilePathNames = [deck.pickCard().getName() for _ in range(8)]
    renderer.updateTileMap(tilePathNames)

    # test of waiting players to join
    # renderer.startAskPlayersToJoin()
    # pygame.time.wait(1000)
    # renderer.updatePlayersJoined(["Nickname0", "Nickname1", "Nickname2", "Nickname3", "Nickname4"])
    # pygame.time.wait(1000)
    # renderer.stopAskPlayersToJoin()

    # for i in range(1,6):
    #     renderer.showRoundNum(i)
    # renderer.showRoundNum(1)

    # renderer.startWaitingForDecisions(["Nickname0", "Nickname1", "Nickname2"])
    # pygame.time.wait(1000)
    # renderer.updateDecisions({"Nickname0":True})
    # pygame.time.wait(2000)
    # renderer.updateDecisions({"Nickname1":True, "Nickname2": False})
    # pygame.time.wait(10)
    # renderer.stopWaitingForDecisions()

    # test of showRevealedTile
    # for i in range(5):
    #     renderer.playersInfo["players"][str(i)]["inCamp"]=True
    #
    # players=[]
    # z=0
    # while 1 :
    #     players.append(str(z))
    #     z+=1
    #     renderer.clock.tick(2)
    #     surf = pygame.Surface((500,500))
    #     surf.fill((128,128,0))
    #     surf.blit(renderer.getPlayersTileSurf(500, players), (0,0))
    #     renderer.displaySurface.blit(surf, (0,0))
    #     renderer.checkIfPygameExit()
    #     renderer.update()

    renderer.showRevealedTile(tilePathNames[-1])




# infoObj = pygame.display.Info()

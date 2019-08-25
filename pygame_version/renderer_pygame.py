import pygame
import time
import math
import random
import threading
import os
import sys
import pickle
import json
# import game_Module

from ctypes import windll
windll.user32.SetProcessDPIAware()


BASE_TILES_NAMES_GLOBAL = [["base", "base"] for _ in range(2)]
WIDTH_WHOLE_MAP_GLOBAL = 8
HEIGHT_WHOLE_MAP_GLOBAL = 6
rulesPath = os.path.join(os.path.abspath(""), "assets", "texts", "rules.txt")

RULES_GLOBAL = ""
with open(rulesPath, "r") as f:
    RULES_GLOBAL = f.read()
FPS = 60
NUM_OF_PLAYER_SKINS = 8


class Renderer():
    def __init__(self, resolution=(800, 600), graphics="default", fullscreen=False, fontStyle="Comic Sans MS", fontColor=(255, 255, 255), port=0):
        self.port = port

        global BASE_TILES_NAMES_GLOBAL
        global WIDTH_WHOLE_MAP_GLOBAL
        global HEIGHT_WHOLE_MAP_GLOBAL
        global RULES_GLOBAL

        self.graphics = graphics


        self.fontStyle = fontStyle
        self.myFontColor = fontColor

        self.widthWholeMap = WIDTH_WHOLE_MAP_GLOBAL
        self.heightWholeMap = HEIGHT_WHOLE_MAP_GLOBAL
        self.baseTilesNames = BASE_TILES_NAMES_GLOBAL
        self.tilePath = []
        self.rules = RULES_GLOBAL
        self.tileMap = []
        self.playersInfo = {
            "playerCount": 0,
            "availablePlayerColors": self.playerSurfacesGen(),
            "nicknames": [],
            "players": {
                # "nickname1":{
                # "playerNicknameSurface": nickname surface made with a font module
                # "playerSurface": playerSurface taken from playerSurfaces,
                # "unsecuredGems":0,
                # "inCamp":True,
                # "explores":False
                # }
            }
        }

        pygame.init()
        self.clock = pygame.time.Clock()
        
        if fullscreen:
            self.displaySurface = pygame.display.set_mode(
                resolution, pygame.FULLSCREEN)
        else:
            self.displaySurface = pygame.display.set_mode(resolution)

        pygame.display.set_caption("Emeralds")


        #fullscreen, num_of_rounds are just placeholders, the real values will be loaded from json file
        self.settings = {
            "resolutions" : pygame.display.list_modes(),
            "resolution" : self.displaySurface.get_size(),
            "resolutionStr" : str(self.displaySurface.get_width())+"×"+str(self.displaySurface.get_height()),
            "fullscreen" : fullscreen,
            "num_of_rounds" : 0,
            "max_round_num" : 10,
            "texture_packs" : ["default", "pola"],
            "texture_pack" : graphics
        }

        basedir = os.path.abspath("")
        # self.renderingArr = [False, False, False, False] #indexes 0- askPlayersToJoin, 1-showRules, 2-waitForDecisions, 3-showEndOfGameScreen
        if self.graphics == "default":
            self.textures = {
                "gem": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Tile_Gem.png")).convert(),
                "relict_full": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Tile_Relict_Full.png")).convert(),
                "relict_empty": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Tile_Relict_Empty.png")).convert(),
                "jungle": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Tile_Jungle.png")).convert(),
                "base": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Tile_Base.png")).convert(),
                "trap": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Tile_Trap.png")).convert()
            }
        elif self.graphics == "pola":
            self.textures = {
                "gem": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Tiles", "Tile_Gem.png")).convert(),
                "relict_full": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Tiles", "Tile_Relict_Full.png")).convert(),
                "relict_empty": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Tiles", "Tile_Relict_Empty.png")).convert(),
                "jungle": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Tiles", "Tile_Jungle.png")).convert(),
                "base": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Tiles", "Tile_Base.png")).convert(),
                "trap_default": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Tiles", "Tile_Trap.png")).convert(),
                "trap_lava": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Tiles", "Tile_Trap_Lava.png")).convert(),
                "trap_spiders": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Tiles", "Tile_Trap_Spider.png")).convert(),
                "trap_snakes": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Tiles", "Tile_Trap_Snakes.png")).convert(),
                "trap_wreckingball": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Tiles", "Tile_Trap_Wreckingball.png")).convert(),
                "trap_tiger": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Tiles", "Tile_Trap_Tiger.png")).convert(),


                "background_cave": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Backgrounds", "Background_Cave.png")).convert(),
                "background_welcome": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Backgrounds", "Background_Welcome.png")).convert(),
                "background_decisions": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Backgrounds", "Background_Decisions.png")).convert(),
                "background_menu": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Backgrounds", "Background_Menu.png")).convert(),
                "background_credits": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Backgrounds", "Background_Credits.png")).convert(),


                "player_1": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Players", "Player_1.png")).convert_alpha(),
                "player_2": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Players", "Player_2.png")).convert_alpha(),
                "player_3": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Players", "Player_3.png")).convert_alpha(),
                "player_4": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Players", "Player_4.png")).convert_alpha(),
                "player_5": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Players", "Player_5.png")).convert_alpha(),
                "player_6": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Players", "Player_6.png")).convert_alpha(),
                "player_7": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Players", "Player_7.png")).convert_alpha(),
                "player_8": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Players", "Player_8.png")).convert_alpha(),
                "player_9": pygame.image.load(os.path.join(basedir, "assets", "graphics", graphics, "Players", "Player_9.png")).convert_alpha(),

                # "menu_placeholder":pygame.image.load("D:\GIT\Emeralds\Graphics\menu_placeholder.png").convert(),
            }

        self.positions_config = {
            1: [
                [0, 0, 0],
                [0, 1, 0],
                [0, 0, 0]
            ],
            2: [
                [1, 0, 0],
                [0, 0, 0],
                [0, 0, 1]
            ],
            3: [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
            ],
            4: [
                [1, 0, 1],
                [0, 0, 0],
                [1, 0, 1]
            ],
            5: [
                [1, 0, 1],
                [0, 1, 0],
                [1, 0, 1]
            ],
            6: [
                [1, 0, 1],
                [1, 0, 1],
                [1, 0, 1]
            ],
            7: [
                [1, 0, 1],
                [1, 1, 1],
                [1, 0, 1]
            ],
            8: [
                [1, 1, 1],
                [1, 0, 1],
                [1, 1, 1]
            ],
            9: [
                [1, 1, 1],
                [1, 1, 1],
                [1, 1, 1]
            ]
        }

        self.loadCache()

    def loadCache(self):
        basedir = os.path.abspath("")

        try:
            with open(os.path.join(basedir, "cache.cache"), "rb") as f:
                cache = pickle.load(f)
        except FileNotFoundError:
            cache = {
                "cachedSize": {}
            }

        self._cachedSize = cache["cachedSize"]
        self._cachedGameStats = {}
        self._cachedPlayersInfo = {"nicknames": []}
        self._cachedLastRenderedFunction = ""
        self._cachedLastTexture = ["", 0]

    def saveCache(self):
        basedir = os.path.abspath("")

        try:
            with open(os.path.join(basedir, "cache.cache"), "rb") as f:
                cache = pickle.load(f)
        except FileNotFoundError:
            with open(os.path.join(basedir, "cache.cache"), "wb") as f:
                cacheDict = {
                    "cachedSize": {}
                }
                cache = cacheDict

        cache["cachedSize"].update(self._cachedSize)

        with open(os.path.join(basedir, "cache.cache"), "wb") as f:
            pickle.dump(cache, f)

    def clearCache(self):
        self._cachedSize = {}
        self._cachedGameStats = {}
        self._cachedPlayersInfo = {"nicknames": []}
        self._cachedLastRenderedFunction = ""
        self._cachedLastTexture = ["", 0]

    def saveSettings(self):
        BASE_DIR = os.path.abspath("")
        with open(os.path.join(BASE_DIR, "launch_settings.json"), "w") as f:
            settingsDict = {
                "resolution": self.settings["resolution"],
                "fullscreen" : self.settings["fullscreen"],
                "num_of_rounds" : self.settings["num_of_rounds"],
                "texture_pack" : self.settings["texture_pack"],
                "port" : self.port
            }
            json.dump(settingsDict, f, indent=4)

    def playerSurfacesGen(self):
        global NUM_OF_PLAYER_SKINS

        if self.graphics == "default":
            surf = pygame.Surface((100, 100))

            surf.fill((255, 0, 0))
            yield surf.copy()
            surf.fill((255, 128, 0))
            yield surf.copy()
            surf.fill((255, 255, 0))
            yield surf.copy()
            surf.fill((0, 255, 0))
            yield surf.copy()
            surf.fill((0, 255, 255))
            yield surf.copy()
            surf.fill((0, 0, 255))
            yield surf.copy()
            surf.fill((127, 0, 255))
            yield surf.copy()
            surf.fill((255, 51, 255))
            yield surf.copy()
            surf.fill((255, 255, 254))
            yield surf.copy()

        elif self.graphics == "pola":
            surf = pygame.Surface((100, 100))

            playerNum = 1
            while playerNum < 10:
                yield self.getTexture("player_" + str(playerNum))
                playerNum += 1

            # surf.fill((255, 128, 0))
            # yield surf.copy()
            # surf.fill((255, 255, 0))
            # yield surf.copy()
            # surf.fill((0, 255, 0))
            # yield surf.copy()
            # surf.fill((0, 255, 255))
            # yield surf.copy()
            # surf.fill((0, 0, 255))
            # yield surf.copy()
        # final
        # for i in range(1, NUM_OF_PLAYER_SKINS+1):
        #     yield(pygame.image.load("D:\GIT\Emeralds\Graphics\Player_Skin_" + str(i) ".png"))
        # close()

    def checkIfPygameExit(self):
        #checks for quit event  
        for event in pygame.event.get(): #eventtype=(pygame.QUIT
            if event.type == pygame.QUIT:
                self.onExit()
        #checks for alt + f4
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LALT] or keys[pygame.K_RALT]) and keys[pygame.K_F4]:
            self.onExit()
        
        
    def onExit(self):
        self.saveCache()
        pygame.quit()
        sys.exit()

    def getTexture(self, tileName):
        # final version should be:
        # return self.textures[tileName]

        if tileName == self._cachedLastTexture[0] and self._cachedLastRenderedFunction != "applySettings":
            return self._cachedLastTexture[1]
        else:
            self._cachedLastTexture[0] = tileName

        if self.graphics == "default":

            # temporary
            if tileName[:3] == "gem":
                textureName = "gem"
                gemsLeft, gemsMax = tileName[4:].split("/")

                # temporary
                text = gemsLeft

            elif tileName[:4] == "trap":
                textureName = "trap"
                trapName = tileName[5:]

                # trap
                text = trapName

            elif tileName[:6] == "relict":
                value = tileName.split("_")[1]

                if tileName[-4:] == "full":
                    textureName = "relict_full"
                    # temporarry
                    text = value
                else:
                    textureName = "relict_empty"
                    text = ""

            elif tileName[:10] == "background":
                if tileName[11:] == "cave":
                    caveSurf = pygame.Surface((10, 10))
                    caveSurf.fill((255, 255, 0, 255))
                    self._cachedLastTexture[1] = caveSurf
                    return caveSurf.copy()
                elif tileName[11:] == "decisions":
                    decisionSurf = pygame.Surface((10, 10))
                    decisionSurf.fill((0, 0, 0))
                    self._cachedLastTexture[1] = decisionSurf
                    return decisionSurf.copy()
                elif tileName[11:] == "welcome":
                    welcomeSurf = pygame.Surface((10, 10))
                    welcomeSurf.fill((0, 0, 0))
                    self._cachedLastTexture[1] = welcomeSurf
                    return welcomeSurf.copy()
                elif tileName[11:] == "menu":
                    menuSurf = pygame.Surface((10, 10))
                    menuSurf.fill((0, 0, 0))
                    self._cachedLastTexture[1] = menuSurf
                    return menuSurf.copy()
                elif tileName[11:] == "credits":
                    creditsSurf = pygame.Surface((10, 10))
                    creditsSurf.fill((0, 0, 0))
                    self._cachedLastTexture[1] = creditsSurf
                    return creditsSurf.copy()

            else:
                textureName = tileName
                text = ""

            tileTexture = self.textures[textureName].copy()
            tileTexture = pygame.transform.scale(tileTexture, (400, 400))
            tileRect = tileTexture.get_rect()
            textSurf = self.getFontSurfacesFromString(text, maxTextSize=(
                tileTexture.get_width()/2, tileTexture.get_height()/2))[0]
            textRect = textSurf.get_rect()
            textRect.center = tileRect.center

            tileTexture.blit(textSurf, textRect)
            self._cachedLastTexture[1] = tileTexture
            return tileTexture

        elif self.graphics == "pola":
            # temporary
            if tileName[:3] == "gem":
                textureName = "gem"
                gemsLeft, gemsMax = tileName[4:].split("/")

                # temporary
                text = gemsLeft

            elif tileName[:6] == "relict":
                value = tileName.split("_")[1]

                if tileName[-4:] == "full":
                    textureName = "relict_full"
                    # temporarry
                    text = value
                else:
                    textureName = "relict_empty"
                    text = ""

            elif tileName[:4] == "trap":
                textureName = tileName
                text = ""
                # trapName = tileName[5:]
                # textureName = "trap_" + trapName
                # text = ""
                # if trapName in ("lava", "spiders", "snakes", "wreckingball"):
                #     textureName = "trap_" + trapName
                #     text = ""
                # else:
                #     textureName = "trap_default"
                #     text = trapName

            else:
                textureName = tileName
                text = ""

            tileTexture = self.textures[textureName].copy()
            tileTexture = pygame.transform.scale(tileTexture, (400, 400))
            if text != "":
                tileRect = tileTexture.get_rect()
                textSurf = self.getFontSurfacesFromString(text, maxTextSize=(
                    tileTexture.get_width()/2, tileTexture.get_height()/2))[0]
                textRect = textSurf.get_rect()
                textRect.center = tileRect.center

                tileTexture.blit(textSurf, textRect)
            self._cachedLastTexture[1] = tileTexture
            return tileTexture

    def getFontSurfacesFromString(self, text, fontSize=None, fontStyle=None, fontColor=None, backgroundColor=None, maxTextSize=None, antialias=True):
        # tStart = time.time()
        if not fontStyle:
            fontStyle = self.fontStyle
        if not fontColor:
            fontColor = self.myFontColor

        if maxTextSize:
            maxTextSize = (int(maxTextSize[0]), int(maxTextSize[1]))
            longestText = max(text.split("\n"), key=len)
            if (maxTextSize, longestText) in self._cachedSize:
                cacheHit = True
                size = self._cachedSize[(maxTextSize, longestText)]
            else:
                cacheHit = False
                size = max(maxTextSize)
            font = pygame.font.SysFont(fontStyle, size)
            #same thing as in the loop
            longestTextSize = font.size(longestText)
            differenceWidth = longestTextSize[0] - maxTextSize[0]
            differenceHeight = longestTextSize[1] - maxTextSize[1]

            while (differenceWidth > 0) or (differenceHeight > 0):
                if differenceWidth > 9000 or  differenceHeight > 9000:
                    size -= 100
                elif differenceWidth > 1100 or  differenceHeight > 1100:
                    size -= 20
                elif differenceHeight > 20:
                    size -= 10
                elif differenceHeight > 10:
                    size -= 2
                else:
                    size -= 1
                
                if size < 1:
                    raise Exception("Too much text, no font could be found")
                    break

                differenceWidth = longestTextSize[0] - maxTextSize[0]
                differenceHeight = longestTextSize[1] - maxTextSize[1]
                font = pygame.font.SysFont(fontStyle, size)
                longestTextSize = font.size(longestText)
                # print("size:", size, ",", longestTextSize)
                # print("difference in width:", differenceWidth, "difference in height:", differenceHeight)
                
            # print("found fontSize:", size)
            fontSize = size
            if not cacheHit:
                self._cachedSize[(maxTextSize, longestText)] = size

        if fontSize == None and maxTextSize == None:
            raise Exception("No fontSize nor maxTextHeight given as arguments")

        font = pygame.font.SysFont(fontStyle, fontSize)
        surfaces = []
        for line in text.split("\n"):
            surfaces.append(font.render(
                line, antialias, fontColor, backgroundColor))
        # tStop = time.time()
        # print("found in:", tStop - tStart)
        return surfaces

    def renderPlayersJoined(self, ipAdress, port):

        if (self.playersInfo["nicknames"] == self._cachedPlayersInfo["nicknames"]) and (self._cachedLastRenderedFunction == "renderPlayersJoined"):
            framerate = 1000/self.clock.tick(FPS)
            self.checkIfPygameExit()
        else:
            caveSurf = self.getTexture("background_welcome")
            caveSurf = pygame.transform.scale(
                caveSurf, (self.displaySurface.get_size()))
            self.displaySurface.blit(caveSurf, (0, 0))

            maxTextSize = (self.displaySurface.get_width() * 0.9,
                           self.displaySurface.get_height() * 0.1)
            waitingBanner = self.getFontSurfacesFromString(
                f"Go to http://{ipAdress}:{port} to join.", maxTextSize=maxTextSize)[0]
            wBannerPosX = self.calculateCenterX(waitingBanner)

            wBannerHeight = waitingBanner.get_height()

            self.displaySurface.blit(waitingBanner, (wBannerPosX, 0))

            index = 0
            for nickname in self.playersInfo["players"]:
                nicknameSurface = self.getFontSurfacesFromString(
                    str(nickname), maxTextSize=maxTextSize)[0]
                self.displaySurface.blit(nicknameSurface, (self.calculateCenterX(
                    nicknameSurface), index*nicknameSurface.get_height() + wBannerHeight))
                index += 1

            self._cachedPlayersInfo["nicknames"] = self.playersInfo["nicknames"]
            self._cachedLastRenderedFunction = "renderPlayersJoined"

            framerate = 1000/self.clock.tick(FPS)
            self.checkIfPygameExit()
            self.update()
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            return "go_back"
        else:
            return ""

    def updatePlayersJoined(self, playerNicknames):
        # temporary have to add a way to limit adding players

        self.playersInfo["nicknames"] = playerNicknames
        self.playersInfo["playerCount"] = len(playerNicknames)

        for nickname in playerNicknames:
            if nickname not in self.playersInfo["players"]:
                self.playersInfo["players"][nickname] = {}
                self.playersInfo["players"][nickname]["unsecuredGems"] = 0
                self.playersInfo["players"][nickname]["inCamp"] = True
                self.playersInfo["players"][nickname]["explores"] = False
                self.playersInfo["players"][nickname]["decides"] = True
                self.playersInfo["players"][nickname]["playerSurface"] = next(
                    self.playersInfo["availablePlayerColors"])

        toDel = set()
        for key in self.playersInfo["players"]:
            if key not in playerNicknames:
                toDel.add(key)
        for nick in toDel:
            del self.playersInfo["players"][nick]

    def renderRules(self):
        if self._cachedLastRenderedFunction != "renderRules":
            self._cachedLastRenderedFunction != "renderRules"
            self.displaySurface.fill((0, 0, 0))

            # display banner Rules:
            bannerMaxSize = (self.displaySurface.get_width(),
                            self.displaySurface.get_height()*0.15)
            bannerSurf = self.getFontSurfacesFromString(
                "Rules:", maxTextSize=bannerMaxSize)[0]
            bannerHeight = bannerSurf.get_height()
            self.displaySurface.blit(
                bannerSurf, (self.calculateCenterX(bannerSurf), 0))

            maxRulesTextSize = (self.displaySurface.get_width(),
                (self.displaySurface.get_height() - bannerHeight)/len(self.rules.split("\n")))#/len(self.rules.split("\n")) )
            # print("max rules size:", maxRulesTextSize)
            # print("rules length", len(self.rules.split("\n")))
            rulesSurfaces = self.getFontSurfacesFromString(
                self.rules, maxTextSize=maxRulesTextSize)
            ruleSurfHeight = rulesSurfaces[0].get_height()

            for surfaceIndex in range(len(rulesSurfaces)):
                self.displaySurface.blit(
                    rulesSurfaces[surfaceIndex], (0, bannerHeight + surfaceIndex*ruleSurfHeight))

        self.clock.tick(FPS)
        self.checkIfPygameExit()
        self.update()

    def showRoundNum(self, roundNum):

        roundNum = self.getFontSurfacesFromString(str(roundNum), maxTextSize=(
            self.displaySurface.get_width(), self.displaySurface.get_height()*0.75))[0]
        banner = self.getFontSurfacesFromString("round", maxTextSize=(
            self.displaySurface.get_width(), self.displaySurface.get_height()*0.15))[0]

        animationTime = 3
        alpha = 0
        timeS = time.time()
        self.clock.tick()
        while(alpha < 255):
            roundNum.set_alpha(alpha)
            banner.set_alpha(alpha)
            self.displaySurface.fill((0, 0, 0))
            self.displaySurface.blit(
                roundNum, (self.calculateCenterX(roundNum), 0))
            self.displaySurface.blit(
                banner, (self.calculateCenterX(banner), roundNum.get_height()))

            self.checkIfPygameExit()
            self.update()

            framerate = 1000/self.clock.tick(FPS)
            alphaChange = round(255/(animationTime*framerate))
            alpha += alphaChange

        print("Showing round num")
        print("Animation time", time.time() - timeS)
        print("Framerate:", framerate)

    def renderWaitingForDecisions(self, playersThatDecide, decisionsDict):
        # decisionsDict should be dictionary with "playersNickname":decision pairs
        # temporary should add graphics
        self._cachedLastRenderedFunction = "renderWaitingForDecisions"
        backgroundSurf = self.getTexture("background_decisions")
        backgroundSurf = pygame.transform.scale(
            backgroundSurf, self.displaySurface.get_size())
        self.displaySurface.blit(backgroundSurf, (0, 0))

        nicknamesDeciding = ["Waiting for decisions of:"]
        for nickname in playersThatDecide:
            if nickname not in decisionsDict:
                nicknamesDeciding.append(nickname)
        maxTextSize = (self.displaySurface.get_width()*0.8,
                       self.displaySurface.get_height()/len(nicknamesDeciding))
        nicknamesSurfaces = self.getFontSurfacesFromString(
            "\n".join(nicknamesDeciding), maxTextSize=maxTextSize)

        y = 0
        for surf in nicknamesSurfaces:
            self.displaySurface.blit(surf, (self.calculateCenterX(surf), y))
            y += surf.get_height()

        self.clock.tick(FPS)
        self.checkIfPygameExit()
        self.update()

    def renderMenu(self):
        displaySize = self.displaySurface.get_size()
        returnString = ""

        backgroundSurf = self.getTexture("background_menu")
        backgroundSurf = pygame.transform.scale(
            backgroundSurf, displaySize)
        if self._cachedLastRenderedFunction != "renderMenu":
            self.displaySurface.blit(backgroundSurf, (0, 0))

            emeraldsTextSurf = self.getFontSurfacesFromString(
                "Emeralds", fontColor=(235, 81, 61), maxTextSize=(displaySize[0]*0.6, displaySize[1]*0.2))[0]
            emeraldsTextRect = emeraldsTextSurf.get_rect()
            emeraldsTextRect.center = (displaySize[0]/2, displaySize[1]*0.1)
            self.displaySurface.blit(emeraldsTextSurf, emeraldsTextRect)


        menuTexts = ["Play", "Settings", "Credits", "Quit"]
        #indexes have to be the same as the menuTexts
        longestText = max(menuTexts, key=len)
        menuString = "\n".join(menuTexts)
        menuTextSurfs = self.getFontSurfacesFromString(
            menuString, maxTextSize=(displaySize[0]*0.25, displaySize[1]*0.15))

        menuTextRects = []
        index = 0
        for surf in menuTextSurfs:
            rect = surf.get_rect()
            rect.center = (displaySize[0]/2, displaySize[1]
                           * 0.15*index + displaySize[1]*0.35)
            menuTextRects.append(rect)

            self.displaySurface.blit(surf, rect)
            index += 1

        mousePos = pygame.mouse.get_pos()
        for i in range(len(menuTextRects)):
            if menuTextRects[i].collidepoint(mousePos):
                newSurf = self.getFontSurfacesFromString(menuTexts[i] + "\n" + longestText, maxTextSize=(
                    displaySize[0]*0.25, displaySize[1]*0.15), fontColor=(212, 219, 66))[0]
                #blits the background
                self.displaySurface.blit(backgroundSurf, menuTextRects[i], menuTextRects[i])
                self.displaySurface.blit(newSurf, menuTextRects[i])
                break
        
        for event in pygame.event.get(eventtype=pygame.MOUSEBUTTONUP):
            if event.type == pygame.MOUSEBUTTONUP:
                clickPos = pygame.mouse.get_pos()
        
                for i in range(len(menuTextRects)):
                    if menuTextRects[i].collidepoint(clickPos):
                        returnString = menuTexts[i]

        if self._cachedLastRenderedFunction != "renderMenu":
            self._cachedLastRenderedFunction = "renderMenu"
            pygame.display.update()
        else:
            pygame.display.update(menuTextRects)

        self.checkIfPygameExit()
        framerate = 1000/self.clock.tick(FPS)
        # print(framerate)
        if returnString == "Quit":
            self.onExit()
        else:
            return returnString
        
    def renderPause(self):
        print("renderingPause")
        displaySize = self.displaySurface.get_size()
        # pauseSurface = pygame.Surface(displaySize)
        # pauseSurface.fill(255, 0, 255) #magenta color
        # pauseSurface.set_colorkey((255, 0, 255))
        
        pauseTextsSurfs = self.getFontSurfacesFromString("Resume\nMenu", maxTextSize=(displaySize[0]/3, displaySize[1]/10))
        resumeSurf = pauseTextsSurfs[0]
        resumeRect = resumeSurf.get_rect()
        resumeRect.center = (displaySize[0]/2, displaySize[1]/2 - resumeRect.height)

        menuSurf = pauseTextsSurfs[1]
        menuRect = resumeSurf.get_rect()
        menuRect.center = (displaySize[0]/2, displaySize[1]/2 + menuRect.height)

        pauseTextsRects = [resumeRect, menuRect]
        self.displaySurface.blit(resumeSurf, resumeRect)
        self.displaySurface.blit(menuSurf, menuRect)

        #checks if the mouse if over a rectangle
        mousePos = pygame.mouse.get_pos()
        for i in range(len(pauseTextsRects)):
            if pauseTextsRects[i].collidepoint(mousePos):
                newSurf = self.getFontSurfacesFromString(["Resume", "Menu"][i] + "\n" + "Resume",
                    maxTextSize=(displaySize[0]/3, displaySize[1]/10),
                    fontColor=(212, 219, 66))[0]
                #blits the background
                self.displaySurface.blit(newSurf, pauseTextsRects[i])
                break
        
        #checks if there was a click
        returnString = ""
        for event in pygame.event.get(eventtype=pygame.MOUSEBUTTONUP):
            if event.type == pygame.MOUSEBUTTONUP:
                clickPos = pygame.mouse.get_pos()
        
                for i in range(len(pauseTextsRects)):
                    if pauseTextsRects[i].collidepoint(clickPos):
                        returnString = ["Resume", "Menu"][i]
        
        self.update()

        self.checkIfPygameExit()
        self.clock.tick(FPS)

        return returnString
    
    def renderSettings(self):
        
        if self._cachedLastRenderedFunction != "renderSettings":
            with open(os.path.join(os.path.abspath(""), "launch_settings.json")) as f:
                settings = json.load(f)
            self.settings["num_of_rounds"] = settings["num_of_rounds"]
            
            
        displaySize = self.displaySurface.get_size()

        returnString = ""

        backgroundSurf = self.getTexture("background_menu")
        backgroundSurf = pygame.transform.scale(
            backgroundSurf, displaySize)
            
        if self._cachedLastRenderedFunction != "renderSettings":
            self.displaySurface.blit(backgroundSurf, (0, 0))

        settingsTexts = [
            "Resolution", self.settings["resolutionStr"],
            "Fullscreen", str(self.settings["fullscreen"]),
            "Number of rounds", str(self.settings["num_of_rounds"]),
            "Texture pack", self.settings["texture_pack"]
            ]

        settingsTexts.extend(["Go back", "Apply"])
        #indexes have to be the same as the settingsTexts
        longestText = max(settingsTexts, key=len)

        settingsString = "\n".join(settingsTexts)
        settingsTextSurfs = self.getFontSurfacesFromString(
            settingsString,
            maxTextSize=(displaySize[0]/3, displaySize[1]/((len(settingsTexts)+1)/2)),
            fontColor=(255, 255, 255)
            )

        settingsTextRects = []
        index = 0
        verticalPos = 0
        for surf in settingsTextSurfs:
                
            rect = surf.get_rect()

            if index % 2 == 0:
                rect.center = (displaySize[0]/3, 0)
                rect.top = displaySize[1]/((len(settingsTexts)+1)/2) * verticalPos + 50
            else:
                rect.center = (2*displaySize[0]/3, 0)
                rect.top = displaySize[1]/((len(settingsTexts)+1)/2) * verticalPos + 50        
                verticalPos += 1
            index += 1
            settingsTextRects.append(rect)

            backgroundUpdaterRect = rect.copy()
            backgroundUpdaterRect.width = displaySize[0]
            self.displaySurface.blit(backgroundSurf, backgroundUpdaterRect, backgroundUpdaterRect)
            self.displaySurface.blit(surf, rect)
            

        mousePos = pygame.mouse.get_pos()
        for i in range(len(settingsTextRects)):
            if i % 2 == 1 or i >= len(settingsTextRects) - 2:
                if settingsTextRects[i].collidepoint(mousePos):
                    newSurf = self.getFontSurfacesFromString(settingsTexts[i] + "\n" + longestText,
                        maxTextSize=(displaySize[0]/3, displaySize[1]/((len(settingsTexts)+1)/2)),
                        fontColor=(212, 219, 66))[0]
                    
                    #blits the background
                    # self.displaySurface.blit(backgroundSurf, settingsTextRects[i], settingsTextRects[i])
                    self.displaySurface.blit(newSurf, settingsTextRects[i])
                    break
        
        for event in pygame.event.get(eventtype=pygame.MOUSEBUTTONUP):
            if event.type == pygame.MOUSEBUTTONUP:
                clickPos = pygame.mouse.get_pos()
        
                for i in range(len(settingsTextRects)):
                    if i % 2 == 1 or i >= len(settingsTextRects) - 2:
                        if settingsTextRects[i].collidepoint(clickPos):
                            #go back
                            if i == len(settingsTextRects)-2:
                                returnString = "go_back"
                            #apply
                            elif i == len(settingsTextRects)-1:
                                self.saveSettings()
                                if self.settings["fullscreen"]:
                                    self.displaySurface = pygame.display.set_mode(self.settings["resolution"], pygame.FULLSCREEN)
                                else:
                                    self.displaySurface = pygame.display.set_mode(self.settings["resolution"])
                                self._cachedLastRenderedFunction = "apply"
                                returnString = "num_of_rounds " + str(self.settings["num_of_rounds"])
                                self.graphics = self.settings["texture_pack"]
                            #resolution
                            elif settingsTexts[i-1] == "Resolution":
                                index = self.settings["resolutions"].index(self.settings["resolution"])
                                if  index > 0:
                                    self.settings["resolution"] = self.settings["resolutions"][index - 1]
                                    self.settings["resolutionStr"] = str(self.settings["resolution"][0]) + "×" + str(self.settings["resolution"][1])

                                else:
                                    self.settings["resolution"] = self.settings["resolutions"][-1]
                                    self.settings["resolutionStr"] = str(self.settings["resolution"][0]) + "×" + str(self.settings["resolution"][1])
                            #texture pack
                            elif settingsTexts[i-1] == "Texture pack":
                                index = self.settings["texture_packs"].index(self.settings["texture_pack"])
                                if  index > 0:
                                    self.settings["texture_pack"] = self.settings["texture_packs"][index - 1]

                                else:
                                    self.settings["texture_pack"] = self.settings["texture_packs"][-1]

                            #fullscreen
                            elif settingsTexts[i-1] == "Fullscreen":
                                self.settings["fullscreen"] = not self.settings["fullscreen"]

                            #number of rounds
                            elif settingsTexts[i-1] == "Number of rounds":
                                if self.settings["num_of_rounds"] + 1 <= self.settings["max_round_num"]:
                                    self.settings["num_of_rounds"] += 1
                                else:
                                    self.settings["num_of_rounds"] = 1

        if self._cachedLastRenderedFunction != "renderSettings":
            if self._cachedLastRenderedFunction != "apply":
                self._cachedLastRenderedFunction = "renderSettings"
            else:
                self._cachedLastRenderedFunction = "applySettings"
            pygame.display.update()
        else:
            pygame.display.update()

            # pygame.display.update(menuTextRects)

        self.checkIfPygameExit()
        framerate = 1000/self.clock.tick(FPS)
        # print(framerate)
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            returnString = "go_back"
        if returnString == "Quit":
            self.onExit()
        else:
            return returnString
    
    def renderCredits(self):
        returnString = ""
        displaySize = self.displaySurface.get_size()

        creditsSurf = self.getTexture("background_credits")
        creditsSurf = pygame.transform.scale(creditsSurf, displaySize)
        if self._cachedLastRenderedFunction != "renderCredits":
            self._cachedLastRenderedFunction = "renderCredits"
            self.displaySurface.blit(creditsSurf, (0,0))

        quitButtonSurf = self.getFontSurfacesFromString("Go back", maxTextSize=(displaySize[0]/4, displaySize[1]/6))[0]
        quitButtonRect = quitButtonSurf.get_rect()
        quitButtonRect.center = (displaySize[0]/2, displaySize[1]*0.85)
        self.displaySurface.blit(quitButtonSurf, quitButtonRect)

        mousePos = pygame.mouse.get_pos()
        if quitButtonRect.collidepoint(mousePos):
            newSurf = self.getFontSurfacesFromString("Go back", maxTextSize=(
                displaySize[0]/4, displaySize[1]/6), fontColor=(212, 219, 66))[0]
            #blits the background
            self.displaySurface.blit(creditsSurf, quitButtonRect, quitButtonRect)
            self.displaySurface.blit(newSurf, quitButtonRect)
        
        for event in pygame.event.get(eventtype=pygame.MOUSEBUTTONUP):
            if event.type == pygame.MOUSEBUTTONUP:
                clickPos = pygame.mouse.get_pos()
        
                if quitButtonRect.collidepoint(clickPos):
                    returnString = "go_back"

        self.update()
        self.checkIfPygameExit()
        self.clock.tick(FPS)
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            returnString = "go_back"
        return returnString

    def renderGoingBack(self, tilePath, currentPlayers, pastPlayers):
        # temporary lacking animation

        # check which players returned to base
        # playersThatWentBack=[]
        # for playerPast, playerCurr in zip(pastPlayers, currentPlayers):
        #     if playerCurr["inCamp"] and  not playerPast["inCamp"]:
        #         playersThatWentBack.append(playerCurr["nickname"])
        self._cachedLastRenderedFunction = "renderGoingBack"

        tileMap = self.getTileMapFromTilePath(tilePath)
        tileMapResolution = (self.displaySurface.get_width(
        ), self.displaySurface.get_height())  # -self.myFont.get_height())
        tileMapRects = self.getTileMapRects(
            tileMapResolution, len(tileMap[0]), len(tileMap))
        tileMapSurf = self.getTileMapSurface(tileMap, tileMapResolution)

        # distinguishes who is where
        nicknamesInBase = []
        nicknamesExploring = []
        for player in pastPlayers:
            if player["inCamp"]:
                nicknamesInBase.append(player["nickname"])
            elif player["explores"]:
                nicknamesExploring.append(player["nickname"])
            else:
                nicknamesExploring.append(player["nickname"])

        if len(nicknamesInBase) > 0:
            playersBaseSurf = self.getPlayersTileSurf(
                tileMapRects[0][0].width, nicknamesInBase)
        else:
            playersBaseSurf = None

        if len(nicknamesExploring) > 0:
            playersExploringSurf = self.getPlayersTileSurf(
                tileMapRects[0][0].width, nicknamesExploring)
        else:
            playersExploringSurf = None

        if len(tilePath) > 0:
            newestTileX, newestTileY = self.getTileIndexes(
                0, tilePath, len(tileMap[0]), len(tileMap), 2, 2)

        self.displaySurface.fill((0, 0, 0))
        # self.myFont.get_height()))
        self.displaySurface.blit(tileMapSurf, (0, 0))
        if playersBaseSurf:
            # self.myFont.get_height()))
            self.displaySurface.blit(
                playersBaseSurf, tileMapRects[0][0].move(0, 0))
        if playersExploringSurf:
            self.displaySurface.blit(playersExploringSurf, tileMapRects[newestTileX][newestTileY].move(
                0, 0))  # self.myFont.get_height()))
        self.update()

        duration = 2  # in seconds
        tStart = time.time()
        while time.time() - tStart < duration:
            self.checkIfPygameExit()
            self.clock.tick(FPS)

        nicknamesInBase = []
        nicknamesExploring = []
        for player in currentPlayers:
            if player["inCamp"]:
                nicknamesInBase.append(player["nickname"])
            elif player["explores"]:
                nicknamesExploring.append(player["nickname"])

        if len(nicknamesInBase) > 0:
            playersBaseSurf = self.getPlayersTileSurf(
                tileMapRects[0][0].width, nicknamesInBase)
        else:
            playersBaseSurf = None

        if len(nicknamesExploring) > 0:
            playersExploringSurf = self.getPlayersTileSurf(
                tileMapRects[0][0].width, nicknamesExploring)
        else:
            playersExploringSurf = None

        if len(tilePath) > 0:
            newestTileX, newestTileY = self.getTileIndexes(
                0, tilePath, len(tileMap[0]), len(tileMap), 2, 2)

        self.displaySurface.fill((0, 0, 0))
        # self.myFont.get_height()))
        self.displaySurface.blit(tileMapSurf, (0, 0))
        if playersBaseSurf:
            # self.myFont.get_height()))
            self.displaySurface.blit(
                playersBaseSurf, tileMapRects[0][0].move(0, 0))
        if playersExploringSurf:
            self.displaySurface.blit(playersExploringSurf, tileMapRects[newestTileX][newestTileY].move(
                0, 0))  # self.myFont.get_height()))

        self.update()

        duration = 2
        tStart = time.time()
        while time.time() - tStart < duration:
            # to do, render pause
            # for event in pygame.event.get():
            #     print(event)
            #     if event.type == pygame.KEYUP:
            #         if event.key == pygame.K_ESCAPE:
            #             print("escape up")
            #             returnString = ""
            #             tPauseStart = time.time()
            #             while returnString == "":
            #                 returnString = self.renderPause()
            #             self.renderGoingBack(tilePath, currentPlayers, pastPlayers)
            #             if returnString == "Resume":
            #                 print("Return")
            #                 tPauseStop = time.time()
            #                 duration += tPauseStop - tPauseStart
            #             elif returnString == "Menu":
            #                 print("place holder go back")
            self.checkIfPygameExit()
                
            self.clock.tick(FPS)

    def showRevealedTile(self, tilePath, playersDicts):
        # temporary, final should be:
        # background=pygame.image.load("D:\GIT\Emeralds\Graphics\Tile_Gem.png"
        caveSurf = self.getTexture("background_cave")
        caveSurf = pygame.transform.scale(
            caveSurf, (self.displaySurface.get_size()))

        tileMapBackground = pygame.Surface((10, 10))
        tileMapBackground.fill((0, 0, 0, 255))
        tileMapBackground = pygame.transform.scale(
            tileMapBackground, (self.displaySurface.get_size()))

        revealedTileSurf = self.getTexture(tilePath[-1])
        currentSize = 1

        maxTileSize = int(self.displaySurface.get_height()*0.8)
        currentTileSurf = pygame.transform.scale(
            revealedTileSurf, (currentSize, currentSize))

        animationTime = 2
        self.displaySurface.fill((0, 0, 0))
        self.displaySurface.blit(caveSurf, (0, 0))
        self.clock.tick()
        tStart = time.time()
        # scales up the tile
        while(currentSize < maxTileSize):

            currentTileSurf = pygame.transform.scale(
                revealedTileSurf, (currentSize, currentSize))
            self.displaySurface.blit(
                currentTileSurf, self.calculateCenter(currentTileSurf))

            self.checkIfPygameExit()
            self.update()

            framerate = 1000/self.clock.tick(FPS)
            TILE_SCALING_SPEED = round(
                (maxTileSize-1)/(animationTime*framerate))

            if currentSize+TILE_SCALING_SPEED > maxTileSize:
                TILE_SCALING_SPEED = maxTileSize-currentSize

            currentSize += TILE_SCALING_SPEED

        print("Revealing tile")
        print("Scaling Time:", time.time()-tStart)
        print("Framerate:", framerate)
        # whitespaceSize = self.myFont.size(" ")
        # widthOfNicknames = len(self.playerNicknames)-1
        # for surface in self.playersNicknamesSurfaces:
        #     widthOfNicknames += surface.get_width()

        # displays the image for 1 seconds
        pygame.time.wait(1000)

        alpha = 255
        self.clock.tick()
        tStart = time.time()
        animationTime = 2
        # dissapeares the background and the tile
        disapearingSurf = pygame.Surface(self.displaySurface.get_size())
        disapearingSurf.blit(caveSurf, (0, 0))
        disapearingSurf.blit(
            currentTileSurf, self.calculateCenter(currentTileSurf))

        tileMapResolution = (self.displaySurface.get_width(
        ), self.displaySurface.get_height())  # -self.myFont.get_height())
        tileMap = self.getTileMapFromTilePath(tilePath)
        tileMapRects = self.getTileMapRects(
            tileMapResolution, len(tileMap[0]), len(tileMap))
        tileMapSurf = self.getTileMapSurface(
            tileMap, resolution=tileMapResolution)
        playersInBaseSurf = self.getPlayersInBaseTileSurf(
            tileMapRects[0][0].width, playersDicts)
        playersExploringSurf = self.getPlayersExploringTileSurf(
            tileMapRects[0][0].width, playersDicts)

        mapSurf = pygame.Surface(tileMapSurf.get_size())
        mapSurf.blit(tileMapSurf, (0, 0))
        mapSurf.blit(playersInBaseSurf, tileMapRects[0][0])
        xPos, yPos = self.getTileIndexes(
            0, tilePath, len(tileMap[0]), len(tileMap), 2, 2)
        mapSurf.blit(playersExploringSurf, tileMapRects[xPos][yPos])

        while(alpha > 0):
            disapearingSurf.set_alpha(alpha)
            self.displaySurface.blit(tileMapBackground, (0, 0))
            # self.myFont.get_height()))
            self.displaySurface.blit(mapSurf, (0, 0))

            # blit player nicknames
            self.displaySurface.blit(disapearingSurf, (0, 0))

            self.checkIfPygameExit()
            self.update()
            framerate = 1000/self.clock.tick(FPS)
            DISAPPEARING_SPEED = round(255/(animationTime * framerate))
            alpha -= DISAPPEARING_SPEED
        print("Revealing tile")
        print("Disappearing time:", time.time()-tStart)
        print("Framerate:", framerate)

    def update(self):
        pygame.display.update()

    def getPlayersInBaseTileSurf(self, tileSize, playersDicts):
        nicknamesInBase = []
        for player in playersDicts:
            if player["inCamp"]:
                nicknamesInBase.append(player["nickname"])

        if len(nicknamesInBase) > 0:
            return self.getPlayersTileSurf(tileSize, nicknamesInBase)
        else:
            surf = pygame.Surface((tileSize, tileSize))
            surf.fill((255, 255, 255))
            surf.set_colorkey((255, 255, 255))
            return surf

    def getPlayersExploringTileSurf(self, tileSize, playersDicts):
        nicknamesExploring = []
        for player in playersDicts:
            if not player["inCamp"]:
                if player["explores"]:
                    nicknamesExploring.append(player["nickname"])

        if len(nicknamesExploring) > 0:
            return self.getPlayersTileSurf(tileSize, nicknamesExploring)
        else:
            surf = pygame.Surface((tileSize, tileSize))
            surf.fill((255, 255, 255))
            surf.set_colorkey((255, 255, 255))
            return surf

    def getTileIndexes(self, indexFromEnd, tilePath, width, height, baseWidth, baseHeight):
        if len(tilePath) > 0:
            currIndex = 1
            lookingFor = len(tilePath) - indexFromEnd

            rowPos = 0
            colPos = 0
            lastColPos = 0
            change = 1
            for i in range(width*height):
                if (rowPos < baseHeight) and (colPos < baseWidth):
                    lastColPos = colPos
                    colPos += change
                    if colPos > (width-1) or colPos < 0:
                        change = -change
                        lastColPos = colPos
                        colPos += change
                        rowPos += 1
                    continue
                if (rowPos == baseHeight) and (change == 1) and (colPos < baseWidth):
                    colPos += 1
                    continue

                if currIndex == lookingFor:
                    return (rowPos, colPos)

                currIndex += 1
                lastColPos = colPos
                colPos += change
                if colPos > (width-1) or colPos < 0:
                    change = -change
                    lastColPos = colPos
                    colPos += change
                    rowPos += 1

            raise Exception("index not in tilemap")
        else:
            raise Exception("Tile path empty")

    # , resolution=self.displaySurface.get_size(), width=self.widthWholeMap, height=self.heightWholeMap):
    def getTileMapRects(self, resolution, width, height):
        # returns a 2d array of rectangles that can be used to create tile map surface

        # calculates the tile Size in order to fit the tile map into resolution
        # check if tile map has more tiles in y
        if (height >= width) or (width/height < (resolution[0]/resolution[1])):
            tileSize = math.floor(resolution[1]/height)
        else:
            tileSize = math.floor(resolution[0]/width)

        # calculates the starting position of x and y coordinates (calculates the gaps)
        xGap = (resolution[0] - tileSize*width)/2
        yGap = (resolution[1] - tileSize*height)/2

        # array that shall be returned by a function
        rectArr = [[] for _ in range(width)]
        # rectangle that will be moved and the copies of it will be created
        movingRect = pygame.Rect((xGap, yGap), (tileSize, tileSize))

        for x in range(height):
            for y in range(width):
                rectArr[x].append(movingRect.copy())
                movingRect = movingRect.move(tileSize, 0)
            movingRect = movingRect.move(0, tileSize)
            movingRect.left = xGap

        return rectArr

    def getTileMapFromTilePath(self, tilePath):
        tilePathIndex = 0
        row = 0
        column = 0
        columnChange = 1  # direction where the column goes
        map2d = [[None for _ in range(self.widthWholeMap)]
                 for _ in range(self.heightWholeMap)]

        while row < self.heightWholeMap:
            if (row < len(self.baseTilesNames)) and (column < len(self.baseTilesNames[row])):
                map2d[row][column] = self.baseTilesNames[row][column]
            elif tilePathIndex < len(tilePath):
                map2d[row][column] = tilePath[tilePathIndex]
                tilePathIndex += 1
            else:
                map2d[row][column] = "jungle"

            column += columnChange

            if column > self.widthWholeMap-1:
                row += 1
                columnChange = -columnChange
                column += columnChange

            if column < 0:
                row += 1
                columnChange = -columnChange
                column += columnChange

        return map2d

    def getTileMapSurface(self, tileMap, resolution="AUTO", background="fill_black"):
        # returns a tile map surface from an 2d array Arr of string names of the tiles

        if resolution == "AUTO":
            resolution = self.displaySurface.get_size()

        tileMapRects = self.getTileMapRects(
            resolution, len(tileMap[0]), len(tileMap))

        tileMapSurface = pygame.Surface(resolution)

        if background == "fill_black":
            tileMapSurface.fill((0, 0, 0))
        else:
            resizedBackground = pygame.transform.scale(
                background, (resolution))
            tileMapSurface.blit(resizedBackground, (0, 0))

        tileToPlace = pygame.Surface(tileMapRects[0][0].size)
        for x in range(len(tileMap)):
            for y in range(len(tileMap[0])):
                tileTexture = self.getTexture(tileMap[x][y])
                tileToPlace = pygame.transform.scale(
                    tileTexture, tileMapRects[x][y].size)
                tileMapSurface.blit(tileToPlace, tileMapRects[x][y])

        return tileMapSurface

    def showEndOfRoundScreen(self, roundStats):
        displayStr = "Round stats\n" + "tiles revealed: " + \
            str(roundStats["tilesRevealed"]) + "\n"
        displayStr = displayStr + "discovered gems: " + \
            str(roundStats["discoveredGems"]) + "\n"
        displayStr = displayStr + "gems collected: " + \
            str(roundStats["collectedGems"])

        maxTextSize = (self.displaySurface.get_width(
        ), self.displaySurface.get_height()/len(displayStr.split("\n")))
        textSurfs = self.getFontSurfacesFromString(
            displayStr, maxTextSize=maxTextSize)

        self.displaySurface.fill((0, 0, 0))

        # display banner stats:
        bannerHeight = textSurfs[0].get_height()
        self.displaySurface.blit(
            textSurfs[0], (self.calculateCenterX(textSurfs.pop(0)), 0))

        textSurfHeight = textSurfs[0].get_height()
        for surfaceIndex in range(len(textSurfs)):
            self.displaySurface.blit(
                textSurfs[surfaceIndex], (0, bannerHeight + (surfaceIndex)*textSurfHeight))

        self.update()
        self.checkIfPygameExit()
        self.clock.tick(FPS)

    def showEndOfGameScreen(self, gameStats):
        # if gameStats in self._cachedGameStats:
        #     cacheHit = True
        #     displayStr = self._cachedGameStats[gameStats]
        # else:
            # cacheHit = False
        displayStr = "Game stats\n"
        winnersStr = ", ".join(gameStats["winners"])
        displayStr += f"Winner/s: {winnersStr}\n" + \
            "tiles revealed: " + str(gameStats["tilesRevealed"]) + "\n"
        displayStr = displayStr + "discovered gems: " + \
            str(gameStats["discoveredGems"]) + "\n"
        displayStr = displayStr + "gems collected: " + \
            str(gameStats["collectedGems"])
        # self._cachedGameStats[gameStats] = displayStr

        maxTextSize = (self.displaySurface.get_width(
        ), self.displaySurface.get_height()/len(displayStr.split("\n")))
        textSurfs = self.getFontSurfacesFromString(
            displayStr, maxTextSize=maxTextSize)

        self.displaySurface.fill((0, 0, 0))

        # display banner stats:
        bannerHeight = textSurfs[0].get_height()
        self.displaySurface.blit(
            textSurfs[0], (self.calculateCenterX(textSurfs.pop(0)), 0))

        for surfaceIndex in range(len(textSurfs)):
            self.displaySurface.blit(textSurfs[surfaceIndex], (
                0, bannerHeight + (surfaceIndex)*textSurfs[surfaceIndex].get_height()))

        self.update()
        self.checkIfPygameExit()
        self.clock.tick(FPS)

    def showresultsOfRevealedTile(self, tilePath, playersDicts):
        tileMap = self.getTileMapFromTilePath(tilePath)
        tileMapResolution = (self.displaySurface.get_width(
        ), self.displaySurface.get_height())  # -self.myFont.get_height())
        tileMapRects = self.getTileMapRects(
            tileMapResolution, len(tileMap[0]), len(tileMap))
        tileMapSurf = self.getTileMapSurface(tileMap, tileMapResolution)

        # distinguishes who is where
        nicknamesInBase = []
        nicknamesExploring = []
        for player in playersDicts:
            if player["explores"]:
                nicknamesExploring.append(player["nickname"])
            elif player["inCamp"]:
                nicknamesInBase.append(player["nickname"])

        if len(nicknamesInBase) > 0:
            playersBaseSurf = self.getPlayersTileSurf(
                tileMapRects[0][0].width, nicknamesInBase)
        else:
            playersBaseSurf = None

        if len(nicknamesExploring) > 0:
            playersExploringSurf = self.getPlayersTileSurf(
                tileMapRects[0][0].width, nicknamesExploring)
        else:
            playersExploringSurf = None

        if len(tilePath) > 0:
            newestTileX, newestTileY = self.getTileIndexes(
                0, tilePath, len(tileMap[0]), len(tileMap), 2, 2)

        self.displaySurface.fill((0, 0, 0))
        # self.myFont.get_height()))
        self.displaySurface.blit(tileMapSurf, (0, 0))
        if playersBaseSurf:
            # self.myFont.get_height()))
            self.displaySurface.blit(
                playersBaseSurf, tileMapRects[0][0].move(0, 0))
        if playersExploringSurf:
            self.displaySurface.blit(playersExploringSurf, tileMapRects[newestTileX][newestTileY].move(
                0, 0))  # self.myFont.get_height()))

        self.update()
        self.checkIfPygameExit()
        self.clock.tick(FPS)

    def getPlayersTileSurf(self, tileSize, nicknames):
        surf = pygame.Surface((tileSize, tileSize))
        surf.fill((255, 255, 255))
        surf.set_colorkey((255, 255, 255))
        if len(nicknames) > 0:
            config = self.positions_config[len(nicknames)]

            nicknamesIndex = 0
            row = 0
            multiPl = [0.25, 0.5, 0.75]

            while row < 3:
                column = 0
                while column < 3:

                    if config[row][column]:
                        playerSurf = self.playersInfo["players"][nicknames[nicknamesIndex]
                                                                 ]["playerSurface"]
                        playerSurf = pygame.transform.scale(
                            playerSurf, (round(tileSize/5), round(tileSize/5)))
                        nicknamesIndex += 1
                        surf.blit(playerSurf, (tileSize*multiPl[row]-math.floor(playerSurf.get_width(
                        )/2), tileSize*multiPl[column]-math.floor(playerSurf.get_height()/2)))
                    column += 1
                row += 1
            return surf
        else:
            return surf

    def calculateCenterX(self, surface):
        return math.floor((self.displaySurface.get_width()-surface.get_width())/2)

    def calculateCenter(self, surface):
        return (math.floor((self.displaySurface.get_width()-surface.get_width())/2), math.floor((self.displaySurface.get_height()-surface.get_height())/2))


if __name__ == "__main__":
    resolution = (1280, 720)
    renderer = Renderer(resolution=resolution, fullscreen=False)
    renderer.clearCache()

    while True:
        renderer.renderRules()
        # renderer.renderGoingBack([], {}, {})

    # renderer.updatePlayersJoined([str(i) for i in range(9)])

    # test of waiting players to join
    # renderer.renderPlayersJoined()
    # pygame.time.wait(10000)
    # renderer.updatePlayersJoined(["Nickname0", "Nickname1", "Nickname2", "Nickname3", "Nickname4"])
    # pygame.time.wait(10000)
    # renderer.stopAskPlayersToJoin()

    # for i in range(1,6):
    #     renderer.showRoundNum(i)

    # renderer.startWaitingForDecisions(["Nickname0", "Nickname1", "Nickname2"])
    # pygame.time.wait(1000)
    # renderer.updateDecisions({"Nickname0":True})
    # pygame.time.wait(2000)
    # renderer.updateDecisions({"Nickname1":True, "Nickname2": False})
    # pygame.time.wait(10)
    # renderer.stopWaitingForDecisions()

    # test of blitting players
    # for i in range(5):
    #     renderer.playersInfo["players"][str(i)]["inCamp"]=True
    # players=[]
    # z=0
    # while 1 :
    #     if z==9:
    #         z=0
    #         players=[]
    #     else:
    #         players.append(str(z))
    #         z+=1
    #     renderer.clock.tick(2)
    #     surf = pygame.Surface((500,500))
    #     surf.fill((128,128,0))
    #     surf.blit(renderer.getPlayersTileSurf(500, players), (0,0))
    #     renderer.displaySurface.blit(surf, (0,0))
    #     renderer.checkIfPygameExit()
    #     renderer.update()

    # test of showRevealedTile
    # import game_Module
    # game = game_Module.Game()
    # nicknames = ["player1", "player2"]
    # game.addPlayers(nicknames)
    # renderer.updatePlayersJoined(nicknames)
    # game.revealTile()
    # renderer.showRevealedTile(game.getTilePathNames(), game.getPlayers())


# infoObj = pygame.display.Info()

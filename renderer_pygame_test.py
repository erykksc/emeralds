import unittest
import game_Module
import renderer_pygame
import pygame
from pprint import pprint

import pickle

import ctypes


class TileMapRenderingTestCase(unittest.TestCase):
    def setUp(self):
        self.renderer = renderer_pygame.Renderer(resolution = (1600, 800), fullscreen = True)
        print(pygame.display.list_modes(depth=24, flags= pygame.FULLSCREEN))
        deck = game_Module.Deck()
        #tilePath = [deck.pickCard() for _ in range(25)]

        tilePath=[]
        baseTilesNames = [["base","base"] for i in range(6)]
        x=0
        while x<=36:
            self.renderer.clock.tick(60)
            self.renderer.checkIfPygameExit()
            tilePathNames = self.renderer.convertTilePathToNames(tilePath)
            for i in range(len(tilePathNames)):
                if tilePathNames[i][:3]=="gem":
                    tilePathNames[i]="gem"
                elif tilePathNames[i][:6]=="relict":
                    if tilePathNames[i][-4:]=="Full":
                        tilePathNames[i]="relict_Full"
                    else:
                        tilePathNames[i]="relict_Empty"
                elif tilePathNames[i][:4]=="trap":
                    tilePathNames[i]="trap"

            tileMap = self.renderer.convertTilePathNamesTo2dMap(tilePathNames, baseTilesNames, 8, 6)
            tileMapSurf = self.renderer.getTileMapSurface(tileMap)
            self.renderer.displaySurface.fill((0,0,0))
            self.renderer.displaySurface.blit(tileMapSurf, (0,0))
            self.renderer.update()
            tilePath.append(deck.pickCard())
            x+=1

    def testConverTilePathToNames(self):
        with open("tests_correct_files/tilePath.correct", "rb") as tilePath_file:
            tilePath = pickle.load(tilePath_file)

        with open("tests_correct_files/tilePathNames.correct", "rb") as tilePathNames_file:
            correct_tilePathNames = pickle.load(tilePathNames_file)

        self.assertEqual(self.renderer.convertTilePathToNames(tilePath), correct_tilePathNames)


    def testconvertTilePathNamesTo2dMap(self):
        with open("tests_correct_files/tilePathNames.correct", "rb") as tilePathNames_file:
            correct_tilePathNames = pickle.load(tilePathNames_file)

        #temporary
        tilePathNames = correct_tilePathNames
        for i in range(len(tilePathNames)):
            if tilePathNames[i][:3]=="gem":
                tilePathNames[i]="gem"
            elif tilePathNames[i][:6]=="relict":
                if tilePathNames[i][-4:]=="Full":
                    tilePathNames[i]="relict_Full"
                else:
                    tilePathNames[i]="relict_Empty"
            elif tilePathNames[i][:4]=="trap":
                tilePathNames[i]="trap"

        baseTilesNames=[["base", "base"] for _ in range(6)]

        with open("tests_correct_files/tileMap2D.correct", "rb") as tileMap2D_file:
            correct_TileMap2D = pickle.load(tileMap2D_file)

        self.assertEqual(self.renderer.convertTilePathNamesTo2dMap(correct_tilePathNames, baseTilesNames, 8, 6), correct_TileMap2D)


    def testBlitTileMap(self):
        with open("tests_correct_files/tileMap2D.correct", "rb") as tileMap2D_file:
            correct_TileMap2D = pickle.load(tileMap2D_file)

        tileMapSurface = self.renderer.getTileMapSurface(correct_TileMap2D)

        with open("tests_correct_files/correctSurfaceString.correct", "rb") as correctSurfaceString_file:
            correctTileMapSurface = pickle.load(correctSurfaceString_file)

        surfaceToCheck = pygame.image.tostring(tileMapSurface, "ARGB")

        self.assertEqual(surfaceToCheck, correctTileMapSurface)

if __name__=="__main__":
    ctypes.windll.user32.SetProcessDPIAware()
    #true_res = (windll.user32.GetSystemMetrics(0),windll.user32.GetSystemMetrics(1))

    renderer = renderer_pygame.Renderer(resolution = (1920,1080), fullscreen = True)
    print("Available resolutions:", pygame.display.list_modes(depth=0, flags= pygame.FULLSCREEN))
    deck = game_Module.Deck()
    #tilePath = [deck.pickCard() for _ in range(25)]

    tilePath=[]
    baseTilesNames = [["base","base"] for i in range(6)]
    x=0
    while x<=36:
        renderer.clock.tick(60)
        renderer.checkIfPygameExit()
        tilePathNames = renderer.convertTilePathToNames(tilePath)
        for i in range(len(tilePathNames)):
            if tilePathNames[i][:3]=="gem":
                tilePathNames[i]="gem"
            elif tilePathNames[i][:6]=="relict":
                if tilePathNames[i][-4:]=="Full":
                    tilePathNames[i]="relict_Full"
                else:
                    tilePathNames[i]="relict_Empty"
            elif tilePathNames[i][:4]=="trap":
                tilePathNames[i]="trap"

        tileMap = renderer.convertTilePathNamesTo2dMap(tilePathNames, baseTilesNames, 8, 6)
        tileMapSurf = renderer.getTileMapSurface(tileMap)
        renderer.displaySurface.fill((0,0,0))
        renderer.displaySurface.blit(tileMapSurf, (0,0))
        renderer.update()
        tilePath.append(deck.pickCard())
        x+=1
    #unittest.main()

import game_Module
import renderer_pygame
import server_pygame
from server import webserver
import threading

class Emeralds():

    def __init__(self, numOfRounds=5, resolution=(800, 600)):
        # self.webserver = webserver.WebServer()
        self.webserverThread = threading.Thread(target=self.webserverFunc, name="webserverThread")
        self.webserverThread.start()
        self.server = server_pygame.Server()
        self.game = game_Module.Game()
        self.renderer = renderer_pygame.Renderer(resolution=resolution)
        self.round = 1
        self.numOfRounds = numOfRounds
        #self.renderer.menu()
        #temporary
        self.addPlayersToGame()
        self.playGame()
    
    def webserverFunc(self):
        server = webserver.WebServer()
        server.main()

    def addPlayersToGame(self):
        #add players to a self.game
        self.server.startWaitingForPlayers()
        while self.server.waitingForPlayers():
            #ask players to join and show players that have already joined
            self.renderer.updatePlayersJoined(self.server.getPlayersNicknames())

            self.renderer.renderPlayersJoined()

            if self.server.continuteToGame():
                self.server.stopWaitingForPlayers()
                
        self.game.addPlayers(self.server.getPlayersNicknames())

    def showRules(self):
        #show rules
        self.server.startWaitingForPlayers()
        while self.server.waitingForPlayers():
            self.renderer.showRules()

            if self.server.continuteToGame():
                self.server.stopWaitingForPlayers()

    def showRoundNum(self):
        self.renderer.showRoundNum(self.round)

    def decisions(self):
        #get players decisions
        playersThatDecide = self.game.getPlayersNamesThatDecide()
        print("Players that decide:", playersThatDecide)
        
        self.server.startWaitingForDecisions(playersThatDecide, self.game.getPlayers())
        while self.server.waitingForDecisions():
            self.renderer.renderWaitingForDecisions(playersThatDecide, self.server.getDecisions())

            if self.server.allDecisionsReady():
                self.server.stopWaitingForDecisions()
        self.game.setDecisions(self.server.getDecisions())

    def goingBack(self):
        print("Emeralds: goingBack")

        pastReference = self.game.getPlayers() #each player stats
        self.game.goingBack()
        #show effects based on player stats
        self.renderer.renderGoingBack(self.game.getTilePathNames(), self.game.getPlayers(), pastReference)


    def tileReveal(self):
        print("Emeralds: tileReveal")
        if self.game.isAnybodyExploring():
            self.game.revealTile()
            self.renderer.showRevealedTile(self.game.getTilePathNames(), self.game.getPlayers())

            self.game.resultsOfRevealedTile()
            reference = self.game.getPlayers()

            if self.game.isEndOfRound():
                self.server.startWaitingForPlayers()
                while self.server.waitingForPlayers():
                    self.renderer.showEndOfRoundScreen(self.game.getRoundStats())
                    if self.server.continuteToGame():
                        self.server.stopWaitingForPlayers()

            else:
                self.server.startWaitingForPlayers()
                while self.server.waitingForPlayers():
                    self.renderer.showresultsOfRevealedTile(self.game.getTilePathNames(), reference)
                    if self.server.continuteToGame():
                        self.server.stopWaitingForPlayers()

        elif self.game.isEndOfRound():
            self.server.startWaitingForPlayers()
            while self.server.waitingForPlayers():
                self.renderer.showEndOfRoundScreen(self.game.getRoundStats())
                if self.server.continuteToGame():
                    self.server.stopWaitingForPlayers()

    def playShortRound(self):
        self.decisions()
        self.goingBack()
        self.tileReveal()
        # self.consequences() not needed

    def playGame(self):
        self.showRules()
        while self.round <= self.numOfRounds:
            self.game.nextRound()
            self.showRoundNum()

            while not self.game.isEndOfRound():
                self.playShortRound()
            self.round += 1
        self.renderer.showEndOfGameScreen(self.game.getStats()) #wait for pc mouse
        # self.renderer.menu()

if __name__=="__main__":
    emeralds=Emeralds()

import game_Module
import renderer_pygame
import server_pygame

class Emeralds():

    def __init__(self, numOfRounds=5, resolution=(800, 600)):
        self.renderer = renderer_pygame.Renderer(resolution=resolution)
        self.game = game_Module.Game()
        self.server = server_pygame.Server()
        self.round = 1
        self.numOfRounds = numOfRounds
        #self.renderer.menu()
        #temporary
        self.addPlayersToGame()
        self.playGame()

    def addPlayersToGame(self):
        #add players to a self.game
        self.server.startWaitingForPlayers()
        self.server.startUpdatingPlayersNicknames()
        while self.server.waitingForPlayers():
            #ask players to join and show players that have already joined
            self.renderer.updatePlayersJoined(self.server.getPlayersNicknames())

            self.renderer.renderPlayersJoined()

            if self.server.continuteToGame():
                self.server.stopWaitingForPlayers()
                
        self.game.addPlayers(self.server.getPlayersNicknames())
        self.server.stopUpdatingPlayersNicknames()

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
        
        self.renderer.resetDecisions(playersThatDecide)
        self.server.startWaitingForDecisions(playersThatDecide)
        while self.server.waitingForDecisions():
            self.renderer.updateDecisions(self.server.getDecisions())
            self.renderer.renderWaitingForDecisions()
            if self.server.allDecisionsReady():
                self.server.stopWaitingForDecisions()
        self.game.setDecisions(self.server.getDecisions())

    def goingBack(self):
        if self.game.isAnybodyGoingBack():
            pastReference = self.game.getPlayers() #each player stats
            self.game.goingBack()
            #show effects based on player stats
            self.renderer.renderGoingBack(self.game.getTilePath(), self.game.getPlayers(), pastReference)
        else:
            state = self.game.getPlayers()
            self.renderer.showNotGoingBack(self.game.getTilePath(), state, state)

    def tileReveal(self):
        if self.game.isAnybodyExploring():
            self.game.revealTile()
            self.renderer.showRevealedTile(self.game.getRevealedTile())

            reference = self.game.getPlayers()
            self.game.resultsOfRevealedTile()

            if self.game.isEndOfRound():
                self.renderer.showEndOfRoundScreen(self.game.getRoundStats())
            else:
                self.renderer.showresultsOfRevealedTile(self.game.getRevealedTile(), reference, self.game.getPlayers())
        else:
            self.renderer.showEndOfRoundScreen(self.game.getRoundStats())

    def playRound(self):
        self.showRoundNum()
        self.decisions()
        self.goingBack()
        self.tileReveal()
        self.consequences()

    def playGame(self):
        self.showRules()
        if self.round <= self.numOfRounds:
            self.game.nextRound()
            while not self.game.isEndOfRound():
                self.playRound()
            self.round += 1
        self.renderer.showEndOfGameScreen(self.game.getStats()) #wait for pc mouse
        self.renderer.menu()

if __name__=="__main__":
    emeralds=Emeralds()

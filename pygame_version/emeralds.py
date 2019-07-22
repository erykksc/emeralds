import game_Module
import renderer_pygame
import server

class Emeralds():

    def __init__(self, numOfRounds=5, resolution=(800, 600)):
        self.renderer = renderer_pygame.Renderer(resolution=resolution)
        self.game = game_Module.Game()
        self.server = server.Server()
        self.round = 1
        self.numOfRounds = numOfRounds
        #self.renderer.menu()
        #temporary
        self.addPlayersToGame()
        self.playGame()

    def addPlayersToGame(self):
        #add players to a self.game
        self.server.startWaitingForPlayers()
        self.renderer.startAskPlayersToJoin()
        while self.server.waitingForPlayers():
            self.server.temporaryAddPlayers()
            #ask players to join and show players that have already joined

            #temporary
            self.renderer.updatePlayersJoined(self.server.getPlayersNicknames())
            #mouseClick or something or self.server.continuteToGame()
            if self.server.continuteToGame():
                self.server.stopWaitingForPlayers()
        self.game.addPlayers(self.server.getPlayersNicknames())
        self.renderer.stopAskPlayersToJoin()

    def showRules(self):
        #show rules
        self.renderer.startShowingRules()
        self.server.waitForPlayersToContinue()
        self.renderer.stopShowingRules()

    def showRoundNum(self):
        self.renderer.showRoundNum(self.round)

    def decisions(self):
        #get players decisions
        playersThatDecide = self.game.getPlayersNamesThatDecide()
        self.renderer.startWaitingForDecisions(playersThatDecide)
        self.server.startWaitingForDecisions(playersThatDecide)
        while self.server.waitingForDecisions():
            self.renderer.updateAlreadyDoneDecisions(self.server.getDecisions())
            if self.server.allDecisionsReady():
                self.server.stopWaitingForDecisions()
        self.game.setDecisions(self.server.getDecisions())
        self.renderer.stopWaitingForDecisions()

    def goingBack(self):
        if self.game.isAnybodyGoingBack():
            pastReference = self.game.getPlayers() #each player stats
            self.game.goingBack()
            #show effects based on player stats
            self.renderer.showGoingBack(self.game.getTilePath(), self.game.getPlayers(), pastReference)
        else:
            self.renderer.showNotGoingBack()

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

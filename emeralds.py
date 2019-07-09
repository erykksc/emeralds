import game_Module
import renderer_Module


class Emeralds():

    def __init__(self, numOfRounds=5, dispRes=(800, 600)):
        self.renderer = renderer.Renderer(dispRes)
        self.game = game.Game()
        self.server = server.Server()
        self.round = 1
        self.numOfRounds = numOfRounds
        renderer.menu()

    def addPlayersToGame(self):
        #add players to a game
        server.startWaitingForPlayers()
        renderer.startAskPlayersToJoin()
        while server.waitingForPlayers():
            #ask players to join and show players that have already joined
            renderer.UpdatePlayersJoined(server.getPlayersNicknames())
            #mouseClick or something or server.continuteToGame()
            if server.continuteToGame():
                server.stopWaitingForPlayers()

        renderer.stopAskPlayersToJoin()
        game.addPlayers(server.getPlayerNicknames())

    def showRules(self):
        #show rules
        renderer.startShowingRules()
        server.waitForPlayersToContinue()
        renderer.stopShowingRules()

    def showRoundNum(self):
        renderer.showRoundNum(self.round())

    def decisions(self):
        #get players decisions
        playersThatDecide = game.getPlayersThatDecide()
        renderer.startWaitingForDecisions(playersThatDecide)
        server.startWaitingForDecisions(playersThatDecide)
        while server.waitingForDecisions():
            renderer.updateAlreadyDoneDecisions(server.getDecisions())
            if server.allDecisionsReady():
                server.stopWaitingForDecisions()
        game.setDecisions(server.getDecisions())
        renderer.stopWaitingForDecisions()

    def goingBack(self):
        if game.isAnybodyGoingBack():
            pastReference = game.getPlayers() #each player stats
            game.goingBack()
            #show effects based on player stats
            renderer.showGoingBack(game.getTilePath(), game.getPlayers(), pastReference)
        else:
            renderer.showNotGoingBack()

    def tileReveal(self):
        if game.isAnybodyExploring():
            game.revealTile()
            renderer.showRevealedTile(game.getRevealedTile())

            reference = game.getPlayers()
            game.resultsOfRevealedTile()

            if game.isEndOfRound():
                renderer.showEndOfRoundScreen(game.getRoundStats())
            else:
                renderer.showresultsOfRevealedTile(game.getRevealedTile(), reference, game.getPlayers())
        else:
            renderer.showEndOfRoundScreen(game.getRoundStats())

    def playRound(self):
        self.showRoundNum()
        self.decisions()
        self.goingBack()
        self.tileReveal()

    def playGame(self):
        self.showRules()
        if self.round <= self.numOfRounds:
            self.game.nextRound()
            while not game.isEndOfRound():
                self.playRound()
            self.round += 1
        renderer.showEndOfGameScreen(game.getStats()) #wait for pc mouse
        renderer.menu()

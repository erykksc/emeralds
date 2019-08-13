import game_Module
import renderer_pygame
import server_pygame

class Emeralds():

	def __init__(self, numOfRounds=5, resolution=(800, 600), fullscreen=False, graphics="default"):
		self.server = None
		self.gameIP = ""
		self.gamePort = ""
		self.game = None 
		self.renderer = renderer_pygame.Renderer(resolution=resolution, fullscreen=fullscreen, graphics=graphics)
		self.round = 0
		self.numOfRounds = numOfRounds

		self.serverReady = False

	def main(self):
		self.menu()
		
	def menu(self):
		returnString = ""
		while returnString == "":
			returnString = self.renderer.renderMenu()
		if returnString == "Play":
			self.setUpGame()

		elif returnString == "Settings":
			returnSettingsString = ""
			while returnSettingsString != "go_back":
				returnSettingsString = self.renderer.renderSettings()

				if returnSettingsString.split(" ")[0] == "num_of_rounds":
					self.numOfRounds = int(returnSettingsString.split(" ")[1])
					print("new round number:", self.numOfRounds)


		elif returnString == "Credits":
			while self.renderer.renderCredits() != "go_back":
				pass

		self.menu()

	def setUpGame(self):
		if not self.serverReady:

			self.server = server_pygame.Server()
			self.gameIP = self.server.getIp()
			self.gamePort = self.server.getPort()
			self.serverReady = True
		
		self.game = game_Module.Game()
		self.round = 1

		self.addPlayersToGame()
		self.playGame()

	def addPlayersToGame(self):
		#add players to a self.game
		self.server.startWaitingForPlayers()
		self.server.startWaitingForNicknames()
		self.server.askPlayersForNicknames()
		returnString = ""
		while self.server.waitingForPlayers():
			#ask players to join and show players that have already joined
			self.renderer.updatePlayersJoined(self.server.getPlayersNicknames())


			returnString = self.renderer.renderPlayersJoined(self.gameIP, self.gamePort)

			if self.server.continuteToGame() or returnString == "go_back":
				self.server.stopWaitingForPlayers()
				self.server.stopWaitingForNicknames()
		if returnString == "go_back":
			self.menu()
		else:
			self.game.addPlayers(self.server.getPlayersNicknames())

	def showRules(self):
		#show rules
		self.server.startWaitingForPlayers()
		while self.server.waitingForPlayers():
			self.renderer.renderRules()

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
		self.server.startWaitingForPlayers()
		while self.server.waitingForPlayers():
			self.renderer.showEndOfGameScreen(self.game.getGameStats())
			if self.server.continuteToGame():
				self.server.stopWaitingForPlayers()
		self.menu()

if __name__ == "__main__":
	emeralds = Emeralds(resolution=(1920, 1080), fullscreen=True, graphics="pola")
	emeralds.main()

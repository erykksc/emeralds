class Server():
    def __init__(self):
        self.players=[]
        self.waitingForPlayersV=False

    def getPlayersNicknames(self):
        return self.players

    def continuteToGame(self):
        #temporary
        inp = input("Continue to game y/n\n")
        if inp=="y":
            return True
        else:
            return False

    def startWaitingForPlayers(self):
        # temporary
        self.waitingForPlayersV=True

    def waitingForPlayers(self):
        return self.waitingForPlayersV

    def stopWaitingForPlayers(self):
        # temporary
        self.waitingForPlayersV=False

    def temporaryAddPlayers(self):
        self.players=["eryk", "maks", "terarm"]

    def waitForPlayersToContinue(self):
        input("\nwaitForPlayersToContinue\nPress enter to continue")

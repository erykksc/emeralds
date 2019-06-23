import json_loader
import random
import time
import math

gemCardValues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
trapCardNames = ["snakes", "spiders", "lava", "wrecking-ball", "guns"]
relictCardValues = [3, 5, 7, 9, 11]

class TrapCard():
    def __init__(self, name):
        self.type = "trap"
        self.name = name

    def getName(self):
        return ("trap_" + str(self.name))

class GemCard():
    def __init__(self, amountOfGems):
        self.type = "gem"
        self.amountOfGems = amountOfGems
        self.gemsLeft = amountOfGems

    def resetGems(self):
        self.gemsLeft=self.amountOfGems

    def decreaseGemsLeft(self, amount):
        self.gemsLeft-=amount

    def getName(self):
        return ("gem_" + str(self.amountOfGems))

class RelictCard():
    def __init__(self, value):
        self.type = "relict"
        self.value = value

    def getName(self):
        return ("relict_" + str(self.value))

class Player():
    def __init__(self, nickname):
        self.nickname = nickname
        self.securedGems = 0 #Gems in chest
        self.unsecuredGems = 0 #Gems outside the chest
        self.inCamp = True
        self.explores = False

    def secureGems(self):
        self.securedGems += self.unsecuredGems
        self.unsecuredGems = 0

    def loseUnsecuredGems(self):
        self.unsecuredGems = 0

    def receiveGems(self, amount):
        self.unsecuredGems += amount

class Deck():
    def __init__(self):
        self.newDeck()

    def newDeck(self):
        global gemCardValues
        global trapCardNames
        global relictCardValues

        gemCards = [GemCard(amount) for amount in gemCardValues]
        trapCards = [TrapCard(trapName) for trapName in trapCardNames]
        relictCards = [RelictCard(relictValue) for relictValue in relictCardValues]
        self.deck = gemCards + 3*trapCards + relictCards

    def pickCard(self): # picks random card from a deck
        return self.deck[random.randint(0, len(self.deck)-1)]

    def resetGemCards(self):
        for index in range(len(self.deck)):
            card = self.deck[index]
            if card.type == "gem":
                card.resetGems()

    def removeCardFromDeck(self, cardType, value): #returns True if removed sucessfully else returns False
        for index in range(len(self.deck)):
            card = self.deck[index]
            if card.type == cardType:
                if card.type=="trap":
                    if card.name == value:
                        self.deck.pop(index)
                        return True
                elif card.type=="gem":
                    if card.amountOfGems==value:
                        self.deck.pop(index)
                        return True
                elif card.type=="relict":
                    if card.value == value:
                        self.deck.pop(index)
                        return True
        return False

class Game:
    def __init__(self):
        self.players = [Player(player) for player in json_loader.readValue("players") ]
        json_loader.updatePair("playerCount", len(self.players))

        self.gameDeck = Deck()
        self.roundDeck = self.gameDeck
        self.traps=[] #list of traps that were already revealed
        self.tilePath=[]

    def allPlayersInCamp(self):
        for player in self.players:
            if not player.inCamp:
                return False
        return True

    def copyPath2Json(self):
        tilePathNames = []
        for i in range(len(self.tilePath)):
            tilePathNames.append(self.tilePath[i].getName())

        json_loader.updatePair("tilePath", tilePathNames)

    def copyPlayersFromGameState(self):
        self.game_state = json_loader.readFromJson()
        for playerD, playerC in list(zip(self.game_state["players"], self.players)): # playerD - player dictionary, playerC - player class
            playerC.securedGems = self.game_state["players"][playerD]["securedGems"]
            playerC.unsecuredGems = self.game_state["players"][playerD]["unsecuredGems"]
            playerC.inCamp = self.game_state["players"][playerD]["inCamp"]
            playerC.explores = self.game_state["players"][playerD]["explores"]

    def copyPlayersToGameState(self):
        self.game_state = json_loader.readFromJson()
        for playerD, playerC in list(zip(self.game_state["players"], self.players)): # playerD - player dictionary, playerC - player class
            self.game_state["players"][playerD]["securedGems"] = playerC.securedGems
            self.game_state["players"][playerD]["unsecuredGems"] = playerC.unsecuredGems
            self.game_state["players"][playerD]["inCamp"] = playerC.inCamp
            self.game_state["players"][playerD]["explores"] = playerC.explores
        json_loader.write2json(self.game_state)

    def playGame(self):
        while(json_loader.readValue("roundNum") < json_loader.readValue("numOfRounds")):
            print("Playing round")
            self.playRound()

    def playRound(self):
        self.tilePath=[]
        json_loader.updatePair("tilePath", [])
        self.traps=[] #list of traps that were already revealed
        json_loader.updatePair("traps", [])
        json_loader.updatePair("roundNum", json_loader.readValue("roundNum") +1)
        self.roundDeck = self.gameDeck

        print("playing shortRound")
        self.playShortRound()
        while not(self.allPlayersInCamp()):
            print("playing shortRound")
            self.playShortRound()

    def playShortRound(self):
        self.gameDeck.resetGemCards()
        self.decisions()
        self.wait4ready2Continue()
        if self.goingBack():
            self.wait4ready2Continue()

        if self.tileReveal(): #lose or win
            self.wait4ready2Continue()
            self.consequences()
            self.wait4ready2Continue()

        self.updateRewardForGoingBack()

    def decisions(self):
        self.wait4decisions()
        self.copyPlayersFromGameState()

    def wait4decisions(self):
        json_loader.updatePair("state", 0)
        json_loader.updatePair("waiting4Answers", True)

        print("waiting for input")
        while(json_loader.readValue("waiting4Answers")):
            #wait for everybody
            time.sleep(1)

        json_loader.updatePair("waiting4Answers", False)

    def goingBack(self):
        if not(self.allPlayersInCamp()):
            json_loader.updatePair("state", 1)
            playersGB = [] #players going back

            for playerIndex in range(len(self.players)):
                if not self.players[playerIndex].inCamp:
                    if not self.players[playerIndex].explores:
                        playersGB.append(playerIndex)

            if len(playersGB)>0:

                for tileIndex in range(len(self.tilePath)-1, -1, -1): #index is decrementing for the entire path
                    tile = self.tilePath[tileIndex]

                    if tile.type == "gems" and tile.gemsLeft>0:
                        for playerIndex in playersGB:
                            self.players[playerIndex].receiveGems(math.floor(tile.gemsLeft/len(playersGB)))
                        self.tilePath[tileIndex].gemsLeft %= len(playersGB)

                    elif tile.type == "relict" and len(playersGB)==1:
                        self.players[playersGB[0]].receiveGems(tile.value)
                        self.gameDeck.removeCardFromDeck("relict", tile.value)
                        relicts = json_loader.readValue("relicts4GoingBack")
                        self.tilePath.pop(tileIndex)
                        json_loader.updatePair("relicts4GoingBack", relicts)

                for playerIndex in playersGB:
                    self.players[playerIndex].secureGems()
                    self.players[playerIndex].inCamp = True
                self.copyPlayersToGameState()
                return True
        return False

    def wait4ready2Continue(self):
        while(json_loader.readValue("ready2Continue")==False):
            time.sleep(1)
        json_loader.updatePair("ready2Continue", False)

    def updateRewardForGoingBack(self):
        gemsAmount = 0
        relictsLeft=[]
        for tile in self.tilePath:
            if tile.type == "gem":
                gemsAmount += tile.gemsLeft
            elif tile.type == "relict":
                relictsLeft.append(tile.getName())
        json_loader.updatePair("gems4GoingBack", gemsAmount)
        json_loader.updatePair("relicts4GoingBack", relictsLeft)

    def tileReveal(self):
        if not(self.allPlayersInCamp()):
            json_loader.updatePair("state", 2)
            tileRevealed = self.roundDeck.pickCard()
            self.tilePath.append(tileRevealed)
            self.copyPath2Json()
            return True
        return False

    def consequences(self):
        if not(self.allPlayersInCamp()):
            tileRevealed = self.tilePath[len(self.tilePath)-1]
            playersE = [] #players exploring (indexes)
            for playerIndex in range(len(self.players)):
                if not self.players[playerIndex].inCamp:
                    if self.players[playerIndex].explores:
                        playersE.append(playerIndex)

            if tileRevealed.type=="trap":
                self.roundDeck.removeCardFromDeck("trap", tileRevealed.name)
                self.traps.append(tileRevealed)

                traps = json_loader.readValue("traps")
                traps.append(tileRevealed.getName())
                json_loader.updatePair("traps", traps)

                checkTrapsResult = self.checkTraps()
                if (checkTrapsResult): #check if there are 2 traps of the same kind
                    json_loader.updatePair("state", 4)
                    for playerIndex in playersE:
                        self.players[playerIndex].loseUnsecuredGems()
                        self.players[playerIndex].inCamp = True

                    self.gameDeck.removeCardFromDeck("trap", checkTrapsResult)
                    json_loader.updatePair("killed_by", checkTrapsResult)
                    removedCards = json_loader.readValue("removedCards")
                    removedCards.append(checkTrapsResult)
                    json_loader.updatePair("removedCards", removedCards)


            elif tileRevealed.type=="gem":
                json_loader.updatePair("state", 3)
                self.roundDeck.removeCardFromDeck("gem", tileRevealed.amountOfGems)
                for playerIndex in playersE:
                    self.players[playerIndex].receiveGems(math.floor(tileRevealed.gemsLeft/len(playersE)))
                self.tilePath[len(self.tilePath)-1].gemsLeft %= len(playersE)
                self.copyPath2Json()

            else:
                self.roundDeck.removeCardFromDeck("relict", tileRevealed.value)

            self.copyPlayersToGameState()

    def checkTraps(self):
        trapsChecked=[]
        for i in range(len(self.traps)):
            if not self.traps[i] in trapsChecked:
                trapsChecked.append(self.traps[i])
            else:
                return self.traps[i].name
        return False


if __name__ == "__main__":
    json_loader.createJson()
    #input("Enter when ready:")

    dict={"player1":{
        "securedGems" : 0,
        "unsecuredGems" : 0,
        "inCamp" : False,
        "explores" : True
        },"player2":{
        "securedGems" : 0,
        "unsecuredGems" : 0,
        "inCamp" : False,
        "explores" : True
        }
    }
    file=json_loader.readFromJson()
    file["players"]=dict
    json_loader.write2json(file)
    game = Game()
    game.playGame()

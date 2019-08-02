import random
import math
import copy

gemCardValues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
trapCardNames = ["snakes", "spiders", "lava", "wreckingball", "guns"]
relictCardValues = [3, 5, 7, 9, 11]

# implement in the future


class Tile():
    def __init__(self, tileType):
        self.type = tileType

    def getType(self):
        return self.type

    def getName(self):
        return self.type


class TrapCard(Tile):
    def __init__(self, name):
        Tile.__init__(self, "trap")
        self.name = name

    def getName(self):
        return ("trap_" + str(self.name))


class GemCard(Tile):
    def __init__(self, amountOfGems):
        Tile.__init__(self, "gem")
        self.amountOfGems = amountOfGems
        self.gemsLeft = amountOfGems

    def resetGems(self):
        self.gemsLeft = self.amountOfGems

    def decreaseGemsLeft(self, amount):
        self.gemsLeft -= amount

    def setGemsLeft(self, amount):
        self.gemsLeft = amount

    def getGemsLeft(self):
        return self.gemsLeft

    def getName(self):
        return ("gem_" + str(self.gemsLeft) + "/" + str(self.amountOfGems))

    def getAmountOfGems(self):
        return self.amountOfGems


class RelictCard(Tile):
    def __init__(self, value):
        Tile.__init__(self, "relict")
        self.value = value
        self.containsRelictV = True

    def getName(self):
        if self.containsRelictV:
            return ("relict_" + str(self.value) + "_full")
        else:
            return ("relict_" + str(self.value) + "_empty")

    def removeRelict(self):
        self.containsRelictV = False

    def containsRelict(self):
        return self.containsRelictV

    def resetRelict(self):
        self.containsRelictV = True

    def getValue(self):
        return self.value


class Player():
    def __init__(self, nickname):
        self.nickname = nickname
        self.securedGems = 0  # Gems in chest
        self.unsecuredGems = 0  # Gems outside the chest
        self.inCamp = True
        self.explores = False
        self.decides = True

    def secureGems(self):
        self.securedGems += self.unsecuredGems
        self.unsecuredGems = 0

    def loseUnsecuredGems(self):
        self.unsecuredGems = 0

    def receiveGems(self, amount):
        self.unsecuredGems += amount

    def isExploring(self):
        return self.explores

    def setExploring(self, value):
        self.explores = value

    def isInCamp(self):
        return self.inCamp

    def setInCamp(self, value):
        self.inCamp = value

    def restartDecision(self):
        self.setInCamp(True)
        self.setExploring(False)
        self.decides = True
    
    def getNickname(self):
        return self.nickname
    
    def getDictionary(self):
        d={}
        d["nickname"] = self.nickname
        d["inCamp"] = self.inCamp
        d["explores"] = self.explores
        d["unsecuredGems"] = self.unsecuredGems
        d["securedGems"] = self.securedGems
        return d

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

    def pickCard(self):  # picks random card from a deck
        return self.deck[random.randint(0, len(self.deck)-1)]
    
    def copy(self):
        return copy.deepcopy(self)

    def resetCards(self):
        for index in range(len(self.deck)):
            card = self.deck[index]
            if card.type == "gem":
                self.deck[index].resetGems()
            if card.type == "relict":
                self.deck[index].resetRelict()

    # returns True if removed sucessfully else returns False
    def removeCardFromDeck(self, cardType, value):
        for index in range(len(self.deck)):
            card = self.deck[index]
            if card.type == cardType:
                if card.type == "trap":
                    if card.name == value:
                        self.deck.pop(index)
                        return True
                elif card.type == "gem":
                    if card.amountOfGems == value:
                        self.deck.pop(index)
                        return True
                elif card.type == "relict":
                    if card.value == value:
                        self.deck.pop(index)
                        return True
        return False


class Game:
    def __init__(self, deck=Deck()):  # deck should be Deck() class
        self.players = []
        self.gameDeck = deck
        self.roundDeck = self.gameDeck.copy()
        self.roundNum = 0

        self.traps = []
        self.tilePath = []
        self.removedCards = []
        self.killedBy = None

    def addPlayers(self, playersArr):
        players = []
        for player in playersArr:
            players.append(Player(player))
        self.players = players

    def getPlayers(self):
        rArr = [] #return dictionary
        for player in self.players:
            rArr.append(player.getDictionary())
        return rArr

    def nextRound(self):
        self.roundNum += 1
        self.resetDecisions()
        self.gameDeck.resetCards()
        self.traps = []
        self.tilePath = []
        self.roundDeck = self.gameDeck.copy()

    def resetDecisions(self):
        for index in range(len(self.players)):
            self.players[index].restartDecision()

    def getRoundNum(self):
        return self.roundNum

    def getRoundStats(self):
        """returns a dictionary with round stats"""
        stats = {
            "tilesRevealed": len(self.tilePath), 
            "discoveredGems": self.countDiscoveredGems(),
             "collectedGems": self.countCollectedGems()
            }
        return stats

    def getGameStats(self):
        #temporary
        stats = {
            "winners": self.getWinners,
            "tilesRevealed": "Not yet implemented", 
            "discoveredGems": "Not yet implemented",
             "collectedGems": "Not yet implemented"
            }
        return stats

    def getWinners(self):
        most = 0
        winners = []
        for player in self.players:
            if player.securedGems >most:
                most = player.securedGems
        
        for player in self.players:
            if player.securedGems == most:
                winners.append(player.nickname)
        return winners

    def countDiscoveredGems(self):
        discovered = 0
        for tile in self.tilePath:
            if tile.type == "gem":
                discovered += tile.getAmountOfGems()
        return discovered

    def countCollectedGems(self):
        collected = 0
        for tile in self.tilePath:
            if tile.type == "gem":
                collected += tile.getAmountOfGems() - tile.getGemsLeft()
        return collected

    def allPlayersInCamp(self):
        for player in self.players:
            if not player.inCamp:
                return False
        return True

    def allPlayersNotDeciding(self):
        for player in self.players:
            if player.decides:
                return False
        return True

    def isEndOfRound(self):
        if self.allPlayersInCamp() and self.allPlayersNotDeciding():
            return True
        else:
            return False

    # dictOfPlayersDecisions {"Nickname1":True, "Nickname2":False}
    def setDecisions(self, dictOfPlayersDecisions):
        for playerKeyName in dictOfPlayersDecisions:
            for index in range(len(self.players)):
                if self.players[index].nickname == playerKeyName:
                    self.players[index].setExploring(
                        dictOfPlayersDecisions[playerKeyName])
                    break

    def getPlayersNamesThatDecide(self):
        arr = []
        for player in self.players:
            if player.decides:
                arr.append(player.nickname)
        return arr

    def isAnybodyGoingBack(self):
        for player in self.players:
            if not player.isInCamp() and not player.isExploring():
                return True
        return False

    def isAnybodyExploring(self):
        for player in self.players:
            if player.decides and player.isExploring():
                return True
        return False

    def goingBack(self):
        if not self.allPlayersNotDeciding():

            # adds players that are going back to IndexesOfPlayersGB
            IndexesOfPlayersGB = []  # players going back

            for playerIndex in range(len(self.players)):
                if self.players[playerIndex].decides:
                    if not self.players[playerIndex].isExploring():
                        IndexesOfPlayersGB.append(playerIndex)
            print("Players going back:", [self.players[i].nickname for i in IndexesOfPlayersGB])
            # Perform actions for people that are going back
            if len(IndexesOfPlayersGB) > 0:

                # index is decrementing for the entire path
                for tileIndex in range(len(self.tilePath)-1, -1, -1):
                    tile = self.tilePath[tileIndex]

                    if (tile.type == "gem") and (tile.getGemsLeft() > 0):
                        for playerIndex in IndexesOfPlayersGB:
                            self.players[playerIndex].receiveGems(
                                math.floor(tile.getGemsLeft()/len(IndexesOfPlayersGB)))
                        gemsLeft = self.tilePath[tileIndex].getGemsLeft() % len(
                            IndexesOfPlayersGB)
                        self.tilePath[tileIndex].setGemsLeft(gemsLeft)

                    elif tile.type == "relict" and len(IndexesOfPlayersGB) == 1:
                        self.players[IndexesOfPlayersGB[0]].receiveGems(tile.getValue())
                        self.gameDeck.removeCardFromDeck("relict", tile.getValue())
                        self.tilePath[tileIndex].removeRelict()

                for playerIndex in IndexesOfPlayersGB:
                    self.players[playerIndex].secureGems()
                    self.players[playerIndex].setInCamp(True)
                    self.players[playerIndex].decides = False

    def revealTile(self):
        tileRevealed = self.roundDeck.pickCard()
        self.tilePath.append(tileRevealed)

    def getRevealedTile(self):
        return self.tilePath[-1].getName()

    def resultsOfRevealedTile(self):
        if not self.allPlayersNotDeciding():
            tileRevealed = self.tilePath[-1]
            playersE = []  # players exploring (indexes)
            for playerIndex in range(len(self.players)):
                if self.players[playerIndex].decides:
                    if self.players[playerIndex].explores:
                        playersE.append(playerIndex)
                        self.players[playerIndex].setInCamp(False)

            if tileRevealed.type == "trap":
                self.roundDeck.removeCardFromDeck("trap", tileRevealed.name)
                self.traps.append(tileRevealed)

                checkTrapsResult = self.checkTraps()
                if (checkTrapsResult):  # check if there are 2 traps of the same kind
                    for playerIndex in playersE:
                        self.players[playerIndex].loseUnsecuredGems()
                        self.players[playerIndex].setInCamp(True)
                        self.players[playerIndex].decides = False

                    self.gameDeck.removeCardFromDeck("trap", checkTrapsResult.name)

            elif tileRevealed.type == "gem":
                self.roundDeck.removeCardFromDeck("gem", tileRevealed.amountOfGems)
                for playerIndex in playersE:
                    self.players[playerIndex].receiveGems(
                        math.floor(tileRevealed.gemsLeft/len(playersE)))
                gemsLeft = self.tilePath[-1].getGemsLeft() % len(playersE)
                self.tilePath[-1].setGemsLeft(gemsLeft)

            else:
                self.roundDeck.removeCardFromDeck("relict", tileRevealed.value)

    def checkTraps(self):
        # checks if there are two traps of the same type
        trapsChecked = []
        for i in range(len(self.traps)):
            if not self.traps[i] in trapsChecked:
                trapsChecked.append(self.traps[i])
            else:
                return self.traps[i]
        return False

    def getTilePathNames(self):
        tileMapNames = []
        for tile in self.tilePath:
            tileMapNames.append(tile.getName())
        return tileMapNames

    def getTilePath(self):
        return self.tilePath


if __name__ == "__main__":
    deck = Deck()
    game = Game(deck)
    game.addPlayers(["player1", "player2"])
    print(game.getPlayersNamesThatDecide())
    decisions = {
        "player1":True,
        "player2":False
    }
    game.nextRound()
    game.setDecisions(decisions)
    for i in range(10):
        game.goingBack()
        game.revealTile()
        print("rcopyevealed tile:", game.tilePath[-1].getName())
        game.resultsOfRevealedTile()
    
    print(game.gameDeck)
    game.nextRound()
    print(game.gameDeck)
    # print(game.getPlayers())


from websocket import create_connection
import threading
import time
import json

def readInfo():
    try:
        with open("server/players_info.json") as f:
            return  json.load(f)
           
    except FileNotFoundError:
        print("No json file found")


class Server():
    def __init__(self):
        self.waitingForPlayersV = False

        self.nicknames = []
        self.nicknamesUpdating = False

        self.playersThatDecide = []
        self.waitingForDecisionsV = False

        info = readInfo()

        ip = str(info["ip"])
        port = str(info["port"])
        url = "ws://"+ip+":"+port+"/adminwebsocket"
        print("Connecting to:", url)
        self.ws = create_connection(url)

    def startUpdatingPlayersNicknames(self):
        self.nicknamesUpdating = True
        updatingThread = threading.Thread(target = self.updatePlayersNicknames)
        updatingThread.start()
    
    def updatePlayersNicknames(self):
        while self.nicknamesUpdating:
            info = readInfo()
            self.nicknames = [nick for nick in info["players"]]
            time.sleep(0.1)
    
    def stopUpdatingPlayersNicknames(self):
        self.nicknamesUpdating = False

    def getPlayersNicknames(self):
        return self.nicknames

    def continuteToGame(self):
        info = readInfo()
        return info["continue"]

    def startWaitingForPlayers(self):
        self.ws.send("changeAccept n True")
        self.ws.send("sendToAll RENDER PRESS_TO_CONTINUE")
        self.ws.send("changeContinue False")
        self.waitingForPlayersV = True

    def waitingForPlayers(self):
        return self.waitingForPlayersV

    def stopWaitingForPlayers(self):
        self.ws.send("changeAccept n False")
        self.waitingForPlayersV = False

    def startWaitingForDecisions(self, playersThatDecide):
        self.playersThatDecide = playersThatDecide
        self.waitingForDecisionsV = True
        self.ws.send("resetDecisions")
        self.ws.send("changeAccept d True")
        self.ws.send("sendToAll RENDER DECISION")

    def waitingForDecisions(self):
        return self.waitingForDecisionsV

    def stopWaitingForDecisions(self):
        self.waitingForDecisionsV = False
        self.ws.send("changeAccept d False")
        self.ws.send("sendToAll RENDER WAITING")

    def getDecisions(self):
        info = readInfo()
        decisions = {}

        for player in info["players"]:
            if info["players"][player]["currentDecision"]:
                decisions[player] = info["players"][player]["decision"]

        return decisions
    
    def allDecisionsReady(self):
        decisions = self.getDecisions()

        for nickname in self.playersThatDecide:
            if nickname not in decisions:
                return False
        return True


if __name__=="__main__":
    server = Server()
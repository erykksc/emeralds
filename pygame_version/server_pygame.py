import time
import json
from websocket import create_connection
import threading
import asyncio
from server import internal_webserver

def readInfo():
    while True:
        try:
            with open("players_info.json") as f:
                return  json.load(f)
        
        except:
            time.sleep(0.05)
            continue

def start_server(webserver):
    asyncio.set_event_loop(asyncio.new_event_loop())
    webserver.run()

class Server():
    def __init__(self):
        webserver = internal_webserver.WebServer()
        webserverThread = threading.Thread(target = start_server, args=(webserver,))
        webserverThread.daemon = True
        webserverThread.start()

        self.waitingForPlayersV = False

        self.playersThatDecide = []
        self.waitingForDecisionsV = False

        info = readInfo()

        self.ip = str(info["ip"])
        self.port = str(info["port"])
        url = "ws://" + self.ip + ":" + self.port + "/adminwebsocket"
        print("Connecting to:", url)
        connected = False
        while not connected:
            try:
                self.ws = create_connection(url)
                connected = True
            except:
                time.sleep(0.05)
                continue
    
    def getIp(self):
        return self.ip
    
    def getPort(self):
        return self.port
    
    def getPlayersNicknames(self):
        info = readInfo()            
        return [nick for nick in info["players"]]

    def continuteToGame(self):
        info = readInfo()
        return info["continue"]

    def startWaitingForPlayers(self):
        self.ws.send("changeAccept n True")
        self.ws.send("sendToAll RENDER PRESS_TO_CONTINUE")
        self.ws.send("changeContinue False")
        self.waitingForPlayersV = True
        time.sleep(0.2)
    
    def askPlayersForNicknames(self):
        self.ws.send("sendToAll RENDER ENTER_NICKNAMES")

    def waitingForPlayers(self):
        return self.waitingForPlayersV

    def stopWaitingForPlayers(self):
        self.waitingForPlayersV = False
        self.ws.send("changeAccept n False")

    def startWaitingForDecisions(self, playersThatDecide, playersDicts):
        self.playersThatDecide = playersThatDecide
        self.waitingForDecisionsV = True
        self.ws.send("resetDecisions")
        self.ws.send("changeAccept d True")
        self.ws.send("sendToAll RENDER DECISION")
        for player in playersDicts:
            str2Send = "sendToUser " + str(player["nickname"]) + " GEMS " + str(player["securedGems"]) + " " + str(player["unsecuredGems"])
            self.ws.send(str2Send)
        time.sleep(0.2)


        #send json file to each player including information how many gems does he have

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
                decisions[player] = True if info["players"][player]["decision"]=="true" else False

        return decisions
    
    def allDecisionsReady(self):
        decisions = self.getDecisions()

        for nickname in self.playersThatDecide:
            if nickname not in decisions:
                return False
        return True


if __name__=="__main__":
    server = Server()
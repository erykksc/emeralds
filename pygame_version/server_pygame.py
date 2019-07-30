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

        ip = str(info["ip"])
        port = str(info["port"])
        url = "ws://"+ip+":"+port+"/adminwebsocket"
        print("Connecting to:", url)
        connected = False
        while not connected:
            try:
                self.ws = create_connection(url)
                connected = True
            except:
                time.sleep(0.05)
                continue
    
    def runTornado(self):
        TWebServer = internal_webserver.WebServer()
        app = TWebServer.getApp()
        app.listen(8888)
        ioloop.start()

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

    def waitingForPlayers(self):
        return self.waitingForPlayersV

    def stopWaitingForPlayers(self):
        self.ws.send("changeAccept n False")
        self.waitingForPlayersV = False

    def startWaitingForDecisions(self, playersThatDecide, playersDicts):
        self.playersThatDecide = playersThatDecide
        self.waitingForDecisionsV = True
        self.ws.send("resetDecisions")
        self.ws.send("changeAccept d True")
        self.ws.send("sendToAll RENDER DECISION")
        for player in playersDicts:
            str2Send = "sendToUser " + str(player["nickname"]) + " GEMS " + str(player["securedGems"]) + " " + str(player["unsecuredGems"])
            self.ws.send(str2Send)


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
import os
import socket
import tornado
from tornado.httpserver import HTTPServer
from tornado.options import define, options
import tornado.web
from tornado import websocket

from server import jsonED

connections = []
usernames = {}

accept={
    "n" : False,
    "d" : False
}

#ADMIN FUNCTIONS
def send_to_all(message):
    for connection in connections:
        connection.write_message(message)

def disconnectEverybody():
    for connection in connections:
        print(connection.request.remote_ip, "Disconnected")
        connection.close()
        try:
            info = jsonED.readFromJson()
            del info["players"][usernames[connection]]
            jsonED.write2json(info)

            del usernames[connection]

        except KeyError:
            #player didn't enter the nickname and has diconnected
            pass
        connections.remove(connection)

class IndexRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(200)
        with open(os.path.join(os.path.dirname(__file__), "static", "index.html")) as f:
            self.write(f.read())

class ClientJsRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(200)
        with open(os.path.join(os.path.dirname(__file__), "scripts", "client.js")) as f:
            self.write(f.read())

class normalWebSocket(tornado.websocket.WebSocketHandler):

    def open(self):
        print(self.request.remote_ip, "Connected")

        connections.append(self)

    def on_message(self, message):
        '''
        Dictionary for message headers
        n:nickname
        d:decision
        '''
        data = message.split(" ")
        if data[0] == "n":
            if accept["n"]:
                print(self.request.remote_ip, ":", message)
                if data[1] not in usernames.values():
                    usernames[self]=data[1]
                    info = jsonED.readFromJson()
                    info["players"][data[1]] = {}
                    info["players"][data[1]]["decisions"] = False
                    info["players"][data[1]]["currentDecision"] = False
                    jsonED.write2json(info)
                    self.write_message("USERNAME OK")
                else:
                    self.write_message("USERNAME TAKEN")
            else:
                self.write_message("USERNAME NOT_ACCEPTING")

        elif data[0] == "d":
            if accept["d"]:
                print(self.request.remote_ip, ":", message)
                name = usernames[self]
                info = jsonED.readFromJson()
                info["players"][name]["decision"] = data[1]
                info["players"][name]["currentDecision"] = True
                jsonED.write2json(info)
                self.write_message("DECISION OK")
            else:
                self.write_message("DECISION NOT_ACCEPTING")

        elif data[0] == "continue":
            info = jsonED.readFromJson()
            info["continue"] = True
            jsonED.write2json(info)
            print(self.request.remote_ip, ":", message)

        else:
            self.write_message("INVALID INPUT")

    def on_close(self):
        print(self.request.remote_ip, "Disconnected")
        connections.remove(self)
        try:
            info = jsonED.readFromJson()
            del info["players"][usernames[self]]
            jsonED.write2json(info)

            del usernames[self]

        except KeyError:
            #player didn't enter the nickname and has diconnected
            pass

class adminWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("Admin connected")

    def on_message(self, message):
        data = message.split(" ")
        if data[0] == "sendToAll":
            dataToSend = " ".join(data[1:])
            send_to_all(dataToSend)
            print("Sending message from admin: ", dataToSend)
            self.write_message("Sending message")
        
        elif data[0] == "sendToUser":
            for key, value in usernames.items():
                if value == data[1]:
                    websocket = key
                    dataToSend = " ".join(data[2:])
                    websocket.write_message(dataToSend)
                    self.write_message("Sending message")
                    break

        elif data[0] == "changeAccept":
            #example: changeAccept d True
            accept[data[1]] = data[2] == "True"
            print("Changing accept", data[1], "to", data[2])
            self.write_message(str(accept))
        
        elif data[0] == "print":
            if data[1]=="usernames":
                usernamesStr= " ".join(usernames.values())
                self.write_message(usernamesStr)
        
        elif data[0]=="changeContinue":
            info = jsonED.readFromJson()
            info["continue"]=True if data[1]=="True" else False
            jsonED.write2json(info)
            self.write_message("Continue changed")

        elif data[0]=="resetDecisions":
            info = jsonED.readFromJson()
            for player in info["players"]:
                info["players"][player]["currentDecision"] = False
            jsonED.write2json(info)
            self.write_message("Decisions reset")
        
        elif data[0]=="disconnectEverybody":
            disconnectEverybody()
            self.write_message("Everybody disconnected")


    def on_close(self):
        print("Admin disconnected")


class WebServer(tornado.web.Application):
    def __init__(self):
        basedir = os.path.dirname(__file__)
        handlers=[
            (r"/", IndexRequestHandler),
            (r"/client.js", ClientJsRequestHandler),
            (r"/graphics/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(basedir, "graphics")}),
            (r"/scripts/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(basedir, "scripts")}),
            (r"/stylesheets/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(basedir, "stylesheets")}),
            (r"/socketserver", normalWebSocket),
            (r"/adminwebsocket", adminWebSocket)
        ]

        define('port', default=8888, help='port to listen on')
        define('ip', default="localhost", help='ip to listen on')
        define("websocket_max_message_size", default=128, help="max length in bytes of the socket message")

        jsonED.createJson()
        info = jsonED.readFromJson()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 1))
            info["ip"] = s.getsockname()[0]
        except Exception:
            info["ip"] = "127.0.0.1"
        finally:
            s.close()
        info["port"] = options.port
        jsonED.write2json(info)

        super().__init__(handlers, websocket_max_message_size=options.websocket_max_message_size)

    def run(self, port):
        print("starting server at port:", port)
        self.listen(port)
        tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    webserver = WebServer()
    
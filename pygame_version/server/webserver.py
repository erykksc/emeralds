# __init__.py
import tornado
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from tornado import websocket

import json
import os
import jsonE_D


define('port', default=8888, help='port to listen on')
define('ip', default="0.0.0.0", help='ip to listen on')
define("websocket_max_message_size", default = 128, help="max length in bytes of the socket message")

connections=[]

accept={
    "n":True,
    "d":True
}

#ADMIN FUNCTIONS
def send_to_all(message):
    print(connections)
    for connection in connections:
        connection.write_message(message)

class IndexRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(200)
        self.render("static/index.html")

class ClientJsRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/client.js")

class normalWebSocket(tornado.websocket.WebSocketHandler):
    usernames={}

    def open(self):
        print("Connection")
        connections.append(self)
 
    def on_message(self, message):
        '''
        Dictionary for message headers
        n:nickname
        d:choice
        '''
        data = message.split(" ")
        if data[0] == "n":
            if accept["n"]:
                print(self.request.remote_ip, ":", message)
                if data[1] not in self.usernames.values():
                    self.usernames[self]=data[1]
                    info = jsonE_D.readFromJson()
                    info[data[1]]=False
                    jsonE_D.write2json(info)
                    self.write_message("OK")
                else:
                    self.write_message("taken")
            else:
                self.write_message("not accepting")
        elif data[0]=="d":
            if accept["d"]:
                print(self.request.remote_ip, ":", message)
                info = jsonE_D.readFromJson()
                name = self.usernames[self]
                info[name]=data[1]
                jsonE_D.write2json(info)
                self.write_message("OK")
            else:
                self.write_message("server is not accepting usernames at the moment")
        else:
            self.write_message("invalid input")
 
    def on_close(self):
        connections.remove(self)
        try:
            del self.usernames[self]
        except KeyError:
            #player didn't enter the nickname and has diconnected
            pass
class adminWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print("Admin connected")
 
    def on_message(self, message):
        data = message.split(" ")
        if data[0] == "sendToAll":
            send_to_all(data[1])
            print("Sending message from admin: ", data[1])
            self.write_message("Sending message")
        if data[0] == "changeAccept":
            #example: changeAccept d True
            accept[data[1]]= True if data[2]==True else False
            print(bool(data[2]))
            print("Changing accept", data[1], "to", data[2])
            self.write_message(str(accept))
 
    def on_close(self):
        print("Admin disconnected")
 
def main():
    """Construct and serve the tornado application."""
    jsonE_D.createJson()
    basedir = os.path.abspath("")
    handlers=[
        (r"/", IndexRequestHandler),
        (r"/client.js", ClientJsRequestHandler),
        (r"/graphics/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(basedir, "graphics")}),
        (r"/scripts/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(basedir, "scripts")}),
        (r"/socketserver", normalWebSocket),
        (r"/adminwebsocket", adminWebSocket)
    ]
    app = Application(handlers, options.websocket_max_message_size)
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()

if __name__=="__main__":
    main()
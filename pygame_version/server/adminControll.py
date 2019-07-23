from websocket import create_connection


commands = ("changeAccept", "sendToAll")

IP="192.168.1.136"
PORT="8888"

url = "ws://"+IP+":"+PORT+"/adminwebsocket"

ws = create_connection(url)
print("Client connected to:", url)

def send2Server(message):
    ws.send(message)

while True:
    inp = input("")
    if inp.split(" ")[0] in commands:
        send2Server(inp)
        print(ws.recv())
    elif inp=="help":
        print(commands)
    else:
        print("Unknown command")


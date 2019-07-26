from websocket import create_connection

commands = ("changeAccept", "sendToAll", "print", "sendToUser", "setContinue", "resetDecisions")
commandsDetails ={
    "changeAccept" : ["argument 1: n/d (nickname/ decision", "argument 2: True/False"],
    "sendToAll" : ["argument 1: Message to send to everyone connected"],
    "print" : ["argument 1: usernames"],
    "sendToUser" : ["argument 1: Username", "argument 2: messsage"],
    "setContinue" : ["argument 1: True/False"],
    "resetDecisions" : []
}

IP="192.168.1.136"
PORT="8888"

url = "ws://"+IP+":"+PORT+"/adminwebsocket"

ws = create_connection(url)
print("Client connected to:", url)

def send2Server(message):
    ws.send(message)

while True:
    inp = input("> ")
    inpArr=inp.split(" ")
    if inpArr[0] in commands:
        send2Server(inp)
        print("< ", ws.recv(), sep="")
    elif inpArr[0]=="help":
        if len(inpArr)==1:
            for command in commands:
                print(command)
        else:
            for argument in commandsDetails[inpArr[1]]:
                print(argument)
    else:
        print("Unknown command")


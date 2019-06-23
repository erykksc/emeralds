import json

def write2json(dict):
    with open('game_state.json', 'w') as f:
        json.dump(dict, f, indent=4)

def readFromJson():
    with open('game_state.json') as f:
        return json.load(f)

def updatePair(key, value):
    file = readFromJson()
    file[key]=value
    write2json(file)

def readValue(key):
    file = readFromJson()
    return file[key]

def createJson():
    dict={
        "waiting4Answers": False,
        "ready2Continue": False,
        "state": 0, #0- decisions, 1 - going back, 2- reveal, 3-consequences, 4-kill
        "players": {},
        "tilePath": [],
        "traps": [],
        "killed_by": "nothing",
        "roundNum": 0,
        "numOfRounds": 5,
        "gems4GoingBack": 0,
        "relicts4GoingBack": [],
        "removedCards":[],
        "playerCount": 0
    }
    with open('game_state.json', 'w') as f:
        json.dump(dict, f, indent=4)

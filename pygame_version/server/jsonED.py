import os
import json
import time

FILE_NAME = "players_info.json"

basedir = os.path.dirname(os.path.dirname(__file__))

def write2json(dic):
    with open(os.path.join(basedir, FILE_NAME), 'w') as f:
        dic["last_update"] = time.asctime(time.localtime(time.time()))
        json.dump(dic, f, indent=4)

def readFromJson():
    with open(os.path.join(basedir, FILE_NAME)) as f:
        return json.load(f)

def updatePair(key, value):
    file = readFromJson()
    file[key]=value
    write2json(file)

def readValue(key):
    file = readFromJson()
    return file[key]

def createJson():
    dic = {
        "last_update" : 0,
        "ip":"",
        "port":"",
        "continue" : False,
        "players" : {}
    }
    with open(os.path.join(basedir, FILE_NAME), 'w') as file:
        json.dump(dic, file, indent=4)

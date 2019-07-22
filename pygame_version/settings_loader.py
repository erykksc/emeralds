import json

def write2settings(dict):
    with open('settings/emeralds_settings.json', 'w') as f:
        json.dump(dict, f, indent=4)

def readSettings():
    with open('settings/emeralds_settings.json') as f:
        return json.load(f)

def updatePair(key, value):
    file = readFromJson()
    file[key]=value
    write2settings(file)

def readValue(key):
    file = readFromJson()
    return file[key]

def createJson():
    dict={
        "resolution": (800, 600),
        "fullscreen": False,
        "fontStyle": "Comic Sans MS",
        "fontSize": 30,
        "fontColor": (255, 255, 255),
        "game_settings":{
            BASE_TILES_NAMES_GLOBAL = [['base', 'base'], ['base', 'base'], ['base', 'base'], ['base', 'base'], ['base', 'base'], ['base', 'base']],
            WIDTH_WHOLE_MAP_GLOBAL = 8,
            HEIGHT_WHOLE_MAP_GLOBAL = 6,
            RULES_GLOBAL = "Rules:\nRule 1\nRule 2\nRule 3",
            FPS=60,
            NUM_OF_PLAYER_SKINS = 8
            }
        }
    write2settings(dict)

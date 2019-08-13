import os
import json
import emeralds


BASE_DIR = os.path.abspath("")

try:
    with open(os.path.join(BASE_DIR, "launch_settings.json")) as f:
        settings = json.load(f)
except:
    with open(os.path.join(BASE_DIR, "launch_settings.json"), "w") as f:
        settingsDict = {
            "resolution": [800, 600],
            "fullscreen" : False,
            "num_of_rounds" : 5,
            "texture_pack" : "pola"
        }
        json.dump(settingsDict, f, indent=4)
        settings = settingsDict


game = emeralds.Emeralds(numOfRounds=settings["num_of_rounds"], resolution=settings["resolution"], fullscreen=settings["fullscreen"], graphics=settings["texture_pack"])

game.main()

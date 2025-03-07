import requests
import os
import base64
from json import loads

def getPlayerData(Folder):
    if os.path.exists(Folder):
        Names = list()
        for file in os.listdir(Folder):
            if file.endswith(".dat_old"):
                continue
            if file.endswith(".dat"):
                uuid = file.split('.')[0]  # Extrahiere die UUID aus dem Dateinamen
                try:
                    response = requests.get(
                        f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}",
                        allow_redirects=True  # Standardmäßig aktiviert, explizit angegeben zur Klarheit
                    )
                    response.raise_for_status()  # Überprüfe, ob die Anfrage erfolgreich war
                    jsonData = response.json()
                    Names.append([jsonData["name"], loads(base64.b64decode(jsonData["properties"][0]["value"]).decode("utf-8"))["textures"]["SKIN"]["url"], uuid])
                except:
                    print("Error while fetching data for UUID:", uuid)
                    Names.append([jsonData["name"], loads(base64.b64decode(jsonData["properties"][0]["value"]).decode("utf-8"))["textures"]["SKIN"]["url"], uuid])

        return Names
    return []
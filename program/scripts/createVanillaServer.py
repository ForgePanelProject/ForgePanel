import json
import requests
from os import path
def download(MinecraftVersion, ServerPath, Fabric):
    response = requests.get("https://raw.githubusercontent.com/ForgePanelProject/ForgePanel/refs/heads/main/webdata/VanillaDownloadLinks.json")
    if response.status_code == 200:
        VersionList = response.json()
        server = requests.get(VersionList[MinecraftVersion])
        if server.status_code == 200:
            with open(ServerPath+"/server.jar", "wb") as file:
                file.write(server.content)
                file.close()
                __done__(ServerPath, MinecraftVersion, False)
        else:
            __done__(ServerPath, MinecraftVersion, True)
    else:
        __done__(ServerPath, MinecraftVersion, True)

def __done__(ServerPath, MinecraftVersion, Error):
    print("Done")
    with open(path.join(ServerPath,"downloadResponse.json"), 'w') as file:
        if Error == True:
            json.dump(["0"], file)
        else:
            json.dump(["1", MinecraftVersion, "", "Vanilla"], file)
        file.close()
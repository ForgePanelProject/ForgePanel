import os
import requests
import xml.etree.ElementTree as ET
import json
from subprocess import Popen
from time import sleep

#Fetch/init script
def download(MinecraftVersion, ServerPath):
    url = "https://maven.minecraftforge.net/net/minecraftforge/forge/maven-metadata.xml"
    response = requests.get(url)
    if response.status_code == 200:
        VersionlistRaw = ET.fromstring(response.content)
        versions = [version.text for version in VersionlistRaw.find("versioning").findall("versions/version")]
        ForgeVersions = [v for v in versions if v.startswith(MinecraftVersion+"-")]
        ForgeVersions.sort(reverse=True)  # Sort versions in descending order
        if ForgeVersions:
            NewestForgeVersion = ForgeVersions[0]  # The first version in the sorted list
            print(ForgeVersions[0])
            __downloadForgeInstaller__(NewestForgeVersion, ServerPath, MinecraftVersion)
        else:
            print(f"No Forge versions found for Minecraft {MinecraftVersion}.")
            __done__(ServerPath, MinecraftVersion, NewestForgeVersion, True)
    else:
        print("Failed to fetch Forge versions.")
        __done__(ServerPath, MinecraftVersion, NewestForgeVersion, True)


#download script
def __downloadForgeInstaller__(ForgeVersion, ServerPath, MinecraftVersion):
    if not os.path.exists(ServerPath):
        os.makedirs(ServerPath)
    url = fr"https://files.minecraftforge.net/maven/net/minecraftforge/forge/{ForgeVersion}/forge-{ForgeVersion}-installer.jar"
    response = requests.get(url)
    if response.status_code == 200:
        file_path = os.path.join(ServerPath, f"forge-{ForgeVersion}-installer.jar")
        with open(file_path, "wb") as file:
            file.write(response.content)
            file.close()
            print(f"Downloaded {file_path} successfully.")
            print("PreInstall1")
            __install__(ForgeVersion, ServerPath, MinecraftVersion)
    else:
        print(f"Failed to download Forge installer for version {ForgeVersion}")
        __done__(ServerPath, MinecraftVersion, ForgeVersion, True)

def __install__(ForgeVersion, ServerPath, MinecraftVersion):
    print("Install1")
    Popen(f'cd "{ServerPath}" && java -jar forge-{ForgeVersion}-installer.jar --installServer', shell=True)
    print("Install2")
    if checkInstall(os.path.join(ServerPath, f"forge-{ForgeVersion}-installer.jar.log")):
        os.remove(os.path.join(ServerPath, f"forge-{ForgeVersion}-installer.jar"))
        __done__(ServerPath, MinecraftVersion, ForgeVersion, False)


def checkInstall(LogPath):
    while True:
        if os.path.exists(LogPath):
            with open(LogPath, 'r') as log_file:
                content = log_file.read()
                if "The server installed successfully" in content:
                    log_file.close()
                    print("Server installation complete!")
                    sleep(0.5)
                    return True
                elif "There was an error during installation" in content:
                    log_file.close()
                    print("Server installation failed.")
                    return False
        sleep(1)



def __done__(ServerPath, MinecraftVersion, NewestForgeVersion, Error):
    with open(os.path.join(ServerPath,"downloadResponse.json"), 'w') as file:
        if Error == True:
            json.dump(["0"], file)
        else:
            json.dump(["1", MinecraftVersion, NewestForgeVersion, "Forge"], file)
        file.close()


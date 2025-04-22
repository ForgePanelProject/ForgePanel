import requests
from xml.etree import ElementTree as ET
import json
import os
from time import sleep
from subprocess import Popen

def Download(MinecraftVersion, ServerPath):
    URL = 'https://maven.neoforged.net/releases/net/neoforged/neoforge/maven-metadata.xml'
    Response = requests.get(URL)
    VersionlistRaw = ET.fromstring(Response.content)
        # Finding all versions and filtering by Minecraft version
    Versions = VersionlistRaw.findall('./versioning/versions/version')
    for version in reversed(Versions):
        if MinecraftVersion[2:] in version.text:
            LatestVersion = version.text
            if LatestVersion:
                print("Downloading "+version.text+"...")
                __DownloadInstaller__(MinecraftVersion, LatestVersion, ServerPath)
                break
            else:
                print(f"No NeoForge version found for Minecraft {MinecraftVersion}.")
                __Done__(ServerPath, MinecraftVersion, version, True)
                break

# Function to download the installer
def __DownloadInstaller__(MinecraftVersion, version, ServerPath):
    BaseURL = 'https://maven.neoforged.net/releases/net/neoforged/neoforge/'
    InstallerURL = f'{BaseURL}{version}/neoforge-{version}-installer.jar'
    InstallerPath = f'neoforge-{version}-installer.jar'
    if not os.path.exists(ServerPath):
        os.makedirs(ServerPath)
    try:
        response = requests.get(InstallerURL)
    except:
        __Done__(ServerPath, MinecraftVersion, version, True)
    try:
        with open(fr"{ServerPath}\{InstallerPath}", 'wb') as file:
            file.write(response.content)
        print("Installer downloaded successfully!")
        __install__(ServerPath, version, MinecraftVersion)
    except:
        __Done__(ServerPath, MinecraftVersion, version, True)
        print("Download failed!")

def __install__(ServerPath,NeoforgeVersion,MinecraftVersion):
    Popen(f'cd "{ServerPath}" && java -jar neoforge-{NeoforgeVersion}-installer.jar --installServer', shell=True)
    if CheckInstall(os.path.join(ServerPath, f"neoforge-{NeoforgeVersion}-installer.jar.log")):
        os.remove(os.path.join(ServerPath, f"neoforge-{NeoforgeVersion}-installer.jar"))
        __Done__(ServerPath, MinecraftVersion, NeoforgeVersion, False)
        
def CheckInstall(LogPath):
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

def __Done__(ServerPath, MinecraftVersion, NewestNeoforgeVersion, Error):
    print("Done")
    with open(os.path.join(ServerPath,"downloadResponse.json"), 'w') as file:
        if Error == True:
            json.dump(["0"], file)
        else:
            json.dump(["1", MinecraftVersion, NewestNeoforgeVersion, "NeoForge"], file)
        file.close()
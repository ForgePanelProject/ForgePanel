import json
import os

def convertSettingsProperties(Settings, inputPath, outputPath):
# Read settings.json
    with open(inputPath, 'r') as f:
    #modify data
        settings = json.load(f)
        if settings['Gamemode'] == 0:
            settings['Gamemode'] = "survival"
        elif settings['Gamemode'] == 1:
            settings['Gamemode'] = "creative"
        elif settings['Gamemode'] == 2:
            settings['Gamemode'] = "adventure"
        elif settings['Gamemode'] == 3:
            settings['Gamemode'] = "spectator"

        if settings['Difficulty'] == 0:
            settings['Difficulty'] = "peaceful"
        elif settings['Difficulty'] == 1:
            settings['Difficulty'] = "easy"
        elif settings['Difficulty'] == 2:
            settings['Difficulty'] = "normal"
        elif settings['Difficulty'] == 3:
            settings['Difficulty'] = "hard"
    
    # Map settings to server.properties format
    properties = f"""allow-flight={str(settings['AllowFlight']).lower()}
allow-nether={str(settings['AllowNether']).lower()}
broadcast-console-to-ops={str(settings['BroadcastConsoleOP']).lower()}
difficulty={str(settings['Difficulty'])}
enable-command-block={str(settings['CommandBlocks']).lower()}
enforce-whitelist={str(settings['Whitelist']).lower()}
force-gamemode={str(settings['ForceGamemode']).lower()}
function-permission-level={str(settings['FunctionPermissionLevel'])}
gamemode={str(settings['Gamemode'])}
generate-structures={str(settings['Structures']).lower()}
hardcore={str(settings['Hardcore']).lower()}
level-name={settings['LevelName']}
level-type={settings['LevelType']}
max-players={str(settings['MaxPlayers'])}
max-tick-time={str(settings['MaxTickTime'])}
max-world-size={str(settings['MaxWorldSize'])}
motd={settings['MOTD']}
online-mode={str(settings['MS-Auth']).lower()}
player-idle-timeout={str(settings['Timeout'])}
pvp={str(settings['PVP']).lower()}
server-port={str(settings['Port'])}
simulation-distance={str(settings['MaxSimDist'])}
spawn-animals={str(settings['SpawnAnimals']).lower()}
spawn-monsters={str(settings['SpawnMonsters']).lower()}
spawn-npcs={str(settings['SpawnNPCs']).lower()}
spawn-protection={str(settings['SpawnProtection'])}
view-distance={str(settings['MaxViewDist'])}
white-list={str(settings['Whitelist']).lower()}"""
    
    # Write modified data to server.properties
    with open(outputPath, 'w') as f:
        f.write(properties)
#This is a full version of the SettingsProperiesConverter.py script adding more options than ForgePanel is using.
#This script isn't used by ForgePanel.
import json
import os

def main(Settings, inputPath, outputPath):
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
enable-jmx-monitoring={str(settings['EnableJMXMonitoring']).lower()}
enable-query={str(settings['EnableQuery']).lower()}
enable-rcon={str(settings['EnableRCON']).lower()}
enable-status={str(settings['EnableStatus']).lower()}
enforce-whitelist={str(settings['Whitelist']).lower()}
entity-broadcast-range-percentage={str(settings['EntityBroadcastRange'])}
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
network-compression-threshold={str(settings['NetworkCompressionThreshold'])}
online-mode={str(settings['MS-Auth']).lower()}
op-permission-level={str(settings['OPPermissionLevel'])}
player-idle-timeout={str(settings['Timeout'])}
prevent-proxy-connections={str(settings['PreventProxyConnections']).lower()}
pvp={str(settings['PVP']).lower()}
query.port={str(settings['QueryPort'])}
rate-limit={str(settings['RateLimit'])}
rcon.password={settings['RCONPassword']}
rcon.port={str(settings['RCONPort'])}
require-resource-pack={str(settings['RequireResourcePack']).lower()}
resource-pack={settings['ResourcePack']}
resource-pack-prompt={settings['ResourcePackPrompt']}
resource-pack-sha1={settings['ResourcePackSHA1']}
server-port={str(settings['Port'])}
simulation-distance={str(settings['MaxSimDist'])}
spawn-animals={str(settings['SpawnAnimals']).lower()}
spawn-monsters={str(settings['SpawnMonsters']).lower()}
spawn-npcs={str(settings['SpawnNPCs']).lower()}
spawn-protection={str(settings['SpawnProtection'])}
sync-chunk-writes={str(settings['SyncChunkWrites']).lower()}
text-filtering-config={settings['TextFilteringConfig']}
use-native-transport={str(settings['UseNativeTransport']).lower()}
view-distance={str(settings['MaxViewDist'])}
white-list={str(settings['Whitelist']).lower()}"""
    
    # Write modified data to server.properties
    with open(outputPath, 'w') as f:
        f.write(properties)
#Sorry for the terrible code, at least it works. somehow.
from shutil import which as InstallCheck
import customtkinter as ctk
from os import path
from webbrowser import open as OpenURL
java_path = InstallCheck("java")
print(java_path)
if java_path:
    print(java_path)
    from customtkinter import CTkButton, CTkLabel, CTkFrame, CTkEntry, CTkOptionMenu
    from time import sleep
    from PIL import Image
    import subprocess
    import psutil
    from threading import Thread
    from CTkMessagebox import CTkMessagebox
    from scripts.createForgeServer import download as downloadForge
    from scripts.createForgeServer import checkInstall as checkForgeInstall
    from scripts.createNeoForgeServer import download as downloadNeoForge
    from scripts.createNeoForgeServer import checkInstall as checkNeoForgeInstall
    from scripts.createVanillaServer import download as downloadVanilla
    from scripts.SettingsPropertiesConverter import convertSettingsProperties
    from scripts.getPlayerData import getPlayerData
    from re import search as stringSearch
    import platform
    import requests
    import json
    import os
    from shutil import copy as CopyFile
    from shutil import copytree as CopyFolder
    from shutil import rmtree as RemoveFolder
    from shutil import make_archive
    from shutil import unpack_archive
    from shutil import move as MoveFile
    from io import BytesIO
    from types import SimpleNamespace
    import datetime
    
    if platform.system()=="Windows":
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    Server = ""
    FPPath = f"{path.dirname(path.abspath(__file__))}"
    if path.exists(path.join(FPPath,"temp")): RemoveFolder(path.join(FPPath,"temp"))
    with open(path.join(FPPath,"settings.json"), "r") as fpsettings:
        ProgramSettings = json.load(fpsettings)
    with open(path.join(FPPath,"lang",f"{ProgramSettings['lang']}.json"), "r") as langjson:
        lang = json.load(langjson)
    translation = SimpleNamespace(**lang)
    try:
        VERSION_DATA = requests.get("https://raw.githubusercontent.com/ForgePanelProject/ForgePanel/refs/heads/main/webdata/VersionList.json").json()    
        VERSION_DATA = dict(reversed(VERSION_DATA.items()))
        if not path.exists(path.join(FPPath,"LocalWebData")):
            os.makedirs(path.join(FPPath,"LocalWebData"))
        with open(path.join(FPPath,"LocalWebData","VersionList.json"), "w") as file:
            json.dump(VERSION_DATA, file)
    except:
        try:
            print("Failed to get version data")
            if path.exists(path.join(FPPath,"LocalWebData")):
                with open(path.join(FPPath,"LocalWebData","VersionList.json"), "r") as file:
                    VERSION_DATA = json.load(file)
        except:
            GUI = ctk.CTk(fg_color="white")
            GUI.title("ForgePanel - Fatal Error")
            GUI.iconbitmap(path.join(FPPath,"assets","ForgePanel","FP.ico"))
            ErrorLabel = ctk.CTkLabel(GUI, text="Failed to retrive version data from GitHub. \nVisit the documentation for additional details.", font=("Futura", 15))
            ErrorLabel.pack(padx=10, pady=10)
            button = ctk.CTkButton(GUI, text="Close", command=exit())
            button.pack(padx=10, pady=10)
            DocsButton = ctk.CTkButton(GUI, text="Documentation", command=lambda: OpenURL("https://fpp.gitbook.io/fp/troubleshooting/failed-to-retrive-version-data-from-github"))
            GUI.mainloop()

    def UpdateCheck(*args):
        try:
            latest_version = requests.get("https://raw.githubusercontent.com/ForgePanelProject/ForgePanel/refs/heads/main/program/settings.json").json()
            if latest_version['SecretVersion'] > ProgramSettings['SecretVersion']:
                UpdatePopup = CTkMessagebox(
                    title=translation.ForgePanelUpdateNotificationTitle, 
                    message=translation.ForgePanelUpdateNotificationTxt1+ProgramSettings['ForgePanelVersion']+translation.ForgePanelUpdateNotificationTxt2+latest_version['ForgePanelVersion']+translation.ForgePanelUpdateNotificationTxt3+latest_version['Changelog'],
                    icon="info",
                    option_1=translation.OpenUpdatePage,
                    option_2=translation.LaterButtonTxt,
                )
                if UpdatePopup.get() == translation.OpenUpdatePage:
                    OpenURL("https://github.com/ForgePanelProject/ForgePanel/releases")
        except:
            print("Failed to check for updates")
    svmem = psutil.virtual_memory()
    Page = ""
    UIconPath = path.join(FPPath, "assets", "SystemUIcon")
    if not path.exists(path.join(FPPath, "Servers")):
        os.makedirs(path.join(FPPath, "Servers"))
    AllServerList = os.listdir(path.join(FPPath, "Servers"))
    ServerList = [translation.SelectServerEntry]
    for i in range(len(AllServerList)):
        try:
            with open(path.join(FPPath, "Servers", AllServerList[i], "settings.json"), 'r') as file:
                ServerSettings = json.load(file)
            if ServerSettings["installed"]:
                ServerList.append(AllServerList[i])
            if ServerSettings["ForgePanelVersion"] == "b.1.0":
                ServerList.append(AllServerList[i])
                ServerSettings["installed"] = True
                ServerSettings["ForgePanelVersion"] = ProgramSettings["ForgePanelVersion"]

        except: continue
    ListLen = len(ServerList)-1
    if path.exists(path.join(FPPath,"temp")):
        RemoveFolder(path.join(FPPath,"temp"))
    ServerProcess = None
    ServerState = "Offline"
    ServerSoftware = ""
    ctk.set_appearance_mode("light")
    GUI = ctk.CTk(fg_color="white")
    GUI.title("ForgePanel")
    GUI.iconbitmap(path.join(FPPath,"assets","ForgePanel","FP.ico"))
    GUI.geometry("1920x1050")
    GUI.rowconfigure(1, weight=1)
    GUI.columnconfigure(1, weight=1)
    UpdateCheck()

    def ShowSidebarButtons(*args):
        Logo = ctk.CTkImage(Image.open(f'{FPPath}/assets/ForgePanel/FPlogo_512.png'), size=(50, 50))
        FPTxt = CTkLabel(Sidebar, text="ForgePanel", font=("Futura", 30, "bold"), text_color="black")
        FPImg = CTkLabel(Sidebar, image=Logo, text="")
        FPTxt.grid(column=2, row=0, padx=(10,15), pady=(15,0))
        FPImg.grid(column=1, row=0, padx=(15,0), pady=(15,0))
        if Page != "Setup":
            HomeButton.grid_propagate(False)
            HomeButton.configure(width=240, height=45)
            HomeButton.grid_rowconfigure(0, weight=1)
            HomeButton.grid_rowconfigure(2, weight=1)

            HomeButton.grid(column=1, row=2, columnspan=2, padx=8, pady=(60,0))
            HomeButtonImg.grid(row=1, column=0, padx=2)
            HomeButtonTxt.grid(row=1, column=1)

            Sidebar.rowconfigure(8, weight=1)
            FeedbackButton.grid_propagate(False)
            FeedbackButton.configure(width=240, height=35)
            FeedbackButton.grid(column=1, row=11, columnspan=2, padx=8, pady=(10,0), sticky="s")
            FeedbackButtonImg.grid(row=1, column=0, padx=2)
            FeedbackButtonTxt.grid(row=1, column=1)

            SettingsButton.grid_propagate(False)
            SettingsButton.configure(width=240, height=35)
            SettingsButton.grid(column=1, row=12, columnspan=2, padx=8, pady=(10,0), sticky="s")
            SettingsButtonImg.grid(row=1, column=0, padx=2)
            SettingsButtonTxt.grid(row=1, column=1)
            VersionLabel.grid(column=1, columnspan=2, row=13, pady=(10,20), sticky="s")
            if Server != "":
                DashboardButton.grid_propagate(False)
                DashboardButton.configure(width=240, height=45)
                DashboardButton.grid_rowconfigure(0, weight=1)
                DashboardButton.grid_rowconfigure(2, weight=1)

                DashboardButton.grid(column=1, row=3, columnspan=2, padx=8, pady=(10,0))
                DashboardButtonImg.grid(row=1, column=0, padx=2)
                DashboardButtonTxt.grid(row=1, column=1)

                ConsoleButton.grid_propagate(False)
                ConsoleButton.configure(width=240, height=45)
                ConsoleButton.grid_rowconfigure(0, weight=1)
                ConsoleButton.grid_rowconfigure(2, weight=1)

                ConsoleButton.grid(column=1, row=4, columnspan=2, padx=8, pady=(10,0))
                ConsoleButtonImg.grid(row=1, column=0, padx=2)
                ConsoleButtonTxt.grid(row=1, column=1)

                ConfigButton.grid_propagate(False)
                ConfigButton.configure(width=240, height=45)
                ConfigButton.grid_rowconfigure(0, weight=1)
                ConfigButton.grid_rowconfigure(2, weight=1)

                ConfigButton.grid(column=1, row=5, columnspan=2, padx=8, pady=(10,0))
                ConfigButtonImg.grid(row=1, column=0, padx=2)
                ConfigButtonTxt.grid(row=1, column=1)

                ServerDirButton.grid_propagate(False)
                ServerDirButton.configure(width=240, height=45)
                ServerDirButton.grid_rowconfigure(0, weight=1)
                ServerDirButton.grid_rowconfigure(2, weight=1)

                ServerDirButton.grid(column=1, row=6, columnspan=2, padx=8, pady=(10,0))
                ServerDirButtonImg.grid(row=1, column=0, padx=2)
                ServerDirButtonTxt.grid(row=1, column=1)

                PlayersButton.grid_propagate(False)
                PlayersButton.configure(width=240, height=45)
                PlayersButton.grid(column=1, row=7, columnspan=2, padx=8, pady=(10,0))
                PlayersButtonImg.grid(row=1, column=0, padx=2)
                PlayersButtonTxt.grid(row=1, column=1)

                Sidebar.rowconfigure(9, weight=1)

                # Status frame moves down one row
                StatusFrame.grid(column=1, row=10, columnspan=2, padx=8, pady=(10,0), sticky="s")
                with open(path.join(FPPath, "Servers", Server, "settings.json"), 'r') as file:
                    ServerSettings = json.load(file)
                if ServerSettings["Whitelist"] == True:
                    WhitelistButton.grid_propagate(False)
                    WhitelistButton.configure(width=240, height=45)
                    WhitelistButton.grid(column=1, row=8, columnspan=2, padx=8, pady=(10,0), sticky="n")
                    WhitelistButtonImg.grid(row=1, column=0, padx=2)
                    WhitelistButtonTxt.grid(row=1, column=1)

    def DeletePageContent(*args):
        for widget in ContentFrame.winfo_children():
            widget.grid_forget()
        for widget in Sidebar.winfo_children():
            widget.grid_forget()
        try:
            VersionBar.grid_forget()
        except: pass
        ContentFrame.columnconfigure(0, weight=0)
        ContentFrame.columnconfigure(1, weight=0)
        ContentFrame.columnconfigure(2, weight=0)
        ContentFrame.columnconfigure(3, weight=0)
        ContentFrame.columnconfigure(4, weight=0)
        ContentFrame.columnconfigure(5, weight=0)
        ContentFrame.columnconfigure(6, weight=0)
        ContentFrame.rowconfigure(0, weight=0)
        ContentFrame.rowconfigure(1, weight=0)
        ContentFrame.rowconfigure(2, weight=0)
        ShowSidebarButtons()

    def HomePageLoad(*args):
        global Page
        Page = "Home"
        DeletePageContent()
        ContentFrame.grid_columnconfigure(1, weight=1)
        ContentFrame.grid_columnconfigure(4, weight=1)
        Title.configure(text=translation.HomePageTitle)
        WelcomeTxt.grid(column=2, row=0, padx=10, pady=(75,25), columnspan=2)
        if ListLen >= 1:
            ChooseServerTxt.grid(column=2, row=1, padx=10)
            ChooseServerMenu.grid(column=2, row=2, padx=10, pady=5)
            ChooseServerButton.grid(column=2, row=3, padx=10)
            CreateServerTxt.grid(column=3, row=1, padx=10)
            CreateServerEntry.grid(column=3, row=2, padx=10, pady=5)
            CreateServerButton.grid(column=3, row=3, padx=10)
        else:
            CreateServerTxt.grid(column=2, row=1, padx=10, columnspan=2)
            CreateServerEntry.grid(column=2, row=2, padx=10, pady=5, columnspan=2)
            CreateServerButton.grid(column=2, row=3, padx=10, columnspan=2)
            HelpHomeButton.grid(column=2, row=4, padx=10, pady=7, columnspan=2)

    def DashboardPageLoad(*args):
        global Page
        global scrollframe
        Page = "Dashboard"
        with open(path.join(FPPath, "Servers", Server, "settings.json"), 'r') as file:
            ServerSettings = json.load(file)
        DeletePageContent()
        Title.configure(text=Server+" - "+translation.DashboardPageTitle)
        ContentFrame.columnconfigure(0, weight=1)
        ContentFrame.rowconfigure(0, weight=1)

        # Create scrollable frame for widgets
        scrollframe = ctk.CTkScrollableFrame(ContentFrame, fg_color="white")
        scrollframe.grid(row=0, column=0, sticky="nsew")

        # Server Info Widget
        info_frame = ctk.CTkFrame(scrollframe, fg_color="grey95", width=295, height=180)
        info_frame.grid_propagate(False)
        info_frame.grid(row=0, column=0, padx=15, pady=20)
        info_frame.grid_columnconfigure(0, weight=1)

        CTkLabel(info_frame, text=f"{ServerSettings['MinecraftVersion']} {ServerSettings['Software']}", font=("Futura", 30,"bold")).grid(row=0, column=0, pady=5)
        CTkButton(info_frame, text=translation.ResetButtonTxt, width=245, fg_color="red", hover_color="red3", command=lambda: ResetChangeServerPage(False,True)).grid(row=2, column=0, padx=5, pady=5)
        CTkButton(info_frame, text=translation.ChangeButtonTxt, width=245, fg_color="red", command=lambda: ResetChangeServerPage(True,True)).grid(row=1, column=0, padx=5, pady=5)
        CTkButton(info_frame, text=translation.DeleteButtonTxt, width=245, fg_color="red", hover_color="red3", command=lambda: ResetChangeServerPage(False,False)).grid(row=3, column=0, padx=5, pady=5)

        # Documentation Widget
        docs_frame = CTkFrame(scrollframe, fg_color="grey95", width=295, height=180)
        docs_frame.grid_propagate(False)
        docs_frame.grid(row=0, column=2, padx=15, pady=20)
        docs_frame.grid_columnconfigure(0, weight=1)

        CTkLabel(docs_frame, text=translation.NeedHelpTxt, font=("Futura", 30, "bold")).grid(row=0, column=0, pady=5)
        CTkButton(docs_frame, text=translation.DocumentationTxt, command=lambda: OpenURL("https://fpp.gitbook.io/fp/")).grid(row=1, column=0, pady=10)

        DiskFrame = CTkFrame(scrollframe, fg_color="grey95", width=295, height=180)
        DiskFrame.grid_propagate(False)
        DiskFrame.columnconfigure(0, weight=1)
        DiskFrame.columnconfigure(2, weight=1)

        '''RAMFrame.grid(column=0, row=0, sticky="nsew")
        CPUFrame.grid(column=1, row=0, sticky="nsew")'''
        DiskFrame.grid(row=0, column=1, padx=15, pady=20)
        disk_usage = get_directory_size(path.join(FPPath, "Servers", Server))
        DiskTitleLabel = CTkLabel(DiskFrame, text="Storage", font=("Futura", 30, "bold"))
        DiskTitleLabel.grid(column=1, row=1, pady=5)
        DiskLabel = CTkLabel(DiskFrame, text="0 MB", font=("Futura", 25), text_color="black")
        DiskLabel.grid(column=1, row=2, pady=10)
        DiskLabel.configure(text=f"{disk_usage:.1f} MB")

    def ResetChangeServerPage(VersionChange, ShowKeepBoxes):
        global keep_config
        global keep_world
        global keep_mods
        global cancel_button
        global continue_button
        global warning_label
        DeletePageContent()
        ContentFrame.grid_columnconfigure(1, weight=1)
        ContentFrame.grid_columnconfigure(4, weight=1)
        
        warning_label = CTkLabel(ContentFrame, text=translation.WarningServerDelete, 
                            text_color="red", font=("Futura", 25, "bold"))
        warning_label.grid(row=0, column=2, columnspan=2, pady=(75,15))
        
        # Checkboxes for keeping components
        if ShowKeepBoxes:
            keep_world_var = ctk.BooleanVar()
            keep_world = ctk.CTkCheckBox(ContentFrame, text=translation.KeepWorldTxt, variable=keep_world_var)
            keep_world.grid(row=1, column=2, columnspan=2, pady=5)
            
            keep_config_var = ctk.BooleanVar()
            keep_config = ctk.CTkCheckBox(ContentFrame, text=translation.KeepConfigsTxt, variable=keep_config_var)
            keep_config.grid(row=2, column=2, columnspan=2, pady=5)
            
            keep_mods_var = ctk.BooleanVar()
            keep_mods = ctk.CTkCheckBox(ContentFrame, text=translation.KeepModsTxt, variable=keep_mods_var)
            keep_mods.grid(row=3, column=2, columnspan=2, pady=5)
        
        # Action buttons
        continue_button = CTkButton(ContentFrame, text=translation.ContinueAnyway, command=lambda: ExecuteReset(keep_world_var.get(), keep_config_var.get(), keep_mods_var.get(), VersionChange, False, [warning_label, keep_world, keep_config, keep_mods, continue_button, cancel_button]) if ShowKeepBoxes else ExecuteReset(False, False, False, False, True, [warning_label, continue_button, cancel_button]), fg_color="red", hover_color="red3")
        continue_button.grid(row=4, column=2, pady=30, padx=7)
        
        cancel_button = CTkButton(ContentFrame, text=translation.Cancel, command=DashboardPageLoad)
        cancel_button.grid(row=4, column=3, pady=30, padx=7)
        

    def ExecuteReset(keep_world, keep_config, keep_mods, VersionChange, Delete, widgets):
        global Page
        global Server
        Page = "Setup"
        with open(path.join(FPPath, "Servers", Server, "settings.json"), 'r') as file:
            ServerSettings = json.load(file)
        if not Delete:
            server_path = path.join(FPPath, "Servers", Server, "Server")
            temp_backup_path = path.join(FPPath, "temp", Server, "temp_backup")
            if not path.exists(temp_backup_path):
                os.makedirs(temp_backup_path, exist_ok=True)

            # Backup selected components first
            if keep_world:
                world_files = [f for f in os.listdir(server_path) if f.startswith("world")]
                for f in world_files:
                    CopyFolder(path.join(server_path, f), path.join(temp_backup_path, f))
                    
            if keep_config and path.exists(path.join(server_path, "config")):
                CopyFolder(path.join(server_path, "config"), path.join(temp_backup_path, "config"))
                
            if keep_mods and path.exists(path.join(server_path, "mods")):
                CopyFolder(path.join(server_path, "mods"), path.join(temp_backup_path, "mods"))
        else:
            server_path = path.join(FPPath, "Servers", Server)

        # Delete all files in server directory
        for item in os.listdir(server_path):
            item_path = path.join(server_path, item)
            if path.isfile(item_path):
                os.remove(item_path)
            elif path.isdir(item_path):
                RemoveFolder(item_path)

        # Restore backed up components
        if not Delete:
            if keep_world:
                for f in world_files:
                    CopyFolder(path.join(temp_backup_path, f), path.join(server_path, f))
                    
            if keep_config:
                CopyFolder(path.join(temp_backup_path, "config"), path.join(server_path, "config"))
                
            if keep_mods:
                CopyFolder(path.join(temp_backup_path, "mods"), path.join(server_path, "mods"))

            # Clean up temp backup
            RemoveFolder(temp_backup_path)
        if not Delete:
            CopyFile(fr'{FPPath}/assets/ForgePanel/server-icon.png', f"{path.join(FPPath, "Servers", Server, "Server", "server-icon.png")}")
            with open(fr'{FPPath}/Servers/{Server}/Server/eula.txt', 'w') as file:
                file.write("eula = true")
            if VersionChange:
                DeletePageContent()
                VersionBar.grid(column=1,row=1,sticky="nesw")
            else:
                CreateServer(ServerSettings["MinecraftVersion"], ServerSettings["Software"])
        else:
            RemoveFolder(server_path)
            global ListLen
            global ServerList
            AllServerList = os.listdir(path.join(FPPath, "Servers"))
            ServerList = [translation.SelectServerEntry]
            for i in range(len(AllServerList)):
                try:
                    with open(path.join(FPPath, "Servers", AllServerList[i], "settings.json"), 'r') as file:
                        ServerSettings = json.load(file)
                    if ServerSettings["installed"]:
                        ServerList.append(AllServerList[i])
                    if ServerSettings["ForgePanelVersion"] == "b.1.0":
                        ServerList.append(AllServerList[i])
                        ServerSettings["installed"] = True
                        ServerSettings["ForgePanelVersion"] = ProgramSettings["ForgePanelVersion"]

                except: continue
            ListLen = len(ServerList)-1
            if path.exists(path.join(FPPath,"temp")):
                RemoveFolder(path.join(FPPath,"temp"))
            Server = ""
            for widget in widgets:
                widget.grid_forget()
            ChooseServerMenu.configure(values=ServerList)
            ChooseServerMenu.set(translation.SelectServerEntry)
            DeletePageContent()
            HomePageLoad()

    def ConsolePageLoad(*args):
        global Page
        Page = "Console"
        DeletePageContent()
        Title.configure(text=Server+" - "+translation.ConsoleTitle)
        ContentFrame.columnconfigure(0, weight=1)
        ContentFrame.columnconfigure(1, weight=1)
        ContentFrame.columnconfigure(2, weight=1)
        ContentFrame.columnconfigure(3, weight=1)
        ContentFrame.columnconfigure(4, weight=1)
        ContentFrame.columnconfigure(5, weight=1)
        ContentFrame.rowconfigure(1, weight=1)
        ConsoleOutput.grid(row=1, column=0, sticky="nsew", padx=5, pady=5, columnspan=6)
        CommandEntry.grid(row=2, column=0, padx=5, pady=5, sticky="ew", columnspan=5)
        SendButton.grid(row=2, column=5, padx=5, pady=5, sticky="ew")
    def ConfigPageLoad(*args):
        global Page
        Page = "Config"
        DeletePageContent()
        Title.configure(text=Server+" - "+translation.ConfigTitle)

        # Load current settings
        with open(path.join(FPPath, "Servers", Server, "settings.json"), 'r') as file:
            current_settings = json.load(file)
        ContentFrame.grid_columnconfigure(0, weight=1)
        ContentFrame.rowconfigure(0, weight=1)
        global scrollframe
        scrollframe = ctk.CTkScrollableFrame(ContentFrame, fg_color="white")
        scrollframe.grid(row=0, column=0, sticky="nsew")
        scrollframe.columnconfigure(0, weight=1)
        scrollframe.columnconfigure(1, weight=1)
        scrollframe.columnconfigure(2, weight=1)
        scrollframe.columnconfigure(3, weight=1)

        def AutoSave(setting, value, nonone):
            if nonone and value == "":
                return
            with open(path.join(FPPath, "Servers", Server, "settings.json"), 'r') as file:
                settings = json.load(file)
                
            if setting == "Gamemode":
                gamemode_map = {"survival": 0, "creative": 1, "adventure": 2, "spectator": 3}
                settings[setting] = gamemode_map[value]
            elif setting == "Difficulty":
                difficulty_map = {"peaceful": 0, "easy": 1, "normal": 2, "hard": 3}
                settings[setting] = difficulty_map[value]
            elif setting in ["MaxPlayers", "Port", "MaxSimDist", "MaxViewDist", "SpawnProtection", "FunctionPermissionLevel"]:
                settings[setting] = int(value)
            elif setting in ["AllowFlight", "AllowNether", "CommandBlocks", "Whitelist", "PVP", "Structures", 
                            "SpawnAnimals", "SpawnMonsters", "SpawnNPCs", "MS-Auth", "ForceGamemode", "Hardcore"]:
                settings[setting] = value.lower() == "true"
            elif setting == "MaxRAM":
                settings[setting] = float(value)
            else:
                settings[setting] = value

            with open(path.join(FPPath, "Servers", Server, "settings.json"), 'w') as file:
                json.dump(settings, file)
            
            convertSettingsProperties(settings, 
                                    path.join(FPPath, "Servers", Server, "settings.json"),
                                    path.join(FPPath, "Servers", Server, "Server", "server.properties"))

        # Convert numeric values to string representations
        gamemode_values = {0: "survival", 1: "creative", 2: "adventure", 3: "spectator"}
        difficulty_values = {0: "peaceful", 1: "easy", 2: "normal", 3: "hard"}

        settings_list = [
            ("Gamemode", ["survival", "creative", "adventure", "spectator"], gamemode_values[current_settings["Gamemode"]], "Gamemode"),
            ("Difficulty", ["peaceful", "easy", "normal", "hard"], difficulty_values[current_settings["Difficulty"]], "Difficulty"),
            ("Allow Flight", ["true", "false"], str(current_settings["AllowFlight"]).lower(), "AllowFlight"),
            ("Allow Nether", ["true", "false"], str(current_settings["AllowNether"]).lower(), "AllowNether"),
            ("Command Blocks", ["true", "false"], str(current_settings["CommandBlocks"]).lower(), "CommandBlocks"),
            ("Whitelist", ["true", "false"], str(current_settings["Whitelist"]).lower(), "Whitelist"),
            ("PVP", ["true", "false"], str(current_settings["PVP"]).lower(), "PVP"),
            ("Structures", ["true", "false"], str(current_settings["Structures"]).lower() ,"Structures"),
            ("Spawn Animals", ["true", "false"], str(current_settings["SpawnAnimals"]).lower(), "SpawnAnimals"),
            ("Spawn Monsters", ["true", "false"], str(current_settings["SpawnMonsters"]).lower(), "SpawnMonsters"),
            ("Spawn NPCs", ["true", "false"], str(current_settings["SpawnNPCs"]).lower(), "SpawnNPCs"),
            ("Online Mode", ["true", "false"], str(current_settings["MS-Auth"]).lower(), "MS-Auth"),
            ("Force Gamemode", ["true", "false"], str(current_settings["ForceGamemode"]).lower(), "ForceGamemode"),
            ("Hardcore", ["true", "false"], str(current_settings["Hardcore"]).lower(), "Hardcore"),
            ("Max Players", "entry", str(current_settings["MaxPlayers"]), "MaxPlayers"),
            ("Port", "entry", str(current_settings["Port"]), "Port"),
            ("Simulation Distance", "entry", str(current_settings["MaxSimDist"]), "MaxSimDist"),
            ("View Distance", "entry", str(current_settings["MaxViewDist"]), "MaxViewDist"),
            ("Spawn Protection", "entry", str(current_settings["SpawnProtection"]), "SpawnProtection"),
            ("Function Permission Level", "entry", str(current_settings["FunctionPermissionLevel"]), "FunctionPermissionLevel"),
            ("RAM (in GB)", "entry", str(current_settings["MaxRAM"]), "MaxRAM")
        ]

        row = 0
        col = 0
        for setting, input_type, current_value, setting_key in settings_list:
            frame = CTkFrame(scrollframe, fg_color="grey95", width=295, height=150)
            frame.grid_propagate(False)
            frame.grid(row=row, column=col, pady=10)
            frame.grid_columnconfigure(0, weight=1)

            CTkLabel(frame, text=setting, font=("Futura", 20, "bold")).grid(row=0, column=0, pady=20)
            
            if isinstance(input_type, list):
                menu = CTkOptionMenu(frame, values=input_type,
                                command=lambda x, s=setting_key: AutoSave(s, x, True))
                menu.set(current_value)
                menu.grid(row=1, column=0)
            else:
                entry = CTkEntry(frame)
                entry.insert(0, current_value)
                entry.grid(row=1, column=0, padx=20)
                entry.bind('<KeyRelease>', lambda e, s=setting_key: AutoSave(s, e.widget.get(), True))

            col += 1
            if col > 3:
                col = 0
                row += 1




    def PlayerLimitSlider(*args):
        EasyPlayerLimitTitle.configure(text=f"Player limit: {round(EasyPlayerLimit.get())}")
    def RAMLimitSlider(*args):
        tempvar=EasyRAMLimit.get()
        if str(tempvar)[1:] == ".0":
            EasyRAMLimitTitle.configure(text=f"Max RAM: {round(EasyRAMLimit.get())}GB")
        else:
            EasyRAMLimitTitle.configure(text=f"Max RAM: {EasyRAMLimit.get()}GB")

    def SetupPageLoad(type, *args):
        DeletePageContent()
        if type == "quick":
            ContentFrame.grid_columnconfigure(1, weight=1)
            ContentFrame.grid_columnconfigure(4, weight=1)
            Title.configure(text=Server+" - "+translation.QuickSetupTxt)
            EasyPlayerLimitTitle.grid(row=0, column=2, columnspan=2, pady=20)
            EasyPlayerLimit.set(5)
            EasyPlayerLimit.grid(row=1, column=2, columnspan=2, padx=5)
            EasyRAMLimitTitle.grid(row=2, column=2, columnspan=2, pady=20)
            EasyRAMLimit.set(4)
            EasyRAMLimit.grid(row=3, column=2, columnspan=2, padx=5)

            GamemodeIntuptTitle.grid(row=4, column=2, columnspan=2, pady=20)
            GamemodeInput.grid(row=5, column=2, columnspan=2)
            DifficultyInputTitle.grid(row=6, column=2, columnspan=2, pady=20)
            DifficultyInput.set("Normal")
            DifficultyInput.grid(row=7, column=2, columnspan=2)
            OnlineModeSelectTitle.grid(row=8, column=2, columnspan=2, pady=20)
            OnlineModeSelect.grid(row=9, column=2, columnspan=2)
            WhitelistSelectTitle.grid(row=10, column=2, columnspan=2, pady=20)
            WhitelistSelect.grid(row=11, column=2, columnspan=2)
            NextButton.grid(row=12, column=2, pady=30, padx=7)
            HelpSetUpButton.grid(row=12, column=3, pady=30, padx=7)
        if type == "advanced":
            ChooseServerTxt.configure(text=Server+" - "+translation.AdvancedSetupTxt)

    def OnlineModeWarnPage(*args):
        DeletePageContent()
        ContentFrame.grid_columnconfigure(1, weight=1)
        ContentFrame.grid_columnconfigure(4, weight=1)
        OnlineModeChangeTitle.grid(row=0, column=2, columnspan=2, pady=(75,15))
        OnlineModeChangeButton.grid(row=1, column=2, pady=10, padx=7)
        OnlineModeProceedButton.grid(row=1, column=3, pady=10, padx=7)

    def WhitelistWarnPage(*args):
        DeletePageContent()
        ContentFrame.grid_columnconfigure(1, weight=1)
        ContentFrame.grid_columnconfigure(4, weight=1)
        WhitelistChangeTitle.grid(row=0, column=2, columnspan=2, pady=(75,15))
        WhitelistChangeButton.grid(row=1, column=2, pady=10, padx=7)
        WhitelistAddButton.grid(row=1, column=3, pady=10, padx=7)

    def check(mode, str):
        if mode == "ServerName":
            pattern = r'[^\.a-zA-Z0-9äÄöÖüÜß#\- ]'
        if stringSearch(pattern, str):
            return False
        else:
            return True

    def OnlineModeChange(OnlineMode,*args):
        WhitelistWarnVar = False
        with open(path.join(FPPath, "Servers", Server, "settings.json"), 'r') as file:
            Settings = json.load(file)
            if Settings["Whitelist"]:
                WhitelistWarnVar = True
            if OnlineMode:
                Settings["MS-Auth"] = True
                with open(path.join(FPPath, "Servers", Server, "settings.json"), 'w') as file:
                    json.dump(Settings, file)
                convertSettingsProperties(Settings, path.join(FPPath, "Servers", Server, "settings.json"), path.join(FPPath, "Servers", Server, "Server", "server.properties"))
        if not WhitelistWarnVar:
            DashboardPageLoad()
        else:
            WhitelistWarnPage()

    def WhitelistChange(*args):
        with open(path.join(FPPath, "Servers", Server, "settings.json"), 'r') as file:
            Settings = json.load(file)
            Settings["Whitelist"] = False
        with open(path.join(FPPath, "Servers", Server, "settings.json"), 'w') as file:
            json.dump(Settings, file)
        convertSettingsProperties(Settings, path.join(FPPath, "Servers", Server, "settings.json"), path.join(FPPath, "Servers", Server, "Server", "server.properties"))
        DashboardPageLoad()

    def WhitelistAdd(*args):
        with open(path.join(FPPath, "Servers", Server, "settings.json"), 'r') as file:
            Settings = json.load(file)
            Settings["Whitelist"] = True
        with open(path.join(FPPath, "Servers", Server, "settings.json"), 'w') as file:
            json.dump(Settings, file)
        convertSettingsProperties(Settings, path.join(FPPath, "Servers", Server, "settings.json"), path.join(FPPath, "Servers", Server, "Server", "server.properties"))
        WhitelistPageLoad()
        DashboardPageLoad()

    def HelpSetUpButtonAction(*args):
        OpenURL("https://fpp.gitbook.io/fp/getting-started/set-up-server")

    def QuickConfigButton(*args):
        global OnlineModeWarnVar
        global ServerRam
        ServerRam = int(EasyRAMLimit.get()*1024)
        with open(path.join(FPPath, "Servers", Server, "settings.json"), 'r') as file:
            Settings = json.load(file)
            OnlineModeWarnVar = False
            WhitelistWarnVar = False 
            if GamemodeInput.get() == "Survival":
                Settings["Gamemode"] = 0
            elif GamemodeInput.get() == "Creative":
                Settings["Gamemode"] = 1
            if DifficultyInput.get() == "Peaceful":
                Settings["Difficulty"] = 0
            elif DifficultyInput.get() == "Easy":
                Settings["Difficulty"] = 1
            elif DifficultyInput.get() == "Normal":
                Settings["Difficulty"] = 2
            elif DifficultyInput.get() == "Hard":
                Settings["Difficulty"] = 3
            if OnlineModeSelect.get() == "True":
                Settings["MS-Auth"] = True
            elif OnlineModeSelect.get() == "False":
                Settings["MS-Auth"] = False
                OnlineModeWarnVar = True
            if WhitelistSelect.get() == "True":
                Settings["Whitelist"] = True
                WhitelistWarnVar = True
            Settings["MaxPlayers"] = round(EasyPlayerLimit.get())
            Settings["MaxRAM"] = EasyRAMLimit.get()
        with open(path.join(FPPath, "Servers", Server, "settings.json"), 'w') as file:
            json.dump(Settings, file)
        convertSettingsProperties(Settings, path.join(FPPath, "Servers", Server, "settings.json"), path.join(FPPath, "Servers", Server, "Server", "server.properties"))
        if OnlineModeWarnVar:
            OnlineModeWarnPage()
        else:
            if WhitelistWarnVar:
                WhitelistWarnPage()
            else:
                DashboardPageLoad()

    #Server Page Action
    def ChooseServerButtonAction(*args):
        if ChooseServerMenu.get() != translation.SelectServerEntry:
            global Server
            global ServerSoftware
            global ServerRam
            global ServerProcess
            global ServerState
            global Players
            Server=""
            HomePageLoad()
            ChooseServerButton.configure(state="disabled")
            CreateServerButton.configure(state="disabled")
            if ServerProcess != None:
                ServerProcess.stdin.write("stop\n")
                try:
                    ServerProcess.stdin.flush()
                except: pass
                while ServerProcess.poll() != None:
                    sleep(0.1)
                    continue
                ServerProcess = None
                ServerState = "Offline"

            ConsoleOutput.configure(state="normal")
            ConsoleOutput.delete("1.0", "end")
            ConsoleOutput.configure(state="disabled")
            Server = ChooseServerMenu.get()

            temp_dir = path.join(FPPath, "temp", Server)
            if not path.exists(temp_dir):
                os.makedirs(temp_dir)

            # Get and cache player data
            players_cache_file = path.join(temp_dir, "players.json")
            try:
                Players = getPlayerData(path.join(FPPath, "Servers", Server, "Server", "world", "playerdata"))
            except FileNotFoundError:
                Players = []
            except:
                Players = []
                print("Unknown error getting player data")
            
            with open(players_cache_file, 'w') as f:
                json.dump(Players, f)

            with open(path.join(FPPath, "Servers", Server, "settings.json"), 'r') as file:
                ServerSettings = json.load(file)
                ServerSoftware = ServerSettings["Software"]
                ServerRam = int(ServerSettings["MaxRAM"]*1024)
            print(ServerSoftware)
            ChooseServerButton.configure(state="normal")
            CreateServerButton.configure(state="normal")
            DashboardPageLoad()

    def CreateServerButtonAction(*args):
        if check(mode="ServerName", str=CreateServerEntry.get()):
            ServerNameError = False
            for entry in ServerList:
                if entry == CreateServerEntry.get():
                    ServerNameError = True
            if not ServerNameError:
                if CreateServerEntry.get() != "":
                    global ListLen
                    global Page
                    global Server
                    global ChooseServerMenu
                    Page = "Setup"
                    Server = CreateServerEntry.get()
                    DeletePageContent()
                    ChooseServerMenu = ctk.CTkOptionMenu(ContentFrame, values=ServerList)
                    os.makedirs(fr'{FPPath}/Servers/{Server}/Server')
                    CopyFile(fr'{FPPath}/assets/ForgePanel/server-icon.png', f"{path.join(FPPath, "Servers", Server, "Server", "server-icon.png")}")
                    CreateServerEntry.delete(19, last_index=None)
                    with open(fr'{FPPath}/Servers/{Server}/Server/eula.txt', 'w') as file:
                        file.write("eula = true")
                    VersionBar.grid(column=1,row=1,sticky="nesw")
                    Title.configure(text=Server+translation.ServerCreateTitle)
                    ListLen+=1
            else:
                ErrorTxt.configure(text=translation.ErrorServerNameDuplicate)
                if ListLen < 1:
                    ErrorTxt.grid(row=4, column=2, columnspan=2)
                else:
                    ErrorTxt.grid(row=4, column=3)

        else:
            ErrorTxt.configure(text=translation.ErrorServerNameForbiddenCharacters)
            if ListLen < 1:
                ErrorTxt.grid(row=4, column=2, columnspan=2)
            else:
                ErrorTxt.grid(row=4, column=3)
    def OpenServerDir(*args):
        subprocess.Popen(fr'explorer.exe "{FPPath}\Servers\{Server}\Server"') #Windows exclusive
    def SettingsPageLoad(*args):
        Title.configure(text=translation.SettingsTitle)
        global settings_frame
        DeletePageContent()
        ContentFrame.grid_columnconfigure(0, weight=1)
        ContentFrame.grid_rowconfigure(0, weight=1)
        
        # Create main settings frame
        settings_frame = CTkFrame(ContentFrame, fg_color="white", width=600, height=400)
        settings_frame.grid(column=0, row=0, sticky="nesw")
        settings_frame.grid_columnconfigure(0, weight=1)

        CTkLabel(settings_frame, text=translation.SettingsLangChangeTitle, font=("Futura", 20)).grid(row=0, column=0, pady=10)
        
        # Get available languages from lang folder
        lang_files = [f.split('.')[0] for f in os.listdir(path.join(FPPath, "lang")) if f.endswith('.json')]
        
        def change_language(new_lang):
            ProgramSettings['lang'] = new_lang
            with open(path.join(FPPath, "settings.json"), "w") as settings_file:
                json.dump(ProgramSettings, settings_file)
            CTkMessagebox(title=translation.LangChangeTitle, message=translation.LangChangeInfoTxt)
        
        lang_menu = CTkOptionMenu(
            settings_frame, 
            values=lang_files,
            command=change_language
        )
        lang_menu.set(ProgramSettings['lang'])
        lang_menu.grid(row=1, column=0, pady=10)
        
        #Backups
        def backup():
            if platform.system() == "Windows":
                backup_dir = ctk.filedialog.asksaveasfilename(initialdir=os.path.join(path.expanduser('~'), "Documents"), defaultextension=".fpbackup", filetypes=[("ForgePanel Backup", "*.fpbackup")], title="Select Backup Location", initialfile=f"backup-{str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))}.fpbackup")
            else:
                backup_dir = ctk.filedialog.asksaveasfilename(path.expanduser('~'), defaultextension=".fpbackup", filetypes=[("ForgePanel Backup", "*.fpbackup")], title="Select Backup Location", initialfile=f"backup-{str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))}.fpbackup")
            if backup_dir:
                if path.exists(path.join(FPPath, "temp", "backup")):
                    RemoveFolder(path.join(FPPath, "temp", "backup"))
                os.makedirs(path.join(FPPath, "temp", "backup"))
                CopyFolder(path.join(FPPath, "Servers"), path.join(FPPath, "temp", "backup", "Servers"))
                CopyFile(path.join(FPPath, "settings.json"), path.join(FPPath, "temp", "backup", "settings.json"))
                make_archive(path.join(FPPath, "temp", "backup"), 'zip', path.join(FPPath, "temp", "backup"))
                os.rename(path.join(FPPath, "temp", "backup.zip"), path.join(FPPath, "temp", path.basename(backup_dir)))
                MoveFile(path.join(FPPath, "temp", path.basename(backup_dir)), backup_dir)
                os.startfile(path.dirname(backup_dir))
                RemoveFolder(path.join(FPPath, "temp", "backup"))
        def backupRestore():
            if path.exists(path.join(FPPath, "temp", "backup")):
                RemoveFolder(path.join(FPPath, "temp", "backup"))
            os.makedirs(path.join(FPPath, "temp", "backup"))
            if platform.system() == "Windows":
                backup_file = ctk.filedialog.askopenfilename(initialdir=os.path.join(path.expanduser('~'), "Documents"), defaultextension=".fpbackup", filetypes=[("ForgePanel Backup", "*.fpbackup")], title="Select Backup File")
            else:
                backup_file = ctk.filedialog.askopenfilename(initialdir=os.path.join(path.expanduser('~')), filetypes=[("ForgePanel Backup", "*.fpbackup")], title="Select Backup File")
            if backup_file:
                deleteMessage = CTkMessagebox(title=translation.SettingsBackupImportButtonTxt, message=translation.SettingsRestoreWarnTxt, icon="warning", option_1=translation.Cancel, option_2=translation.ContinueAnyway)
                if deleteMessage.get() == translation.ContinueAnyway:
                    global Server
                    global ListLen

                    Server=""
                    if path.exists(path.join(FPPath, "temp", "backup")):
                        RemoveFolder(path.join(FPPath, "temp", "backup"))
                    os.makedirs(path.join(FPPath, "temp", "backup"))
                    CopyFile(backup_file, path.join(FPPath, "temp", "backup.zip"))
                    unpack_archive(path.join(FPPath, "temp", "backup.zip"), path.join(FPPath, "temp", "backup"))
                    os.remove((path.join(FPPath, "temp", "backup.zip")))
                    with open(path.join(FPPath, "temp", "backup", "settings.json"), 'r') as file:
                        BackupSettings = json.load(file)
                    with open(path.join(FPPath, "settings.json"), 'r') as file:
                        ProgramSettings = json.load(file)
                    
                    if float(BackupSettings["ForgePanelVersion"][2:]) <= float(ProgramSettings["ForgePanelVersion"][2:]):
                        if path.exists(path.join(FPPath, "Servers")):
                            RemoveFolder(path.join(FPPath, "Servers"))
                        if path.exists(path.join(FPPath, "settings.json")):
                            os.remove(path.join(FPPath, "settings.json"))
                        CopyFolder(path.join(FPPath, "temp", "backup", "Servers"), path.join(FPPath, "Servers"))
                        CopyFile(path.join(FPPath, "temp", "backup", "settings.json"), path.join(FPPath, "settings.json"))
                        
                        AllServerList = os.listdir(path.join(FPPath, "Servers"))
                        ServerList = [translation.SelectServerEntry]
                        for i in range(len(AllServerList)):
                            try:
                                with open(path.join(FPPath, "Servers", AllServerList[i], "settings.json"), 'r') as file:
                                    ServerSettings = json.load(file)
                                if ServerSettings["installed"]:
                                    ServerList.append(AllServerList[i])
                                if ServerSettings["ForgePanelVersion"] == "b.1.0":
                                    ServerList.append(AllServerList[i])
                                    ServerSettings["installed"] = True
                                    ServerSettings["ForgePanelVersion"] = ProgramSettings["ForgePanelVersion"]

                            except: continue
                        ListLen = len(ServerList)
                        if path.exists(path.join(FPPath,"temp")):
                            RemoveFolder(path.join(FPPath,"temp"))
                        ChooseServerMenu.configure(values=ServerList)
                        HomePageLoad()
                        if BackupSettings["lang"] != ProgramSettings["lang"]:
                            CTkMessagebox(title=translation.LangChangeTitle, message=translation.LangChangeInfoTxt, icon="info")
                    else:
                        CTkMessagebox(title=translation.SettingsBackupImportButtonTxt, message=translation.SettingsRestoreUncompatibleTxt, icon="cancel")
                        if path.exists(path.join(FPPath,"temp")):
                            RemoveFolder(path.join(FPPath,"temp"))
        CTkLabel(settings_frame, text=translation.SettingsBackupTitle, font=("Futura", 20)).grid(row=2, column=0, pady=10)
        CTkButton(settings_frame, text=translation.SettingsBackupCreateButtonTxt, command=lambda: backup()).grid(row=3, column=0, pady=10)
        CTkButton(settings_frame, text=translation.SettingsBackupImportButtonTxt, command=lambda: backupRestore()).grid(row=4, column=0, pady=10)

    def FeedbackPageLoad(*args):
        OpenURL("https://docs.google.com/forms/d/e/1FAIpQLSdHLa3h43drvhhbmJ7OSV85xlqR5s1Vr8JI4bHtomUEB9zGEA/viewform")
    def PlayersPageLoad(*args):
        global Page
        global PlayerPageFrame
        Page = "Players"
        DeletePageContent()
        Title.configure(text=Server+" - "+translation.PlayersTitle)
        ContentFrame.grid_columnconfigure(0, weight=1)
        ContentFrame.rowconfigure(0, weight=1)

        PlayerPageFrame = ctk.CTkScrollableFrame(ContentFrame, fg_color="white")
        PlayerPageFrame.grid(row=0, column=0, sticky="nsew")
        PlayerPageFrame.grid_columnconfigure(0, weight=1)
        PlayerPageFrame.grid_columnconfigure(1, weight=1)
        PlayerPageFrame.grid_columnconfigure(2, weight=1)
        PlayerPageFrame.grid_columnconfigure(3, weight=1)
        # Load or create banned.json
        banned_file = path.join(FPPath, "Servers", Server, "banned.json")
        if not path.exists(banned_file):
            with open(banned_file, 'w') as f:
                json.dump([], f)
        
        with open(banned_file, 'r') as f:
            banned_players = json.load(f)

        def updatePlayerCache():
            global Players
            Players = getPlayerData(path.join(FPPath, "Servers", Server, "Server", "world", "playerdata"))
            with open(path.join(FPPath, "temp", Server, "players.json"), 'w') as f:
                json.dump(Players, f)
        def handle_ban(player_name):
            if player_name in banned_players:
                banned_players.remove(player_name)
                SendCommandToProcess(ServerProcess, f"/pardon {player_name}")
            else:
                banned_players.append(player_name)
                SendCommandToProcess(ServerProcess, f"/ban {player_name}")
            
            with open(banned_file, 'w') as f:
                json.dump(banned_players, f)
            PlayersPageLoad()

        for i, Player in enumerate(Players):
            row = i // 4
            col = i % 4

            player_frame = CTkFrame(PlayerPageFrame, fg_color="grey95")
            player_frame.grid(row=row, column=col, padx=15, pady=10)
            player_frame.grid_columnconfigure(0, weight=1)
            player_frame.grid_rowconfigure(0, weight=1)
        
            header_frame = CTkFrame(player_frame, fg_color="grey95")
            header_frame.grid(row=0, column=0, pady=10)

            head_url = f"https://mc-heads.net/avatar/{Player[0]}/50"
            response = requests.get(head_url)
            head_image = Image.open(BytesIO(response.content))
            head_photo = ctk.CTkImage(head_image, size=(40, 40))
            CTkLabel(header_frame, image=head_photo, text="").grid(row=0, column=0, padx=5)

            CTkLabel(header_frame, text=Player[0], font=("Futura", 25, "bold")).grid(row=0, column=1, padx=5)

            button_frame = CTkFrame(player_frame, fg_color="grey95")
            button_frame.grid(row=1, column=0, pady=10, padx=5, sticky="s")

            is_banned = Player[0] in banned_players
            ban_button = CTkButton(
                button_frame,
                text=translation.UnbanTxt if is_banned else translation.BanTxt,
                width=75,
                fg_color="green4" if is_banned else "red",
                hover_color="green" if is_banned else "red3",
                command=lambda p=Player[0]: handle_ban(p)
            )
            ban_button.grid(row=0, column=0, padx=5, sticky="sw")

            op_button = CTkButton(
                button_frame,
                text="OP",
                width=75,
                command=lambda p=Player[0]: OperatorPlayer(p, Player[2])
            )
            op_button.grid(row=0, column=1, padx=5, sticky="se")
        Thread(target=updatePlayerCache).start()

    def WhitelistPageLoad(*args):
        def RemovePlayer(player_name):
            with open(path.join(FPPath, "Servers", Server, "Server", "whitelist.json"), 'r') as file:
                Whitelist = json.load(file)
            # Correct iteration to find and remove player
            for i, player in enumerate(Whitelist):
                if player["name"] == player_name:
                    Whitelist.pop(i)
                    break
            with open(path.join(FPPath, "Servers", Server, "Server", "whitelist.json"), 'w') as file:
                json.dump(Whitelist, file)
            WhitelistPageLoad()

        def AddPlayer(player_name):
            try:
                # Get UUID from Mojang API
                response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player_name}")
                if response.status_code == 200:
                    player_data = response.json()
                    uuid = player_data["id"]
                    
                    # Load or create whitelist
                    whitelist_path = path.join(FPPath, "Servers", Server, "Server", "whitelist.json")
                    if path.exists(whitelist_path):
                        with open(whitelist_path, 'r') as file:
                            Whitelist = json.load(file)
                    else:
                        Whitelist = []
                    
                    # Add new player entry
                    Whitelist.append({
                        "uuid": uuid[:8]+"-"+uuid[8:12]+"-"+uuid[12:16]+"-"+uuid[16:20]+"-"+uuid[20:],
                        "name": player_name
                    })
                    
                    # Save updated whitelist
                    with open(whitelist_path, 'w') as file:
                        json.dump(Whitelist, file)
                    
                    WhitelistPageLoad()
                else:
                    print(f"Failed to get UUID for player {player_name}")
            except Exception as e:
                print(f"Error adding player to whitelist: {e}")
        global Page
        global WhiteListFrame
        global AddPlayerFrame
        Page = "Whitelist"
        DeletePageContent()
        Title.configure(text=Server+" - "+translation.WhitelistTitle)
        ContentFrame.grid_columnconfigure(0, weight=1)
        ContentFrame.rowconfigure(0, weight=1)

        WhiteListFrame = ctk.CTkScrollableFrame(ContentFrame, fg_color="white")
        WhiteListFrame.grid(row=0, column=0, sticky="nsew")

        if path.exists(path.join(FPPath, "Servers", Server, "Server", "whitelist.json")):
            with open(path.join(FPPath, "Servers", Server, "Server", "whitelist.json"), 'r') as file:
                Whitelist = json.load(file)
                if Whitelist:
                    for i, player in enumerate(Whitelist):
                        row = i // 4
                        col = i % 4

                        player_frame = CTkFrame(WhiteListFrame, fg_color="grey95")
                        player_frame.grid(row=row, column=col, padx=15, pady=10)
                        player_frame.grid_columnconfigure(0, weight=1)
                        player_frame.grid_rowconfigure(0, weight=1)

                        header_frame = CTkFrame(player_frame, fg_color="grey95")
                        header_frame.grid(row=0, column=0, pady=10)

                        # Use the player name directly since it's a string
                        head_url = f"https://mc-heads.net/avatar/{player["name"]}/50"
                        response = requests.get(head_url)
                        head_photo = ctk.CTkImage(Image.open(BytesIO(response.content)), size=(40, 40))
                        CTkLabel(header_frame, image=head_photo, text="").grid(row=0, column=0, padx=5)

                        CTkLabel(header_frame, text=player["name"], font=("Futura", 25, "bold")).grid(row=0, column=1, padx=5)

                        RemoveButton = CTkButton(player_frame, fg_color="red", hover_color="red3", text=translation.WhitelistRemovePlayerTxt, command=lambda p=player["name"]: RemovePlayer(p))
                        RemoveButton.grid(row=1, column=0, pady=10, padx=5, sticky="s")

        AddPlayerFrame = CTkFrame(Topbar, fg_color="grey95")
        AddPlayerFrame.grid(row=0, column=2, pady=[10,0], sticky="e", padx=[0,20])

        AddPlayerEntry = CTkEntry(AddPlayerFrame)
        AddPlayerEntry.grid(row=0, column=0, pady=10)
        AddPlayerButton = CTkButton(AddPlayerFrame, fg_color="green4", hover_color="green", text=translation.WhitelistAddPlayerTxt, command=lambda: AddPlayer(AddPlayerEntry.get()))
        AddPlayerButton.grid(row=0, column=1, pady=10)


    def OperatorPlayer(Player, UUID, *args):
        opPath = path.join(FPPath, "Servers", Server, "Server", "ops.json")
        with open(opPath, 'r') as file:
            ops = json.load(file)
        with open(opPath, 'w') as file:
            ops.append({"uuid": UUID, "name": Player, "level": 4, "bypassesPlayerLimit": False})
            json.dump(ops, file)

    def PastInstall(*args):
        DeletePageContent()
        ContentFrame.grid_columnconfigure(1, weight=1)
        ContentFrame.grid_columnconfigure(4, weight=1)
        SetupIntroTxt.grid(column=2, row=1, columnspan=2, pady=25)
        SetupIntroButton1.grid(column=2, row=2)
        SetupIntroButton2.grid(column=3, row=2)
        SetupIntroButton2.configure(state="disabled")
        StandardSettings = {
            "MaxRAM":4,
            "MaxPlayers":5,
            "Gamemode":0, #0-Survival,1-Creative,2-Adventure,3-Spectator
            "Difficulty":2, #0-Peaceful,1-Easy,2-Normal,3-Hard
            "Port":25565,

            "MaxSimDist":8,
            "MaxViewDist":8,
            "Nether":True,
            "Structures":True,
            "MOTD":Server+" is a self-hosted §1§lForgePanel §rMinecraft Server",
            "MS-Auth":True,
            "SpawnProtection":0,
            "SpawnMonsters":True,
            "SpawnAnimals":True,
            "SpawnNPCs":True,
            "AllowFlight":False,
            "AllowNether":True,
            "CommandBlocks":True,
            "PVP":True,
            "Whitelist":False,#Including EnforceWhitelist
            "WhitelistPlayers":[],
            "Timeout":0,
            "LogIP":True,
            "Hardcore":False,
            "HideOnlinePlayers":False,
            "ForceGamemode":False,
            "FunctionPermissionLevel":4,
            "BroadcastConsoleOP":True,

            "MaxTickTime":60000,
            "MaxWorldSize":29999984,
            "LevelType":r"minecraft\:normal",
            "LevelName":"world",

            "MinecraftVersion":f"{MinecraftVersion}",
            "Software":ServerSoftware,
            "SettingsVersion":1,
            "ForgePanelVersion":ProgramSettings["ForgePanelVersion"],
            "installed":True
            }
        with open(fr'{FPPath}/Servers/{Server}/settings.json', 'w') as file:
            json.dump(StandardSettings, file)

    def CreateServer(version, versiontype, *args):
        global ServerSoftware
        global MinecraftVersion
        MinecraftVersion = version
        ServerSoftware = versiontype
        DeletePageContent()
        ContentFrame.columnconfigure(0, weight=1)
        ContentFrame.columnconfigure(2, weight=1)
        ContentFrame.rowconfigure(0, weight=1)
        ContentFrame.rowconfigure(2, weight=1)
        if versiontype == "Vanilla":
            ServerSoftware = "Vanilla"
            LoadingTxt = CTkLabel(ContentFrame, text=translation.ServerVanillaDownloadText, text_color="black", font=("Futura", 20))
            LoadingTxt.grid(column=1, row=1)
            print(1)
            sleep(0.1)
            downloadVanilla(version, f"{path.join(FPPath, 'Servers', Server, 'Server')}", False)
            while True:
                sleep(0.5)
                GUI.update()
                if path.exists(f"{path.join(FPPath, 'Servers', Server, 'Server')}/downloadResponse.json"):
                    with open(f"{path.join(FPPath, 'Servers', Server, 'Server')}/downloadResponse.json", "rb") as file:
                        filedata = json.load(file)
                        if filedata[0] == "1":
                            LoadingTxt.grid_forget()
                            PastInstall()
                            break
                        elif filedata[0] == "0":
                                LoadingTxt.configure(text=translation.ServerDownloadErrorText)

        elif versiontype == "Forge":
            ServerSoftware = "Forge"
            LoadingTxt = CTkLabel(ContentFrame, text=translation.ServerForgeDownloadText, text_color="black", font=("Futura", 20))
            LoadingTxt.grid(column=1, row=1)
            sleep(0.1)
            downloadForge(version, f"{path.join(FPPath,'Servers', Server, 'Server')}")
            while not checkForgeInstall or checkForgeInstall == None:
                sleep(0.5)
                GUI.update()
            if checkForgeInstall:
                LoadingTxt.grid_forget()
                PastInstall()

        elif versiontype == "NeoForge":
            ServerSoftware = "NeoForge"
            LoadingTxt = CTkLabel(ContentFrame, text=translation.ServerNeoForgeDownloadText, text_color="black", font=("Futura", 20))
            LoadingTxt.grid(column=1, row=1)
            sleep(0.1)
            downloadNeoForge(version, f"{path.join(FPPath, 'Servers', Server, 'Server')}")
            while not checkNeoForgeInstall or checkNeoForgeInstall == None:
                sleep(0.5)
                GUI.update()
            if checkNeoForgeInstall:
                LoadingTxt.grid_forget()
                PastInstall()
    #    elif versiontype == "Fabric":
    #        PastInstall(loader="fabric")

    #Console functions
    def GetStartupCommand(software):
        with open(path.join(FPPath, 'Servers', Server, 'settings.json'), 'r') as file:
            settings = json.load(file)
            ServerRam = settings["MaxRAM"]
        try:
            with open(path.join(FPPath, "Servers", Server, "Server", "user_jvm_args.txt"), "w") as f:
                f.write(f"-Xmx{int(ServerRam)}G -Xms{int(ServerRam)}G")
        except: pass
        if software == "Forge" or software == "NeoForge":
            return rf'cd "{FPPath}\Servers\{Server}\Server" & run.bat -nogui'
        else:
            return rf'cd "{FPPath}\Servers\{Server}\Server" & java -jar -Xmx{int(ServerRam)}G server.jar -nogui'
    def RunSubprocessAndUpdateOutput(command):
        ProcessInstance = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True, stdin=subprocess.PIPE, encoding="utf-8", errors="replace")
        '''def update_memory_usage():
            while True:
                memory_usage = get_memory_usage(ProcessInstance)
                cpu_usage = get_cpu_usage(ProcessInstance)
                if memory_usage is not None:
                    RAMLabel.configure(text=f"{memory_usage:.0f} MB", text_color="black")
                    CPULabel.configure(text=f"{cpu_usage:.1f}%", text_color="black")
                else:
                    RAMLabel.configure(text="Offline", text_color="red")
                    CPULabel.configure(text="Offline", text_color="red")
                sleep(0.5)'''
        def UpdateOutput(stream, tag):
            global ServerState
            for line in stream:
                try:
                    GUI.after(0, lambda: ConsoleOutput.configure(state="normal"))
                    GUI.after(0, lambda l=line: ConsoleOutput.insert("end", l, tag))
                    GUI.after(0, lambda: ConsoleOutput.see("end"))
                    GUI.after(0, lambda: ConsoleOutput.configure(state="disabled"))
                    if "Done" in line:
                        GUI.after(0, lambda: StatusLabel.configure(text="Online", text_color="green"))
                        ServerState="Online"
                    elif "All dimensions are saved" in line:
                        GUI.after(0, lambda: StatusLabel.configure(text="Offline", text_color="red"))
                        ServerState="Quitting"
                        def endServerProcess():
                            global ServerState
                            sleep(15)
                            ServerState="Offline"
                            ProcessInstance.kill()
                        Thread(target=endServerProcess).start()
                except: pass
            stream.close()
        def UpdateStatus(process):
            while True:
                if process.poll() is not None:
                    try:
                        GUI.after(0, lambda: StatusLabel.configure(text="Offline", text_color="red"))
                    except: pass
                    break
                sleep(1)
        Thread(target=UpdateOutput, args=(ProcessInstance.stdout, "stdout")).start()
        Thread(target=UpdateOutput, args=(ProcessInstance.stderr, "stderr")).start()
        Thread(target=UpdateStatus, args=(ProcessInstance,)).start()
        '''Thread(target=update_memory_usage).start()
        Thread(target=update_memory_usage).start()
        Thread(target=update_disk_usage).start()'''

        return ProcessInstance

    def SendCommandToProcess(process, command):
        global ServerProcess, ServerState
        CommandEntry.delete(0, "end")
        if command in ("start","/start"):
            if ServerState == "Online" or ServerState == "Starting":
                ConsoleOutput.configure(state="normal")
                ConsoleOutput.insert("end", "Server is already running or starting\n", "stderr")
                ConsoleOutput.see("end")
                ConsoleOutput.configure(state="disabled")
                return
            ServerState = "Starting"
            ServerProcess = RunSubprocessAndUpdateOutput(GetStartupCommand(ServerSoftware))
        else:
            if process and process.poll() is None:
                try:
                    process.stdin.write(command + "\n")
                    process.stdin.flush()
                    if command == "stop":
                        ServerState = "Stopping"
                        process.wait()
                        ServerProcess = None
                except:
                    ConsoleOutput.configure(state="normal")
                    ConsoleOutput.insert("end", "Cannot send command - server not running\n", "stderr")
                    ConsoleOutput.see("end")
                    ConsoleOutput.configure(state="disabled")

    def CheckProcessStatus(process, status_label):
        while True:
            if process.poll() is not None:
                status_label.configure(text="Offline", text_color="red")
                break
            sleep(1)

    #Dashboard functions
    '''def get_memory_usage(process):
        try:
            process_info = psutil.Process(process.pid)
            total_memory = process_info.memory_info().rss
            for child in process_info.children(recursive=True):
                total_memory += child.memory_info().rss
            return total_memory / (1024 * 1024)  # In MB
        except psutil.NoSuchProcess:
            return None

    def get_cpu_usage(process):
        try:
            process_info = psutil.Process(process.pid)
            cpu_count = psutil.cpu_count()
            
            # Get CPU usage across all cores and normalize it
            cpu_percent = process_info.cpu_percent() / cpu_count
            
            # Include child processes
            for child in process_info.children(recursive=True):
                cpu_percent += child.cpu_percent() / cpu_count
            
            # Ensure the value stays within 0-100% range
            cpu_percent = min(100, max(0, cpu_percent))
            return cpu_percent
        except psutil.NoSuchProcess:
            return None'''
    def get_directory_size(directory):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = path.join(dirpath, filename)
                total_size += path.getsize(filepath)
        return total_size / (1024 * 1024)
    Topbar = CTkFrame(GUI, border_color="grey95", fg_color="transparent", border_width=2)
    Topbar.grid_propagate(False)
    Topbar.configure(height=75)
    Topbar.columnconfigure(2, weight=1)
    Sidebar = CTkFrame(GUI, fg_color="grey95")
    Sidebar.grid_propagate(False)
    Sidebar.configure(width=256)
    Title = CTkLabel(Topbar, text=translation.HomePageTitle, font=("Futura", 30, "bold"))
    ContentFrame = ctk.CTkFrame(GUI, fg_color="white")

    ContentFrame.grid_propagate(False)
    ContentFrame.configure(width=1280, height=975)
    #Menu Buttons:
    #ServerButton
    HomeButtonIcon = ctk.CTkImage(Image.open(f'{UIconPath}/home.png'), size=(35, 35))
    HomeButton = CTkFrame(Sidebar, fg_color="grey92")
    HomeButtonImg = CTkLabel(HomeButton, image=HomeButtonIcon, text="")
    HomeButtonTxt = CTkLabel(HomeButton, text=translation.HomePageTitle, font=("Futura", 25))
    HomeButton.bind('<Button-1>', HomePageLoad)
    HomeButtonImg.bind('<Button-1>', HomePageLoad)
    HomeButtonTxt.bind('<Button-1>', HomePageLoad)
    #DashboardButton
    DashboardButtonIcon = ctk.CTkImage(Image.open(f'{UIconPath}/dashboard.png'), size=(35, 35))
    DashboardButton = CTkFrame(Sidebar, fg_color="grey92")
    DashboardButtonImg = CTkLabel(DashboardButton, image=DashboardButtonIcon, text="")
    DashboardButtonTxt = CTkLabel(DashboardButton, text=translation.DashboardPageTitle, font=("Futura", 25))
    DashboardButton.bind('<Button-1>', DashboardPageLoad)
    DashboardButtonImg.bind('<Button-1>', DashboardPageLoad)
    DashboardButtonTxt.bind('<Button-1>', DashboardPageLoad)
    #ConsoleButton
    ConsoleButtonIcon = ctk.CTkImage(Image.open(f'{UIconPath}/terminal.png'), size=(35, 35))
    ConsoleButton = CTkFrame(Sidebar, fg_color="grey92")
    ConsoleButtonImg = CTkLabel(ConsoleButton, image=ConsoleButtonIcon, text="")
    ConsoleButtonTxt = CTkLabel(ConsoleButton, text=translation.ConsoleTitle, font=("Futura", 25))
    ConsoleButton.bind('<Button-1>', ConsolePageLoad)
    ConsoleButtonImg.bind('<Button-1>', ConsolePageLoad)
    ConsoleButtonTxt.bind('<Button-1>', ConsolePageLoad)

    #ConfigButton
    ConfigButtonIcon = ctk.CTkImage(Image.open(f'{UIconPath}/config.png'), size=(35, 35))
    ConfigButton = CTkFrame(Sidebar, fg_color="grey92")
    ConfigButtonImg = CTkLabel(ConfigButton, image=ConfigButtonIcon, text="")
    ConfigButtonTxt = CTkLabel(ConfigButton, text=translation.ConfigTitle, font=("Futura", 25))
    ConfigButton.bind('<Button-1>', ConfigPageLoad)
    ConfigButtonImg.bind('<Button-1>', ConfigPageLoad)
    ConfigButtonTxt.bind('<Button-1>', ConfigPageLoad)
    #ServerDirButton
    ServerDirButtonIcon = ctk.CTkImage(Image.open(f'{UIconPath}/folder.png'), size=(35, 35))
    ServerDirButton = CTkFrame(Sidebar, fg_color="grey92")
    ServerDirButtonImg = CTkLabel(ServerDirButton, image=ServerDirButtonIcon, text="")
    ServerDirButtonTxt = CTkLabel(ServerDirButton, text=translation.FolderTitle, font=("Futura", 25))
    ServerDirButton.bind('<Button-1>', OpenServerDir)
    ServerDirButtonImg.bind('<Button-1>', OpenServerDir)
    ServerDirButtonTxt.bind('<Button-1>', OpenServerDir)

    PlayersButtonIcon = ctk.CTkImage(Image.open(f'{UIconPath}/player.png'), size=(35, 35))
    PlayersButton = CTkFrame(Sidebar, fg_color="grey92")
    PlayersButtonImg = CTkLabel(PlayersButton, image=PlayersButtonIcon, text="")
    PlayersButtonTxt = CTkLabel(PlayersButton, text=translation.PlayersTitle, font=("Futura", 25))
    PlayersButton.bind('<Button-1>', PlayersPageLoad)
    PlayersButtonImg.bind('<Button-1>', PlayersPageLoad)
    PlayersButtonTxt.bind('<Button-1>', PlayersPageLoad)

    WhitelistButtonIcon = ctk.CTkImage(Image.open(f'{UIconPath}/whitelist.png'), size=(35, 35))
    WhitelistButton = CTkFrame(Sidebar, fg_color="grey92")
    WhitelistButtonImg = CTkLabel(WhitelistButton, image=WhitelistButtonIcon, text="")
    WhitelistButtonTxt = CTkLabel(WhitelistButton, text=translation.WhitelistTitle, font=("Futura", 25))
    WhitelistButton.bind('<Button-1>', WhitelistPageLoad)
    WhitelistButtonImg.bind('<Button-1>', WhitelistPageLoad)
    WhitelistButtonTxt.bind('<Button-1>', WhitelistPageLoad)

    FeedbackButtonIcon = ctk.CTkImage(Image.open(f'{UIconPath}/feedback.png'), size=(35, 35))
    FeedbackButton = CTkFrame(Sidebar, fg_color="grey92")
    FeedbackButtonImg = CTkLabel(FeedbackButton, image=FeedbackButtonIcon, text="")
    FeedbackButtonTxt = CTkLabel(FeedbackButton, text=translation.FeedbackButtonText, font=("Futura", 25))
    FeedbackButton.bind('<Button-1>', FeedbackPageLoad)
    FeedbackButtonImg.bind('<Button-1>', FeedbackPageLoad)
    FeedbackButtonTxt.bind('<Button-1>', FeedbackPageLoad)

    SettingsButtonIcon = ctk.CTkImage(Image.open(f'{UIconPath}/settings.png'), size=(35, 35))
    SettingsButton = CTkFrame(Sidebar, fg_color="grey92")
    SettingsButtonImg = CTkLabel(SettingsButton, image=SettingsButtonIcon, text="")
    SettingsButtonTxt = CTkLabel(SettingsButton, text=translation.SettingsTitle, font=("Futura", 25))
    SettingsButton.bind('<Button-1>', SettingsPageLoad)
    SettingsButtonImg.bind('<Button-1>', SettingsPageLoad)
    SettingsButtonTxt.bind('<Button-1>', SettingsPageLoad)

    VersionLabel = CTkLabel(Sidebar, text=f"ForgePanel {ProgramSettings['ForgePanelVersion']}", font=("Futura", 15))
    #Pages:
    #Server/Start Page
    WelcomeTxt = CTkLabel(ContentFrame, text=translation.Greeting, font=("Futura", 60, "bold"))
    ChooseServerTxt = CTkLabel(ContentFrame, text=translation.ChooseServerTXT, font=("Futura", 25))
    ChooseServerMenu = ctk.CTkOptionMenu(ContentFrame, values=ServerList)
    ChooseServerButton = CTkButton(ContentFrame, text=translation.ChooseServerTXT, command=ChooseServerButtonAction)
    CreateServerTxt = CTkLabel(ContentFrame, text=translation.CreateServerTXT, font=("Futura", 25))
    CreateServerEntry = ctk.CTkEntry(ContentFrame, placeholder_text=translation.NameEntryTxt)
    CreateServerButton = CTkButton(ContentFrame, text="+ "+translation.CreateServerTXT, command=CreateServerButtonAction)
    HelpHomeButton = CTkButton(ContentFrame, text=translation.HelpButtonTXT, command=HelpSetUpButtonAction)

    #Quick Setup Page:
    EasyPlayerLimitTitle = CTkLabel(ContentFrame, text="Player limit: 5", font=("Futura", 25))
    EasyPlayerLimit = ctk.CTkSlider(ContentFrame, from_=1, to=25, number_of_steps=24, command=PlayerLimitSlider)
    EasyRAMLimitTitle = CTkLabel(ContentFrame, text="Max RAM: 4GB", font=("Futura", 25))
    EasyRAMLimit = ctk.CTkSlider(ContentFrame, from_=2, to=8, number_of_steps=12, command=RAMLimitSlider)
    GamemodeIntuptTitle = CTkLabel(ContentFrame, text="Gamemode", font=("Futura", 25))
    GamemodeInput = ctk.CTkOptionMenu(ContentFrame, values=["Survival", "Creative"])
    DifficultyInputTitle = CTkLabel(ContentFrame, text="Difficulty", font=("Futura", 25))
    DifficultyInput = ctk.CTkOptionMenu(ContentFrame, values=["Peaceful", "Easy", "Normal", "Hard"])
    OnlineModeSelectTitle = CTkLabel(ContentFrame, text="Mojang Auth", font=("Futura", 25))
    OnlineModeSelect = ctk.CTkOptionMenu(ContentFrame, values=["True", "False"])
    WhitelistSelectTitle = CTkLabel(ContentFrame, text="Whitelist", font=("Futura", 25))
    WhitelistSelect = ctk.CTkOptionMenu(ContentFrame, values=["False", "True"])

    NextButton = ctk.CTkButton(ContentFrame, text=translation.NextButtonTXT, command=QuickConfigButton)
    HelpSetUpButton = ctk.CTkButton(ContentFrame, text=translation.HelpButtonTXT, command=HelpSetUpButtonAction)

    #CreateServer(1)
    VersionBar = ctk.CTkTabview(GUI, fg_color="white", segmented_button_unselected_color="grey95", segmented_button_unselected_hover_color="grey90", text_color="black", segmented_button_fg_color="grey95")
    for major_ver, data in VERSION_DATA.items():
        tab = VersionBar.add(major_ver)
        versions = list(reversed(data["versions"]))  # Newest first
        total_versions = len(versions)
        
        for i, version in enumerate(versions):
            frame = ctk.CTkFrame(tab, fg_color="grey95", width=295, height=180)
            frame.grid_propagate(False)
            frame.columnconfigure((0, 2), weight=1)
            
            row = i // 4
            col = i % 4
            x_pos = 15 + (col * 315)
            y_pos = 20 + (row * 200)
            
            frame.place(x=x_pos, y=y_pos)
            
            text = CTkLabel(frame, text=f"Minecraft {version}", font=("Futura", 30))
            text.grid(column=1, row=0, pady=20)
            
            option_menu = ctk.CTkOptionMenu(frame, values=data["modloaders"][version])
            option_menu.grid(column=1, row=1, pady=[26,8])
            button = CTkButton(frame, text=translation.NextButtonTXT, command=lambda v=version, om=option_menu: Thread(target=CreateServer, args=(v, om.get())).start())
            button.grid(column=1, row=2, pady=[0,25])
    #Dashboard:
    '''    #RAM:
    RAMFrame = CTkFrame(ContentFrame, fg_color="grey95", width=150,height=125)
    RAMFrame.grid_propagate(False)
    RAMFrame.columnconfigure(0, weight=1)
    RAMFrame.columnconfigure(2, weight=1)
    CPUFrame = CTkFrame(ContentFrame, fg_color="grey95", width=150, height=125)
    CPUFrame.grid_propagate(False)
    CPUFrame.columnconfigure(0, weight=1)
    CPUFrame.columnconfigure(2, weight=1)
    RAMTitleLabel = CTkLabel(RAMFrame, text="RAM", font=("Futura", 25, "bold"))
    RAMTitleLabel.grid(column=1, row=1, pady=10)
    RAMLabel = CTkLabel(RAMFrame, text="Offline", font=("Futura", 25), text_color="red")
    RAMLabel.grid(column=1, row=2, pady=10)

    CPUTitleLabel = CTkLabel(CPUFrame, text="CPU", font=("Futura", 25, "bold"))
    CPUTitleLabel.grid(column=1, row=1, pady=10)
    CPULabel = CTkLabel(CPUFrame, text="Offline", font=("Futura", 25), text_color="red")
    CPULabel.grid(column=1, row=2, pady=10)'''

    #Misc:
    ErrorTxt = CTkLabel(ContentFrame, text_color="red", text="")

    #CreateServer(2)
    SetupIntroTxt = CTkLabel(ContentFrame, text=translation.NewServerGreetingTxt, font=("Futura", 35))
    SetupIntroButton1 = CTkButton(ContentFrame, text=translation.QuickSetupTxt, font=("Futura", 20), command=lambda: SetupPageLoad("quick"))
    SetupIntroButton2 = CTkButton(ContentFrame, text=translation.AdvancedSetupTxt, font=("Futura", 20))

    OnlineModeChangeTitle = CTkLabel(ContentFrame, text=translation.OnlineModeWarnTxt, text_color="red")
    OnlineModeChangeButton = CTkButton(ContentFrame, text=translation.ContinueAnyway, command=lambda: OnlineModeChange(False))
    OnlineModeProceedButton = CTkButton(ContentFrame, text=translation.NoOnlineModeProceed, command=lambda: OnlineModeChange(True))

    WhitelistChangeTitle = CTkLabel(ContentFrame, text=translation.WhitelistInfoPageTxt, text_color="red")
    WhitelistAddButton = CTkButton(ContentFrame, text=translation.WhitelistAddPlayerTxt, command=lambda: WhitelistPageLoad())
    WhitelistChangeButton = CTkButton(ContentFrame, text=translation.DeactivateWhitelistButtonTxt, command=WhitelistChange)
    #Console Page:
    CommandEntry = ctk.CTkEntry(ContentFrame, placeholder_text=translation.EnterCommandPlaceholder, font=("Helvetica", 15))
    ConsoleOutput = ctk.CTkTextbox(ContentFrame, wrap="word", fg_color="gray10", font=("Helvetica", 15), state="disabled")
    ConsoleOutput.tag_config("stderr", foreground="red")
    ConsoleOutput.tag_config("stdout", foreground="white")
    SendButton = CTkButton(ContentFrame, text=translation.SendCommandTxt, command=lambda: SendCommandToProcess(ServerProcess, CommandEntry.get()))
    StatusFrame = CTkFrame(Sidebar, fg_color="grey92")
    StatusFrame.grid_propagate(False)
    StatusFrame.configure(width=240, height=100)
    StatusLabel = CTkLabel(StatusFrame, text="Offline", text_color="red", font=("Futura", 24))
    StartButton = CTkButton(StatusFrame, text="Start", command=lambda: SendCommandToProcess(None, "start"), fg_color="green4", hover_color="green", width=105)
    StopButton = CTkButton(StatusFrame, text="Stop", command=lambda: SendCommandToProcess(ServerProcess, "/stop"), fg_color="red", hover_color="red3", width=105)
    StatusLabel.grid(column=1, row=0, padx=(10,0), pady=(10,0), columnspan=2)
    StartButton.grid(column=1, row=1, padx=10, pady=10)
    StopButton.grid(column=2, row=1, padx=(0,10), pady=10)

    Title.grid(column=1, row=0, pady=(23,0), padx=(15,0))
    Topbar.grid(column=1,row=0, sticky="nesw")
    Sidebar.grid(column=0,row=0, rowspan=2, sticky="nsew")
    ContentFrame.grid(column=1,row=1,sticky="nesw")

    if Page == "":
        HomePageLoad()

    GUI.protocol("WM_DELETE_WINDOW", lambda: os._exit(0))
    GUI.mainloop()
else:
    GUI = ctk.CTk()
    GUI.title("ForgePanel - Fatal Error")
    GUI.iconbitmap(path.join(f"{path.dirname(path.abspath(__file__))}","assets","ForgePanel","FP.ico"))
    ErrorLabel = ctk.CTkLabel(GUI, text="Java is required to use ForgePanel.", font=("Futura", 15))
    ErrorLabel.pack(padx=10, pady=10)
    button = ctk.CTkButton(GUI, text="Download Temurin (Java)", command=lambda: OpenURL("adoptium.net"))
    button.pack(padx=10, pady=10)
    button2 = ctk.CTkButton(GUI, text="Close", command=exit)
    button2.pack(padx=10, pady=10)
    GUI.mainloop()
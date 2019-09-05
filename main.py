import pymem
import pymem.process
import requests
import string
import random
import os
import time
import tkinter as tkk
import subprocess
import sys
import keyboard
import win32api as winAPI
import win32con
import ctypes

from random import randint, uniform
from colorama import init as colorama_init 
from colorama import Fore, Back, Style
from cryptography.fernet import Fernet
from setproctitle import setproctitle
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import themed_tk as tk
from os import rename
from glob import glob
from threading import Thread

colorama_init()

def update_offsets(raw):
    raw = raw.replace('[signatures]','#signatures\n')
    raw = raw.replace('[netvars]','#netvars\n')
    return raw

def execfile_safely(text):
    notallowed = ["global", "globals()", "system", "import", "print", ":", "ctypes", "win32api", "win32con", "win32gui_thread", "winAPI",
                  "wingui_thread", "is_pressed", "Thread", "subprocess", "sys", "ttk"]
    for i in range(len(notallowed)):
        if notallowed[i] in str(text):
            print(notallowed[i])
            print(Fore.RED + ">>Error: File couldn't be loaded." + Fore.RESET)
            return False
        else:
            pass
    exec(text, globals())
    return True

#Loading settings
try:
    load = open("config.ini", "r")
    execfile_safely(load.read())
    print("'config.ini' has been found and loaded.")
except:
    wallhack = False
    bunnyhop = False
    noflash = False
    topmost = False
    rapidfire = False
    triggerbot = True
    rapidbutton = "x"
    triggerbutton = "c"
    thirdperson = False
    print("'config.ini' was not found, default settings applied.")

#Self updating offsets
try:
    offsets = requests.get("https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.toml").text
    offsets_to_call = update_offsets(offsets)
    execfile_safely(offsets_to_call)
    print("Offsets have been updated succesfuly. :)")
except:
    print("Something went wrong. Is your internet connection working? Does the program have permission to access the internet?")
    print("Closing...")
    time.sleep(5)
    os._exit(0)

class App:
    def __init__(self, wallhack, bunnyhop, noflash, topmost, rapidfire, triggerbot, rapidbutton, triggerbutton, thirdperson):
        self.wallhack = wallhack
        self.bunnyhop = bunnyhop
        self.noflash = noflash
        self.topmost = topmost
        self.rapidfire = rapidfire
        self.triggerbot = triggerbot
        self.rapidbutton = rapidbutton
        self.triggerbutton = triggerbutton
        self.thirdperson = thirdperson
        self.checkforteam = False
        
        #Game process, modules
        self.pm_memory = pymem.Pymem("csgo.exe")
        self.engine = pymem.process.module_from_name(self.pm_memory.process_handle, "engine.dll").lpBaseOfDll
        self.client = pymem.process.module_from_name(self.pm_memory.process_handle, "client_panorama.dll").lpBaseOfDll
        self.lcbase = self.pm_memory.read_int(self.client + dwLocalPlayer)
        
        #Starting Threads
        Thread(target = self.gui_thread).start()
        Thread(target = self.updategui_thread).start()
        Thread(target = self.wallhack_thread).start() 
        Thread(target = self.bunnyhop_thread).start()
        Thread(target = self.noflash_thread).start()
        Thread(target = self.rapidfire_thread).start()
        Thread(target = self.triggerbot_thread).start()
        Thread(target = self.thirdperson_thread).start()
    
    def gui_thread(self):
        self.root = tkk.Tk()
        self.root.title("Menu & Settings")
        self.root.configure(background = "black")
        self.root.minsize(int(ctypes.windll.user32.GetSystemMetrics(0)/5), 0)
        self.root.resizable(False, False)
        self.root.attributes("-topmost", self.topmost)
        self.frameleft = tkk.Frame(background = "black")
        self.frameleft.pack(side = "top")
        self.setfov = tkk.Button(self.frameleft, background = "black", foreground = "white", text = "SetFov", command = lambda: self.fov(int(self.entryfov.get())))
        self.setfov.pack(side = "left")
        self.entryfov = tkk.Scale(self.frameleft, foreground = "white", orient = "horizontal", to = 150, background = "black")
        self.entryfov.pack(side = "left")
        
        #Feautures Enable/disable
        self.featureslabel = tkk.Label(text = "Features Enable/Disable", fg = "gold", bg = "black", font = "Arial 12")
        self.featureslabel.pack()
        self.togglewallhack = tkk.Button(text = "Wallhack", command = lambda: self.wallhack_toggle(), background = "black")
        self.togglewallhack.pack(fill="x")
        self.togglebunnyhop = tkk.Button(text = "Bunnyhop", command = lambda: self.bunnyhop_toggle(), background = "black")
        self.togglebunnyhop.pack(fill="x")
        self.togglenoflash = tkk.Button(text = "NoFlash", command = lambda: self.noflash_toggle(), background = "black")
        self.togglenoflash.pack(fill="x")
        self.togglethirdperson = tkk.Button(text = "Third person", command = lambda: self.thirdperson_toggle(), background = "black")
        self.togglethirdperson.pack(fill="x")
        self.toggletriggerbot = tkk.Button(text = "TriggerBot"+ " ('" + str(self.triggerbutton) + "')", command = lambda: self.triggerbot_toggle(), background = "black")
        self.toggletriggerbot.pack(fill="x")
        self.togglerapidfire= tkk.Button(text = "RapidFire" + " ('" + str(self.rapidbutton) + "')", command = lambda: self.rapidfire_toggle(), background = "black")
        self.togglerapidfire.pack(fill="x")
        
        #Glowhack/wallhack settings
        self.glowhacklabel = tkk.Label(text = "Wallhack settings", fg = "gold", bg = "black", font = "Arial 12")
        self.glowhacklabel.pack()
        self.togglecheckforteam = tkk.Button(text = "Glow enemies only", command = lambda: self.checkforteam_toggle(), background = "black")
        self.togglecheckforteam.pack(fill="x")
        
        #RapidFire settings
        self.rapidfirelabel = tkk.Label(text = "RapidFire settings", fg = "gold", bg = "black", font = "Arial 12")
        self.rapidfirelabel.pack()
        self.rapidlabel = tkk.Label(text = "Vertical recoil reduction [pixels]", fg = "white", bg = "black")
        self.rapidlabel.pack()
        self.entryverticalrecoil = tkk.Scale(foreground = "white", orient = "horizontal",from_ = 0, to = 100, background = "black")
        self.entryverticalrecoil.pack(fill ="x")
        self.entryverticalrecoil.set(0)
        self.rapidlabel2 = tkk.Label(text = "RapidFire delay [ms]", fg = "white", bg = "black")
        self.rapidlabel2.pack()
        self.entryrapidfireclock = tkk.Scale(foreground = "white", orient = "horizontal",from_ = 5, to = 250, background = "black")
        self.entryrapidfireclock.pack(fill ="x")
        self.entryrapidfireclock.set(0)
        
        #Triggerbot settings
        self.triggerbotlabel = tkk.Label(text = "TriggerBot settings", fg = "gold", bg = "black", font = "Arial 12")
        self.triggerbotlabel.pack()
        self.triggerbotlabel2 = tkk.Label(text = "TriggerBot delay [ms]", fg = "white", bg = "black")
        self.triggerbotlabel2.pack()
        self.entrytriggerbotclock = tkk.Scale(foreground = "white", orient = "horizontal",from_ = 5, to = 500, background = "black")
        self.entrytriggerbotclock.pack(fill ="x")
        
        #GUI settings
        self.guilabel = tkk.Label(text = "GUI settings", fg = "gold", bg = "black", font = "Arial 12")
        self.guilabel.pack()
        self.toggletopmost = tkk.Button(text = "TopMost", command = lambda: self.topmost_toggle(), background = "black", fg = "white")
        self.toggletopmost.pack(side = "bottom", fill="x")
        self.guilabel = tkk.Label(text = "Visibility of menu window [%]", fg = "white", bg = "black")
        self.guilabel.pack()
        self.entrytransparency = tkk.Scale(foreground = "white", orient = "horizontal",from_ = 25, to = 100, background = "black")
        self.entrytransparency.pack(fill ="x")
        self.entrytransparency.set(100)
        
        self.root.mainloop()
        
    def updategui_thread(self):
        while True:
            time.sleep(0.05)
            
            #Hiding the window of menu
            if keyboard.is_pressed("insert"):
                self.topmost_toggle()
                time.sleep(0.1)
                    
            #Updating buttons
            if self.wallhack:
                self.togglewallhack.configure(fg = "green")
            else:
                self.togglewallhack.configure(fg = "red")
                
            if self.bunnyhop:
                self.togglebunnyhop.configure(fg = "green")
            else:
                self.togglebunnyhop.configure(fg = "red")
                
            if self.noflash:
                self.togglenoflash.configure(fg = "green")
            else:
                self.togglenoflash.configure(fg = "red")
            
            if self.topmost:
                self.toggletopmost.configure(fg = "green")
            else:
                self.toggletopmost.configure(fg = "red")
                
            if self.thirdperson:
                self.togglethirdperson.configure(fg = "green")
            else:
                self.togglethirdperson.configure(fg = "red")
                
            if self.checkforteam:
                self.togglecheckforteam.configure(fg = "green")
            else:
                self.togglecheckforteam.configure(fg = "red")
            
            if self.rapidfire:
                self.togglerapidfire.configure(fg = "green",text = "RapidFire" + " ('" + str(self.rapidbutton) + "')")
            else:
                self.togglerapidfire.configure(fg = "red", text = "RapidFire" + " ('" + str(self.rapidbutton) + "')")
                
            if self.triggerbot:
                self.toggletriggerbot.configure(fg = "green", text = "TriggerBot"+ " ('" + str(self.triggerbutton) + "')")
            else:
                self.toggletriggerbot.configure(fg = "red", text = "TriggerBot"+ " ('" + str(self.triggerbutton) + "')")
                
            #Update transparency
            self.root.attributes("-alpha", self.entrytransparency.get()/100)
             
    def triggerbot_thread(self):
        shooting = False
        while True:
            time.sleep(0.15)
            while self.triggerbot:
                time.sleep(0.01)
                self.lcbase = self.pm_memory.read_int(self.client + dwLocalPlayer)
                
                if keyboard.is_pressed(self.triggerbutton):
                    entity = self.pm_memory.read_int(player + m_iCrosshairId)
                    if entity > 0 and entity <= 64:
                        entity = self.pm_memory.read_int(self.client + dwEntityListt + (entity -1) * 0x10)
                        entity_team = self.pm_memory.read_int(entity + m_iTeamNum)
                        player_team = self.pm_memory.read_int(player + m_iTeamNum)
                        if player_team != entity_team:
                            shooting = True
                            time.sleep(self.entrytriggerbotclock.get()/1000)
                            self.pm_memory.write_int(self.client + dwForceAttack, 5)
                            
                if not keyboard.is_pressed(self.triggerbutton) and shooting == True:
                    self.pm_memory.write_int(self.client + dwForceAttack, 4)
                    shooting = False
                    

    def rapidfire_thread(self):
        while True:
            time.sleep(0.15)
            while self.rapidfire:
                time.sleep(0.01)
                while keyboard.is_pressed(self.rapidbutton):
                    ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
                    ctypes.windll.user32.mouse_event(0x0001, 0, int(self.entryverticalrecoil.get()), 0, 0)
                    time.sleep(self.entryrapidfireclock.get()/1000)
                    ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
                    
    def wallhack_thread(self):
        while True:
            time.sleep(0.15)
            while self.wallhack:
                time.sleep(0.02)
                glow_manager = self.pm_memory.read_int(self.client + dwGlowObjectManager)
                for i in range(1, 32): 
                    entity = self.pm_memory.read_int(self.client + dwEntityListt + i * 0x10)
                    if entity:
                        entity_team_id = self.pm_memory.read_int(entity + m_iTeamNum)
                        entity_glow = self.pm_memory.read_int(entity + m_iGlowIndex)
                        
                        #Check for team which you are playing in
                        player = self.pm_memory.read_int(self.client + dwLocalPlayer)
                        checkforteam = self.pm_memory.read_int(player + m_iTeamNum)
                      
                        #Glow only allies if this is enabled
                        if self.checkforteam == True:
                            
                            if checkforteam == 3:
                                
                                if entity_team_id == 2:  # Terrorist
                                    self.pm_memory.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0.5))   # R 
                                    self.pm_memory.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))   # G
                                    self.pm_memory.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))   # B
                                    self.pm_memory.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                                    self.pm_memory.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow
                            else:
        
                                if entity_team_id == 3:  # Counter-terrorist
                                    self.pm_memory.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0))   # R
                                    self.pm_memory.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(1))   # G
                                    self.pm_memory.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))   # B
                                    self.pm_memory.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                                    self.pm_memory.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow
                                    
                        #Glow enemies and allies if this is disabled
                        else:
                            if entity_team_id == 2:  # Terrorist
                                self.pm_memory.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0.5))   # R 
                                self.pm_memory.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))   # G
                                self.pm_memory.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))   # B
                                self.pm_memory.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                                self.pm_memory.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow
                                
                            elif entity_team_id == 3:  # Counter-terrorist
                                self.pm_memory.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0))   # R
                                self.pm_memory.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(1))   # G
                                self.pm_memory.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))   # B
                                self.pm_memory.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                                self.pm_memory.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow
                            
                            
    def bunnyhop_thread(self):
        while True:
            time.sleep(0.15)
            while self.bunnyhop:
                    time.sleep(0.001)
                    try:
                        player = self.pm_memory.read_int(self.client + dwLocalPlayer)
                        force_jump = self.client + dwForceJump
                        on_ground = self.pm_memory.read_int(player + m_fFlags)

                        if keyboard.is_pressed("space"):
                            if on_ground == 257:
                                self.pm_memory.write_int(force_jump, 5)
                                time.sleep(0.17)
                                self.pm_memory.write_int(force_jump, 4)
                            time.sleep(0.002)
                    except pymem.exception.MemoryReadError:
                        pass
                    
    def thirdperson_thread(self):
        self.lcbase = self.pm_memory.read_int(self.client + dwLocalPlayer)
        do = False
        while True:
            if do == True:
                self.pm_memory.write_int(player + m_iObserverMode, 0)
                do = False
            time.sleep(0.15)
            while self.thirdperson:
                self.pm_memory.write_int(player + m_iObserverMode, 1)
                do = True
                time.sleep(0.25)
                    
    def noflash_thread(self):
        while True:
            time.sleep(0.15)
            while self.noflash:
                time.sleep(0.025)
                try:
                    self.lcbase = self.pm_memory.read_int(self.client + dwLocalPlayer)
                    flash_value = player + m_flFlashMaxAlpha
                    self.pm_memory.write_float(flash_value, float(0))
                    time.sleep(0.025)
                except pymem.exception.MemoryReadError:
                    pass
                except pymem.exception.MemoryWriteError:
                    pass
                        
    def fov(self, inputFOV):
        c = 0
        while c < 3000:
            self.pm_memory.write_int(self.lcbase + m_iFOV, inputFOV)
            c+=1
            
    def thirdperson_toggle(self):
        if self.thirdperson == True:
            self.thirdperson = False
        else:
            self.thirdperson = True
            
    def triggerbot_toggle(self):
        if self.triggerbot == True:
            self.triggerbot = False
        else:
            self.triggerbot = True
    
    def rapidfire_toggle(self):
        if self.rapidfire == True:
            self.rapidfire = False
        else:
            self.rapidfire = True
            
    def topmost_toggle(self):
        if self.topmost == True:
            self.topmost = False
            self.root.attributes("-topmost", self.topmost)
        else:
            self.topmost = True
            self.root.attributes("-topmost", self.topmost)
            
    def wallhack_toggle(self):
        if self.wallhack == True:
            self.wallhack = False
        else:
            self.wallhack = True
            
    def bunnyhop_toggle(self):
        if self.bunnyhop == True:
            self.bunnyhop = False
        else:
            self.bunnyhop = True
    
    def noflash_toggle(self):
        if self.noflash == True:
            self.noflash = False
        else:
            self.noflash = True
            
    def checkforteam_toggle(self):
        if self.checkforteam == True:
            self.checkforteam = False
        else:
            self.checkforteam = True

App(wallhack, bunnyhop, noflash, topmost, rapidfire, triggerbot, rapidbutton, triggerbutton, thirdperson)

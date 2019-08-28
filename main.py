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


#Mouse & Keyboard stuff
from pynput.mouse import Button, Controller
mouse = Controller()

#random string
def randomString(stringLength):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))
#random string

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

class App:
    def __init__(self, wallhack, bunnyhop, noflash, topmost, rapidfire, triggerbot, rapidbutton, triggerbutton):
        self.wallhack = wallhack
        self.bunnyhop = bunnyhop
        self.noflash = noflash
        self.topmost = topmost
        self.rapidfire = rapidfire
        self.triggerbot = triggerbot
        self.rapidbutton = rapidbutton
        self.triggerbutton = triggerbutton
        
        self.pwritemodule = pymem.Pymem("csgo.exe")
        self.client = pymem.process.module_from_name(self.pwritemodule.process_handle, "client_panorama.dll").lpBaseOfDll
        self.lcbase = self.pwritemodule.read_int(self.client + dwLocalPlayer)
        
        #Starting Threads
        Thread(target = self.gui_thread).start()
        Thread(target = self.updategui_thread).start()
        Thread(target = self.wallhack_thread).start() 
        Thread(target = self.bunnyhop_thread).start()
        Thread(target = self.noflash_thread).start()
        Thread(target = self.rapidfire_thread).start()
        Thread(target = self.triggerbot_thread).start()
    
    def gui_thread(self):
        self.root = tkk.Tk()
        self.root.title("Menu & Settings")
        self.root.configure(background = "black")
        self.root.minsize(300, 250)
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
        self.toggletriggerbot = tkk.Button(text = "TriggerBot"+ " ('" + str(self.triggerbutton) + "')", command = lambda: self.triggerbot_toggle(), background = "black")
        self.toggletriggerbot.pack(fill="x")
        self.togglerapidfire= tkk.Button(text = "RapidFire" + " ('" + str(self.rapidbutton) + "')", command = lambda: self.rapidfire_toggle(), background = "black")
        self.togglerapidfire.pack(fill="x")
        
        #RapidFire settings
        self.rapidfirelabel = tkk.Label(text = "RapidFire settings", fg = "gold", bg = "black", font = "Arial 12")
        self.rapidfirelabel.pack()
        self.rapidlabel = tkk.Label(text = "Vertical recoil reduction [pixels]", fg = "white", bg = "black")
        self.rapidlabel.pack()
        self.entryverticalrecoil = tkk.Scale(foreground = "white", orient = "horizontal",length = 200, from_ = 0, to = 100, background = "black")
        self.entryverticalrecoil.pack()
        self.entryverticalrecoil.set(0)
        self.rapidlabel2 = tkk.Label(text = "RapidFire delay [ms]", fg = "white", bg = "black")
        self.rapidlabel2.pack()
        self.entryrapidfireclock = tkk.Scale(foreground = "white", orient = "horizontal",length = 200, from_ = 5, to = 250, background = "black")
        self.entryrapidfireclock.pack()
        self.entryrapidfireclock.set(0)
        
        #Triggerbot settings
        self.triggerbotlabel = tkk.Label(text = "TriggerBot settings", fg = "gold", bg = "black", font = "Arial 12")
        self.triggerbotlabel.pack()
        self.triggerbotlabel2 = tkk.Label(text = "TriggerBot delay [ms]", fg = "white", bg = "black")
        self.triggerbotlabel2.pack()
        self.entrytriggerbotclock = tkk.Scale(foreground = "white", orient = "horizontal",length = 200, from_ = 5, to = 500, background = "black")
        self.entrytriggerbotclock.pack()
        
        #GUI settings
        self.guilabel = tkk.Label(text = "GUI settings", fg = "gold", bg = "black", font = "Arial 12")
        self.guilabel.pack()
        self.toggletopmost = tkk.Button(text = "TopMost", command = lambda: self.topmost_toggle(), background = "black", fg = "white")
        self.toggletopmost.pack(side = "bottom", fill="x")
        self.guilabel = tkk.Label(text = "Transparency of window", fg = "white", bg = "black")
        self.guilabel.pack()
        self.entrytransparency = tkk.Scale(foreground = "white", orient = "horizontal",from_ = 25, to = 100, background = "black")
        self.entrytransparency.pack()
        self.entrytransparency.set(100)
        
        self.root.mainloop()
        
    def updategui_thread(self):
        while True:
            time.sleep(0.025)
            #Updating colors of buttons
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
                player = self.pwritemodule.read_int(self.client + dwLocalPlayer)
                
                if keyboard.is_pressed(self.triggerbutton):
                    entity = self.pwritemodule.read_int(player + m_iCrosshairId)
                    if entity > 0 and entity <= 64:
                        entity = self.pwritemodule.read_int(self.client + dwEntityList + (entity -1) * 0x10)
                        entity_team = self.pwritemodule.read_int(entity + m_iTeamNum)
                        player_team = self.pwritemodule.read_int(player + m_iTeamNum)
                        if player_team != entity_team:
                            shooting = True
                            time.sleep(self.entrytriggerbotclock.get()/1000)
                            self.pwritemodule.write_int(self.client + dwForceAttack, 5)
                            
                if not keyboard.is_pressed(self.triggerbutton) and shooting == True:
                    self.pwritemodule.write_int(self.client + dwForceAttack, 4)
                    shooting = False
                    

    def rapidfire_thread(self):
        while True:
            time.sleep(0.15)
            while self.rapidfire:
                time.sleep(0.01)
                while keyboard.is_pressed(self.rapidbutton):
                    mouse.press(Button.left)
                    ctypes.windll.user32.mouse_event(0x0001, 0, int(self.entryverticalrecoil.get()), 0, 0)
                    time.sleep(self.entryrapidfireclock.get()/1000)
                    mouse.release(Button.left)
                    
    def wallhack_thread(self):
        while True:
            time.sleep(0.15)
            while self.wallhack:
                time.sleep(0.025)
                glow_manager = self.pwritemodule.read_int(self.client + dwGlowObjectManager)
                for i in range(1, 32): 
                    entity = self.pwritemodule.read_int(self.client + dwEntityList + i * 0x10)
                    if entity:
                        entity_team_id = self.pwritemodule.read_int(entity + m_iTeamNum)
                        entity_glow = self.pwritemodule.read_int(entity + m_iGlowIndex)
                        
                        if entity_team_id == 2:  # Terrorist
                            self.pwritemodule.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0.5))   # R 
                            self.pwritemodule.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))   # G
                            self.pwritemodule.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))   # B
                            self.pwritemodule.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                            self.pwritemodule.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow

                        elif entity_team_id == 3:  # Counter-terrorist
                            self.pwritemodule.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(0))   # R
                            self.pwritemodule.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(1))   # G
                            self.pwritemodule.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(1))   # B
                            self.pwritemodule.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # Alpha
                            self.pwritemodule.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1)           # Enable glow
                            
    def bunnyhop_thread(self):
        while True:
            time.sleep(0.15)
            while self.bunnyhop:
                    time.sleep(0.001)
                    try:
                        player = self.pwritemodule.read_int(self.client + dwLocalPlayer)
                        force_jump = self.client + dwForceJump
                        on_ground = self.pwritemodule.read_int(player + m_fFlags)

                        if keyboard.is_pressed("space"):
                            if on_ground == 257:
                                self.pwritemodule.write_int(force_jump, 5)
                                time.sleep(0.17)
                                self.pwritemodule.write_int(force_jump, 4)
                            time.sleep(0.002)
                    except pymem.exception.MemoryReadError:
                        pass
                    
    def noflash_thread(self):
        while True:
            time.sleep(0.15)
            while self.noflash:
                time.sleep(0.025)
                try:
                    player = self.pwritemodule.read_int(self.client + dwLocalPlayer)
                    flash_value = player + m_flFlashMaxAlpha
                    self.pwritemodule.write_float(flash_value, float(0))
                    time.sleep(0.025)
                except pymem.exception.MemoryReadError:
                    pass
                except pymem.exception.MemoryWriteError:
                    pass
                        
    def fov(self, inputFOV):
        c = 0
        while c < 3000:
            self.pwritemodule.write_int(self.lcbase + m_iFOV, inputFOV)
            c+=1
            
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

#Loading offsets and settings
try:
    load = open("config.ini", "r")
    execfile_safely(load.read())
except:
    #Default Offsets
    dwEntityList = (0x4D06DC4)
    dwGlowObjectManager = (0x5247210)
    m_iGlowIndex = (0xA40C)
    m_iTeamNum = (0xF4)
    dwLocalPlayer = (0xCF4A4C)
    m_iFOV = (0x31E4)
    dwForceJump = (0x51AA47C)
    m_fFlags = (0x104)
    m_flFlashMaxAlpha = (0xA3F0)
    dwForceAttack = (0x3138480)
    m_iCrosshairId = (0xB3AC)
    #Default settings
    wallhack = False
    bunnyhop = False
    noflash = False
    topmost = True
    rapidfire = False
    triggerbot = False
    rapidbutton = "x"
    triggerbutton = "c"

App(wallhack, bunnyhop, noflash, topmost, rapidfire, triggerbot, rapidbutton, triggerbutton)

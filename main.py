import pymem
import pymem.process
import requests
from random import randint, uniform
import string
import random
import os
from colorama import init as colorama_init 
from colorama import Fore, Back, Style
from cryptography.fernet import Fernet
from setproctitle import setproctitle
import time
import tkinter as tkk
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import themed_tk as tk
import subprocess
import sys
import keyboard
from os import rename
from glob import glob
import win32api as winAPI
import win32con
from threading import Thread
import ctypes



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

"""
class RaFunctions:
    def __init__(self, name):
        self.functions = 0
        self.name = name
        self.createFunction()
    
    def createFunction(self):
        self.functions += 1
        rvar = randomString(1)
        rnum = randint(0, 1000)
        rsleep = uniform(0.5, 2)
        exec("def " + str(self.name) +"()" + ":" +"\n" + "    " +str(rvar)+" = " + str(rnum) + "\n"+"    while True:" +"\n" + "        time.sleep(" + str(rsleep) + ")" + "\n" + "        " + str(rvar) + "+=1", globals())

class RaClasses:
    def __init__(self, name):
        self.functions = 0
        self.name = name
        self.createClass()
    
    def createClass(self):
        self.functions += 1
        rvar = randomString(10)
        rnum = randint(0, 1000)
        rsleep = uniform(0.5, 2)
        exec("class " + str(self.name) +"()" + ":" +"\n" +"    " + "def __init__(self, " +str(rvar) +"):" +"\n" + "        self." + str(rvar) +"=" + str(rvar)  + "\n" + "        self." +str(randomString(5)) + "=" + str(rnum), globals())


        
def randomthings():
    for i in range(randint(200, 300)):
        exec(str(randomString(randint(10, 25))) + "= RaClasses(randomString(randint(25, 50)))", globals())
        
    for i in range(randint(200, 300)):
        exec(str(randomString(randint(10, 25))) + "= RaFunctions(randomString(randint(25, 50)))", globals())

    #Random variables
    for i in range(randint(200, 300)):
        intorstring = randint(0, 1)
        if intorstring == 0:
            exec(str(randomString(randint(10, 25))) + " = int", globals())
        else:
            exec(str(randomString(randint(10, 25))) + " = str", globals())
    #Random variables
randomthings()


def change_filename_and_processname():
    os.system("title " +str(randomString(10)))
    setproctitle(str(randomString(10)))
    rnstr = str(randomString(10))
    for fname in glob('*.exe'):
        rename(fname, rnstr + ".exe")
        
        
def connection():
    def download(id):
        try:
            URL = "https://docs.google.com/uc?entry_horizontalport=download"
            session = requests.Session()
            response = session.get(URL, params = { 'id' : id }, stream = True)
            token = gettoken(response)
            if token:
                params = { 'id' : id, 'confirm' : token }
                response = session.get(URL, params = params, stream = True)
            save(response)
        except:
            os._exit(0)

    def gettoken(response):
        for thekey, value in response.cookies.items():
            if thekey.startswith('download_warning'):
                return value
            else:
                os._exit(0)
                try:
                    #Deleting old tempdata#
                    os.startfile("temp.bat")
                    #Deleting old tempdata#
                except:
                    pass
        return None
            
    def save(response):
        global auth
        global secure_string
        CHUNK_SIZE = 32768
        print(Fore.GREEN + "Server: Connected" + Fore.RESET)
        auth = True
        for chunk in response.iter_content(CHUNK_SIZE):
            secure_string = chunk

    file_id = '1obTUiJVUDL7QpM-2uS5L0HGzFZB7pYz0'
    download(file_id)
            
def GetUUID():
    cmd = 'wmic csproduct get uuid'
    uuid = str(subprocess.check_output(cmd))
    pos1 = uuid.find("\\n")+2
    uuid = uuid[pos1:-15]
    return uuid

def deletedetails():
    global username, password, hwid_list, secure_string
    global uinput, pinput
    del uinput, pinput
    del username
    del password
    del hwid_list
    del secure_string

logginned = False
uinput = ""
pinput = ""
def login():
    global logginned
    global uinput, pinput
    passed = False
    while True:
        global username, password, hwid_list, secure_string, auth
        time.sleep(1)
        try:
            
            def Logingui_thread():
                loginroot = tk.Tk()
                def switch():
                    global logginned
                    global uinput, pinput
                    uinput = str(euser.get())
                    pinput = int(epass.get())
                    logginned = True
                    loginroot.quit()
                    loginroot.destroy()
                    
                
                loginroot.title(str(randomString(3)))
                loginroot.minsize(200, 125)
                ulabel = tk.Label(loginroot, text = "Username")
                ulabel.pack()
                euser = tk.Entry(loginroot)
                euser.pack()
                plabel = tk.Label(loginroot, text = "Password")
                plabel.pack()
                epass = tk.Entry(loginroot, show ="*")
                epass.pack()
                process = tk.Button(loginroot, text = "Login", command = lambda: switch())
                process.pack()
                loginroot.mainloop()
            
            Thread(target = Logingui_thread).start()
                
            while logginned == False:
                time.sleep(0.1)
                pass
            f = Fernet(b'-eGZHTlW2xIiGCx4LABEEm-fwj8WaLegRKBQU3v06us=')
            l = secure_string
            l = f.decrypt(l)
            l = l.decode()
            execfile_safely(l)
            uuid = GetUUID()
            if uinput == username[username.index(uinput)] and pinput == password[username.index(uinput)] and hwid_list[username.index(uinput)] == uuid:
                deletedetails()
                print(Fore.GREEN + "You have granted an access" + Fore.RESET)
                print("\n")
                passed = True
                break
            else:
                deletedetails()
                print(Fore.RED + "Login didn't go well")
                auth = False
                time.sleep(2)
                os._exit(0)
        except:
            deletedetails()
            print(Fore.RED + "Login didn't go well")
            auth = False
            time.sleep(2)
            os._exit(0)
    if passed:
        pass
    else:
        os._exit(0)


auth = False
secure_string = b""
username = []
password = []
hwid_list = []
connection()
login()
change_filename_and_processname()
if auth == True:
    pass
else:
    os._exit(0)
"""

#Mouse & Keyboard stuff
from pynput.mouse import Button, Controller

mouse = Controller()

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
        
        """
        self.pwritemodule = pymem.Pymem("csgo.exe")
        self.client = pymem.process.module_from_name(self.pwritemodule.process_handle, "client_panorama.dll").lpBaseOfDll
        self.lcbase = self.pwritemodule.read_int(self.client + dwLocalPlayer)
        """
        
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
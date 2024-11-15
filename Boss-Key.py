from core import BossKey
import sys
import ctypes
import os
import psutil
import wx
from core.config import Config

errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2) # Win10 and Win8
success = ctypes.windll.user32.SetProcessDPIAware() #Win7 and below
def windows_message_box(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)

def write_pid(name):
    with open(name, "w") as f:
        f.write(str(psutil.Process().pid))
def is_already_running(name):
    if os.path.exists(name):
        with open(name, "r") as f:
            pid=f.read()
        if pid == "":
            write_pid(name)
        else:
            try:
                process=psutil.Process(int(pid))
                if process.is_running():
                    return True
                else:
                    write_pid(name)
                    return False
            except:
                write_pid(name)
                return False
    else:
        write_pid(name)

if is_already_running(sys.argv[0][:-4]+".lock"):
    windows_message_box("Boss Key", "Boss Key is already running")
    sys.exit(0)
else:
    app = wx.App()
    Config.HotkeyWindow=BossKey.HotkeyWindow()
    Config.SettingWindow=BossKey.SettingWindow()
    Config.TaskBarIcon=BossKey.TaskBarIcon()
    if Config.first_start:
        Config.SettingWindow.Show()
    app.MainLoop()
    

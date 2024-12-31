from core.config import Config
import core.tools as tool
from win32gui import GetForegroundWindow, ShowWindow
from win32con import SW_HIDE, SW_SHOW
import sys
from pynput import keyboard
import time

class HotkeyListener():
    def __init__(self):
        try:
            ShowWindow(Config.hwnd, SW_SHOW)
            if Config.mute_after_hide:
                tool.changeMute(Config.hwnd,0)
        except:
            pass
        tool.sendNotify("Boss Key正在运行！", "Boss Key正在为您服务，您可通过托盘图标看到我")
        self.listener = None
        self.reBind()
    
    def stop(self):
        if self.listener:
            self.listener.stop()
            self.listener = None
    
    def reBind(self):
        self.stop()
        self.BindHotKey()
        
    def BindHotKey(self):
        self.hotkeys = {
            Config.hide_hotkey: self.onHide,
            Config.close_hotkey: self.Close
        }
        self.hotkeys = tool.keyConvert(self.hotkeys)
        print(self.hotkeys)
        self.listener = keyboard.GlobalHotKeys(self.hotkeys)
        self.listener.start()

    def onHide(self,e=""):
        if Config.times == 1:
            # 隐藏窗口
            current = GetForegroundWindow()
            if Config.send_before_hide:
                time.sleep(0.2)
                keyboard.Controller().tap(keyboard.KeyCode.from_vk(0xB2))
                
            ShowWindow(current, SW_HIDE)
            if Config.mute_after_hide:
                tool.changeMute(current,1)
            Config.hwnd=current
            Config.times = 0
        else:
            # 显示窗口
            ShowWindow(Config.hwnd, SW_SHOW)
            if Config.mute_after_hide:
                tool.changeMute(Config.hwnd,0)
            Config.times = 1
        Config.save()

    def Close(self,e=""):
        tool.sendNotify("Boss Key已停止服务", "Boss Key已成功退出")
        if Config.times == 0:
            ShowWindow(Config.hwnd, SW_SHOW)
            Config.times = 1
            
        self.stop()
        Config.TaskBarIcon.Destroy()
        Config.SettingWindow.Destroy()
        sys.exit(0)

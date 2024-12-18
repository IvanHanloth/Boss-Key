from core.config import Config
import core.tools as tool
from win32gui import GetForegroundWindow, ShowWindow
from win32con import SW_HIDE, SW_SHOW
import sys
from pynput import keyboard

class HotkeyListener():
    def __init__(self):
        try:
            ShowWindow(Config.hwnd, SW_SHOW)
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
            Config.startup_hotkey: self.onStartup,
            Config.close_hotkey: self.Close
        }
        self.hotkeys = tool.keyConvert(self.hotkeys)
        print(self.hotkeys)
        self.listener = keyboard.GlobalHotKeys(self.hotkeys)
        self.listener.start()

    def onHide(self,e=""):
        Config.hwnd_n = GetForegroundWindow()
        if Config.times == 1:
            # 隐藏窗口
            ShowWindow(Config.hwnd_n, SW_HIDE)
            if Config.mute_after_hide:
                tool.changeMute(Config.hwnd_n,1)
            Config.hwnd_b=Config.hwnd_n
            Config.hwnd=Config.hwnd_b
            Config.times = 0
        else:
            # 显示窗口
            ShowWindow(Config.hwnd_b, SW_SHOW)
            if Config.mute_after_hide:
                tool.changeMute(Config.hwnd_b,0)
            Config.hwnd_b = ""
            Config.times = 1
        Config.save()

    def onStartup(self,e=""):
        tool.sendNotify(
            title="嗨！你好！",
            message="也许你还在习惯于使用快捷键来切换开机启动，但是这个功能已经被移除了。\n现在你可以在托盘菜单中直接切换开机启动状态，希望你喜欢！\n此提示将在下个版本完全移除"
        )

    def Close(self,e=""):
        tool.sendNotify("Boss Key已停止服务", "Boss Key已成功退出")
        if Config.times == 0:
            ShowWindow(Config.hwnd_b, SW_SHOW)
            Config.hwnd_b = ""
            Config.times = 1
            
        self.stop()
        Config.TaskBarIcon.Destroy()
        Config.SettingWindow.Destroy()
        sys.exit(0)

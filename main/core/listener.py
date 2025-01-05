from core.config import Config
import core.tools as tool
from win32gui import GetForegroundWindow, ShowWindow
from win32con import SW_HIDE, SW_SHOW
import sys
from pynput import keyboard
import multiprocessing
import time

class HotkeyListener():
    def __init__(self):
        try:
            self.ShowWindows()
        except:
            pass
        tool.sendNotify("Boss Key正在运行！", "Boss Key正在为您服务，您可通过托盘图标看到我")
        self.listener = None
        self.reBind()
    
    def stop(self):
        if self.listener is not None:
            try:
                self.listener.terminate()
                self.listener.join()
            except:
                pass
            finally:
                self.listener = None
    
    def reBind(self):
        self.stop()
        self.BindHotKey()
    
    def ListenerProcess(self,hotkey):
        print(hotkey)
        with keyboard.GlobalHotKeys(hotkey) as listener:
            while True: #避免意外退出
                listener.join()
                print("线程意外退出")

    def BindHotKey(self):
        hotkeys = {
            Config.hide_hotkey: self.onHide,
            Config.close_hotkey: self.Close
        }
        hotkeys = tool.keyConvert(hotkeys)
                
        self.listener = multiprocessing.Process(target=self.ListenerProcess,daemon=True,args=(hotkeys,),name="Boss-Key热键监听进程")
        self.listener.start()

    def onHide(self,e=""):
        if Config.times == 1:
            # 隐藏窗口
            self.HideWindows()
        else:
            self.ShowWindows()

    def ShowWindows(self):
        # 显示窗口
        for i in Config.history:
            ShowWindow(i, SW_SHOW)
            if Config.mute_after_hide:
                tool.changeMute(i,0)
                
        Config.times = 1
        Config.save()
    
    def HideWindows(self):
        # 隐藏窗口
        needHide=[]
        windows=tool.getAllWindows()
        
        outer=windows
        inner=Config.hide_binding

        #减少循环次数，选择相对较少的做外循环
        if len(Config.hide_binding) < len(windows):
            outer=Config.hide_binding
            inner=windows

        for i in outer:
            for j in inner:
                if tool.isSameWindow(i,j,False):
                    if outer==Config.hide_binding: # 此时i是绑定的元素，j是窗口元素，需要隐藏j
                        needHide.append(j['hwnd'])
                    else:
                        needHide.append(i['hwnd'])
                    break

        if Config.hide_current: # 插入当前窗口的句柄
            needHide.append(GetForegroundWindow())

        needHide=tool.remove_duplicates(needHide) # 去重
        for i in needHide:
            if Config.send_before_hide:
                time.sleep(0.2)
                keyboard.Controller().tap(keyboard.KeyCode.from_vk(0xB2))
                
            ShowWindow(i, SW_HIDE)
            if Config.mute_after_hide:
                tool.changeMute(i,1)

        Config.history=needHide
        Config.times = 0
        Config.save()

    def Close(self,e=""):
        tool.sendNotify("Boss Key已停止服务", "Boss Key已成功退出")
        self.ShowWindows()
            
        self.stop()
        Config.TaskBarIcon.Destroy()
        Config.SettingWindow.Destroy()
        sys.exit(0)

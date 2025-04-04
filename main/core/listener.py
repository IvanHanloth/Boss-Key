from core.config import Config
import core.tools as tool
from win32gui import GetForegroundWindow, ShowWindow
from win32con import SW_HIDE, SW_SHOW
import sys
from pynput import keyboard
import multiprocessing
import threading
import time
import wx

class HotkeyListener():
    def __init__(self):
        try:
            self.ShowWindows()
        except:
            pass
        tool.sendNotify("Boss Key正在运行！", "Boss Key正在为您服务，您可通过托盘图标看到我")
        self.Queue = multiprocessing.Queue()
        self.listener = None
        self.reBind()
        threading.Thread(target=self.listenToQueue,daemon=True).start()

    def listenToQueue(self):
        exit_flag = False
        while True:
            try:
                msg = self.Queue.get()
                if msg == "showTaskBarIcon":
                    if hasattr(Config, 'TaskBarIcon') and Config.TaskBarIcon and wx.GetApp():
                        wx.CallAfter(Config.TaskBarIcon.ShowIcon)
                elif msg == "hideTaskBarIcon":
                    if hasattr(Config, 'TaskBarIcon') and Config.TaskBarIcon and wx.GetApp():
                        wx.CallAfter(Config.TaskBarIcon.HideIcon)
                elif msg == "closeApp":
                    print("收到关闭消息")
                    tool.sendNotify("Boss Key已停止服务", "Boss Key已成功退出")
                    self.ShowWindows()
                    self.stop()
                    # 先解除所有窗口的事件处理器绑定
                    try:
                        if wx.GetApp():  # 确保应用程序仍在运行
                            wx.CallAfter(self.cleanup_windows)
                    except Exception as e:
                        print(f"清理窗口时出错: {e}")
                    exit_flag = True
                    break
            except Exception as e:
                print(f"处理队列消息时出错: {e}")
                pass

        if exit_flag:
            if wx.GetApp():
                wx.CallAfter(wx.GetApp().ExitMainLoop)
            sys.exit(0)

    def cleanup_windows(self):
        """安全清理窗口资源"""
        try:
            if hasattr(Config, 'SettingWindow') and Config.SettingWindow:
                if Config.SettingWindow.IsShown():
                    Config.SettingWindow.Hide()
                Config.SettingWindow.Destroy()
                Config.SettingWindow = None
                
            if hasattr(Config, 'UpdateWindow') and Config.UpdateWindow:
                if Config.UpdateWindow.IsShown():
                    Config.UpdateWindow.Hide()
                Config.UpdateWindow.Destroy()
                Config.UpdateWindow = None
                
            if hasattr(Config, 'TaskBarIcon') and Config.TaskBarIcon:
                Config.TaskBarIcon.Destroy()
                Config.TaskBarIcon = None
        except Exception as e:
            print(f"清理窗口资源时出错: {str(e)}")
            
    def reBind(self):
        self.stop()
        self.BindHotKey()
    
    def ListenerProcess(self,hotkey):
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

    def ShowWindows(self,load=True):
        # 显示窗口
        if load:
            Config.load()
        for i in Config.history:
            ShowWindow(i, SW_SHOW)
            if Config.mute_after_hide:
                tool.changeMute(i,0)

        if Config.hide_icon_after_hide:
            self.Queue.put("showTaskBarIcon")
                
        Config.times = 1
        Config.save()
    
    def HideWindows(self):
        # 隐藏窗口

        Config.load()
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
                if tool.isSameWindow(i, j, False, not Config.path_match):
                    if outer==Config.hide_binding: # 此时i是绑定的元素，j是窗口元素，需要隐藏j
                        needHide.append(j.hwnd)
                    else:
                        needHide.append(i.hwnd)
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
        if Config.hide_icon_after_hide:
            self.Queue.put("hideTaskBarIcon")
        Config.save()

    def Close(self,e=""):
        self.Queue.put("closeApp")
    
    def stop(self):
        if self.listener is not None:
            try:
                self.listener.terminate()
                self.listener.join()
            except:
                pass
            finally:
                self.listener = None

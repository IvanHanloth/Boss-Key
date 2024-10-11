# -*- coding: utf-8 -*-
from core.config import Config,save_config
from winreg import OpenKey,HKEY_CURRENT_USER,QueryValueEx,DeleteValue,CloseKey,KEY_ALL_ACCESS,SetValueEx,REG_SZ
from win32gui import GetForegroundWindow, ShowWindow
from win32con import SW_HIDE, SW_SHOW, WM_APP
import win32process
import psutil
from win32api import SendMessage
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import wx
import wx.adv
from win11toast import notify
import sys

key_map = {
    "A": 65,
    "B": 66,
    "C": 67,
    "D": 68,
    "E": 69,
    "F": 70,
    "G": 71,
    "H": 72,
    "I": 73,
    "J": 74,
    "K": 75,
    "L": 76,
    "M": 77,
    "N": 78,
    "O": 79,
    "P": 80,
    "Q": 81,
    "R": 82,
    "S": 83,
    "T": 84,
    "U": 85,
    "V": 86,
    "W": 87,
    "X": 88,
    "Y": 89,
    "Z": 90,
    "0": 48,
    "1": 49,
    "2": 50,
    "3": 51,
    "4": 52,
    "5": 53,
    "6": 54,
    "7": 55,
    "8": 56,
    "9": 57,
    ".": 46,
    ",": 44,
    "/": 47,
    ";": 59,
    "'": 39,
    "[": 91,
    "]": 93,
    "Num 0": wx.WXK_NUMPAD0,
    "Num 1": wx.WXK_NUMPAD1,
    "Num 2": wx.WXK_NUMPAD2,
    "Num 3": wx.WXK_NUMPAD3,
    "Num 4": wx.WXK_NUMPAD4,
    "Num 5": wx.WXK_NUMPAD5,
    "Num 6": wx.WXK_NUMPAD6,
    "Num 7": wx.WXK_NUMPAD7,
    "Num 8": wx.WXK_NUMPAD8,
    "Num 9": wx.WXK_NUMPAD9,
    "Up": wx.WXK_UP,
    "Down": wx.WXK_DOWN,
    "Left": wx.WXK_LEFT,
    "Right": wx.WXK_RIGHT,
    "F1": wx.WXK_F1,
    "F2": wx.WXK_F2,
    "F3": wx.WXK_F3,
    "F4": wx.WXK_F4,
    "F5": wx.WXK_F5,
    "F6": wx.WXK_F6,
    "F7": wx.WXK_F7,
    "F8": wx.WXK_F8,
    "F9": wx.WXK_F9,
    "F10": wx.WXK_F10,
    "F11": wx.WXK_F11,
    "F12": wx.WXK_F12,
    "Space": wx.WXK_SPACE,
    "Esc": wx.WXK_ESCAPE,
    "Tab": wx.WXK_TAB,
    "Caps Lock": wx.WXK_CAPITAL,
    "Delete": wx.WXK_DELETE,
    "Insert": wx.WXK_INSERT,
    "Home": wx.WXK_HOME,
    "End": wx.WXK_END,
    "Page Up": wx.WXK_PAGEUP,
    "Page Down": wx.WXK_PAGEDOWN
}

key_mod_map = {
    "Ctrl": wx.MOD_CONTROL,
    "Alt": wx.MOD_ALT,
    "Shift": wx.MOD_SHIFT,
    "Win": wx.MOD_WIN
}

modifiers_map = {
    1: "Alt",
    2: "Ctrl",
    4: "Shift",
    8: "Win",
}
class SettingWindow(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, title="Boss-Key")
        self.SetIcon(wx.Icon(wx.Image(Config.icon).ConvertToBitmap()))
        
        self.init_UI()

        self.Bind_EVT()
        self.SetData()
        self.SetSize((650, 350))

        self.Center()


    def init_UI(self):
        # 创建面板
        panel = wx.Panel(self)

        # 创建布局管理器
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        #设置隐显窗口热键（SW)
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        SW_label = wx.StaticText(panel, label="隐藏/显示窗口热键:")
        self.SW_choice = wx.Choice(panel, -1, choices = list(key_mod_map.keys()))
        self.SW2_choice = wx.Choice(panel, -1, choices = list(key_map.keys()))
        hbox1.Add(SW_label, proportion=1, flag=wx.LEFT, border=10)
        hbox1.Add(self.SW_choice , proportion=1, flag=wx.EXPAND|wx.LEFT, border=10)
        hbox1.Add(self.SW2_choice , proportion=1, flag=wx.EXPAND|wx.RIGHT, border=10)
        vbox.Add(hbox1, proportion=1, flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=10)
        
        #设置自启热键（CS)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        CS_label = wx.StaticText(panel, label="修改自启动热键:")
        self.CS_choice = wx.Choice(panel, -1, choices = list(key_mod_map.keys()))
        self.CS2_choice = wx.Choice(panel, -1, choices = list(key_map.keys()))
        hbox2.Add(CS_label, proportion=1, flag=wx.LEFT, border=10)
        hbox2.Add(self.CS_choice , proportion=1, flag=wx.EXPAND|wx.LEFT, border=10)
        hbox2.Add(self.CS2_choice , proportion=1, flag=wx.EXPAND|wx.RIGHT, border=10)
        vbox.Add(hbox2, proportion=1, flag=wx.EXPAND|wx.BOTTOM, border=10)

        
        #设置关闭热键（CL）
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        CL_label = wx.StaticText(panel, label="一键关闭程序热键:")
        self.CL_choice = wx.Choice(panel, -1, choices = list(key_mod_map.keys()))
        self.CL2_choice = wx.Choice(panel, -1, choices = list(key_map.keys()))
        hbox3.Add(CL_label, proportion=1, flag=wx.LEFT, border=10)
        hbox3.Add(self.CL_choice , proportion=1, flag=wx.EXPAND|wx.LEFT, border=10)
        hbox3.Add(self.CL2_choice , proportion=1, flag=wx.EXPAND|wx.RIGHT, border=10)
        vbox.Add(hbox3, proportion=1, flag=wx.EXPAND|wx.BOTTOM, border=10)

        # 设置提示1
        # hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        # StaticText1=wx.StaticText(panel,label="录制时，所有热键将失效，保存后恢复")
        # hbox4.Add(StaticText1, proportion=1, flag=wx.LEFT, border=10)
        # vbox.Add(hbox4, proportion=1, flag=wx.EXPAND|wx.BOTTOM, border=10)
        
        #设置提示2
        if Config.first_start:
            hbox6 = wx.BoxSizer(wx.HORIZONTAL)
            StaticText2=wx.StaticText(panel,label="本页面仅在首次启动时自动显示，后续可通过托盘图标打开本页面")
            hbox6.Add(StaticText2, proportion=1, flag=wx.LEFT, border=10)
            vbox.Add(hbox6, proportion=1, flag=wx.EXPAND|wx.BOTTOM, border=10)
        
        # 创建复选框
        hbox7 = wx.BoxSizer(wx.HORIZONTAL)
        Mute_after_hide_label = wx.StaticText(panel, label="隐藏窗口后静音")
        self.Mute_after_hide_checkbox = wx.CheckBox(panel, -1, "")
        hbox7.Add(Mute_after_hide_label, proportion=1, flag=wx.LEFT, border=10)
        hbox7.Add(self.Mute_after_hide_checkbox, proportion=1, flag=wx.LEFT, border=10)
        vbox.Add(hbox7, proportion=1, flag=wx.BOTTOM, border=10)

        # 创建按钮
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.Reset_btn = wx.Button(panel,size=(100,60), label="重置热键")
        self.Save_btn = wx.Button(panel,size=(100,60), label="保存热键")
        hbox5.Add(self.Reset_btn, proportion=1, flag=wx.LEFT, border=20)
        hbox5.Add(self.Save_btn, proportion=1, flag=wx.RIGHT, border=20)
        vbox.Add(hbox5, proportion=1, flag=wx.EXPAND|wx.BOTTOM, border=10)


        panel.SetSizer(vbox)

    def Bind_EVT(self):
        self.Save_btn.Bind(wx.EVT_BUTTON, self.OnSave)
        self.Reset_btn.Bind(wx.EVT_BUTTON,self.OnReset)
        # self.Bind(wx.EVT_CLOSE,self.OnClose)

    def SetData(self):
        self.SW_choice.SetStringSelection(Config.hide_f)
        self.SW2_choice.SetStringSelection(Config.hide_v)
        self.CS_choice.SetStringSelection(Config.startup_f)
        self.CS2_choice.SetStringSelection(Config.startup_v)
        self.CL_choice.SetStringSelection(Config.close_f)
        self.CL2_choice.SetStringSelection(Config.close_v)
        self.Mute_after_hide_checkbox.SetValue(bool(Config.mute_after_hide))

    def OnSave(self,e):
        Config.hide_f=self.SW_choice.GetStringSelection()
        Config.hide_v=self.SW2_choice.GetStringSelection()
        Config.startup_f=self.CS_choice.GetStringSelection()
        Config.startup_v=self.CS2_choice.GetStringSelection()
        Config.close_f=self.CL_choice.GetStringSelection()
        Config.close_v=self.CL2_choice.GetStringSelection()
        Config.HotkeyWindow.reBind()
        Config.mute_after_hide=self.Mute_after_hide_checkbox.GetValue()
        save_config()
        wx.MessageDialog(None, u"保存成功", u"Boss_Key", wx.OK | wx.ICON_INFORMATION).ShowModal()

    def OnReset(self,e):
        self.SW_choice.SetStringSelection("Ctrl")
        self.SW2_choice.SetStringSelection("Q")
        self.CS_choice.SetStringSelection("Alt")
        self.CS2_choice.SetStringSelection("Q")
        self.CL_choice.SetStringSelection("Ctrl")
        self.CL2_choice.SetStringSelection(".")
        wx.MessageDialog(None, u"已重置选项，请保存热键以启用", u"Boss_Key", wx.OK | wx.ICON_INFORMATION).ShowModal()

class HotkeyWindow(wx.Frame):
    def __init__(self):
        try:
            ShowWindow(Config.hwnd, SW_SHOW)
            self.changeMute(Config.hwnd,0)
        except:
            pass
        wx.Frame.__init__(self, None, title="Boss-Key")
        self.sendNotify("Boss Key正在运行！", "Boss Key正在为您服务，您可通过托盘图标看到我")
        self.reBind()
    
    def reBind(self):#没考虑重复等情况
        self.regHotKey()
        self.BindHotKey()

    def regHotKey(self):
        self.RegisterHotKey(1, key_mod_map[Config.hide_f], key_map[Config.hide_v])#hide-1
        self.RegisterHotKey(2, key_mod_map[Config.startup_f], key_map[Config.startup_v])#startup-2
        self.RegisterHotKey(3, key_mod_map[Config.close_f], key_map[Config.close_v])#close-3

    def BindHotKey(self):
        self.Bind(wx.EVT_HOTKEY, self.onHide, id = 1)
        self.Bind(wx.EVT_HOTKEY, self.onStartup, id = 2)
        self.Bind(wx.EVT_HOTKEY, self.onClose, id = 3)

    def onHide(self,e=""):
        Config.hwnd_n = GetForegroundWindow()
        if Config.times == 1:
            # 隐藏窗口
            ShowWindow(Config.hwnd_n, SW_HIDE)
            if Config.mute_after_hide:
                self.changeMute(Config.hwnd_n,1)
            Config.hwnd_b=Config.hwnd_n
            Config.hwnd=Config.hwnd_b
            Config.times = 0
        else:
            # 显示窗口
            ShowWindow(Config.hwnd_b, SW_SHOW)
            if Config.mute_after_hide:
                self.changeMute(Config.hwnd_b,0)
            Config.hwnd_b = ""
            Config.times = 1
        save_config()

    def changeMute(self,hwnd,flag=1):
        """
        flag=1 mute
        """
        # print(hwnd)
        # SendMessage(int(hwnd),0x319, 0x200eb0, 0x08*0x10000)
        hwnd=int(hwnd)
        process=win32process.GetWindowThreadProcessId(hwnd)
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session.SimpleAudioVolume
            # if session.Process:
            #     print(session.Process.pid)
            #     print("process[1]",psutil.Process(process[1]))
            #     print("session.Process",session.Process)
            if session.Process and session.Process.name() == psutil.Process(process[1]).name():
                print("mute")
                volume.SetMute(flag, None)
                break
    def onStartup(self,e=""):
        try:
            res = self.modifyStartup("Boss Key Application",file_path=Config.file_path)
            if res == "Added":
                self.sendNotify(title="开机自启状态变化",message="Boss Key开机自启已开启")
            elif res == "Removed":
                self.sendNotify(title="开机自启状态变化",message="Boss Key开机自启已关闭")
            else:
                self.sendNotify(title="开机自启状态变化",message="Boss Key开机自启状态未知")
        except:
            self.sendNotify(title="程序运行出错",message=f"Boss Key程序运行出错，请尝试按下{Config.close_f}+{Config.close_v}重启程序")
    def onClose(self,e=""):
        self.sendNotify("Boss Key已停止服务", "Boss Key已成功退出")
        if Config.times == 0:
            ShowWindow(Config.hwnd_b, SW_SHOW)
            Config.hwnd_b = ""
            Config.times = 1
            
        wx.GetApp().Destroy()
        try:
            Config.TaskBarIcon.Destroy()
        except:
            pass
        try:            
            Config.SettingWindow.Close()
        except:
            pass
        try:
            self.Destroy()
        except:
            pass
        sys.exit(0)
        

    def modifyStartup(self,name: str, file_path: str):
        key = OpenKey(HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, KEY_ALL_ACCESS)
        try:
            existing_value, _ = QueryValueEx(key, name)

            if existing_value == file_path:
                DeleteValue(key, name)
                CloseKey(key)
                return "Removed"
            else:
                SetValueEx(key, name, 0, REG_SZ, file_path)
                return "Added"
        except WindowsError:
            SetValueEx(key, name, 0, REG_SZ, file_path)
            return "Added"

    def sendNotify(self,title,message):
        notify(title,message,icon=Config.icon_info,duration="short")
    

class TaskBarIcon(wx.adv.TaskBarIcon):

    MENU_ID1,MENU_ID2 = wx.NewIdRef(count=2)

    def __init__(self):
        super().__init__()
        self.Icon = wx.Icon(wx.Image(Config.icon).ConvertToBitmap())
        # 设置图标和提示
        self.SetIcon(self.Icon, 'Boss Key')

        # 绑定菜单项事件
        self.Bind(wx.EVT_MENU, self.onOne, id=self.MENU_ID1)
        self.Bind(wx.EVT_MENU, self.onExit, id=self.MENU_ID2)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.MENU_ID1, '设置')
        menu.Append(self.MENU_ID2, '退出')
        return menu

    def onOne(self,e):
        Config.SettingWindow.Show()

    def onExit(self,e):
        try:
            Config.SettingWindow.Close()
        except:
            pass
        Config.HotkeyWindow.onClose()

class BossKey():
    def __init__(self):
        app = wx.App()
        Config.HotkeyWindow=HotkeyWindow()
        Config.SettingWindow=SettingWindow()
        Config.TaskBarIcon=TaskBarIcon()
        if Config.first_start:
            Config.SettingWindow.Show()
        app.MainLoop()

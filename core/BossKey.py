from core.config import Config,save_config
from winreg import OpenKey,HKEY_CURRENT_USER,QueryValueEx,DeleteValue,CloseKey,KEY_ALL_ACCESS,SetValueEx,REG_SZ
from win32gui import GetForegroundWindow, ShowWindow
from win32con import SW_HIDE, SW_SHOW, WM_APP
from win32api import SendMessage
import win32api,win32con,win32gui
import win32process
import psutil
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import wx
import wx.adv
from win11toast import notify
import sys
from pynput import keyboard, mouse
import threading
import time
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
        self.SW_text = wx.TextCtrl(panel, -1, value=Config.hide_hotkey)
        self.SW_record_btn = wx.Button(panel, -1, label="录制热键")
        hbox1.Add(SW_label, proportion=1, flag=wx.LEFT, border=10)
        hbox1.Add(self.SW_text, proportion=1, flag=wx.EXPAND|wx.LEFT, border=10)
        hbox1.Add(self.SW_record_btn, proportion=1, flag=wx.EXPAND|wx.RIGHT, border=10)
        vbox.Add(hbox1, proportion=1, flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=10)
        
        #设置自启动热键（CS)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        CS_label = wx.StaticText(panel, label="修改自启动热键:")
        self.CS_text = wx.TextCtrl(panel, -1, value=Config.startup_hotkey)
        self.CS_record_btn = wx.Button(panel, -1, label="录制热键")
        hbox2.Add(CS_label, proportion=1, flag=wx.LEFT, border=10)
        hbox2.Add(self.CS_text, proportion=1, flag=wx.EXPAND|wx.LEFT, border=10)
        hbox2.Add(self.CS_record_btn, proportion=1, flag=wx.EXPAND|wx.RIGHT, border=10)
        vbox.Add(hbox2, proportion=1, flag=wx.EXPAND|wx.BOTTOM, border=10)

        
        #设置关闭热键（CL）
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        CL_label = wx.StaticText(panel, label="一键关闭程序热键:")
        self.CL_text = wx.TextCtrl(panel, -1, value=Config.close_hotkey)
        self.CL_record_btn = wx.Button(panel, -1, label="录制热键")
        hbox3.Add(CL_label, proportion=1, flag=wx.LEFT, border=10)
        hbox3.Add(self.CL_text, proportion=1, flag=wx.EXPAND|wx.LEFT, border=10)
        hbox3.Add(self.CL_record_btn, proportion=1, flag=wx.EXPAND|wx.RIGHT, border=10)
        vbox.Add(hbox3, proportion=1, flag=wx.EXPAND|wx.BOTTOM, border=10)


        #隐藏前发送热键（HS）
        hbox8 = wx.BoxSizer(wx.HORIZONTAL)
        HS_label = wx.StaticText(panel, label="隐藏前发送热键（beta）:")
        self.HS_text = wx.TextCtrl(panel, -1, value=Config.hide_send_hotkey)
        self.HS_record_btn = wx.Button(panel, -1, label="录制热键")
        hbox8.Add(HS_label, proportion=1, flag=wx.LEFT, border=10)
        hbox8.Add(self.HS_text, proportion=1, flag=wx.EXPAND|wx.LEFT, border=10)
        hbox8.Add(self.HS_record_btn, proportion=1, flag=wx.EXPAND|wx.RIGHT, border=10)
        vbox.Add(hbox8, proportion=1, flag=wx.EXPAND|wx.BOTTOM, border=10)

        # 设置提示1
        # hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        # StaticText1=wx.StaticText(panel,label="录制时，所有热键将失效，保存后恢复")
        # hbox4.Add(StaticText1, proportion=1, flag=wx.LEFT, border=10)
        # vbox.Add(hbox4, proportion=1, flag=wx.EXPAND|wx.BOTTOM, border=10)
        
        #设置提示2
        if Config.first_start:
            hbox6 = wx.BoxSizer(wx.HORIZONTAL)
            StaticText2=wx.StaticText(panel,label="本页面仅在首次启动或内容有更新时自动显示，后续可通过托盘图标打开本页面")
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
        self.SW_record_btn.Bind(wx.EVT_BUTTON, self.OnRecordSW)
        self.CS_record_btn.Bind(wx.EVT_BUTTON, self.OnRecordCS)
        self.CL_record_btn.Bind(wx.EVT_BUTTON, self.OnRecordCL)
        self.HS_record_btn.Bind(wx.EVT_BUTTON, self.OnRecordHS)
        # self.Bind(wx.EVT_CLOSE,self.OnClose)

    def SetData(self):
        self.SW_text.SetValue(Config.hide_hotkey)
        self.CS_text.SetValue(Config.startup_hotkey)
        self.CL_text.SetValue(Config.close_hotkey)
        self.HS_text.SetValue(Config.hide_send_hotkey)
        self.Mute_after_hide_checkbox.SetValue(bool(Config.mute_after_hide))

    def OnSave(self,e):
        Config.hide_hotkey = self.SW_text.GetValue()
        Config.startup_hotkey = self.CS_text.GetValue()
        Config.close_hotkey = self.CL_text.GetValue()
        Config.hide_send_hotkey = self.HS_text.GetValue()
        Config.HotkeyWindow.reBind()
        Config.mute_after_hide = self.Mute_after_hide_checkbox.GetValue()
        save_config()
        wx.MessageDialog(None, u"保存成功", u"Boss_Key", wx.OK | wx.ICON_INFORMATION).ShowModal()

    def OnReset(self,e):
        self.SW_text.SetValue("Ctrl+Q")
        self.CS_text.SetValue("Alt+Q")
        self.CL_text.SetValue("Win+Esc")
        self.HS_text.SetValue("Space")
        wx.MessageDialog(None, u"已重置选项，请保存热键以启用", u"Boss_Key", wx.OK | wx.ICON_INFORMATION).ShowModal()

    def OnRecordSW(self, e):
        self.recordHotkey(self.SW_text)

    def OnRecordCS(self, e):
        self.recordHotkey(self.CS_text)

    def OnRecordCL(self, e):
        self.recordHotkey(self.CL_text)

    def OnRecordHS(self, e):
        self.recordHotkey(self.HS_text)

    def recordHotkey(self, text_ctrl):
        self.recording = True
        self.keys_pressed = set()
        self.keys_recorded = set()
        self.mouse_pressed = set()
        text_ctrl.SetValue("请按下热键组合...")

        self.keyboard_listener = keyboard.Listener(
            on_press=self.onKeyPress,
            on_release=self.onKeyRelease)
        # self.mouse_listener = mouse.Listener(
            # on_click=self.onClick)
        self.keyboard_listener.start()
        # self.mouse_listener.start()

        self.text_ctrl = text_ctrl

    def onKeyPress(self, key):
        key_name = self.getKeyName(key)
        self.keys_pressed.add(key_name)
        self.keys_recorded.add(key_name)

    def onKeyRelease(self, key):
        key_name = self.getKeyName(key)
        if key_name in self.keys_pressed:
            self.keys_pressed.remove(key_name)
        self.checkStopRecording()

    def onClick(self, x, y, button, pressed):
        button_name = button.name.upper()
        if pressed:
            self.mouse_pressed.add(button_name)
            self.keys_recorded.add(button_name)
        else:
            if button_name in self.mouse_pressed:
                self.mouse_pressed.remove(button_name)
        self.checkStopRecording()

    def checkStopRecording(self):
        if not self.keys_pressed and not self.mouse_pressed:
            self.stopRecording()
            hotkey_str = "+".join(sorted(self.keys_recorded))
            self.text_ctrl.SetValue(hotkey_str)

    def stopRecording(self):
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None
        # if self.mouse_listener:
        #     self.mouse_listener.stop()
        #     self.mouse_listener = None
        self.recording = False

    def getKeyName(self, key):
        if hasattr(key, 'char') and key.char is not None:
            return key.char.upper()
        elif hasattr(key, 'name') and key.name is not None:
            key_name = key.name.lower()
            if key_name in ('ctrl_l', 'ctrl_r'):
                return 'Ctrl'
            elif key_name in ('alt_l', 'alt_r', 'alt_gr'):
                return 'Alt'
            elif key_name in ('shift_l', 'shift_r'):
                return 'Shift'
            elif key_name == 'esc':
                return 'Esc'
            elif key_name == 'enter':
                return 'Enter'
            elif key_name == 'cmd':
                return 'Win'
            elif key_name == 'button.middle':
                return 'MIDDLE'
            else:
                return key.name.upper()
        else:
            return str(key).upper()

class HotkeyWindow():
    def __init__(self):
        try:
            ShowWindow(Config.hwnd, SW_SHOW)
            self.changeMute(Config.hwnd,0)
        except:
            pass
        self.sendNotify("Boss Key正在运行！", "Boss Key正在为您服务，您可通过托盘图标看到我")
        self.listener = None
        self.reBind()
    
    def reBind(self):
        if self.listener:
            self.listener.stop()
        self.BindHotKey()

    def expandHotkeys(self):
        expanded_hotkeys = {}
        need_check = {}
        flag = True
        # 将self.hotkeys中的每一项的键修改为小写
        for hotkey, action in self.hotkeys.items():
            hotkey = hotkey.lower()
            need_check[hotkey] = action
        while flag:
            flag = False
            this_round = need_check.copy()
            function_keys=[
                'ctrl',
                'alt',
                'shift',
                'esc',
                'enter',
                'cmd',
                'page_up',
                'page_down',
                'home',
                'end',
                'insert',
                'delete',
                'backspace',
                'space',
                'up',
                'down',
                'left',
                'right',
                'tab',
                'caps_lock',
                'num_lock',
                'scroll_lock',
                'print_screen',
                'pause',
                'menu'
            ]
            for i in range(1,13):
                function_keys.append(f'f{i}')
            for hotkey, action in this_round.items():
                hotkey = hotkey.lower()
                keys = hotkey.split('+')
                intersect = list(set(keys) & set(function_keys))
                if len(intersect)>=1:
                    i=intersect[0]
                    del need_check['+'.join(keys)]
                    keys.remove(i)
                    keys.append(f"<{i}>")
                    need_check['+'.join(keys)] = action
                    flag = True
                    continue

                if 'win' in keys:
                    del need_check['+'.join(keys)]
                    keys.remove('win')
                    keys.append('<cmd>')
                    need_check['+'.join(keys)] = action
                    flag = True
                    continue
                else:
                    expanded_hotkeys['+'.join(keys)] = action

        self.hotkeys = expanded_hotkeys

    def BindHotKey(self):
        self.hotkeys = {
            Config.hide_hotkey: self.onHide,
            Config.startup_hotkey: self.onStartup,
            Config.close_hotkey: self.onClose
        }
        self.expandHotkeys()
        print(self.hotkeys)
        self.listener = keyboard.GlobalHotKeys(self.hotkeys)
        self.listener.start()

    def onHide(self,e=""):
        Config.hwnd_n = GetForegroundWindow()
        if Config.times == 1:
            # 发送热键
            # if Config.hide_send_hotkey:
            #     print("send")
            #     try:
            #         keyboard.Controller().tap(keyboard.Key.space)
            #     except Exception as e:
            #         print(e)
            #         pass
            # time.sleep(0.25)
            if Config.hide_send_hotkey:
                
                win32api.SendMessage(Config.hwnd_n, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0)
                time.sleep(2)
                win32api.SendMessage(Config.hwnd_n, win32con.WM_KEYUP, win32con.VK_SPACE, 0)
                time.sleep(2)
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
            self.sendNotify(title="程序运行出错",message=f"Boss Key程序运行出错，请尝试按下{Config.close_hotkey}重启程序")

    def onClose(self,e=""):
        self.sendNotify("Boss Key已停止服务", "Boss Key已成功退出")
        if Config.times == 0:
            ShowWindow(Config.hwnd_b, SW_SHOW)
            Config.hwnd_b = ""
            Config.times = 1
            
        if self.listener:
            self.listener.stop()
        try:
            Config.TaskBarIcon.Destroy()
            Config.SettingWindow.Destroy()
        except:
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
        Config.HotkeyWindow.onClose()
        sys.exit(0)

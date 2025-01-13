# nuitka-project: --onefile
# nuitka-project: --windows-console-mode=disable
# nuitka-project: --standalone
# nuitka-project: --follow-import-to=core
# nuitka-project: --windows-icon-from-ico=icon.ico
# nuitka-project: --windows-product-name="Boss Key"
# nuitka-project: --windows-file-description="Boss Key Application"
# nuitka-project: --copyright="Copyright (C) 2025 Ivan Hanloth All Rights Reserved. "
# nuitka-project: --windows-company-name="Ivan Hanloth"

from GUI import setting, taskbar
from core import listener
import sys
import ctypes
import os
import psutil
import wx
from core.config import Config

ctypes.windll.shcore.SetProcessDpiAwareness(2) # Win10 and Win8
ctypes.windll.user32.SetProcessDPIAware() #Win7 and below

class APP(wx.App):
    def __init__(self):
        wx.App.__init__(self)
        
        # 设置语言环境为中文
        self.locale = wx.Locale(wx.LANGUAGE_CHINESE_SIMPLIFIED)
        self.SetAppName(Config.AppName)
        self.SetAppDisplayName(Config.AppName)
        self.SetVendorName(Config.AppAuthor)
        lock=os.path.join(os.path.dirname(sys.argv[0]),"Boss-Key.lock")
        if self.is_already_running(lock):
            ask=wx.MessageBox("Boss Key 可能已在运行\n点击“确定”继续运行新的Boss-Key程序\n点击“取消”直接关闭此窗口","Boss Key", wx.OK | wx.ICON_INFORMATION | wx.CANCEL | wx.CANCEL_DEFAULT)
            if ask==wx.OK:
                os.remove(lock)
                self.is_already_running(lock)
            else:
                sys.exit(0)

    def write_pid(self,name):
        with open(name, "w") as f:
            f.write(str(psutil.Process().pid))

    def is_already_running(self,name):
        if os.path.exists(name):
            with open(name, "r") as f:
                pid=f.read()
            if pid == "":
                self.write_pid(name)
            else:
                try:
                    process=psutil.Process(int(pid))
                    if process.is_running():
                        this_name=psutil.Process(psutil.Process().pid).name() #获取当前进程名
                        if this_name==process.name():
                            return True
                        else:
                            self.write_pid(name)
                            return False
                    else:
                        self.write_pid(name)
                        return False
                except:
                    self.write_pid(name)
                    return False
        else:
            self.write_pid(name)

if __name__ == '__main__':
    app = APP()
    Config.TaskBarIcon=taskbar.TaskBarIcon()
    Config.HotkeyListener=listener.HotkeyListener()
    Config.SettingWindow=setting.SettingWindow()
    if Config.first_start:
        Config.SettingWindow.Show()
    app.MainLoop()
    

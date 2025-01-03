import wx, wx.adv
from core.config import Config
import core.tools as tool
from GUI import about
import sys

class TaskBarIcon(wx.adv.TaskBarIcon):

    MENU_SETTING,MENU_EXIT,MENU_STARTUP,MENU_UPDATE = wx.NewIdRef(count=4)

    def __init__(self):
        super().__init__()
        self.Icon = wx.Icon(wx.Image(Config.icon).ConvertToBitmap())
        # 设置图标和提示
        self.SetIcon(self.Icon, 'Boss Key')
        self.BindEVT()

    def BindEVT(self):
        # 绑定菜单项事件
        self.Bind(wx.EVT_MENU, self.onSetting, id=self.MENU_SETTING)
        self.Bind(wx.EVT_MENU, self.onStartup, id=self.MENU_STARTUP)
        self.Bind(wx.EVT_MENU, self.onExit, id=self.MENU_EXIT)
        self.Bind(wx.EVT_MENU, self.onAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.onUpdate, id=self.MENU_UPDATE)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.MENU_SETTING, '设置')
        menu.Append(self.MENU_STARTUP, '开机自启', kind=wx.ITEM_CHECK)
        menu.Check(self.MENU_STARTUP, tool.checkStartup("Boss Key Application",Config.file_path))
        menu.AppendSeparator()
        menu.Append(self.MENU_UPDATE, '检查更新')
        menu.Append(wx.ID_ABOUT, '关于')
        menu.AppendSeparator()
        menu.Append(self.MENU_EXIT, '退出')
        return menu
    
    def onStartup(self,e):
        try:
            res = tool.modifyStartup("Boss Key Application",file_path=Config.file_path)
            if res == "Added":
                tool.sendNotify(title="开机自启状态变化",message="Boss Key开机自启已开启")
            elif res == "Removed":
                tool.sendNotify(title="开机自启状态变化",message="Boss Key开机自启已关闭")
            else:
                tool.sendNotify(title="开机自启状态变化",message="Boss Key开机自启状态未知")
        except:
            tool.sendNotify(title="程序运行出错",message=f"Boss Key程序运行出错，请尝试重启程序")

    def onSetting(self,e):
        Config.SettingWindow.Show()

    def onAbout(self,e):
        about.AboutWindow().Show()

    def onExit(self,e):
        Config.HotkeyWindow.Close()
        sys.exit(0)

    def onUpdate(self,e):
        if Config.UpdateWindow!="":
            Config.UpdateWindow.Show()
        else:
            Config.UpdateWindow=about.UpdateWindow()
            Config.UpdateWindow.Show()

import wx, wx.adv
from core.config import Config
import core.tools as tool
import sys

class TaskBarIcon(wx.adv.TaskBarIcon):

    MENU_SETTING,MENU_EXIT,MENU_STARTUP = wx.NewIdRef(count=3)

    def __init__(self):
        super().__init__()
        self.Icon = wx.Icon(wx.Image(Config.icon).ConvertToBitmap())
        # 设置图标和提示
        self.SetIcon(self.Icon, 'Boss Key')
        self.BindEVT()

    def BindEVT(self):
        # 绑定菜单项事件
        self.Bind(wx.EVT_MENU, self.onSetting, id=self.MENU_SETTING)
        self.Bind(wx.EVT_MENU, self.onExit, id=self.MENU_EXIT)
        self.Bind(wx.EVT_MENU, self.onStartup, id=self.MENU_STARTUP)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.MENU_SETTING, '设置')
        menu.Append(self.MENU_STARTUP, '开机自启', kind=wx.ITEM_CHECK)
        menu.Check(self.MENU_STARTUP, tool.checkStartup("Boss Key Application",Config.file_path))
        # menu.Append(wx.ID_ABOUT, '关于')
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
            tool.sendNotify(title="程序运行出错",message=f"Boss Key程序运行出错，请尝试按下{Config.close_hotkey}重启程序")

    def onSetting(self,e):
        Config.SettingWindow.Show()

    def onExit(self,e):
        Config.HotkeyWindow.onClose()
        sys.exit(0)

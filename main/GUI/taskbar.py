import wx, wx.adv
from core.config import Config
import core.tools as tool
from GUI import about
from GUI.window_restore import WindowRestoreDialog
import sys

class TaskBarIcon(wx.adv.TaskBarIcon):

    MENU_SETTING, MENU_EXIT, MENU_STARTUP, MENU_UPDATE, MENU_RESTORE = wx.NewIdRef(count=5)
    ID_RESTORE = wx.NewIdRef(count=1)

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
        self.Bind(wx.EVT_MENU, self.onRestore, id=self.MENU_RESTORE)
        # 绑定任务栏图标单击事件
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.onLeftClick)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.MENU_SETTING, '设置')
        menu.Append(self.MENU_STARTUP, '开机自启', kind=wx.ITEM_CHECK)
        menu.Check(self.MENU_STARTUP, tool.checkStartup("Boss Key Application", Config.file_path))
        menu.AppendSeparator()
        menu.Append(self.MENU_RESTORE, '窗口恢复工具')
        menu.Append(self.MENU_UPDATE, '检查更新')
        menu.Append(wx.ID_ABOUT, '关于')
        menu.AppendSeparator()
        menu.Append(self.MENU_EXIT, '退出')
        return menu
    
    def onLeftClick(self, e=''):
        if Config.click_to_hide:
            if Config.HotkeyListener != "":
                Config.HotkeyListener.onHide()

    def onStartup(self, e):
        if tool.checkStartup("Boss Key Application", Config.file_path):
            if tool.removeStartup("Boss Key Application"):
                tool.sendNotify(title="开机自启状态变化", message="Boss Key开机自启已关闭")
            else:
                tool.sendNotify(title="开机自启状态变化", message="Boss Key开机自启关闭失败")
        else:
            if tool.addStartup("Boss Key Application", Config.file_path):
                tool.sendNotify(title="开机自启状态变化", message="Boss Key开机自启已开启")
            else:
                tool.sendNotify(title="开机自启状态变化", message="Boss Key开机自启开启失败")

    def onSetting(self, e):
        window=wx.FindWindowById(Config.SettingWindowId)
        window.RefreshLeftList()
        window.Show()

    def onAbout(self, e):
        about.AboutWindow().Show()

    def onExit(self, e):
        Config.HotkeyListener.Close()

    def onUpdate(self, e):
        if Config.UpdateWindowId != -1:
            wx.FindWindowById(Config.UpdateWindowId).Show()
        else:
            about.UpdateWindow(Config.UpdateWindowId).Show()

    def onRestore(self, e):
        """显示窗口恢复对话框"""
        dialog = wx.FindWindowById(self.ID_RESTORE)
        if dialog is None:
            WindowRestoreDialog(self.ID_RESTORE).Show()
        else:
            dialog.Restore()
            dialog.Raise()
            dialog.RefreshLeftList()

    def HideIcon(self):
        wx.CallAfter(self.RemoveIcon)

    def ShowIcon(self):
        wx.CallAfter(self.SetIcon, self.Icon, 'Boss Key')

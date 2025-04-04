import wx
import wx.adv
from core.tools import *
import threading
from core.config import Config
import webbrowser
import datetime

class AboutWindow():
    def __init__(self):
        self.info = wx.adv.AboutDialogInfo()
        self.info.SetName(Config.AppName)
        self.info.SetVersion(Config.AppVersion)
        self.info.SetIcon(wx.Icon(wx.Image(Config.icon).ConvertToBitmap()))
        self.info.SetCopyright(Config.AppCopyRight)
        self.info.SetWebSite(Config.AppWebsite)
        self.info.SetLicence(Config.AppLicense)
        self.info.AddDeveloper(Config.AppAuthor)
        self.info.SetDescription(Config.AppDescription)
        
    def Show(self):
        wx.adv.AboutBox(self.info)

class UpdateWindow(wx.Dialog):
    # 定义组件ID常量
    ID_ACTIVITY_INDICATOR = wx.NewId()
    ID_INFO_TEXT = wx.NewId()
    ID_CURRENT_VERSION = wx.NewId()
    ID_NEW_VERSION = wx.NewId()
    ID_RELEASE_TIME = wx.NewId()
    ID_INFO_LABEL = wx.NewId()
    ID_INFO_TEXT_CTRL = wx.NewId()
    
    def __init__(self):
        super().__init__(None, title="检查更新 - Boss Key", style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP | wx.RESIZE_BORDER)
        self.SetIcon(wx.Icon(wx.Image(Config.icon).ConvertToBitmap()))
        
        self.init_Load_UI()

        self.SetSize((500, 600))

        self.Center()
        
        self.onCheckUpdate()

    def init_Load_UI(self):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        ai = wx.ActivityIndicator(panel, id=self.ID_ACTIVITY_INDICATOR)
        ai.Start()

        text = wx.StaticText(panel, id=self.ID_INFO_TEXT, label="正在获取版本信息，请稍后...")

        # 使元素完全居中
        sizer.AddStretchSpacer(3)
        sizer.Add(ai, 0, wx.ALIGN_CENTER)
        sizer.AddStretchSpacer()
        sizer.Add(text, 0, wx.ALIGN_CENTER)
        sizer.AddStretchSpacer(3)
        panel.SetSizer(sizer)

    def onCheckUpdate(self):
        def checkUpdate():
            try:
                info = checkUpdate()
            except:
                wx.CallAfter(self.init_error_UI)
                return
            
            wx.CallAfter(self.init_real_UI, info)
        threading.Thread(target=checkUpdate).start()

    def init_real_UI(self, info):
        ## 清空原有元素
        self.sizer.Clear()
        self.ai.Stop()
        self.ai.Destroy()

        for i in self.panel.GetChildren():
            i.Destroy()

        ## 重绘UI

        current_version = wx.StaticText(self.panel, id=self.ID_CURRENT_VERSION, label="当前版本："+Config.AppVersion)
        self.sizer.Add(current_version, 0, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL, 5)
        
        new_version = wx.StaticText(self.panel, id=self.ID_NEW_VERSION, label="最新版本："+info['tag_name'])
        self.sizer.Add(new_version, 0, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL, 5)

        release_time = wx.StaticText(self.panel, id=self.ID_RELEASE_TIME, label="发布时间："+datetime.datetime.strftime(info['published_at'], "%Y-%m-%d %H:%M:%S"))
        self.sizer.Add(release_time, 0, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL, 5)

        info_label = wx.StaticText(self.panel, id=self.ID_INFO_LABEL, label="更新内容：")
        info_text = wx.TextCtrl(self.panel, id=self.ID_INFO_TEXT_CTRL, style=wx.TE_MULTILINE | wx.TE_READONLY)
        if Config.AppVersion == info['tag_name']:
            addtion_info = "您的版本已经是最新版本 :) \n\n"
        else:
            addtion_info = "有更新版本可用，请前往下载 :) \n\n"
        info_text.SetValue(addtion_info+info['body'])
        self.sizer.Add(info_label, 0, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL, 5)
        self.sizer.Add(info_text, 1, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL, 5)
        
        button_sizer = wx.BoxSizer(wx.VERTICAL)
        for i, asset in enumerate(info['assets']):
            download_button = wx.Button(self.panel, id=wx.NewId(), label=asset['name'])
            # 使用lambda捕获当前值
            download_button.Bind(wx.EVT_BUTTON, lambda e, url=asset['browser_download_url'], is_latest=(Config.AppVersion == info['tag_name']): self.Btn_click(url, is_latest))
            button_sizer.Add(download_button, 0, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL, 5)
        
        self.sizer.Add(button_sizer, 0, wx.ALIGN_LEFT|wx.EXPAND|wx.ALL, 5)

        self.panel.SetSizer(self.sizer)
        self.sizer.Layout()
    
    def init_error_UI(self):
        if self.FindWindowById(self.ID_ACTIVITY_INDICATOR):
            self.FindWindowById(self.ID_ACTIVITY_INDICATOR).Stop()
        wx.MessageBox("无法连接至更新服务器，情稍后再试", "检查更新失败", wx.OK | wx.ICON_ERROR)
        self.Close()

    def Btn_click(self, url, is_latest):
        if is_latest:
            ask = wx.MessageBox("您的版本已经是最新版本，是否仍前往下载", "无需更新", wx.OK | wx.ICON_INFORMATION | wx.CANCEL | wx.CANCEL_DEFAULT)
            if ask == wx.CANCEL:
                return
        webbrowser.open(url)
        self.Hide()

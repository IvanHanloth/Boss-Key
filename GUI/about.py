import wx
import wx.adv

from core.config import Config

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

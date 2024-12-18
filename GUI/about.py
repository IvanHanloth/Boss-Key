import wx
from core.config import Config

class AboutWindow(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, title="关于 - Boss Key", style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.SetIcon(wx.Icon(wx.Image(Config.icon).ConvertToBitmap()))
        
        self.init_UI()
        self.SetSize((500, 500))

        self.Center()

    def init_UI(self):
        # 创建面板
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        #设置图标
        IconHbox = wx.BoxSizer(wx.HORIZONTAL)
        icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap(Config.icon_info))
        IconHbox.Add(icon, proportion=1, flag=wx.LEFT, border=10)
        vbox.Add(IconHbox, proportion=1, flag=wx.EXPAND, border=10)

        #设置标题
        TitleHbox = wx.BoxSizer(wx.HORIZONTAL)
        title = wx.StaticText(panel, label="Boss Key", style=wx.ALIGN_CENTER)
        title.SetFont(wx.Font(18, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        TitleHbox.Add(title, proportion=1, flag=wx.CENTER)
        vbox.Add(TitleHbox, proportion=1, flag=wx.EXPAND)

        #设置版本
        VersionHbox = wx.BoxSizer(wx.HORIZONTAL)
        version = wx.StaticText(panel, label=f"版本: {Config.AppVersion}  发布于：{Config.AppReleaseDate}", style=wx.ALIGN_CENTER)
        VersionHbox.Add(version, proportion=1, flag=wx.CENTER)
        vbox.Add(VersionHbox, proportion=1, flag=wx.EXPAND)

        #设置作者
        AuthorHbox = wx.BoxSizer(wx.HORIZONTAL)
        author = wx.StaticText(panel, label=f"作者: {Config.AppAuthor}", style=wx.ALIGN_CENTER)
        AuthorHbox.Add(author, proportion=1, flag=wx.CENTER)
        vbox.Add(AuthorHbox, proportion=1, flag=wx.EXPAND)
        
        #设置版权
        copyrightHbox = wx.BoxSizer(wx.HORIZONTAL)
        copyright= wx.StaticText(panel, label=Config.AppCopyRight, style=wx.ALIGN_CENTER)
        copyrightHbox.Add(copyright, proportion=1, flag=wx.CENTER)
        vbox.Add(copyrightHbox, proportion=1, flag=wx.EXPAND)

        panel.SetSizer(vbox)
        self.Layout()

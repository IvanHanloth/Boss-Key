import wx
from core.config import Config
import GUI.record as record

class SettingWindow(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, title="设置 - Boss Key", style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
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
        # hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        # CS_label = wx.StaticText(panel, label="修改自启动热键:")
        # self.CS_text = wx.TextCtrl(panel, -1, value=Config.startup_hotkey)
        # self.CS_record_btn = wx.Button(panel, -1, label="录制热键")
        # hbox2.Add(CS_label, proportion=1, flag=wx.LEFT, border=10)
        # hbox2.Add(self.CS_text, proportion=1, flag=wx.EXPAND|wx.LEFT, border=10)
        # hbox2.Add(self.CS_record_btn, proportion=1, flag=wx.EXPAND|wx.RIGHT, border=10)
        # vbox.Add(hbox2, proportion=1, flag=wx.EXPAND|wx.BOTTOM, border=10)
        
        #设置关闭热键（CL）
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        CL_label = wx.StaticText(panel, label="一键关闭程序热键:")
        self.CL_text = wx.TextCtrl(panel, -1, value=Config.close_hotkey)
        self.CL_record_btn = wx.Button(panel, -1, label="录制热键")
        hbox3.Add(CL_label, proportion=1, flag=wx.LEFT, border=10)
        hbox3.Add(self.CL_text, proportion=1, flag=wx.EXPAND|wx.LEFT, border=10)
        hbox3.Add(self.CL_record_btn, proportion=1, flag=wx.EXPAND|wx.RIGHT, border=10)
        vbox.Add(hbox3, proportion=1, flag=wx.EXPAND|wx.BOTTOM, border=10)
        
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
        SendBeforeHideLabel = wx.StaticText(panel, label="隐藏前发送暂停键（Beta）")
        SBHTip=wx.ToolTip("隐藏窗口前发送暂停键，用于关闭弹出的输入框等，隐藏窗口会存在一定的延迟")
        SendBeforeHideLabel.SetToolTip(SBHTip)
        self.SendBeforeHideCheckbox = wx.CheckBox(panel, -1, "")
        hbox7.Add(Mute_after_hide_label, proportion=1, flag=wx.LEFT, border=10)
        hbox7.Add(self.Mute_after_hide_checkbox, proportion=1, flag=wx.LEFT, border=10)
        hbox7.Add(SendBeforeHideLabel, proportion=1, flag=wx.LEFT, border=10)
        hbox7.Add(self.SendBeforeHideCheckbox, proportion=1, flag=wx.LEFT, border=10)
        vbox.Add(hbox7, proportion=1, flag=wx.BOTTOM, border=10)

        # 创建按钮
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        self.Reset_btn = wx.Button(panel,size=(100,60), label="重置热键")
        self.Save_btn = wx.Button(panel,size=(100,60), label="保存设置")
        hbox5.Add(self.Reset_btn, proportion=1, flag=wx.LEFT, border=20)
        hbox5.Add(self.Save_btn, proportion=1, flag=wx.RIGHT, border=20)
        vbox.Add(hbox5, proportion=1, flag=wx.EXPAND|wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

    def Bind_EVT(self):
        self.Save_btn.Bind(wx.EVT_BUTTON, self.OnSave)
        self.Reset_btn.Bind(wx.EVT_BUTTON,self.OnReset)
        self.SW_record_btn.Bind(wx.EVT_BUTTON, self.OnRecordSW)
        # self.CS_record_btn.Bind(wx.EVT_BUTTON, self.OnRecordCS)
        self.CL_record_btn.Bind(wx.EVT_BUTTON, self.OnRecordCL)
        self.SendBeforeHideCheckbox.Bind(wx.EVT_CHECKBOX, self.OnSendBeforeHide)
        # self.Bind(wx.EVT_CLOSE,self.OnClose)

    def SetData(self):
        Config.load()
        self.SW_text.SetValue(Config.hide_hotkey)
        # self.CS_text.SetValue(Config.startup_hotkey)
        self.CL_text.SetValue(Config.close_hotkey)
        self.Mute_after_hide_checkbox.SetValue(bool(Config.mute_after_hide))
        self.SendBeforeHideCheckbox.SetValue(bool(Config.send_before_hide))

    def OnSave(self,e):
        Config.hide_hotkey = self.SW_text.GetValue()
        # Config.startup_hotkey = self.CS_text.GetValue()
        Config.close_hotkey = self.CL_text.GetValue()
        Config.mute_after_hide = self.Mute_after_hide_checkbox.GetValue()
        Config.send_before_hide = self.SendBeforeHideCheckbox.GetValue()
        Config.save()
        try:
            Config.HotkeyWindow.reBind()
            wx.MessageDialog(None, u"保存成功", u"Boss_Key", wx.OK | wx.ICON_INFORMATION).ShowModal()
        except:
            wx.MessageDialog(None, u"热键绑定失败，请重试", u"Boss Key", wx.OK | wx.ICON_ERROR).ShowModal()
        

    def OnReset(self,e):
        self.SW_text.SetValue("Ctrl+Q")
        # self.CS_text.SetValue("Alt+Q")
        self.CL_text.SetValue("Win+Esc")
        wx.MessageDialog(None, u"已重置选项，请保存设置以启用", u"Boss Key", wx.OK | wx.ICON_INFORMATION).ShowModal()

    def OnSendBeforeHide(self,e):
        if self.SendBeforeHideCheckbox.GetValue():
            wx.MessageDialog(None, u"隐藏窗口前向被隐藏的窗口发送空格，用于暂停视频等。启用此功能可能会延迟窗口的隐藏", u"Boss Key", wx.OK | wx.ICON_INFORMATION).ShowModal()

    def OnRecordSW(self, e):
        self.recordHotkey(self.SW_text, self.SW_record_btn)

    # def OnRecordCS(self, e):
    #     self.recordHotkey(self.CS_text, self.CS_record_btn)

    def OnRecordCL(self, e):
        self.recordHotkey(self.CL_text, self.CL_record_btn)

    def recordHotkey(self, text_ctrl, btn):
        try:
            Config.HotkeyWindow.stop()
        except:
            pass
        btn.Disable()
        btn.SetLabel("录制中...")
        record.RecordedHotkey.confirm=False
        RecordWindow = record.RecordWindow()
        RecordWindow.ShowModal()
        btn.Enable()
        btn.SetLabel("录制热键")
        if record.RecordedHotkey.confirm:
            text_ctrl.SetValue(record.RecordedHotkey.final_key)



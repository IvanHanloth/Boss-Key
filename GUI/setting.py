import wx
from core.config import Config
import GUI.record as record
import wx.lib.buttons as buttons

class SettingWindow(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, title="设置 - Boss Key", style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.SetIcon(wx.Icon(wx.Image(Config.icon).ConvertToBitmap()))
        
        self.init_UI()

        self.Bind_EVT()
        self.SetData()
        self.SetSize((1200, 600))

        self.Center()

    def init_UI(self):
        panel = wx.Panel(self)

        # 主 sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # 上方sizer
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # 左边列表
        left_staticbox = wx.StaticBox(panel, label="现有窗口进程")
        left_sizer = wx.StaticBoxSizer(left_staticbox, wx.VERTICAL)
        left_listctrl = wx.ListCtrl(panel, style=wx.LC_REPORT)
        left_listctrl.InsertColumn(0, '选择', width=50)
        left_listctrl.InsertColumn(1, '窗口标题', width=100)
        left_listctrl.InsertColumn(2, '窗口句柄', width=100)
        left_listctrl.InsertColumn(3, '启动进程', width=100)
        left_sizer.Add(left_listctrl, 1, wx.EXPAND | wx.ALL, 5)

        # 中键按钮
        middle_sizer = wx.BoxSizer(wx.VERTICAL)
        button1 = buttons.GenButton(panel, label="添加窗口")
        button2 = buttons.GenButton(panel, label="删除窗口")
        middle_sizer.Add(button1, 0, wx.EXPAND | wx.ALL, 5)
        middle_sizer.Add(button2, 0, wx.EXPAND | wx.ALL, 5)

        # 右边列表
        right_staticbox = wx.StaticBox(panel, label="已绑定进程")
        right_sizer = wx.StaticBoxSizer(right_staticbox, wx.VERTICAL)
        right_listctrl = wx.ListCtrl(panel, style=wx.LC_REPORT)
        right_listctrl.InsertColumn(0, '选择', width=50)
        right_listctrl.InsertColumn(1, '窗口标题', width=100)
        right_listctrl.InsertColumn(2, '窗口句柄', width=100)
        right_listctrl.InsertColumn(3, '启动进程', width=100)
        right_sizer.Add(right_listctrl, 1, wx.EXPAND | wx.ALL, 5)

        # 加到上方的sizer中
        top_sizer.Add(left_sizer, 1, wx.EXPAND | wx.ALL, 5)
        top_sizer.Add(middle_sizer, 0, wx.EXPAND | wx.ALL, 5)
        top_sizer.Add(right_sizer, 1, wx.EXPAND | wx.ALL, 5)

        # 下方设置
        bottom_staticbox = wx.StaticBox(panel, label="设置")
        bottom_sizer = wx.StaticBoxSizer(bottom_staticbox, wx.VERTICAL)

        hotkey_sizer=wx.BoxSizer(wx.HORIZONTAL)

        #设置隐显窗口热键
        hide_show_hotkey_sizer = wx.BoxSizer(wx.HORIZONTAL)
        hide_show_hotkey_label = wx.StaticText(panel, label="隐藏/显示窗口热键:")
        self.hide_show_hotkey_text = wx.TextCtrl(panel, -1, value=Config.hide_hotkey)
        self.hide_show_hotkey_btn = wx.Button(panel, -1, label="录制热键")
        hide_show_hotkey_sizer.Add(hide_show_hotkey_label, proportion=1, flag=wx.EXPAND| wx.ALL, border=10)
        hide_show_hotkey_sizer.Add(self.hide_show_hotkey_text, proportion=2, flag=wx.EXPAND| wx.ALL, border=10)
        hide_show_hotkey_sizer.Add(self.hide_show_hotkey_btn, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)
        hotkey_sizer.Add(hide_show_hotkey_sizer, proportion=4, flag=wx.EXPAND|wx.ALL, border=10)
        
        #设置关闭热键
        close_hotkey_sizer = wx.BoxSizer(wx.HORIZONTAL)
        close_hotkey_label = wx.StaticText(panel, label="一键关闭程序热键:")
        self.close_hotkey_text = wx.TextCtrl(panel, -1, value=Config.close_hotkey)
        self.close_hotkey_btn = wx.Button(panel, -1, label="录制热键")
        close_hotkey_sizer.Add(close_hotkey_label, proportion=1, flag=wx.EXPAND| wx.ALL, border=10)
        close_hotkey_sizer.Add(self.close_hotkey_text, proportion=2, flag=wx.EXPAND| wx.ALL, border=10)
        close_hotkey_sizer.Add(self.close_hotkey_btn, proportion=1, flag=wx.EXPAND| wx.ALL, border=10)
        hotkey_sizer.Add(close_hotkey_sizer, proportion=4, flag=wx.EXPAND| wx.ALL, border=10)
        
        bottom_sizer.Add(hotkey_sizer,proportion=1, flag=wx.EXPAND| wx.ALL)

        # 创建复选框
        settings_checkbox_sizer = wx.BoxSizer(wx.HORIZONTAL)

        mute_after_hide_sizer=wx.BoxSizer(wx.HORIZONTAL)
        mute_after_hide_label = wx.StaticText(panel, label="隐藏窗口后静音")
        self.mute_after_hide_checkbox = wx.CheckBox(panel, -1, "")
        mute_after_hide_sizer.Add(mute_after_hide_label,proportion=1, flag=wx.EXPAND| wx.ALL)
        mute_after_hide_sizer.Add(self.mute_after_hide_checkbox,proportion=1, flag=wx.EXPAND| wx.ALL)

        send_before_hide_sizer=wx.BoxSizer(wx.HORIZONTAL)
        send_before_hide_label = wx.StaticText(panel, label="隐藏前发送暂停键（Beta）")
        send_before_hide_label.SetToolTip(wx.ToolTip("隐藏窗口前发送暂停键，用于关闭弹出的输入框等，隐藏窗口会存在一定的延迟"))
        self.send_before_hide_checkbox = wx.CheckBox(panel, -1, "")
        send_before_hide_sizer.Add(send_before_hide_label,proportion=1, flag=wx.EXPAND| wx.ALL)
        send_before_hide_sizer.Add(self.send_before_hide_checkbox,proportion=1, flag=wx.EXPAND| wx.ALL)
        
        settings_checkbox_sizer.Add(mute_after_hide_sizer,proportion=1,flag=wx.EXPAND| wx.ALL, border=10)
        settings_checkbox_sizer.Add(send_before_hide_sizer, proportion=1,flag=wx.EXPAND| wx.ALL, border=10)

        bottom_sizer.Add(settings_checkbox_sizer, proportion=1,flag=wx.EXPAND| wx.ALL, border=10)
        
        #设置提示
        if Config.first_start:
            StaticText2=wx.StaticText(panel,label="本页面仅在首次启动或内容有更新时自动显示，后续可通过托盘图标打开本页面")
            bottom_sizer.Add(StaticText2, proportion=1, flag=wx.EXPAND|wx.BOTTOM, border=10)

        # 创建按钮
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.reset_btn = wx.Button(panel,size=(100,60), label="重置热键")
        self.save_btn = wx.Button(panel,size=(100,60), label="保存设置")
        button_sizer.Add(self.reset_btn, proportion=1, flag=wx.LEFT, border=20)
        button_sizer.Add(self.save_btn, proportion=1, flag=wx.RIGHT, border=20)
        bottom_sizer.Add(button_sizer, proportion=1, flag=wx.EXPAND|wx.BOTTOM, border=10)

        # Add top and bottom sizers to the main sizer
        main_sizer.Add(top_sizer, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(bottom_sizer, 0, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(main_sizer)
        main_sizer.Fit(self)

    def Bind_EVT(self):
        self.save_btn.Bind(wx.EVT_BUTTON, self.OnSave)
        self.reset_btn.Bind(wx.EVT_BUTTON,self.OnReset)
        self.hide_show_hotkey_btn.Bind(wx.EVT_BUTTON, self.OnRecordSW)
        # self.CS_record_btn.Bind(wx.EVT_BUTTON, self.OnRecordCS)
        self.close_hotkey_btn.Bind(wx.EVT_BUTTON, self.OnRecordCL)
        self.send_before_hide_checkbox.Bind(wx.EVT_CHECKBOX, self.OnSendBeforeHide)
        # self.Bind(wx.EVT_CLOSE,self.OnClose)

    def SetData(self):
        Config.load()
        self.hide_show_hotkey_text.SetValue(Config.hide_hotkey)
        # self.CS_text.SetValue(Config.startup_hotkey)
        self.close_hotkey_text.SetValue(Config.close_hotkey)
        self.mute_after_hide_checkbox.SetValue(bool(Config.mute_after_hide))
        self.send_before_hide_checkbox.SetValue(bool(Config.send_before_hide))

    def OnSave(self,e):
        Config.hide_hotkey = self.hide_show_hotkey_text.GetValue()
        # Config.startup_hotkey = self.CS_text.GetValue()
        Config.close_hotkey = self.close_hotkey_text.GetValue()
        Config.mute_after_hide = self.mute_after_hide_checkbox.GetValue()
        Config.send_before_hide = self.send_before_hide_checkbox.GetValue()
        Config.save()
        try:
            Config.HotkeyWindow.reBind()
            wx.MessageDialog(None, u"保存成功", u"Boss_Key", wx.OK | wx.ICON_INFORMATION).ShowModal()
        except:
            wx.MessageDialog(None, u"热键绑定失败，请重试", u"Boss Key", wx.OK | wx.ICON_ERROR).ShowModal()
        

    def OnReset(self,e):
        self.hide_show_hotkey_text.SetValue("Ctrl+Q")
        # self.CS_text.SetValue("Alt+Q")
        self.close_hotkey_text.SetValue("Win+Esc")
        wx.MessageDialog(None, u"已重置选项，请保存设置以启用", u"Boss Key", wx.OK | wx.ICON_INFORMATION).ShowModal()

    def OnSendBeforeHide(self,e):
        if self.send_before_hide_checkbox.GetValue():
            wx.MessageDialog(None, u"隐藏窗口前向被隐藏的窗口发送空格，用于暂停视频等。启用此功能可能会延迟窗口的隐藏", u"Boss Key", wx.OK | wx.ICON_INFORMATION).ShowModal()

    def OnRecordSW(self, e):
        self.recordHotkey(self.hide_show_hotkey_text, self.hide_show_hotkey_btn)

    # def OnRecordCS(self, e):
    #     self.recordHotkey(self.CS_text, self.CS_record_btn)

    def OnRecordCL(self, e):
        self.recordHotkey(self.close_hotkey_text, self.close_hotkey_btn)

    def recordHotkey(self, text_ctrl:wx.TextCtrl, btn:wx.Button):
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



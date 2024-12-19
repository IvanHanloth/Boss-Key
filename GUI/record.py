import wx
from core.config import Config
from core.tools import keyMux
import keyboard

class RecordedHotkey:
    keys_recorded = set()
    keys_pressing = set()
    recording = False
    finishOneTime = False
    final_key = None
    confirm = False

class RecordWindow(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, title="录制热键 - Boss Key", style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.SetIcon(wx.Icon(wx.Image(Config.icon).ConvertToBitmap()))
        
        self.init_UI()

        self.SetSize((500, 400))

        self.Center()
        try:
            Config.HotkeyWindow.stop()
        except:
            pass
        RecordedHotkey.recording = True
        RecordedHotkey.keys_recorded = set()
        RecordedHotkey.keys_pressing = set()
        keyboard.hook(self.onKeyEvent,suppress=True)

    def init_UI(self):
        # 创建面板
        panel = wx.Panel(self)

        # 创建布局管理器
        vbox = wx.BoxSizer(wx.VERTICAL)

        # 创建一个静态文本，居中对齐
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.StaticText(panel, label="正在录制热键",style=wx.ALIGN_CENTER)
        self.text.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.text.SetSize(self.text.GetBestSize())
        hbox1.Add(self.text, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=20)
        vbox.Add(hbox1, proportion=1, flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=20)

        # 创建一个静态文本，居中对齐，字号变大，加粗
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.text2 = wx.StaticText(panel,style=wx.ALIGN_CENTER, label="请按下热键")
        self.text2.SetFont(wx.Font(22, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.text2.SetSize(self.text2.GetBestSize())
        hbox2.Add(self.text2, proportion=1, flag=wx.LEFT|wx.RIGHT, border=20)
        vbox.Add(hbox2, proportion=1, flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=20)

        # 创建一个按钮，居中对齐
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.record_btn = wx.Button(panel, -1, label="确定")
        hbox3.Add(self.record_btn, proportion=1, flag=wx.LEFT|wx.RIGHT, border=20)
        vbox.Add(hbox3, proportion=1, flag=wx.EXPAND|wx.TOP|wx.BOTTOM, border=20)
        self.record_btn.Bind(wx.EVT_BUTTON, self.Confirm)
        self.Bind(wx.EVT_CLOSE, self.onClose)

        panel.SetSizer(vbox)
        
    def onKeyEvent(self, event):
        key=keyMux(event)
        if event.event_type == 'down':
            if len(RecordedHotkey.keys_pressing)==0:
                RecordedHotkey.keys_recorded.clear()
            RecordedHotkey.keys_pressing.add(key)
            RecordedHotkey.keys_recorded.add(key)
        elif event.event_type == 'up':
            RecordedHotkey.keys_pressing.discard(key)
            if len(RecordedHotkey.keys_pressing)<=2:
                self.stopRecording()
            else:
                RecordedHotkey.finishOneTime = False
        self.text2.SetLabel("+".join(RecordedHotkey.keys_recorded))
        self.text2.SetExtraStyle(wx.ALIGN_CENTER)

    def stopRecording(self):
        RecordedHotkey.finishOneTime = True
        RecordedHotkey.final_key = "+".join(RecordedHotkey.keys_recorded)
        
    def Confirm(self, event):
        self.stopRecording()
        RecordedHotkey.recording = False
        keyboard.unhook_all()
        self.Destroy()
        RecordedHotkey.confirm = True

    def onClose(self,event):
        self.stopRecording()
        RecordedHotkey.recording = False
        keyboard.unhook_all()
        self.Destroy()
        RecordedHotkey.confirm= False
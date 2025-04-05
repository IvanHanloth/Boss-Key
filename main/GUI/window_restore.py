import wx
import wx.dataview as dataview
import win32gui
import win32con
from .setting import SettingWindow
from core import tools as tool

class WindowRestoreDialog(SettingWindow):
    def __init__(self, id):
        super().__init__(id=id)
        self.SetSize((700, 600))

        self.SetTitle("窗口恢复")

        self.Center()
        
    def init_UI(self):
        self.window_info = []
        
        # 创建界面
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # 树形列表
        self.left_treelist = dataview.TreeListCtrl(panel, style=dataview.TL_CHECKBOX)
        self.left_treelist.AppendColumn('窗口标题', width=300)
        self.left_treelist.AppendColumn('窗口句柄', width=100)
        self.left_treelist.AppendColumn('进程PID', width=150)
        
        # 按钮区域
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.show_btn = wx.Button(panel, label="显示窗口")
        self.hide_btn = wx.Button(panel, label="隐藏窗口")
        btn_sizer.Add(self.show_btn, proportion=1, flag=wx.RIGHT, border=5)
        btn_sizer.Add(self.hide_btn, proportion=1, flag=wx.LEFT, border=5)
        
        # 布局
        vbox.Add(self.left_treelist, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=5)
        vbox.Add(btn_sizer, flag=wx.EXPAND|wx.ALL, border=10)
        
        panel.SetSizer(vbox)        

    def SetData(self):
        self.RefreshLeftList()

    def RefreshLeftList(self, e=None):
        windows = tool.getAllWindows()
        list = []
        for window in windows:
            list.append(window)
        self.InsertTreeList(list, self.left_treelist, True)
    
    def Bind_EVT(self):
        self.show_btn.Bind(wx.EVT_BUTTON, self.on_show_window)
        self.hide_btn.Bind(wx.EVT_BUTTON, self.on_hide_window)
        self.left_treelist.Bind(dataview.EVT_TREELIST_ITEM_CHECKED, self.OnToggleCheck)

    def on_show_window(self,e=None):
        windows = self.ItemsData(self.left_treelist, only_checked=True)
        result = wx.MessageBox(f"将恢复{len(windows)}个窗口\r\n恢复未知的窗口可能会导致窗口出错", "警告", wx.OK | wx.CANCEL | wx.ICON_WARNING)
        if result != wx.OK:
            return
        for window in windows:
            win32gui.ShowWindow(window.hwnd, win32con.SW_SHOW)

    def on_hide_window(self,e=None):
        windows = self.ItemsData(self.left_treelist, only_checked=True)
        result = wx.MessageBox(f"将隐藏{len(windows)}个窗口\r\n隐藏未知的窗口可能会导致窗口出错", "警告", wx.OK | wx.CANCEL | wx.ICON_WARNING)        
        if result != wx.OK:
            return
        for window in windows:
            win32gui.ShowWindow(window.hwnd, win32con.SW_HIDE)
        
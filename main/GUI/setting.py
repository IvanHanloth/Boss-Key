import wx
import wx.dataview as dataview
import wx.dataview
from core.config import Config
import GUI.record as record
import core.tools as tool
import json
import wx.lib.buttons as buttons

class SettingWindow(wx.Frame):
    def __init__(self):
        super().__init__(None, title="设置 - Boss Key", style=wx.DEFAULT_FRAME_STYLE | wx.RESIZE_BORDER)
        self.SetIcon(wx.Icon(wx.Image(Config.icon).ConvertToBitmap()))
        
        self.init_UI()

        self.Bind_EVT()
        self.SetData()
        self.SetSize((1500, 800))

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
        self.left_treelist = dataview.TreeListCtrl(panel, style=wx.dataview.TL_CHECKBOX)
        self.left_treelist.AppendColumn('窗口标题', width=300)
        self.left_treelist.AppendColumn('窗口句柄', width=100)
        self.left_treelist.AppendColumn('进程PID', width=150)
        left_sizer.Add(self.left_treelist, 1, wx.EXPAND | wx.ALL, 5)
        

        # 中键按钮
        middle_sizer = wx.BoxSizer(wx.VERTICAL)
        self.add_binding_btn = buttons.GenButton(panel, label="添加绑定-->")
        self.remove_binding_btn = buttons.GenButton(panel, label="<--删除绑定")
        self.refresh_btn = buttons.GenButton(panel, label="刷新进程")
        middle_sizer.Add(self.add_binding_btn, 0, wx.EXPAND | wx.ALL, 5)
        middle_sizer.Add(self.remove_binding_btn, 0, wx.EXPAND | wx.ALL, 5)
        middle_sizer.Add(self.refresh_btn, 0, wx.EXPAND | wx.ALL, 5)

        # 右边列表
        right_staticbox = wx.StaticBox(panel, label="已绑定进程")
        right_sizer = wx.StaticBoxSizer(right_staticbox, wx.VERTICAL)
        self.right_treelist = dataview.TreeListCtrl(panel, style=wx.dataview.TL_CHECKBOX)
        self.right_treelist.AppendColumn('窗口标题', width=300)
        self.right_treelist.AppendColumn('窗口句柄', width=100)
        self.right_treelist.AppendColumn('进程PID', width=150)
        right_sizer.Add(self.right_treelist, 1, wx.EXPAND | wx.ALL, 5)

        # 加到上方的sizer中
        top_sizer.Add(left_sizer, 1, wx.EXPAND | wx.ALL, 5)
        top_sizer.Add(middle_sizer, 0, wx.EXPAND | wx.ALL, 5)
        top_sizer.Add(right_sizer, 1, wx.EXPAND | wx.ALL, 5)

        # 下方设置
        bottom_staticbox = wx.StaticBox(panel, label="其他设置")
        bottom_sizer = wx.StaticBoxSizer(bottom_staticbox, wx.VERTICAL)

        hotkey_sizer=wx.GridSizer(rows=0, cols=2, gap=(10, 10))

        #设置隐显窗口热键
        hide_show_hotkey_sizer = wx.BoxSizer(wx.HORIZONTAL)
        hide_show_hotkey_label = wx.StaticText(panel, label="隐藏/显示窗口热键:")
        self.hide_show_hotkey_text = wx.TextCtrl(panel, -1, value=Config.hide_hotkey)
        self.hide_show_hotkey_btn = wx.Button(panel, -1, label="录制热键")
        hide_show_hotkey_sizer.Add(hide_show_hotkey_label, proportion=1, flag=wx.EXPAND| wx.ALL, border=10)
        hide_show_hotkey_sizer.Add(self.hide_show_hotkey_text, proportion=1, flag=wx.EXPAND| wx.ALL, border=10)
        hide_show_hotkey_sizer.Add(self.hide_show_hotkey_btn, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)
        hotkey_sizer.Add(hide_show_hotkey_sizer, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)
        
        #设置关闭热键
        close_hotkey_sizer = wx.BoxSizer(wx.HORIZONTAL)
        close_hotkey_label = wx.StaticText(panel, label="一键关闭程序热键:")
        self.close_hotkey_text = wx.TextCtrl(panel, -1, value=Config.close_hotkey)
        self.close_hotkey_btn = wx.Button(panel, -1, label="录制热键")
        close_hotkey_sizer.Add(close_hotkey_label, proportion=1, flag=wx.EXPAND| wx.ALL, border=10)
        close_hotkey_sizer.Add(self.close_hotkey_text, proportion=1, flag=wx.EXPAND| wx.ALL, border=10)
        close_hotkey_sizer.Add(self.close_hotkey_btn, proportion=1, flag=wx.EXPAND| wx.ALL, border=10)
        hotkey_sizer.Add(close_hotkey_sizer, proportion=1, flag=wx.EXPAND| wx.ALL, border=10)
        
        bottom_sizer.Add(hotkey_sizer, flag=wx.EXPAND| wx.ALL)

        # 创建复选框
        settings_checkbox_sizer = wx.GridSizer(rows=0, cols=3, gap=(10, 10))

        mute_after_hide_sizer=wx.BoxSizer(wx.HORIZONTAL)
        mute_after_hide_label = wx.StaticText(panel, label="隐藏窗口后静音")
        self.mute_after_hide_checkbox = wx.CheckBox(panel, -1, "")
        mute_after_hide_sizer.Add(mute_after_hide_label,proportion=1, flag=wx.EXPAND| wx.ALL)
        mute_after_hide_sizer.Add(self.mute_after_hide_checkbox,proportion=1, flag=wx.EXPAND| wx.ALL)
        settings_checkbox_sizer.Add(mute_after_hide_sizer,proportion=1,flag=wx.EXPAND| wx.ALL, border=10)

        send_before_hide_sizer=wx.BoxSizer(wx.HORIZONTAL)
        send_before_hide_label = wx.StaticText(panel, label="隐藏前发送暂停键（Beta）")
        send_before_hide_label.SetToolTip(wx.ToolTip("隐藏窗口前发送暂停键，用于关闭弹出的输入框等，隐藏窗口会存在一定的延迟"))
        self.send_before_hide_checkbox = wx.CheckBox(panel, -1, "")
        send_before_hide_sizer.Add(send_before_hide_label,proportion=1, flag=wx.EXPAND| wx.ALL)
        send_before_hide_sizer.Add(self.send_before_hide_checkbox,proportion=1, flag=wx.EXPAND| wx.ALL)
        settings_checkbox_sizer.Add(send_before_hide_sizer, proportion=1,flag=wx.EXPAND| wx.ALL, border=10)

        hide_current_sizer=wx.BoxSizer(wx.HORIZONTAL)
        hide_current_label = wx.StaticText(panel, label="同时隐藏当前活动窗口")
        self.hide_current_checkbox = wx.CheckBox(panel, -1, "")
        hide_current_sizer.Add(hide_current_label,proportion=1, flag=wx.EXPAND| wx.ALL)
        hide_current_sizer.Add(self.hide_current_checkbox,proportion=1, flag=wx.EXPAND| wx.ALL)
        settings_checkbox_sizer.Add(hide_current_sizer, proportion=1,flag=wx.EXPAND| wx.ALL, border=10)
        
        click_to_hide_sizer=wx.BoxSizer(wx.HORIZONTAL)
        click_to_hide_label = wx.StaticText(panel, label="点击托盘图标切换隐藏状态")
        self.click_to_hide_checkbox = wx.CheckBox(panel, -1, "")
        click_to_hide_sizer.Add(click_to_hide_label,proportion=1, flag=wx.EXPAND| wx.ALL)
        click_to_hide_sizer.Add(self.click_to_hide_checkbox,proportion=1, flag=wx.EXPAND| wx.ALL)
        settings_checkbox_sizer.Add(click_to_hide_sizer, proportion=1,flag=wx.EXPAND| wx.ALL, border=10)

        hide_icon_after_hide_sizer=wx.BoxSizer(wx.HORIZONTAL)
        hide_icon_after_hide_label = wx.StaticText(panel, label="隐藏窗口后隐藏托盘图标")
        self.hide_icon_after_hide_checkbox = wx.CheckBox(panel, -1, "")
        hide_icon_after_hide_sizer.Add(hide_icon_after_hide_label,proportion=1, flag=wx.EXPAND| wx.ALL)
        hide_icon_after_hide_sizer.Add(self.hide_icon_after_hide_checkbox,proportion=1, flag=wx.EXPAND| wx.ALL)
        settings_checkbox_sizer.Add(hide_icon_after_hide_sizer, proportion=1,flag=wx.EXPAND| wx.ALL, border=10)
        
        bottom_sizer.Add(settings_checkbox_sizer, flag=wx.EXPAND| wx.ALL, border=10)
        
        #设置提示
        if Config.first_start:
            StaticText2=wx.StaticText(panel,label="本页面仅在首次启动或内容有更新时自动显示，后续可通过托盘图标打开本页面")
            bottom_sizer.Add(StaticText2, proportion=1, flag=wx.EXPAND|wx.BOTTOM, border=10)

        # 创建按钮
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.reset_btn = wx.Button(panel,size=(100,60), label="重置设置")
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
        self.close_hotkey_btn.Bind(wx.EVT_BUTTON, self.OnRecordCL)
        self.send_before_hide_checkbox.Bind(wx.EVT_CHECKBOX, self.OnSendBeforeHide)
        self.refresh_btn.Bind(wx.EVT_BUTTON, self.RefreshLeftList)
        self.add_binding_btn.Bind(wx.EVT_BUTTON, self.OnAddBinding)
        self.remove_binding_btn.Bind(wx.EVT_BUTTON, self.OnRemoveBinding)
        # self.left_treelist.Bind(dataview.EVT_TREELIST_SELECTION_CHANGED, self.OnToggleCheck)
        # self.right_treelist.Bind(dataview.EVT_TREELIST_SELECTION_CHANGED, self.OnToggleCheck)
        self.left_treelist.Bind(dataview.EVT_TREELIST_ITEM_CHECKED, self.OnToggleCheck)
        self.right_treelist.Bind(dataview.EVT_TREELIST_ITEM_CHECKED, self.OnToggleCheck)
        
        self.Bind(wx.EVT_CLOSE,self.OnClose)

    def SetData(self):
        Config.load()
        self.hide_show_hotkey_text.SetValue(Config.hide_hotkey)
        self.close_hotkey_text.SetValue(Config.close_hotkey)
        self.mute_after_hide_checkbox.SetValue(Config.mute_after_hide)
        self.send_before_hide_checkbox.SetValue(Config.send_before_hide)
        self.hide_current_checkbox.SetValue(Config.hide_current)
        self.click_to_hide_checkbox.SetValue(Config.click_to_hide)
        self.hide_icon_after_hide_checkbox.SetValue(Config.hide_icon_after_hide)
        self.InsertTreeList(Config.hide_binding, self.right_treelist, True)
        self.RefreshLeftList()

    def OnSave(self,e):
        Config.hide_hotkey = self.hide_show_hotkey_text.GetValue()
        Config.close_hotkey = self.close_hotkey_text.GetValue()
        Config.mute_after_hide = self.mute_after_hide_checkbox.GetValue()
        Config.send_before_hide = self.send_before_hide_checkbox.GetValue()
        Config.hide_current = self.hide_current_checkbox.GetValue()
        Config.click_to_hide = self.click_to_hide_checkbox.GetValue()
        Config.hide_icon_after_hide = self.hide_icon_after_hide_checkbox.GetValue()
        Config.hide_binding = self.ItemsData(self.right_treelist, only_checked=False)

        Config.HotkeyListener.ShowWindows(load=False)
        Config.save()
        try:
            Config.HotkeyListener.reBind()
            wx.MessageDialog(None, u"保存成功", u"Boss Key", wx.OK | wx.ICON_INFORMATION).ShowModal()
        except:
            wx.MessageDialog(None, u"热键绑定失败，请重试", u"Boss Key", wx.OK | wx.ICON_ERROR).ShowModal()
        
    def OnAddBinding(self,e):
        left_checked = self.ItemsData(self.left_treelist, only_checked=True)
        self.InsertTreeList(left_checked, self.right_treelist, False)
        for item in left_checked:
            self.RemoveItem(self.left_treelist, item)
            

    def OnRemoveBinding(self,e):
        right_checked = self.ItemsData(self.right_treelist, only_checked=True)
        self.InsertTreeList(right_checked, self.left_treelist, False)
        for item in right_checked:
            self.RemoveItem(self.right_treelist, item)

    def OnReset(self,e):
        self.hide_show_hotkey_text.SetValue("Ctrl+Q")
        self.close_hotkey_text.SetValue("Win+Esc")
        self.mute_after_hide_checkbox.SetValue(True)
        self.send_before_hide_checkbox.SetValue(False)
        self.hide_current_checkbox.SetValue(True)
        self.InsertTreeList([],self.right_treelist,True)
        self.RefreshLeftList()
        
        wx.MessageDialog(None, u"已重置选项，请保存设置以启用", u"Boss Key", wx.OK | wx.ICON_INFORMATION).ShowModal()

    def OnToggleCheck(self, e):
        treelist = e.GetEventObject()
        item = e.GetItem()
        is_checked = treelist.GetCheckedState(item)
        treelist.CheckItemRecursively(item, is_checked)
        # 检查父级是否需要修改状态
        parent = treelist.GetItemParent(item)
        if parent == treelist.GetRootItem():
            return
        else:
            if treelist.AreAllChildrenInState(parent, wx.CHK_CHECKED):
                treelist.CheckItem(parent, wx.CHK_CHECKED)
            elif treelist.AreAllChildrenInState(parent, wx.CHK_UNCHECKED):
                treelist.CheckItem(parent, wx.CHK_UNCHECKED)

    def OnSendBeforeHide(self,e):
        if self.send_before_hide_checkbox.GetValue():
            wx.MessageDialog(None, u"隐藏窗口前向被隐藏的窗口发送空格，用于暂停视频等。启用此功能可能会延迟窗口的隐藏", u"Boss Key", wx.OK | wx.ICON_INFORMATION).ShowModal()

    def OnRecordSW(self, e):
        self.recordHotkey(self.hide_show_hotkey_text, self.hide_show_hotkey_btn)

    def OnClose(self, e):
        self.Hide()

    def OnRecordCL(self, e):
        self.recordHotkey(self.close_hotkey_text, self.close_hotkey_btn)
    
    def RefreshLeftList(self,e=None):
        windows=tool.getAllWindows()
        right=self.ItemsData(self.right_treelist,only_checked=False)
        list=[]
        for window in windows:
            flag=0
            for i in right:
                if tool.isSameWindow(window,i,True):
                    flag=1
                    break
            if not flag:
                list.append(window)
        self.InsertTreeList(list,self.left_treelist,True)

    def InsertTreeList(self, data: list, treelist: dataview.TreeListCtrl, clear=True):
        if clear:
            treelist.DeleteAllItems()
        root = treelist.GetRootItem()
        process_map = {}
        for window in data:
            process = window['process']
            if process not in process_map:
                exists_node=self.SearchProcessNode(treelist, process)
                if exists_node is None:
                    process_map[process] = treelist.AppendItem(root, process)
                else:
                    process_map[process] = exists_node
            item = treelist.AppendItem(process_map[process], window['title'])
            treelist.SetItemText(item, 1, str(window['hwnd']))
            treelist.SetItemText(item, 2, str(window['PID']))
            treelist.SetItemData(item, {"title":window['title'],"hwnd": window['hwnd'], "process": window['process'], "PID": window['PID']})
        treelist.Expand(root)
        for process in process_map:
            treelist.Expand(process_map[process])

    def SearchProcessNode(self, treelist: dataview.TreeListCtrl, process):
        item = treelist.GetRootItem()
        while item.IsOk():
            item = treelist.GetNextItem(item)
            if not item.IsOk():
                break
            data = treelist.GetItemData(item)
            if data is not None and data and data['process'] == process:
                return treelist.GetItemParent(item)
            
    def RemoveItem(self, treelist: dataview.TreeListCtrl, data):
        node=item = self.SearchProcessNode(treelist, data['process'])
        if item is not None:
            item = treelist.GetFirstChild(item)
            while item.IsOk():
                if treelist.GetItemData(item) == data:
                    treelist.DeleteItem(item)
                    break
                item = treelist.GetNextSibling(item)

            if not treelist.GetFirstChild(node).IsOk():
                # 如果没有子节点了，删除父节点
                treelist.DeleteItem(node)

    def ItemsData(self, treelist: dataview.TreeListCtrl, only_checked=False, item_object=False):
        res = []
        item = treelist.GetRootItem()
        while item.IsOk():
            item = treelist.GetNextItem(item)
            if not item.IsOk():
                break
            if only_checked and treelist.GetCheckedState(item) != wx.CHK_CHECKED:
                continue
            if item_object:
                res.append(item)
            else:
                data = treelist.GetItemData(item)
                if data is not None and data:
                    res.append(data)
        return res

    def recordHotkey(self, text_ctrl:wx.TextCtrl, btn:wx.Button):
        try:
            Config.HotkeyListener.stop()
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



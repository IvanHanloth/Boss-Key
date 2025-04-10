import wx
import wx.dataview as dataview
from core.config import Config
import GUI.record as record
import core.tools as tool
import wx.lib.buttons as buttons
from core.model import WindowInfo

class SettingWindow(wx.Frame):
    # 定义组件ID常量
    ID_LEFT_TREELIST = wx.NewIdRef()
    ID_RIGHT_TREELIST = wx.NewIdRef()
    ID_ADD_BINDING_BTN = wx.NewIdRef()
    ID_REMOVE_BINDING_BTN = wx.NewIdRef()
    ID_REFRESH_BTN = wx.NewIdRef()
    ID_HIDE_SHOW_HOTKEY_TEXT = wx.NewIdRef()
    ID_HIDE_SHOW_HOTKEY_BTN = wx.NewIdRef()
    ID_CLOSE_HOTKEY_TEXT = wx.NewIdRef() 
    ID_CLOSE_HOTKEY_BTN = wx.NewIdRef()
    ID_MUTE_AFTER_HIDE_CHECKBOX = wx.NewIdRef()
    ID_SEND_BEFORE_HIDE_CHECKBOX = wx.NewIdRef()
    ID_HIDE_CURRENT_CHECKBOX = wx.NewIdRef()
    ID_CLICK_TO_HIDE_CHECKBOX = wx.NewIdRef()
    ID_HIDE_ICON_AFTER_HIDE_CHECKBOX = wx.NewIdRef()
    ID_PATH_MATCH_CHECKBOX = wx.NewIdRef()
    ID_RESET_BTN = wx.NewIdRef()
    ID_SAVE_BTN = wx.NewIdRef()
    
    def __init__(self,id=None):
        super().__init__(None,id=id, title="设置 - Boss Key", style=wx.DEFAULT_FRAME_STYLE | wx.RESIZE_BORDER)
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
        self.left_treelist = dataview.TreeListCtrl(panel, self.ID_LEFT_TREELIST, style=dataview.TL_CHECKBOX)
        self.left_treelist.AppendColumn('窗口标题', width=300)
        self.left_treelist.AppendColumn('窗口句柄', width=100)
        self.left_treelist.AppendColumn('进程PID', width=150)
        left_sizer.Add(self.left_treelist, 1, wx.EXPAND | wx.ALL, 5)
        

        # 中键按钮
        middle_sizer = wx.BoxSizer(wx.VERTICAL)
        add_binding_btn = buttons.GenButton(panel, self.ID_ADD_BINDING_BTN, label="添加绑定-->")
        remove_binding_btn = buttons.GenButton(panel, self.ID_REMOVE_BINDING_BTN, label="<--删除绑定")
        refresh_btn = buttons.GenButton(panel, self.ID_REFRESH_BTN, label="刷新进程")
        middle_sizer.Add(add_binding_btn, 0, wx.EXPAND | wx.ALL, 5)
        middle_sizer.Add(remove_binding_btn, 0, wx.EXPAND | wx.ALL, 5)
        middle_sizer.Add(refresh_btn, 0, wx.EXPAND | wx.ALL, 5)

        # 右边列表
        right_staticbox = wx.StaticBox(panel, label="已绑定进程")
        right_sizer = wx.StaticBoxSizer(right_staticbox, wx.VERTICAL)
        self.right_treelist = dataview.TreeListCtrl(panel, self.ID_RIGHT_TREELIST, style=dataview.TL_CHECKBOX)
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
        hide_show_hotkey_text = wx.TextCtrl(panel, self.ID_HIDE_SHOW_HOTKEY_TEXT, value=Config.hide_hotkey)
        hide_show_hotkey_btn = wx.Button(panel, self.ID_HIDE_SHOW_HOTKEY_BTN, label="录制热键")
        hide_show_hotkey_sizer.Add(hide_show_hotkey_label, proportion=1, flag=wx.EXPAND| wx.ALL, border=10)
        hide_show_hotkey_sizer.Add(hide_show_hotkey_text, proportion=1, flag=wx.EXPAND| wx.ALL, border=10)
        hide_show_hotkey_sizer.Add(hide_show_hotkey_btn, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)
        hotkey_sizer.Add(hide_show_hotkey_sizer, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)
        
        #设置关闭热键
        close_hotkey_sizer = wx.BoxSizer(wx.HORIZONTAL)
        close_hotkey_label = wx.StaticText(panel, label="一键关闭程序热键:")
        close_hotkey_text = wx.TextCtrl(panel, self.ID_CLOSE_HOTKEY_TEXT, value=Config.close_hotkey)
        close_hotkey_btn = wx.Button(panel, self.ID_CLOSE_HOTKEY_BTN, label="录制热键")
        close_hotkey_sizer.Add(close_hotkey_label, proportion=1, flag=wx.EXPAND| wx.ALL, border=10)
        close_hotkey_sizer.Add(close_hotkey_text, proportion=1, flag=wx.EXPAND| wx.ALL, border=10)
        close_hotkey_sizer.Add(close_hotkey_btn, proportion=1, flag=wx.EXPAND| wx.ALL, border=10)
        hotkey_sizer.Add(close_hotkey_sizer, proportion=1, flag=wx.EXPAND| wx.ALL, border=10)
        
        bottom_sizer.Add(hotkey_sizer, flag=wx.EXPAND| wx.ALL)

        # 创建复选框
        settings_checkbox_sizer = wx.GridSizer(rows=0, cols=3, gap=(10, 10))

        mute_after_hide_sizer=wx.BoxSizer(wx.HORIZONTAL)
        mute_after_hide_label = wx.StaticText(panel, label="隐藏窗口后静音")
        mute_after_hide_checkbox = wx.CheckBox(panel, self.ID_MUTE_AFTER_HIDE_CHECKBOX, "")
        mute_after_hide_sizer.Add(mute_after_hide_label,proportion=1, flag=wx.EXPAND| wx.ALL)
        mute_after_hide_sizer.Add(mute_after_hide_checkbox,proportion=1, flag=wx.EXPAND| wx.ALL)
        settings_checkbox_sizer.Add(mute_after_hide_sizer,proportion=1,flag=wx.EXPAND| wx.ALL, border=10)

        send_before_hide_sizer=wx.BoxSizer(wx.HORIZONTAL)
        send_before_hide_label = wx.StaticText(panel, label="隐藏前发送暂停键（Beta）")
        send_before_hide_label.SetToolTip(wx.ToolTip("隐藏窗口前发送暂停键，用于关闭弹出的输入框等，隐藏窗口会存在一定的延迟"))
        send_before_hide_checkbox = wx.CheckBox(panel, self.ID_SEND_BEFORE_HIDE_CHECKBOX, "")
        send_before_hide_sizer.Add(send_before_hide_label,proportion=1, flag=wx.EXPAND| wx.ALL)
        send_before_hide_sizer.Add(send_before_hide_checkbox,proportion=1, flag=wx.EXPAND| wx.ALL)
        settings_checkbox_sizer.Add(send_before_hide_sizer, proportion=1,flag=wx.EXPAND| wx.ALL, border=10)

        hide_current_sizer=wx.BoxSizer(wx.HORIZONTAL)
        hide_current_label = wx.StaticText(panel, label="同时隐藏当前活动窗口")
        hide_current_checkbox = wx.CheckBox(panel, self.ID_HIDE_CURRENT_CHECKBOX, "")
        hide_current_sizer.Add(hide_current_label,proportion=1, flag=wx.EXPAND| wx.ALL)
        hide_current_sizer.Add(hide_current_checkbox,proportion=1, flag=wx.EXPAND| wx.ALL)
        settings_checkbox_sizer.Add(hide_current_sizer, proportion=1,flag=wx.EXPAND| wx.ALL, border=10)
        
        click_to_hide_sizer=wx.BoxSizer(wx.HORIZONTAL)
        click_to_hide_label = wx.StaticText(panel, label="点击托盘图标切换隐藏状态")
        click_to_hide_checkbox = wx.CheckBox(panel, self.ID_CLICK_TO_HIDE_CHECKBOX, "")
        click_to_hide_sizer.Add(click_to_hide_label,proportion=1, flag=wx.EXPAND| wx.ALL)
        click_to_hide_sizer.Add(click_to_hide_checkbox,proportion=1, flag=wx.EXPAND| wx.ALL)
        settings_checkbox_sizer.Add(click_to_hide_sizer, proportion=1,flag=wx.EXPAND| wx.ALL, border=10)

        hide_icon_after_hide_sizer=wx.BoxSizer(wx.HORIZONTAL)
        hide_icon_after_hide_label = wx.StaticText(panel, label="隐藏窗口后隐藏托盘图标")
        hide_icon_after_hide_checkbox = wx.CheckBox(panel, self.ID_HIDE_ICON_AFTER_HIDE_CHECKBOX, "")
        hide_icon_after_hide_sizer.Add(hide_icon_after_hide_label,proportion=1, flag=wx.EXPAND| wx.ALL)
        hide_icon_after_hide_sizer.Add(hide_icon_after_hide_checkbox,proportion=1, flag=wx.EXPAND| wx.ALL)
        settings_checkbox_sizer.Add(hide_icon_after_hide_sizer, proportion=1,flag=wx.EXPAND| wx.ALL, border=10)
        
        path_match_sizer=wx.BoxSizer(wx.HORIZONTAL)
        path_icon_sizer = wx.BoxSizer(wx.HORIZONTAL)
        path_match_tooltip = "启用此选项可以一键隐藏绑定程序的所有窗口\r\n关闭此选项后，将会智能精确隐藏指定窗口"
        path_match_label = wx.StaticText(panel, label="文件路径匹配")
        path_match_label.SetToolTip(path_match_tooltip)
        path_match_checkbox = wx.CheckBox(panel, self.ID_PATH_MATCH_CHECKBOX, "")
        path_match_tooltip_icon = wx.StaticBitmap(panel, bitmap=wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, self.FromDIP((14, 14))))
        path_match_tooltip_icon.SetToolTip(path_match_tooltip)
        path_icon_sizer.Add(path_match_label,flag=wx.EXPAND| wx.ALL)
        path_icon_sizer.AddSpacer(5)
        path_icon_sizer.Add(path_match_tooltip_icon,flag=wx.EXPAND| wx.ALL)
        path_match_sizer.Add(path_icon_sizer, proportion=1,flag=wx.EXPAND| wx.ALL)
        path_match_sizer.Add(path_match_checkbox,proportion=1, flag=wx.EXPAND| wx.ALL)
        settings_checkbox_sizer.Add(path_match_sizer, proportion=1,flag=wx.EXPAND| wx.ALL, border=10)
        
        bottom_sizer.Add(settings_checkbox_sizer, flag=wx.EXPAND| wx.ALL, border=10)
        
        #设置提示
        if Config.first_start:
            StaticText2=wx.StaticText(panel,label="本页面仅在首次启动或内容有更新时自动显示，后续可通过托盘图标打开本页面")
            bottom_sizer.Add(StaticText2, proportion=1, flag=wx.EXPAND|wx.BOTTOM, border=10)

        # 创建按钮
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        reset_btn = wx.Button(panel, self.ID_RESET_BTN, size=(100,60), label="重置设置")
        save_btn = wx.Button(panel, self.ID_SAVE_BTN, size=(100,60), label="保存设置")
        button_sizer.Add(reset_btn, proportion=1, flag=wx.LEFT, border=20)
        button_sizer.Add(save_btn, proportion=1, flag=wx.RIGHT, border=20)
        bottom_sizer.Add(button_sizer, proportion=1, flag=wx.EXPAND|wx.BOTTOM, border=10)

        # Add top and bottom sizers to the main sizer
        main_sizer.Add(top_sizer, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(bottom_sizer, 0, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(main_sizer)
        main_sizer.Fit(self)

    def Bind_EVT(self):
        self.Bind(wx.EVT_BUTTON, self.OnSave, id=self.ID_SAVE_BTN)
        self.Bind(wx.EVT_BUTTON, self.OnReset, id=self.ID_RESET_BTN)
        self.Bind(wx.EVT_BUTTON, self.OnRecordSW, id=self.ID_HIDE_SHOW_HOTKEY_BTN)
        self.Bind(wx.EVT_BUTTON, self.OnRecordCL, id=self.ID_CLOSE_HOTKEY_BTN)
        self.Bind(wx.EVT_CHECKBOX, self.OnSendBeforeHide, id=self.ID_SEND_BEFORE_HIDE_CHECKBOX)
        self.Bind(wx.EVT_BUTTON, self.RefreshLeftList, id=self.ID_REFRESH_BTN)
        self.Bind(wx.EVT_BUTTON, self.OnAddBinding, id=self.ID_ADD_BINDING_BTN)
        self.Bind(wx.EVT_BUTTON, self.OnRemoveBinding, id=self.ID_REMOVE_BINDING_BTN)
        self.left_treelist.Bind(dataview.EVT_TREELIST_ITEM_CHECKED, self.OnToggleCheck)
        self.right_treelist.Bind(dataview.EVT_TREELIST_ITEM_CHECKED, self.OnToggleCheck)
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def SetData(self):
        Config.load()
        hide_show_hotkey_text = self.FindWindowById(self.ID_HIDE_SHOW_HOTKEY_TEXT)
        close_hotkey_text = self.FindWindowById(self.ID_CLOSE_HOTKEY_TEXT)
        mute_after_hide_checkbox = self.FindWindowById(self.ID_MUTE_AFTER_HIDE_CHECKBOX)
        send_before_hide_checkbox = self.FindWindowById(self.ID_SEND_BEFORE_HIDE_CHECKBOX) 
        hide_current_checkbox = self.FindWindowById(self.ID_HIDE_CURRENT_CHECKBOX)
        click_to_hide_checkbox = self.FindWindowById(self.ID_CLICK_TO_HIDE_CHECKBOX)
        hide_icon_after_hide_checkbox = self.FindWindowById(self.ID_HIDE_ICON_AFTER_HIDE_CHECKBOX)
        path_match_checkbox = self.FindWindowById(self.ID_PATH_MATCH_CHECKBOX)
        
        hide_show_hotkey_text.SetValue(Config.hide_hotkey)
        close_hotkey_text.SetValue(Config.close_hotkey)
        mute_after_hide_checkbox.SetValue(Config.mute_after_hide)
        send_before_hide_checkbox.SetValue(Config.send_before_hide)
        hide_current_checkbox.SetValue(Config.hide_current)
        click_to_hide_checkbox.SetValue(Config.click_to_hide)
        hide_icon_after_hide_checkbox.SetValue(Config.hide_icon_after_hide)
        path_match_checkbox.SetValue(Config.path_match)
        self.InsertTreeList(Config.hide_binding, self.right_treelist, True)
        self.RefreshLeftList()

    def OnSave(self, e):
        hide_show_hotkey_text = self.FindWindowById(self.ID_HIDE_SHOW_HOTKEY_TEXT)
        close_hotkey_text = self.FindWindowById(self.ID_CLOSE_HOTKEY_TEXT)
        mute_after_hide_checkbox = self.FindWindowById(self.ID_MUTE_AFTER_HIDE_CHECKBOX)
        send_before_hide_checkbox = self.FindWindowById(self.ID_SEND_BEFORE_HIDE_CHECKBOX) 
        hide_current_checkbox = self.FindWindowById(self.ID_HIDE_CURRENT_CHECKBOX)
        click_to_hide_checkbox = self.FindWindowById(self.ID_CLICK_TO_HIDE_CHECKBOX)
        hide_icon_after_hide_checkbox = self.FindWindowById(self.ID_HIDE_ICON_AFTER_HIDE_CHECKBOX)
        path_match_checkbox = self.FindWindowById(self.ID_PATH_MATCH_CHECKBOX)
        
        Config.hide_hotkey = hide_show_hotkey_text.GetValue()
        Config.close_hotkey = close_hotkey_text.GetValue()
        Config.mute_after_hide = mute_after_hide_checkbox.GetValue()
        Config.send_before_hide = send_before_hide_checkbox.GetValue()
        Config.hide_current = hide_current_checkbox.GetValue()
        Config.click_to_hide = click_to_hide_checkbox.GetValue()
        Config.hide_icon_after_hide = hide_icon_after_hide_checkbox.GetValue()
        Config.path_match = path_match_checkbox.GetValue()
        
        # 获取Windows对象列表
        Config.hide_binding = self.ItemsData(self.right_treelist, only_checked=False)

        Config.HotkeyListener.ShowWindows(load=False)
        Config.save()
        try:
            Config.HotkeyListener.reBind()
            wx.MessageDialog(None, u"保存成功", u"Boss Key", wx.OK | wx.ICON_INFORMATION).ShowModal()
        except:
            wx.MessageDialog(None, u"热键绑定失败，请重试", u"Boss Key", wx.OK | wx.ICON_ERROR).ShowModal()
        
    def OnAddBinding(self, e):
        left_checked = self.ItemsData(self.left_treelist, only_checked=True)
        self.InsertTreeList(left_checked, self.right_treelist, False)
        for item in left_checked:
            self.RemoveItem(self.left_treelist, item)

    def OnRemoveBinding(self, e):
        right_checked = self.ItemsData(self.right_treelist, only_checked=True)
        self.InsertTreeList(right_checked, self.left_treelist, False)
        for item in right_checked:
            self.RemoveItem(self.right_treelist, item)

    def OnReset(self, e):
        hide_show_hotkey_text = self.FindWindowById(self.ID_HIDE_SHOW_HOTKEY_TEXT)
        close_hotkey_text = self.FindWindowById(self.ID_CLOSE_HOTKEY_TEXT)
        mute_after_hide_checkbox = self.FindWindowById(self.ID_MUTE_AFTER_HIDE_CHECKBOX)
        send_before_hide_checkbox = self.FindWindowById(self.ID_SEND_BEFORE_HIDE_CHECKBOX) 
        hide_current_checkbox = self.FindWindowById(self.ID_HIDE_CURRENT_CHECKBOX)
        click_to_hide_checkbox = self.FindWindowById(self.ID_CLICK_TO_HIDE_CHECKBOX)
        hide_icon_after_hide_checkbox = self.FindWindowById(self.ID_HIDE_ICON_AFTER_HIDE_CHECKBOX)
        path_match_checkbox = self.FindWindowById(self.ID_PATH_MATCH_CHECKBOX)
        
        hide_show_hotkey_text.SetValue("Ctrl+Q")
        close_hotkey_text.SetValue("Win+Esc")
        mute_after_hide_checkbox.SetValue(True)
        send_before_hide_checkbox.SetValue(False)
        hide_current_checkbox.SetValue(True)
        click_to_hide_checkbox.SetValue(False)
        hide_icon_after_hide_checkbox.SetValue(False)
        path_match_checkbox.SetValue(False)
        self.InsertTreeList([], self.right_treelist, True)
        self.RefreshLeftList()
        
        wx.MessageDialog(None, u"已重置选项，请保存设置以启用", u"Boss Key", wx.OK | wx.ICON_INFORMATION).ShowModal()

    def OnToggleCheck(self, e):
        treelist = e.GetEventObject()
        item = e.GetItem()
        is_checked = treelist.GetCheckedState(item)
        
        # 递归设置子节点状态
        self.CheckItemRecursively(treelist, item, is_checked)
        
        # 更新父节点状态
        self.UpdateParentCheckState(treelist, item)
    
    def CheckItemRecursively(self, treelist, item, check_state):
        """递归设置项目及其子项的选中状态"""
        treelist.CheckItem(item, check_state)
        
        # 处理所有子节点
        child = treelist.GetFirstChild(item)
        while child.IsOk():
            self.CheckItemRecursively(treelist, child, check_state)
            child = treelist.GetNextSibling(child)
    
    def UpdateParentCheckState(self, treelist, item):
        """更新父节点的选中状态"""
        parent = treelist.GetItemParent(item)
        if parent != treelist.GetRootItem():
            # 检查所有兄弟节点状态
            all_checked = True
            all_unchecked = True
            
            child = treelist.GetFirstChild(parent)
            while child.IsOk():
                state = treelist.GetCheckedState(child)
                if state != wx.CHK_CHECKED:
                    all_checked = False
                if state != wx.CHK_UNCHECKED:
                    all_unchecked = False
                child = treelist.GetNextSibling(child)
            
            # 根据子节点状态设置父节点状态
            if all_checked:
                treelist.CheckItem(parent, wx.CHK_CHECKED)
            elif all_unchecked:
                treelist.CheckItem(parent, wx.CHK_UNCHECKED)
            else:
                treelist.CheckItem(parent, wx.CHK_UNDETERMINED)
            
            # 递归更新上层父节点
            self.UpdateParentCheckState(treelist, parent)

    def OnSendBeforeHide(self, e):
        send_before_hide_checkbox = self.FindWindowById(self.ID_SEND_BEFORE_HIDE_CHECKBOX)
        if send_before_hide_checkbox.GetValue():
            wx.MessageDialog(None, u"隐藏窗口前向被隐藏的窗口发送空格，用于暂停视频等。启用此功能可能会延迟窗口的隐藏", u"Boss Key", wx.OK | wx.ICON_INFORMATION).ShowModal()

    def OnRecordSW(self, e):
        hide_show_hotkey_text = self.FindWindowById(self.ID_HIDE_SHOW_HOTKEY_TEXT)
        hide_show_hotkey_btn = self.FindWindowById(self.ID_HIDE_SHOW_HOTKEY_BTN)
        self.recordHotkey(hide_show_hotkey_text, hide_show_hotkey_btn)

    def OnClose(self, e):        
        self.Hide()

    def OnRecordCL(self, e):
        close_hotkey_text = self.FindWindowById(self.ID_CLOSE_HOTKEY_TEXT)
        close_hotkey_btn = self.FindWindowById(self.ID_CLOSE_HOTKEY_BTN)
        self.recordHotkey(close_hotkey_text, close_hotkey_btn)
    
    def RefreshLeftList(self, e=None):
        windows = tool.getAllWindows()
        right = self.ItemsData(self.right_treelist, only_checked=False)
        list = []
        for window in windows:
            flag = 0
            for i in right:
                if tool.isSameWindow(window, i, True):
                    flag = 1
                    break
            if not flag:
                list.append(window)
        self.InsertTreeList(list, self.left_treelist, True)

    def InsertTreeList(self, data: list, treelist: dataview.TreeListCtrl, clear=True):
        if clear:
            treelist.DeleteAllItems()
        root = treelist.GetRootItem()
        process_map = {}
        for window in data:
            # 确保window是WindowInfo对象
            if isinstance(window, dict):
                window = WindowInfo.from_dict(window)
                
            process = window.process
            if process not in process_map:
                exists_node = self.SearchProcessNode(treelist, process)
                if exists_node is None:
                    process_map[process] = treelist.AppendItem(root, process)
                else:
                    process_map[process] = exists_node
            item = treelist.AppendItem(process_map[process], window.title)
            treelist.SetItemText(item, 1, str(window.hwnd))
            treelist.SetItemText(item, 2, str(window.PID))
            treelist.SetItemData(item, window)
        treelist.Expand(root)
        for process in process_map:
            treelist.Expand(process_map[process])
        
        # 初始化所有父节点的选中状态
        for process in process_map:
            self.UpdateParentCheckState(treelist, treelist.GetFirstChild(process_map[process]))

    def SearchProcessNode(self, treelist: dataview.TreeListCtrl, process):
        item = treelist.GetRootItem()
        while item.IsOk():
            item = treelist.GetNextItem(item)
            if not item.IsOk():
                break
            data = treelist.GetItemData(item)
            if data is not None and hasattr(data, 'process') and data.process == process:
                return treelist.GetItemParent(item)
            
    def RemoveItem(self, treelist: dataview.TreeListCtrl, data):
        # 确保data是WindowInfo对象
        if isinstance(data, dict):
            data = WindowInfo.from_dict(data)
            
        node = item = self.SearchProcessNode(treelist, data.process)
        if item is not None:
            item = treelist.GetFirstChild(item)
            while item.IsOk():
                item_data = treelist.GetItemData(item)
                if item_data and item_data == data:
                    treelist.DeleteItem(item)
                    break
                item = treelist.GetNextSibling(item)

            if not treelist.GetFirstChild(node).IsOk():
                # 如果没有子节点了，删除父节点
                treelist.DeleteItem(node)

    def ItemsData(self, treelist: dataview.TreeListCtrl, only_checked=False, item_object=False)->list[WindowInfo]:
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

    def recordHotkey(self, text_ctrl: wx.TextCtrl, btn: wx.Button):
        try:
            Config.HotkeyListener.stop()
        except:
            pass
        btn.Disable()
        btn.SetLabel("录制中...")
        record.RecordedHotkey.confirm = False
        RecordWindow = record.RecordWindow()
        RecordWindow.ShowModal()
        btn.Enable()
        btn.SetLabel("录制热键")
        if record.RecordedHotkey.confirm:
            text_ctrl.SetValue(record.RecordedHotkey.final_key)



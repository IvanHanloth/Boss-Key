import wx
from pynput import keyboard, mouse
import threading

class HotkeyRecorder(wx.Frame):
    def __init__(self, *args, **kw):
        super(HotkeyRecorder, self).__init__(*args, **kw)

        self.panel = wx.Panel(self)
        self.recording = False
        self.keys_pressed = set()
        self.keys_recorded = set()
        self.mouse_pressed = set()
        self.hotkey_display = wx.StaticText(self.panel, label="当前热键：", pos=(20, 80))

        self.textbox1 = wx.TextCtrl(self.panel, pos=(200, 20), size=(150, -1))
        self.textbox2 = wx.TextCtrl(self.panel, pos=(200, 60), size=(150, -1))
        self.textbox3 = wx.TextCtrl(self.panel, pos=(200, 100), size=(150, -1))

        self.button1 = wx.Button(self.panel, label="录制热键1", pos=(20, 20))
        self.button2 = wx.Button(self.panel, label="录制热键2", pos=(20, 60))
        self.button3 = wx.Button(self.panel, label="录制热键3", pos=(20, 100))

        self.button1.Bind(wx.EVT_BUTTON, lambda event: self.startRecording(event, self.textbox1))
        self.button2.Bind(wx.EVT_BUTTON, lambda event: self.startRecording(event, self.textbox2))
        self.button3.Bind(wx.EVT_BUTTON, lambda event: self.startRecording(event, self.textbox3))

        self.rebind_button = wx.Button(self.panel, label="重新绑定热键", pos=(20, 140))
        self.rebind_button.Bind(wx.EVT_BUTTON, self.rebindHotkeys)

        self.keyboard_listener = None
        self.mouse_listener = None
        self.global_listener = None  # 全局热键监听器线程

        self.registered_hotkey_combination = None  # 记录注册的热键组合

        # 处理窗口关闭事件
        self.Bind(wx.EVT_CLOSE, self.onClose)

    def startRecording(self, event, textbox):
        if self.recording:
            self.stopRecording()

        self.recording = True
        self.keys_pressed.clear()
        self.keys_recorded.clear()
        self.mouse_pressed.clear()
        self.hotkey_display.SetLabel("请按下热键组合（包括鼠标按键）...")

        self.keyboard_listener = keyboard.Listener(
            on_press=self.onKeyPress,
            on_release=self.onKeyRelease)
        self.mouse_listener = mouse.Listener(
            on_click=self.onClick)
        self.keyboard_listener.start()
        self.mouse_listener.start()

        self.current_textbox = textbox

    def onKeyPress(self, key):
        key_name = self.getKeyName(key)
        self.keys_pressed.add(key_name)
        self.keys_recorded.add(key_name)

    def onKeyRelease(self, key):
        key_name = self.getKeyName(key)
        if key_name in self.keys_pressed:
            self.keys_pressed.remove(key_name)
        self.checkStopRecording()

    def onClick(self, x, y, button, pressed):
        button_name = button.name.upper()
        if pressed:
            self.mouse_pressed.add(button_name)
            self.keys_recorded.add(button_name)
        else:
            if button_name in self.mouse_pressed:
                self.mouse_pressed.remove(button_name)
        self.checkStopRecording()

    def checkStopRecording(self):
        if not self.keys_pressed and not self.mouse_pressed:
            # 所有按键和鼠标按钮已释放，停止录制
            self.stopRecording()
            hotkey_str = "+".join(sorted(self.keys_recorded))
            wx.CallAfter(self.hotkey_display.SetLabel, f"当前热键：{hotkey_str}")
            if self.current_textbox:
                wx.CallAfter(self.current_textbox.SetValue, hotkey_str)
            
            # 注册热键监听器
            self.registerHotkeyListener(self.keys_recorded, "热键被按下！")

    def stopRecording(self):
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None
        self.recording = False

    def rebindHotkeys(self, event):
        hotkey1 = self.textbox1.GetValue().split('+')
        hotkey2 = self.textbox2.GetValue().split('+')
        hotkey3 = self.textbox3.GetValue().split('+')

        self.registerHotkeyListener(set(hotkey1), "这是1")
        self.registerHotkeyListener(set(hotkey2), "这是2")
        self.registerHotkeyListener(set(hotkey3), "这是3")

    def registerHotkeyListener(self, hotkey_combination, message):
        # 保存注册的热键组合
        self.registered_hotkey_combination = set(hotkey_combination)

        # 启动全局监听器线程
        if self.global_listener:
            # 如果已有监听器，先停止
            self.global_listener.stop()
        self.global_listener = GlobalHotkeyListener(self.registered_hotkey_combination, lambda: self.onHotkeyTriggered(message))
        self.global_listener.start()

    def onHotkeyTriggered(self, message):
        wx.CallAfter(wx.MessageBox, message, "提示", wx.OK | wx.ICON_INFORMATION)

    def getKeyName(self, key):
        if hasattr(key, 'char') and key.char is not None:
            return key.char.upper()
        elif hasattr(key, 'name') and key.name is not None:
            key_name = key.name.lower()
            if key_name in ('ctrl_l', 'ctrl_r'):
                return 'CTRL'
            elif key_name in ('alt_l', 'alt_r', 'alt_gr'):
                return 'ALT'
            elif key_name in ('shift_l', 'shift_r'):
                return 'SHIFT'
            elif key_name == 'esc':
                return 'ESC'
            elif key_name == 'enter':
                return 'ENTER'
            else:
                return key.name.upper()
        else:
            print(str(key))
            return str(key).upper()

    def onClose(self, event):
        # 停止监听器
        if self.global_listener:
            self.global_listener.stop()
        self.Destroy()

class GlobalHotkeyListener(threading.Thread):
    def __init__(self, hotkey_combination, callback):
        super(GlobalHotkeyListener, self).__init__()
        self.hotkey_combination = set(hotkey_combination)
        self.callback = callback
        self.keys_pressed = set()
        self.mouse_pressed = set()
        self.running = True

    def run(self):
        with keyboard.Listener(
                on_press=self.onKeyPress,
                on_release=self.onKeyRelease) as k_listener, \
             mouse.Listener(
                on_click=self.onClick) as m_listener:
            while self.running:
                # 检查是否按下了热键组合
                if self.isHotkeyPressed():
                    self.callback()
                    # 阻止重复触发，等待按键释放
                    while self.isAnyKeyPressed() and self.running:
                        pass
                if not self.running:
                    break
            k_listener.stop()
            m_listener.stop()

    def stop(self):
        self.running = False

    def onKeyPress(self, key):
        key_name = self.getKeyName(key)
        self.keys_pressed.add(key_name)

    def onKeyRelease(self, key):
        key_name = self.getKeyName(key)
        self.keys_pressed.discard(key_name)

    def onClick(self, x, y, button, pressed):
        button_name = button.name.upper()
        if pressed:
            self.mouse_pressed.add(button_name)
        else:
            self.mouse_pressed.discard(button_name)

    def isHotkeyPressed(self):
        current_pressed = self.keys_pressed.union(self.mouse_pressed)
        return self.hotkey_combination == current_pressed

    def isAnyKeyPressed(self):
        return self.keys_pressed or self.mouse_pressed

    def getKeyName(self, key):
        if hasattr(key, 'char') and key.char is not None:
            return key.char.upper()
        elif hasattr(key, 'name') and key.name is not None:
            key_name = key.name.lower()
            if key_name in ('ctrl_l', 'ctrl_r'):
                return 'CTRL'
            elif key_name in ('alt_l', 'alt_r', 'alt_gr'):
                return 'ALT'
            elif key_name in ('shift_l', 'shift_r'):
                return 'SHIFT'
            elif key_name == 'esc':
                return 'ESC'
            elif key_name == 'enter':
                return 'ENTER'
            else:
                return key.name.upper()
        else:
            return str(key).upper()

class MyApp(wx.App):
    def OnInit(self):
        self.frame = HotkeyRecorder(None, title="热键录制示例", size=(400, 200))
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
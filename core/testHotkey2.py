from pynput import keyboard, mouse
import time

class HotkeyListener:
    def __init__(self, hotkeys, callback):
        """
        所有按键使用大写字母
        """
        self.hotkeys = set(hotkeys)
        self.callback = callback
        self.current_keys = set()
        self.is_running = False
        self.k_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.m_listener = mouse.Listener(on_click=self.on_click)

    def start(self):
        if self.is_running:
            return
        self.is_running = True
        self.k_listener.start()
        self.m_listener.start()
    

    def stop(self):
        if not self.is_running:
            return
        self.k_listener.stop()
        self.m_listener.stop()
        self.is_running = False

    def on_press(self, key):
        key_name = self.getKeyName(key)
        print("press",key_name)
        if key_name in self.hotkeys:
            self.current_keys.add(key_name)
            self.checkPressed()

    def on_release(self, key):
        key_name = self.getKeyName(key)
        if key_name in self.hotkeys and key_name in self.current_keys:
                self.current_keys.discard(key_name)
        
    def on_click(self, x, y, button, pressed):
        button_name = button.name.upper()
        if pressed:
            if button_name in self.hotkeys:
                self.current_keys.add(button_name)
        else:
            if button_name in self.hotkeys and button_name in self.current_keys:
                self.current_keys.discard(button_name)
        self.checkPressed()

    def checkPressed(self):
        """
        检查是否按下了热键组合，按下则调用回调函数
        """
        print("current",self.current_keys)
        for hotkey in self.hotkeys:
            if hotkey not in self.current_keys:
                return False
        self.callback()

    def getKeyName(self, key):
        """
        从按键对象中获取按键名称
        """
        key_name = ""
        if hasattr(key, 'char') and key.char is not None:
            key_name = key.char.upper()
        elif hasattr(key, 'name') and key.name is not None:
            key_name = key.name.upper()
        else:
            key_name = str(key).upper()
        return key_name

# 示例回调函数
def my_callback():
    print(time.time(),": 热键组合被按下！")

# 示例使用
hotkeys = ("CTRL_L")
listener = HotkeyListener(hotkeys, my_callback)

# 启动监听器
listener.start()

# 保持程序运行
try:
    while True:
        pass
except KeyboardInterrupt:
    listener.stop()
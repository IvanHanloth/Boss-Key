from winreg import OpenKey,HKEY_CURRENT_USER,QueryValueEx,DeleteValue,CloseKey,KEY_ALL_ACCESS,SetValueEx,REG_SZ
import wx.adv
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from core.config import Config
import win32process
import psutil
import core.vkMap as vkMap

def modifyStartup(name: str, file_path: str):
    key = OpenKey(HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, KEY_ALL_ACCESS)
    try:
        existing_value, _ = QueryValueEx(key, name)

        if existing_value == file_path:
            DeleteValue(key, name)
            CloseKey(key)
            return "Removed"
        else:
            SetValueEx(key, name, 0, REG_SZ, file_path)
            return "Added"
    except WindowsError:
        SetValueEx(key, name, 0, REG_SZ, file_path)
        return "Added"
    
def checkStartup(name: str, file_path: str):
    """
    Check if the startup key exists and if it points to the correct file path

    returns True if the key exists and points to the correct file path
    """
    key = OpenKey(HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, KEY_ALL_ACCESS)
    try:
        existing_value, _ = QueryValueEx(key, name)

        if existing_value == file_path:
            return True
        else:
            return False
    except WindowsError:
        return False
    
def changeMute(hwnd,flag=1):
    """
    flag=1 mute
    """
    # print(hwnd)
    # SendMessage(int(hwnd),0x319, 0x200eb0, 0x08*0x10000)
    hwnd=int(hwnd)
    process=win32process.GetWindowThreadProcessId(hwnd)
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        # if session.Process:
        #     print(session.Process.pid)
        #     print("process[1]",psutil.Process(process[1]))
        #     print("session.Process",session.Process)
        if session.Process and session.Process.name() == psutil.Process(process[1]).name():
            print("mute")
            volume.SetMute(flag, None)
            break

def sendNotify(title,message):
    notify = wx.adv.NotificationMessage(title=title,message=message,parent=None)
    notify.SetIcon(wx.Icon(wx.Image(Config.icon).ConvertToBitmap()))
    notify.UseTaskBarIcon(Config.TaskBarIcon)
    notify.Show(timeout=3) # 1 for short timeout, 100 for long timeout

def keyMux(key):
    """
    按键多合一
    """
    
    key_name = key.name.lower()
    for n,v in vkMap.ScanName2VKName.items():
        if key_name == n.lower():
            return v
        
    return key_name.upper()

def keyConvert(hotkeys: dict):
    """
    按键解析

    传入：
    hotkeys: dict，键为热键，值为函数
    """
    expanded_hotkeys = {}
    need_check = {}
    flag = True
    # 将self.hotkeys中的每一项的键修改为小写
    for hotkey, action in hotkeys.items():
        hotkey = hotkey.lower()
        need_check[hotkey] = action
    while flag:
        flag = False
        this_round = need_check.copy()
        function_keys=[
            'ctrl','alt','shift','esc','enter','cmd','page_up',
            'page_down','home','end','insert','delete','backspace',
            'space','up','down','left','right','tab','caps_lock',
            'num_lock','scroll_lock','print_screen','pause','menu'
        ]
        for i in range(1,13):
            function_keys.append(f'f{i}')
        for hotkey, action in this_round.items():
            hotkey = hotkey.lower()
            keys = hotkey.split('+')
            intersect = list(set(keys) & set(function_keys))
            if len(intersect)>=1:
                i=intersect[0]
                del need_check['+'.join(keys)]
                keys.remove(i)
                keys.append(f"<{i}>")
                need_check['+'.join(keys)] = action
                flag = True
                continue

            if 'win' in keys:
                del need_check['+'.join(keys)]
                keys.remove('win')
                keys.append('<cmd>')
                need_check['+'.join(keys)] = action
                flag = True
                continue
            else:
                expanded_hotkeys['+'.join(keys)] = action

    return expanded_hotkeys
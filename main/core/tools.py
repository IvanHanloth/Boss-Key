import winreg
import wx.adv
import wx
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from core.config import Config
import win32process,win32gui
import psutil
import core.vkMap as vkMap
import datetime
import requests
import json
import win32api
import win32con
import win32ui

def check_update():
    requests.packages.urllib3.disable_warnings()
    # 获取最新版本信息
    try:
        response = requests.get("https://ivanhanloth.github.io/Boss-Key/releases.json", verify=False,timeout=10)
        
        if response.status_code != 200:
            raise Exception("无法检查更新")
    except:
        raise Exception("无法检查更新")

    releases = json.loads(response.text)

    for release in releases:
        release['published_at'] = datetime.datetime.strptime(release['published_at'], "%Y-%m-%dT%H:%M:%SZ")
    
    # 找到最新的版本
    latest_release = max(releases, key=lambda x: x['published_at'])
    
    return latest_release

def addStartup(program_name, program_path):
    """
    将程序添加到开机自启动

    :param program_name: 注册表中的程序名称
    :param program_path: 程序的完整路径
    """
    # 打开注册表中的自启动项
    key = winreg.HKEY_CURRENT_USER
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    try:
        # 打开注册表键
        registry_key = winreg.OpenKey(key, key_path, 0, winreg.KEY_WRITE)
        # 设置注册表项
        winreg.SetValueEx(registry_key, program_name, 0, winreg.REG_SZ, program_path)
        # 关闭注册表键
        winreg.CloseKey(registry_key)
        return True
    except WindowsError as e:
        return False

def removeStartup(program_name):
    """
    从开机自启动中移除程序

    :param program_name: 注册表中的程序名称
    """
    # 打开注册表中的自启动项
    key = winreg.HKEY_CURRENT_USER
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    
    try:
        # 打开注册表键
        registry_key = winreg.OpenKey(key, key_path, 0, winreg.KEY_WRITE)
        # 删除注册表项
        winreg.DeleteValue(registry_key, program_name)
        # 关闭注册表键
        winreg.CloseKey(registry_key)
        return True
    except WindowsError as e:
        return False
    
def checkStartup(name: str, file_path: str):
    """
    Check if the startup key exists and if it points to the correct file path

    returns True if the key exists and points to the correct file path
    """
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ)
    try:
        existing_value, _ = winreg.QueryValueEx(key, name)

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
    try:
        hwnd=int(hwnd)
        process=win32process.GetWindowThreadProcessId(hwnd)
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session.SimpleAudioVolume
            if session.Process and session.Process.name() == psutil.Process(process[1]).name():
                volume.SetMute(flag, None)
                break
    except:
        pass

def remove_duplicates(input_list: list):
    """
    Remove duplicates from a list while preserving the order.
    
    input_list: list, the list from which to remove duplicates
    returns: list, the list without duplicates
    """
    seen = set()
    output_list = []
    for item in input_list:
        if item not in seen:
            seen.add(item)
            output_list.append(item)
    return output_list

def hwnd2processName(hwnd):
    """
    从窗口句柄获取进程名称
    返回None为不存在的窗口
    """
    try:
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        process_name = psutil.Process(pid).name()
    except:
        process_name=None
    return process_name

def hwnd2windowName(hwnd):
    """
    从窗口句柄获取窗口名称
    返回None为不存在的窗口
    """
    try:
        title = win32gui.GetWindowText(hwnd)
        if not title or title=="":
            title="无标题窗口"
    except:
        title=None
    return title

def getAllWindows():
    # 获取所有窗口信息
    def enumHandler(hwnd, windows: list):
        if win32gui.IsWindowVisible(hwnd):
            title = hwnd2windowName(hwnd)
            pid = win32process.GetWindowThreadProcessId(hwnd)[1]
            process_name = psutil.Process(pid).name()
            icon = getProcessIcon(hwnd)
            windows.append({'title': title, 'hwnd': int(hwnd), 'process': process_name, 'PID': int(pid), 'icon': icon})
        return True

    def getProcessIcon(hwnd):
        hicon = win32gui.SendMessage(hwnd, win32con.WM_GETICON, win32con.ICON_SMALL, 0)
        if hicon == 0:
            hicon = win32gui.SendMessage(hwnd, win32con.WM_GETICON, win32con.ICON_BIG, 0)
        if hicon == 0:
            hicon = win32gui.GetClassLong(hwnd, win32con.GCL_HICON)
        if hicon == 0:
            hicon = win32gui.GetClassLong(hwnd, win32con.GCL_HICONSM)
        print(hicon)
        if hicon != 0:
            hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(hwnd))
            hbmp = win32ui.CreateBitmap()
            hbmp.CreateCompatibleBitmap(hdc, 32, 32)
            hdc = hdc.CreateCompatibleDC()
            hdc.SelectObject(hbmp)
            hdc.DrawIcon((0, 0), hicon)
            hdc.DeleteDC()
            bmpinfo = hbmp.GetInfo()
            bmpstr = hbmp.GetBitmapBits(True)
            bmp =wx.Bitmap(32,32)
            bmp.SetHandle(hbmp.GetHandle())
            icon = wx.Icon()
            icon.CopyFromBitmap(bmp)
            return icon
        return None

    windows = []
    win32gui.EnumWindows(enumHandler, windows)
    windows.sort(key=lambda x: x['title'])

    return windows

def isSameWindow(w1:dict,w2:dict,strict=False):
    """
    判断两个窗口的信息是否指向同一个窗口
    w1、w2: dict, 包含hwnd、title、process、PID
    strict: 启用严格模式
    """
    
    ## 一模一样的两个，肯定是同一个
    if w1==w2:
        return True
    
    process_except=["explorer.exe"]

    hwnd_same=w1['hwnd']==w2['hwnd']
    title_same=w1['title']==w2['title'] and w1['title']!="无标题窗口"
    process_name_same=w1['process']==w2['process'] and w1 not in process_except
    PID_same=w1['PID']==w2['PID']
    process_same=process_name_same or PID_same

    ## 非严格模式下
    if not strict:
        ## 进程名称相同且标题名称相同则同一个
        if process_name_same and title_same:
            return True
        ## 窗口句柄相同
        if hwnd_same:
            return True
        
    ## 如果两个窗口句柄相同，并且进程相同，则视为同一个
    if hwnd_same and process_same:
        return True

    ## 进程相同，并且窗口标题相同，则视为同一个
    if process_same and title_same:
        return True

    return False

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
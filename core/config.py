import os
import sys
from .icon import get_icon,icon_info
from configparser import RawConfigParser
import io

class Config:
    hwnd=0
    hwnd_b = ""
    hwnd_n = ''
    times=1

    hide_hotkey = "Ctrl+Q"
    startup_hotkey = "Alt+Q"
    close_hotkey = "Win+Esc"

    mute_after_hide = True
    
    ini_path = os.path.join(os.getcwd(), "config.ini")
    icon=io.BytesIO(get_icon())
    icon_info=os.path.join(os.path.dirname(sys.argv[0]),"icon.ico")
    file_path=sys.argv[0]
    # 判断是否为首次启动
    first_start = not os.path.exists(ini_path)

    SettingWindow=""
    HotkeyWindow=""
    TaskBarIcon=""
    
    recording_hotkey = False
    recorded_hotkey = None

def load_config():
    if Config.first_start:
        save_config()
        return
    
    config = RawConfigParser()
    config.read(Config.ini_path, encoding = "utf-8")

    Config.hwnd = config.getint("history", "hwnd")
    try:
        Config.mute_after_hide=config.getboolean("setting","mute_after_hide")
    except:
        Config.mute_after_hide=True
        Config.first_start=True
        save_config()

    Config.hide_hotkey = config.get("hotkey", "hide_hotkey", fallback="Ctrl+Q")
    Config.startup_hotkey = config.get("hotkey", "startup_hotkey", fallback="Alt+Q")
    Config.close_hotkey = config.get("hotkey", "close_hotkey", fallback="Win+Esc")

def save_config():
    config = RawConfigParser()

    config.add_section("history")
    config['history']['hwnd']=str(Config.hwnd)

    config.add_section("hotkey")
    config['hotkey']['hide_hotkey'] = Config.hide_hotkey
    config['hotkey']['startup_hotkey'] = Config.startup_hotkey
    config['hotkey']['close_hotkey'] = Config.close_hotkey

    config.add_section("setting")
    config['setting']['mute_after_hide']=str(Config.mute_after_hide)

    with open(Config.ini_path, 'w', encoding='utf-8') as configfile:
        config.write(configfile)


load_config()

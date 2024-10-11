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

    hide_f="Ctrl"
    hide_v="Q"

    startup_f="Alt"
    startup_v="Q"

    close_f="Win"
    close_v="Esc"

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

    Config.hide_f = config.get("hotkey", "hide_f")
    Config.hide_v = config.get("hotkey", "hide_v")

    Config.startup_f = config.get("hotkey", "startup_f")
    Config.startup_v = config.get("hotkey", "startup_v")

    Config.close_f = config.get("hotkey", "close_f")
    Config.close_v = config.get("hotkey", "close_v")

def save_config():
    config = RawConfigParser()

    config.add_section("history")
    config['history']['hwnd']=str(Config.hwnd)

    config.add_section("hotkey")
    config['hotkey']['hide_f']=Config.hide_f
    config['hotkey']['hide_v']=Config.hide_v

    config['hotkey']['startup_f'] = Config.startup_f
    config['hotkey']['startup_v'] = Config.startup_v

    config['hotkey']['close_f'] = Config.close_f
    config['hotkey']['close_v'] = Config.close_v

    config.add_section("setting")
    config['setting']['mute_after_hide']=str(Config.mute_after_hide)

    with open(Config.ini_path, 'w', encoding='utf-8') as configfile:
        config.write(configfile)


load_config()

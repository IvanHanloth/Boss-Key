import os
import sys
import json
from .icon import get_icon
from configparser import ConfigParser
import io

class Config:
    AppVersion = "1.4.3.0"
    AppReleaseDate = "2024-12-19"
    AppAuthor = "IvanHanloth"
    AppCopyRight = "Copyright © 2024 Ivan Hanloth All Rights Reserved."

    hwnd=0
    hwnd_b = ""
    hwnd_n = ''
    times=1

    hide_hotkey = "Ctrl+Q"
    startup_hotkey = "Alt+Q"
    close_hotkey = "Win+Esc"

    mute_after_hide = True
    send_before_hide = False
    
    config_path = os.path.join(os.getcwd(), "config.json")
    icon=io.BytesIO(get_icon())
    icon_info=os.path.join(os.path.dirname(os.path.dirname(__file__)),"icon.ico")
    file_path=sys.argv[0]
    # 判断是否为首次启动
    first_start = not os.path.exists(config_path)

    SettingWindow=""
    HotkeyWindow=""
    TaskBarIcon=""
    
    recording_hotkey = False
    recorded_hotkey = None
    
    @staticmethod
    def load():
        if os.path.exists(os.path.join(os.getcwd(), "config.ini")):
            Config.import_from_ini()
            

        if Config.first_start:
            Config.save()
            return

        with open(Config.config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        Config.hwnd = config.get("history", {}).get("hwnd", 0)
        Config.mute_after_hide = config.get("setting", {}).get("mute_after_hide", True)
        Config.send_before_hide = config.get("setting", {}).get("send_before_hide", False)
        Config.hide_hotkey = config.get("hotkey", {}).get("hide_hotkey", "Ctrl+Q")
        Config.startup_hotkey = config.get("hotkey", {}).get("startup_hotkey", "Alt+Q")
        Config.close_hotkey = config.get("hotkey", {}).get("close_hotkey", "Win+Esc")

        if config.get('version', '') != Config.AppVersion:
            Config.save()
            Config.first_start = True

    @staticmethod
    def save():
        config = {
            'version': Config.AppVersion,
            'history': {
                'hwnd': Config.hwnd
            },
            'hotkey': {
                'hide_hotkey': Config.hide_hotkey,
                'startup_hotkey': Config.startup_hotkey,
                'close_hotkey': Config.close_hotkey
            },
            'setting': {
                'mute_after_hide': Config.mute_after_hide,
                'send_before_hide': Config.send_before_hide
            }
        }

        with open(Config.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

    @staticmethod
    def import_from_ini():
        ## import from the old config file
        config = ConfigParser()
        configpath=os.path.join(os.getcwd(), "config.ini")
        config.read(configpath, encoding='utf-8')
    
        Config.hwnd = config.getint("history", "hwnd", fallback=0)
        Config.mute_after_hide = config.getboolean("setting", "mute_after_hide", fallback=True)
        Config.send_before_hide = config.getboolean("setting", "send_before_hide", fallback=False)
        Config.hide_hotkey = config.get("hotkey", "hide_hotkey", fallback="Ctrl+Q")
        Config.startup_hotkey = config.get("hotkey", "startup_hotkey", fallback="Alt+Q")
        Config.close_hotkey = config.get("hotkey", "close_hotkey", fallback="Win+Esc")
        Config.save()
        os.remove(configpath)
        

Config.load()

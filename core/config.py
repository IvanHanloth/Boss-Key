import os
import sys
from .icon import get_icon,icon_info
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
    
    @staticmethod
    def load():
        if Config.first_start:
            Config.save()
            return
        
        config = ConfigParser()
        config.read(Config.ini_path, encoding = "utf-8")

        Config.hwnd = config.getint("history", "hwnd")
        try:
            Config.mute_after_hide=config.getboolean("setting","mute_after_hide")
        except:
            Config.mute_after_hide=True
            Config.first_start=True
            Config.save()

        try:
            Config.send_before_hide=config.getboolean("setting","send_before_hide")
        except:
            Config.send_before_hide=False
            Config.first_start=True
            Config.save()

        old_version=False
        
        try:
            Config.hide_hotkey = config.get("hotkey", "hide_f") +config.get("hotkey", "hide_v") 
            Config.startup_hotkey = config.get("hotkey", "startup_f") +config.get("hotkey", "startup_v")
            Config.close_hotkey = config.get("hotkey", "close_f") +config.get("hotkey", "close_v")
            Config.first_start=True
            old_version=True
            ## 适配老版本数据
        except:
            pass
        Config.save()
        if not old_version: 
            # 没有使用老版本
            Config.hide_hotkey = config.get("hotkey", "hide_hotkey", fallback="Ctrl+Q")
            Config.startup_hotkey = config.get("hotkey", "startup_hotkey", fallback="Alt+Q")
            Config.close_hotkey = config.get("hotkey", "close_hotkey", fallback="Win+Esc")
            

    @staticmethod
    def save():
        config = ConfigParser()

        config['history']={
            'hwnd':str(Config.hwnd)
        }
        
        config['hotkey']={
            'hide_hotkey':Config.hide_hotkey,
            'startup_hotkey':Config.startup_hotkey,
            'close_hotkey':Config.close_hotkey
        }

        config['setting']={
            'mute_after_hide':str(Config.mute_after_hide),
            'send_before_hide':str(Config.send_before_hide)
        }

        with open(Config.ini_path, 'w', encoding='utf-8') as configfile:
            config.write(configfile)


Config.load()

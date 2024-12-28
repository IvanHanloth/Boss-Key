import os
import sys
import json
from .icon import get_icon
from configparser import ConfigParser
import io

class Config:
    AppName = "Boss Key"
    AppVersion = "1.4.3.0"
    AppReleaseDate = "2024-12-19"
    AppAuthor = "IvanHanloth"
    AppDescription = "老板来了？快用Boss-Key一键隐藏静音当前窗口！上班摸鱼必备神器"
    AppCopyRight = "Copyright © 2022-2025 Ivan Hanloth All Rights Reserved."
    AppWebsite = "https://github.com/IvanHanloth/Boss-Key"
    AppLicense = """MIT License

Copyright (c) 2022 Ivan Hanloth

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

    hwnd=0
    hwnd_b = ""
    hwnd_n = ''
    times=1

    hide_hotkey = "Ctrl+Q"
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
        Config.close_hotkey = config.get("hotkey", "close_hotkey", fallback="Win+Esc")
        Config.save()
        os.remove(configpath)
        

Config.load()

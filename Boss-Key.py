from core.BossKey import BossKey
import msvcrt
import os
import sys
import ctypes

errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2) # Win10 and Win8
success = ctypes.windll.user32.SetProcessDPIAware() #Win7 and below

def is_already_running(lock_file):
    try:
        # 打开锁文件
        lock_fd = open(lock_file, 'w')
        # 使用msvcrt锁定文件
        msvcrt.locking(lock_fd.fileno(), msvcrt.LK_NBLCK, 1)
        return False
    except IOError:
        return True
if is_already_running(sys.argv[0][:-4]+".lock"):
    sys.exit(1)
print(sys.argv[0][:-4]+".lock")
Boss_Key=BossKey()
Boss_Key.Start()
    

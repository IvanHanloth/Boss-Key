from core.BossKey import BossKey
import psutil
import ctypes

errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2) # Win10 and Win8
success = ctypes.windll.user32.SetProcessDPIAware() #Win7 and below

def isExist_Process(processname):
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        if p.name() == processname:
            return True
    else:
         return False
if not isExist_Process("Boss Key Application"):
    Boss_Key=BossKey()
    Boss_Key.Start()
    

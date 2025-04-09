class WindowInfo:
    """
    窗口信息模型
    """
    title:str = None
    hwnd:int = None
    process:str = None
    PID:int = None
    path:str = None

    def __init__(self, title:str, hwnd:int, process:str, PID:int, path:str=None):
        self.title = title
        self.hwnd = hwnd
        self.process = process
        self.PID = PID
        self.path = path
    
    def to_dict(self):
        """将对象转为字典，用于JSON序列化"""
        return {
            "title": self.title,
            "hwnd": self.hwnd,
            "process": self.process,
            "PID": self.PID,
            "path": self.path
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建对象，用于JSON反序列化"""
        return cls(
            title=data.get('title', '无标题窗口'),
            hwnd=data.get('hwnd', 0),
            process=data.get('process', ''),
            PID=data.get('PID', 0),
            path=data.get('path', '')
        )
    
    def __eq__(self, other):
        """比较两个WindowInfo是否相等"""
        if not isinstance(other, WindowInfo):
            return False
        return (self.hwnd == other.hwnd and 
                self.process == other.process and 
                self.PID == other.PID and 
                self.title == other.title and
                self.path == other.path)
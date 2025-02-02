# Boss-Key

![](/src/static/bannar.jpg)

![Github Release Version](https://img.shields.io/github/v/release/IvanHanloth/Boss-Key)
![Github Repo License](https://img.shields.io/github/license/IvanHanloth/Boss-Key)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/IvanHanloth/Boss-Key/tag-release.yml)
![Supported Platform](https://img.shields.io/badge/Platform-Windows_10\+-cornflowerblue)
![Python Version](https://img.shields.io/badge/Python-3.11.9-coral)

老板来了？快用Boss-Key老板键一键隐藏窗口！上班摸鱼必备神器。

支持多窗口隐藏、多进程隐藏、自定义热键、隐藏活动窗口、静音窗口、暂停视频播放等超多功能，完全免费、开源，无强制弹窗等

## 应用截图
![](/src/static/screenshot-1.png)

![](/src/static/screenshot-2.png)

![](/src/static/screenshot-3.png)

![](/src/static/screenshot-4.png)

## 使用说明
从v2.0.0版本开始，每个版本都会提供三种类型的程序，可以从[Release页面](https://github.com/IvanHanloth/Boss-Key/releases)下载
- onefile - 单文件版，只有一个可执行程序，相对简洁、方便。由于每次启动都需要解压依赖，启动较慢、可能会被报毒
- multifile - 多文件版，标准的程序版本，所有依赖文件被压缩到一个压缩包里，解压后可用
- installer - 安装程序（推荐），完整封装的Boss-Key程序安装程序，提供一键安装、更新、卸载，可以更高效的管理Boss-Key程序


### 基础使用

安装或更新后首次打开Boss-Key，会自动弹出设置页面，可以在其中进行热键修改、进程及窗口绑定的等操作。

而一般使用时，可以通过右键点击托盘图标打开菜单。点击菜单中的“设置”即可打开设置页面。

右键点击托盘图标还有退出程序、检查更新、设置开机自启等功能。

按下隐藏/显示窗口热键可以一键隐藏所绑定的窗口。按下一键关闭程序热键可以一键关闭Boss-Key程序

完成设置后，**记得点击下方的“保存设置”按钮保存并启用设置**

### 绑定窗口

通过绑定窗口，可以同时隐藏多个窗口，摸鱼更安全~

设置窗口中上方部分，左边列表是当前存在的窗口，右边列表是已经绑定的窗口

在左边列表中选中希望隐藏的窗口，点击“添加绑定”可以将窗口信息添加到右边。同理，在右边窗口中选择不需要绑定的窗口，点击“删除绑定”可以将绑定信息移动到左边。

如果发现新打开的窗口没有在列表中显示，可以点击“刷新进程”按钮，刷新左边的列表。

完成所有选择后，**记得点击下方的“保存设置”按钮保存并启用设置**

### 修改热键

修改热键有两种方式，可以通过直接编辑文本框中的内容来修改绑定的热键，或者点击“录制热键”按钮，打开热键录制窗口进行录制。

打开热键录制窗口后，按下的组合键将被记录，并显示在窗口中，如果确认无误，点击确认，将自动填写至热键文本框中。

完成所有热键修改后，**记得点击下方的“保存设置”按钮保存并启用设置**

### 检查更新

右键点击托盘打开托盘菜单，选择“检查更新”即可打开当前检查更新窗口。

检查更新窗口会自动尝试从Github获取最新版本更新信息以及更新地址，点击需要的版本可以跳转下载。

### 其他功能
#### 隐藏窗口后静音
启用该功能后，如果需要隐藏的窗口正在播放音频，则该窗口将被静音。恢复显示后静音将被取消

#### 隐藏前发送暂停键
启用该功能后，隐藏窗口前会向窗口发送暂停键尝试暂停其中的媒体播放。

注意！此功能仍在测试，启用后会导致窗口隐藏出现延时

#### 同时隐藏当前活动窗口
启用该功能后，按下隐藏窗口热键时，除了会隐藏绑定的窗口，还会隐藏当前被激活的窗口。

#### 点击托盘图标切换隐藏状态
启用该功能后，可以通过单击托盘图标来显示或隐藏窗口

### 设置和关闭开机自启
如果需要让Boss-Key程序开机自启，可以右键点击托盘图标，在弹出的菜单中选择“开机自启”来切换开机自启状态

## 常见问题
**为什么我的电脑运行不了编译后的程序**

编译版由于使用的Python3.11版本进行的封装，Windows10以下的版本可能无法正常使用，可参考[https://blog.ivan-hanloth.cn/archives/664/](https://blog.ivan-hanloth.cn/archives/664/)尝试解决

如果你安装了python环境，也可以尝试克隆仓库后，运行Boss-Key.py文件来启动窗口

**为什么我一直没办法检查更新**
检查更新的服务依赖Github提供的Github Page，如果你的电脑无法访问[https://ivanhanloth.github.io/Boss-Key](https://ivanhanloth.github.io/Boss-Key)，则无法检查更新

## 项目结构
仓库项目结构及解释如下：

```
Boss-Key
├── .github     Github配置文件、工作流文件
│   ├── inno-script     InnoSetup配置文件夹
│   └── workflows       Github Action工作流文件
│       ├── build-test.yml      构建测试工作流
│       ├── jekyll-gh-pages.yml     GithubPage构建工作流
│       └── tag-release.yml     推送tag自动构建发布Release工作流
├── main     程序所在目录
│   ├── core    核心文件目录
│   │   ├── __init__.py     初始化包
│   │   ├── config.py     配置文件相关
│   │   ├── icon.py     图标信息
│   │   ├── listener.py     热键监听进程
│   │   ├── tools.py     工具函数
│   │   └── vkMap.py     vk映射表
│   ├── GUI     GUI界面目录
│   │   ├── __init__.py     初始化包
│   │   ├── about.py     关于页面
│   │   ├── record.py     录制热键页面
│   │   ├── setting.py     设置页面
│   │   └── taskbar.py     托盘图标
│   └── Boss-Key.py     项目入口文件
├── src     网站相关目录
│   └── static     静态文件目录
├── .gitignore     git忽略文件列表
├── icon.ico     Boss-Key logo文件
├── LICENSE     开源协议
├── README.md     README文件
└── requirements.txt     项目依赖文件

```

## 已知问题
- 无法隐藏部分游戏窗口，可能由于游戏窗口加密导致

## 更新日志
**V2.1.0 （更新于2025/1/17）**
- 修改已在运行时的提醒
- 修复窗口销毁后再打开隐藏失败的问题
- 优化同时运行检测
- 保存新窗口绑定时自动显示已隐藏的窗口

**V2.0.0 （更新于2025/1/5）**
- 重构设置页面
- 新增支持多窗口、多进程隐藏
- 新增检查更新功能
- 新增点击托盘图标切换窗口隐藏功能
- 新增是否同时隐藏当前窗口的选项
- 完全移除启动切换热键
- 优化配置文件存储
- 优化窗口通知功能
- 优化窗口隐藏相关功能
- 优化热键监听稳定性

**V1.4.3 （更新于2024/12/19）**
- 新增隐藏前发送暂停功能
- 新增热键录制窗口
- 新增关于页面
- 新增托盘开机自启设置菜单项
- 修复部分热键录制时出错问题
- 修复单文件版提示无图标的问题

**V1.4.2（更新于2024/11/16）**
- 新增允许2个以上按键的热键
- 新增录制热键功能
- 优化后台适配

**V1.4.0（更新于2024/10/11）**
- 新增窗口隐藏后静音功能
- 修改默认关闭程序键位
- 修复每次弹窗的问题
- 修复重复启动导致的绑定出错问题
- 优化退出速度

**V1.3.0（更新于2023/9/17）**
- 使用面向对象重写
- 新增设置GUI页面
- 新增托盘图标菜单
- 新增一键安装程序
- 优化使用体验
- 优化适配Windows11系统
- 修复自启动失败问题
- 取消单文件版程序

**v1.2.0（更新于2023/5/21）**
- 修复自启动修改出错问题

**V1.1.0（更新于2023/5/21）**
- 修复部分电脑报毒问题

**V1.0.0（更新于2023/5/12）**
- Boss-Key发布

![](/src/static/icon.png)
# BaiduyunDownload
一款由python编写的可以不限速下载百度云网盘的macOS客户端

## 说明
本软件通过注入百度云客户端获取用户信息，利用aria2软件通过百度云的API多线程下载网盘文件
本软件暂只支持下载自己网盘的文件

## 用法
1. `python3 main.py` or [下载](https://github.com/lyp741/BaiduyunDownload/releases/download/1.0/BaiduDownload-v1.0.zip)
双击可执行文件
2. 点击上方按钮，自动打开百度云客户端
![](https://github.com/lyp741/BaiduyunDownload/raw/master/imgs/open.png)
3. 成功后下方会列出网盘里的文件 (若不成功多试几次，百度云崩溃属于正常现象。。)
![](https://github.com/lyp741/BaiduyunDownload/raw/master/imgs/load.png)
4. 选中文件名或文件夹开始下载,
![](https://github.com/lyp741/BaiduyunDownload/raw/master/imgs/download.png)
5. 终端显示下载进度和速度
![](https://github.com/lyp741/BaiduyunDownload/raw/master/imgs/speed.png)
## Requirements
安装python包
`pip3 install requests,frida,pyqt5,pexpect`

- 需要安装百度云mac客户端
- 需要安装aria2下载器

## 打包
通过如下命令可将python文件打包为可执行文件
`pyinstaller --windowed --onefile --clean --noconfirm main.py`
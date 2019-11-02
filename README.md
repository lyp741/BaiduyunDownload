# BaiduyunDownload
一款由python编写的可以不限速下载百度云网盘的macOS客户端

## 说明
本软件通过注入百度云客户端获取用户信息，利用aria2软件通过百度云的API多线程下载网盘文件
本软件暂只支持下载自己网盘的文件

## 用法
1. `python3 main.py`
2. 点击上方按钮，自动打开百度云客户端
3. 成功后下方会列出网盘里的文件
4. 双击文件名称开始下载

## Requirements
安装python包
`pip3 install requests,frida,pyqt5,pexpect`

- 需要安装百度云mac客户端
- 需要安装aria2下载器


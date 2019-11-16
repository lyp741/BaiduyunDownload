import ssl
from DownloadBaiduYun import DownloadBDY
import sys
import PyQt5.QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

class PathList():
    def __init__(self):
        self.stack = []
    def add(self,o):
        self.stack.append(o)
    def pop(self):
        if len(self.stack)>0:
            return self.stack.pop()
        else:
            return None
    def __str__(self):
        s = ''
        for i in self.stack:
            s += '/'
            s += i
        s += '/'
        if s == '':
            s = '/'
        return s
    def __len__(self):
        return len(self.stack)

class InitThread(QThread):
    def __init__(self,UI):
        super().__init__()
        self.UI = UI
    def run(self):
        self.UI.bdy = DownloadBDY()
        self.UI.label.setText('Complete')
        self.UI.bdy.list_files()
        for l in self.UI.bdy.filelist:
            self.UI.listW.addItem(('📁' if l['isdir']== 1 else '' )+ l['server_filename'])

class DownloadThread(QThread):
    def __init__(self, fname, bdyd, show=True):
        super().__init__()
        self.fname = fname
        self.bdyd = bdyd
        self.show = show
    def run(self):
        if self.show:
            self.bdyd.sigDlded.emit('Downloading','Downloading '+self.fname) 
        self.bdyd.bdy.Download_from_path(self.fname)
        if self.show:
            self.bdyd.sigDlded.emit('Downloaded','Download '+self.fname+' Success!') 

class DownloadPath(QThread):
    def __init__(self,dirname,bdyd):
        super().__init__()
        self.dirname = dirname
        self.bdyd = bdyd
    def run(self):
        filenameList = self.bdyd.walkPath(self.dirname)
        print(filenameList)
        for i in filenameList:
            self.t = DownloadThread(i,self.bdyd,False)
            self.t.start()
            self.t.wait()
        if self.bdyd.bdy.failed != []:
            self.bdyd.sigDlded.emit('Downloaded','Download '+self.dirname+' Failed!')
            print('failed.....')
            print(self.bdyd.bdy.failed)
            self.bdyd.bdy.failed = []
        else:
            self.bdyd.sigDlded.emit('Downloaded','Download '+self.dirname+' Success!')


class BDYDownload(QWidget):
    bdy = None
    sigDlded = pyqtSignal(str, str)
    
    def buttonClick(self):
        self.listW.clear()
        self.label.setText('Open Baidu Yun')
        self.initT = InitThread(self)
        self.initT.start()
    
    def download(self):
        i = self.listW.currentRow()
        if i != -1:
            item = self.bdy.filelist[i]
            if item['isdir'] != 1:
                fileName = self.pathBox.displayText()
                self.t = DownloadThread(fileName,self)
                self.t.start()
                return
        self.downloadPath(self.pathBox.displayText())
        
        # self.ShowMsg('error','暂不支持下载文件夹')
    
    def walkPath(self, dirname):
        total = []
        l = self.bdy.get_list_files(dirname)
        for i in l:
            if i['isdir'] == 1:
                total += self.walkPath(dirname + '/' + i['server_filename'])
            else:
                total.append(dirname + '/' + i['server_filename'])
        return total

    def downloadPath(self,dirname):
        self.pt = DownloadPath(dirname,self)
        self.pt.start()
        self.ShowMsg('Downloading','Downloading '+dirname)


    def ShowMsg(self, title, info):
        # global app, label, listW, window, bdy
        QMessageBox.information(self.window, title, info, QMessageBox.Yes)

    def listDoubleClicked(self):
        
        # global app, label, listW, window, bdy
        i = self.listW.currentRow()
        item = self.bdy.filelist[i]
        if item['isdir'] == 1:
            self.bdy.list_files(str(self.curPath)+item['server_filename'])
            self.curPath.add(item['server_filename'])
            self.list_files()

    def __init__(self):
        super().__init__()
        self.InitUI()

    def list_files(self):
        self.listW.clear()
        for l in self.bdy.filelist:
            self.listW.addItem(('📁' if l['isdir']== 1 else '' )+ l['server_filename'])

    def itemClicked(self):
        i = self.listW.currentRow()
        item = self.bdy.filelist[i]
        
        self.pathBox.setText(str(self.curPath)+item['server_filename'])

    def up(self):
        self.curPath.pop()
        self.bdy.list_files(str(self.curPath))
        self.list_files()
        self.pathBox.setText(str(self.curPath))


    def InitUI(self):
        self.label = QLabel('点击“打开百度云”获取账号信息')
        self.button = QPushButton('打开百度云')
        self.window = QWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)

        self.pathBox = QLineEdit(self)
        self.curPath = PathList()
        self.pathBox.setText(str(self.curPath))
        self.pathBox.setReadOnly(True)
        self.pathLayout = QHBoxLayout()
        self.pathLayout.addWidget(self.pathBox)
        self.upPath = QPushButton('返回上一层')
        self.upPath.clicked.connect(self.up)
        self.pathLayout.addWidget(self.upPath)
        self.downloadButton = QPushButton('下载')
        self.downloadButton.clicked.connect(self.download)
        self.pathLayout.addWidget(self.downloadButton)
        self.layout.addLayout(self.pathLayout)
        self.listW = QListWidget()
        self.listW.itemDoubleClicked.connect(self.listDoubleClicked)
        self.listW.itemClicked.connect(self.itemClicked)
        self.layout.addWidget(self.listW)

        self.sigDlded.connect(self.ShowMsg)

        self.window.setLayout(self.layout)
        self.window.setGeometry(300, 100, 800, 600)
        self.window.show()
        self.button.clicked.connect(self.buttonClick)

app = QApplication([])
app.setStyle('Fusion')
bdydl = BDYDownload()
app.exec_()
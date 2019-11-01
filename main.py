from DownloadBaiduYun import DownloadBDY
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

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
        def __init__(self, item, bdyd):
            super().__init__()
            self.item = item
            self.bdyd = bdyd
        def run(self):
            fname = self.item['server_filename']
            self.bdyd.sigDlded.emit('Downloading','Downloading '+fname) 
            self.bdyd.bdy.Download_from_path(fname)
            self.bdyd.sigDlded.emit('Downloaded','Download '+fname+' Success!') 

class BDYDownload(QWidget):
    bdy = None
    sigDlded = pyqtSignal(str, str)
    
    def buttonClick(self):
        self.listW.clear()
        self.label.setText('Open Baidu Yun')
        self.initT = InitThread(self)
        self.initT.start()
        
        
    def ShowMsg(self, title, info):
        # global app, label, listW, window, bdy
        QMessageBox.information(self.window, title, info, QMessageBox.Yes)

    def listDoubleClicked(self):
        # global app, label, listW, window, bdy
        i = self.listW.currentRow()
        item = self.bdy.filelist[i]
        if item['isdir'] != 1:
            self.t = DownloadThread(item,self)
            self.t.start()
            # QMessageBox.information(self.window, 'Downloading...','Downloading...', QMessageBox.Yes)

    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.label = QLabel('Press "Push" to get the information')
        self.button = QPushButton('Push')
        self.window = QWidget()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.listW = QListWidget()
        self.listW.itemDoubleClicked.connect(self.listDoubleClicked)
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
import requests
import json
import concurrent
from concurrent.futures import ThreadPoolExecutor, wait
import subprocess
from injectBd import injectBD
import sys

class DownloadBDY:
    inited = False
    def __init__(self):
        ibd = injectBD()
        self.tm, self.rand, self.devuid, self.bduss, self.stoken = ibd.Init('百度网盘')
        self.cookie = 'BDUSS=' + self.bduss + ';STOKEN=' + self.stoken 
        self.params = '?devuid='+self.devuid+'&time='+self.tm+'&rand='+self.rand+'&method=locatedownload&app_id=250528&ver=4.0'
        self.Headers = {
            # 'Host':'baidu.com',
            # 'Range': 'bytes=0-',
            'Cookie':self.cookie,
            'User-Agent':'netdisk;2.2.3;pc;pc-mac;10.15.1;macbaiduyunguanjia'
        }
        print('Cookie::', self.cookie)

    def list_files(self,dir='/'):
        host = 'https://pan.baidu.com'
        u = '/api/list' + self.params + '&dir=' + dir
        ret = []
        r = requests.get(host+u,headers=self.Headers)
        file_list = json.loads(r.content)['list']
        for l in file_list:
            d = {'isdir':l['isdir'], 'server_filename': l['server_filename']}
            ret.append(d)
        self.filelist = ret


    def Download_from_path(self,file_name='氯化虫4_x264.mp4'):
        host = 'https://d.pcs.baidu.com'
        u = '/rest/2.0/pcs/file'+self.params+'&path=/'+file_name
        r = requests.get(host+u,headers=self.Headers)
        u = json.loads(r.content)['urls'][0]['url']
        self.Download_from_url(u,file_name)
        
    def Download_from_url(self, u,file_name):
        print('Downloading from url:'+ u)
        cmd = './aria2c "'+u + '" --out "'+file_name+'" --header "User-Agent: netdisk;2.2.3;pc;pc-mac;10.15.1;macbaiduyunguanjia" --header "Cookie: '+self.cookie+'" -s 128 -k 1M --max-connection-per-server=128 --continue=true'
        # p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        # for i in iter(p.stdout.readline,'b'):
        #     if not i:
        #         break
        #     print(i.decode('utf-8'), end='')
        
        # Using pexpect can show progress
        import pexpect
        process = pexpect.spawn(cmd)
        process.interact()

if __name__ == "__main__":
    print('Downloading...')
    # Download_from_path('阳光电影www.ygdy8.com.速度与激情：特别行动.HD.1080p.中英双字幕.mkv')
    # Download_from_url('https://d.pcs.baidu.com/file/f0fc7e66973f129974e5d35e7d560049?fid=2712021640-250528-533246122739205&amp;dstime=1572172464&amp;rt=sh&amp;sign=FDtAERV-DCb740ccc5511e5e8fedcff06b081203-Qfd4wQ4LK3KxgqE4OLNNHTf%2Buwc%3D&amp;expires=8h&amp;chkv=1&amp;chkbd=0&amp;chkpc=&amp;dp-logid=6952602860418330679&amp;dp-callid=0&amp;shareid=2837947211&amp;r=798114631','ps.dmg')
    print('Done!')
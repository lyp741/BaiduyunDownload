import requests
import json
import concurrent
from concurrent.futures import ThreadPoolExecutor, wait
import subprocess
from injectBd import injectBD
import sys
import os
import pickle

class DownloadBDY:
    inited = False
    failed = []
    user_cookie = 'user.pkl'
    def inject(self):
        ibd = injectBD()
        self.tm, self.rand, self.devuid, self.bduss, self.stoken = ibd.Init('百度网盘')
        self.cookie = 'BDUSS=' + self.bduss + ';STOKEN=' + self.stoken 
        self.params = '?devuid='+self.devuid+'&time='+self.tm+'&rand='+self.rand+'&method=locatedownload&app_id=250528&ver=4.0'
        self.Headers = {
            # 'Host':'baidu.com',
            # 'Range': 'bytes=0-',
            'Cookie':self.cookie,
            'User-Agent':'netdisk;2.2.3;pc;pc-mac;10.15.1;macbaiduyunguanjia',
            "Content-Type": "text/plain; charset=utf-8"
        }
        print('Cookie::', self.cookie)
        with open(self.user_cookie,'wb') as f:
            pickle.dump(self,f)

    def __init__(self):
        if os.path.exists(self.user_cookie):
            with open(self.user_cookie,'rb') as f:
                tmp = pickle.load(f)
                self.cookie = tmp.cookie
                self.params = tmp.params
                self.Headers = tmp.Headers
                self.tm = tmp.tm
                self.rand = tmp.rand
                self.devuid = tmp.devuid
                self.bduss = tmp.bduss
                self.stoken = tmp.stoken
        else:
            self.inject()

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

    def get_list_files(self, dir='/'):
        host = 'https://pan.baidu.com'
        u = '/api/list' + self.params + '&dir=' + dir
        ret = []
        r = requests.get(host+u,headers=self.Headers)
        file_list = json.loads(r.content)['list']
        for l in file_list:
            d = {'isdir':l['isdir'], 'server_filename': l['server_filename']}
            ret.append(d)
        return ret

    def Download_from_path(self,file_name='氯化虫4_x264.mp4'):
        host = 'https://d.pcs.baidu.com'
        u = '/rest/2.0/pcs/file'#+self.params+'&path='+file_name
        addr = host+u
        dat = {
            'devuid':self.devuid,
            'time':self.tm,
            'rand':self.rand,
            'path':file_name,
            'method':'locatedownload',
            'app_id':'250528',
            'ver':'4.0'
        }
        r = requests.get(addr,params=dat,headers=self.Headers)
        # print(addr,r.content)
        try:
            u = json.loads(r.content)['urls'][0]['url']
            self.Download_from_url(u,file_name)
        except:
            self.failed.append(file_name)
            print(addr,r.content)
            return -1
        return 0
        
    def Download_from_url(self, u,file_name):
        print('Downloading from url:'+ u)
        # print(os.path.split(os.path.realpath(__file__))[0])
        dir = os.path.dirname(os.path.realpath(sys.argv[0]))
        print(dir)
        # cmd = dir + '/aria2c "'+u + '" --out "'+file_name+'" --header "User-Agent: netdisk;2.2.4;pc;pc-mac;10.14.5;macbaiduyunguanjia","X-Download-From: baiduyun","Cache-Control: no-cache","Pragma: no-cache" --header "Cookie: '+self.cookie+'" --split=8 -k 1M --max-connection-per-server=128 --continue=true '+ ' --dir='+os.path.expanduser('~/Downloads')
        cmd = dir + '/aria2c "'+u + '" --out "'+file_name+'" --header "User-Agent: netdisk;2.2.4;pc;pc-mac;10.14.5;macbaiduyunguanjia","X-Download-From: baiduyun","Cache-Control: no-cache","Pragma: no-cache" --header "Cookie: '+self.cookie+'" --split=8 --max-download-limit=10000000M --continue=true '+ ' --dir='+os.path.expanduser('~/Downloads')

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
    a = DownloadBDY()
    a.cookie = ''
    # a.Download_from_path('/52 数据分析实战45讲【瑞客论坛 www.ruike1.com】/pdf/Do_09 数据采集如何用八爪鱼采集微博上的“D&G”评论.pdf')
    a.Download_from_url('','ps.zip')
    print('Done!')
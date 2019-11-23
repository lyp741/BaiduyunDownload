import requests
import json
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from DownloadBaiduYun import *


u = 'http://ladder.enfi.vip:8084/v3/parse?dvcId=cd6fddb57d76ef5bd224bfd3898a847e'

data = {
    'shareurl': 'https://pan.baidu.com/s/1w-J2EYyL-aHs0WDU9lYkug',
    'sharecode': '3jb8',
    'filelist':'["/The Complete FCPX教程 Video Editing Crash Course.zip"]'
}

data2 = {
    'shareurl': 'https://pan.baidu.com/s/1JYgYTKxAh16eNQzIkpRnWg',
    'sharecode': 'nyau',
    'filelist':'["/q-s1-4.zip"]'

}

headers = {
    'Cookie':'enfi-uid=cd6fddb57d76ef5bd224bfd3898a847e; enfi-token=3de2e03a7cf9c4a651f9a938b78cb846cb3d5d6616e3fb3bfd33fbdeaa17db59'
}

r = requests.post(u,headers=headers,data=data)
res = json.loads(r.text)
rdata = res['data']

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from Crypto import Random
# rdata = 'NiFiqsdbNOmOORAZtZuVBLDYWIq7HSR09FV6O9jHTs/lwUXkTsQGeiIjij+a1wIBgkOZ0K67/GOINCAPmbi4p+1gsUaZC9aDqZI7rWHay8Vde8lyspJa2xau9phVP7oRnJUXY2hg1lFjEmrRb4Tkc4D49wfhRISboyNTYDU8g7OIdVFGphoi2QE5GFxW138T'
# padding算法
BS = AES.block_size # aes数据分组长度为128 bit
pad = lambda s: s + (BS - len(s) % BS) * chr(0)

key = 'zTckeF$U#iMaufRo'
ciphertext = base64.b64decode(rdata)
cryptor = AES.new(key, AES.MODE_CBC, key)
plaintext = cryptor.decrypt(ciphertext)
a = plaintext.decode('utf-8')
pad = ord(a[-1])
a = a[:-pad]
ret = json.loads(a)
urls = ret[0]['urls']
url = urls[0]['url']
fname = ret[0]['path']
# url = 'https://d0.baidupcs.com/file/2a1d7cf031c707ab9002d8d1a3e8ae86?bkt=en-d3a65691252603d3494327a160ccebb6a9adce9f38d940dd5159b4d8e95bc67a950d9c2fefaab02a&xcode=9ffb3ca33f931be6a19a416933d7b7e4c2bb410054d9e84fec4c28343236b4309a9e56fe9bcb6c9f1dd4bee20de11f799717ec4418c70769&fid=2982705443-250528-469698402216836&time=1574243262&sign=FDTAXGERQBHSKfa-DCb740ccc5511e5e8fedcff06b081203-drH%2BDFNO25bgxoj1LPJvAReEzks%3D&to=d0&size=3715757911&sta_dx=3715757911&sta_cs=634&sta_ft=zip&sta_ct=5&sta_mt=0&fm2=MH%2CQingdao%2CAnywhere%2C%2Czhejiang%2Cany&ctime=1558783709&mtime=1574229511&resv0=cdnback&resv1=0&resv2=rlim&resv3=5&resv4=3715757911&vuk=2982705443&iv=2&htype=&randtype=&esl=1&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-c219ec389c10fb213529b666f6d10844a10d7459b29f5dd199af10858e0bd0c03d95e9d17eae996d&expires=8h&rt=pr&r=938319053&mlogid=MjAxOTEwMTYxNzE1NDE1MTgsZjBlOTlmMDhjMGY0ZGQ0N2Y3NjkxYzU2ZDM3OTk3NGUsODczNA%3D%3D&vbdid=-&fin=The+Complete+FCPX%E6%95%99%E7%A8%8B+Video+Editing+Crash+Course.zip&bflag=d0,h5,70,66,75,80,d6,h1,9,5,14,19-d0&err_ver=1.0&check_blue=1&rtype=1&devuid=569f41f328848cc3f34a5c6509c563e7&dp-logid=1647540795823092912&dp-callid=0.1&hps=1&tsl=0&csl=0&csign=t29GOQfiLKGyKocav48XfPGd3Q0%3D&so=0&ut=1&uter=-1&serv=0&uc=723103325&ti=78cccb630bb0656e4e16db9273b32410ee93af4ef16f2878&reqlabel=250528_l_0753a3061760344812aac133bf7469e2&by=themis'
# url = 'https://d0.baidupcs.com/file/2a1d7cf031c707ab9002d8d1a3e8ae86?bkt=en-d3a65691252603d3494327a160ccebb6a9adce9f38d940dd5159b4d8e95bc67a950d9c2fefaab02a&xcode=57db9ad78b6d645fb1b2672785c09269c2bb410054d9e84fec4c28343236b4309a9e56fe9bcb6c9f1dd4bee20de11f799717ec4418c70769&fid=2982705443-250528-469698402216836&time=1574245076&sign=FDTAXGERQBHSKfa-DCb740ccc5511e5e8fedcff06b081203-Yy36z4%2Biqm0vOaoR9m7jGS2tr8I%3D&to=d0&size=3715757911&sta_dx=3715757911&sta_cs=634&sta_ft=zip&sta_ct=5&sta_mt=0&fm2=MH%2CQingdao%2CAnywhere%2C%2Czhejiang%2Cany&ctime=1558783709&mtime=1574229511&resv0=cdnback&resv1=0&resv2=rlim&resv3=5&resv4=3715757911&vuk=2982705443&iv=2&htype=&randtype=&esl=1&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=en-c219ec389c10fb213529b666f6d10844a10d7459b29f5dd199af10858e0bd0c03d95e9d17eae996d&expires=8h&rt=pr&r=116074424&mlogid=MjAxOTEwMTYxNzE1NDE1MTgsZjBlOTlmMDhjMGY0ZGQ0N2Y3NjkxYzU2ZDM3OTk3NGUsODczNA%3D%3D&vbdid=-&fin=The+Complete+FCPX%E6%95%99%E7%A8%8B+Video+Editing+Crash+Course.zip&bflag=d0,h5,66,70,75,80,d6,h1,5,9,14,19-d0&err_ver=1.0&check_blue=1&rtype=1&devuid=569f41f328848cc3f34a5c6509c563e7&dp-logid=1647540795823092912&dp-callid=0.1&hps=1&tsl=0&csl=0&csign=t29GOQfiLKGyKocav48XfPGd3Q0%3D&so=0&ut=1&uter=-1&serv=0&uc=723103325&ti=b2375bf93e10fe6937ed612da28f2f95ad7393f2253d60ff&reqlabel=250528_l_0753a3061760344812aac133bf7469e2&by=themis'
if __name__ == "__main__":
    print('Downloading...')
    a = DownloadBDY()
    # a.cookie = ''
    # a.Download_from_path('/52 数据分析实战45讲【瑞客论坛 www.ruike1.com】/pdf/Do_09 数据采集如何用八爪鱼采集微博上的“D&G”评论.pdf')
    a.Download_from_url(url,'fname')
    print('Done!')
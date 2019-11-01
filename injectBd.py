import frida
import sys
import codecs
import time
import subprocess

class injectBD:
    ts = ''
    rand = ''
    devuid = ''
    bd = None
    inited = False
    

    def Init(self,target_process):
        subprocess.call(['open','-a','BaiduNetdisk_mac'])
        time.sleep(1)
        while self.inited != True:
            try:
                session = frida.attach(target_process)
            
                # if session != None:
                #     break
        
                # with codecs.open('injectBd.js', 'r', 'utf-8') as f:
                #     source = f.read()
            
                script = session.create_script('''var resolver = new ApiResolver('objc');
                    var matches = resolver.enumerateMatches('*[* userSignWithTimeStamp*]');
                    var first = matches[0];

                    Interceptor.attach(first.address,{
                        onEnter: function(args) {
                            var chatMsg = args[2].readByteArray(64);
                            send('ts',chatMsg);
                        },
                        onLeave: function(retval) {
                            
                            var chatMsg = retval.readByteArray(64);
                            send('rand',chatMsg);
                        },
                    });
                    
                        var matches = resolver.enumerateMatches('*[* secDeviceUUID*]');
                    var first = matches[0];

                    Interceptor.attach(first.address,{
                        onEnter: function(args) {
                            
                        },
                        onLeave: function(retval) {
                            
                            var chatMsg = retval.readByteArray(64);
                            send('devuid',chatMsg);
                        },
                    });

                    var matches = resolver.enumerateMatches('*[BDUser bduss*]');
                    var first = matches[0];

                    Interceptor.attach(first.address,{
                        onEnter: function(args) {
                            
                        },
                        onLeave: function(retval) {
                            var chatMsg = retval.readByteArray(256);
                            
                            send('bduss',chatMsg);
                        },
                    });
                    var matches = resolver.enumerateMatches('*[BDUser stoken*]');
                    var first = matches[0];

                    Interceptor.attach(first.address,{
                        onEnter: function(args) {
                        },
                        onLeave: function(retval) {
                            var chatMsg = retval.readByteArray(128);
                            
                            send('stoken',chatMsg);
                        },
                    });
                    ''')
            
                    
                def on_message(message, data):
                    if self.inited == True:
                        return
                    if message['payload'] == 'ts':
                        self.ts = str(data[17:27], encoding = "utf8")
                    elif message['payload'] == 'rand':
                        self.rand = str(data[17:57], encoding = "utf8")
                    elif message['payload'] == 'devuid':
                        self.devuid = str(data[17:49], encoding = "utf8")
                    elif message['payload'] == 'bduss':
                        self.bduss = str(data[17:209], encoding = "utf8")
                    elif message['payload'] == 'stoken':
                        self.stoken = str(data[17:81], encoding = "utf8")   
                
                script.on("message", on_message)
                script.load()
                print("[!] Please open Baidu Net Disk!!\n")
                if self.ts and self.rand and self.devuid and self.bduss and self.stoken:
                    self.inited = True
            except:
                print("Cant't find BaiduYun")
                session = None
                time.sleep(2)
        session.detach()
        print('[!] Get infomation successed!!')
        subprocess.call(['killall','BaiduNetdisk_mac'])
        return self.ts, self.rand, self.devuid, self.bduss, self.stoken
    
if __name__ == "__main__":
    pass
    # main('百度网盘')
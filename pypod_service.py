#!/usr/bin/env python
#-*- coding:utf-8 -*-

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import requests
import ssl

import httplib, urllib
import socket
import time
import sys,os,ConfigParser
import win32serviceutil 
import win32service 
import win32event 
import gc

import urllib3
# 关SSL连接警告
urllib3.disable_warnings()

g_logname = "dnspod.log"

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1_2)

class pydnspod:
    _login_token = ""
    _domain_id = ""
    _record_id = ""
    _sub_domain = ""
    _modname = "pydnspod"
    _account = "dnspod"
    _user_agent = "ELSESKY DDNS DNSPOD CLIENT/V1.0.20180904/(elsesky@elsesky.bid)"
    current_ip = ""
    # 连接超时时间
    connect_timeout = 10
    # 读取数据超时时间
    read_timeout = 10
    # 默认重试次数
    connect_retry_times = 3


    params = {
            "login_token": None, 
            "format": "json", 
            "domain_id": None,
            "record_id": None,
            "sub_domain": None,
            "record_line": "默认"
            }
    
    def __init__(self,login_token,domain_id,record_id,sub_domain):
        self._login_token = login_token
        self._domain_id = domain_id
        self._record_id = record_id
        self._sub_domain = sub_domain
        self.set_params()

    def set_params(self):
        self.params = {
            "login_token": self._login_token, 
            "format": "json", 
            "domain_id": self._domain_id,
            "record_id": self._record_id,
            "sub_domain": self._sub_domain,
            "record_line": "默认"
            }

    # 通用POST方法
    def post_url_content(self,url,headers,params):
        try:
            s = requests.Session()
            s.mount('https://', MyAdapter(max_retries = self.connect_retry_times))
            response = s.post(
                url, 
                data = params , 
                headers = headers , 
                verify=False , 
                timeout=(
                    self.connect_timeout , 
                    self.read_timeout , 
                )
            )
            return response.text
        except Exception, e:
            do_log(self._modname,self._account,"---------" + str(e) + "  @post_url_content-------------" )
            return ""
            pass

    #从服务端获取设置的IP
    def get_current_ip_from_dnspot(self):
        try:
            
            headers = {'User-Agent': self._user_agent,"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
            url = 'https://dnsapi.cn/Record.Info'
            response = self.post_url_content(url,headers,self.params)
            t_ip = response.split('value":"')[1].split('",')[0]
            do_log(self._modname,self._account,"The IP on server is: " +  t_ip , self._modname + ".log")
            self.current_ip = t_ip
            do_log(self._modname,self._account,"Force set ini old ip to server ip: " +  t_ip , self._modname + ".log")
            self.set_current_ip_to_ini(t_ip)
        except Exception, e:
            do_log(self._modname,self._account,"Got IP on server error!,use ini file." , self._modname + ".log")
            do_log(self._modname,self._account,"---------" + str(e) + "  @get_current_ip_from_dnspot-------------", self._modname + ".log")
            self.current_ip = self.get_current_ip_from_ini()
            pass

    #从INI文件获取设置的IP
    def get_current_ip_from_ini(self):
        ospath = cur_file_dir()
        ip_ini_path = ini_path = ospath + "/site.ini"
        c_ip = ConfigParser.ConfigParser()
        try:
            c_ip.readfp(open(ip_ini_path))
            current_ini_ip = c_ip.get("site",self._sub_domain)
            self.current_ip = current_ini_ip
            do_log(self._modname,self._account,"Current ini ip is:"  + current_ini_ip, self._modname + ".log")
        except Exception, e:
            do_log(self._modname,self._account,"Got IP on ini error!,IP is set to 0." , self._modname + ".log")
            self.current_ip = "0"
            pass
    
    #设置INI文件中的IP
    def set_current_ip_to_ini(self,ip):
        ospath = cur_file_dir()
        ip_ini_path = ini_path = ospath + "/site.ini"
        c_ip = ConfigParser.ConfigParser()
        try:
            c_ip.read(ip_ini_path)
            c_ip.set("site",self._sub_domain,ip)
            c_ip.write(open(ip_ini_path, "r+"))
        except Exception, e:
            print "ERROR @ set_current_ip_to_ini"
            print e
            pass


    #调用API接口设置IP
    def ddns(self,ip):
        # 添加DNS解析记录
        self.params.update(dict(value=ip))
        url = 'https://dnsapi.cn/Record.Ddns'
        headers = {'User-Agent': self._user_agent,"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
        try:

            response = self.post_url_content(url,headers,self.params)
            # do_log(self._modname,self._account,str(response.status) + response.reason )
            data = response
            do_log(self._modname,self._account,data)
            return True
        except Exception, e:
            do_log(self._modname,self._account,"---------Setting ddns ip failed  @ddns-------------", self._modname + ".log")
            do_log(self._modname,self._account,"---------" + str(e) + "  @ddns-------------" , self._modname + ".log")
            delay_sec = 600
            return False
            pass


        

    #获取外网IP
    def getip(self,current_ip):
        try:
            # DNSPOD这个接口有问题
            # sock = socket.create_connection(('ns1.dnspod.net', 6666))
            # sock = socket.create_connection(('http://ipinfo.io/ip', 6666))
            # sock.settimeout(30)
            # ip = sock.recv(16)
            # sock.close()
            # 换requests接口从另外的外网IP接口获取IP
            s = requests.Session()
            headers = {'User-Agent': "IE","Content-type": "application/x-www-form-urlencoded"}
            # 备用URL
            # url = 'http://ipinfo.io/ip'
            url = 'http://members.3322.org/dyndns/getip'

            r = s.get(url,headers=headers,timeout=300)
            ip = r.text.split("\n")[0]
            do_log(self._modname,self._account,"Got outter IP is: " + ip )
        except Exception, e:
            do_log(self._modname,self._account,"Get outter IP failed, use ini ip instead!" )
            do_log(self._modname,self._account,"---------" + str(e) + "  @getip-------------" )
            ip = current_ip
            print e
            pass
        return ip


    #整体IP设置流程
    def open(self):
        do_log(self._modname,self._account, "----------------" + self._sub_domain + "-----begin-------" )
        try:
            #从服务器端读取老IP到类全局变量
            try:
                self.get_current_ip_from_dnspot()
            except Exception, e:
                do_log(self._modname,self._account,"---------" + str(e) + " function get_current_ip_from_dnspot @open-------------" )
                pass
            time.sleep(1)
            try:
                ip = self.getip(self.current_ip)
            except Exception, e:
                do_log(self._modname,self._account,"---------" + str(e) + " function getip @open-------------" )
                ip = self.current_ip
                pass  
            do_log(self._modname,self._account,"Current outter IP is: " +  ip )
            time.sleep(1)
            # 当服务端IP与本地出网IP不一致，且本地IP以及服务端IP不为空时，更新服务端IP
            if (self.current_ip != ip) and (ip) and (self.current_ip):
                t_result = False
                try:
                    t_result = self.ddns(ip)
                except Exception, e:
                    do_log(self._modname,self._account,"---------" + str(e) + " function ddns @open-------------" )
                    pass
                if t_result:
                    do_log(self._modname,self._account,"Got new IP,old IP is: " +  self.current_ip + " ,and new IP is: " + ip )
                    #写配置文件记录
                    self.current_ip = ip
                    self.set_current_ip_to_ini(ip)
            else:
                do_log(self._modname,self._account,"IP no change.Old ip is: " + self.current_ip)
            do_log(self._modname,self._account,"----------------" + self._sub_domain + "-----Done-------" )
        except Exception, e:
            print e
            do_log(self._modname,self._account,"---------" + str(e) + "  @open-------------" )
            do_log(self._modname,self._account,"----------------" + self._sub_domain + "-----Error-------" )
            pass
    

def do_log(modname,account,log_detail,logname = g_logname):
    logname = g_logname
    print modname + '|' + account + ':' + log_detail
    ospath = cur_file_dir()
    fp = open(ospath + '/' + logname,"a")
    ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    fp.write(ctime + "|"  + modname + '|' + account + ':' +log_detail + "\n")
    fp.close()


def cur_file_dir():
    #获取脚本路径
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，
    #如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


#类名务必和服务名以及文件名保持一致，否则执行会失败
class pypod_service(win32serviceutil.ServiceFramework): 
    _svc_name_ = "pypod_service" 
    _svc_display_name_ = "pypod_service" 
    _svc_description_ = "pypod_service" 
    _modname = "pypod_service"
    _account = "dnspod"
    run = True
    
    def __init__(self, args): 
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
    
    def SvcDoRun(self): 
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        do_log(self._modname,self._account,"----------Service start!-------------" )
        ospath = cur_file_dir()
        # 设置requests的ca根证书
        ca_path = ospath + "/cacert.pem"
        requests.utils.DEFAULT_CA_BUNDLE_PATH = ca_path
        # 读取INI配置
        config = ConfigParser.ConfigParser()
        ini_path = ospath + "/user.ini"
        #设置默认延时
        delay_sec = 600
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        while True:
            #取延时
            try:
                config.read(ini_path)
                delay_sec = int(config.get("delay_in_s","delay_in_s"))
                #当设定小于5分钟，强制设为5分钟
                if delay_sec < 300:
                    delay_sec = 300
                #当设定大于2小时，前置设为2小时
                elif delay_sec > 7200:
                    delay_sec = 7200
            except Exception, e:
                print e
                do_log(self._modname,self._account,"----------Got delay seconds error , set to 10 min-------------" )
                delay_sec = 600
                pass
            try:
                do_log(self._modname,self._account,"---------delay seconds is " + str(delay_sec) + "-------------" )
                login_token = config.options("login_token")
                domain_id = config.options("domain_id")
                record_id = config.options("record_id")
                sub_domain = config.options("sub_domain")
                login_dnspods={}
                for i in range(0,len(login_token)):
                    time.sleep(5)
                    login_dnspods[i] = pydnspod(
                                        urllib.unquote(\
                                        config.get("login_token",login_token[i])),\
                                        config.get("domain_id",domain_id[i]),\
                                        config.get("record_id",record_id[i]),\
                                        config.get("sub_domain",sub_domain[i]),\
                                        )
                    print "----------------" + str(config.get("sub_domain",sub_domain[i])) + "--------------------"
                    try:
                        login_dnspods[i].open()
                        # 增加延迟，避免多个域名更新的时候弹出请求过多被拒绝的情况
                        # 默认延迟1分钟
                        time.sleep(60)
                    except Exception, e:
                        do_log(self._modname,self._account,"----------" + str(e) + " ERROR@ function open in SvcDoRun-------------" )
                        pass
                    print "-------------------------------------------"
                del login_dnspods
                del login_token
                del domain_id
                del record_id
                del sub_domain
                gc.collect()
            except Exception, e:
                print e
                do_log(self._modname,self._account,"---------" + str(e) + "  @SvcDoRun-------------" )
                delay_sec = 600
                pass
            time.sleep(delay_sec) 
            do_log(self._modname,self._account,"---------Self killed @SvcDoRun-------------" )
            #定期杀进程，避免获取到奇怪的外网IP的情况
            os.system('TASKKILL /F /IM pypod_service.exe')
            




    def SvcStop(self): 
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        do_log(self._modname,self._account,"----------Service stop!-------------" )
        #避免停不掉，直接杀进程
        os.system('TASKKILL /F /IM pypod_service.exe')

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(pypod_service)

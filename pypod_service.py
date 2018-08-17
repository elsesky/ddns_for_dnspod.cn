#!/usr/bin/env python
#-*- coding:utf-8 -*-


import httplib, urllib
import socket
import time
import sys,os,ConfigParser
import win32serviceutil 
import win32service 
import win32event 

g_logname = "dnspod.log"

class pydnspod:
    _login_token = ""
    _domain_id = ""
    _record_id = ""
    _sub_domain = ""
    _modname = "pydnspod"
    _account = "dnspod"
    current_ip = ""
    params = dict(
        login_token=None,
        format="json",
        domain_id=None, # replace with your domain_od, can get it by API Domain.List
        record_id=None, # replace with your record_id, can get it by API Record.List
        sub_domain=None, # replace with your sub_domain
        record_line="默认",
    )
    
    def __init__(self,login_token,domain_id,record_id,sub_domain):
        self._login_token = login_token
        self._domain_id = domain_id
        self._record_id = record_id
        self._sub_domain = sub_domain
        self.set_params()
        
    def set_params(self):
        self.params = dict(
            login_token=self._login_token,
            format="json",
            domain_id=self._domain_id,
            record_id=self._record_id, 
            sub_domain=self._sub_domain, 
            record_line="默认",
        )

    #从服务端获取设置的IP
    def get_current_ip_from_dnspot(self):
        try:
            headers = {'User-Agent': 'ELSESKY DDNS DNSPOD CLIENT/V1.0.20180817',"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
            conn = httplib.HTTPSConnection("dnsapi.cn")
            conn.request("POST", "/Record.Info", urllib.urlencode(self.params), headers)
            response = conn.getresponse().read()
            t_ip = response.split('value":"')[1].split('",')[0]
            do_log(self._modname,self._account,"The IP on server is: " +  t_ip , self._modname + ".log")
            self.current_ip = t_ip
            do_log(self._modname,self._account,"Force set ini old ip to server ip: " +  t_ip , self._modname + ".log")
            self.set_current_ip_from_ini(t_ip)
        except Exception, e:
            do_log(self._modname,self._account,"Got IP on server error!,use ini file." , self._modname + ".log")
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
            print "Current ini ip is: " + current_ini_ip
            self.current_ip = current_ini_ip
        except Exception, e:
            do_log(self._modname,self._account,"Got IP on ini error!,IP is set to 0." , self._modname + ".log")
            self.current_ip = "0"
            pass
    
    #设置INI文件中的IP
    def set_current_ip_from_ini(self,ip):
        ospath = cur_file_dir()
        ip_ini_path = ini_path = ospath + "/site.ini"
        c_ip = ConfigParser.ConfigParser()
        try:
            c_ip.read(ip_ini_path)
            c_ip.set("site",self._sub_domain,ip)
            c_ip.write(open(ip_ini_path, "r+"))
        except Exception, e:
            print "ERROR @ set_current_ip_from_ini"
            print e
            pass


    #调用API接口设置IP
    def ddns(self,ip):
        self.params.update(dict(value=ip))
        headers = {'User-Agent': 'ELSESKY DDNS DNSPOD CLIENT/V1.0.20180817',"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
        conn = httplib.HTTPSConnection("dnsapi.cn")
        conn.request("POST", "/Record.Ddns", urllib.urlencode(self.params), headers)
        
        response = conn.getresponse()
        do_log(self._modname,self._account,str(response.status) + response.reason )
        # print response.status, response.reason
        data = response.read()
        # print data
        do_log(self._modname,self._account,data)
        conn.close()
        return response.status == 200

    #获取外网IP
    def getip(self,current_ip):
        sock = socket.create_connection(('ns1.dnspod.net', 6666))
        sock.settimeout(10)
        try:
            ip = sock.recv(16)
        except Exception, e:
            ip = current_ip
            print e
        sock.close()
        return ip


    #整体IP设置流程
    def open(self):
        do_log(self._modname,self._account, "----------------" + self._sub_domain + "-----begin-------" )
        try:
            #从服务器端读取老IP到类全局变量
            self.get_current_ip_from_dnspot()
            ip = self.getip(self.current_ip)
            print "CURRENT IP:",ip
            if self.current_ip != ip:
                if self.ddns(ip):
                    do_log(self._modname,self._account,"Got new IP,old IP is: " +  self.current_ip + " ,and new IP is: " + ip )
                    #写配置文件记录
                    self.current_ip = ip
                    self.set_current_ip_from_ini(ip)
            else:
                do_log(self._modname,self._account,"IP no change.Old ip is: " + self.current_ip)
            do_log(self._modname,self._account,"----------------" + self._sub_domain + "-----Done-------" )
        except Exception, e:
            print e
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
            do_log(self._modname,self._account,"---------delay seconds is " + str(delay_sec) + "-------------" )
            login_token = config.options("login_token")
            domain_id = config.options("domain_id")
            record_id = config.options("record_id")
            sub_domain = config.options("sub_domain")
            login_dnspods={}
            for i in range(0,len(login_token)):
            #for i in range(2,3):
                time.sleep(5)
                login_dnspods[i] = pydnspod(
                                    urllib.unquote(\
                                    config.get("login_token",login_token[i])),\
                                    config.get("domain_id",domain_id[i]),\
                                    config.get("record_id",record_id[i]),\
                                    config.get("sub_domain",sub_domain[i]),\
                                    )
                print "----------------" + str(config.get("sub_domain",sub_domain[i])) + "--------------------"
                login_dnspods[i].open()
                print "-------------------------------------------"
            time.sleep(delay_sec) 


    def SvcStop(self): 
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        do_log(self._modname,self._account,"----------Service stop!-------------" )
        #避免停不掉，直接杀进程
        os.system('TASKKILL /F /IM pypod_service.exe')

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(pypod_service)
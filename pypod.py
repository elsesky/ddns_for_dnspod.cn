#!/usr/bin/env python
#-*- coding:utf-8 -*-

FZ = """ 
                            _ooOoo_  
                           o8888888o  
                           88" . "88  
                           (| -_- |)  
                           O\  =  /O  
                        ____/`---'\____  
                      .'  \\|     |//  `.  
                     /  \\|||  :  |||//  \  
                    /  _||||| -:- |||||-  \  
                    |   | \\\  -  /// |   |  
                    | \_|  ''\---/''  |   |  
                    \  .-\__  `-`  ___/-. /  
                  ___`. .'  /--.--\  `. . __  
               ."" '<  `.___\_<|>_/___.'  >'"".  
              | | :  `- \`.;`\ _ /`;.`/ - ` : | |  
              \  \ `-.   \_ __\ /__ _/   .-` /  /  
         ======`-.____`-.___\_____/___.-`____.-'======  
                            `=---='  
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
                      佛祖保佑       永无BUG 
""" 
print FZ.decode("UTF-8").encode("GB18030")

import httplib, urllib
import socket
import time
import sys,os,ConfigParser
import json

g_logname = "dnspod.log"

class pydnspod:
    _login_token = ""
    _domain_id = ""
    _record_id = ""
    _sub_domain = ""
    _modname = "dnspod"
    _account = "elsesky"
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

    def get_current_ip_from_dnspot(self):
        try:
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
            conn = httplib.HTTPSConnection("dnsapi.cn")
            conn.request("POST", "/Record.Info", urllib.urlencode(self.params), headers)
            response = conn.getresponse().read()
            t_ip = response.split('value":"')[1].split('",')[0]
            do_log(self._modname,self._account,"The IP on server is: " +  t_ip)
            self.current_ip = t_ip
            self.set_current_ip_from_ini(t_ip)

        except Exception, e:
            self.current_ip = "0"
            pass

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
            self.current_ip = "0"
            pass

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
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
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

    #获取IP
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
            #从配置文件读取老IP到类全局变量
            self.get_current_ip_from_dnspot()
            # self.get_current_ip_from_ini()
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


if __name__ == '__main__':
    ospath = cur_file_dir()
    config = ConfigParser.ConfigParser()
    ini_path = ospath + "/user.ini"
    config.read(ini_path)
    login_token = config.options("login_token")
    domain_id = config.options("domain_id")
    record_id = config.options("record_id")
    sub_domain = config.options("sub_domain")
    while True:
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
        time.sleep(30)
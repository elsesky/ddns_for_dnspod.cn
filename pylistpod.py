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
import requests,requests.utils, pickle

g_logname = "dnspod.log"
g_txtname = "domainlist.txt"

class pylistdnspod:
    _login_token = ""
    _domain_id = ""
    _record_id = ""
    _sub_domain = ""
    _modname = "pylistdnspod"
    _account = "dnspod"
    _pre_site_url = "https://dnsapi.cn/"
    _headers = {}
    current_ip = ""

    
    def __init__(self,login_token):
        self._login_token = login_token
    

    #整体IP设置流程
    def open(self):
        ospath = cur_file_dir()
        #删除文件
        try:
            os.remove(ospath + '/' + g_txtname)
            
        except Exception,e:
            do_log(self._modname ,self._account ,'Can not delete domainlist file! Skip delete.',g_logname)
            pass
        # s = requests.Session()
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)',\
            'Accept-Encoding': 'text/json',\
            'Content-type': 'application/x-www-form-urlencoded',\
        }
        try:
            post_data = dict(
                login_token=self._login_token,
                format="json",
            )

            conn = httplib.HTTPSConnection("dnsapi.cn")
            conn.request("POST", "/Domain.List", urllib.urlencode(post_data), self._headers)
            list_domain = json.loads(conn.getresponse().read())
            #获取域名数量
            try:
                domain_num = int(list_domain["info"]["domain_total"])
            except Exception,e:
                domain_num = 0
                pass
            #基于域名获取域名ID
            for i in range(0,domain_num):
                do_log(
                    self._modname ,self._account , \
                    '----------------Domain name: ' + list_domain["domains"][i]["name"] + " |and id: " + str(list_domain["domains"][i]["id"]) + "--------------", \
                    g_txtname
                )
                #获取记录名清单
                c_domain_id = str(list_domain["domains"][i]["id"])
                r_list_data = dict(
                    login_token=self._login_token,
                    domain_id=c_domain_id,
                    format="json",
                )
                conn.request("POST", "/Record.List", urllib.urlencode(r_list_data), self._headers)
                #取该域名下的记录数，如果失败，直接置零
                try :
                    list_r = json.loads(conn.getresponse().read())
                    r_num = int(list_r["info"]["records_num"])
                except Exception,e:
                    r_num = 0
                    pass
                for j in range(0,r_num):
                    do_log(
                        self._modname ,self._account , \
                        '----------------Recode name: ' + list_r["records"][j]["name"] + " |id: " + str(list_r["records"][j]["id"]) + "  |type :" + list_r["records"][j]["type"], \
                        g_txtname
                    )
                do_log(
                    self._modname ,self._account , \
                    '----------------End of domain:' + list_domain["domains"][i]["name"] + "-------------------------------" , \
                    g_txtname
                )
        except Exception,e:
            print e
            do_log(self._modname ,self._account ,'Unknown ERR!',g_logname)
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
    login_dnspods={}
    for i in range(0,len(login_token)):
        time.sleep(3)
        login_dnspods[i] = pylistdnspod(
                            urllib.unquote(\
                            config.get("login_token",login_token[i])),\
                            )
        login_dnspods[i].open()
    os.system('notepad ' + ospath + "/" + g_txtname)
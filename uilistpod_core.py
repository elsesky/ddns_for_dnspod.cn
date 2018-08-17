#! /usr/bin/python
# -*- coding: utf-8 -*-

import win32clipboard as w
import time,os,MySQLdb,win32con,webbrowser,sys
from time import sleep
import httplib, urllib
import socket
import time
import sys,os,ConfigParser
import json
import requests,requests.utils, pickle

g_logname = "dnspod.log"
g_txtname = "domainlist.txt"


from PyQt4.QtCore import *
from PyQt4.QtGui import *
from uilistpod.Core import *
from uilistpod.uilistpod import *
from __builtin__ import file
from win32com.server import exception

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class uilistpod_core():
    _login_token = "63805,5637da6240113f2cff536e6962875937"
    _domain_id = ""
    _record_id = ""
    _sub_domain = ""
    _modname = "pylistdnspod"
    _account = "dnspod"
    _pre_site_url = "https://dnsapi.cn/"
    _headers = {}
    current_ip = ""
    ini_recode_id_list = []
    #初始化
    def __init__(self, window):
        #传入上层窗口
        self.window = window

        
#############################事件关联处理函数#############################
    #点击获取记录清单按钮
    def  pushButton_getrecode_click(self,current=0):
        self.get_recode_list()
        return 0

    #点击生成INI配置文件按钮
    def  pushButton_makeini_click(self,current=0):
        QMessageBox.information(self.window, _fromUtf8("Done"),  _fromUtf8("该操作将直接覆盖原有配置文件。\n点确认/OK前，请确保您已备份原有配置文件(user.ini)"), buttons=QMessageBox.Ok)
        self.make_ini()
        QMessageBox.information(self.window, _fromUtf8("Done"),  _fromUtf8("配置文件生成完毕"), buttons=QMessageBox.Ok)
        return 0

    #点击安装服务并启动
    def pushButton_install_and_start_service_click(self,current=0):
        QMessageBox.information(self.window, _fromUtf8("Done"),  _fromUtf8("请确保您有管理员权限，\n且配置文件无误！"), buttons=QMessageBox.Ok)
        try:
            os.system('sc create _dnspod_ddns_service start= delayed-auto binPath= %cd%\pypod_service.exe')
            os.system('net start _dnspod_ddns_service')
        except Exception,e:
            print e
            pass
        QMessageBox.information(self.window, _fromUtf8("Done"),  _fromUtf8("命令执行完毕"), buttons=QMessageBox.Ok)
        return 0

    #点击卸载服务并停止
    def pushButton_stop_and_del_service_click(self,current=0):
        QMessageBox.information(self.window, _fromUtf8("Done"),  _fromUtf8("请确保您有管理员权限！"), buttons=QMessageBox.Ok)
        try:
            os.system('net stop _dnspod_ddns_service')
            os.system('sc delete _dnspod_ddns_service')
            os.system('taskkill /im pypod_service.exe -f')
        except Exception,e:
            print e
            pass
        QMessageBox.information(self.window, _fromUtf8("Done"),  _fromUtf8("命令执行完毕"), buttons=QMessageBox.Ok)
        return 0




#############################通用函数#############################
    #从INI文件获取记录ID
    def get_recode_list_from_ini(self):
        ospath = cur_file_dir()
        try:
            config = ConfigParser.ConfigParser()
            ini_path = ospath + "/user.ini"
            config.read(ini_path)
            record_id = config.options("record_id")
            self.ini_recode_id_list = []
            for i in range(0,len(record_id)):
                self.ini_recode_id_list.append(config.get("record_id",record_id[i]))
        except Exception,e:
            print e
            do_log(
                    self._modname ,self._account , \
                    '----------------Get recode id list from ini error!-------------------------------' , \
                    g_logname
            )
            self.ini_recode_id_list = []
            pass
        return self.ini_recode_id_list

    #从dnspod获取记录清单，并高亮显示已配置的
    def get_recode_list(self):
        ospath = cur_file_dir()
        #删除文件
        self._headers = {
            'User-Agent': 'ELSESKY DDNS DNSPOD CLIENT/V1.0.20180817',\
            'Accept-Encoding': 'text/json',\
            'Content-type': 'application/x-www-form-urlencoded',\
        }
        self.window.record_list.setRowCount(0)
        self.window.record_list.clearContents()
        try:
            conn = httplib.HTTPSConnection("dnsapi.cn")
            #获取用户输入的TOKEN,检测token合法性
            c_token = self.qstr_2_pystr(self.window.txt_podtoken.text()).strip()
            if not self.token_check(c_token):
                QMessageBox.critical(self.window, _fromUtf8("Token error!"),  _fromUtf8("Token非法，请检查输入"), buttons=QMessageBox.Ok)
                return
            self._login_token = c_token
            check_data = dict(
                login_token=self._login_token,
                format="json",
            )
            conn.request("POST", "/User.Detail", urllib.urlencode(check_data), self._headers)
            login_status = json.loads(conn.getresponse().read())["status"]['code']
            if login_status != "1":
                QMessageBox.critical(self.window, _fromUtf8("Done"),  _fromUtf8("Token 无效，错误代码：" + str(login_status)), buttons=QMessageBox.Ok)
                return
            #获取域名下的ID清单
            post_data = dict(
                login_token=self._login_token,
                format="json",
            )
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
                    g_logname
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
                    self.add_recode( \
                        list_domain["domains"][i]["name"], \
                        str(list_domain["domains"][i]["id"]), \
                        list_r["records"][j]["name"], \
                        str(list_r["records"][j]["id"]), \
                        list_r["records"][j]["type"], \
                        self._login_token, \
                    )
                do_log(
                    self._modname ,self._account , \
                    '----------------End of domain:' + list_domain["domains"][i]["name"] + "-------------------------------" , \
                    g_logname
                )
            #通过INI的记录ID，自动完成选择
            ini_r_list = self.get_recode_list_from_ini()
            for ii in range(0,len(ini_r_list)):
                for jj in range(0,self.window.record_list.rowCount()):
                    if ini_r_list[ii] == self.window.record_list.item(jj,3).text():
                        self.window.record_list.selectRow(jj)

        except Exception,e:
            print e
            do_log(self._modname ,self._account ,'Unknown ERR!',g_logname)
            pass
        QMessageBox.information(self.window, _fromUtf8("Done"),  _fromUtf8("获取完毕。\n配置文件中设置的已高亮显示。"), buttons=QMessageBox.Ok)

    #TOKEN合法性检查
    def token_check(self,c_token):
        if len(c_token) < 36 or len(c_token) > 40:
            return False
        elif (c_token.find(",") == -1):
            return False
        else:
            return True

    #生成INI文件
    def make_ini(self):
        ospath = cur_file_dir()
        try:
            config = ConfigParser.ConfigParser()
            ini_path = ospath + "/user.ini"
            #读取间隔时间，如果读取失败，间隔直接设置成300秒
            config.readfp(open(ini_path))
            current_ini_delay = config.get("delay_in_s","delay_in_s")
        except Exception,e:
            print e
            do_log(
                    self._modname ,self._account , \
                    '----------------Error @ make_ini-------------------------------' , \
                    g_logname
            )
            current_ini_delay = 600
            pass
        #获取选中行的信息
        index_list = []
        domain_ids = []
        record_ids = []
        sub_domains = []
        login_tokens = []
        
        index_num = 0
        items = self.window.record_list.selectedIndexes()    #每行每个单元的
        for i in items:
            #如果不同行，加入数组中
            if i.row() not in index_list:
                index_list.append(i.row())
                #生成对应数组
                domain_ids.append(self.window.record_list.item(i.row(), 1).text())
                sub_domains.append(self.window.record_list.item(i.row(), 2).text())
                record_ids.append(self.window.record_list.item(i.row(), 3).text())
                login_tokens.append(self.window.record_list.item(i.row(), 5).text())


        #生成配置文件内容
        config_w = ConfigParser.ConfigParser()
        config_w.add_section('delay_in_s')
        config_w.add_section('login_token')
        config_w.add_section('domain_id')
        config_w.add_section('record_id')
        config_w.add_section('sub_domain')
        config_w.set('delay_in_s', 'delay_in_s', str(current_ini_delay))
        for i in range(0,len(domain_ids)):
            #根据之前的数组设置INI内容
            config_w.set('login_token', 'login_token' + str(i), login_tokens[i])
            config_w.set('domain_id', 'domain_id' + str(i), domain_ids[i])
            config_w.set('record_id', 'record_id' + str(i), record_ids[i])
            config_w.set('sub_domain', 'sub_domain' + str(i), sub_domains[i])

        #根据选择内容生成清单
        with open(ospath + '/user.ini', 'w') as configfile:
            config_w.write(configfile)
        return 0


        
    
#################################辅助函数#################################
    #在记录清单中添加一行
    def  add_recode(self,domain_name,domain_id,recode_name,recode_id,recode_type,token):
        q_domain_name = QTableWidgetItem(_fromUtf8(domain_name))
        q_domain_id = QTableWidgetItem(_fromUtf8(domain_id))
        q_recode_name = QTableWidgetItem(_fromUtf8(recode_name))
        q_recode_id = QTableWidgetItem(_fromUtf8(recode_id))
        q_recode_type = QTableWidgetItem(_fromUtf8(recode_type))
        q_token = QTableWidgetItem(_fromUtf8(token))
        last_row = self.window.record_list.rowCount()
        self.window.record_list.insertRow(last_row)
        self.window.record_list.setItem(last_row, 0, q_domain_name)
        self.window.record_list.setItem(last_row, 1, q_domain_id)
        self.window.record_list.setItem(last_row, 2, q_recode_name)
        self.window.record_list.setItem(last_row, 3, q_recode_id)
        self.window.record_list.setItem(last_row, 4, q_recode_type)
        self.window.record_list.setItem(last_row, 5, q_token)
        #由于可能显示不全，添加提示
        self.window.record_list.item(last_row, 0).setToolTip(_fromUtf8(domain_name))
        self.window.record_list.item(last_row, 2).setToolTip(_fromUtf8(recode_name))
        self.window.record_list.item(last_row, 5).setToolTip(_fromUtf8(token))
        self.window.record_list.resizeColumnsToContents()
        #每次刷新重新定义列宽
        self.window.record_list.setColumnWidth(0,100)
        self.window.record_list.setColumnWidth(1,80)
        self.window.record_list.setColumnWidth(2,100)
        self.window.record_list.setColumnWidth(3,80)
        self.window.record_list.setColumnWidth(4,60)
        
        
    #qstring转标准str
    def qstr_2_pystr(self, qStr):
    # # QString，如果内容是中文，则直接使用会有问题，要转换成 python string
        return unicode(qStr.toUtf8(), 'utf-8', 'ignore')



        
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

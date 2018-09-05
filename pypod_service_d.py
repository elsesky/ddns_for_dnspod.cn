#!/usr/bin/env python
#-*- coding:utf-8 -*-


import httplib, urllib
import socket
import time
import sys,os,ConfigParser
import win32serviceutil 
import win32service 
import win32event 

g_logname = "dnspod_d.log"




class pydnspod_d:
    _service_exe_name = "pypod_service.exe"
    _dnspod_ddns_service = "_dnspod_ddns_service"
    _modname = "pypod_service_d"
    _account = "dnspod"

    def __init__(self):
        cmd = 'tasklist /fi "imagename eq ' + self._service_exe_name + '"' + ' | findstr .exe '
        result = os.popen(cmd).read()
        resultList = result.split("\n")
        if len(resultList) < 2:
            do_log(self._modname,self._account,"----------Service stop! Now restart!-------------" )
            start_cmd = 'net start ' + self._dnspod_ddns_service
            result = os.popen(start_cmd).read()
            resultList = result.split("\n")
            for i in range(0,len(resultList)):
                do_log(self._modname,self._account,resultList[i])
        else:
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
class pypod_service_d(win32serviceutil.ServiceFramework): 
    _service_exe_name = "pypod_service.exe"
    _service_d_exe_name = "pypod_service_d.exe"
    _svc_name_ = "pypod_service_d" 
    _svc_display_name_ = "pypod_service_d" 
    _svc_description_ = "pypod_service_d" 
    _modname = "pypod_service_d"
    _account = "dnspod"
    _dnspod_ddns_service = "_dnspod_ddns_service"
    run = True
    
    def __init__(self, args): 
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
    
    def SvcDoRun(self): 
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        do_log(self._modname,self._account,"----------Service_D start!-------------" )
        ospath = cur_file_dir()
        #设置默认延时
        delay_sec = 5
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        while True:
            try:
                #检测服务状态
                cmd = 'tasklist /fi "imagename eq ' + self._service_exe_name + '"' + ' | findstr .exe '
                result = os.popen(cmd).read()
                resultList = result.split("\n")
                #系统进程中没有服务进程,则认为服务停止,启动服务
                if len(resultList) < 2:
                    do_log(self._modname,self._account,"----------Service stop! Now restart!-------------" )
                    start_cmd = 'net start ' + self._dnspod_ddns_service
                    result = os.popen(start_cmd).read()
                    resultList = result.split("\n")
                    for i in range(0,len(resultList)):
                        do_log(self._modname,self._account,resultList[i])
                else:
                    pass
            except Exception, e:
                print e
                do_log(self._modname,self._account,"-----------" + str(e) + " @pypod_service_d SvcDoRun------------")
                pass
            time.sleep(delay_sec)


    def SvcStop(self): 
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        do_log(self._modname,self._account,"----------Service stop!-------------" )
        #避免停不掉，直接杀进程
        os.system('TASKKILL /F /IM pypod_service_d.exe')

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(pypod_service_d)
    # temp_c = pydnspod_d()

#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from uilistpod_core import *


VERSION = "0.9.9." + str(int(time.time()))


app = QApplication(sys.argv)


try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

if __name__ == "__main__":
    #初始化窗体
    window = MainWindow()
    window.init_signals()
    #设置窗口置顶
    window.setWindowFlags(Qt.WindowStaysOnTopHint)
    #初始化处理（注意，窗体需要先初始化）
    dmzjcore =  uilistpod_core(window)
    
    #消息发送，处理函数定义在Core.py
    #查询按钮
    QObject.connect(window.pushButton_getrecode,SIGNAL(_fromUtf8("clicked()")),dmzjcore.pushButton_getrecode_click)
    #生成ini文件按钮
    QObject.connect(window.pushButton_makeini,SIGNAL(_fromUtf8("clicked()")),dmzjcore.pushButton_makeini_click)
    #安装并启动服务按钮
    QObject.connect(window.pushButton_install_and_start_service,SIGNAL(_fromUtf8("clicked()")),dmzjcore.pushButton_install_and_start_service_click)
    #停止并删除服务按钮
    QObject.connect(window.pushButton_stop_and_del_service,SIGNAL(_fromUtf8("clicked()")),dmzjcore.pushButton_stop_and_del_service_click)
    
    QApplication.setQuitOnLastWindowClosed(False)
    window.show()
    sys.exit(app.exec_())
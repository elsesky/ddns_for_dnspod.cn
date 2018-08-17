# -*- coding: utf-8 -*-

import operator,time

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from uilistpod import *


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
class MainWindow(QMainWindow, Ui_uilistpod):
    #初始化函数，用于设定窗口格式以及基础内容
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.createActions()
        
        #设置表头
        self.record_list.setHorizontalHeaderLabels([_fromUtf8('域名'),_fromUtf8('域ID'),_fromUtf8('记录名'),_fromUtf8('记录ID'),_fromUtf8('记录类型'),_fromUtf8('token')])
        #设置列宽
        self.record_list.setColumnWidth(0,100)
        self.record_list.setColumnWidth(1,100)
        self.record_list.setColumnWidth(2,100)
        self.record_list.setColumnWidth(3,100)
        # self.record_list.resizeColumnsToContents()
        #设置样式及基础属性
        font_t = self.record_list.horizontalHeader().font()
        font_t.setBold(True);
        #记录列表
        self.set_style(self.record_list, font_t)
        
    #设置表格样式
    def set_style(self,listwed,font_t):
        stylesheet = "::section{Background-color:rgb(220,220,220);border-radius:20px;border: 1px solid #6c6c6c}"
        listwed.horizontalHeader().setFont(font_t)
        listwed.horizontalHeader().setStretchLastSection(True)
        listwed.horizontalHeader().setStyleSheet(stylesheet)
        listwed.verticalHeader().setFont(font_t)
        listwed.verticalHeader().setStyleSheet(stylesheet)
        # listwed.resizeColumnToContents(1)#第二列根据标题自适应
        listwed.setMouseTracking(True)
        #允许右键菜单
        listwed.setContextMenuPolicy(Qt.CustomContextMenu)
        #单个选择
        listwed.setSelectionMode(QAbstractItemView.MultiSelection)
        #整行选择
        listwed.setSelectionBehavior(QAbstractItemView.SelectRows) 
        #禁止编辑
        listwed.setEditTriggers(QAbstractItemView.NoEditTriggers) 
    
    #重新定义关闭事件
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, _fromUtf8("关闭?"), \
                                           _fromUtf8("确认关闭程序?"),\
                                            QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
            qApp.quit()
        else:
            event.ignore()
        
            
    def createActions(self):
        self.minimizeAction = QAction(_fromUtf8("隐藏至系统栏"), self,
                                            triggered=self.hide)
        self.restoreAction = QAction(_fromUtf8("显示主窗口"), self,
                                           triggered=self.showNormal)
        self.quitAction = QAction(_fromUtf8("关闭"), self,
                                        triggered=qApp.quit)
        

        
############################初始化事件关联################################
    def init_signals(self):
        return 0
    
    

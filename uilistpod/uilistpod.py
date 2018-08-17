# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uilistpod.ui'
#
# Created: Fri Aug 17 13:20:49 2018
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_uilistpod(object):
    def setupUi(self, uilistpod):
        uilistpod.setObjectName(_fromUtf8("uilistpod"))
        uilistpod.resize(750, 480)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(uilistpod.sizePolicy().hasHeightForWidth())
        uilistpod.setSizePolicy(sizePolicy)
        uilistpod.setMinimumSize(QtCore.QSize(750, 480))
        uilistpod.setMaximumSize(QtCore.QSize(750, 480))
        self.record_list = QtGui.QTableWidget(uilistpod)
        self.record_list.setGeometry(QtCore.QRect(10, 60, 731, 381))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.record_list.sizePolicy().hasHeightForWidth())
        self.record_list.setSizePolicy(sizePolicy)
        self.record_list.setObjectName(_fromUtf8("record_list"))
        self.record_list.setColumnCount(6)
        self.record_list.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Adobe Devanagari"))
        item.setFont(font)
        self.record_list.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.record_list.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.record_list.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.record_list.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.record_list.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.record_list.setHorizontalHeaderItem(5, item)
        self.pushButton_getrecode = QtGui.QPushButton(uilistpod)
        self.pushButton_getrecode.setGeometry(QtCore.QRect(644, 20, 91, 23))
        self.pushButton_getrecode.setObjectName(_fromUtf8("pushButton_getrecode"))
        self.txt_podtoken = QtGui.QLineEdit(uilistpod)
        self.txt_podtoken.setGeometry(QtCore.QRect(100, 20, 531, 20))
        self.txt_podtoken.setObjectName(_fromUtf8("txt_podtoken"))
        self.label = QtGui.QLabel(uilistpod)
        self.label.setGeometry(QtCore.QRect(10, 20, 91, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.widget = QtGui.QWidget(uilistpod)
        self.widget.setGeometry(QtCore.QRect(20, 450, 701, 25))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_makeini = QtGui.QPushButton(self.widget)
        self.pushButton_makeini.setObjectName(_fromUtf8("pushButton_makeini"))
        self.horizontalLayout.addWidget(self.pushButton_makeini)
        self.pushButton_install_and_start_service = QtGui.QPushButton(self.widget)
        self.pushButton_install_and_start_service.setObjectName(_fromUtf8("pushButton_install_and_start_service"))
        self.horizontalLayout.addWidget(self.pushButton_install_and_start_service)
        self.pushButton_stop_and_del_service = QtGui.QPushButton(self.widget)
        self.pushButton_stop_and_del_service.setObjectName(_fromUtf8("pushButton_stop_and_del_service"))
        self.horizontalLayout.addWidget(self.pushButton_stop_and_del_service)

        self.retranslateUi(uilistpod)
        QtCore.QMetaObject.connectSlotsByName(uilistpod)

    def retranslateUi(self, uilistpod):
        uilistpod.setWindowTitle(_translate("uilistpod", "配置文件生成工具", None))
        item = self.record_list.horizontalHeaderItem(0)
        item.setText(_translate("uilistpod", "域名", None))
        item = self.record_list.horizontalHeaderItem(1)
        item.setText(_translate("uilistpod", "域ID", None))
        item = self.record_list.horizontalHeaderItem(2)
        item.setText(_translate("uilistpod", "记录名", None))
        item = self.record_list.horizontalHeaderItem(3)
        item.setText(_translate("uilistpod", "记录ID", None))
        item = self.record_list.horizontalHeaderItem(4)
        item.setText(_translate("uilistpod", "记录类型", None))
        item = self.record_list.horizontalHeaderItem(5)
        item.setText(_translate("uilistpod", "token", None))
        self.pushButton_getrecode.setText(_translate("uilistpod", "获取记录清单", None))
        self.label.setText(_translate("uilistpod", "输入API TOKEN", None))
        self.pushButton_makeini.setText(_translate("uilistpod", "生成INI配置文件", None))
        self.pushButton_install_and_start_service.setText(_translate("uilistpod", "安装并启动服务", None))
        self.pushButton_stop_and_del_service.setText(_translate("uilistpod", "停止并删除服务", None))


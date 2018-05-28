# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'repair.ui'
#
# Created: Tue Jan 02 19:59:05 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Warning_Dialog(object):
    def setupUi(self, Warning_Dialog):
        Warning_Dialog.setObjectName("Warning_Dialog")
        Warning_Dialog.resize(481, 437)
        self.repair_verticalLayout_01 = QtGui.QVBoxLayout(Warning_Dialog)
        self.repair_verticalLayout_01.setObjectName("repair_verticalLayout_01")
        self.widget = QtGui.QWidget(Warning_Dialog)
        self.widget.setObjectName("widget")
        self.repair_verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.repair_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.repair_verticalLayout.setObjectName("repair_verticalLayout")
        self.repair_tableWidget = QtGui.QTableWidget(self.widget)
        self.repair_tableWidget.setObjectName("repair_tableWidget")
        self.repair_tableWidget.setColumnCount(0)
        self.repair_tableWidget.setRowCount(0)
        self.repair_verticalLayout.addWidget(self.repair_tableWidget)
        self.repair_pushButton = QtGui.QPushButton(self.widget)
        self.repair_pushButton.setObjectName("repair_pushButton")
        self.repair_verticalLayout.addWidget(self.repair_pushButton)
        self.repair_verticalLayout_01.addWidget(self.widget)

        self.retranslateUi(Warning_Dialog)
        QtCore.QMetaObject.connectSlotsByName(Warning_Dialog)

    def retranslateUi(self, Warning_Dialog):
        Warning_Dialog.setWindowTitle(QtGui.QApplication.translate("Warning_Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.repair_pushButton.setText(QtGui.QApplication.translate("Warning_Dialog", "repair", None, QtGui.QApplication.UnicodeUTF8))


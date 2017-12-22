# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\work\src\validation\resources\info_form.ui'
#
# Created: Sat Jan 07 17:08:49 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

#from PySide import QtCore, QtGui
from head import *

class Ui_info_form(object):
    def setupUi(self, info_form):
        info_form.setObjectName("info_form")
        info_form.resize(652, 425)
        self.verticalLayout_2 = QtGui.QVBoxLayout(info_form)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtGui.QFrame(info_form)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.sel_btn = QtGui.QToolButton(self.frame)
        self.sel_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icons/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.sel_btn.setIcon(icon)
        self.sel_btn.setAutoRaise(True)
        self.sel_btn.setObjectName("sel_btn")
        self.horizontalLayout_2.addWidget(self.sel_btn)
        self.expand_btn = QtGui.QToolButton(self.frame)
        self.expand_btn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../icons/group_collapse.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.expand_btn.setIcon(icon1)
        self.expand_btn.setAutoRaise(True)
        self.expand_btn.setObjectName("expand_btn")
        self.horizontalLayout_2.addWidget(self.expand_btn)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.obj_name = QtGui.QLabel(self.frame)
        self.obj_name.setStyleSheet("")
        self.obj_name.setTextFormat(QtCore.Qt.AutoText)
        self.obj_name.setObjectName("obj_name")
        self.horizontalLayout_2.addWidget(self.obj_name)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.del_btn = QtGui.QToolButton(self.frame)
        self.del_btn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../icons/clear_search.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.del_btn.setIcon(icon2)
        self.del_btn.setAutoRaise(True)
        self.del_btn.setObjectName("del_btn")
        self.horizontalLayout_2.addWidget(self.del_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.info_text = QtGui.QTextEdit(self.frame)
        self.info_text.setFrameShape(QtGui.QFrame.NoFrame)
        self.info_text.setFrameShadow(QtGui.QFrame.Plain)
        self.info_text.setReadOnly(True)
        self.info_text.setObjectName("info_text")
        self.verticalLayout.addWidget(self.info_text)
        self.verticalLayout_2.addWidget(self.frame)

        self.retranslateUi(info_form)
        QtCore.QObject.connect(self.del_btn, QtCore.SIGNAL("clicked()"), info_form.close)
        QtCore.QObject.connect(self.expand_btn, QtCore.SIGNAL("clicked(bool)"), self.info_text.setVisible)
        QtCore.QMetaObject.connectSlotsByName(info_form)

    def retranslateUi(self, info_form):
        info_form.setWindowTitle(QtGui.QApplication.translate("info_form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.obj_name.setText(QtGui.QApplication.translate("info_form", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600; color:#ff0000;\">object</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))


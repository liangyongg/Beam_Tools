# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\work\src\validation\resources\item_form.ui'
#
# Created: Sat Jan 07 17:08:48 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

#from PySide import QtCore, QtGui
from head import *

class Ui_item_form(object):
    def setupUi(self, item_form):
        item_form.setObjectName("item_form")
        item_form.resize(445, 42)
        self.horizontalLayout = QtGui.QHBoxLayout(item_form)
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.item_icon = QtGui.QLabel(item_form)
        self.item_icon.setMinimumSize(QtCore.QSize(16, 16))
        self.item_icon.setMaximumSize(QtCore.QSize(16, 16))
        self.item_icon.setText("")
        self.item_icon.setPixmap(QtGui.QPixmap("failure.png"))
        self.item_icon.setScaledContents(True)
        self.item_icon.setObjectName("item_icon")
        self.horizontalLayout.addWidget(self.item_icon)
        self.item_name = QtGui.QLabel(item_form)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.item_name.setFont(font)
        self.item_name.setObjectName("item_name")
        self.horizontalLayout.addWidget(self.item_name)
        spacerItem = QtGui.QSpacerItem(175, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.correct_btn = QtGui.QToolButton(item_form)
        self.correct_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icons/correct.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.correct_btn.setIcon(icon)
        self.correct_btn.setAutoRaise(True)
        self.correct_btn.setObjectName("correct_btn")
        self.horizontalLayout.addWidget(self.correct_btn)
        self.skip_btn = QtGui.QToolButton(item_form)
        self.skip_btn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../icons/clear_search.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.skip_btn.setIcon(icon1)
        self.skip_btn.setPopupMode(QtGui.QToolButton.DelayedPopup)
        self.skip_btn.setAutoRaise(True)
        self.skip_btn.setArrowType(QtCore.Qt.NoArrow)
        self.skip_btn.setObjectName("skip_btn")
        self.horizontalLayout.addWidget(self.skip_btn)

        self.retranslateUi(item_form)
        QtCore.QMetaObject.connectSlotsByName(item_form)

    def retranslateUi(self, item_form):
        item_form.setWindowTitle(QtGui.QApplication.translate("item_form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.item_name.setText(QtGui.QApplication.translate("item_form", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))


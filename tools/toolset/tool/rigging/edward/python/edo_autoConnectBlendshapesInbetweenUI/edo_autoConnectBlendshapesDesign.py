# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/program/git/release/edward/python/edo_autoConnectBlendshapesInbetweenUI/edo_autoConnectBlendshapesDesign.ui'
#
# Created: Thu Jun 04 15:37:54 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from headfile import *

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

class Ui_edo_autoConnectBlendshapesUI(object):
    def setupUi(self, edo_autoConnectBlendshapesUI):
        edo_autoConnectBlendshapesUI.setObjectName(_fromUtf8("edo_autoConnectBlendshapesUI"))
        edo_autoConnectBlendshapesUI.resize(409, 421)
        self.centralwidget = QtGui.QWidget(edo_autoConnectBlendshapesUI)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 391, 371))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.createFacialCtrl = QtGui.QWidget()
        self.createFacialCtrl.setObjectName(_fromUtf8("createFacialCtrl"))
        self.ctrlNameLe = QtGui.QLineEdit(self.createFacialCtrl)
        self.ctrlNameLe.setGeometry(QtCore.QRect(130, 40, 181, 31))
        self.ctrlNameLe.setObjectName(_fromUtf8("ctrlNameLe"))
        self.createCtrlBt = QtGui.QPushButton(self.createFacialCtrl)
        self.createCtrlBt.setEnabled(True)
        self.createCtrlBt.setGeometry(QtCore.QRect(10, 90, 181, 88))
        self.createCtrlBt.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/createFacialCtrl.jpg)"))
        self.createCtrlBt.setText(_fromUtf8(""))
        self.createCtrlBt.setIconSize(QtCore.QSize(181, 91))
        self.createCtrlBt.setObjectName(_fromUtf8("createCtrlBt"))
        self.addMultiplyFrameBt = QtGui.QPushButton(self.createFacialCtrl)
        self.addMultiplyFrameBt.setGeometry(QtCore.QRect(200, 90, 181, 88))
        self.addMultiplyFrameBt.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/complexFrame.jpg)"))
        self.addMultiplyFrameBt.setText(_fromUtf8(""))
        self.addMultiplyFrameBt.setIconSize(QtCore.QSize(181, 91))
        self.addMultiplyFrameBt.setObjectName(_fromUtf8("addMultiplyFrameBt"))
        self.label_3 = QtGui.QLabel(self.createFacialCtrl)
        self.label_3.setGeometry(QtCore.QRect(20, 40, 101, 31))
        self.label_3.setStyleSheet(_fromUtf8("font: 10pt \"MS Shell Dlg 2\";"))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.isctrl_cb = QtGui.QCheckBox(self.createFacialCtrl)
        self.isctrl_cb.setGeometry(QtCore.QRect(20, 20, 131, 16))
        self.isctrl_cb.setStyleSheet(_fromUtf8("font: 10pt \"MS Shell Dlg 2\";"))
        self.isctrl_cb.setChecked(True)
        self.isctrl_cb.setObjectName(_fromUtf8("isctrl_cb"))
        self.tabWidget.addTab(self.createFacialCtrl, _fromUtf8(""))
        self.connect = QtGui.QWidget()
        self.connect.setObjectName(_fromUtf8("connect"))
        self.renameBt = QtGui.QPushButton(self.connect)
        self.renameBt.setGeometry(QtCore.QRect(10, 80, 181, 88))
        self.renameBt.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/renameBlendshape.jpg)"))
        self.renameBt.setText(_fromUtf8(""))
        self.renameBt.setIconSize(QtCore.QSize(181, 91))
        self.renameBt.setObjectName(_fromUtf8("renameBt"))
        self.autoConnectBt = QtGui.QPushButton(self.connect)
        self.autoConnectBt.setGeometry(QtCore.QRect(200, 80, 181, 88))
        self.autoConnectBt.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/connectBlendshape.jpg)"))
        self.autoConnectBt.setText(_fromUtf8(""))
        self.autoConnectBt.setIconSize(QtCore.QSize(181, 91))
        self.autoConnectBt.setObjectName(_fromUtf8("autoConnectBt"))
        self.attachMeshBt = QtGui.QPushButton(self.connect)
        self.attachMeshBt.setGeometry(QtCore.QRect(10, 180, 371, 71))
        self.attachMeshBt.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/meshControlTransform.jpg)"))
        self.attachMeshBt.setText(_fromUtf8(""))
        self.attachMeshBt.setIconSize(QtCore.QSize(372, 52))
        self.attachMeshBt.setObjectName(_fromUtf8("attachMeshBt"))
        self.label_2 = QtGui.QLabel(self.connect)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 111, 31))
        self.label_2.setStyleSheet(_fromUtf8("font: 10pt \"MS Shell Dlg 2\";"))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.dial = QtGui.QDial(self.connect)
        self.dial.setGeometry(QtCore.QRect(280, 16, 71, 58))
        self.dial.setMinimum(0)
        self.dial.setMaximum(100)
        self.dial.setSingleStep(1)
        self.dial.setProperty("value", 1)
        self.dial.setObjectName(_fromUtf8("dial"))
        self.doubleSpinBox = QtGui.QDoubleSpinBox(self.connect)
        self.doubleSpinBox.setGeometry(QtCore.QRect(140, 30, 131, 31))
        self.doubleSpinBox.setDecimals(3)
        self.doubleSpinBox.setMinimum(-5.0)
        self.doubleSpinBox.setMaximum(5.0)
        self.doubleSpinBox.setSingleStep(0.1)
        self.doubleSpinBox.setProperty("value", 1.0)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.tabWidget.addTab(self.connect, _fromUtf8(""))
        self.pick_up = QtGui.QWidget()
        self.pick_up.setObjectName(_fromUtf8("pick_up"))
        self.blendshapeNameBt = QtGui.QPushButton(self.pick_up)
        self.blendshapeNameBt.setGeometry(QtCore.QRect(270, 10, 41, 31))
        self.blendshapeNameBt.setObjectName(_fromUtf8("blendshapeNameBt"))
        self.blendshapeNameLe = QtGui.QLineEdit(self.pick_up)
        self.blendshapeNameLe.setGeometry(QtCore.QRect(120, 10, 141, 31))
        self.blendshapeNameLe.setObjectName(_fromUtf8("blendshapeNameLe"))
        self.pickupAllBlendshapeBt = QtGui.QPushButton(self.pick_up)
        self.pickupAllBlendshapeBt.setGeometry(QtCore.QRect(200, 250, 181, 88))
        self.pickupAllBlendshapeBt.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/pickUpAllBlendshape.jpg)"))
        self.pickupAllBlendshapeBt.setText(_fromUtf8(""))
        self.pickupAllBlendshapeBt.setIconSize(QtCore.QSize(181, 91))
        self.pickupAllBlendshapeBt.setObjectName(_fromUtf8("pickupAllBlendshapeBt"))
        self.pickupSelectedBlendshapeBt = QtGui.QPushButton(self.pick_up)
        self.pickupSelectedBlendshapeBt.setGeometry(QtCore.QRect(10, 250, 181, 88))
        self.pickupSelectedBlendshapeBt.setStyleSheet(_fromUtf8("background:url(:/buttonIcon/pickUpSelectedBlendshape.jpg)"))
        self.pickupSelectedBlendshapeBt.setText(_fromUtf8(""))
        self.pickupSelectedBlendshapeBt.setIconSize(QtCore.QSize(181, 91))
        self.pickupSelectedBlendshapeBt.setObjectName(_fromUtf8("pickupSelectedBlendshapeBt"))
        self.blendshapeListLw = QtGui.QListWidget(self.pick_up)
        self.blendshapeListLw.setGeometry(QtCore.QRect(10, 50, 241, 171))
        self.blendshapeListLw.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.blendshapeListLw.setObjectName(_fromUtf8("blendshapeListLw"))
        self.inbetweenListLw = QtGui.QListWidget(self.pick_up)
        self.inbetweenListLw.setGeometry(QtCore.QRect(270, 50, 111, 171))
        self.inbetweenListLw.setObjectName(_fromUtf8("inbetweenListLw"))
        self.label = QtGui.QLabel(self.pick_up)
        self.label.setGeometry(QtCore.QRect(10, 10, 101, 31))
        self.label.setStyleSheet(_fromUtf8("font: 10pt \"MS Shell Dlg 2\";"))
        self.label.setObjectName(_fromUtf8("label"))
        self.keepConnectionCb = QtGui.QCheckBox(self.pick_up)
        self.keepConnectionCb.setGeometry(QtCore.QRect(20, 230, 101, 18))
        self.keepConnectionCb.setObjectName(_fromUtf8("keepConnectionCb"))
        self.tabWidget.addTab(self.pick_up, _fromUtf8(""))
        self.other = QtGui.QWidget()
        self.other.setObjectName(_fromUtf8("other"))
        self.triangleMatcher_Bt = QtGui.QPushButton(self.other)
        self.triangleMatcher_Bt.setGeometry(QtCore.QRect(8, 3, 87, 86))
        self.triangleMatcher_Bt.setStyleSheet(_fromUtf8("font: italic 9pt \"Gill Sans Ultra Bold\";\n"
"color:rgb(0,0,0);\n"
"background:url(:/buttonIcon/buttonBackground005.jpg);\n"
"\n"
""))
        self.triangleMatcher_Bt.setObjectName(_fromUtf8("triangleMatcher_Bt"))
        self.secondaryControlerl_Bt = QtGui.QPushButton(self.other)
        self.secondaryControlerl_Bt.setEnabled(True)
        self.secondaryControlerl_Bt.setGeometry(QtCore.QRect(103, 3, 87, 86))
        self.secondaryControlerl_Bt.setStyleSheet(_fromUtf8("font: italic 9pt \"Gill Sans Ultra Bold\";\n"
"color:rgb(0,0,0);\n"
"background:url(:/buttonIcon/buttonBackground005.jpg);\n"
"\n"
""))
        self.secondaryControlerl_Bt.setObjectName(_fromUtf8("secondaryControlerl_Bt"))
        self.mirrorbs_bs = QtGui.QPushButton(self.other)
        self.mirrorbs_bs.setEnabled(True)
        self.mirrorbs_bs.setGeometry(QtCore.QRect(8, 260, 87, 86))
        self.mirrorbs_bs.setStyleSheet(_fromUtf8("font: italic 9pt \"Gill Sans Ultra Bold\";\n"
"color:rgb(0,0,0);\n"
"background:url(:/buttonIcon/buttonBackground005.jpg);\n"
"\n"
""))
        self.mirrorbs_bs.setObjectName(_fromUtf8("mirrorbs_bs"))
        self.transfermeshes_bt = QtGui.QPushButton(self.other)
        self.transfermeshes_bt.setEnabled(True)
        self.transfermeshes_bt.setGeometry(QtCore.QRect(103, 260, 87, 86))
        self.transfermeshes_bt.setStyleSheet(_fromUtf8("font: italic 9pt \"Gill Sans Ultra Bold\";\n"
"color:rgb(0,0,0);\n"
"background:url(:/buttonIcon/buttonBackground005.jpg);\n"
"\n"
""))
        self.transfermeshes_bt.setObjectName(_fromUtf8("transfermeshes_bt"))
        self.calculatebs_bt = QtGui.QPushButton(self.other)
        self.calculatebs_bt.setEnabled(True)
        self.calculatebs_bt.setGeometry(QtCore.QRect(293, 3, 87, 86))
        self.calculatebs_bt.setStyleSheet(_fromUtf8("font: italic 9pt \"Gill Sans Ultra Bold\";\n"
"color:rgb(0,0,0);\n"
"background:url(:/buttonIcon/buttonBackground005.jpg);\n"
"\n"
""))
        self.calculatebs_bt.setObjectName(_fromUtf8("calculatebs_bt"))
        self.calculateBs_Bt = QtGui.QPushButton(self.other)
        self.calculateBs_Bt.setEnabled(True)
        self.calculateBs_Bt.setGeometry(QtCore.QRect(293, 260, 87, 86))
        self.calculateBs_Bt.setStyleSheet(_fromUtf8("font: italic 9pt \"Gill Sans Ultra Bold\";\n"
"color:rgb(0,0,0);\n"
"background:url(:/buttonIcon/buttonBackground005.jpg);\n"
"\n"
""))
        self.calculateBs_Bt.setObjectName(_fromUtf8("calculateBs_Bt"))
        self.updateTopology_bt = QtGui.QPushButton(self.other)
        self.updateTopology_bt.setEnabled(True)
        self.updateTopology_bt.setGeometry(QtCore.QRect(200, 3, 87, 86))
        self.updateTopology_bt.setStyleSheet(_fromUtf8("font: italic 9pt \"Gill Sans Ultra Bold\";\n"
"color:rgb(0,0,0);\n"
"background:url(:/buttonIcon/buttonBackground005.jpg);\n"
"\n"
""))
        self.updateTopology_bt.setObjectName(_fromUtf8("updateTopology_bt"))
        self.underworldbs_Bt = QtGui.QPushButton(self.other)
        self.underworldbs_Bt.setEnabled(False)
        self.underworldbs_Bt.setGeometry(QtCore.QRect(200, 260, 87, 86))
        self.underworldbs_Bt.setStyleSheet(_fromUtf8("font: italic 9pt \"Gill Sans Ultra Bold\";\n"
"color:rgb(0,0,0);\n"
"background:url(:/buttonIcon/buttonBackground004.jpg);\n"
"\n"
""))
        self.underworldbs_Bt.setObjectName(_fromUtf8("underworldbs_Bt"))
        self.skeletonDrivingBall_Bt = QtGui.QPushButton(self.other)
        self.skeletonDrivingBall_Bt.setGeometry(QtCore.QRect(8, 89, 87, 86))
        self.skeletonDrivingBall_Bt.setStyleSheet(_fromUtf8("font: italic 9pt \"Gill Sans Ultra Bold\";\n"
"color:rgb(0,0,0);\n"
"background:url(:/buttonIcon/buttonBackground005.jpg);\n"
"\n"
""))
        self.skeletonDrivingBall_Bt.setObjectName(_fromUtf8("skeletonDrivingBall_Bt"))
        self.facialeasyedit_Bt = QtGui.QPushButton(self.other)
        self.facialeasyedit_Bt.setEnabled(False)
        self.facialeasyedit_Bt.setGeometry(QtCore.QRect(293, 174, 87, 86))
        self.facialeasyedit_Bt.setStyleSheet(_fromUtf8("font: italic 9pt \"Gill Sans Ultra Bold\";\n"
"color:rgb(0,0,0);\n"
"background:url(:/buttonIcon/buttonBackground004.jpg);\n"
"\n"
""))
        self.facialeasyedit_Bt.setObjectName(_fromUtf8("facialeasyedit_Bt"))
        self.rbfPoseDeformer_Bt = QtGui.QPushButton(self.other)
        self.rbfPoseDeformer_Bt.setEnabled(False)
        self.rbfPoseDeformer_Bt.setGeometry(QtCore.QRect(103, 89, 87, 86))
        self.rbfPoseDeformer_Bt.setStyleSheet(_fromUtf8("font: italic 9pt \"Gill Sans Ultra Bold\";\n"
"color:rgb(0,0,0);\n"
"background:url(:/buttonIcon/buttonBackground004.jpg);\n"
"\n"
""))
        self.rbfPoseDeformer_Bt.setObjectName(_fromUtf8("rbfPoseDeformer_Bt"))
        self.tabWidget.addTab(self.other, _fromUtf8(""))
        self.normalizedbs_bt = QtGui.QPushButton(self.centralwidget)
        self.normalizedbs_bt.setEnabled(True)
        self.normalizedbs_bt.setGeometry(QtCore.QRect(540, 30, 87, 86))
        self.normalizedbs_bt.setStyleSheet(_fromUtf8("font: italic 9pt \"Gill Sans Ultra Bold\";\n"
"color:rgb(0,0,0);\n"
"background:url(:/buttonIcon/buttonBackground005.jpg);\n"
"\n"
""))
        self.normalizedbs_bt.setObjectName(_fromUtf8("normalizedbs_bt"))
        edo_autoConnectBlendshapesUI.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(edo_autoConnectBlendshapesUI)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 409, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        edo_autoConnectBlendshapesUI.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(edo_autoConnectBlendshapesUI)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        edo_autoConnectBlendshapesUI.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(edo_autoConnectBlendshapesUI)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(edo_autoConnectBlendshapesUI)

    def retranslateUi(self, edo_autoConnectBlendshapesUI):
        edo_autoConnectBlendshapesUI.setWindowTitle(_translate("edo_autoConnectBlendshapesUI", "edo_autoConnectBlendshapesUI", None))
        self.label_3.setText(_translate("edo_autoConnectBlendshapesUI", "facial Ctrl Name:", None))
        self.isctrl_cb.setText(_translate("edo_autoConnectBlendshapesUI", "  is controler", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.createFacialCtrl), _translate("edo_autoConnectBlendshapesUI", "createFacialCtrl", None))
        self.label_2.setText(_translate("edo_autoConnectBlendshapesUI", "inbetween weight:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.connect), _translate("edo_autoConnectBlendshapesUI", "CONNECT", None))
        self.blendshapeNameBt.setText(_translate("edo_autoConnectBlendshapesUI", "GET", None))
        self.label.setText(_translate("edo_autoConnectBlendshapesUI", "blendshapeNode:", None))
        self.keepConnectionCb.setText(_translate("edo_autoConnectBlendshapesUI", "keep connection", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.pick_up), _translate("edo_autoConnectBlendshapesUI", "PICK UP", None))
        self.triangleMatcher_Bt.setText(_translate("edo_autoConnectBlendshapesUI", "Triangle\n"
"Matcher", None))
        self.secondaryControlerl_Bt.setText(_translate("edo_autoConnectBlendshapesUI", "Secondary\n"
"Controler", None))
        self.mirrorbs_bs.setText(_translate("edo_autoConnectBlendshapesUI", "Mirror\n"
"BlendShape", None))
        self.transfermeshes_bt.setText(_translate("edo_autoConnectBlendshapesUI", "transfer\n"
"Meshes", None))
        self.calculatebs_bt.setText(_translate("edo_autoConnectBlendshapesUI", "blendshape\n"
"Calculator", None))
        self.calculateBs_Bt.setText(_translate("edo_autoConnectBlendshapesUI", "Calculate\n"
"Blendshape", None))
        self.updateTopology_bt.setText(_translate("edo_autoConnectBlendshapesUI", "update\n"
"Topology", None))
        self.underworldbs_Bt.setText(_translate("edo_autoConnectBlendshapesUI", "underworld\n"
"BlendShape", None))
        self.skeletonDrivingBall_Bt.setText(_translate("edo_autoConnectBlendshapesUI", "Skeleton\n"
"DrivingBall", None))
        self.facialeasyedit_Bt.setText(_translate("edo_autoConnectBlendshapesUI", "Facial\n"
"EasyEditor", None))
        self.rbfPoseDeformer_Bt.setText(_translate("edo_autoConnectBlendshapesUI", "RBF\n"
"PoseDeformer", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.other), _translate("edo_autoConnectBlendshapesUI", "OTHER", None))
        self.normalizedbs_bt.setText(_translate("edo_autoConnectBlendshapesUI", "normalized\n"
"blendshape\n"
"weights", None))
        self.menuHelp.setTitle(_translate("edo_autoConnectBlendshapesUI", "help", None))

import edo_autoConnectBlendshapesInbetweenUI_rc

# -*- coding: utf-8 -*-

import os
import sys
import functools
import glob
from rigging.taskview.ui.head import *
from rigging.taskview.ui.ui_main_window import ui_main_window
from rigging.taskview.env.Config import Config

try:
    import pymel.core as pm
    import maya.cmds as cmds
    import maya.OpenMaya as OpenMaya
except:
    pass

#from PySide import QtGui,QtCore
class From(QtGui.QMainWindow):

    def __init__(self,parent = None):
        super(From,self).__init__(parent)
        self._plugins_path = []
        self.item_list = []
        self.item_data = {}
        self.info_list = []
        self.cmd = None

        self.setWindowTitle ("rigging_taskview")
        self.setupUI()
        self.getElems()
        self.setDefault()
        self.connections()

    def setupUI (self):
        self.ui_main_window = ui_main_window ()
        self.setCentralWidget (self.ui_main_window)

    def getElems(self):
        self.filepath_label = self.ui_main_window.ui_taskview_widget.main_Widget.filepath_label
        self.asset_comboBox = self.ui_main_window.ui_taskview_widget.main_Widget.asset_comboBox
        self.level_comboBox = self.ui_main_window.ui_taskview_widget.main_Widget.level_comboBox
        self.steps_comboBox = self.ui_main_window.ui_taskview_widget.main_Widget.steps_comboBox

        self.assettype_listWidget = self.ui_main_window.ui_taskview_widget.main_Widget.assettype_listWidget
        self.assetname_listWidget = self.ui_main_window.ui_taskview_widget.main_Widget.assetname_listWidget
        self.version_listWidget = self.ui_main_window.ui_taskview_widget.main_Widget.version_listWidget
        self.gotofile_pushButton = self.ui_main_window.ui_taskview_widget.main_Widget.gotofile_pushButton

    def setDefault(self):
        self.level_comboBox.setCurrentIndex(3)
        self.steps_comboBox.setCurrentIndex (1)
        self.project_asset_work_path = Config.PROJECT_ASSET_RIG_WORK_PATH

        self.version_listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.version_listWidget.customContextMenuRequested.connect(self.showContextMenu)

        self.contextMenu = QtGui.QMenu(self.version_listWidget)
        self.open_maya = self.contextMenu.addAction(u'open maya')
        self.import_maya = self.contextMenu.addAction (u'import maya')
        self.import_reference = self.contextMenu.addAction (u'reference maya')
        self.open_maya.triggered.connect(self.openFile)
        self.import_maya.triggered.connect(self.importFile)
        self.import_reference.triggered.connect (self.referenceFile)

    def connections(self):
        self.asset_comboBox.currentIndexChanged[unicode].connect(self.get_current_asset_combobox)
        self.steps_comboBox.currentIndexChanged [unicode].connect (self.get_current_steps_comboBox)
        self.assetname_listWidget.currentTextChanged.connect(self.get_current_assettype_combobox)
        self.assettype_listWidget.currentTextChanged.connect(self.get_current_version_combobox)
        self.version_listWidget.currentTextChanged.connect(self.get_version_current_item)

        self.gotofile_pushButton.clicked.connect(self.gotofile)

    def get_maya_file(self):
        #self.getcurrenttext ()
        self.current_version_item_sel = self.version_listWidget.currentItem()
        if self.current_version_item_sel:
            self.current_version_item = self.current_version_item_sel.text()
        file_folder = self.version_item.get(self.current_version_item)
        #file_list.extend (glob.glob (os.path.join (file_folder, '*ma')))
        #file_list.extend (glob.glob (os.path.join (file_folder, '*mb')))
        if file_folder:
            maya_file = file_folder
            #print maya_file
            return maya_file

    def get_current_asset_combobox(self):
        self.getcurrenttext()
        self.update_asset_items()

    def get_current_assettype_combobox(self,current):
        self.current_asset_item_sel = self.assetname_listWidget.currentItem()
        if self.current_asset_item_sel:
            self.current_asset_item = self.current_asset_item_sel.text()
        self.update_assettype_items()

    def get_current_version_combobox(self,current):
        self.current_assettype_item_sel = self.assettype_listWidget.currentItem ()
        if self.current_assettype_item_sel:
            self.current_assettype_item = self.current_assettype_item_sel.text()
        self.update_version_items()

    def get_version_current_item(self):
        self.filepath_label.setText('')
        self.current_version_item_sel = self.version_listWidget.currentItem()
        if self.current_version_item_sel:
            self.current_version_item = self.current_version_item_sel.text()
        maya_file = self.get_maya_file()
        self.filepath_label.setText(maya_file)

    def get_current_steps_comboBox(self):
        self.update_steps_items()

    def update_asset_items(self):
        self.getcurrenttext()
        folder_list = list()
        if self.asset and self.level and self.steps:
            assert_path = os.path.join(self.project_asset_work_path,self.asset)
            if os.path.exists(assert_path):
                print assert_path
                folder_list = os.listdir(assert_path)
            #else:
            #    print "path not exsits!!!"
        self.assetname_listWidget.clear()
        if folder_list:
            folder_list.sort()
            self.assetname_listWidget.addItems(folder_list)

    def update_assettype_items(self):
        self.getcurrenttext()
        folder_list = list ()
        if self.asset and self.level and self.steps:
            assettype_path = os.path.join (self.project_asset_work_path, self.asset, self.current_asset_item,
                                           self.steps)
            if os.path.exists(assettype_path):
                print assettype_path
                folder_list = os.listdir(assettype_path)
        self.assettype_listWidget.clear()
        if folder_list:
            folder_list.sort()
            self.assettype_listWidget.addItems(folder_list)

    def update_steps_items(self):
        self.update_asset_items()
        #if self.asset and self.level and self.steps:
        #    steps_path = os.path.join (self.project_asset_work_path, self.asset, self.current_asset_item,
        #                                   self.steps)

    def update_version_items(self):
        self.getcurrenttext ()
        folder_list = list ()
        self.version_item = dict()
        if self.asset and self.level and self.steps:
            assetversion_path = os.path.join (self.project_asset_work_path, self.asset, self.current_asset_item,
                                              self.steps,self.current_assettype_item)
            if os.path.exists(assetversion_path):
                #print assetversion_path
                #folder_list = os.listdir(assetversion_path)
                ma_path = os.path.join(assetversion_path,"*.ma")
                mb_path = os.path.join(assetversion_path,"*.mb")
                #print ma_path,mb_path
                folder_list.extend(glob.glob(ma_path))
                folder_list.extend(glob.glob(mb_path))

        version_list = list()
        if folder_list:
            for folder in folder_list:
                version_file = os.path.basename(folder)
                version_list.append(version_file)
                self.version_item[version_file] = folder
        self.version_listWidget.clear ()
        if version_list:
            version_list.sort()
            self.version_listWidget.addItems(version_list)

    def getcurrenttext(self):
        self.asset = self.asset_comboBox.currentText()
        self.level = self.level_comboBox.currentText()
        self.steps = self.steps_comboBox.currentText()

    def showContextMenu(self):
        self.contextMenu.move(QtGui.QCursor.pos())
        self.contextMenu.show()

    def openFile(self):
        maya_file = self.filepath_label.text()
        if maya_file:
            mFile = OpenMaya.MFileIO()
            mFile.open(r"%s"%os.path.abspath(maya_file).replace("\\","/"),None,True)

    def importFile(self):
        maya_file = self.filepath_label.text ()
        if maya_file:
            mFile = OpenMaya.MFileIO()
            util = OpenMaya.MScriptUtil ()
            ptr = util.asCharPtr ()
            mFile.importFile (r"%s" % os.path.abspath (maya_file).replace ("\\", "/"),
                              None, False,
                              None,False)

    def referenceFile(self):
        maya_file = self.filepath_label.text ()
        if maya_file:
            mFile = OpenMaya.MFileIO()
            mFile.reference(r"%s"%os.path.abspath(maya_file).replace("\\","/"),
                            False,False,os.path.basename(maya_file))

    def gotofile(self):
        maya_file = self.filepath_label.text()
        os.startfile(os.path.dirname(maya_file))

    def showWinodow(self):
        self.myapp = From()
        self.myapp.show()
        return self.myapp

if __name__=="__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = From()
    ui.showWinodow()
    sys.exit(app.exec_())
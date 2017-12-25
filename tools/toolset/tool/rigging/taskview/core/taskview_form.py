# -*- coding: utf-8 -*-

import os
import sys
import functools
from rigging.taskview.ui.head import *
from rigging.taskview.ui.ui_main_window import ui_main_window
from rigging.taskview.env.Config import Config

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

    def setupUI (self):
        self.ui_main_window = ui_main_window ()
        self.setCentralWidget (self.ui_main_window)

    def getElems(self):
        self.assettype_listWidget = self.ui_main_window.ui_taskview_widget.main_Widget.assettype_listWidget

    def setDefault(self):
        self.project_asset_work_path = Config.PROJECT_ASSET_RIG_WORK_PATH

        self.assettype_listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.assettype_listWidget.customContextMenuRequested.connect(self.showContextMenu)

        self.contextMenu = QtGui.QMenu(self.assettype_listWidget)
        self.contextMenu.addAction(u'aaa')
        self.contextMenu.addAction (u'bbb')
        self.contextMenu.addAction (u'ccc')

    def showContextMenu(self):
        self.contextMenu.move(QtGui.QCursor.pos())
        self.contextMenu.show()

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
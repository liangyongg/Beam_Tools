#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import glob

import maya.cmds as cmds
from animation.remove_maya_plug.ui.head import *
from animation.remove_maya_plug.ui.ui_main_window import ui_main_window

class Response(QtGui.QMainWindow):

    def __init__(self,parent=None):
        super(Response,self).__init__(parent)
        self.maya_win = parent
        self.setWindowTitle("remove_maya_plug")
        self.setupUI()
        self.getElems()

    def setupUI(self):
        self.ui_main_window = ui_main_window()
        self.setCentralWidget(self.ui_main_window)

    def getElems(self):
        self.pushButton = self.ui_main_window.ui_check_widget.main_Widget.pushButton

    def setDefault(self):
        pass

    def shake_win(self):
        pass

    def mouseMoveEvent(self,event):
        pass

    def dragMoveEvent(self,event):
        pass

    def dragEnterEvent(self,event):
        pass

    def dropEvent(self,event):
        pass

    def setupConnections(self):
        pass


if __name__=="__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = Response()
    ui.show()
    sys.exit(app.exec_())
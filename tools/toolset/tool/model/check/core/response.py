#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import glob

import maya.cmds as cmds
from model.check.ui.head import *
from model.check.ui.ui_main_window import ui_main_window
class Response(QtWidgets.QMainWindow):

    def __init__(self,parent=None):
        super(Response,self).__init__(parent)
        self.maya_win = parent
        self.setWindowTitle("model_check")
        self.setupUI()
        self.getElems()

    def setupUI(self):
        self.ui_main_window = ui_main_window()
        self.setCentralWidget(self.ui_main_window)

    def getElems(self):
        self.pushButton = self.ui_main_window.ui_check_widget.main_Widget.pushButton

if __name__=="__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Response()
    ui.show()
    sys.exit(app.exec_())
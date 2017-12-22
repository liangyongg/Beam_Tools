#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import glob

import maya.cmds as cmds
from publish.ui.head import *
from publish.ui.ui_main_window import ui_main_window

class Response(QtGui.QMainWindow):

    def __init__(self,parent=None,step="rigging"):
        super(Response,self).__init__(parent)
        self.setWindowTitle ("Beam_Publish_Tool")
        self.step = step
        self.setupUI()

    def setupUI(self):
        self.ui_main_window = ui_main_window()
        self.setCentralWidget(self.ui_main_window)

if __name__=="__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = Response()
    ui.show()
    sys.exit(app.exec_())
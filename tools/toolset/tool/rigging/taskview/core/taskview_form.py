# -*- coding: utf-8 -*-

import os
import sys
import functools
from rigging.taskview.ui.head import *
from rigging.taskview.ui.ui_main_window import ui_main_window

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

    def setupUI (self):
        self.ui_main_window = ui_main_window ()

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
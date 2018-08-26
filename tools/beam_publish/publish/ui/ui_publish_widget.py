#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import inspect
from head import *

class ui_publish_widget(QtWidgets.QWidget):

    def __init__(self,parent=None):
        super(ui_publish_widget,self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.mainVboxLayout = QtWidgets.QVBoxLayout(self)
        path = self.current_path()
        self.main_Widget = self.loadUiWidget(os.path.join(path,"publish_ui.ui"))
        self.mainVboxLayout.addWidget(self.main_Widget)
        #print dir(self.main_Widget)
        return self.main_Widget

    def current_path(self):
        path = os.path.realpath(sys.path[0])
        if os.path.isfile(path):
            path = os.path.dirname(path)
            return os.path.dirname(path)
        else:
            caller_file=inspect.stack()[1][1]
            return os.path.abspath(os.path.dirname(caller_file))

    def loadUiWidget(self,uifilename,parent=None):
        ui = QtCompat.load_ui(uifilename)
        return ui

if __name__ == "__main__":
    app = QtWidgets.QApplication (sys.argv)
    MainWindow = ui_publish_widget()
    MainWindow.show()
    sys.exit (app.exec_ ())
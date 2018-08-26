#!/usr/bin/env python
# -*- coding: utf-8 -*-

from head import *
import ui_piplinetool_widget
reload(ui_piplinetool_widget)
from ui_piplinetool_widget import ui_piplinetool_widget

class ui_main_window(QtWidgets.QWidget):

    def __init__(self,parent = None):
        super(ui_main_window,self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.ui_piplinetool_widget = ui_piplinetool_widget()
        #self.ui_taskview_widget.setupUi(self)
        QWidgetvboxLayout = QtWidgets.QVBoxLayout(self)
        QWidgetvboxLayout.addWidget(self.ui_piplinetool_widget)
        QWidgetvboxLayout.setContentsMargins(0,0,0,0)

if __name__=="__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = ui_main_window()
    ui.show()
    sys.exit(app.exec_())
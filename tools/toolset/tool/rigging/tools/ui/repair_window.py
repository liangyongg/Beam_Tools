#!/usr/bin/env python
# -*- coding: utf-8 -*-

from head import *
import repair_widget
reload(repair_widget)
from repair_widget import ui_repair_widget

class repair_window(QtGui.QDialog):

    def __init__(self,parent = None):
        super(repair_window,self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.ui_repair_widget = ui_repair_widget()
        #self.ui_taskview_widget.setupUi(self)
        QWidgetvboxLayout = QtGui.QVBoxLayout(self)
        QWidgetvboxLayout.addWidget(self.ui_repair_widget)
        QWidgetvboxLayout.setContentsMargins(0,0,0,0)

if __name__=="__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = repair_window()
    ui.show()
    sys.exit(app.exec_())
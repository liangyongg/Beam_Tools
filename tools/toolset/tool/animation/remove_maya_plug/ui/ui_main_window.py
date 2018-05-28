#!/usr/bin/env python
# -*- coding: utf-8 -*-

from head import *
import ui_removeplug_widget
reload(ui_removeplug_widget)
from ui_removeplug_widget import ui_removeplug_widget

class ui_main_window(QtGui.QWidget):

    def __init__(self,parent = None):
        super(ui_main_window,self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.ui_check_widget = ui_removeplug_widget()
        QWidgetvboxLayout = QtGui.QVBoxLayout(self)
        QWidgetvboxLayout.addWidget(self.ui_check_widget)
        QWidgetvboxLayout.setContentsMargins(0,0,0,0)

if __name__=="__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = ui_main_window()
    ui.show()
    sys.exit(app.exec_())
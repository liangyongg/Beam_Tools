#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rigging.tools.ui.head import *
import copyblendshape_widget
reload(copyblendshape_widget)
from copyblendshape_widget import copyblendshape_widget

class copyblendshape_window(QtGui.QDialog):

    def __init__(self,parent = None):
        super(copyblendshape_window,self).__init__(parent)
        self.setWindowTitle("Copy Blendshape")
        self.setupUi()

    def setupUi(self):
        self.copyblendshape_widget = copyblendshape_widget()
        #self.ui_taskview_widget.setupUi(self)
        QWidgetvboxLayout = QtGui.QVBoxLayout(self)
        QWidgetvboxLayout.addWidget(self.copyblendshape_widget)
        QWidgetvboxLayout.setContentsMargins(0,0,0,0)

if __name__=="__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = repair_window()
    ui.show()
    sys.exit(app.exec_())
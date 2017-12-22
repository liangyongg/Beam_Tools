# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.


# from PySide import QtCore, QtGui
from head import *
import os


# from PySide import QtCore, QtGui

class Item_form(QtGui.QWidget):
    """
    Implementation of the main publish UI
    """

    def __init__(self, parent=None):
        """
        Construction
        """
        QtGui.QWidget.__init__(self, parent)

        # set up the UI
        from ..ui.item_form import Ui_item_form
        self._ui = Ui_item_form()
        self._ui.setupUi(self)

        skip_icon = QtGui.QIcon()
        skip_icon.addFile(os.path.join(self.get_icon_path(), 'icons/clear_search.png'))
        correct_icon = QtGui.QIcon()
        correct_icon.addFile(os.path.join(self.get_icon_path(), 'icons/correct.png'))
        self._ui.item_icon.setPixmap(QtGui.QPixmap(os.path.join(self.get_icon_path(), 'icons/clock.png')))
        self._ui.item_icon.setScaledContents(True)
        self._ui.skip_btn.setIcon(skip_icon)
        self._ui.correct_btn.setIcon(correct_icon)
        self._ui.correct_btn.setVisible(0)

        self._ui.item_name.setText('')

    def get_icon_path(self):
        return os.path.dirname(os.path.dirname(__file__))

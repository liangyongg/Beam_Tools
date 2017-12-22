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


class Info_form(QtGui.QWidget):
    """
    Implementation of the main publish UI
    """

    def __init__(self, parent=None):
        """
        Construction
        """
        QtGui.QWidget.__init__(self, parent)
        self.sel_cmd = None
        # set up the UI
        from ..ui.info_form import Ui_info_form
        self._ui = Ui_info_form()
        self._ui.setupUi(self)
        self._ui.frame.setStyleSheet("QFrame{background-color:rgb(90,90,90);}")
        self._ui.info_text.setStyleSheet("QFrame{background-color:rgb(50,50,50);}")

        del_icon = QtGui.QIcon()
        del_icon.addFile(os.path.join(self.get_icon_path(), 'icons/clear_search.png'))
        sel_icon = QtGui.QIcon()
        sel_icon.addFile(os.path.join(self.get_icon_path(), 'icons/search.png'))
        self.expand_icon = QtGui.QIcon()
        self.expand_icon.addFile(os.path.join(self.get_icon_path(), 'icons/group_expand.png'))
        self.collapse_icon = QtGui.QIcon()
        self.collapse_icon.addFile(os.path.join(self.get_icon_path(), 'icons/group_collapse.png'))
        self._ui.expand_btn.setIcon(self.expand_icon)
        self._ui.del_btn.setIcon(del_icon)
        self._ui.sel_btn.setIcon(sel_icon)

        self._ui.info_text.setVisible(0)
        self._ui.sel_btn.setVisible(0)
        self._data = 0

        self._ui.expand_btn.clicked.connect(self._on_expand_btn_clicked)
        self._ui.obj_name.setStyleSheet('QLabel{color:red;font-size:12px; font-weight:bold;}')

    def _on_expand_btn_clicked(self):
        if self._data:
            self._ui.info_text.setVisible(0)
            self._ui.expand_btn.setIcon(self.expand_icon)
            self._data = 0
        else:
            self._ui.info_text.setVisible(1)
            self._ui.expand_btn.setIcon(self.collapse_icon)
            self._data = 1

    def get_icon_path(self):
        return os.path.dirname(os.path.dirname(__file__))


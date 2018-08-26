
from functools import partial
import pymel.core as pm

from rigging.beam.core.shifter.beam_components import guide
from rigging.beam.core import transform
from rigging.beam.ui.Qt import QtWidgets, QtGui, QtCore

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya.app.general.mayaMixin import MayaQDockWidget

import settingsUI as sui

# guide info
AUTHOR = "Jeremie Passerin, Miquel Campos"
URL = "www.jeremiepasserin.com, www.miquel-campos.com"
EMAIL = "geerem@hotmail.com, hello@miquel-campos.com"
VERSION = [1, 4, 0]
TYPE = "arm_02"
NAME = "arm"
DESCRIPTION = "2 bones arm with Maya nodes for roll bones. With elbow Pin"

##########################################################
# CLASS
##########################################################


class Guide(guide.ComponentGuide):

    """Component Guide Class"""
    compType = TYPE
    compName = NAME
    description = DESCRIPTION

    author = AUTHOR
    url = URL
    email = EMAIL
    version = VERSION
##########################################################
# Setting Page
##########################################################

class settingsTab(QtWidgets.QDialog, sui.Ui_Form):
    """The Component settings UI"""

    def __init__(self, parent=None):
        super(settingsTab, self).__init__(parent)
        self.setupUi(self)


class componentSettings(MayaQWidgetDockableMixin, guide.componentMainSettings):
    """Create the component setting window"""

    def __init__(self, parent=None):

        super(self.__class__, self).__init__(parent=parent)

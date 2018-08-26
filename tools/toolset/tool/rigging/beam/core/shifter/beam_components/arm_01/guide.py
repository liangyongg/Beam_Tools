
from functools import partial
import pymel.core as pm

from rigging.beam.core.shifter.beam_components import guide
from rigging.beam.core import transform
from rigging.beam.ui.Qt import QtWidgets, QtGui, QtCore

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya.app.general.mayaMixin import MayaQDockWidget

import settingsUI as sui

# guide info
AUTHOR = "Beam"
URL = "www.jeremiepasserin.com, www.miquel-campos.com"
EMAIL = "geerem@hotmail.com, hello@miquel-campos.com"
VERSION = [1, 4, 0]
TYPE = "arm_01"
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

    connectors = ["shoulder_01"]

    def postInit(self):
        """Initialize the position for the guide"""

        self.save_transform = ["root", "elbow", "wrist", "eff"]


    def addObjects (self):
        self.root = self.addRoot ()

        vTemp = transform.getOffsetPosition (self.root, [3, 0, -.01])
        self.elbow = self.addLoc ("elbow", self.root, vTemp)
        vTemp = transform.getOffsetPosition (self.root, [6, 0, 0])
        self.wrist = self.addLoc ("wrist", self.elbow, vTemp)
        vTemp = transform.getOffsetPosition (self.root, [7, 0, 0])
        self.eff = self.addLoc ("eff", self.wrist, vTemp)

        self.dispcrv = self.addDispCurve ("crv",[self.root, self.elbow, self.wrist, self.eff])

    def addParameters(self):
        """Add the configurations settings"""

        # Default Values
        self.pBlend = self.addParam("blend", "double", 1, 0, 1)
        self.pIkRefArray = self.addParam("ikrefarray", "string", "")
        self.pUpvRefArray = self.addParam("upvrefarray", "string", "")
        self.pUpvRefArray = self.addParam("pinrefarray", "string", "")
        self.pMaxStretch = self.addParam("maxstretch", "double", 1.5, 1, None)
        self.pIKTR = self.addParam("ikTR", "bool", False)
        self.pMirrorMid = self.addParam("mirrorMid", "bool", False)
        self.pMirrorIK = self.addParam("mirrorIK", "bool", False)
        self.pExtraTweak = self.addParam("extraTweak", "bool", False)

        # Divisions
        self.pDiv0 = self.addParam("div0", "long", 2, 1, None)
        self.pDiv1 = self.addParam("div1", "long", 2, 1, None)

        # FCurves
        self.pSt_profile = self.addFCurveParam("st_profile",[[0, 0], [.5, -.5], [1, 0]])
        self.pSq_profile = self.addFCurveParam("sq_profile",[[0, 0], [.5, .5], [1, 0]])

        self.pUseIndex = self.addParam("useIndex", "bool", False)
        self.pParentJointIndex = self.addParam("parentJointIndex","long",-1,None,None)

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

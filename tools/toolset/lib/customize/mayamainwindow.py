#!/usr/bin/env python
# -*- coding: utf-8 -*-

import maya.OpenMayaUI as OpenMayaUI
#from PyQt4 import QtWidgets,QtCore
from customize.head import *
try:
    import shiboken2
except:
    import shiboken

def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    try:
        warp = shiboken2.wrapInstance (long (ptr), QtWidgets.QWidget)
    except:
        warp = shiboken.wrapInstance (long (ptr), QtWidgets.QWidget)
    return warp
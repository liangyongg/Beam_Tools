import maya.OpenMayaUI as omui
import shiboken
import PySide.QtCore as QtCore,PySide.QtGui as QtGui

def edo_getMayaWindow():                                 
    ptr = omui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(ptr), QtGui.QWidget)
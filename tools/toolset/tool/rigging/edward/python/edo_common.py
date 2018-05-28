import maya.OpenMayaUI as omui
from headfile import *

def edo_getMayaWindow():                                 
    ptr = omui.MQtUtil.mainWindow()
    sipname=pyqtsip.__name__
    print sipname
    if sipname=='sip':
        inptr=pyqtsip.wrapinstance(long(ptr), QtCore.QObject)
        print inptr
        return inptr
    else:
        inptr=pyqtsip.wrapInstance(long(ptr), QtGui.QWidget)
        print inptr
        return inptr
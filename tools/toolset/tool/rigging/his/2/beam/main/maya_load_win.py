import sys

from rigging.beam.ui.Qt import QtWidgets, QtGui, QtCore
import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI
#from PyQt4 import QtGui,QtCore
try:
    import shiboken2
except:
    import shiboken

def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    try:
        warp = shiboken2.wrapInstance (long (ptr), QtGui.QWidget)
    except:
        warp = shiboken.wrapInstance (long (ptr), QtGui.QWidget)
    return warp

def MayaLoadWindow():
    for win in QtGui.QApplication.topLevelWidgets():
        if not hasattr(win,'isWindow'):
            continue
        if not win.isWindow():
            continue
        if win.windowTitle() == "Beam Editor":
            win.setParent(None)
            win.deleteLater()
    maya_win = getMayaWindow()
    beamWindow = ShowWindow(maya_win)
    return beamWindow

def ShowWindow(maya_win):
    from ..ui import beam_window as beam_window
    reload(beam_window)
    beamWindow = beam_window.BeamWindow(maya_win)
    beamWindow.show()
    return beamWindow

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    ui = ShowWindow()
    sys.exit(app.exec_())
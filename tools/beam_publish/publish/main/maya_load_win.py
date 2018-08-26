import sys
sys.path.append(r"E:\Beam_tools\tools\beam_publish")

from publish.ui.head import *
import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI
#from PyQt4 import QtWidgets,QtCore
try:
    import shiboken2
except:
    import shiboken

def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    try:
        warp = shiboken2.wrapInstance (long (ptr), QWidget)
    except:
        warp = shiboken.wrapInstance (long (ptr), QWidget)
    return warp

def MayaLoadWindow(step="mod"):
    for win in QApplication.topLevelWidgets():
        if not hasattr(win,'isWindow'):
            continue
        if not win.isWindow():
            continue
        if win.windowTitle() == "Beam_Publish_Tool":
            win.setParent(None)
            win.deleteLater()
    maya_win = getMayaWindow()
    beamWindow = ShowWindow(maya_win,step)
    return beamWindow

def ShowWindow(maya_win,step):
    import publish.core.response as response
    reload(response)
    beamWindow = response.Response(maya_win,step)
    beamWindow.show()
    return beamWindow

if __name__=="__main__":
    import sys
    app = QApplication(sys.argv)
    ui = ShowWindow()
    sys.exit(app.exec_())
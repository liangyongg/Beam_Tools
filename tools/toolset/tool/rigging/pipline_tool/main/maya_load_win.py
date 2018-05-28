import sys
sys.path.append(r"E:\Beam_tools\tools\toolset\tool")

from ..ui.head import *
import maya.cmds as cmds
from customize.mayamainwindow import getMayaWindow

def MayaLoadWindow(step=""):
    for win in QtGui.QApplication.topLevelWidgets():
        if not hasattr(win,'isWindow'):
            continue
        if not win.isWindow():
            continue
        if win.windowTitle() == "rigging_pipline_tool":
            win.setParent(None)
            win.deleteLater()
    maya_win = getMayaWindow()
    beamWindow = ShowWindow(maya_win)
    return beamWindow

def ShowWindow(maya_win,step=""):
    from ..core import pipline_form
    reload(pipline_form)
    beamWindow = pipline_form.From(maya_win)
    beamWindow.show()
    return beamWindow

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    ui = ShowWindow()
    sys.exit(app.exec_())
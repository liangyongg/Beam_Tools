import maya.cmds as cmds
import maya.mel as mel
import edo_autoConnectBlendshapesInbetweenUI.edo_mirrorBlendShape as edo_mirrorBlendShape
import edo_autoConnectBlendshapesInbetweenUI.edo_autoConnectBlendShapes as edo_autoConnectBlendShapes

def edo_connectBlendShapeAsName():
    sels=cmds.ls(sl=1)
    for sel in sels:
        #sel=sels[1]
        tmp=sel.split('__')
        frame=tmp[-1]
        if cmds.objExists(frame):
            ctrl=frame.split('_CTRL')[0]+'_CTRL'
            cmds.parent(sel,frame)
            if cmds.objExists(ctrl):
                cmds.select(ctrl,r=1)
                allbms=edo_autoConnectBlendShapes.edo_autoConnectBlendshapes()
                if cmds.objExists(sel):
                    cmds.delete(sel)
                else:
                    rsel=tmp[0]+'__'+tmp[1]+'__'+tmp[3]
                    if cmds.objExists(rsel):
                        cmds.delete(rsel)
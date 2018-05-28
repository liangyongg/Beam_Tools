import maya.cmds as cmds
import maya.OpenMaya as om

#mattr=edo_unLockReferenceObjectTransformAttrs("reflock:pSphere1")
def edo_unLockReferenceObjectTransformAttrs(object):
    #object="aa:pSphere1";
    msl=om.MSelectionList()
    mgb=om.MGlobal()
    mgb.getSelectionListByName(object,msl)
    #msl.length()
    mobj=om.MObject()
    msl.getDependNode(0,mobj)
    #mobj.apiTypeStr()
    mdn=om.MFnDependencyNode(mobj)
    mtx=mdn.findPlug('translateX')
    mtx.setLocked(0)
    mtx.setKeyable(1)
    mty=mdn.findPlug('translateY')
    mty.setLocked(0)
    mty.setKeyable(1)
    mtz=mdn.findPlug('translateZ')
    mtz.setLocked(0)
    mtz.setKeyable(1)
    mrx=mdn.findPlug('rotateX')
    mrx.setLocked(0)
    mrx.setKeyable(1)
    mry=mdn.findPlug('rotateY')
    mry.setLocked(0)
    mry.setKeyable(1)
    mrz=mdn.findPlug('rotateZ')
    mrz.setLocked(0)
    mrz.setKeyable(1)
    msx=mdn.findPlug('scaleX')
    msx.setLocked(0)
    msx.setKeyable(1)
    msy=mdn.findPlug('scaleY')
    msy.setLocked(0)
    msy.setKeyable(1)
    msz=mdn.findPlug('scaleZ')
    msz.setLocked(0)
    msz.setKeyable(1)
    mv=mdn.findPlug('visibility')
    mv.setLocked(0)
    mv.setKeyable(1)
    return [mtx,mty,mtz,mrx,mry,mrz,msx,msy,msz,mv]

#list=edo_getTransformAttrList("reflock:pSphere1")
def edo_getTransformAttrList(object):
    #object="pSphere1"
    locks=[
    cmds.getAttr(object+'.tx',l=1),cmds.getAttr(object+'.ty',l=1),cmds.getAttr(object+'.tz',l=1),
    cmds.getAttr(object+'.rx',l=1),cmds.getAttr(object+'.ry',l=1),cmds.getAttr(object+'.rz',l=1),
    cmds.getAttr(object+'.sx',l=1),cmds.getAttr(object+'.sy',l=1),cmds.getAttr(object+'.sz',l=1),
    cmds.getAttr(object+'.v',l=1)
    ]
    keys=[
    cmds.getAttr(object+'.tx',k=1),cmds.getAttr(object+'.ty',k=1),cmds.getAttr(object+'.tz',k=1),
    cmds.getAttr(object+'.rx',k=1),cmds.getAttr(object+'.ry',k=1),cmds.getAttr(object+'.rz',k=1),
    cmds.getAttr(object+'.sx',k=1),cmds.getAttr(object+'.sy',k=1),cmds.getAttr(object+'.sz',k=1),
    cmds.getAttr(object+'.v',k=1)
    ]
    return [locks,keys]

#edo_unlockTransformAsList(mattr,list)
def edo_unlockTransformAsList(mattr,list):
    #list
    ln=len(list[0])
    for i in range(0,ln):
        #i=0
        if list[0][i]==True:
            mattr[i].setLocked(1)
        else:
            mattr[i].setLocked(0)
    kn=len(list[1])
    for i in range(0,kn):
        #i=0
        if list[1][i]==False:
            mattr[i].setKeyable(0)
        else:
            mattr[i].setKeyable(1)
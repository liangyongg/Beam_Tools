import maya.cmds as cmds
import edo_general as edo_general
import edo_general.edo_loadPlugin as ELPLUGIN
import edo_general.edo_lockAndUnlockTransform as edo_lockAndUnlockTransform
import edo_autoConnectBlendshapesInbetweenUI.edo_mathBlendShapeUI as edo_mathBlendShapeCmd;reload(edo_mathBlendShapeCmd)

#reload(edo_autoConnectBlendShapes)
mllpath=edo_general.__file__.replace('python\\edo_general\\__init__.pyc','mll').replace('\\','/')

#fbs=edo_calculateBlendShape(cmds.ls(sl=1)[0],cmds.ls(sl=1)[1],0,True)
def edo_calculateBlendShape(target,skmesh,method=2,ignoreBlendShapeEffect=True):
    #target=cmds.ls(sl=1)[0]
    #skmesh=cmds.ls(sl=1)[1]
    #ignoreBlendShapeEffect=False
    #load plugin
    ELPLUGIN.edo_loadPlugin('geometryComputer.mll')
    sk=edo_findNodeFromHis(skmesh,'skinCluster')
    tw=edo_findNodeFromHis(skmesh,'tweak')
    bs=edo_findNodeFromHis(skmesh,'blendShape')
    tm=cmds.duplicate(skmesh,n='CALCULATE_BLENDSHAPE_TARGETMESH')[0]
    sh=cmds.listRelatives(tm,s=1,pa=1,ni=1)
    cmds.delete(sh)
    org=cmds.listRelatives(tm,s=1,pa=1)[0]
    osh=cmds.rename(org,tm+'Shape')
    cmds.setAttr(osh+'.io',0)
    if method==0:
        try:
            temp=cmds.duplicate(tm)[0]
            gcnode=edo_mathBlendShapeCmd.edo_mathBlendShape(temp,tm,target,skmesh,'-','','')
            cmds.delete(temp)
        except:
            print 'calculate blendshape has been failed,please check the result.'
            cmds.delete(tm)
    if method==2:
        #turnOff blendShape
        bsst=None
        if ignoreBlendShapeEffect==True:
            try:
                bsst=cmds.getAttr(bs+'.nodeState')
                cmds.setAttr(bs+'.nodeState',1)
            except:
                print 'turn off the blendShape effect has been failed,please check the result.'
        try:
            gcnode=edo_mathBlendShapeCmd.edo_mathBlendShape('',tm,target,'','SkinCluster_inverse',tw,sk)
        except:
            print 'calculate blendshape has been failed,please check the result.'
            cmds.delete(tm)
            try:
                cmds.setAttr(bs+'.nodeState',bsst)
            except:
                print 'turn off the blendShape effect has failed,please check the result.'
            return False
        try:
            if not bsst==None:
                cmds.setAttr(bs+'.nodeState',bsst)
        except:
            print 'turn off the blendShape effect has failed,please check the result.'
    finalbs=cmds.duplicate(tm)[0]
    cmds.delete(tm)
    edo_lockAndUnlockTransform.edo_unLockReferenceObjectTransformAttrs(finalbs)
    return finalbs
    
def edo_findNodeFromHis(name,type):
    #name=skmesh
    #type='blendShape'
    nodes=[]
    hiss=cmds.listHistory(name,pruneDagObjects=1,groupLevels=1)
    if not hiss==None:
        for his in hiss:
            if cmds.nodeType(his)==type:
                nodes.append(his)
    if nodes and not nodes==[]:
        return nodes[0]
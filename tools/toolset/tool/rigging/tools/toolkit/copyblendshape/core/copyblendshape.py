# -*- coding: utf-8 -*-

import maya.cmds as cmds
import pymel.core as pm

def copyBlendShape(sourceobj,destobj,sourcebs,allTransferState=1,transferAttrList=[],*args):
    destObj_warpGeo = cmds.duplicate(destobj,n='%s_warpGeo' % (destobj),rr=1)[0]
    cmds.select(destObj_warpGeo,sourceobj,r=1)
    warpNode = pm.mel.eval('doWrapArgList "5" {"1","0.02","1","2","1","1"};')[0]
    print warpNode

    bsAttrList = cmds.listAttr("%s.w" % (sourcebs),m=1)

    bsAttrList = [i for i in bsAttrList if not i.startswith('weight[')]
    attrWeightList = cmds.aliasAttr(sourcebs,q=1)
    weightIndexList = []
    for bsAttr in bsAttrList:
        index = attrWeightList.index(bsAttr)
        weightIndx = int(attrWeightList[index+1].split('[')[1].split(']')[0])
        weightIndexList.append(weightIndx)

    destBS = destobj+"_BS"
    targetList = []
    bsCreateState = 0
    weightNum = 0
    for i in xrange(len(bsAttrList)):
        if not allTransferState:
            if bsAttrList[i] not in transferAttrList:
                continue
        sourceAttr = ''
        lockState = 0
        originalValue = cmds.getAttr("%s.%s" % (sourcebs,bsAttrList[i]))
        weightNum+=1
        print "Add the %s few goals"%weightNum,bsAttrList[i]

        if cmds.connectionInfo("%s.%s" % (sourcebs,bsAttrList[i]),isDestination=1):
            sourceAttr = cmds.listConnections("%s.%s" %(sourcebs,bsAttrList[i]),d=0,s=1,plugs=1)[0]
            cmds.disconnectAttr(sourceAttr,"%s.%s" % (sourcebs,bsAttrList[i]))
        if cmds.getAttr("%s.%s" % (sourcebs,bsAttrList[i]),lock=1):
            cmds.getAttr("%s.%s" % (sourcebs,bsAttrList[i]),lock=0)
            lockState=1

        cmds.setAttr("%s.%s" % (sourcebs,bsAttrList[i]),1)
        targetFull = cmds.duplicate(destObj_warpGeo,n = bsAttrList[i],rr=1)[0]
        targetList.append(targetFull)
        if bsCreateState==0:
            destBS = cmds.blendShape(targetFull,destobj,n=destBS,foc=1)[0]
            bsCreateState=1
        else:
            future_weightCount = pm.PyNode(destBS).weightIndexList()[-1]+1
            cmds.blendShape(destBS,e=1,t=(destobj,future_weightCount,targetFull,1.0))

        targetNumberList = cmds.getAttr("%s.inputTarget[0].inputTargetGroup[%s].inputTargetItem" % (sourcebs,weightIndexList[i]),mi=1)
        print "\t%3s" % i,"%40s" % bsAttrList[i],"weight :","%3s" % weightIndexList[i],targetNumberList
        if targetNumberList:
            if len(targetNumberList)>1:
                for n in xrange(len(targetNumberList)-1):
                    inbetweenValue = (targetNumberList[n]-5000)/1000.0
                    print "\tinbetweenValue --- >",inbetweenValue
                    cmds.setAttr("%s.%s" % (sourcebs,attrWeightList[i]),inbetweenValue)
                    targetInbetweenGeo = cmds.duplicate(destObj_warpGeo,rr=1,rc=1,n=destobj+"_inbetween")[0]
                    targetList.append(targetInbetweenGeo)
                    now_weightCount = pm.PyNode(destBS).weightIndexList()[-1]
                    cmds.blendShape(destBS,e=1,ib=1,t=(destobj,now_weightCount,targetInbetweenGeo,inbetweenValue))

        cmds.setAttr("%s.%s" % (sourcebs,bsAttrList[i]),originalValue)
        cmds.setAttr("%s.%s" % (destBS,targetFull),originalValue)

        if sourceAttr:
            cmds.connectAttr(sourceAttr,"%s.%s" % (sourcebs,bsAttrList[i]),lock=1)
            cmds.connectAttr(sourceAttr,"%s.%s" % (destBS,targetFull),lock=1)
        if lockState:
            cmds.setAttr("%s.%s" % (sourcebs,bsAttrList[i]),lock=1)
            cmds.setAttr("%s.%s" % (destBS,targetFull),lock=1)
    cmds.delete(targetList,destObj_warpGeo)
    print targetList,destObj_warpGeo

def getBlendShapeNode(obj):
    bsNode = ''
    objShape = cmds.listRelatives(obj,c=1,s=1,ni=1)[0]
    relatedObjectSetList = cmds.listConnections(objShape,d=1,s=0,type='objectSet')
    for objset in relatedObjectSetList:
        objsets = cmds.listConnections(objset,d=0,s=1,type='blendShape')
        if objsets:
            bsNode = cmds.listConnections(objset,d=0,s=1,type='blendShape')[0]
            break
    if not bsNode:
        raise Exception("%s not have blendshape node !")
    return bsNode
import maya.cmds as cmds
import maya.OpenMaya as om
#edo_projectLocOnCurve(loc,cv,tolerence=1.0e-3)
def edo_projectLocOnCurve(loc,cv,tolerence=1.0e-3):
    #tolerence=1.0e-4
    #loc='locator1'
    #cv='curve1'
    locpo=cmds.xform(loc,q=1,ws=1,t=1)
    locx=locpo[0]
    cvshape=cmds.listRelatives(cv,s=1,pa=1)[0]
    lencv=cmds.getAttr(cvshape+'.spans')+cmds.getAttr(cvshape+'.degree')
    stpointx=cmds.xform(cvshape+'.cv[0]',q=1,ws=1,t=1)[0]
    edpointx=cmds.xform(cvshape+'.cv['+str(lencv-1)+']',q=1,ws=1,t=1)[0]
    sted=cmds.getAttr(cvshape+'.minMaxValue')[0]
    st=sted[0]
    ed=sted[1]
    ct=edo_getClosestPointOnCurve(locpo,cvshape,'yz')
    if locx<min(edpointx,stpointx) or locx>max(edpointx,stpointx):
        ct=[st,stpointx]
        if abs(stpointx-locx)>abs(edpointx-locx):
            ct=[ed,edpointx]
        pjpt=edo_getPointFromParam(ct[0],cvshape)
        #print '====result===='
        #print pjpt
        cmds.spaceLocator(p=[pjpt[1][0],pjpt[1][1],pjpt[1][2]])
        cmds.select(loc,r=1)
        return ct
    dis=abs(pp[1]-locpo[0])
    closeparam=-1.0
    i=0
    lpp=ct
    mi=[0,stpointx]
    mx=[ed,edpointx]
    while dis>tolerence:
    #if 1==1:
        #lpp=nearest
        if mi[1]<=min(ct[1],lpp[1])<=locx:
            mi=ct
            if lpp[1]<=ct[1]:
                mi=lpp
        if mx[1]>max(ct[1],lpp[1])>=locx:
            mx=ct
            if lpp[1]>=ct[1]:
                mx=lpp
        tmp=min(mi[0],mx[0])+(abs(mi[0]-mx[0])/2)
        npp=edo_getPointFromParam(tmp,cvshape)
        dis=abs(npp[1][0]-locpo[0])
        lpp=ct
        ct=[npp[0],npp[1][0]]
        print 'it time:'+str(i)
        #print dis
        #print ct[0]
        i=i+1
        if i>100:
            dis=0.0
    pjpt=edo_getPointFromParam(ct[0],cvshape)
    #print '====result===='
    #print pjpt
    cmds.spaceLocator(p=[pjpt[1][0],pjpt[1][1],pjpt[1][2]])
    cmds.select(loc,r=1)
    return pjpt

def edo_getPointFromParam(param,cv):
    #param=pp[0]
    #cv=cvshape
    mg=om.MGlobal()
    mg.selectByName(cv,mg.kReplaceList)
    msl=om.MSelectionList()
    mg.getActiveSelectionList(msl)
    #msl.length()
    cvobj=om.MObject()
    cvpath=om.MDagPath()
    msl.getDependNode(0,cvobj)
    msl.getDagPath(0,cvpath)
    mfnCv=om.MFnNurbsCurve(cvpath)
    pt=om.MPoint()
    mfnCv.getPointAtParam(param,pt,4)
    ms=om.MScriptUtil()
    closeparam=ms.asDoublePtr() 	
    closeParam=mfnCv.getParamAtPoint(pt,closeparam,4)
    #cmds.spaceLocator(p=[pt[0],pt[1],pt[2]])
    return [ms.getDouble(closeparam),[pt[0],pt[1],pt[2]]]
    
def edo_getClosestPointOnCurve(point,cv,ProjectPlane='yz'):
    #cv=cv+'Shape'
    #point=locpo
    mg=om.MGlobal()
    mg.selectByName(cv,mg.kReplaceList)
    msl=om.MSelectionList()
    mg.getActiveSelectionList(msl)
    #msl.length()
    cvobj=om.MObject()
    cvpath=om.MDagPath()
    msl.getDependNode(0,cvobj)
    msl.getDagPath(0,cvpath)
    #cvobj.apiTypeStr()
    mfnCv=om.MFnNurbsCurve(cvpath)
    closePoint=mfnCv.closestPoint(om.MPoint(point[0],point[1],point[2]),None,1.0e-3,4)
    #print str(closePoint[0])+str(closePoint[1])+str( closePoint[2])
    ms=om.MScriptUtil()
    param=ms.asDoublePtr() 	
    closeParam=mfnCv.getParamAtPoint(closePoint,param,4)
    if ProjectPlane=='yz':
        #cmds.spaceLocator(p=[closePoint[0],closePoint[1],closePoint[2]])
        return [ms.getDouble(param),closePoint[0]]
import maya.cmds as cmds
import maya.OpenMaya as om


#mg=om.MGlobal()
#mg.selectByName('curveShape1',mg.kReplaceList)
#msl=om.MSelectionList()
#mg.getActiveSelectionList(msl)
#msl.length()
#cvobj=om.MObject()
#cvpath=om.MDagPath()
#msl.getDependNode(0,cvobj)
#msl.getDagPath(0,cvpath)

#self=edo_MFnNurbsCurve(cvpath)
#for i in range(0,1000):
#    rs=self.getParamAndPointFromProjectPoint([i*0.01,0,0],0)
#print 'done'

class edo_MFnNurbsCurve(om.MFnNurbsCurve):
    
    MCurveObj=None
    MFnCurve=None
    
    def __init__(self,MCurveObj=None):
        #MCurveObj=cvobj
        print 'create edo_MFnNurbsCurve'
        print MCurveObj
        if MCurveObj:
            print 'api type'
            print MCurveObj.apiType()
            if MCurveObj.apiType()==266:
                print 'nurbsCurve'
                self.MCurveObj=MCurveObj
                self.MFnCurve=om.MFnNurbsCurve(self.MCurveObj)
            
    def getParamAndPointFromProjectPoint(self,locpo,showResult=0,tolerence=1.0e-3):
        #tolerence=1.0e-4
        #loc='locator1'
        #cv='curve1'
        #locpo=cmds.xform(loc,q=1,ws=1,t=1)
        locx=locpo[0]
        cvshape=self.MCurveObj.partialPathName()
        #print cvshape
        lencv=cmds.getAttr(cvshape+'.spans')+cmds.getAttr(cvshape+'.degree')
        stpointx=cmds.xform(cvshape+'.cv[0]',q=1,ws=1,t=1)[0]
        edpointx=cmds.xform(cvshape+'.cv['+str(lencv-1)+']',q=1,ws=1,t=1)[0]
        sted=cmds.getAttr(cvshape+'.minMaxValue')[0]
        st=sted[0]
        ed=sted[1]
        ct=self.getClosestPointOnCurve(locpo,'x')
        if locx<min(edpointx,stpointx) or locx>max(edpointx,stpointx):
            ct=[st,stpointx]
            if abs(stpointx-locx)>abs(edpointx-locx):
                ct=[ed,edpointx]
            pjpt=self.getClosestPointAndParamFloatAtParam(ct[0])
            #print '====result===='
            #print pjpt
            if showResult==1:
                cmds.spaceLocator(p=[pjpt[1][0],pjpt[1][1],pjpt[1][2]])
            return ct
        dis=abs(ct[1]-locpo[0])
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
            npp=self.getClosestPointAndParamFloatAtParam(tmp)
            dis=abs(npp[1][0]-locpo[0])
            lpp=ct
            ct=[npp[0],npp[1][0]]
            #if showResult==1:
            #    print 'it time:'+str(i)
            #print dis
            #print ct[0]
            i=i+1
            if i>100:
                dis=0.0
        pjpt=self.getClosestPointAndParamFloatAtParam(ct[0])
        #print '====result===='
        #print pjpt
        if showResult==1:
            cmds.spaceLocator(p=[pjpt[1][0],pjpt[1][1],pjpt[1][2]])
        return pjpt

    def getClosestPointAndParamFloatAtParam(self,param):
        pt=om.MPoint()
        self.MFnCurve.getPointAtParam(param,pt,4)
        ms=om.MScriptUtil()
        closeparam=ms.asDoublePtr() 	
        closeParam=self.MFnCurve.getParamAtPoint(pt,closeparam,4)
        #cmds.spaceLocator(p=[pt[0],pt[1],pt[2]])
        return [ms.getDouble(closeparam),[pt[0],pt[1],pt[2]]]
    
    def getClosestPointOnCurve(self,point,ProjectPlane='x'):
        #cv=cv+'Shape'
        #point=locpo
        closePoint=self.MFnCurve.closestPoint(om.MPoint(point[0],point[1],point[2]),None,1.0e-3,4)
        #print str(closePoint[0])+str(closePoint[1])+str( closePoint[2])
        ms=om.MScriptUtil()
        param=ms.asDoublePtr() 	
        closeParam=self.MFnCurve.getParamAtPoint(closePoint,param,4)
        if ProjectPlane=='x':
            #cmds.spaceLocator(p=[closePoint[0],closePoint[1],closePoint[2]])
            return [ms.getDouble(param),closePoint[0]]
import maya.cmds as cmds
#edo_addFacialCtrlCmd('test','',1,'_CONNECT')
def edo_addFacialCtrlCmd(ctrlName,parent='',onlyFrame=0,sfix='_CTRL'):
    #ctrlName='test'
    #sfix='_CONNECT'
    #parent=''
    print ctrlName
    if cmds.objExists(ctrlName+'_FRAME'):
        cmds.confirmDialog( title='Confirm', message=ctrlName+sfix + ' .. has already existed in this scene!', button=['got it'] )
        return False
    curve=cmds.curve(d=1,p=[(-1,1,0),(-1,-1,0),(1,-1,0),(1,1,0),(-1,1,0)],k=[0,1,2,3,4])
    curve_zy=cmds.curve(d=1,p=[(-1,0.2,0),(-1,-1,0),(1,-1,0),(1,0.2,0),(-1,0.2,0)],k=[0,1,2,3,4])
    curve_fy=cmds.curve(d=1,p=[(-1,1,0),(-1,-0.2,0),(1,-0.2,0),(1,1,0),(-1,1,0)],k=[0,1,2,3,4])
    curve_zx=cmds.curve(d=1,p=[(-1,1,0),(-1,-1,0),(0.2,-1,0),(0.2,1,0),(-1,1,0)],k=[0,1,2,3,4])
    curve_fx=cmds.curve(d=1,p=[(-0.2,1,0),(-0.2,-1,0),(1,-1,0),(1,1,0),(-0.2,1,0)],k=[0,1,2,3,4])
    curve_zyfy=cmds.curve(d=1,p=[(-1,0.2,0),(-1,-0.2,0),(1,-0.2,0),(1,0.2,0),(-1,0.2,0)],k=[0,1,2,3,4])
    curve_zxfx=cmds.curve(d=1,p=[(-0.2,1,0),(-0.2,-1,0),(0.2,-1,0),(0.2,1,0),(-0.2,1,0)],k=[0,1,2,3,4])
    curve_zyfyfx=cmds.curve(d=1,p=[(-0.2,0.2,0),(-0.2,-0.2,0),(1,-0.2,0),(1,0.2,0),(-0.2,0.2,0)],k=[0,1,2,3,4])
    curve_zyfyzx=cmds.curve(d=1,p=[(-1,0.2,0),(-1,-0.2,0),(0.2,-0.2,0),(0.2,0.2,0),(-1,0.2,0)],k=[0,1,2,3,4])
    curve_zxfxfy=cmds.curve(d=1,p=[(-0.2,1,0),(-0.2,-0.2,0),(0.2,-0.2,0),(0.2,1,0),(-0.2,1,0)],k=[0,1,2,3,4])
    curve_zxfxzy=cmds.curve(d=1,p=[(-0.2,0.2,0),(-0.2,-1,0),(0.2,-1,0),(0.2,0.2,0),(-0.2,0.2,0)],k=[0,1,2,3,4])
    cmds.rename(curve,ctrlName+'_FRAME')
    cmds.rename(curve_zy,ctrlName+'_FRAME_lockzy')
    cmds.rename(curve_fy,ctrlName+'_FRAME_lockfy')
    cmds.rename(curve_zx,ctrlName+'_FRAME_lockzx')
    cmds.rename(curve_fx,ctrlName+'_FRAME_lockfx')
    cmds.rename(curve_zyfy,ctrlName+'_FRAME_lockzyfy')
    cmds.rename(curve_zxfx,ctrlName+'_FRAME_lockzxfx')
    cmds.rename(curve_zyfyfx,ctrlName+'_FRAME_lockzyfyfx')
    cmds.rename(curve_zyfyzx,ctrlName+'_FRAME_lockzyfyzx')
    cmds.rename(curve_zxfxzy,ctrlName+'_FRAME_lockzxfxzy')
    cmds.rename(curve_zxfxfy,ctrlName+'_FRAME_lockzxfxfy')
    allframe=[ctrlName+'_FRAME',ctrlName+'_FRAME_lockzy',ctrlName+'_FRAME_lockfy',ctrlName+'_FRAME_lockzx',ctrlName+'_FRAME_lockfx',ctrlName+'_FRAME_lockzyfy',ctrlName+'_FRAME_lockzxfx',ctrlName+'_FRAME_lockzyfyzx',ctrlName+'_FRAME_lockzyfyfx',ctrlName+'_FRAME_lockzxfxzy',ctrlName+'_FRAME_lockzxfxfy',]
    cmds.addAttr(ctrlName+'_FRAME',ln='up',at='double',min=0)
    cmds.setAttr(ctrlName+'_FRAME.up',keyable=1)
    cmds.addAttr(ctrlName+'_FRAME',ln='dn',at='double',min=0)
    cmds.setAttr(ctrlName+'_FRAME.dn',keyable=1)
    cmds.addAttr(ctrlName+'_FRAME',ln='lf',at='double',min=0)
    cmds.setAttr(ctrlName+'_FRAME.lf',keyable=1)
    cmds.addAttr(ctrlName+'_FRAME',ln='rt',at='double',min=0)
    cmds.setAttr(ctrlName+'_FRAME.rt',keyable=1)
    cmds.addAttr(ctrlName+'_FRAME',ln='lfup',at='double',min=0)
    cmds.setAttr(ctrlName+'_FRAME.lfup',keyable=1)
    cmds.addAttr(ctrlName+'_FRAME',ln='rtup',at='double',min=0)
    cmds.setAttr(ctrlName+'_FRAME.rtup',keyable=1)
    cmds.addAttr(ctrlName+'_FRAME',ln='lfdn',at='double',min=0)
    cmds.setAttr(ctrlName+'_FRAME.lfdn',keyable=1)
    cmds.addAttr(ctrlName+'_FRAME',ln='rtdn',at='double',min=0)
    cmds.setAttr(ctrlName+'_FRAME.rtdn',keyable=1)
    cmds.addAttr(ctrlName+'_FRAME',ln='fourAxis_up',at='double',min=0)
    cmds.setAttr(ctrlName+'_FRAME.fourAxis_up',keyable=1)
    cmds.addAttr(ctrlName+'_FRAME',ln='fourAxis_dn',at='double',min=0)
    cmds.setAttr(ctrlName+'_FRAME.fourAxis_dn',keyable=1)
    cmds.addAttr(ctrlName+'_FRAME',ln='fourAxis_lf',at='double',min=0)
    cmds.setAttr(ctrlName+'_FRAME.fourAxis_lf',keyable=1)
    cmds.addAttr(ctrlName+'_FRAME',ln='fourAxis_rt',at='double',min=0)
    cmds.setAttr(ctrlName+'_FRAME.fourAxis_rt',keyable=1)
    #
    cmds.addAttr(ctrlName+'_FRAME',ln='curveType',dt='string')
    cmds.setAttr(ctrlName+'_FRAME.curveType',sfix,type='string')
    cmds.setAttr(ctrlName+'_FRAME.curveType',e=1,l=1)
    #
    cmds.createNode('transform',n='GRP_'+ctrlName+'_FRAME')
    cmds.parent(allframe,'GRP_'+ctrlName+'_FRAME')
    curve=cmds.curve(d=1,p=[(-1,1,0),(-1,3,0),(-2,3,0),(0,5,0),(2,3,0),(1,3,0),(1,1,0),(4,4,0),(1,1,0),(3,1,0),(3,2,0),(5,0,0),(3,-2,0),(3,-1,0),(1,-1,0),(4,-4,0),(1,-1,0),(1,-3,0),(2,-3,0),(0,-5,0),(-2,-3,0),(-1,-3,0),(-1,-1,0),(-4,-4,0),(-1,-1,0),(-3,-1,0),(-3,-2,0),(-5,0,0),(-3,2,0),(-3,1,0),(-1,1,0),(-4,4,0),(-1,1,0)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32])
    cmds.rename(curve,ctrlName+sfix)
    cmds.setAttr(ctrlName+sfix+'Shape.overrideEnabled',1)
    cmds.setAttr(ctrlName+sfix+'Shape.ovc',17)
    cmds.setAttr(ctrlName+sfix+'.sx',0.05)
    cmds.setAttr(ctrlName+sfix+'.sy',0.05)
    cmds.setAttr(ctrlName+sfix+'.sy',0.05)
    cmds.transformLimits(ctrlName+sfix,etx=(1,1),tx=(-1,1))
    cmds.transformLimits(ctrlName+sfix,ety=(1,1),ty=(-1,1))
    cmds.transformLimits(ctrlName+sfix,etz=(1,1),tz=(0,0))
    cmds.makeIdentity(ctrlName+sfix,apply=1,t=1,r=1,s=1,n=0)
    cmds.group(ctrlName+sfix,n='GRP_'+ctrlName+sfix,p=ctrlName+'_FRAME')
    ##==================

    #=======addReferenceAttribute=======
    cmds.addAttr(ctrlName+sfix,ln='frameSelectAble',at='enum',en='normal:template:reference:')
    cmds.setAttr(ctrlName+sfix+'.frameSelectAble',e=1,k=0,cb=0)
    cmds.setAttr(ctrlName+sfix+'.frameSelectAble',2)
    for frame in allframe:
        #frame=allframe[0]
        cmds.setAttr(frame+'Shape.overrideEnabled',1)
        cmds.connectAttr(ctrlName+sfix+'.frameSelectAble',frame+'Shape.overrideDisplayType',f=1)
        if not frame==ctrlName+'_FRAME':
            cmds.parent(frame,ctrlName+'_FRAME')
    
    if not parent=='':
        cmds.parent('GRP_'+ctrlName+'_FRAME',parent)
    cmds.select(cl=1)
    edo_addAttrBoundaryBox(ctrlName,sfix)
    
    if onlyFrame==1:
        return True
    cmds.createNode('multiplyDivide',n=ctrlName+'_upmult_Xinverse')
    cmds.connectAttr(ctrlName+sfix+'.tx',ctrlName+'_upmult_Xinverse.input2X',f=1)
    cmds.setAttr(ctrlName+'_upmult_Xinverse.input1X',-1)
    cmds.createNode('clamp',n=ctrlName+'_upclamp_PXrange')
    cmds.connectAttr(ctrlName+'_upmult_Xinverse.outputX',ctrlName+'_upclamp_PXrange.inputR',f=1)
    cmds.setAttr(ctrlName+'_upclamp_PXrange.minR',0)
    cmds.setAttr(ctrlName+'_upclamp_PXrange.maxR',1)
    cmds.createNode('clamp',n=ctrlName+'_upclamp_NXrange')
    cmds.connectAttr(ctrlName+sfix+'.tx',ctrlName+'_upclamp_NXrange.inputR',f=1)
    cmds.setAttr(ctrlName+'_upclamp_NXrange.minR',0)
    cmds.setAttr(ctrlName+'_upclamp_NXrange.maxR',1)
    cmds.createNode('plusMinusAverage',n=ctrlName+'_upplus_Xplus')
    cmds.connectAttr(ctrlName+'_upclamp_NXrange.outputR',ctrlName+'_upplus_Xplus.input1D[0]',f=1)
    cmds.connectAttr(ctrlName+'_upclamp_PXrange.outputR',ctrlName+'_upplus_Xplus.input1D[1]',f=1)
    cmds.createNode('reverse',n=ctrlName+'_upreverse_X')
    cmds.connectAttr(ctrlName+'_upplus_Xplus.output1D',ctrlName+'_upreverse_X.inputX',f=1)
    cmds.createNode('clamp',n=ctrlName+'_upclamp_PYrange')
    cmds.connectAttr(ctrlName+sfix+'.ty',ctrlName+'_upclamp_PYrange.inputR',f=1)
    cmds.setAttr(ctrlName+'_upclamp_PYrange.minR',0)
    cmds.setAttr(ctrlName+'_upclamp_PYrange.maxR',1)
    cmds.createNode('multiplyDivide',n=ctrlName+'_upScale')
    cmds.connectAttr(ctrlName+'_upclamp_PYrange.outputR',ctrlName+'_upScale.input1X',f=1)
    cmds.connectAttr(ctrlName+'_upreverse_X.outputX',ctrlName+'_upScale.input2X',f=1)
    cmds.createNode('clamp',n=ctrlName+'_upclamp_finalrange')
    cmds.connectAttr(ctrlName+'_upScale.outputX',ctrlName+'_upclamp_finalrange.inputR',f=1)
    cmds.setAttr(ctrlName+'_upclamp_finalrange.minR',0)
    cmds.setAttr(ctrlName+'_upclamp_finalrange.maxR',1)
    cmds.connectAttr(ctrlName+'_upclamp_finalrange.outputR',ctrlName+'_FRAME.up',f=1)
    ##==================    
    cmds.createNode('multiplyDivide',n=ctrlName+'_dnmult_Yinverse')
    cmds.connectAttr(ctrlName+sfix+'.ty',ctrlName+'_dnmult_Yinverse.input2X',f=1)
    cmds.setAttr(ctrlName+'_dnmult_Yinverse.input1X',-1)
    cmds.createNode('clamp',n=ctrlName+'_dnclamp_PYrange')
    cmds.connectAttr(ctrlName+'_dnmult_Yinverse.outputX',ctrlName+'_dnclamp_PYrange.inputR',f=1)
    cmds.setAttr(ctrlName+'_dnclamp_PYrange.minR',0)
    cmds.setAttr(ctrlName+'_dnclamp_PYrange.maxR',1)
    cmds.createNode('multiplyDivide',n=ctrlName+'_dnScale')
    cmds.connectAttr(ctrlName+'_dnclamp_PYrange.outputR',ctrlName+'_dnScale.input1X',f=1)
    cmds.connectAttr(ctrlName+'_upreverse_X.outputX',ctrlName+'_dnScale.input2X',f=1)
    cmds.createNode('clamp',n=ctrlName+'_dnclamp_finalrange')
    cmds.connectAttr(ctrlName+'_dnScale.outputX',ctrlName+'_dnclamp_finalrange.inputR',f=1)
    cmds.setAttr(ctrlName+'_dnclamp_finalrange.minR',0)
    cmds.setAttr(ctrlName+'_dnclamp_finalrange.maxR',1)
    cmds.connectAttr(ctrlName+'_dnclamp_finalrange.outputR',ctrlName+'_FRAME.dn',f=1)
    
    
    ##==================    
    cmds.createNode('multiplyDivide',n=ctrlName+'_lfmult_Yinverse')
    cmds.connectAttr(ctrlName+sfix+'.ty',ctrlName+'_lfmult_Yinverse.input2X',f=1)
    cmds.setAttr(ctrlName+'_lfmult_Yinverse.input1X',-1)
    cmds.createNode('clamp',n=ctrlName+'_lfclamp_PYrange')
    cmds.connectAttr(ctrlName+'_lfmult_Yinverse.outputX',ctrlName+'_lfclamp_PYrange.inputR',f=1)
    cmds.setAttr(ctrlName+'_lfclamp_PYrange.minR',0)
    cmds.setAttr(ctrlName+'_lfclamp_PYrange.maxR',1)
    cmds.createNode('clamp',n=ctrlName+'_lfclamp_NYrange')
    cmds.connectAttr(ctrlName+sfix+'.ty',ctrlName+'_lfclamp_NYrange.inputR',f=1)
    cmds.setAttr(ctrlName+'_lfclamp_NYrange.minR',0)
    cmds.setAttr(ctrlName+'_lfclamp_NYrange.maxR',1)
    cmds.createNode('plusMinusAverage',n=ctrlName+'_lfplus_Yplus')
    cmds.connectAttr(ctrlName+'_lfclamp_NYrange.outputR',ctrlName+'_lfplus_Yplus.input1D[0]',f=1)
    cmds.connectAttr(ctrlName+'_lfclamp_PYrange.outputR',ctrlName+'_lfplus_Yplus.input1D[1]',f=1)
    cmds.createNode('reverse',n=ctrlName+'_lfreverse_Y')
    cmds.connectAttr(ctrlName+'_lfplus_Yplus.output1D',ctrlName+'_lfreverse_Y.inputX',f=1)
    cmds.createNode('multiplyDivide',n=ctrlName+'_lfmult_Xinverse')
    cmds.connectAttr(ctrlName+sfix+'.tx',ctrlName+'_lfmult_Xinverse.input2X',f=1)
    cmds.setAttr(ctrlName+'_lfmult_Xinverse.input1X',-1)
    cmds.createNode('clamp',n=ctrlName+'_lfclamp_PXrange')
    cmds.connectAttr(ctrlName+'_lfmult_Xinverse.outputX',ctrlName+'_lfclamp_PXrange.inputR',f=1)
    cmds.setAttr(ctrlName+'_lfclamp_PXrange.minR',0)
    cmds.setAttr(ctrlName+'_lfclamp_PXrange.maxR',1)
    cmds.createNode('multiplyDivide',n=ctrlName+'_lfScale')
    cmds.connectAttr(ctrlName+'_lfclamp_PXrange.outputR',ctrlName+'_lfScale.input1X',f=1)
    cmds.connectAttr(ctrlName+'_lfreverse_Y.outputX',ctrlName+'_lfScale.input2X',f=1)
    cmds.createNode('clamp',n=ctrlName+'_lfclamp_finalrange')
    cmds.connectAttr(ctrlName+'_lfScale.outputX',ctrlName+'_lfclamp_finalrange.inputR',f=1)
    cmds.setAttr(ctrlName+'_lfclamp_finalrange.minR',0)
    cmds.setAttr(ctrlName+'_lfclamp_finalrange.maxR',1)
    cmds.connectAttr(ctrlName+'_lfclamp_finalrange.outputR',ctrlName+'_FRAME.lf',f=1)
    
    ##==================    
    cmds.createNode('clamp',n=ctrlName+'_rtclamp_PXrange')
    cmds.connectAttr(ctrlName+sfix+'.tx',ctrlName+'_rtclamp_PXrange.inputR',f=1)
    cmds.setAttr(ctrlName+'_rtclamp_PXrange.minR',0)
    cmds.setAttr(ctrlName+'_rtclamp_PXrange.maxR',1)
    cmds.createNode('multiplyDivide',n=ctrlName+'_rtScale')
    cmds.connectAttr(ctrlName+'_rtclamp_PXrange.outputR',ctrlName+'_rtScale.input1X',f=1)
    cmds.connectAttr(ctrlName+'_lfreverse_Y.outputX',ctrlName+'_rtScale.input2X',f=1)
    cmds.createNode('clamp',n=ctrlName+'_rtclamp_finalrange')
    cmds.connectAttr(ctrlName+'_rtScale.outputX',ctrlName+'_rtclamp_finalrange.inputR',f=1)
    cmds.setAttr(ctrlName+'_rtclamp_finalrange.minR',0)
    cmds.setAttr(ctrlName+'_rtclamp_finalrange.maxR',1)
    cmds.connectAttr(ctrlName+'_rtclamp_finalrange.outputR',ctrlName+'_FRAME.rt',f=1)
    
    ##==================
    cmds.createNode('multiplyDivide',n=ctrlName+'_lfupmult')
    cmds.connectAttr(ctrlName+'_lfclamp_NYrange.outputR',ctrlName+'_lfupmult.input1X',f=1)
    cmds.connectAttr(ctrlName+'_upclamp_PXrange.outputR',ctrlName+'_lfupmult.input2X',f=1)
    cmds.connectAttr(ctrlName+'_lfupmult.outputX',ctrlName+'_FRAME.lfup',f=1)

    ##==================
    cmds.createNode('multiplyDivide',n=ctrlName+'_rtupmult')
    cmds.connectAttr(ctrlName+'_lfclamp_NYrange.outputR',ctrlName+'_rtupmult.input1X',f=1)
    cmds.connectAttr(ctrlName+'_upclamp_NXrange.outputR',ctrlName+'_rtupmult.input2X',f=1)
    cmds.connectAttr(ctrlName+'_rtupmult.outputX',ctrlName+'_FRAME.rtup',f=1)
    
    ##==================
    cmds.createNode('multiplyDivide',n=ctrlName+'_lfdnmult')
    cmds.connectAttr(ctrlName+'_lfclamp_PYrange.outputR',ctrlName+'_lfdnmult.input1X',f=1)
    cmds.connectAttr(ctrlName+'_upclamp_PXrange.outputR',ctrlName+'_lfdnmult.input2X',f=1)
    cmds.connectAttr(ctrlName+'_lfdnmult.outputX',ctrlName+'_FRAME.lfdn',f=1)
  
    ##==================
    cmds.createNode('multiplyDivide',n=ctrlName+'_rtdnmult')
    cmds.connectAttr(ctrlName+'_lfclamp_PYrange.outputR',ctrlName+'_rtdnmult.input1X',f=1)
    cmds.connectAttr(ctrlName+'_upclamp_NXrange.outputR',ctrlName+'_rtdnmult.input2X',f=1)
    cmds.connectAttr(ctrlName+'_rtdnmult.outputX',ctrlName+'_FRAME.rtdn',f=1)
    
    #=======4Aixs=====================
    cmds.connectAttr(ctrlName+'_lfclamp_NYrange.outputR',ctrlName+'_FRAME.fourAxis_up',f=1)
    cmds.connectAttr(ctrlName+'_lfclamp_PYrange.outputR',ctrlName+'_FRAME.fourAxis_dn',f=1)
    cmds.connectAttr(ctrlName+'_upclamp_NXrange.outputR',ctrlName+'_FRAME.fourAxis_rt',f=1)
    cmds.connectAttr(ctrlName+'_upclamp_PXrange.outputR',ctrlName+'_FRAME.fourAxis_lf',f=1)
    cmds.select(cl=1)


def edo_addAttrBoundaryBox(ctrlName,sfix):
    #addAttrBoundaryBox
    upbb=edo_addFacialCtrlAttributeFrame(ctrlName,'up',0,sfix)
    cmds.setAttr(upbb+'.tx',0)
    cmds.setAttr(upbb+'.ty',2.2)
    cmds.setAttr(upbb+'.tz',0)
    dnbb=edo_addFacialCtrlAttributeFrame(ctrlName,'dn',0,sfix)
    cmds.setAttr(dnbb+'.tx',0)
    cmds.setAttr(dnbb+'.ty',-2.2)
    cmds.setAttr(dnbb+'.tz',0)
    lfbb=edo_addFacialCtrlAttributeFrame(ctrlName,'lf',0,sfix)
    cmds.setAttr(lfbb+'.tx',-2.2)
    cmds.setAttr(lfbb+'.ty',0)
    cmds.setAttr(lfbb+'.tz',0)
    lfupbb=edo_addFacialCtrlAttributeFrame(ctrlName,'lfup',0,sfix)
    cmds.setAttr(lfupbb+'.ty',2.2)
    cmds.setAttr(lfupbb+'.tx',-2.2)
    cmds.setAttr(lfupbb+'.tz',0)
    rtbb=edo_addFacialCtrlAttributeFrame(ctrlName,'rt',0,sfix)
    cmds.setAttr(rtbb+'.tx',2.2)
    cmds.setAttr(rtbb+'.ty',0)
    cmds.setAttr(rtbb+'.tz',0)
    rtupbb=edo_addFacialCtrlAttributeFrame(ctrlName,'rtup',0,sfix)
    cmds.setAttr(rtupbb+'.tx',2.2)
    cmds.setAttr(rtupbb+'.ty',2.2)
    cmds.setAttr(rtupbb+'.tz',0)
    lfdnbb=edo_addFacialCtrlAttributeFrame(ctrlName,'lfdn',0,sfix)
    cmds.setAttr(lfdnbb+'.tx',-2.2)
    cmds.setAttr(lfdnbb+'.ty',-2.2)
    cmds.setAttr(lfdnbb+'.tz',0)
    rtdnbb=edo_addFacialCtrlAttributeFrame(ctrlName,'rtdn',0,sfix)
    cmds.setAttr(rtdnbb+'.tx',2.2)
    cmds.setAttr(rtdnbb+'.ty',-2.2)
    cmds.setAttr(rtdnbb+'.tz',0)
    fupbb=edo_addFacialCtrlAttributeFrame(ctrlName,'fourAxisup',0,sfix)
    cmds.setAttr(fupbb+'.tx',0)
    cmds.setAttr(fupbb+'.ty',4.4)
    cmds.setAttr(fupbb+'.tz',0)
    fdnbb=edo_addFacialCtrlAttributeFrame(ctrlName,'fourAxisdn',0,sfix)
    cmds.setAttr(fdnbb+'.tx',0)
    cmds.setAttr(fdnbb+'.ty',-4.4)
    cmds.setAttr(fdnbb+'.tz',0)
    flfbb=edo_addFacialCtrlAttributeFrame(ctrlName,'fourAxislf',0,sfix)
    cmds.setAttr(flfbb+'.tx',-4.4)
    cmds.setAttr(flfbb+'.ty',0)
    cmds.setAttr(flfbb+'.tz',0)
    frtbb=edo_addFacialCtrlAttributeFrame(ctrlName,'fourAxisrt',0,sfix)
    cmds.setAttr(frtbb+'.tx',4.4)
    cmds.setAttr(frtbb+'.ty',0)
    cmds.setAttr(frtbb+'.tz',0)
    cmds.select(ctrlName+'_FRAME',r=1)

def edo_addFacialCtrlAttributeFrame(ctrlName,attrname,vis=0,sfix='_CTRL'):
    #ctrlName='test'
    #attrname='fourAxisup'
    fc=cmds.curve(d=1,p=[(-1,1,0),(-1,-1,0),(1,-1,0),(1,1,0),(-1,1,0)],k=[0,1,2,3,4],n=ctrlName+sfix+'_'+attrname)
    sh=cmds.listRelatives(fc,s=1,pa=1)[0]
    nsh=cmds.rename(sh,fc+'Shape')
    cmds.parent(ctrlName+sfix+'_'+attrname,ctrlName+'_FRAME')
    visattrname=attrname.replace('fourAxis','fourAxis_')
    cmds.addAttr(ctrlName+'_FRAME',ln=visattrname+'_Vis',at='bool')
    cmds.setAttr(ctrlName+'_FRAME.'+visattrname+'_Vis',e=1,cb=1)
    cmds.setAttr(ctrlName+'_FRAME.'+visattrname+'_Vis',vis)
    cmds.connectAttr(ctrlName+'_FRAME.'+visattrname+'_Vis',ctrlName+sfix+'_'+attrname+'.v',f=1)
    cmds.createNode('locator',n=ctrlName+'_LOC_'+visattrname,p=ctrlName+sfix+'_'+attrname)
    cmds.setAttr(ctrlName+'_LOC_'+visattrname+'.v',0)
    return ctrlName+sfix+'_'+attrname
    

#########edo_addMultiplyFrame(cmds.ls(sl=1))
def edo_addMultiplyFrame(frameList):
    #frameList=cmds.ls(sl=1)
    sfix='_CONNECT'
    for f in frameList:
        #f=frameList[0]
        if not '_CONNECT_' in f:
            sfix=''
            break
    if sfix=='':
        sfix='_CTRL'
        for f in frameList:
            #f=frameList[0]
            if not '_CTRL_' in f:
                sfix=''
                break
    print sfix
    if sfix=='':
        cmds.confirmDialog( title='Confirm', message='you have to select same curve type frame to create multiFrame!', button=['got it'] )
        return False
    kuo=')'*(len(frameList)-1)
    frameStr=edo_frameListToFrameStr(frameList).replace('fourAxis','fourAxis_')
    curve=cmds.curve(d=1,p=[(-1,1,0),(-1,-1,0),(1,-1,0),(1,1,0),(-1,1,0)],k=[0,1,2,3,4])
    cmds.rename(curve,frameStr)
    cmds.createNode('locator',n=frameStr.replace(sfix+'_','_LOC_'),p=frameStr)
    cmds.setAttr(frameStr.replace(sfix+'_','_LOC_')+'.v',0)
    ex='//'+frameStr+'_EXPRESSION\n'
    ex+=(frameStr+'.multiplyValue=\n')
    cmds.addAttr(frameStr,ln='connectCurveVis',at='bool')
    cmds.setAttr(frameStr+'.connectCurveVis',e=1,k=1)
    cmds.setAttr(frameStr+'.connectCurveVis',1)
    cmds.addAttr(frameStr,ln='multiplyValue',at='double')
    cmds.setAttr(frameStr+'.multiplyValue',e=1,k=1)
    cmds.addAttr(frameStr,ln='multiplyReverseValue',at='double')
    cmds.setAttr(frameStr+'.multiplyReverseValue',e=1,k=1)
    pl=[]
    for fl in frameList:
        #fl=frameList[1]
        print fl
        fl=fl.replace('fourAxis','fourAxis_')
        fattr=fl.replace(sfix+'_','_FRAME.')
        loc=fl.replace(sfix+'_','_LOC_')
        cmds.addAttr(frameStr,ln=fattr.replace('.','__'),at='double')
        cmds.setAttr(frameStr+'.'+fattr.replace('.','__'),e=1,k=1)
        cmds.connectAttr(fattr,frameStr+'.'+fattr.replace('.','__'),f=1)
        if not fl==frameList[-1].replace('fourAxis','fourAxis_'):
            ex+='min('+frameStr+'.'+fattr.replace('.','__')+',\n'
        else:
            ex+=frameStr+'.'+fattr.replace('.','__')+kuo+'\n'
        cmds.curve(d=1,p=[(-1,0,0),(1,0,0)],k=[0,1],n=fl+'___'+frameStr+'_connectCurve')
        cmds.parent(fl+'___'+frameStr+'_connectCurve',frameStr)
        cmds.setAttr(fl+'___'+frameStr+'_connectCurve.inheritsTransform',0)
        cmds.setAttr(fl+'___'+frameStr+'_connectCurve.overrideEnabled',1)
        cmds.setAttr(fl+'___'+frameStr+'_connectCurve.overrideDisplayType',2)
        cmds.connectAttr(frameStr.replace(sfix+'_','_LOC_')+'.worldPosition[0]',fl+'___'+frameStr+'_connectCurve.controlPoints[0]',f=1)
        cmds.connectAttr(loc+'.worldPosition',fl+'___'+frameStr+'_connectCurve.controlPoints[1]',f=1)
        cmds.connectAttr(frameStr+'.connectCurveVis',fl+'___'+frameStr+'_connectCurve.v',f=1)
        pl+=[cmds.xform(fl.replace('fourAxis_','fourAxis'),q=1,ws=1,t=1)]
    
    p=edo_arrayPositions(pl)
    cmds.xform(frameStr,ws=1,t=p)
    if cmds.objExists(frameStr+'_EXPRESSION'):
        cmds.delete(frameStr+'_EXPRESSION')
    #ex=ex[:-1]+'1'
    #for i in range(len(frameList)):
    #    ex=ex+')'
    #print ex
    ex+=(';\n'+frameStr+'.multiplyReverseValue=1-'+frameStr+'.multiplyValue;\n')
    print ex
    cmds.expression(n=frameStr+'_EXPRESSION',s=ex)
    cmds.select(frameStr,r=1)
    
def edo_arrayPositions(pointList):
    #pointList=[[1,1,1],[-2,-2,-2]]
    fp=[0,0,0]
    l=float(len(pointList))
    for point in pointList:
        #point=pointList[0]
        fp[0]+=point[0]
        fp[1]+=point[1]
        fp[2]+=point[2]
    fp=[fp[0]/l,fp[1]/l,fp[2]/l]
    return fp

def edo_frameListToFrameStr(frameList):
    frameStr=''
    for f in frameList:
        #f=frameList[0]
        frameStr+=(f+'___')
    return frameStr[:-3]
#-*- coding: utf-8 -*-
import maya.cmds as cmds
import edo_general.edo_lsDgGraph as edo_lsDgGraph
from headfile import *
import maya.OpenMaya as om

def edo_targetIsInBlendShapeWeightId(target,bsnode):
    #target=si
    #bsnode=bsname[0]
    #bswc=cmds.blendShape(bsnode,q=1,wc=1)
    bswc=edo_getMaxLocalIndexFromPhysicalCount(bsnode+'.weight')+1
    im=max(5000,bswc)
    for i in range(0,im):
        #i=0
        bsattr=cmds.aliasAttr(bsnode+'.weight['+str(i)+']',q=1)
        if bsattr==target:
            return i
    return -1

#edo_addBlendShapeAndExpressionsByFacialCtrl('test_CTRL')
def edo_addBlendShapeAndExpressionsByFacialCtrl(ctrlName):
    #ctrlName='test_CTRL'
    endstr=ctrlName.split('_')[-1]
    allMeshes=[]
    if endstr=='CTRL':
        upmeshes=cmds.listRelatives(ctrlName+'_up',c=1,type='transform',pa=1)
        dnmeshes=cmds.listRelatives(ctrlName+'_dn',c=1,type='transform',pa=1)
        lfmeshes=cmds.listRelatives(ctrlName+'_lf',c=1,type='transform',pa=1)
        lfupmeshes=cmds.listRelatives(ctrlName+'_lfup',c=1,type='transform',pa=1)
        lfdnmeshes=cmds.listRelatives(ctrlName+'_lfdn',c=1,type='transform',pa=1)
        rtmeshes=cmds.listRelatives(ctrlName+'_rt',c=1,type='transform',pa=1)
        rtupmeshes=cmds.listRelatives(ctrlName+'_rtup',c=1,type='transform',pa=1)
        rtdnmeshes=cmds.listRelatives(ctrlName+'_rtdn',c=1,type='transform',pa=1)
        fourAxisupmeshes=cmds.listRelatives(ctrlName+'_fourAxisup',c=1,type='transform',pa=1)
        fourAxisdnmeshes=cmds.listRelatives(ctrlName+'_fourAxisdn',c=1,type='transform',pa=1)
        fourAxislfmeshes=cmds.listRelatives(ctrlName+'_fourAxislf',c=1,type='transform',pa=1)
        fourAxisrtmeshes=cmds.listRelatives(ctrlName+'_fourAxisrt',c=1,type='transform',pa=1)
        edo_combineAllList(allMeshes,upmeshes)
        edo_combineAllList(allMeshes,dnmeshes)
        edo_combineAllList(allMeshes,lfmeshes)
        edo_combineAllList(allMeshes,rtmeshes)
        edo_combineAllList(allMeshes,lfupmeshes)
        edo_combineAllList(allMeshes,rtupmeshes)
        edo_combineAllList(allMeshes,lfdnmeshes)
        edo_combineAllList(allMeshes,rtdnmeshes)
        edo_combineAllList(allMeshes,fourAxisupmeshes)
        edo_combineAllList(allMeshes,fourAxisdnmeshes)
        edo_combineAllList(allMeshes,fourAxislfmeshes)
        edo_combineAllList(allMeshes,fourAxisrtmeshes)
        if allMeshes==[] or allMeshes==None:
            return False
    else:
        allMeshes=cmds.listRelatives(ctrlName,c=1,type='transform',pa=1)
    bsnodes=[]
    targetMesh=''
    for m in allMeshes:
        #m=allMeshes[0]
        print m
        if 'connectCurve' in m:
            continue
        targetMesh=m.split('__')[1]+'_'
        if cmds.objExists(targetMesh):
            BSname=targetMesh+'_BLENDSHAPE'
            if not BSname in bsnodes:
                bsnodes.append(BSname)
            if not cmds.objExists(BSname):
                bsnode=cmds.blendShape(targetMesh,frontOfChain=1,n=BSname)
            #wc=cmds.blendShape(BSname,q=1,wc=1)
            wc=edo_getMaxLocalIndexFromPhysicalCount(BSname+'.weight')+1
            output=cmds.listConnections(m+'.worldMesh[0]',s=0,d=1,type='blendShape')
            if not output==None:
                if not BSname in cmds.listConnections(m+'.worldMesh[0]',s=0,d=1,type='blendShape'):
                    cmds.blendShape(BSname,e=1,t=[targetMesh,wc,m,1.0])
            else:
                id=edo_targetIsInBlendShapeWeightId(m,BSname)
                if id==-1:
                    cmds.blendShape(BSname,e=1,t=[targetMesh,wc,m,1.0])
                else:
                    cmds.blendShape(BSname,e=1,ib=True,t=[targetMesh,id,m,1.0])
    print 'get expression...'
    for bsnode in bsnodes:
        #bsnode=bsnodes[0]
        exname=ctrlName+'__'+bsnode.replace('_BLENDSHAPE','_EXPRESSION')
        extext='//'+exname+'\n'
        extext+='//don\'t write custom expression in here!,the script will delete this scirpt first before create a new expression\n\n'
        if cmds.objExists(exname):
            cmds.delete(exname)
        #bsattrlen=cmds.blendShape(bsnode,q=1,wc=1)
        bsattrlen=edo_getMaxLocalIndexFromPhysicalCount(bsnode+'.weight')+1
        for i in range(0,bsattrlen):
            #i=1
            print i
            ctrlattrname=''
            if endstr=='CTRL':
                bsattr=cmds.aliasAttr(bsnode+'.weight['+str(i)+']',q=1)
                m=bsattr
                bsattrname=bsnode+'.'+m
                print m
                if not ctrlName in m or '___' in m:
                    print m+' ... pass'
                    continue
                else:
                    print m+' ... addex'
                    ctrlattrname=m.split('__')[len(m.split('__'))-1]
                    ctrlattrname=ctrlattrname.replace('CTRL_','FRAME.')
                    ctrlattrname=ctrlattrname.replace('fourAxis','fourAxis_')
                    extext+=bsattrname+'='+ctrlattrname+';\n'
            else:
                bsattr=cmds.aliasAttr(bsnode+'.weight['+str(i)+']',q=1)
                m=bsattr
                bsattrname=bsnode+'.'+m
                print m
                if not ctrlName in m:
                    print m+' ... pass'
                    continue
                else:
                    print m+' ... addex'
                    tmp=m.split('___')
                    st=tmp[0].split('__')[-1]
                    tmp.remove(tmp[0])
                    ctrlattrname=st
                    for t in tmp:
                        ctrlattrname+=('___'+t)
                    ctrlattrname=ctrlattrname+'.multiplyValue'
                    extext+=bsattrname+'='+ctrlattrname+';\n'
        print 'add expression'
        print exname+' : \n'+extext+'\n'
        cmds.expression(n=exname,s=extext)

def edo_combineAllList(finalList,combineList):
    if combineList==None or combineList==[]:
        return finalList
    finalList+=combineList

def edo_attrIsInBlendShape(bsname,attrname):
    #bsname='MSH_body_new__BLENDSHAPE'
    #attrname='BS__MSH_body_new__Lfeyebrows_CTRL_rtup'
    #wc=cmds.blendShape(bsname,q=1,wc=1)
    wc=edo_getMaxLocalIndexFromPhysicalCount(bsname+'.weight')+1
    for i in range(0,wc):
        #i=0
        atname=bsname+'.weight['+str(i)+']'
        atlname=cmds.aliasAttr(atname,q=1)
        if atlname==attrname:
            return i
    return -1
    
    

def edo_renameBlendShapeMesh():
    sels=cmds.ls(sl=1)
    if sels==None:
        return False
    tn=sels[len(sels)-1]
    if not tn[len(tn)-1]=='_':
        cmds.confirmDialog( title='目标模型命名不规范', message='目标模型后缀没有\'_\',请通知模型添加!', button='god it', defaultButton='Yes', cancelButton='No', dismissString='No')
        return False
    sels.remove(tn)
    for s in sels:
        en=tn.split('|')[len(tn.split('|'))-1]
        nn=cmds.rename(s,'BS__'+en+'_xxxx')
        print 'rename  ...  '+s+'  ...  to  ...  '+nn+'\n'
     
#edo_opBlendShapeByFacialCtrl(cmds.ls(sl=1)[0])
def edo_opBlendShapeByFacialCtrl(ctrlName):
    #ctrlName='Lfmouth_CTRL_fourAxis_dn___Lfdnmouth_sneer_CTRL_dn'
    endstr=ctrlName.split('_')[-1]
    newnames=[]
    if endstr=='CTRL':
        edo_setBlendShapeMeshTransform(ctrlName+'_up')
        edo_setBlendShapeMeshTransform(ctrlName+'_dn')
        edo_setBlendShapeMeshTransform(ctrlName+'_lf')
        edo_setBlendShapeMeshTransform(ctrlName+'_rt')
        edo_setBlendShapeMeshTransform(ctrlName+'_lfup')
        edo_setBlendShapeMeshTransform(ctrlName+'_lfdn')
        edo_setBlendShapeMeshTransform(ctrlName+'_rtup')
        edo_setBlendShapeMeshTransform(ctrlName+'_rtdn')
        edo_setBlendShapeMeshTransform(ctrlName+'_fourAxisup')
        edo_setBlendShapeMeshTransform(ctrlName+'_fourAxisdn')
        edo_setBlendShapeMeshTransform(ctrlName+'_fourAxislf')
        edo_setBlendShapeMeshTransform(ctrlName+'_fourAxisrt')
        #
        newnames.append(edo_renameBlendShapeMeshByFrame(ctrlName+'_up'))
        newnames.append(edo_renameBlendShapeMeshByFrame(ctrlName+'_dn'))
        newnames.append(edo_renameBlendShapeMeshByFrame(ctrlName+'_lf'))
        newnames.append(edo_renameBlendShapeMeshByFrame(ctrlName+'_rt'))
        newnames.append(edo_renameBlendShapeMeshByFrame(ctrlName+'_lfup'))
        newnames.append(edo_renameBlendShapeMeshByFrame(ctrlName+'_lfdn'))
        newnames.append(edo_renameBlendShapeMeshByFrame(ctrlName+'_rtup'))
        newnames.append(edo_renameBlendShapeMeshByFrame(ctrlName+'_rtdn'))
        newnames.append(edo_renameBlendShapeMeshByFrame(ctrlName+'_fourAxisup'))
        newnames.append(edo_renameBlendShapeMeshByFrame(ctrlName+'_fourAxisdn'))
        newnames.append(edo_renameBlendShapeMeshByFrame(ctrlName+'_fourAxislf'))
        newnames.append(edo_renameBlendShapeMeshByFrame(ctrlName+'_fourAxisrt'))
    else:
        edo_setBlendShapeMeshTransform(ctrlName)
        newnames.append(edo_renameBlendShapeMeshByFrame(ctrlName))
    cmds.select(ctrlName,r=1)
    return newnames
        

def edo_renameBlendShapeMeshByFrame(frameName):
    #frameName='test_CTRL_fourAxisup'
    if not cmds.objExists('GRP_wrongNameBlendShapes'):
        cmds.createNode('transform',n='GRP_wrongNameBlendShapes')
    childs=cmds.listRelatives(frameName,s=0,c=1,pa=1,type='transform')
    if childs==None:
        return False
    newnames=[]
    for c in childs:
        #c=childs[0]
        if c.split('_')[-1]=='connectCurve':
            print 'pass connectCurve'
            continue
        if cmds.nodeType(c)=='transform':
            tc=c.split('|')[-1]
            objname=tc.split('__')[1]
            if not cmds.objExists(objname+'_'):
                cmds.parent(c,'GRP_wrongNameBlendShapes')
                continue
            newname=edo_removeLastStr(c,'__')+frameName
            nn=newname.split('|')[len(newname.split('|'))-1]
            newname=cmds.rename(c,nn)
            newnames.append(newname)
    return newnames

                
def edo_removeLastStr(name,flag='_'):
    #name='face_CTRL_up|BS__MSH_facial__xxxx'
    #flag='__'
    sn=name.split(flag)
    rn=''
    for i in range(0,len(sn)-1):
        rn+=sn[i]+flag
    return rn
        
        
    
def edo_setBlendShapeMeshTransform(frameName):
    #frameName='Lfmouth_CTRL_fourAxis_dn___Lfdnmouth_sneer_CTRL_dn'
    po=cmds.xform(frameName,q=1,ws=1,t=1)
    if not cmds.objExists('GRP_wrongNameBlendShapes'):
        cmds.createNode('transform',n='GRP_wrongNameBlendShapes')
    childs=cmds.listRelatives(frameName,type='transform',c=1,pa=1)
    if childs==None:
        return False
    for c in childs:
        #c=childs[2]
        if c.split('_')[-1]=='connectCurve':
            print 'pass connectCurve'
            continue
        if cmds.nodeType(c)=='transform':
            tc=c.split('|')[-1]
            oc=tc.split('__')
            if not cmds.objExists(oc[1]+'_'):
                cmds.parent(c,'GRP_wrongNameBlendShapes')
                continue
            if 'BS__' in c:
                cmds.xform(c,ws=1,t=po)
            else:
                cmds.parent(c,'GRP_wrongNameBlendShapes')


def edo_addFollicelPlane():
    sels=cmds.ls(sl=1)
    if sels:
        for s in sels:
            #s=sels[0]
            mesh=cmds.polyPlane(n='FCM_'+s,sw=1,sh=1)
            #cmds.delete(mesh[1])
            #f=cmds.createNode('follicle',n=mesh[0]+'_follicleShape')
            #fo=cmds.listRelatives(f,p=1,pa=1)[0]
            #cmds.rename(fo,mesh[0]+'_follicle')
            #cmds.connectAttr(mesh[0]+'.outMesh',f+'.inputMesh',f=1)
            #cmds.connectAttr(mesh[0]+'.worldMatrix',f+'.inputWorldMatrix',f=1)
            #cmds.connectAttr(f+'.outTranslate',mesh[0]+'_follicle.translate',f=1)
            #cmds.connectAttr(f+'.outRotate',mesh[0]+'_follicle.rotate',f=1)
            #cmds.setAttr(f+'.parameterU',0.5)
            #cmds.setAttr(f+'.parameterV',0.5)
            cmds.delete(cmds.parentConstraint(s,mesh[0],mo=0))
            cmds.makeIdentity(mesh[0],apply=1,t=1,r=1,s=1,n=0)
#edo_renameBlendShapeMeshInbetween()            
def edo_renameBlendShapeMeshInbetween(inbetweenDsb='1.0'):
    #inbetweenDsb='1.0'
    sels=cmds.ls(sl=1)
    nn=''
    if sels:
        #cmds.objectTypeUI('inbetweenDsb')
        #inbetween=str(int(float(cmds.textField('inbetweenDsb',q=1,tx=1))*1000+5000))
        inbetween=str(int(float(inbetweenDsb)*1000+5000))
        if sels==None:
            return False
        tn=sels[len(sels)-1]
        if not tn[len(tn)-1]=='_':
            cmds.confirmDialog( title='目标模型命名不规范', message='目标模型后缀没有\'_\',请通知模型添加!', button='god it', defaultButton='Yes', cancelButton='No', dismissString='No')
            return False
        sels.remove(tn)
        nnn=''
        for s in sels:
            #s=sels[0]
            en=tn.split('|')[len(tn.split('|'))-1]
            nn=cmds.rename(s,'BS__'+en+'_'+inbetween+'__xxxx')
            print 'rename  ...  '+s+'  ...  to  ...  '+nn+'\n'
            if nnn=='':
                nnn=nn
        return nnn
    return False

def edo_autoConnectBlendshapes():
    sels=cmds.ls(sl=1)
    allbms=[]
    if not sels:
        cmds.confirmDialog( title='需要选择控制器', message='需要选择控制器再执行命令', button='god it', defaultButton='Yes', cancelButton='No', dismissString='No')
        return False
    allbms=edo_opBlendShapeByFacialCtrlInbetween(sels[0])
    #allbms=edo_opBlendShapeByFacialCtrl
    edo_addBlendShapeAndExpressionsByFacialCtrlInbetween(sels[0])
    return allbms
    
def edo_opBlendShapeByFacialCtrlInbetween(ctrlName):
    #ctrlName='test_CTRL'
    #ctrlName='aaa_CONNECT'
    #ctrlName='bbb_CONNECT_lfup___aaa_CONNECT_fourAxis_up'
    endstr=ctrlName.split('_')[-1]
    newbms=[]
    if endstr=='CTRL' or endstr=='CONNECT':
        edo_setBlendShapeMeshTransform(ctrlName+'_up')
        edo_setBlendShapeMeshTransform(ctrlName+'_dn')
        edo_setBlendShapeMeshTransform(ctrlName+'_lf')
        edo_setBlendShapeMeshTransform(ctrlName+'_rt')
        edo_setBlendShapeMeshTransform(ctrlName+'_lfup')
        edo_setBlendShapeMeshTransform(ctrlName+'_lfdn')
        edo_setBlendShapeMeshTransform(ctrlName+'_rtup')
        edo_setBlendShapeMeshTransform(ctrlName+'_rtdn')
        edo_setBlendShapeMeshTransform(ctrlName+'_fourAxisup')
        edo_setBlendShapeMeshTransform(ctrlName+'_fourAxisdn')
        edo_setBlendShapeMeshTransform(ctrlName+'_fourAxislf')
        edo_setBlendShapeMeshTransform(ctrlName+'_fourAxisrt')
        #
        newbms.append(edo_renameBlendShapeMeshByFrameInbetween(ctrlName+'_up'))
        newbms.append(edo_renameBlendShapeMeshByFrameInbetween(ctrlName+'_dn'))
        newbms.append(edo_renameBlendShapeMeshByFrameInbetween(ctrlName+'_lf'))
        newbms.append(edo_renameBlendShapeMeshByFrameInbetween(ctrlName+'_rt'))
        newbms.append(edo_renameBlendShapeMeshByFrameInbetween(ctrlName+'_lfup'))
        newbms.append(edo_renameBlendShapeMeshByFrameInbetween(ctrlName+'_lfdn'))
        newbms.append(edo_renameBlendShapeMeshByFrameInbetween(ctrlName+'_rtup'))
        newbms.append(edo_renameBlendShapeMeshByFrameInbetween(ctrlName+'_rtdn'))
        newbms.append(edo_renameBlendShapeMeshByFrameInbetween(ctrlName+'_fourAxisup'))
        newbms.append(edo_renameBlendShapeMeshByFrameInbetween(ctrlName+'_fourAxisdn'))
        newbms.append(edo_renameBlendShapeMeshByFrameInbetween(ctrlName+'_fourAxislf'))
        newbms.append(edo_renameBlendShapeMeshByFrameInbetween(ctrlName+'_fourAxisrt'))
    else:
        edo_setBlendShapeMeshTransform(ctrlName)
        newbms.append(edo_renameBlendShapeMeshByFrame(ctrlName))
    cmds.select(ctrlName,r=1)
    return newbms
    
def edo_renameBlendShapeMeshByFrameInbetween(frameName):
    #frameName=ctrlName+'_up'
    if not cmds.objExists('GRP_wrongNameBlendShapes'):
        cmds.createNode('transform',n='GRP_wrongNameBlendShapes')
    childs=cmds.listRelatives(frameName,s=0,c=1,pa=1,type='transform')
    if childs==None:
        return False
    newnames=[]
    for c in childs:
        #c=childs[0]
        if c.split('_')[-1]=='connectCurve':
            print 'pass connectCurve'
            continue
        if cmds.nodeType(c)=='transform':
            tc=c.split('|')[-1]
            objname=tc.split('__')[1]
            if not cmds.objExists(objname+'_'):
                cmds.parent(c,'GRP_wrongNameBlendShapes')
                continue
            newname=edo_removeLastStr(c,'__')+frameName
            nn=newname.split('|')[len(newname.split('|'))-1]
            newname=cmds.rename(c,nn)
            newnames.append(newname)
    return newnames

def edo_addBlendShapeAndExpressionsByFacialCtrlInbetween(ctrlName):
    #ctrlName=sels[0]
    #ctrlName='bbb_CONNECT_lfup___aaa_CONNECT_fourAxis_up'
    sfix=''
    if '_CTRL' in ctrlName:
        sfix='_CTRL'
    if '_CONNECT' in ctrlName:
        sfix='_CONNECT'
    if sfix=='':
        #cmds.confirmDialog( title='Confirm', message='this node is not created by autoBlendShapeManagerTools', button=['got it'] )
        raise Exception('this node  ['+ ctrlName +']  is not created by autoBlendShapeManagerTools')
        return False
    endstr=ctrlName.split('_')[-1]
    allMeshes=[]
    if endstr=='CTRL' or endstr=='CONNECT':
        upmeshes=cmds.listRelatives(ctrlName+'_up',c=1,type='transform',pa=1)
        dnmeshes=cmds.listRelatives(ctrlName+'_dn',c=1,type='transform',pa=1)
        lfmeshes=cmds.listRelatives(ctrlName+'_lf',c=1,type='transform',pa=1)
        lfupmeshes=cmds.listRelatives(ctrlName+'_lfup',c=1,type='transform',pa=1)
        lfdnmeshes=cmds.listRelatives(ctrlName+'_lfdn',c=1,type='transform',pa=1)
        rtmeshes=cmds.listRelatives(ctrlName+'_rt',c=1,type='transform',pa=1)
        rtupmeshes=cmds.listRelatives(ctrlName+'_rtup',c=1,type='transform',pa=1)
        rtdnmeshes=cmds.listRelatives(ctrlName+'_rtdn',c=1,type='transform',pa=1)
        fourAxisupmeshes=cmds.listRelatives(ctrlName+'_fourAxisup',c=1,type='transform',pa=1)
        fourAxisdnmeshes=cmds.listRelatives(ctrlName+'_fourAxisdn',c=1,type='transform',pa=1)
        fourAxislfmeshes=cmds.listRelatives(ctrlName+'_fourAxislf',c=1,type='transform',pa=1)
        fourAxisrtmeshes=cmds.listRelatives(ctrlName+'_fourAxisrt',c=1,type='transform',pa=1)
        edo_combineAllList(allMeshes,upmeshes)
        edo_combineAllList(allMeshes,dnmeshes)
        edo_combineAllList(allMeshes,lfmeshes)
        edo_combineAllList(allMeshes,rtmeshes)
        edo_combineAllList(allMeshes,lfupmeshes)
        edo_combineAllList(allMeshes,rtupmeshes)
        edo_combineAllList(allMeshes,lfdnmeshes)
        edo_combineAllList(allMeshes,rtdnmeshes)
        edo_combineAllList(allMeshes,fourAxisupmeshes)
        edo_combineAllList(allMeshes,fourAxisdnmeshes)
        edo_combineAllList(allMeshes,fourAxislfmeshes)
        edo_combineAllList(allMeshes,fourAxisrtmeshes)
        if allMeshes==[] or allMeshes==None:
            return False
    else:
        allMeshes=cmds.listRelatives(ctrlName,c=1,type='transform',pa=1)
    bsnodes=[]
    targetMesh=''
    for mm in allMeshes:
        #mm=allMeshes[2]
        print mm
        if 'connectCurve' in mm:
            continue
        targetMesh=mm.split('__')[1]+'_'
        targetCtrl=mm.split('__')[-1]
        ##if selected object is a ctrl
        if cmds.objExists(targetMesh) and cmds.objExists(targetCtrl):
            BSname=targetMesh+'_BLENDSHAPE'
            m=cmds.rename(mm,edo_splitBlendshapeWeightStr(mm,'6000'))
            print m
            if m[-1].lower()==m[-1].upper():
                print m+'... is a wrong named target,passed...'
                continue
            if len(m.split('__'))==4 and m.split('__')[2].upper()==m.split('__')[2].lower():
                print 'add inbetween...'
                if not BSname in bsnodes:
                    bsnodes.append(BSname)
                if not cmds.objExists(BSname):
                    bsnode=cmds.blendShape(targetMesh,frontOfChain=1,n=BSname)
                #wc=cmds.blendShape(BSname,q=1,wc=1)
                wc=edo_getMaxLocalIndexFromPhysicalCount(BSname+'.weight')+1
                attrname=edo_splitBlendshapeWeightStr(m,m.split('__')[2])
                id=edo_targetIsInBlendShapeWeightId(attrname,BSname)
                wv=(float(m.split('__')[2])-5000)/1000
                output=cmds.listConnections(m+'.worldMesh[0]',s=0,d=1,type='blendShape')
                if not output==None:
                    if not BSname in cmds.listConnections(m+'.worldMesh[0]',s=0,d=1,type='blendShape'):
                        if id==-1:
                            cmds.blendShape(BSname,e=1,t=[targetMesh,wc,m,wv])
                        else:
                            cmds.blendShape(BSname,e=1,ib=True,t=[targetMesh,id,m,mv])
                        try:
                            cmds.aliasAttr(attrname,BSname+'.weight['+str(wc)+']')
                        except:
                            print 'pass aliasAttr...'
                else:
                    if id==-1:
                        cmds.blendShape(BSname,e=1,t=[targetMesh,wc,m,wv])
                    else:
                        cmds.blendShape(BSname,e=1,ib=True,t=[targetMesh,id,m,wv])
                    try:
                        cmds.aliasAttr(attrname,BSname+'.weight['+str(wc)+']')
                    except:
                        print 'pass aliasAttr...'
            else:
                if not BSname in bsnodes:
                    bsnodes.append(BSname)
                if not cmds.objExists(BSname):
                    bsnode=cmds.blendShape(targetMesh,frontOfChain=1,n=BSname)
                #attrname=edo_splitBlendshapeWeightStr(m,m.split('__')[2])
                id=edo_targetIsInBlendShapeWeightId(m,BSname)
                #wc=cmds.blendShape(BSname,q=1,wc=1)
                wc=edo_getMaxLocalIndexFromPhysicalCount(BSname+'.weight')+1
                output=cmds.listConnections(m+'.worldMesh[0]',s=0,d=1,type='blendShape')
                if not output==None:
                    if not BSname in cmds.listConnections(m+'.worldMesh[0]',s=0,d=1,type='blendShape'):
                        cmds.blendShape(BSname,e=1,t=[targetMesh,wc,m,1.0])
                else:
                    if id==-1:
                        cmds.blendShape(BSname,e=1,t=[targetMesh,wc,m,1.0])
                    else:
                        cmds.blendShape(BSname,e=1,ib=True,t=[targetMesh,id,m,1.0])
        else:
            ##if selected object is a complexed frame
            if cmds.objExists(mm[(len(ctrlName)*-1):]):
                print 'selected object is a complexed frame'
                BSname=targetMesh+'_BLENDSHAPE'
                #mm='BS__pSphere1__5500__aaa_CTRL_rtdn___bbb_CTRL_lfdn'
                m=cmds.rename(mm,edo_splitBlendshapeWeightStr(mm,'6000'))
                print m
                if m[-1].lower()==m[-1].upper():
                    print m+'... is a wrong named target,passed...'
                    continue
                if len(m.split('__'))==5 and m.split('__')[2].upper()==m.split('__')[2].lower():
                    print 'add inbetween...'
                    if not BSname in bsnodes:
                        bsnodes.append(BSname)
                    if not cmds.objExists(BSname):
                        bsnode=cmds.blendShape(targetMesh,frontOfChain=1,n=BSname)
                    #wc=cmds.blendShape(BSname,q=1,wc=1)
                    wc=edo_getMaxLocalIndexFromPhysicalCount(BSname+'.weight')+1
                    attrname=edo_splitBlendshapeWeightStr(m,m.split('__')[2])
                    id=edo_targetIsInBlendShapeWeightId(attrname,BSname)
                    wv=(float(m.split('__')[2])-5000)/1000
                    output=cmds.listConnections(m+'.worldMesh[0]',s=0,d=1,type='blendShape')
                    if not output==None:
                        if not BSname in cmds.listConnections(m+'.worldMesh[0]',s=0,d=1,type='blendShape'):
                            if id==-1:
                                cmds.blendShape(BSname,e=1,t=[targetMesh,wc,m,wv])
                            else:
                                cmds.blendShape(BSname,e=1,ib=True,t=[targetMesh,id,m,mv])
                            try:
                                cmds.aliasAttr(attrname,BSname+'.weight['+str(wc)+']')
                            except:
                                print 'pass aliasAttr...'
                    else:
                        if id==-1:
                            cmds.blendShape(BSname,e=1,t=[targetMesh,wc,m,wv])
                        else:
                            cmds.blendShape(BSname,e=1,ib=True,t=[targetMesh,id,m,wv])
                        try:
                            cmds.aliasAttr(attrname,BSname+'.weight['+str(wc)+']')
                        except:
                            print 'pass aliasAttr...'
                else:
                    if not BSname in bsnodes:
                        bsnodes.append(BSname)
                    if not cmds.objExists(BSname):
                        bsnode=cmds.blendShape(targetMesh,frontOfChain=1,n=BSname)
                    #attrname=edo_splitBlendshapeWeightStr(m,m.split('__')[2])
                    id=edo_targetIsInBlendShapeWeightId(m,BSname)
                    #wc=cmds.blendShape(BSname,q=1,wc=1)
                    wc=edo_getMaxLocalIndexFromPhysicalCount(BSname+'.weight')+1
                    output=cmds.listConnections(m+'.worldMesh[0]',s=0,d=1,type='blendShape')
                    if not output==None:
                        if not BSname in cmds.listConnections(m+'.worldMesh[0]',s=0,d=1,type='blendShape'):
                            cmds.blendShape(BSname,e=1,t=[targetMesh,wc,m,1.0])
                    else:
                        if id==-1:
                            cmds.blendShape(BSname,e=1,t=[targetMesh,wc,m,1.0])
                        else:
                            cmds.blendShape(BSname,e=1,ib=True,t=[targetMesh,id,m,1.0])
    #add expression....
    print 'get expression...'
    for bsnode in bsnodes:
        #bsnode=bsnodes[0]
        exname=ctrlName+'__'+bsnode.replace('_BLENDSHAPE','_EXPRESSION')
        extext='//'+exname+'\n'
        extext+='//don\'t write custom expression in here!,the script will delete this scirpt first before create a new expression\n\n'
        if cmds.objExists(exname):
            cmds.delete(exname)
        #bsattrlen=cmds.blendShape(bsnode,q=1,wc=1)
        bsattrlen=edo_getMaxLocalIndexFromPhysicalCount(bsnode+'.weight')+1
        for i in range(0,bsattrlen):
            #i=0
            print i
            ctrlattrname=''
            if endstr=='CTRL' or endstr=='CONNECT':
                bsattr=cmds.aliasAttr(bsnode+'.weight['+str(i)+']',q=1)
                m=bsattr
                bsattrname=bsnode+'.'+m
                print m
                if not ctrlName in m or '___' in m:
                    print m+' ... pass'
                    continue
                else:
                    print m+' ... addex'
                    ctrlattrname=m.split('__')[len(m.split('__'))-1]
                    ctrlattrname=ctrlattrname.replace(sfix+'_','_FRAME.')
                    ctrlattrname=ctrlattrname.replace('fourAxis','fourAxis_')
                    extext+=bsattrname+'='+ctrlattrname+';\n'
            else:
                bsattr=cmds.aliasAttr(bsnode+'.weight['+str(i)+']',q=1)
                m=bsattr
                bsattrname=bsnode+'.'+m
                print m
                if not ctrlName in m:
                    print m+' ... pass'
                    continue
                else:
                    print m+' ... addex'
                    tmp=m.split('___')
                    st=tmp[0].split('__')[-1]
                    tmp.remove(tmp[0])
                    ctrlattrname=st
                    for t in tmp:
                        ctrlattrname+=('___'+t)
                    ctrlattrname=ctrlattrname+'.multiplyValue'
                    extext+=bsattrname+'='+ctrlattrname+';\n'
        print 'add expression'
        print exname+' : \n'+extext+'\n'
        try:
            cmds.expression(n=exname,s=extext)
        except:
            print 'you probably connect some attribute to this blendshape attribute, the script can not create expression on it'
        
def edo_splitBlendshapeWeightStr(bsmesh,weight):
    #bsmesh='BS__pSphere1__6000__aaa_CTRL_up'
    sp=bsmesh.split('__')
    rbsmesh=''
    if not sp[2]==weight:
        rbsmesh=bsmesh
        return rbsmesh
    for t in range(0,len(sp)):
        if t==2:
            continue
        rbsmesh=rbsmesh+sp[t]+'__'
    print rbsmesh[:-2]
    return rbsmesh[:-2]

def edo_getSelectedBlendshape(filedObject,blendshapeListLw):
    #filedObject=ui.blendshapeNameLe
    #blendshapeListLw=ui.blendshapeListLw
    sels=cmds.ls(sl=1,type='blendShape')
    if sels:
        sel=sels[0]
        #cmds.textField('blendshapeNameLe',e=1,tx=sel)
        #filedObject=blendshapeNameLe
        #blendshapeListLw=blendshapeListLw
        filedObject.setText(sel)
        edo_getBlendshapeAttrList(blendshapeListLw,sel)

def edo_getBlendshapeAttrList(blendshapeListLw,blendshape):
    #blendshape='pengzhuangti__BLENDSHAPE'
    #blendshapeListLw
    #wc=cmds.blendShape(blendshape,q=1,wc=1)
    wc=edo_getMaxLocalIndexFromPhysicalCount(blendshape+'.weight')+1
    attrlist=[]
    blendshapeListLw.clear() 
    im=max(5000,wc)
    for w in range(0,im):
        #print w
        #w=1
        attr=blendshape+'.weight['+str(w)+']'
        aattr=cmds.aliasAttr(attr,q=1)
        #print aattr
        if (not aattr in attrlist) and (not aattr==''):
            attrlist.append(aattr)
            blendshapeListLw.addItem(aattr)
    it=blendshapeListLw.item(0)
    blendshapeListLw.setCurrentItem(it)

#edo_getBlendshapeAttrInbetweenList(blendshapeNameLe,blendshapeListLw,inbetweenListLw)
def edo_getBlendshapeAttrInbetweenList(blendshapeNameLe,blendshapeListLw,inbetweenListLw):
    #blendshapeNameLe=ui.blendshapeNameLe
    #blendshapeListLw=ui.blendshapeListLw
    #inbetweenListLw=ui.inbetweenListLw
    #keepConnectionCb=ui.keepConnectionCb
    print 'getBlendshapeAttrInbetweenList...'
    bsname=str(blendshapeNameLe.text())
    inbetweenListLw.clear()
    #bsname='pSphere1__BLENDSHAPE'
    n=blendshapeListLw.count()
    #QselectAttrs=[]
    #for i in range(n):
    #    it = blendshapeListLw.item(i)
    #    if it.isSelected():
    #        QselectAttrs.append(it)
    #ci=len(QselectAttrs)
    #print 'select items count : '+str(ci)
    #if not ci==1:
    #    return True
    sis=[str(blendshapeListLw.currentItem().text())]
    if sis:
        si=sis[0]
        id=edo_targetIsInBlendShapeWeightId(si,bsname)
        #.inputTarget[0].inputTargetGroup[0].inputTargetItem[6000].inputGeomTarget
        attrname=bsname+'.inputTarget[0].inputTargetGroup['+str(id)+'].inputTargetItem'
        attrlist=cmds.getAttr(attrname,mi=1)
    if attrlist==None:
        return False
    for a in attrlist:
        #a=attrlist[0]
        print a
        inbetweenListLw.addItem(str(a)+':'+str(((float(a)-5000)/1000)))
        it=inbetweenListLw.item(0)
        inbetweenListLw.setCurrentItem(it)

def edo_getAllQWidgetItemList(QWidgetList,type='str',selectOnly=0):
    #QWidgetList=inbetweenListLw
    #selectOnly=0
    ct=QWidgetList.count()
    QselectAttrs=[]
    selectAttrs=[]
    for i in range(0,ct):
        #i=1
        tt=QWidgetList.item(i)
        t=str(tt.text())
        if selectOnly==0:
            print 'pick up all inbetween ... '
            if not t in selectAttrs:
                QselectAttrs.append(tt)
                selectAttrs.append(t)
        else:
            if tt.isSelected():
                print 'pick up selected inbetween ... '
                if not t in selectAttrs:
                    QselectAttrs.append(tt)
                    selectAttrs.append(t)
    if type=='str':
        return selectAttrs
    if type=='QListWidgetItem':
        return QselectAttrs

#edo_pickupSelectedBlendshape(ui.blendshapeNameLe,ui.blendshapeListLw,ui.inbetweenListLw,ui.keepConnectionCb,all=0)
def edo_pickupSelectedBlendshape(blendshapeNameLe,blendshapeListLw,inbetweenListLw,keepConnectionCb,all=0,inbOnly=0):
    #blendshapeNameLe=ui.blendshapeNameLe
    #blendshapeListLw=ui.blendshapeListLw
    #inbetweenListLw=ui.inbetweenListLw
    #keepConnectionCb=ui.keepConnectionCb
    #all=1
    #inbOnly=0
    sels=cmds.ls(sl=1,type='transform')
    if not sels:
        return False
    sel=sels[0]
    sks=edo_lsDgGraph.edo_findNodeFromHis(sel,'skinCluster')
    sk=''
    if sks:
        sk=sks[0]
        cmds.setAttr(sk+'.nodeState',1)
    cb=keepConnectionCb.isChecked()
    bsname=str(blendshapeNameLe.text())
    QselectAttrs=[]
    n=blendshapeListLw.count()
    for i in range(n):
        it = blendshapeListLw.item(i)
        if it.isSelected():
            QselectAttrs.append(it)
    if all==1:
        selectAttrs=[]
        print 'get all blendshape...'
        QselectAttrs=edo_getAllQWidgetItemList(blendshapeListLw,'QListWidgetItem',0)
    #print QselectAttrs
    if QselectAttrs:
        #sc=len(selectAttrs)
        for sii in QselectAttrs:
            #sii=QselectAttrs[1]
            si=str(sii.text())
            print si
            blendshapeListLw.setCurrentItem(sii)
            state=edo_getBlendshapeAttrInbetweenList(blendshapeNameLe,blendshapeListLw,inbetweenListLw)
            if state==False:
                continue
            inbetweenList=edo_getAllQWidgetItemList(inbetweenListLw,'str',inbOnly)            
            input=cmds.listConnections(bsname+'.'+si,d=0,s=1,p=1)
            if input:
                cmds.disconnectAttr(input[0],bsname+'.'+si)
            id=edo_targetIsInBlendShapeWeightId(si,bsname)
            attrname=bsname+'.inputTarget[0].inputTargetGroup['+str(id)+'].inputTargetItem'
            for ib in inbetweenList:
                #ib=inbetweenList[0]
                t=ib.split(':')
                p=t[0]
                w=float(t[1])
                cmds.setAttr(bsname+'.'+si,w)
                mname=si.replace(sel,sel+'_'+p+'_',1)
                tm=cmds.duplicate(sel,n=mname)[0]
                cmds.setAttr(bsname+'.'+si,0.0)
                frame=tm.split('__')[-1]
                if frame==tm:
                    tm=cmds.rename(tm,sel+'_'+p)
                if cmds.objExists(frame):
                    cmds.parent(tm,frame)
                    edo_setBlendShapeMeshTransform(frame)
                else:
                    try:
                        cmds.parent(tm,w=1)
                    except:
                        print tm+'... has already parent in world!'
                    nname=si+'_'+p
                    tm=cmds.rename(tm,nname)
                    bb=cmds.xform(sel,q=1,os=1,bb=1)
                    print bb
                    h=bb[4]-bb[1]
                    print h
                    cmds.move(0,h*1.2,0,tm,r=1,os=1,ws=1)
                if cb==1:
                    cmds.connectAttr(tm+'.worldMesh[0]',bsname+'.inputTarget[0].inputTargetGroup['+str(id)+'].inputTargetItem['+p+'].inputGeomTarget',f=1)
            if input:
                cmds.connectAttr(input[0],bsname+'.'+si,f=1)
    if not sk=='':
        cmds.setAttr(sk+'.nodeState',0)
        
def edo_getMaxLocalIndexFromPhysicalCount(attrname):
    #attrname=bsnode+'.weight'
    sps=attrname.split('.')
    objname=sps[0]
    attr=sps[1]
    msl=om.MSelectionList()
    om.MGlobal.getSelectionListByName(objname,msl)
    obj=om.MObject()
    msl.getDependNode(0,obj)
    #obj.apiTypeStr()
    mfndg=om.MFnDependencyNode(obj)
    plug=mfndg.findPlug(attr)
    wc=plug.numElements()
    wc=wc-1
    if wc<0:
        return wc
    plug_c=plug.elementByPhysicalIndex(wc)
    maxlocalIndex=plug_c.logicalIndex()
    return maxlocalIndex
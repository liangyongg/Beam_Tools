import maya.cmds as cmds
import edo_skeletonDrivingBallToolUI
import edo_general.edo_loadPlugin as ELPLUGIN
import edo_autoConnectBlendshapesInbetweenUI.edo_mathBlendShapeUI as edo_mathBlendShapeCmd
import edo_general.edo_lockAndUnlockTransform as edo_lockAndUnlockTransform
import edo_skeletonDrivingBallToolUI.edo_autoConnectBlendShapes as edo_skautoConnectBlendShapes
reload(edo_skautoConnectBlendShapes)

mllpath=edo_skeletonDrivingBallToolUI.__file__.replace('python\\edo_skeletonDrivingBallToolUI\\__init__.pyc','mll').replace('\\','/')

#edo_autoConnectCorrectBlendShape(1)
def edo_autoConnectCorrectBlendShape(clearbs=1):
    #axis=8
    sels=cmds.ls(sl=1)
    if len(sels)>=3:
        target=sels[0]
        skmesh=sels[1]
        skdbf=sels[2]
        dctrl=skdbf.replace('_FRAME','_CONNECT')
        #record driver angle
        drsk=''
        drsks=None
        if cmds.objExists(skdbf+'.SKDB'):
            drsks=cmds.listConnections(skdbf+'.SKDB',s=1,d=0)
        if drsks:
            drsk=drsks[0]
        else:
            drsk=edo_findoutDriverSkeletonFromSKDB(skdbf)
        maxrt=edo_getSKDBCurrenctAttrFromAttrs(skdbf)
        if float(maxrt.split(':')[1])<=0.001:
            print 'attributes are too small,please repose your character'
            return False
        #rcattr=''
        #if not mr=='':
        #    rcattr=skdbf+'.'+drsk+'__'+mr
        #if rcattr=='':
        #    print 'the joint doesnt have any rotation, so you don\t need add any correct blendshape to it'
        #    return
        ##rewrite rotation Value list 
        #edo_rewriteRotationValueList(skdbf,rcattr,mv,mr)
        edo_rewriteDirValueList(skdbf,maxrt,drsk)
        #auto calculate and connect  blendshape
        fbs=edo_calculateBlendShape(target,skmesh)
        axis=4
        if cmds.objExists(skdbf.replace('FRAME','eightDirPlane_curve')):
            axis=8
        mxattr=''
        if axis==4:
            mxattr=edo_getSKDBmaxCurrentAttrFromFourAttrs(skdbf)
        else:
            mxattr=edo_getSKDBmaxCurrentAttrFromEightAttrs(skdbf)
        outs = cmds.listConnections(skdbf+'.'+mxattr[0],d=1,s=0,p=1)
        animCurves=[]
        if outs:
            for out in outs:
                #out = outs[0]
                outobj = cmds.ls(out.split('.')[0],type='animCurve')
                if outobj:
                    animCurves.append(outobj[0])
        #print animCurve
        dirvalue = mxattr[1]
        outvalue = mxattr[1]
        cbs=edo_findNodeFromHis(skmesh,'blendShape')
        canim=''
        if not cbs==None:
            if animCurves:
                for am in animCurves:
                    #am = animCurves[0]
                    outputs = cmds.listConnections(am,s=0,d=1)
                    if outputs:
                        for output in outputs:
                            #output = outputs[0]
                            if output == cbs:
                                canim=am
        if not canim=='':
            outvalue=cmds.getAttr(canim+'.output')
        cmds.select(fbs)
        #skmesh=skmesh+'_'
        cmds.select(skmesh,add=1)
        bsmeshes=edo_skautoConnectBlendShapes.edo_renameBlendShapeMeshInbetween(outvalue)
        cmds.parent(bsmeshes,dctrl+'_'+mxattr[0])
        cmds.select(dctrl)
        allbms=edo_skautoConnectBlendShapes.edo_autoConnectBlendshapes()
        allbms=cmds.ls(bsmeshes.split('__')[0]+'__'+bsmeshes.split('__')[1]+'*',type='transform')
        #delete blendshape mesh
        if clearbs==1:
            print 'clear blendshape : '+ bsmeshes
            if allbms:
                for bm in allbms:
                    #bm=allbms[0]
                    if cmds.objExists(bm):
                        shs=cmds.listRelatives(bm,p=1,pa=1)
                        if shs:
                            sh=shs[0]
                            if dctrl+'_' in sh:
                                cmds.delete(bm)
        #convert expression to setDriven Key
        cbs=edo_findNodeFromHis(skmesh,'blendShape')
        if cbs==skmesh+'_BLENDSHAPE':
            #cbs mxattr[1] 
            edo_convertBlendShapeDrivingExToSdk(cbs,canim,dirvalue,outvalue)
        return [maxrt]

def edo_autoMirrorBlendShapes(mesh,skdbf,rp=['L_','R_']):
    #mesh='test_'
    #skdbf='L_jnt1_FRAME'
    bs=mesh+'_BLENDSHAPE'
    otherside=skdbf.replace(rp[0],rp[1])
    if otherside==skdbf:
        print 'you do not need mirror the ['+skdbf+'] to itself ['+otherside+']'
        return False
    if cmds.objExists(bs) and cmds.objExists(skdbf) and cmds.objExists(otherside) and cmds.objExists(mesh):
        print 'pick up all targets to '+skdbf
        print 'clear all targets in '+otherside

def edo_findAllRecordedRotationAttributeFromSKDB(skdbf):
    attrs=[]
    if cmds.objExists(skdbf+'.up_data'):
        attrs.append(skdbf+'.up_data')
    if cmds.objExists(skdbf+'.dn_data'):
        attrs.append(skdbf+'.dn_data')
    if cmds.objExists(skdbf+'.lf_data'):
        attrs.append(skdbf+'.lf_data')
    if cmds.objExists(skdbf+'.rt_data'):
        attrs.append(skdbf+'.rt_data')
    if cmds.objExists(skdbf+'.lfup_data'):
        attrs.append(skdbf+'.lfup_data')
    if cmds.objExists(skdbf+'.lfdn_data'):
        attrs.append(skdbf+'.lfdn_data')
    if cmds.objExists(skdbf+'.rtup_data'):
        attrs.append(skdbf+'.rtup_data')
    if cmds.objExists(skdbf+'.rtdn_data'):
        attrs.append(skdbf+'.rtdn_data')
    print attrs
    return attrs
    
def edo_findAllRecordedRotationAttribute(skdbf):
    alllistattr=[]
    if not cmds.objExists(skdbf):
        return False
    drsk=''
    drsks=cmds.listConnections(skdbf+'.SKDB',s=1,d=0)
    if drsks:
        drsk=drsks[0]
    else:
        drsk=edo_findoutDriverSkeletonFromSKDB(skdbf)
    if not drsk:
        return False
    drx=skdbf+'.'+drsk+'__rx'
    if cmds.objExists(drx):
        alllistattr.append(drx)
    dry=skdbf+'.'+drsk+'__ry'
    if cmds.objExists(dry):
        alllistattr.append(dry)
    drz=skdbf+'.'+drsk+'__rz'
    if cmds.objExists(drz):
        alllistattr.append(drz)
    print alllistattr
    return alllistattr

def edo_rewriteDirValueList(skdbf,maxrt,drsk):
    rx=cmds.getAttr(drsk+'.rx')
    ry=cmds.getAttr(drsk+'.ry')
    rz=cmds.getAttr(drsk+'.rz')
    tmp=maxrt.split(':')
    attr=tmp[0]
    tx=cmds.getAttr(skdbf+'.'+attr+'_data')
    rotations=str(rx)+','+str(ry)+','+str(rz)
    data=maxrt+':'+rotations+';'
    if tx=='' or tx==None:
        print 'first time write data'
        cmds.setAttr(skdbf+'.'+attr+'_data',data,type='string')
    else:
        datas=tx.split(';')[:-1]
        ntx=''
        for txd in datas:
            #txd=datas[1]
            sp=txd.split(':')
            ad=sp[0]+':'+sp[1]
            if not maxrt==ad:
               ntx=ntx+txd+';'
        print ntx
        ntx=ntx+data
        cmds.setAttr(skdbf+'.'+attr+'_data',ntx,type='string')
        
def edo_rewriteRotationValueList(skdbf,rcattr,mv,mr):
    rl=[]
    drsk=''
    drsks=cmds.listConnections(skdbf+'.SKDB',s=1,d=0)
    if drsks:
        drsk=drsks[0]
    else:
        drsk=edo_findoutDriverSkeletonFromSKDB(skdbf)
    if not drsk:
        return False
    if cmds.objExists(rcattr):
        rl=cmds.getAttr(skdbf+'.'+drsk+'__'+mr)[0]
        cmds.deleteAttr(skdbf+'.'+drsk+'__'+mr)
    cmds.addAttr(skdbf,ln=drsk+'__'+mr,at='double',multi=True)
    if rl:
        rl=list(rl)
    if rl:
        if mv in list(rl):
            print 'remove this rotate value form list'
            rl.remove(mv)
    rl.append(mv)
    print 'reset the rotation list to: \n'
    print rl
    i=0
    for r in rl:
        #cmds.setAttr(skdbf+'.'+drsk+'__'+mr+'[2]',rl[0])
        cmds.setAttr(skdbf+'.'+drsk+'__'+mr+'['+str(i)+']',rl[i])
        i=i+1

def edo_findoutDriverSkeletonFromSKDB(skdb):
    #skdb=skdbf
    if not cmds.objExists(skdb):
        print skdb+' dose not exists'
        return False
    skdbc=skdb.replace('_FRAME','_centerLoc')
    cs=cmds.listConnections(skdbc+'.rotateX',s=1,d=0)
    if cs:
        c=cs[0]
        if 'Constraint' in cmds.nodeType(c):
            ss=cmds.listConnections(c+'.target[0].targetRotate',s=1,d=0)
            if ss:
                s=ss[0]
                return s
    return False
        
        
def edo_convertBlendShapeDrivingExToSdk(cbs,canim,dirvalue,outvalue):
    #cbs mxattr[1]
    #value =  mxattr[1]
    wc=cmds.blendShape(cbs,q=1,wc=1)
    for i in range(0,wc):
        #i=0
        attr=cbs+'.weight['+str(i)+']'
        nattr=cbs+'.'+cmds.aliasAttr(attr,q=1)
        connects=cmds.listConnections(attr,s=1,d=0)
        if connects:
            connect=connects[0]
            if cmds.nodeType(connect)=='expression' and cbs.replace('__BLENDSHAPE','__EXPRESSION') in connect:
                print 'convert expression to setDrivenKey'
                drivers=cmds.listConnections(connect+'.input',s=1,d=0,p=1)
                if drivers:
                    driver=drivers[0]
                    cmds.delete(connect.split('.')[0])
                    edo_createSetDrivenKey(driver,nattr,dirvalue,outvalue)
            else:
                ans=cmds.ls(connect,type='animCurve')
                if ans:
                    an=ans[0]
                    if not an==canim:
                        continue
                    drivers=cmds.listConnections(an+'.input',s=1,d=0,p=1)
                    if drivers:
                        driver=drivers[0]
                        print 'add set driven key frame on ... '+nattr
                        cmds.setDrivenKeyframe(nattr,cd=driver,dv=float(dirvalue),v=float(outvalue),itt='linear',ott='linear')
        else:
            dvattr=nattr.split('__')[-1].replace('_CONNECT_','_FRAME.').replace('fourAxis','fourAxis_')
            print 'check ... '+dvattr + ' is existed?'
            if cmds.objExists(dvattr):
                print 'add setNewDrivenKeyFrame...'
                edo_createSetDrivenKey(dvattr,nattr,dirvalue,outvalue)

def edo_createSetDrivenKey(driver,driven,dirvalue,outvalue):
    #driven=nattr
    sdkn=driven.replace('.','_')
    cmds.setDrivenKeyframe(driven,cd=driver,dv=0.0,v=0.0,itt='linear',ott='linear')
    cmds.setDrivenKeyframe(driven,cd=driver,dv=dirvalue,v=outvalue,itt='linear',ott='linear')
    
def edo_getSKDBdriverSkMaxAngle(jnt,collect=1):
    #jnt=drsk
    rx=cmds.getAttr(jnt+'.rx')
    ry=cmds.getAttr(jnt+'.ry')
    rz=cmds.getAttr(jnt+'.rz')
    mxattr=''
    mxv=0
    vl=[rx,ry,rz]
    al=['rx','ry','rz']
    c=len(vl)
    for i in range(0,c):
        #v=vl[0]
        v=vl[i]
        a=al[i]
        #print v
        #abs(-10)
        if abs(v)>abs(mxv):
            print str(v) + '..bigger than..' + str(mxv) 
            mxattr=a
            mxv=v
    print [mxattr,mxv]
    return [mxattr,mxv]

def edo_getSKDBCurrenctAttrFromAttrs(skdbf):
    f=cmds.getAttr(skdbf+'.up')
    d=cmds.getAttr(skdbf+'.dn')
    l=cmds.getAttr(skdbf+'.lf')
    r=cmds.getAttr(skdbf+'.rt')
    lu=cmds.getAttr(skdbf+'.lfup')
    ru=cmds.getAttr(skdbf+'.rtup')
    ld=cmds.getAttr(skdbf+'.lfdn')
    rd=cmds.getAttr(skdbf+'.rtdn')
    mxattr=''
    mxv=-1
    vl=[f,d,l,r,lu,ru,ld,rd]
    al=['up','dn','lf','rt','lfup','rtup','lfdn','rtdn']
    c=len(vl)
    for i in range(0,c):
        #v=vl[0]
        v=vl[i]
        a=al[i]
        #print v
        if v>mxv:
            #print str(v) + '..bigger than..' + str(mxv) 
            mxattr=a
            mxv=v
    print mxattr+':'+str(mxv)
    return mxattr+':'+str(mxv)
   
def edo_getSKDBmaxCurrentAttrFromEightAttrs(skdbf):
    #skdbf = 'joint2_FRAME'
    f=cmds.getAttr(skdbf+'.up')
    d=cmds.getAttr(skdbf+'.dn')
    l=cmds.getAttr(skdbf+'.lf')
    r=cmds.getAttr(skdbf+'.rt')
    lu=cmds.getAttr(skdbf+'.lfup')
    ru=cmds.getAttr(skdbf+'.rtup')
    ld=cmds.getAttr(skdbf+'.lfdn')
    rd=cmds.getAttr(skdbf+'.rtdn')
    mxattr=''
    mxv=-1
    vl=[f,d,l,r,lu,ru,ld,rd]
    al=['up','dn','lf','rt','lfup','rtup','lfdn','rtdn']
    c=len(vl)
    for i in range(0,c):
        #v=vl[0]
        v=vl[i]
        a=al[i]
        #print v
        if v>mxv:
            #print str(v) + '..bigger than..' + str(mxv) 
            mxattr=a
            mxv=v
    print [mxattr,mxv]
    return [mxattr,mxv]
    
def edo_getSKDBmaxCurrentAttrFromFourAttrs(skdbf):
    f=cmds.getAttr(skdbf+'.fourAxis_up')
    d=cmds.getAttr(skdbf+'.fourAxis_dn')
    l=cmds.getAttr(skdbf+'.fourAxis_lf')
    r=cmds.getAttr(skdbf+'.fourAxis_rt')
    mxattr=''
    mxv=-1
    vl=[f,d,l,r]
    al=['fourAxisup','fourAxisdn','fourAxislf','fourAxisrt']
    c=len(vl)
    for i in range(0,c):
        #v=vl[0]
        v=vl[i]
        a=al[i]
        #print v
        if v>mxv:
            #print str(v) + '..bigger than..' + str(mxv) 
            mxattr=a
            mxv=v
    print [mxattr,mxv]
    return [mxattr,mxv]

#fbs=edo_calculateBlendShape(cmds.ls(sl=1)[0],cmds.ls(sl=1)[1])
def edo_calculateBlendShape(target,skmesh,method=2):
    #target='body_skin_proxy2'
    #skmesh='body_skin_proxy'
    #load plugin
    ELPLUGIN.edo_loadPlugin('geometryComputer.mll')
    sk=edo_findNodeFromHis(skmesh,'skinCluster')
    tw=edo_findNodeFromHis(skmesh,'tweak')
    bs=edo_findNodeFromHis(skmesh,'blendShape')
    org=''
    orgid=-1
    skorg=cmds.listRelatives(skmesh,s=1,pa=1)
    if not skorg:
        cmds.error('skin mesh has no org node')
        return False
    norg=cmds.listRelatives(skmesh,s=1,pa=1,ni=1)[0]
    skorg.remove(norg)
    i=0
    for so in skorg:
        #so=skorg[1]
        if cmds.listConnections(so+'.worldMesh',d=1,s=0,p=1):
            org=so
            orgid=i
        i+=1
    if org=='':
        cmds.error('skin mesh has no org node')
        return False
    tm=cmds.duplicate(org,n='CALCULATE_BLENDSHAPE_TARGETMESH')[0]
    shs=cmds.listRelatives(tm,s=1,pa=1)
    if not shs:
        cmds.error('skin mesh has no org node')
        return False
    sh=cmds.listRelatives(tm,s=1,pa=1,ni=1)[0]
    shs.remove(sh)
    cmds.delete(sh)
    org =shs[orgid]
    osh=cmds.rename(org,tm+'Shape')
    cmds.setAttr(osh+'.io',0)
    #turnOff blendShape
    bsst=1
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
    finalbs=cmds.duplicate(tm)[0]
    cmds.delete(tm)
    try:
        cmds.setAttr(bs+'.nodeState',bsst)
    except:
        print 'turn off the blendShape effect has failed,please check the result.'
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
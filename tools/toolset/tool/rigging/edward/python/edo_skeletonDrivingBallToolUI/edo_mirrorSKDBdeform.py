import maya.cmds as cmds
import edo_autoConnectBlendshapesInbetweenUI.edo_mirrorBlendShape as edo_mirrorBlendShape
import edo_autoConnectBlendshapesInbetweenUI.edo_autoConnectBlendShapes as edo_autoConnectBlendShapes
import edo_general.edo_lockAndUnlockTransform as edo_lockAndUnlockTransform
#reload(edo_mirrorBlendShape)
#edo_mirrorSKDBdeform(['L_','R_'],1) 
#edo_mirrorSKDBdeform(['L_','R_'],0)  
def edo_mirrorSKDBdeform(rp=['L_','R_'],mode=0):
    #mode=1
    sels=cmds.ls(sl=1)
    mesh=sels[0]
    skdbs=sels[1:]
    cmds.select(skdbs,r=1)
    edo_mirrorSKDBvalue(rp)
    #
    af=0
    af=edo_checkTheEndStr(mesh)
    if af==1:
        mesh=mesh+'_'
    oaf=0
    omesh=''
    if mode==1:
        omesh=mesh.replace(rp[0],rp[1])
        if omesh[-1]=='_':
            omesh=omesh[:-1]
        oaf=edo_checkTheEndStr(omesh)
        if not omesh[-1]=='_':
            omesh=omesh+'_'
        if not cmds.objExists(omesh):
            print 'can not find the mesh in the other side'
            return False
    #mirrorBs
    allbs=edo_findAllBlendshapeInTheFrame(rp)
    fallbs=[]
    for bs in allbs:
        #bs=allbs[0]
        edo_lockAndUnlockTransform.edo_unLockReferenceObjectTransformAttrs(bs)
        if mesh in bs:
            fallbs.append(bs)
    allbs=fallbs
    allmirrorbs=[]
    if mode==0:
        edo_lockAndUnlockTransform.edo_unLockReferenceObjectTransformAttrs(mesh)
        orgmesh=cmds.duplicate(mesh,n='ORG_'+mesh)[0]
        cmds.select(orgmesh,r=1)
        cmds.select(allbs,add=1)
        allmirrorbs=edo_mirrorBlendShape.edo_mirrorBlendShape()
        cmds.delete(orgmesh)
    if mode==1:
        for bs in allbs:
            #bs=allbs[0]
            dbs=cmds.duplicate(bs,n=bs.replace(rp[0],rp[1]))[0]
            cmds.parent(dbs,w=1)
            cmds.xform(dbs,ws=1,t=[0,0,0],ro=[0,0,0],s=[-1,1,1])
            cmds.makeIdentity(dbs,a=1,t=0,r=1,s=1,n=0)
            allmirrorbs.append(dbs)
    #cmds.select(allmirrorbs)
    mirroredCurve=[]
    for bs in allmirrorbs:
        #bs=allmirrorbs[0]
        #bsname=bs.split()
        #rbs=bs.replace('CTRR_','CTRL_')
        rbs=bs
        rbs=cmds.rename(bs,rbs)
        frame=rbs.split('__')[-1]
        if cmds.objExists(frame):
            cmds.parent(rbs,frame)
            ms=frame.split('_CONNECT')[0]+'_CONNECT'
            if cmds.objExists(ms):
                cmds.select(ms,r=1)
                #reload(edo_autoConnectBlendShapes)
                allbms=edo_autoConnectBlendShapes.edo_autoConnectBlendshapes()
                #delete blendshape mesh
                cbs=''
                #cbs=allbms[2]
                for bms in allbms:
                    if bms:
                        bms=bms[0]
                        if cmds.objExists(bms):
                            cmds.delete(bms)
                            cbs=bms
                if cmds.objExists(rbs):
                    cmds.delete(rbs)
                tmp=rbs.split('__')
                rbs=tmp[0]+'__'+tmp[1]+'__'+tmp[3]
                if cmds.objExists(rbs):
                    cmds.delete(rbs)
                #mirror set driven key
                #if cbs=='':
                #    continue
                bsn=rbs.split('__')[1]+'__BLENDSHAPE'
                lbsn=bsn.replace(rp[1],rp[0])
                tmp=rbs.replace(rp[1],rp[0]).split('__')
                ocbs=tmp[0]+'__'+tmp[1]+'__'+tmp[2]
                if cmds.objExists(lbsn+'.'+ocbs):
                    anc=cmds.listConnections(lbsn+'.'+ocbs,s=1,d=0,p=1)
                    if anc:
                        an=anc[0]
                        if cmds.nodeType(an)[0:9]=='animCurve':
                            print 'duplicate anim curve'
                            if an in mirroredCurve:
                                continue
                            if cmds.objExists(an.split('.')[0].replace(rp[0],rp[1])):
                                print 'delete animCurve ... '+an.split('.')[0].replace(rp[0],rp[1])
                                cmds.delete(an.split('.')[0].replace(rp[0],rp[1]))
                            oc=cmds.duplicate(an,n=an.split('.')[0].replace(rp[0],rp[1]))
                            mirroredCurve.append(an)
                            if oc:
                                c=oc[0]
                                #rnc=c.replace('_CTRR','_CTRL')
                                rnc=c
                                #if cmds.objExists(rnc):
                                #    print 'delete animCurve ... '+rnc
                                #    cmds.delete(rnc)
                                #rnc=cmds.rename(c,rnc)
                                #bsattr=(bsn+'.'+ocbs).replace(rp[0],rp[1]).replace('_CTRR','_CTRL')
                                bsattr=(bsn+'.'+ocbs).replace(rp[0],rp[1])
                                if cmds.objExists(bsattr):
                                    cmds.connectAttr(rnc+'.output',bsattr,f=1)
                                inattr=rnc.split('__')[-1].replace('_CONNECT_','_FRAME.')
                                if cmds.objExists(inattr):
                                    cmds.connectAttr(inattr,rnc+'.input',f=1)
                                    print 'mirror  ..  ' + bs +'  ..  was successful.'
    if af==1:
        cmds.rename(mesh,mesh[:-1])
    if oaf==1:
        cmds.rename(omesh,omesh[:-1])
    cmds.delete(allbs)

def edo_checkTheEndStr(name,st='_'):
    #name='shoes_a_R'
    if name[-1]=='_':
        return 0
    else:
        if cmds.objExists(name):
            nname=name+'_'
            cmds.rename(name,nname)
            return 1
        else:
            return 0

#rp=['L_','R_']
#mesh='body_collide_sk_'
def edo_findAllBlendshapeInTheFrame(rp=['L_','R_']):
    dir=rp[0]
    rpl=rp[1]
    sels=cmds.ls(sl=1)
    allMeshes=[]
    for sel in sels:
        #sel=sels[0]
        ctrlName=sel.replace('_FRAME','_CONNECT')
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
            continue
    print allMeshes
    return allMeshes
    
def edo_combineAllList(finalList,combineList):
    if combineList==None or combineList==[]:
        return finalList
    finalList+=combineList


def edo_mirrorSKDBvalue(rp=['L_','R_']):
    dir=rp[0]
    rpl=rp[1]
    sels=cmds.ls(sl=1)
    for sel in sels:
        #sel=sels[0]
        remap=sel.replace('_FRAME','_eightDirPlane_curve')
        ossel=sel.replace(dir,rpl)
        osremap=remap.replace(dir,rpl)
        if cmds.objExists(sel) and cmds.objExists(ossel) and cmds.objExists(remap) and cmds.objExists(osremap):
            ao=cmds.getAttr(sel+'.Axis_4_or_8')
            rv=cmds.getAttr(remap+'.remapDisWeight')
            cmds.setAttr(ossel+'.Axis_4_or_8',ao)
            cmds.setAttr(osremap+'.remapDisWeight',rv)
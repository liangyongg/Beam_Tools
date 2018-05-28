import maya.cmds as cmds
import maya.OpenMaya as om
import math

#edo_ThreePointMatherAsSelectedListCT([0,1,2],[0,1,2],0)
def edo_ThreePointMatherAsSelectedListCT(sourcevtx=[0,1,2],targetvtx=[0,1,2],SHEAR=0,cpb=0):
    sels=cmds.ls(sl=1)
    if sels:
        for sel in sels:
            edo_unlockAllTransform(sel)
        source=sels[0]
        sels.remove(source)
        l=len(sels)
        id=0
        for target in sels:
            #target=sels[0]
            c=str(id)+'/'+str(l)
            print c+' : make  '+target +'  match to  '+source
            nds=edo_ThreePointMatherCmd(source,target,sourcevtx,targetvtx,SHEAR)
            grps=edo_createMatchCtrlRig(target,nds,cpb)
            print nds
            if cmds.objExists('GRP_EDO_TRIANGEL_MATCH'):
                cmds.parent(grps[1],'GRP_EDO_TRIANGEL_MATCH')
            id=id+1
            
def edo_createMatchCtrlRig(name,nds,cpb):
    #name=target
    #nds=nds
    #cpb=0
    ctrlname=name+'_ctrl'
    print 'create contorler'
    ns=edo_createMatchCtrl(ctrlname,'circle',17)
    cmds.parent(ns[1],nds)
    cmds.xform(ns[1],os=1,t=[0,0,0])
    cmds.xform(ns[1],os=1,ro=[0,0,0])
    cmds.parent(ns[1],w=1)
    cmds.xform(ns[1],os=1,s=[1,1,1])
    cmds.delete(nds)
    bb=cmds.xform(name,q=1,os=1,bb=1)
    ssx=bb[3]-bb[0]
    ssz=bb[5]-bb[2]
    bb=cmds.xform(ns[0],q=1,os=1,bb=1)
    csx=bb[3]-bb[0]
    csz=bb[5]-bb[2]
    sx=(ssx/csx)*1.3
    sz=(ssz/csz)*1.3
    cmds.select(ns[0]+'.cv[*]')
    cmds.scale(sx,1,sz,r=1,ocp=1)
    cmds.select(cl=1)
    ps=name
    #cpb=1
    print 'CPB is '+str(cpb)
    for i in range(0,cpb):
        pss=cmds.listRelatives(ps,p=1,pa=1)
        if not pss==None:
            ps=pss[0]
    print ps
    cmds.parentConstraint(ns[0],ps,mo=1)
    cmds.scaleConstraint(ns[0],ps,mo=1)
    return ns

def edo_createMatchCtrl(name,shape='box',colorid=17):
    #name=ctrlname
    #colorid=13
    if shape=='box':
        cmds.curve(n=name,d=1,p=[[-0.5,-0.5,-0.5],[0.5,-0.5,-0.5],[0.5,-0.5,0.5],[-0.5,-0.5,0.5],[-0.5,-0.5,-0.5],[-0.5,0.5,-0.5],[0.5,0.5,-0.5],[0.5,-0.5,-0.5],[0.5,0.5,-0.5],[0.5,0.5,0.5],[0.5,-0.5,0.5],[0.5,0.5,0.5],[-0.5,0.5,0.5],[-0.5,-0.5,0.5],[-0.5,0.5,0.5],[-0.5,0.5,-0.5]])
    if shape=='circle':
        cmds.delete(cmds.circle(ch=1,o=1,nr=[0,1,0],n=name)[1])
    if shape=='square':
        cmds.curve(n=name,d=1,p=[[-10,-10,0],[-10,10,0],[10,10,0],[10,-10,0],[-10,-10,0]])
    cmds.group(name,n='GRP_'+name)
    ss=cmds.listRelatives(name,s=1)[0]
    cmds.rename(ss,name+'Shape')
    cmds.setAttr(name+'Shape.overrideEnabled',1)
    cmds.setAttr(name+'Shape.ovc',colorid)
    return [name,'GRP_'+name]

#edo_ThreePointMatherAsSelectedList([0,1,2],[0,1,2],1)
#edo_ThreePointMatherAsSelectedList([7,3,5],[229,146,226],0)
def edo_ThreePointMatherAsSelectedList(sourcevtx=[0,1,2],targetvtx=[0,1,2],SHEAR=1):
    sels=cmds.ls(sl=1)
    if sels:
        for sel in sels:
            edo_unlockAllTransform(sel)
        source=sels[0]
        sels.remove(source)
        l=len(sels)
        id=0
        for target in sels:
            #target=sels[0]
            c=str(id)+'/'+str(l)
            print c+' : make  '+target +'  match to  '+source
            nds=edo_ThreePointMatherCmd(source,target,sourcevtx,targetvtx,SHEAR)
            print nds
            id=id+1

#edo_ThreePointMatherAsSelectedListMO([0,1,2],[0,1,2],0)  
def edo_ThreePointMatherAsSelectedListMO(sourcevtx=[0,1,2],targetvtx=[0,1,2],SHEAR=1):
    sels=cmds.ls(sl=1)
    if sels:
        for sel in sels:
            edo_unlockAllTransform(sel)
        target=sels[-1]
        sels.remove(target)
        l=len(sels)
        id=0
        for source in sels:
            c=str(id)+'/'+str(l)
            print c+' : make  '+target +'  match to  '+source
            nds=edo_ThreePointMatherCmd(source,target,sourcevtx,targetvtx,SHEAR)
            print nds
            id=id+1

def edo_unlockAllTransform(node):
    #node='MSH_c_hi_mo_ca_1_'
    cmds.setAttr(node+'.t',lock=0)
    cmds.setAttr(node+'.tx',lock=0)
    cmds.setAttr(node+'.ty',lock=0)
    cmds.setAttr(node+'.tz',lock=0)
    cmds.setAttr(node+'.r',lock=0)
    cmds.setAttr(node+'.rx',lock=0)
    cmds.setAttr(node+'.ry',lock=0)
    cmds.setAttr(node+'.rz',lock=0)
    cmds.setAttr(node+'.s',lock=0)
    cmds.setAttr(node+'.sx',lock=0)
    cmds.setAttr(node+'.sy',lock=0)
    cmds.setAttr(node+'.sz',lock=0)
    cmds.setAttr(node+'.sh',lock=0)
    cmds.setAttr(node+'.shxy',lock=0)
    cmds.setAttr(node+'.shxz',lock=0)
    cmds.setAttr(node+'.shyz',lock=0)
    cmds.setAttr(node+'.rp',lock=0)
    cmds.setAttr(node+'.rpx',lock=0)
    cmds.setAttr(node+'.rpy',lock=0)
    cmds.setAttr(node+'.rpz',lock=0)
    cmds.setAttr(node+'.rpt',lock=0)
    cmds.setAttr(node+'.rptx',lock=0)
    cmds.setAttr(node+'.rpty',lock=0)
    cmds.setAttr(node+'.rptz',lock=0)
    cmds.setAttr(node+'.sp',lock=0)
    cmds.setAttr(node+'.spx',lock=0)
    cmds.setAttr(node+'.spy',lock=0)
    cmds.setAttr(node+'.spz',lock=0)
    cmds.setAttr(node+'.spt',lock=0)
    cmds.setAttr(node+'.sptx',lock=0)
    cmds.setAttr(node+'.spty',lock=0)
    cmds.setAttr(node+'.sptz',lock=0)
    cmds.setAttr(node+'.ra',lock=0)
    cmds.setAttr(node+'.rax',lock=0)
    cmds.setAttr(node+'.ray',lock=0)
    cmds.setAttr(node+'.raz',lock=0)
    
#edo_ThreePointMatherCmd('O_002','T_002',[0,1,5],[1,6,5],0)
def edo_ThreePointMatherCmd(source,target,sourcevtx=[0,1,2],targetvtx=[0,1,2],SHEAR=1):
    #source='pSphere1_dsjkabfsa_fsnafsjka_fnsajkfas_fnsajkfwe_fska1'
    #target='group2|pSphere1_dsjkabfsa_fsnafsjka_fnsajkfas_fnsajkfwe_fska'
    #sourcevtx=[0,1,2]
    #targetvtx=[0,1,2]
    #edo_lockPivot(source)
    #edo_lockPivot(target)
    #edo_transferPivot(source,target)
    SOTS=edo_duplicateONTandOHTmodle(source,sourcevtx,SHEAR)
    SONT=SOTS[0]
    SOHT=SOTS[1]
    TOTS=edo_duplicateONTandOHTmodle(target,targetvtx,SHEAR)
    TONT=TOTS[0]
    TOHT=TOTS[1]
    if SHEAR==1:
        #print 'completely match'
        edo_matchTriangles(SONT,TONT,source,target,sourcevtx,targetvtx,SHEAR=1)
    else:
        #print 'no shear match'
        edo_matchTriangles(SONT,TONT,source,target,sourcevtx,targetvtx,SHEAR=0)
    #edo_matchTriangle(SONT,TONT,sourcevtx,targetvtx)
    #edo_matchTriangle(SONT,TONT,sourcevtx,targetvtx)
    #if cmds.objExists('EDO_TRIANGEL_MATCH_'+source):
    #    cmde.delete('EDO_TRIANGEL_MATCH_'+source)
    shortname=source.split('|')[-1]
    ds=cmds.duplicate(source,n='EDO_TRIANGEL_MATCH_'+shortname)[0]
    transferTransform(SOHT,ds)
    edo_setTriangleView(ds,sourcevtx)
    grp='GRP_EDO_TRIANGEL_MATCH'
    if not cmds.objExists(grp):
        grp=cmds.createNode('transform',n=grp)
    cmds.select(ds)
    cmds.parent(ds,grp)
    nds=cmds.ls(sl=1)
    cmds.delete(SOHT)
    return ds

def edo_setTransformZero(t):
    cmds.setAttr(t+'.tx',0)
    cmds.setAttr(t+'.ty',0)
    cmds.setAttr(t+'.tz',0)
    cmds.setAttr(t+'.rx',0)
    cmds.setAttr(t+'.ry',0)
    cmds.setAttr(t+'.rz',0)
    cmds.setAttr(t+'.sx',1)
    cmds.setAttr(t+'.sy',1)
    cmds.setAttr(t+'.sz',1)
    cmds.setAttr(t+'.shxy',0)
    cmds.setAttr(t+'.shxz',0)
    cmds.setAttr(t+'.shyz',0)
    

def edo_setFourByFourMatrixFromMatrix(matrix,disconnect=1):
    #matrix=OMatrix
    lc=cmds.spaceLocator()[0]
    TMatrix=om.MTransformationMatrix(matrix)
    #setTranslate
    Vtranslate=TMatrix.getTranslation(4)
    tx=Vtranslate.x
    ty=Vtranslate.y
    tz=Vtranslate.z
    cmds.setAttr(lc+'.tx',tx)
    cmds.setAttr(lc+'.ty',ty)
    cmds.setAttr(lc+'.tz',tz)
    #setRotation
    Erotation=TMatrix.eulerRotation()
    rx=math.degrees(Erotation.x)
    ry=math.degrees(Erotation.y)
    rz=math.degrees(Erotation.z)
    cmds.setAttr(lc+'.rx',rx)
    cmds.setAttr(lc+'.ry',ry)
    cmds.setAttr(lc+'.rz',rz)
    #setScalse
    mu=om.MScriptUtil()
    mu.createFromDouble(0,0,0)
    dbptr=mu.asDoublePtr()
    TMatrix.getScale(dbptr,4)
    sx=mu.getDoubleArrayItem(dbptr,0)
    sy=mu.getDoubleArrayItem(dbptr,1)
    sz=mu.getDoubleArrayItem(dbptr,2)
    cmds.setAttr(lc+'.sx',sx)
    cmds.setAttr(lc+'.sy',sy)
    cmds.setAttr(lc+'.sz',sz)
    #getShear
    TMatrix.getShear(dbptr,4)
    shxy=mu.getDoubleArrayItem(dbptr,0)
    shxz=mu.getDoubleArrayItem(dbptr,1)
    shyz=mu.getDoubleArrayItem(dbptr,2)
    cmds.setAttr(lc+'.shxy',shxy)
    cmds.setAttr(lc+'.shxz',shxz)
    cmds.setAttr(lc+'.shyz',shyz)
    return lc
    

def edo_createMatrixFromTriangle(triangle,normal=1):
    #triangle=triangle
    #normal=1
    Op=triangle[0]
    Xp=triangle[1]
    Zp=triangle[2]
    OX=[Xp[0]-Op[0],Xp[1]-Op[1],Xp[2]-Op[2]]
    OZ=[Zp[0]-Op[0],Zp[1]-Op[1],Zp[2]-Op[2]]
    MOX=om.MVector(OX[0],OX[1],OX[2])
    MOZ=om.MVector(OZ[0],OZ[1],OZ[2])
    MOY=(MOX^MOZ).normal()
    if (normal==1):
        MOZ=(MOX^MOY).normal()
        MOX=MOX.normal()
    Matrix=om.MMatrix()
    ms=om.MScriptUtil()
    ms.createMatrixFromList([MOX.x,MOX.y,MOX.z,0,  MOY.x,MOY.y,MOY.z,0,  MOZ.x,MOZ.y,MOZ.z,0,  Op[0],Op[1],Op[2],1],Matrix)
    return Matrix
    
def edo_getTransformFromMatirx(Matrix):
    #Matrix=OMatrix.inverse()
    TMatrix=om.MTransformationMatrix(Matrix)
    #get translate
    Vtranslate=TMatrix.getTranslation(4)
    tx=Vtranslate.x
    ty=Vtranslate.y
    tz=Vtranslate.z
    #print 'TX = '+str(tx)+'   ...   '+'TY = '+str(ty)+'   ...   '+'TZ = '+str(tz)+'   ...   '
    #get scale
    double3=om.MScriptUtil()
    double3.createFromDouble(0.0, 0.0, 0.0)
    double3ptr=double3.asDoublePtr()
    TMatrix.getScale(double3ptr,om.MSpace.kWorld)
    sx=double3.getDoubleArrayItem(double3ptr,0)
    sy=double3.getDoubleArrayItem(double3ptr,1)
    sz=double3.getDoubleArrayItem(double3ptr,2)
    #print 'SX = '+str(sx)+'   ...   '+'SY = '+str(sy)+'   ...   '+'SZ = '+str(sz)+'   ...   ' 
    #get shear
    TMatrix.getShear(double3ptr,om.MSpace.kWorld)
    shx=double3.getDoubleArrayItem(double3ptr,0)
    shy=double3.getDoubleArrayItem(double3ptr,1)
    shz=double3.getDoubleArrayItem(double3ptr,2)
    #print 'SHX = '+str(shx)+'   ...   '+'SHY = '+str(shy)+'   ...   '+'SHZ = '+str(shz)+'   ...   '
    #get rotate
    erotation=TMatrix.eulerRotation()
    rx=math.degrees(erotation.x)
    ry=math.degrees(erotation.y)
    rz=math.degrees(erotation.z)
    print 'RX = '+str(rx)+'   ...   '+'RY = '+str(ry)+'   ...   '+'RZ = '+str(rz)+'   ...   '
    return [[tx,ty,tz],[rx,ry,rz],[sx,sy,sz],[shx,shy,shz]]
    
def edo_setTriangleView(obj,vtx=[0,1,2]):
    #obj='O_002'
    if cmds.objExists('TRIANGLEVIWE_'+obj):
        cmds.delete('TRIANGLEVIWE_'+obj)
    Ttriangle=[cmds.xform(obj+'.vtx['+str(vtx[0])+']',q=1,ws=1,t=1),cmds.xform(obj+'.vtx['+str(vtx[1])+']',q=1,ws=1,t=1),cmds.xform(obj+'.vtx['+str(vtx[2])+']',q=1,ws=1,t=1)]
    vm=cmds.polyCreateFacet(n='TRIANGLEVIWE_'+obj,ch=1,tx=1,s=1,p=Ttriangle)
    cmds.parent(vm[0],obj)
    cmds.delete(vm[1])
    cmds.polyColorPerVertex(vm[0],r=1,g=1,b=0,a=1,cdo=1)
    return vm[0]

def edo_duplicateONTandOHTmodle(obj,vtx=[0,1,2],SHEAR=1):
    print 'edo_duplicateONTandOHTmodle'
    #obj=target
    #vtx=[0,1,2]
    #SHEAR=0
    shortname=obj.split('|')[-1]
    ONT=cmds.duplicate(obj,n='ONT_'+shortname)[0]
    OHT=cmds.duplicate(obj,n=ONT.replace('ONT','OHT'))[0]
    cmds.parent(OHT,ONT)
    op=cmds.xform(obj+'.vtx['+str(vtx[0])+']',q=1,ws=1,t=1)
    cmds.xform(ONT,ws=1,piv=op)
    triangle=[op,cmds.xform(obj+'.vtx['+str(vtx[1])+']',q=1,ws=1,t=1),cmds.xform(obj+'.vtx['+str(vtx[2])+']',q=1,ws=1,t=1)]
    OMatrix=edo_createMatrixFromTriangle(triangle,(1-SHEAR))
    #Itransform=edo_getTransformFromMatirx(OMatrix.inverse())
    #if Itransform:
    #    cmds.setAttr(ONT+'.tx',Itransform[0][0])
    #    cmds.setAttr(ONT+'.ty',Itransform[0][1])
    #    cmds.setAttr(ONT+'.tz',Itransform[0][2])
    #    cmds.setAttr(ONT+'.rx',Itransform[1][0])
    #    cmds.setAttr(ONT+'.ry',Itransform[1][1])
    #    cmds.setAttr(ONT+'.rz',Itransform[1][2])
    #    cmds.setAttr(ONT+'.sx',Itransform[2][0])
    #    cmds.setAttr(ONT+'.sy',Itransform[2][1])
    #    cmds.setAttr(ONT+'.sz',Itransform[2][2])
    #    cmds.setAttr(ONT+'.shearXY',Itransform[3][0])
    #    cmds.setAttr(ONT+'.shearXZ',Itransform[3][1])
    #    cmds.setAttr(ONT+'.shearYZ',Itransform[3][2])
    lc=edo_setFourByFourMatrixFromMatrix(OMatrix)
    cmds.parent(ONT,lc)
    edo_setTransformZero(lc)
    cmds.parent([OHT,ONT],w=1)
    cmds.makeIdentity(ONT,apply=1,t=1,r=1,s=1,n=0)
    cmds.parent(OHT,ONT)
    cmds.delete(lc)
    return [ONT,OHT]

def edo_matchTriangles(dpsource,dptarget,source,target,sourcevtx=[0,1,2],targetvtx=[0,1,2],SHEAR=1):
    print 'edo_matchTriangles'
    #dpsource=SONT
    #dptarget=TONT
    #source=source
    #target=target
    #sourcevtx=sourcevtx
    #targetvtx=targetvtx
    if SHEAR==0:
        STtriangle=[cmds.xform(dpsource+'.vtx['+str(sourcevtx[0])+']',q=1,ws=1,t=1),cmds.xform(dpsource+'.vtx['+str(sourcevtx[1])+']',q=1,ws=1,t=1),cmds.xform(dpsource+'.vtx['+str(sourcevtx[2])+']',q=1,ws=1,t=1)]
        TTtriangle=[cmds.xform(dptarget+'.vtx['+str(targetvtx[0])+']',q=1,ws=1,t=1),cmds.xform(dptarget+'.vtx['+str(targetvtx[1])+']',q=1,ws=1,t=1),cmds.xform(dptarget+'.vtx['+str(targetvtx[2])+']',q=1,ws=1,t=1)]
        SMatrix=edo_createMatrixFromTriangle(STtriangle,0)
        TMatrix=edo_createMatrixFromTriangle(TTtriangle,0)
        SOX=[SMatrix(0,0),SMatrix(0,1),SMatrix(0,2)]
        SVOX=om.MVector(SOX[0],SOX[1],SOX[2])
        TOX=[TMatrix(0,0),TMatrix(0,1),TMatrix(0,2)]
        TVOX=om.MVector(TOX[0],TOX[1],TOX[2])
        sx=TVOX.length()/SVOX.length()
        cmds.setAttr(dpsource+'.sx',sx)
        cmds.setAttr(dpsource+'.sy',sx)
        cmds.setAttr(dpsource+'.sz',sx)
    cmds.parent(dpsource.replace('ONT_','OHT_'),dptarget.replace('ONT_','OHT_'))
    cmds.parent(dptarget.replace('ONT_','OHT_'),w=1)
    edo_setTransformZero(dptarget.replace('ONT_','OHT_'))
    edo_transferPivot(target,dptarget.replace('ONT_','OHT_'))
    cmds.parent(dpsource.replace('ONT_','OHT_'),w=1)
    cmds.delete([dptarget,dpsource,dptarget.replace('ONT_','OHT_')])
        
def edo_matchTriangle_backup(dpdpdpdpsource,target,sourcevtx=[0,1,2],targetvtx=[0,1,2],SHEAR=1):
    print 'edo_matchTriangle'
    #source=SONT
    #target=TONT
    #sourcevtx=sourcevtx
    #targetvtx=targetvtx
    STtriangle=[cmds.xform(source+'.vtx['+str(sourcevtx[0])+']',q=1,ws=1,t=1),cmds.xform(source+'.vtx['+str(sourcevtx[1])+']',q=1,ws=1,t=1),cmds.xform(source+'.vtx['+str(sourcevtx[2])+']',q=1,ws=1,t=1)]
    TTtriangle=[cmds.xform(target+'.vtx['+str(targetvtx[0])+']',q=1,ws=1,t=1),cmds.xform(target+'.vtx['+str(targetvtx[1])+']',q=1,ws=1,t=1),cmds.xform(target+'.vtx['+str(targetvtx[2])+']',q=1,ws=1,t=1)]
    SMatrix=edo_createMatrixFromTriangle(STtriangle,0)
    TMatrix=edo_createMatrixFromTriangle(TTtriangle,0)
    SOX=[SMatrix(0,0),SMatrix(0,1),SMatrix(0,2)]
    SOY=[SMatrix(1,0),SMatrix(1,1),SMatrix(1,2)]
    SOZ=[SMatrix(2,0),SMatrix(2,1),SMatrix(2,2)]
    TOX=[TMatrix(0,0),TMatrix(0,1),TMatrix(0,2)]
    TOY=[TMatrix(1,0),TMatrix(1,1),TMatrix(1,2)]
    TOZ=[TMatrix(2,0),TMatrix(2,1),TMatrix(2,2)]
    SVOX=om.MVector(SOX[0],SOX[1],SOX[2])
    SVOY=om.MVector(SOY[0],SOY[1],SOY[2])
    SVOZ=om.MVector(SOZ[0],SOZ[1],SOZ[2])
    TVOX=om.MVector(TOX[0],TOX[1],TOX[2])
    TVOY=om.MVector(TOY[0],TOY[1],TOY[2])
    TVOZ=om.MVector(TOZ[0],TOZ[1],TOZ[2])
    lc=edo_setFourByFourMatrixFromMatrix(SMatrix.inverse())
    tlc=edo_setFourByFourMatrixFromMatrix(TMatrix.inverse())
    if SHEAR==1:
        #print 'set shear'
        cmds.setAttr(source+'.sx',cmds.getAttr(lc+'.sx'))
        cmds.setAttr(source+'.sy',cmds.getAttr(lc+'.sy'))
        cmds.setAttr(target+'.sx',cmds.getAttr(tlc+'.sx'))
        cmds.setAttr(target+'.sy',cmds.getAttr(tlc+'.sy'))
        cmds.setAttr(source+'.sz',cmds.getAttr(lc+'.sz'))
        cmds.setAttr(target+'.sz',cmds.getAttr(tlc+'.sz'))
        cmds.setAttr(source+'.shxz',cmds.getAttr(lc+'.shxz'))
        cmds.setAttr(target+'.shxz',cmds.getAttr(tlc+'.shxz'))
    else:
        #print 'just only set calculate the scale...'
        sx=TVOX.length()/SVOX.length()
        cmds.setAttr(source+'.sx',sx)
        cmds.setAttr(source+'.sy',sx)
        cmds.setAttr(source+'.sz',sx)
    cmds.parent(source.replace('ONT_','OHT_'),target.replace('ONT_','OHT_'))
    cmds.parent(target.replace('ONT_','OHT_'),w=1)
    edo_setTransformZero(target.replace('ONT_','OHT_'))
    edo_transferPivot(target.replace('ONT_',''),target.replace('ONT_','OHT_'))
    cmds.parent(source.replace('ONT_','OHT_'),w=1)
    cmds.delete([lc,tlc,target,source,target.replace('ONT_','OHT_')])

def edo_lockPivot(t,l=1):
    #t='O'
    cmds.setAttr(t+'.rotatePivotX',e=1,lock=l)
    cmds.setAttr(t+'.rotatePivotY',e=1,lock=l)
    cmds.setAttr(t+'.rotatePivotZ',e=1,lock=l)
    cmds.setAttr(t+'.scalePivotX',e=1,lock=l)
    cmds.setAttr(t+'.scalePivotY',e=1,lock=l)
    cmds.setAttr(t+'.scalePivotZ',e=1,lock=l)
    cmds.setAttr(t+'.rotatePivotTranslateX',e=1,lock=l)
    cmds.setAttr(t+'.rotatePivotTranslateY',e=1,lock=l)
    cmds.setAttr(t+'.rotatePivotTranslateZ',e=1,lock=l)
    cmds.setAttr(t+'.scalePivotTranslateX',e=1,lock=l)
    cmds.setAttr(t+'.scalePivotTranslateY',e=1,lock=l)
    cmds.setAttr(t+'.scalePivotTranslateZ',e=1,lock=l)
    
def edo_transferPivot(s,t):
    #s='O'
    #t='T'
    cmds.setAttr(t+'.rotatePivotX',cmds.getAttr(s+'.rotatePivotX'))
    cmds.setAttr(t+'.rotatePivotY',cmds.getAttr(s+'.rotatePivotY'))
    cmds.setAttr(t+'.rotatePivotZ',cmds.getAttr(s+'.rotatePivotZ'))
    cmds.setAttr(t+'.scalePivotX',cmds.getAttr(s+'.scalePivotX'))
    cmds.setAttr(t+'.scalePivotY',cmds.getAttr(s+'.scalePivotY'))
    cmds.setAttr(t+'.scalePivotZ',cmds.getAttr(s+'.scalePivotZ'))
    cmds.setAttr(t+'.rotatePivotTranslateX',cmds.getAttr(s+'.rotatePivotTranslateX'))
    cmds.setAttr(t+'.rotatePivotTranslateY',cmds.getAttr(s+'.rotatePivotTranslateY'))
    cmds.setAttr(t+'.rotatePivotTranslateZ',cmds.getAttr(s+'.rotatePivotTranslateZ'))
    cmds.setAttr(t+'.scalePivotTranslateX',cmds.getAttr(s+'.scalePivotTranslateX'))
    cmds.setAttr(t+'.scalePivotTranslateY',cmds.getAttr(s+'.scalePivotTranslateY'))
    cmds.setAttr(t+'.scalePivotTranslateZ',cmds.getAttr(s+'.scalePivotTranslateZ'))
 
def transferTransform(s,t):
    #s='OHT_O'
    #t='O1_ctrl'
    tx=cmds.getAttr(s+'.tx')+cmds.getAttr(s+'.rotatePivotTranslateX')+cmds.getAttr(s+'.scalePivotTranslateX')
    cmds.setAttr(t+'.tx',tx)
    ty=cmds.getAttr(s+'.ty')+cmds.getAttr(s+'.rotatePivotTranslateY')+cmds.getAttr(s+'.scalePivotTranslateY')
    cmds.setAttr(t+'.ty',ty)
    tz=cmds.getAttr(s+'.tz')+cmds.getAttr(s+'.rotatePivotTranslateZ')+cmds.getAttr(s+'.scalePivotTranslateZ')
    cmds.setAttr(t+'.tz',tz)
    rx=cmds.getAttr(s+'.rx')
    cmds.setAttr(t+'.rx',rx)
    ry=cmds.getAttr(s+'.ry')
    cmds.setAttr(t+'.ry',ry)
    rz=cmds.getAttr(s+'.rz')
    cmds.setAttr(t+'.rz',rz)
    sx=cmds.getAttr(s+'.sx')
    cmds.setAttr(t+'.sx',sx)
    sy=cmds.getAttr(s+'.sy')
    cmds.setAttr(t+'.sy',sy)
    sz=cmds.getAttr(s+'.sz')
    cmds.setAttr(t+'.sz',sz)
    shxy=cmds.getAttr(s+'.shxy')
    cmds.setAttr(t+'.shxy',shxy)
    shxz=cmds.getAttr(s+'.shxz')
    cmds.setAttr(t+'.shxz',shxz)
    shyz=cmds.getAttr(s+'.shyz')
    cmds.setAttr(t+'.shyz',shyz)
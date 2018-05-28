import maya.cmds as cmds
import maya.OpenMaya as om
global edo_g_selectBlendShape
import edo_autoConnectBlendshapesInbetweenUI.edo_transferMesh as edo_transferMesh
from functools import partial

def edo_attatchBlendShapeAsSkinCluster():
    mesh=cmds.ls(sl=1)[0]
    sks=edo_findNodeFromHis(mesh,'skinCluster')[0]
    infs=cmds.skinCluster(sks,q=1,inf=1)
    if not cmds.objExists('GRP_'+mesh+'TARGETS'):
        cmds.createNode('transform',n='GRP_'+mesh+'TARGETS')
    bsms=[]
    for i in infs:
        #i=infs[0]
        bsm=cmds.duplicate(sels,n='BS_'+i+'_'+mesh)[0]
        cmds.parent(bsm,'GRP_'+mesh+'TARGETS')
        cmds.select(bsm,r=1)
        cmds.CenterPivot()
        cmds.setAttr(bsm+'.sx',0.1)
        cmds.setAttr(bsm+'.sy',0.1)
        cmds.setAttr(bsm+'.sz',0.1)
        cmds.delete(cmds.parentConstraint(i,bsm,mo=0))
        bsms.append(bsm)
    cmds.select(bsms,r=1)
    cmds.select(mesh,add=1)
    cmds.blendShape(n='BS_'+sks)
    cmds.select(mesh,r=1)
    edo_makeBlendShapeWeightNormalizePaintable()

#edo_namesOfArrayAttr('blendShape1','weight','attr')
def edo_namesOfArrayAttr(name,attr):
    #name='blendShape1'
    #attr='weight'
    attrs=[]
    obj=om.MObject()
    msel=om.MSelectionList()
    mg=om.MGlobal()
    cmds.select(name)
    mg.getActiveSelectionList(msel)
    msel.getDependNode(0,obj)
    mfndg=om.MFnDependencyNode()
    mfndg.setObject(obj)
    plug=mfndg.findPlug(attr)
    num=plug.numElements()
    for n in range(0,num):
        #n=0
        p=plug.elementByLogicalIndex(n)
        attrname=p.name()
        lens=len(attrname.split('.'))
        attrname=attrname.split('.')[lens-1]
        attrs.append(attrname)
    return attrs
        

def edo_findNodeFromHis(name,type):
    #name='pCylinder1'
    #type='skinCluster'
    nodes=[]
    hiss=cmds.listHistory(name,pruneDagObjects=1,groupLevels=1)
    if not hiss==None:
        for his in hiss:
            if cmds.nodeType(his)==type:
                nodes.append(his)
    return nodes

def edo_findSelectedVtxsId(sels):
    ids=[]
    vtxs=cmds.ls(sels,fl=1)
    for v in vtxs:
        #v=vtxs[0]
        id=int(v.split('.')[1].split('[')[1].replace(']',''))
        ids.append(id)
    return ids
    
def edo_makeAllBlendShapeWeightNormalizePaintable(*arg):
    sels=cmds.ls(sl=1)
    for sel in sels:
        cmds.select(sel,r=1)
        edo_makeBlendShapeWeightNormalizePaintable()

def edo_makeBlendShapeWeightNormalizePaintable(*arg):
    global edo_g_selectBlendShape
    sels=cmds.ls(sl=1)
    sourcemesh=''
    ids=[]
    if sels==None:
        cmds.confirmDialog( title='error', message='please select the source mesh!', button='god it', defaultButton='Yes', cancelButton='No', dismissString='No' )
        return False
    if '.vtx[' in sels[0]:
        sourcemesh=sels[0].split('.')[0]
        ids=edo_findSelectedVtxsId(sels)
    else:
        if not len(sels)==1:
            cmds.confirmDialog( title='error', message='you can select only one mesh!', button='god it', defaultButton='Yes', cancelButton='No', dismissString='No' )
            return False
        sourcemesh=sels[0]
    bs=''
    bss=edo_findNodeFromHis(sourcemesh,'blendShape')
    if len(bss)==1:
        bs=bss[0]
    else:
        bs=cmds.confirmDialog( title='error', message='more than blendshape find,select one!', button=bss, defaultButton='Yes', cancelButton='No', dismissString='No' )
    if bs=='':
        cmds.confirmDialog( title='error', message='can not find blendShape node!', button='god it', defaultButton='Yes', cancelButton='No', dismissString='No' )
        return False
    targets=edo_namesOfArrayAttr(bs,'weight')
    skins=edo_findNodeFromHis(sourcemesh,'skinCluster')
    joints=[]
    #if not skins==[]:
    #    bb=cmds.confirmDialog( title='error', message='more than skinCluster find,select one!', button=['create New One','transfer To Old'], defaultButton='Yes', cancelButton='No', dismissString='No' )
    #cmds.undoInfo(closeChunk=False)
    if skins==[]:
        for t in targets:
            #t=targets[0]
            po=[0,0,0]
            if cmds.objExists(t):
                po=cmds.xform(t,q=1,ws=1,rp=1)
            joints.append(cmds.createNode('joint',n=t+'_bsweight'))
            cmds.xform(joints[(len(joints)-1)],ws=1,t=po)
        cmds.select(joints)
        cmds.select(sourcemesh,add=1)
        cmds.skinCluster(sourcemesh,joints,tsb=True)
        skin=edo_findNodeFromHis(sourcemesh,'skinCluster')[0]
    else:
        if len(skins)==1:
            skin=skins[0]
            joints=cmds.skinCluster(skin,q=1,inf=1)
        else:
            skin=cmds.confirmDialog( title='error', message='more than skinCluster find,select one!', button=skins, defaultButton='Yes', cancelButton='No', dismissString='No' )
            joints=cmds.skinCluster(skin,q=1,inf=1)
    wl=edo_namesOfArrayAttr(skin,'weightList')
    for s in range(0,len(wl)):
        #s=0
        if (not ids==[]) and  not (s in ids):
            continue
        w=wl[s]
        #print s
        for i in range(0,len(targets)):
            #i=1
            onput=skin+'.'+w+'.weights['+str(i)+']'
            input=bs+'.it[0].itg['+str(i)+'].tw['+str(s)+']'
            cmds.setAttr(input,cmds.getAttr(onput))
    #cmds.undoInfo(closeChunk=True)
    cmds.select(sels)

    
def edo_BlendShapeListUIBT1cmd():
    global edo_g_selectBlendShape
    edo_g_selectBlendShape=cmds.textScrollList('edo_BlendShapeListUITSL01',q=1,si=1)
    print edo_g_selectBlendShape
    cmds.deleteUI('edo_BlendShapeListUI')


def edo_getNewTargetWithBlendShapeNode(*arg):
    sel=cmds.ls(sl=1)[0]
    bsss=[]
    shape=cmds.listRelatives(sel,s=1,ni=1)[0]
    nodes=cmds.listHistory(shape)
    bss=edo_findNodeFromList(nodes,'blendShape')
    bs=''
    if len(bss)==1:
        bs=bss[0]
    else:
        bs=cmds.confirmDialog( title='error', message='more than blendshape find,select one!', button=bss, defaultButton='Yes', cancelButton='No', dismissString='No' )
    if bs=='':
        cmds.confirmDialog( title='error', message='can not find blendShape node!', button='god it', defaultButton='Yes', cancelButton='No', dismissString='No' )
        return False
    print ('get the target from '+bs[0])+'  :'
    attr=cmds.blendShape(bs,q=1,weight=1)
    num=len(attr)
    if not cmds.objExists('GRP_'+bs+'_newBlendShape'):
        cmds.createNode('transform',n='GRP_'+bs+'_newBlendShape')
    for u in range(0,num):
        attrname=bs+'.weight['+str(u)+']'
        cmds.setAttr(attrname,0)
    for n in range(0,num):
        #n=0
        attrname=bs+'.weight['+str(n)+']'
        longname=cmds.aliasAttr(attrname,q=1)
        print 'get '+longname+'  ...'
        cmds.setAttr(attrname,1)
        dup=cmds.duplicate(sel,n='new_'+longname)
        bsss.append(dup[0])
        cmds.parent(dup,'GRP_'+bs+'_newBlendShape')
        cmds.setAttr(attrname,0)
    return bsss 

def edo_findNodeFromList(nodes,type):
    bc=[]
    for node in nodes:
        if cmds.nodeType(node)==type:
            bc.append(node)
            print node
    return bc

def edo_unlocktransform(objs):
    for o in objs:
        #o=objs[0]
        #o=om
        cmds.setAttr(o+'.tx',e=1,l=0)
        cmds.setAttr(o+'.ty',e=1,l=0)
        cmds.setAttr(o+'.tz',e=1,l=0)
        cmds.setAttr(o+'.rx',e=1,l=0)
        cmds.setAttr(o+'.ry',e=1,l=0)
        cmds.setAttr(o+'.rz',e=1,l=0)
        cmds.setAttr(o+'.sx',e=1,l=0)
        cmds.setAttr(o+'.sy',e=1,l=0)
        cmds.setAttr(o+'.sz',e=1,l=0)

#edo_departAllBlendshape()
def edo_departAllBlendshape(*arg):
    sels=cmds.ls(sl=1)
    oms=sels[0]
    sels.remove(oms)
    edo_unlocktransform([oms])
    nodes=cmds.listHistory(oms)
    bss=edo_findNodeFromList(nodes,'blendShape')
    if bss:
        bs=bss[0]
        tbs=cmds.blendShape(bs,q=1,t=1)
        for s in sels:
            #s=sels[1]
            po=cmds.xform(s,q=1,ws=1,t=1)
            #for t in tbs:
                #t=tbs[1]
                #try:
                #    cmds.connectAttr(s+'.outMesh',t+'.inMesh',f=1)
                #    #cmds.disconnectAttr(s+'.outMesh',t+'.inMesh')
                #except:
                #    print 'pass'
            cmds.select(s,r=1)
            cmds.select(tbs,add=1)
            edo_transferMesh.edo_transferMeshes()
            cmds.select(oms,r=1)
            bsss=edo_getNewTargetWithBlendShapeNode()
            cmds.xform(bsss,ws=1,t=po)
            for b in bsss:
                cmds.rename(b,b.replace('new_','')+'_'+s)
    
def edo_makeBlendShapeWeightNormalizePaintableUI():
    if cmds.window("edo_makeBlendShapeWeightNormalizePaintableUI",ex=1):
        cmds.deleteUI("edo_makeBlendShapeWeightNormalizePaintableUI")
    cmds.window("edo_makeBlendShapeWeightNormalizePaintableUI",title="edo_makeBlendShapeWeightNormalizePaintableUI")
    cmds.columnLayout( columnAttach=('both', 5), rowSpacing=5, columnWidth=190)
    cmds.button('edo_makeBlendShapeWeightNormalizePaintableUIBT1',label='transfer blendshape weights',h=27,bgc=(0.1,0.9,0.7),c=partial(edo_makeAllBlendShapeWeightNormalizePaintable))
    cmds.button('edo_makeBlendShapeWeightNormalizePaintableUIBT2',label='get all blendshape target',h=27,bgc=(0.8,0.7,0.2),c=partial(edo_getNewTargetWithBlendShapeNode))
    cmds.button('edo_makeBlendShapeWeightNormalizePaintableUIBT3',label='depart all blendshape target',h=27,bgc=(0.8,0.4,0.6),c=partial(edo_departAllBlendshape))
    cmds.showWindow("edo_makeBlendShapeWeightNormalizePaintableUI")
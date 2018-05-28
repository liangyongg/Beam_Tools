import maya.cmds as cmds
def edo_transferMesh():
    sels=cmds.ls(sl=1)
    if sels==None or sels==[]:
        cmds.confirmDialog( title='error', message='you must select something', button='god it', defaultButton='Yes', cancelButton='No', dismissString='No')
        return False
    if not len(sels)>=2:
        cmds.confirmDialog( title='error', message='you must select more than two mesh', button='god it', defaultButton='Yes', cancelButton='No', dismissString='No')
        return False
    sc=sels[0]
    dt=sels[1]
    input=cmds.listConnections(dt+'.inMesh',s=1,d=0)
    if not input==None:
        cmds.confirmDialog( title='error', message='the direct mesh is connected,check it!', button='god it', defaultButton='Yes', cancelButton='No', dismissString='No')
        return False
    else:
        edo_setMeshVertexsZero(dt)
        cmds.connectAttr(sc+'.outMesh',dt+'.inMesh',f=1)
        edo_setMeshVertexsZero(dt)
        cmds.disconnectAttr(sc+'.outMesh',dt+'.inMesh')
        
def edo_transferMeshes():
    sels=cmds.ls(sl=1)
    sc=sels[0]
    for i in range(1,len(sels)):
        dt=sels[i]
        cmds.select(sc)
        cmds.select(dt,add=1)
        edo_transferMesh()


def edo_setMeshVertexsZero(mesh):
    #mesh='BS_facial_eb_inup6'
    print 'reset vertex position!'
    num=cmds.polyEvaluate(mesh,v=1)
    for n in range(0,num):
        #n=56
        #print n
        vertex=mesh+'.vtx['+str(n)+']'
        cmds.setAttr(vertex+'.pntx',0)
        cmds.setAttr(vertex+'.pnty',0)
        cmds.setAttr(vertex+'.pntz',0)

def tramsferMeshWithBlendShape():
    sls = cmds.filterExpand(sm=12)
    vtx = cmds.filterExpand(sm=31)
    if sls==None and vtx==None:
        print ( "No Polygon or Vertices selected" )
        return
    if len(sls)==2:
        cmds.blendShape(sls[-1],sls[0],origin="local",w=[0,1])
        print ( "Shapes [%s]-->[%s]"%(sls[-1],sls[0]) )
    elif len(sls)==1 and vtx!=None:
        cmds.blendShape(sls[-1],vtx,origin="local",w=[0,1])
        print ( "Selected Vetexs as <%s>"%sls[-1] )
    cmds.delete(sls[0],ch=True)
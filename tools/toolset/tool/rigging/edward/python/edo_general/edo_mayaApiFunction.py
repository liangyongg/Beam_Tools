import maya.cmds as cmds
import maya.OpenMaya as om

#+++++++++++++++++++++++++++build MObject+++++++++++++++++++++++++++++++++
def edo_getMSelectionListFromSelected():
    mg=om.MGlobal()
    mls=om.MSelectionList()
    mg.getActiveSelectionList(mls)
    print mls.length()
    return mls
        
#edo_getMObjectFromSelected(1)
def edo_getMObjectFromSelected(shape=0):
    sels=cmds.ls(sl=1)
    if sels:
        sel=sels[0]
        if shape==1:
            ss=cmds.listRelatives(sel,s=1,pa=1)
            if ss:
                sel=ss[0]
        mg=om.MGlobal()
        mls=om.MSelectionList()
        mg.getSelectionListByName(sel,mls)
        #print mls.length()
        mobj=om.MObject()
        mls.getDependNode(0,mobj)
        print mobj.apiTypeStr()
        return mobj
    else:
        return False
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++modify maya readOnly nodes++++++++++++++++++++++++++++++++++
#edo_renameDefualtRenderLayerName()
def edo_renameDefualtRenderLayerName(newname='defaultRenderLayer'):
    drl=cmds.listConnections('renderLayerManager.rlmi[0]',s=0,d=1)[0]
    if not drl=='defaultRenderLayer':
        try:
            cmds.delete('defaultRenderLayer')
        except:
            print 'defaultRenderLayer is not found!'
    cmds.select(drl,r=1)
    msl=om.MSelectionList()
    mg=om.MGlobal()
    mg.getActiveSelectionList(msl)
    msl.length()
    mobj=om.MObject()
    msl.getDependNode(0,mobj)
    mfndn=om.MFnDependencyNode(mobj)
    mfndn.setName(newname)
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++++++++++++++++++get nodes information+++++++++++++++++++++++++++++++++++++++
#getSelectAttrApiType('message')
def getSelectAttrApiType(attrName):
    #attrName='translate'
    msl=om.MSelectionList()
    mg=om.MGlobal()
    mg.getActiveSelectionList(msl)
    obj=om.MObject()
    msl.length()
    msl.getDependNode(0,obj)
    print 'nodeType  is  '+obj.apiTypeStr()+"\n"
    mfndn=om.MFnDependencyNode(obj)
    cp=mfndn.findPlug(attrName)
    print attrName+ ': the type of this attribute  is '+cp.attribute().apiTypeStr()+"\n"
    return cp.attribute().apiTypeStr()
#=====================================================
#edo_getConnectedVerticesFromSelectedMeshAndId(edo_getMObjectFromSelected(1),12,1)
def edo_getConnectedVerticesFromSelectedMeshAndId(meshobj=edo_getMObjectFromSelected(1),id=0,returnList=1):
    mmit=om.MItMeshVertex(meshobj)
    #print mmit.count()
    #print mmit.index()
    mintarray=om.MIntArray()
    for i in range(0,mmit.count()):
        #print i
        if mmit.index()==id:
            mmit.getConnectedVertices(mintarray)
            break;
        mmit.next()
    l=mintarray.length()
    print str(l) + ' vertexes connect to vertex ['+str(id)+']'
    connectVtxs=[]
    for i in range(0,l):
        connectVtxs.append(mintarray[i])
    print 'they are : '
    print connectVtxs
    if returnList==1:
        return connectVtxs
    else:
        return mintarray
#edo_getgetOppositeVertexFromSelectedMeshAndId(edo_getMObjectFromSelected(1),12,23)     
def edo_getgetOppositeVertexFromSelectedMeshAndId(meshobj=edo_getMObjectFromSelected(1),vid=0,edgeid=0):
    mmit=om.MItMeshVertex(meshobj)
    #print mmit.count()
    #print mmit.index()
    mintarray=om.MIntArray()
    ut=om.MScriptUtil()
    ut.createFromInt(-1)
    opid=ut.asIntPtr()
    opidint=-1
    for i in range(0,mmit.count()):
        #print i
        if mmit.index()==vid:
            mmit.getOppositeVertex(opid,edgeid)
            opidint=ut.getInt(opid)
            break;
        mmit.next()
    return opidint
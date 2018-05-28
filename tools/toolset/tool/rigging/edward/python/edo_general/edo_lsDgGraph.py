import maya.cmds as cmds
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
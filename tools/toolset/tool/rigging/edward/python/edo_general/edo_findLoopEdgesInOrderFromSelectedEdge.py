import maya.cmds as cmds

def edo_findLoopEdgesInOrderFromSelectedEdge():
    fedges=cmds.ls(sl=1,fl=1)
    cmds.SelectEdgeRingSp()
    alledges=cmds.ls(sl=1,fl=1)
    for e in alledges:
        #e=alledges[0]
        #print e
        #cmds.select(fedges[-1])
        te=cmds.ls(cmds.polyListComponentConversion(cmds.polyListComponentConversion(fedges[-1],tf=1),te=1),fl=1)
        #cmds.select(te,r=1)
        for ie in te:
            print ie
            if (not ie in fedges) and (ie in alledges):
                print 'append '+ie
                fedges.append(ie)
                break
        cmds.select(fedges)
    return fedges

#edo_findIntervalEdgesFromSelectedEdge(2)
def edo_findIntervalEdgesFromSelectedEdge(interval=2):
    alledges=edo_findLoopEdgesInOrderFromSelectedEdge()
    fedges=[]
    i=0
    for e in alledges:
        if i%interval==0:
            fedges.append(e)
        i=i+1
    cmds.select(fedges,r=1)
    return fedges
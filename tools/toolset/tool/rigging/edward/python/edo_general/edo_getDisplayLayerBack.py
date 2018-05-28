import maya.cmds as cmds
def edo_getDisplayLayerBack():
    layers=cmds.ls(type='displayLayer')
    count=len(layers)
    for i in range(0,count):
        ly=layers[i]
        if ly=='defaultLayer':
            print 'pass'
            continue
        print 'connectAttr   layerManager.displayLayerId['+str(i+1)+']   to   '+ly+'.identification'
        try:
            cmds.connectAttr('layerManager.displayLayerId['+str(i+1)+']',ly+'.identification',f=1)
        except:
            print "pass"

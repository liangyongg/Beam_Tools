import maya.cmds as cmds
def edo_feedbackSelectedBlendShapeAttrId():
    target=cmds.channelBox('mainChannelBox',q=1,selectedHistoryAttributes=1)
    if target:
        bsname='blendShape1'
        ct=cmds.blendShape(bsname,q=1,wc=1)
        ci=0
        for i in range(0,ct):
            #i=0
            cbs=cmds.aliasAttr(bsname+'.weight['+str(i)+']',q=1)
            if cbs==target[0]:
                print 'find out..:' + cbs +'\n'
                ci=i+1
        print ci
        return ci
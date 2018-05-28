import maya.cmds as cmds
def edo_createSimpleFacialAttrChannelRig():
    sels=cmds.ls(sl=1)
    b=sels[0]
    fc=sels[1]
    bss=cmds.blendShape(b,q=1,t=1)
    for bs in bss:
        #bs=bss[0]
        if not cmds.objExists(fc+'.'+bs):
            cmds.addAttr(fc,ln=bs,at='double',min=0,dv=0,max=1)
            cmds.setAttr(fc+'.'+bs,e=1,k=1)
        try:
            cmds.connectAttr(fc+'.'+bs,b+'.'+bs,f=1)
        except:
            print 'pass' + bs
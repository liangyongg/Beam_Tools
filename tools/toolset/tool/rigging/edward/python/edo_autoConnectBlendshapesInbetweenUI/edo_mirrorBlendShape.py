import maya.cmds as cmds
import maya.mel as mel
#edo_mirrorBlendShape('BS_','MSH_')
def edo_mirrorBlendShape():
    sels=cmds.ls(sl=1)
    s=sels[0]
    bd=cmds.xform(s,q=1,bb=1)
    w=bd[3]-bd[0]
    cmds.setAttr(s+'.sx',20)
    cmds.setAttr(s+'.sy',20)
    cmds.setAttr(s+'.sz',20)
    d=cmds.duplicate(s,n='edo_mirrorBlendShape_'+s)[0]
    cmds.setAttr(d+'.sx',-20)
    cmds.setAttr(d+'.v',0)
    cmds.select(d,r=1)
    cmds.select(s,add=1)
    #mel.eval('CreateWrap')
    cmd='string $wraps[]=`doWrapArgList "7" { "1","0","1", "2", "1", "1", "0", "0" }`;'
    wrap=mel.eval(cmd)[0]
    print 'quick mirror model...'
    sels.remove(s)
    cmds.select(sels,r=1)
    cmds.select(s,add=1)
    bs=cmds.blendShape(n='edo_mirrorBlendShape')[0]
    mbs=[]
    for t in sels:
        #t=sels[0]
        print t
        px=''
        rx=''
        dr=1
        if 'Lf_' in t:
            px='Lf_'
            rx='Rt_'
            dr=-1
        if 'Rt_' in t:
            px='Rt_'
            rx='Lf_'
        if 'LF_' in t:
            px='LF_'
            rx='RT_'
            dr=-1
        if 'RT_' in t:
            px='RT_'
            rx='LF_'
        if 'lf_' in t:
            px='lf_'
            rx='rt_'
            dr=-1
        if 'rt_' in t:
            px='rt_'
            rx='lf_'
        if 'left_' in t:
            px='left_'
            rx='right_'
            dr=-1
        if 'right_' in t:
            px='right_'
            rx='left_'
        if 'L_' in t:
            px='L_'
            rx='R_'
        if 'R_' in t:
            px='R_'
            rx='L_'
        wp=cmds.xform(t,q=1,ws=1,t=1)
        nwp=[wp[0]+(dr*w*0.5),wp[1],wp[2]]
        cmds.setAttr(bs+'.'+t,1)
        b=cmds.duplicate(d,n=t.replace(px,rx))[0]
        cmds.setAttr(b+'.sx',1)
        cmds.setAttr(b+'.sy',1)
        cmds.setAttr(b+'.sz',1)
        cmds.setAttr(b+'.v',1)
        cmds.setAttr(bs+'.'+t,0)
        cmds.xform(b,ws=1,t=nwp)
        mbs.append(b)
    cmds.setAttr(s+'.sx',1)
    cmds.setAttr(s+'.sy',1)
    cmds.setAttr(s+'.sz',1)
    cmds.delete(bs,d)
    return mbs
import maya.cmds as cmds
def edo_lightchaserCtrlRename():
    ctrls=cmds.ls('*_ctrl*',s=0,type='transform')
    Ctrls=cmds.ls('*_Ctrl*',s=0,type='transform')
    CTRLS=cmds.ls('*_CTRL*',s=0,type='transform')
    jctrls=cmds.ls('*_ctrl*',s=0,type='joint')
    jCtrls=cmds.ls('*_Ctrl*',s=0,type='joint')
    jCTRLS=cmds.ls('*_CTRL*',s=0,type='joint')
    allctrls=ctrls+Ctrls+CTRLS+jctrls+jCtrls+jCTRLS
    for ctrl in allctrls:
        #ctrl=allctrls[0]
        sha=cmds.listRelatives(ctrl,s=1,pa=1)
        if sha:
            print ctrl
            #ctrl='yingshuiji_14_fk_ctrl3'
            tmp=ctrl.replace('_Ctrl','_ctrl').replace('_CTRL','_ctrl')
            nc=tmp.replace('_ctrl','')+'_ctrl'
            cmds.rename(ctrl,nc)
            print 'rename '+ctrl+' .. to .. '+nc
        
def edo_lightchaserShakeAttrRename():
    sels=cmds.ls(sl=1)
    for sel in sels:
        #sel=sels[0]
        if cmds.objExists(sel+'.sizeY'):
            try:
                cmds.aliasAttr('Y',sel+'.sizeY')
            except:
                print 'pass'
        if cmds.objExists(sel+'.sizeZ'):
            try:
                cmds.aliasAttr('Z',sel+'.sizeZ')
            except:
                print 'pass'
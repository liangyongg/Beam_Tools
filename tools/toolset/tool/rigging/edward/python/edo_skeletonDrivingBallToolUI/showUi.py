from headfile import *
import maya.cmds as cmds
import edo_common
import os
import edo_skeletonDrivingBallToolUI.edo_skeletonDrivingBallToolUIDesign as edo_skeletonDrivingBallToolUIDesign;reload(edo_skeletonDrivingBallToolUIDesign)
import edo_skeletonDrivingBallToolUI
import edo_general.edo_loadPlugin as ELPLUGIN
import edo_skeletonDrivingBallToolUI.edo_autoConnectCorrectBlendShapeCmd as edo_autoConnectCorrectBlendShapeCmd;reload(edo_autoConnectCorrectBlendShapeCmd)
import edo_skeletonDrivingBallToolUI.edo_skeletonDrivingBallCmd as edo_skeletonDrivingBallCmd;reload(edo_skeletonDrivingBallCmd)
import edo_skeletonDrivingBallToolUI.edo_mirrorSKDBdeform as edo_mirrorSKDBdeform;reload(edo_mirrorSKDBdeform)
import edo_skeletonDrivingBallToolUI.edo_connectBlendShapeToBlendShape as edo_connectBlendShapeToBlendShape;reload(edo_connectBlendShapeToBlendShape)
mllpath=edo_skeletonDrivingBallToolUI.__file__.replace('python\\edo_skeletonDrivingBallToolUI\\__init__.pyc','mll').replace('\\','/')
uipath=os.path.dirname(edo_skeletonDrivingBallToolUIDesign.__file__).replace('\\','/')

#self=ui
#cmds.select(jntlist)
class edo_skeletonDrivingBallToolUI(edo_skeletonDrivingBallToolUIDesign.Ui_edo_skeletonDrivingBallToolUI):
    def setupUi(self,edo_skeletonDrivingBallToolUI):
        edo_skeletonDrivingBallToolUIDesign.Ui_edo_skeletonDrivingBallToolUI.setupUi(self,edo_skeletonDrivingBallToolUI)
        #self.loadChain_bt.clicked.connect(self.edo_loadChain_)
        #self.nurbsIk_bt.clicked.connect(self.edo_addNurbsIkSpline_)
        #self.loadCtrl_le.setText(sels[0])
        #self.ctrlHierarchy_list.addItem(l)
        #self.ctrlHierarchy_list.setCurrentRow(0)
        #load plugin
        self.createskdb_bt.clicked.connect(self.edo_createSKDB_cmd_)
        self.connectcbs_bt.clicked.connect(self.edo_autoConnectCorrectBlendShape_cmd_)
        self.loadctrl_bt.clicked.connect(self.edo_loadctrl_cmd_)
        self.loadskdb_bt.clicked.connect(self.edo_loadskdb_cmd_)
        self.loadskdb_le.textChanged.connect(lambda:self.edo_lineEditChanged_(self.loadskdb_le))
        self.attribute_lw.itemSelectionChanged.connect(self.edo_attribute_lw_slchanged_)
        self.attribute_lw.itemClicked.connect(self.edo_attribute_lw_slchanged_)
        self.rotation_lw.itemSelectionChanged.connect(self.edo_rotation_lw_slchanged_)
        self.rotation_lw.itemClicked.connect(self.edo_rotation_lw_slchanged_)
        #LC_BODY
        self.createskdbforlcbr_bt.clicked.connect(self.edo_createskdbforlcbr_bt_cmd_)
        #mirror
        self.mirrordbs_bt.clicked.connect(self.edo_mirrordbs_bt_cmd_)
        self.connectBsToBs_bt.clicked.connect(self.edo_connectBsToBs_bt_cmd_)
        ELPLUGIN.edo_loadPlugin('geometryComputer.mll')
        print 'createUi'
        
    def edo_connectBsToBs_bt_cmd_(self):
        sels=cmds.ls(sl=1,type='blendShape')
        if sels:
            if len(sels)>=2:
                sbs=sels[-1]
                tbs=sels[:-1]
                edo_connectBlendShapeToBlendShape.edo_connectBlendShapeToBlendShape(sbs,tbs)
        
    def edo_mirrordbs_bt_cmd_(self):
        #self=ui
        fr=str(self.from_le.text())
        to=str(self.to_le.text())
        cmds.undoInfo(openChunk=True)
        try:
            af=0
            sels=cmds.ls(sl=1,type='transform')
            mesh=''
            if sels:
                sel=sels[0]
                if not sel[-1]=='_':
                    mesh=cmds.rename(sel,sel+'_')
                    af=1
            if 'L_' in mesh or 'R_' in mesh:
                print 'different mesh'
                edo_mirrorSKDBdeform.edo_mirrorSKDBdeform([fr,to],1)
            else:
                print 'same mesh'
                edo_mirrorSKDBdeform.edo_mirrorSKDBdeform([fr,to],0)
            if af==1:
                cmds.rename(mesh,mesh[:-1])
            print 'done'
        except:
            cmds.undoInfo(closeChunk=True)
            #cmds.undo()
            print 'something was wrong in your scene'
            cmds.error('something was wrong in your scene')
        cmds.undoInfo(closeChunk=True)
        
    def edo_createskdbforlcbr_bt_cmd_(self):
        print 'add SKDB to all LC body rig'
        cmds.undoInfo(openChunk=True)
        try:
            self.edo_createskdbforlcbr_bt_cmd()
        except:
            cmds.undoInfo(closeChunk=True)
            #cmds.undo()
            print 'something was wrong in your scene'
            cmds.error('something was wrong in your scene')
        cmds.undoInfo(closeChunk=True)
        
    def edo_createskdbforlcbr_bt_cmd(self):
        #self=ui
        txtpath=uipath+'/LC_bodyRigSKDB.txt'
        if self.nofinger_cb.isChecked():
            txtpath=uipath+'/LC_bodyRigSKDB_nofinger.txt'
        print txtpath
        fobj=open(txtpath,'r')
        txt=fobj.read()
        fobj.close()
        txs=txt.split('\n')
        txs=txs[1:]
        for tx in txs:
            #tx=txs[0]
            tx=tx.replace('\r','')
            ts=tx.split(':')
            dvjnt=ts[0]
            ctrl=ts[1]
            pajnt=ts[2]
            rotations=ts[3]
            tmp=rotations.split(';')
            rotation=[]
            for t in tmp:
                #t=tmp[0]
                r=t
                if ',' in t:
                    r=t.split(',')
                rotation.append(r)
            sels=[dvjnt,ctrl]
            sel=sels[0]
            skdb=sel+'_FRAME'
            if not cmds.objExists(skdb):
                edo_skeletonDrivingBallCmd.edo_addSkeletonBall(sel,1,pajnt,rotation,8)
            if cmds.objExists('rig.size'):
                s=cmds.getAttr('rig.size')
                cmds.setAttr(skdb+'.globalScale',s*3)
            if len(sels)>1:
                print 'connect SKDB...'
                if not cmds.objExists(sels[1]+'.SKDB'):
                    cmds.addAttr(sels[1],ln='SKDB',at='message')
                if not cmds.objExists(skdb+'.SKDB'):
                    cmds.addAttr(skdb,ln='SKDB',at='message')
                try:
                    cmds.connectAttr(sels[1]+'.SKDB',skdb+'.SKDB',f=1)
                    cmds.setAttr(skdb+'Shape0.ovc',13)
                except:
                    print 'pass connection: ' +skdb
        
    def edo_rotation_lw_slchanged_(self):
        print 'edo_rotation_lw_slchanged_'
        #self=ui
        ctrl=''
        ctrl=str(self.loadctrl_le.text())
        skdbf=str(self.loadskdb_le.text())
        data=str(self.rotation_lw.currentItem().text())
        attr=str(self.attribute_lw.currentItem().text())
        print attr
        print data
        #self.attribute_lw.clear()
        if attr=='' or attr==None:
            print 'cleaning the attribute list... pass set rotations'
            return False
        if data=='' or data==None:
            print 'no rotation data selected...pass set rotations'
            return False
        rotations=data.split('     [')[-1].replace(']','').split(',')
        if ctrl=='' or ctrl==None:
            if cmds.objExists(skdbf+'.SKDB'):
                ctrls=cmds.listConnections(skdbf+'.SKDB',s=1,d=0)
                if ctrls:
                    ctrl=ctrls[0]
                else:
                    return False
        rx=round(float(rotations[0]),3)
        ry=round(float(rotations[1]),3)
        rz=round(float(rotations[2]),3)
        try:
            cmds.setAttr(ctrl+'.rx',rx)
            cmds.setAttr(ctrl+'.ry',ry)
            cmds.setAttr(ctrl+'.rz',rz)
        except:
            print 'can not move the controler'
        
    def edo_attribute_lw_slchanged_(self):
        print 'edo_attribute_lw_slchanged_'
        #self=ui
        self.edo_getRecordedRotationValueList()
        
    def edo_getRecordedRotationValueList(self):
        #self=ui
        slattr=str(self.attribute_lw.currentItem().text())
        skdbf=str(self.loadskdb_le.text())
        attrname=skdbf+'.'+slattr
        self.rotation_lw.clear()
        if cmds.objExists(attrname):
            datatxt=cmds.getAttr(attrname)
            if datatxt=='' or datatxt==None:
                return False
            poses=datatxt.split(';')[:-1]
            for pos in poses:
                #pos=poses[0]
                pv=pos.split(':')[1]+'     ['+pos.split(':')[2]+']'
                self.rotation_lw.addItem(pv)
        if self.rotation_lw.count>=1:
            #self.rotation_lw.setCurrentRow(0)
            print 'done'
            
    def edo_findItemFromGivenText(self,lw,txt):
        #self=ui
        #lw=self.rotation_lw
        #txt=rtxt
        its=lw.findItems(txt,QtCore.Qt.MatchStartsWith)
        if its==[]:
            return False
        it=its[0]
        print it.text()
        return it
        
    def edo_autoConnectCorrectBlendShape_cmd_(self):
        cmds.undoInfo(openChunk=True)
        try:
            print 'try'
            #csels,wsels,jntlist,replaceTrans
            sels=cmds.ls(sl=1)
            if len(sels)>=3:
                skmesh=sels[1]
                add=0
                if not skmesh[-1]=='_':
                    add=1
                    skmf=cmds.rename(skmesh,skmesh+'_')
                mxattr=edo_autoConnectCorrectBlendShapeCmd.edo_autoConnectCorrectBlendShape(1)
                if add==1:
                    cmds.rename(skmf,skmf[:-1])
            #self=ui
            self.edo_lineEditChanged_(self.loadskdb_le)
            if (not mxattr==[]) and mxattr:
                atxt=mxattr[0].split(':')[0]
                rtxt=mxattr[0].split(':')[1]
                at=self.edo_findItemFromGivenText(self.attribute_lw,atxt)
                if at:
                    self.attribute_lw.setCurrentItem(at)
                rt=self.edo_findItemFromGivenText(self.rotation_lw,rtxt)
                if rt:
                    self.rotation_lw.setCurrentItem(rt)
        except:
            cmds.undoInfo(closeChunk=True)
            #cmds.undo()
            print 'something was wrong in your scene'
            cmds.error('something was wrong in your scene')
        cmds.undoInfo(closeChunk=True)
 
    def edo_createSKDB_cmd_(self):
        cmds.undoInfo(openChunk=True)
        try:
            print 'try'
            #csels,wsels,jntlist,replaceTrans
            sels=cmds.ls(sl=1)
            sel=sels[0]
            edo_skeletonDrivingBallCmd.edo_addSkeletonBall(sel,1,None,None,8)
            skdb=sel+'_FRAME'
            if not cmds.objExists(skdb+'.SKDB'):
                cmds.addAttr(skdb,ln='SKDB',at='message')
            if len(sels)>1:
                print 'connect SKDB...'
                if not cmds.objExists(sels[1]+'.SKDB'):
                    cmds.addAttr(sels[1],ln='SKDB',at='message')
                cmds.connectAttr(sels[1]+'.SKDB',skdb+'.SKDB',f=1)
                cmds.setAttr(skdb+'Shape0.ovc',13)
        except:
            cmds.undoInfo(closeChunk=True)
            #cmds.undo()
            print 'something was wrong in your scene'
            cmds.error('something was wrong in your scene')
        cmds.undoInfo(closeChunk=True)

    def edo_lineEditChanged_(self,le):
        #lw=self.loadinfjnt_lw
        #le=self.loadskdb_le
        #self=ui
        print 'load attr and rotation'
        self.attribute_lw.clear()
        skdbf=str(self.loadskdb_le.text())
        aral=edo_autoConnectCorrectBlendShapeCmd.edo_findAllRecordedRotationAttributeFromSKDB(skdbf)
        if aral:
            for a in aral:
                #a=aral[0]
                if cmds.objExists(a):
                    an=a.split('.')[-1]
                    self.attribute_lw.addItem(an)
        if self.attribute_lw.count>=1:
            #self.attribute_lw.setCurrentRow(0)
            print 'done'
            
    def edo_loadskdb_cmd_(self):
        sels=cmds.ls(sl=1)
        if not sels==[]:
            self.loadskdb_le.setText(sels[0])
            self.edo_lineEditChanged_(self.loadskdb_le)
    
    def edo_loadctrl_cmd_(self):
        sels=cmds.ls(sl=1)
        if not sels==[]:
            self.loadctrl_le.setText(sels[0])
        
if cmds.window('edo_skeletonDrivingBallToolUI',q=1,ex=1):
    cmds.deleteUI('edo_skeletonDrivingBallToolUI')
mayawindow=edo_common.edo_getMayaWindow()
ui=edo_skeletonDrivingBallToolUI()
qtwindow=QtGui.QMainWindow(mayawindow)
ui.setupUi(qtwindow)
qtwindow.show()
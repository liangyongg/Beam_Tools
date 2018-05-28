from headfile import *
import maya.cmds as cmds
import edo_ThreePointMatherUI.edo_ThreePointMatherUIDesign as ETPMUI
import edo_ThreePointMatherUI.edo_ThreePointMatherCmd as ETPMC
import edo_common

#reload(ETPMC)
class edo_ThreePointMatherUI(ETPMUI.Ui_edo_ThreePointMatherUI):
    def setupUi(self, edo_ThreePointMatherUI):
        ETPMUI.Ui_edo_ThreePointMatherUI.setupUi(self,edo_ThreePointMatherUI)
        self.loadSource_bt.clicked.connect(self.edo_getSelectedSourcePoint_)
        self.loadTarget_bt.clicked.connect(self.edo_getSelectedTargetPoint_)
        self.transformMatch_bt.clicked.connect(self.edo_transformMatchCmd_)
        self.transformMatchMO_bt.clicked.connect(self.edo_transformMatchMOCmd_)
        self.controlerMatch_bt.clicked.connect(self.edo_ctrlMatchCmd_)
        print 'set trackSelection on...'
        t=cmds.selectPref( q=1,trackSelectionOrder=1 )
        if t==False:
            cmds.selectPref( trackSelectionOrder=1 )
            
    def edo_transformMatchCmd_(self):
        #undoflush=ui.undoflush_cb.isChecked()
        undoflush=self.undoflush_cb.isChecked()
        if undoflush==True:
            cmds.undoInfo(st=False)
        cmds.undoInfo(openChunk=True)
        try:
            ui.edo_transformMatchCmd()
        except:
            cmds.undoInfo(closeChunk=True) 
            print 'something was wrong in your scene'
            cmds.error('something was wrong in your scene')
            cmds.undoInfo(st=True)
        cmds.undoInfo(closeChunk=True)
        cmds.undoInfo(st=True)
        print 'done'
        
    def edo_transformMatchMOCmd_(self):
        undoflush=self.undoflush_cb.isChecked()
        if undoflush==True:
            cmds.undoInfo(st=False)
        cmds.undoInfo(openChunk=True)
        try:
            self.edo_transformMatchMOCmd()
        except:
            cmds.undoInfo(closeChunk=True) 
            print 'something was wrong in your scene'
            cmds.error('something was wrong in your scene')
            cmds.undoInfo(st=True)
        cmds.undoInfo(closeChunk=True)
        cmds.undoInfo(st=True)
        print 'done'
        
    def edo_ctrlMatchCmd_(self):
        undoflush=self.undoflush_cb.isChecked()
        #cpb=ui.constraint_pb.value()
        cpb=self.constraint_pb.value()
        if undoflush==True:
            cmds.undoInfo(st=False)
        cmds.undoInfo(openChunk=True)
        try:
            self.edo_ctrlMatchCmd(cpb)
        except:
            cmds.undoInfo(closeChunk=True) 
            print 'something was wrong in your scene'
            cmds.error('something was wrong in your scene')
            cmds.undoInfo(st=True)
        cmds.undoInfo(closeChunk=True)
        cmds.undoInfo(st=True)
        print 'done'
        
    def edo_ctrlMatchCmd(self,cpb):
        sids=[str(self.sourceOp_le.text()),str(self.sourceXp_le.text()),str(self.sourceZp_le.text())]
        print sids
        tids=[str(self.targetOp_le.text()),str(self.targetXp_le.text()),str(self.targetZp_le.text())]
        print tids
        useShear=int(self.shear_cb.isChecked())
        print useShear
        #ui.shear_cb.isChecked()
        ETPMC.edo_ThreePointMatherAsSelectedListCT(sids,tids,useShear,cpb)
        
    def edo_transformMatchCmd(self):
        sids=[str(self.sourceOp_le.text()),str(self.sourceXp_le.text()),str(self.sourceZp_le.text())]
        print sids
        tids=[str(self.targetOp_le.text()),str(self.targetXp_le.text()),str(self.targetZp_le.text())]
        print tids
        useShear=int(self.shear_cb.isChecked())
        print useShear
        #ui.shear_cb.isChecked()
        ETPMC.edo_ThreePointMatherAsSelectedList(sids,tids,useShear)
        
    def edo_transformMatchMOCmd(self):
        sids=[str(self.sourceOp_le.text()),str(self.sourceXp_le.text()),str(self.sourceZp_le.text())]
        print sids
        tids=[str(self.targetOp_le.text()),str(self.targetXp_le.text()),str(self.targetZp_le.text())]
        print tids
        useShear=int(self.shear_cb.isChecked())
        print useShear
        #ui.shear_cb.isChecked()
        ETPMC.edo_ThreePointMatherAsSelectedListMO(sids,tids,useShear)


    def edo_getSelectedSourcePoint_(self):
        #lineEditor=[self.sourceOp_le,self.sourceXp_le,self.sourceZp_le]
        sels=cmds.ls(os=1)
        pid=self.edo_pickUpId(sels)
        print pid
        if len(pid)>=1:
            self.sourceOp_le.setText(pid[0])
        if len(pid)>=2:
            self.sourceXp_le.setText(pid[1])
        if len(pid)>=3:
            self.sourceZp_le.setText(pid[2])
        
    def edo_getSelectedTargetPoint_(self):
        #lineEditor=[self.sourceOp_le,self.sourceXp_le,self.sourceZp_le]
        sels=cmds.ls(os=1)
        pid=self.edo_pickUpId(sels)
        print pid
        if len(pid)>=1:
            self.targetOp_le.setText(pid[0])
        if len(pid)>=2:
            self.targetXp_le.setText(pid[1])
        if len(pid)>=3:
            self.targetZp_le.setText(pid[2])
        
    def edo_pickUpId(self,points):
        #points=sels
        pid=[]
        for p in points:
            #p=points[0]
            #p='nurbsSphere1.cv[4][6]'
            ts=p.split('.')[-1].split('[')
            id=''
            for t in ts:
                #t=ts[2]
                tn=t.replace(']','')
                if tn.isdigit():
                   id=id+tn+':'
            id=id[:-1]
            print id
            if not id=='':
                pid.append(id)
        return pid
         
if cmds.window('edo_ThreePointMatherUI',q=1,ex=1):
    cmds.deleteUI('edo_ThreePointMatherUI')
mayawindow=edo_common.edo_getMayaWindow()
ui=edo_ThreePointMatherUI()
qtwindow=QtGui.QMainWindow(mayawindow)
ui.setupUi(qtwindow)
qtwindow.show()
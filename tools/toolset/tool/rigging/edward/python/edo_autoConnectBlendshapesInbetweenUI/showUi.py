#import edo_autoConnectBlendshapesInbetweenUI.showUi as showUi
#reload(ACBD)
from headfile import *
import maya.cmds as cmds
import maya.mel as mel
import edo_common
import edo_autoConnectBlendshapesInbetweenUI.edo_autoConnectBlendshapesDesign as ACBD;reload(ACBD)
import edo_autoConnectBlendshapesInbetweenUI.edo_createFacialCtrl as CFC;reload(CFC)
import edo_autoConnectBlendshapesInbetweenUI.edo_autoConnectBlendShapes as ACBS;reload(ACBS)
import edo_autoConnectBlendshapesInbetweenUI.edo_mirrorBlendShape as EMBS
import edo_autoConnectBlendshapesInbetweenUI.edo_transferMesh as ETFM
import edo_autoConnectBlendshapesInbetweenUI.edo_mathBlendShapeUI as EMBIUI
import edo_autoConnectBlendshapesInbetweenUI.edo_makeBlendShapeWeightNormalizePaintableUI as MBSWNPUI
import edo_createSoftDeformSecCtrlUI.edo_createSoftDeformSecCtrlUI as ECSDSCUI
import edo_autoConnectBlendshapesInbetweenUI.edo_crateNewBlendShapeMeshToNewMeshWindow as ENBSMTNMW
#import edo_autoConnectBlendshapesInbetweenUI.edo_createUnderWorldBlendShapeUI as ECUWBSUI
import edo_autoConnectBlendshapesInbetweenUI.edo_calculateBlendShapeCmd as edo_calculateBlendShapeCmd

class edo_autoConnectBlendshapesUI(ACBD.Ui_edo_autoConnectBlendshapesUI):
    def setupUi(self,edo_autoConnectBlendshapesUI):
        ACBD.Ui_edo_autoConnectBlendshapesUI.setupUi(self,edo_autoConnectBlendshapesUI)
        #self.basicCtrl_bt.setText(_fromUtf8("aaaaa"))
        #self.basicCtrl_bt.clicked.connect(BCFSUD_ACTJC.edo_addContorlToJointChain)
        self.dial.valueChanged.connect(self.setInbetweenWeightFromDial)
        #self.doubleSpinBox.editingFinished.connect(self.setInbetweenWeightFromSpinBox)
        self.createCtrlBt.clicked.connect(self.edo_addFacialCtrlCmd_)
        self.addMultiplyFrameBt.clicked.connect(self.edo_addMultiplyFrame_)
        self.renameBt.clicked.connect(self.edo_renameBlendShapeMeshInbetween_)
        self.autoConnectBt.clicked.connect(self.edo_autoConnectBlendshapes_)
        self.attachMeshBt.clicked.connect(self.edo_edo_addFollicelPlane_)
        self.blendshapeNameBt.clicked.connect(self.edo_getSelectedBlendshape_)
        self.blendshapeListLw.currentItemChanged.connect(self.edo_blendshapeListLwItemChangedCmd_)
        self.pickupSelectedBlendshapeBt.clicked.connect(self.edo_pickUpSelectedBlendshapes_)
        self.pickupAllBlendshapeBt.clicked.connect(self.edo_pickUpAllBlendshapes_)
        self.triangleMatcher_Bt.clicked.connect(self.edo_triangleMatcher_Bt_)
        self.secondaryControlerl_Bt.clicked.connect(self.edo_secondaryControlerl_Bt_)
        self.mirrorbs_bs.clicked.connect(self.edo_mirrorbs_Bt_)
        self.transfermeshes_bt.clicked.connect(self.edo_transfermeshes_Bt_)
        self.normalizedbs_bt.clicked.connect(self.edo_normalizedbs_Bt_)
        self.calculatebs_bt.clicked.connect(self.edo_calculatebs_Bt_)
        self.updateTopology_bt.clicked.connect(self.edo_updateTopology_Bt_)
        self.skeletonDrivingBall_Bt.clicked.connect(self.edo_skeletonDrivingBall_Bt_)
        self.calculateBs_Bt.clicked.connect(self.edo_calculateBs_Bt_)
        self.inbetweenListLw.itemDoubleClicked.connect(self.edo_inbetweenListLwDobleClicked_cmd_)
        self.underworldbs_Bt.clicked.connect(self.underworldbs_Bt_cmd_)
        self.facialeasyedit_Bt.clicked.connect(self.facialeasyedit_Bt_cmd)
        self.rbfPoseDeformer_Bt.clicked.connect(self.rbfPoseDeformer_Bt_cmd)
    
    def rbfPoseDeformer_Bt_cmd(self):
        print 'open rbfPoseDeformerUI...'
        import edo_RBFposeDeformerUI.showUi as edo_RBFposeDeformerUI;reload(edo_RBFposeDeformerUI)

    def facialeasyedit_Bt_cmd(self):
        print 'open edo_seperateChFacialBsUI...'
        import edo_seperateChFacialBsUI.showUi as edo_seperateChFacialBsUIShowUi;reload(edo_seperateChFacialBsUIShowUi)
        
    def underworldbs_Bt_cmd_(self):
        print 'run underworldBlendShape UI..'
        import edo_underworldBlendShapeUI.showUi as edo_underworldBlendShapeUI
        reload(edo_underworldBlendShapeUI)
        cmds.loadPlugin('underworldBlendShape',qt=1)

    def edo_inbetweenListLwDobleClicked_cmd_(self):
        print 'edo_inbetweenListLw is Doble Clicked..'
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
            ACBS.edo_pickupSelectedBlendshape(self.blendshapeNameLe,self.blendshapeListLw,self.inbetweenListLw,self.keepConnectionCb,0,1)
            if af==1:
                cmds.rename(mesh,mesh[:-1])
        except:
            cmds.undoInfo(closeChunk=True)
            #cmds.undo()
            print 'something was wrong in your scene'
            cmds.error('something was wrong in your scene')
        cmds.undoInfo(closeChunk=True)
        
    def edo_calculateBs_Bt_(self):
        print 'calculate blendshapes'
        cmds.undoInfo(openChunk=True)
        try:
            fbs=edo_calculateBlendShapeCmd.edo_calculateBlendShape(cmds.ls(sl=1)[0],cmds.ls(sl=1)[1])
            cmds.select(fbs,r=1)
            cmds.sets(fbs,e=1,forceElement='initialShadingGroup')   
        except:
            cmds.undoInfo(closeChunk=True)
            #cmds.undo()
            print 'something was wrong in your scene'
            cmds.error('something was wrong in your scene')
        cmds.undoInfo(closeChunk=True)
        
    def edo_skeletonDrivingBall_Bt_(self):
        print 'open edo_skeletonDrivingBallTool'
        import edo_skeletonDrivingBallToolUI.showUi as edo_skeletonDrivingBallToolUIshowUi
        reload(edo_skeletonDrivingBallToolUIshowUi)
        
    def edo_updateTopology_Bt_(self):
        print 'open updateTopologyTools' 
        ENBSMTNMW.edo_crateNewBlendShapeMeshToNewMeshWindow()
        
    def edo_calculatebs_Bt_(self): 
        print 'open calculatebsBlendShapeTools'
        EMBIUI.edo_mathBlendShapeUI()

    def edo_normalizedbs_Bt_(self):
        print 'open normalizeBlendShapeWeightsTools'
        MBSWNPUI.edo_makeBlendShapeWeightNormalizePaintableUI()
    
    def edo_transfermeshes_Bt_(self):
        print 'transfer meshes'
        cmds.undoInfo(openChunk=True)
        sels=cmds.ls(sl=1)
        if not sels:
            cmds.undoInfo(closeChunk=True)
            return False
        org=sels[0]
        sels=sels[1:]
        try:
            for sel in sels:
                print 'transfer to sels'
                cmds.select(org,r=1)
                cmds.select(sel,add=1)
                ETFM.edo_transferMesh()
        except:
            cmds.undoInfo(closeChunk=True)
            #cmds.undo()
            print 'something was wrong in your scene'
            cmds.error('something was wrong in your scene')
        cmds.undoInfo(closeChunk=True)
    
    def edo_mirrorbs_Bt_(self):
        print 'mirror blendshapes'
        cmds.undoInfo(openChunk=True)
        try:
            EMBS.edo_mirrorBlendShape()
        except:
            cmds.undoInfo(closeChunk=True)
            #cmds.undo()
            print 'something was wrong in your scene'
            cmds.error('something was wrong in your scene')
        cmds.undoInfo(closeChunk=True)
     
    def edo_addMultiplyFrame_(self):
        cmds.undoInfo(openChunk=True)
        try:
            CFC.edo_addMultiplyFrame(cmds.ls(sl=1))
        except:
            cmds.undoInfo(closeChunk=True)
            #cmds.undo()
            print 'something was wrong in your scene'
            cmds.error('something was wrong in your scene')
        cmds.undoInfo(closeChunk=True)
    
    def edo_secondaryControlerl_Bt_(self):
        print 'open secondaryControlerTool'
        ECSDSCUI.edo_createSoftDeformSecCtrlUI()

    def edo_triangleMatcher_Bt_(self):
        print 'open triangleMatcherTool' 
        import edo_ThreePointMatherUI.showUi as edo_ThreePointMatherUIshowUi
        reload(edo_ThreePointMatherUIshowUi)
        
    def setInbetweenWeightFromDial(self):
        value=self.dial.value()*0.01
        #print value
        self.doubleSpinBox.setValue(value)
        
    def setInbetweenWeightFromSpinBox(self):
        value=self.doubleSpinBox.value()
        #print value
        self.dial.setValue(value)
        
    def edo_addFacialCtrlCmd_(self):
        #self=ui
        cmds.undoInfo(openChunk=True)
        tx=str(self.ctrlNameLe.text())
        isctrl=self.isctrl_cb.isChecked()
        sfix='_CTRL'
        if isctrl==False:
            sfix='_CONNECT'
        try:
            CFC.edo_addFacialCtrlCmd(tx,'',0,sfix)
        except:
            cmds.undoInfo(closeChunk=True)
            #cmds.undo()
            print 'something was wrong in your scene'
            cmds.error('something was wrong in your scene')
        cmds.undoInfo(closeChunk=True)
     
    def edo_addMultiplyFrame_(self):
        cmds.undoInfo(openChunk=True)
        try:
            CFC.edo_addMultiplyFrame(cmds.ls(sl=1))
        except:
            cmds.undoInfo(closeChunk=True)
            #cmds.undo()
            print 'something was wrong in your scene'
            cmds.error('something was wrong in your scene')
        cmds.undoInfo(closeChunk=True)
            
    def edo_renameBlendShapeMeshInbetween_(self):
        cmds.undoInfo(openChunk=True)
        inbetween=str(self.doubleSpinBox.value())
        print inbetween
        try:
            ACBS.edo_renameBlendShapeMeshInbetween(inbetween)
        except:
            cmds.undoInfo(closeChunk=True)
            #cmds.undo()
            print 'something was wrong in your scene'
            cmds.error('something was wrong in your scene')
        cmds.undoInfo(closeChunk=True)
            
    def edo_autoConnectBlendshapes_(self):
        cmds.undoInfo(openChunk=True)
        try:
            sels=cmds.ls(sl=1)
            for sel in sels:
                cmds.select(sel,r=1)
                ACBS.edo_autoConnectBlendshapes()
        except:
            cmds.undoInfo(closeChunk=True)
            #cmds.undo()
            print 'something was wrong in your scene'
            cmds.error('something was wrong in your scene')
        cmds.undoInfo(closeChunk=True)
            
    def edo_edo_addFollicelPlane_(self):
        cmds.undoInfo(openChunk=True)
        try:
            ACBS.edo_addFollicelPlane()
        except:
            cmds.undoInfo(closeChunk=True)
            #cmds.undo()
            print 'something was wrong in your scene'
            cmds.error('something was wrong in your scene')
        cmds.undoInfo(closeChunk=True)
            
    def edo_getSelectedBlendshape_(self):
        cmds.undoInfo(openChunk=True)
        try:
            ACBS.edo_getSelectedBlendshape(self.blendshapeNameLe,self.blendshapeListLw)
        except:
            cmds.undoInfo(closeChunk=True)
            #cmds.undo()
            print 'something was wrong in your scene'
            cmds.error('something was wrong in your scene')
        cmds.undoInfo(closeChunk=True)
            
    def edo_blendshapeListLwItemChangedCmd_(self):
        #print 'blendshapeListLw selected item changed'
        ACBS.edo_getBlendshapeAttrInbetweenList(self.blendshapeNameLe,self.blendshapeListLw,self.inbetweenListLw)
        
    def edo_pickUpSelectedBlendshapes_(self):
        #print 'aaa'
        #self=ui
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
            ACBS.edo_pickupSelectedBlendshape(self.blendshapeNameLe,self.blendshapeListLw,self.inbetweenListLw,self.keepConnectionCb,0)
            if af==1:
                cmds.rename(mesh,mesh[:-1])
        except:
            cmds.undoInfo(closeChunk=True)
            #cmds.undo()
            print 'something was wrong in your scene'
            cmds.error('something was wrong in your scene')
        cmds.undoInfo(closeChunk=True)

    def edo_pickUpAllBlendshapes_(self):
        #print 'aaa'
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
            ACBS.edo_pickupSelectedBlendshape(self.blendshapeNameLe,self.blendshapeListLw,self.inbetweenListLw,self.keepConnectionCb,1)
            if af==1:
                cmds.rename(mesh,mesh[:-1])
        except:
            cmds.undoInfo(closeChunk=True)
            #cmds.undo()
            print 'something was wrong in your scene'
            cmds.error('something was wrong in your scene')
        cmds.undoInfo(closeChunk=True)

if cmds.window('edo_autoConnectBlendshapesUI',q=1,ex=1):
    cmds.deleteUI('edo_autoConnectBlendshapesUI')
mayawindow=edo_common.edo_getMayaWindow()
ui=edo_autoConnectBlendshapesUI()
qtwindow=QtGui.QMainWindow(mayawindow)
ui.setupUi(qtwindow)
qtwindow.show()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from head import *
import maya.cmds as cmds
import pymel.core as pm
import maya.OpenMaya as OpenMaya
import ui_reference_widget
reload(ui_reference_widget)
from ui_reference_widget import ui_reference_widget
from qtundo.undo import qtundo
from customize.maya_customize import maya_customize

class ui_reference_window(QtWidgets.QDialog):

    def __init__(self,parent = None):
        super(ui_reference_window,self).__init__(parent)

        self.reference_objects_skingeo = "reference_objects_skingeo"
        self.copy_objects_skingeo = "copy_objects_skingeo"

        self.reference_objects_con = "reference_objects_con"
        self.reference_objects_deform = "reference_objects_deform"

        self.copy_objects_deform = "copy_objects_deform"

        self.setupUi()

    def setupUi(self):
        self.ui_reference_widget = ui_reference_widget()
        #self.ui_taskview_widget.setupUi(self)
        QWidgetvboxLayout = QtWidgets.QVBoxLayout(self)
        QWidgetvboxLayout.addWidget(self.ui_reference_widget)
        QWidgetvboxLayout.setContentsMargins(0,0,0,0)

    @qtundo
    def createreferenceobjets(self):
        if not cmds.objExists (self.reference_objects_skingeo):
            cmds.createNode("transform",name = self.reference_objects_skingeo)
            cmds.createNode("transform",name = "base_objects_skingeo",p = self.reference_objects_skingeo)
            cmds.createNode ("transform", name = self.copy_objects_skingeo, p = self.reference_objects_skingeo)
        if not cmds.objExists (self.reference_objects_con):
            cmds.createNode("transform",name = self.reference_objects_con)
        if not cmds.objExists (self.reference_objects_deform):
            cmds.createNode("transform", name = self.reference_objects_deform)
            cmds.createNode ("transform", name = "base_objects_deform",p = self.reference_objects_deform)
            cmds.createNode ("transform", name = self.copy_objects_deform, p = self.reference_objects_deform)

    @qtundo
    def duplicate_model(self,type=""):
        selections = pm.ls(sl=1)
        print selections
        if selections:
            for selection in selections:
                if selection.getShape():
                    print selection.getShape()
                    dup_obj_str = "%s_%s" % (selection.name(),type)
                    if ":" in selection.name():
                        obj_name = selection.name().split(":")[-1]
                        dup_obj_str = "%s_%s" % (obj_name,type)
                    dup_obj = selection.duplicate(rr=1,name = dup_obj_str)[0]
                    print dup_obj
                    self.delete_orig_shape([dup_obj])
                    if type == "skingeo_bs":
                        dup_obj.setParent(self.copy_objects_skingeo)
                    if type =="blend_bs":
                        dup_obj.setParent (self.copy_objects_deform)

    def importReference(self):
        ref_cls = maya_customize()
        refNodes = ref_cls.get_RefereceNodes()
        mFile = OpenMaya.MFileIO()
        for i in range (refNodes.length ()):
            ref_filename = mFile.getReferenceFileByNode(refNodes[i])
            cmds.file(ref_filename,importReference=1)

    #@qtundo
    def delete_orig_shape(self,obj_list):
        for obj in obj_list:
            if pm.objExists(obj):
                shapes = obj.getShapes()
                print shapes
                if shapes:
                    for shape in shapes:
                        if shape.intermediateObject.get():
                            pm.delete(shape)

    def getElems (self):
        self.Reference_pushButton = self.ui_reference_widget.main_Widget.Reference_pushButton
        self.Duplicate_pushButton = self.ui_reference_widget.main_Widget.Duplicate_pushButton
        self.Duplicate_skinpushButton = self.ui_reference_widget.main_Widget.Duplicate_skinpushButton
        self.Importobj_pushButton = self.ui_reference_widget.main_Widget.Importobj_pushButton


    def connection(self):
        self.Reference_pushButton.clicked.connect (self.createreferenceobjets)
        self.Duplicate_pushButton.clicked.connect (lambda :self.duplicate_model('skingeo_bs'))
        self.Duplicate_skinpushButton.clicked.connect (lambda: self.duplicate_model ('blend_bs'))
        self.Importobj_pushButton.clicked.connect (self.importReference)

    def showUI(self):
        self.getElems()
        self.connection()
        try:
            self.close()
        except:
            pass
        self.show()

if __name__=="__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = ui_reference_window()
    ui.show()
    sys.exit(app.exec_())
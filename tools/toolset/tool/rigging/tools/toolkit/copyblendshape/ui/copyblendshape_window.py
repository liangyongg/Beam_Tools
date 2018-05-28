#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rigging.tools.ui.head import *
import copyblendshape_widget
reload(copyblendshape_widget)
from copyblendshape_widget import copyblendshape_widget
from rigging.tools.toolkit.copyblendshape.core import copyblendshape
reload(copyblendshape)
from qtundo import undo
import maya.cmds as cmds

class copyblendshape_window(QtGui.QDialog):

    def __init__(self,parent = None):
        super(copyblendshape_window,self).__init__(parent)
        self.setWindowTitle("Copy Blendshape")

        self.setupUi()
        self.getElems()
        self.setDefault()
        self.setupConnnections()

    def setupUi(self):
        self.copyblendshape_widget = copyblendshape_widget()
        #self.ui_taskview_widget.setupUi(self)
        QWidgetvboxLayout = QtGui.QVBoxLayout(self)
        QWidgetvboxLayout.addWidget(self.copyblendshape_widget)
        QWidgetvboxLayout.setContentsMargins(0,0,0,0)

    def getElems(self):
        self.CopyBlendShape_lineEdit01 = self.copyblendshape_widget.main_Widget.CopyBlendShape_lineEdit01
        self.Load_pushButton01 = self.copyblendshape_widget.main_Widget.Load_pushButton01
        self.CopyBlendShape_lineEdit02 = self.copyblendshape_widget.main_Widget.CopyBlendShape_lineEdit02
        self.CopyBlendShape_listWidget01 = self.copyblendshape_widget.main_Widget.CopyBlendShape_listWidget01
        self.Load_pushButton02 = self.copyblendshape_widget.main_Widget.Load_pushButton02
        self.CopyBlendShape_listWidget02 = self.copyblendshape_widget.main_Widget.CopyBlendShape_listWidget02
        self.CopyBlendShape_pushButton = self.copyblendshape_widget.main_Widget.CopyBlendShape_pushButton


    def setDefault(self):
        pass

    def setupConnnections(self):
        self.Load_pushButton01.clicked.connect(lambda :self.getObjectToLineEditCmd("surceObject"))
        self.CopyBlendShape_lineEdit01.textChanged.connect(lambda :self.getSourceObjectBlendshapeCmd())
        self.CopyBlendShape_lineEdit02.textChanged.connect(lambda :self.fillInSourceBSAttributesToList())
        self.Load_pushButton02.clicked.connect(lambda :self.getObjectToTargetListWidgetCmd())
        self.CopyBlendShape_pushButton.clicked.connect(lambda :self.copyBlendShapeCmd())

    def getObjectToLineEditCmd(self,lineEdit):
        selections = cmds.ls(sl=1)
        if selections:
            if lineEdit == "surceObject":
                if cmds.listRelatives(selections[0],c=1,s=1):
                    self.CopyBlendShape_lineEdit01.setText(selections[0])
                else:
                    self.CopyBlendShape_lineEdit01.setText('')
                    self.CopyBlendShape_lineEdit02.setText('')
                    self.CopyBlendShape_listWidget01.clear()
                    raise Exception('select objet have not shape node!!!')
        else:
            raise Exception("you must select one object!")

    def fillInSourceBSAttributesToList(self):
        sourceBS = self.CopyBlendShape_lineEdit02.text()
        bsAttrList = cmds.listAttr("%s.w" % (sourceBS),m=1)
        self.CopyBlendShape_listWidget01.clear()
        self.CopyBlendShape_listWidget01.addItems(bsAttrList)

    def getSourceObjectBlendshapeCmd(self):
        sourceObj = self.CopyBlendShape_lineEdit01.text()

        bsNode = copyblendshape.getBlendShapeNode(sourceObj)
        if bsNode:
            self.CopyBlendShape_lineEdit02.setText(bsNode)
        else:
            raise Exception("%s hava not blendshape node !"%sourceObj)

    def getObjectToTargetListWidgetCmd(self):
        selections = cmds.ls(sl=1)
        if selections:
            self.CopyBlendShape_listWidget02.clear()
            for selection in selections:
                if cmds.listRelatives(selection,c=1,s=1):
                    self.CopyBlendShape_listWidget02.addItem(selection)
        else:
            raise Exception("need select objects!")

    @undo.qtundo
    def copyBlendShapeCmd(self):
        source_object = self.CopyBlendShape_lineEdit01.text()
        source_bs = self.CopyBlendShape_lineEdit02.text()

        select_bs_geoList = self.CopyBlendShape_listWidget01.selectedItems()
        select_bsAttr_str_List = [i.text() for i in select_bs_geoList]

        destination_obj_list = []
        for i in xrange(self.CopyBlendShape_listWidget02.count()):
            destination_obj_list.append(self.CopyBlendShape_listWidget02.item(i))
        if not destination_obj_list:
            raise Exception("Need load target object to UI!")
        destination_obj_str_list = [i.text() for i in destination_obj_list]

        for destination_obj_str in destination_obj_str_list:
            copyblendshape.copyBlendShape(source_object,destination_obj_str,source_bs,0,select_bsAttr_str_List)


if __name__=="__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = copyblendshape_window()
    ui.show()
    sys.exit(app.exec_())
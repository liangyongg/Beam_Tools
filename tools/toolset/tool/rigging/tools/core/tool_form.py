# -*- coding: utf-8 -*-

import os
import sys
import functools
#import glob
from rigging.tools.ui.head import *
from rigging.tools.ui.ui_main_window import ui_main_window
from rigging.tools.ui.repair_window import repair_window
from rigging.tools.toolkit.copyblendshape.ui import copyblendshape_window
reload(copyblendshape_window)
from customize import mayamainwindow
#from rigging.tools.env.Config import Config

try:
    import pymel.core as pm
    import maya.cmds as cmds
    import maya.OpenMaya as OpenMaya
    import maya.OpenMayaAnim as OpenMayaAnim
except:
    pass

class From(QtGui.QMainWindow):

    def __init__(self,parent = None):
        super(From,self).__init__(parent)

        self.setWindowTitle ("rigging_tools")
        self.setupUI()
        self.getElems()
        self.setDefault()
        self.connections()

    def setupUI (self):
        self.ui_main_window = ui_main_window ()
        self.setCentralWidget (self.ui_main_window)

        self.Warning_Dialog = repair_window(self)

        self.copyblendshapeUI = copyblendshape_window.copyblendshape_window(mayamainwindow.getMayaWindow())

    def getElems(self):
        self.removeunuseinfluence_pushButton = self.ui_main_window.ui_rigtools_widget.main_Widget.removeunuseinfluence_pushButton
        self.checkaimkeys_pushButton = self.ui_main_window.ui_rigtools_widget.main_Widget.checkaimkeys_pushButton
        self.djRivet_pushButton = self.ui_main_window.ui_rigtools_widget.main_Widget.djRivet_pushButton
        self.copySikinWeights_pushButton = self.ui_main_window.ui_rigtools_widget.main_Widget.copySikinWeights_pushButton
        self.copyblendshape_pushButton = self.ui_main_window.ui_rigtools_widget.main_Widget.copyblendshape_pushButton

        self.repair_pushButton = self.Warning_Dialog.ui_repair_widget.main_Widget.repair_pushButton
        self.update_pushButton = self.Warning_Dialog.ui_repair_widget.main_Widget.update_pushButton
        self.repair_tableWidget = self.Warning_Dialog.ui_repair_widget.main_Widget.repair_tableWidget

    def setDefault(self):
        pass

    def connections(self):
        #self.repair_pushButton.clicked.connect(self.checkAnimKeys)
        #QtCore.QObject.connect (self.repair_pushButton, QtCore.SIGNAL ("clicked"), self.checkAnimKeys)
        QtCore.QObject.connect (self.removeunuseinfluence_pushButton,QtCore.SIGNAL("clicked()"),self.removeunuseinfluence)

        QtCore.QObject.connect (self.checkaimkeys_pushButton, QtCore.SIGNAL ("clicked()"),self.checkAnimKeys)
        #self.checkaimkeys_pushButton.clicked.connect (self.checkAnimKeys)
        QtCore.QObject.connect (self.djRivet_pushButton, QtCore.SIGNAL ("clicked()"), self.djRivet)
        QtCore.QObject.connect (self.copySikinWeights_pushButton, QtCore.SIGNAL ("clicked()"), self.copy_skin)
        QtCore.QObject.connect (self.copyblendshape_pushButton, QtCore.SIGNAL ("clicked()"), self.show_copyblendshape_Win)

    def checkAnimKeys(self):
        animCurveTypes = ['animCurveTA','animCurveTL','animCurveTT','animCurveTU']
        key_objs = list()
        animCurvesNode = list()
        for animCurveType in animCurveTypes:
            animCurves = pm.ls(type=animCurveType)
            if animCurves:
                animCurvesNode.extend (animCurves)
                for animCurve in animCurves:
                    objs = animCurve.outputs(d=1,plugs=0)
                    if objs:
                        key_objs.extend(objs)
        if key_objs:
            self.repair_tableWidget.clear()
            key_objs = list(set(key_objs))
            animCurvesNode = list(set(animCurvesNode))
            print key_objs,animCurvesNode
            pm.select(key_objs)
            self.repair_tableWidget.setRowCount (len (key_objs))
            self.repair_tableWidget.setColumnCount (len (animCurvesNode))

            for i in range(self.repair_tableWidget.rowCount()):
                self.repair_tableWidget.setVerticalHeaderItem(i,QtGui.QTableWidgetItem(unicode(key_objs[i])))
                for j in range(self.repair_tableWidget.columnCount()):
                    self.repair_tableWidget.setItem(i,j,QtGui.QTableWidgetItem(unicode(animCurvesNode[i])))
            try:
                self.Warning_Dialog.close()
            finally:
                self.Warning_Dialog.show()

    def removeunuseinfluence(self):
        pm.mel.eval("removeUnusedInfluences;")

    def djRivet(self):
        path = os.path.dirname(os.path.realpath(__file__))
        djRivet_mel = "djRivet.mel"
        djRivet_mel_path = os.path.join(path,djRivet_mel).replace("\\","/")

        #print djRivet_mel_path
        cmd = "source \"%s\";djRivet;"%(djRivet_mel_path)
        pm.mel.eval(cmd)

    def copy_skin(self):
        selections = cmds.ls(sl=1)
        for i in xrange(len(selections)):
            if 0<i<len(selections):
                self.maya_copyskinweights(selections[0],selections[i])

    def findSkinCluster (self,dagpath):
        skinCluster = OpenMaya.MObject ()
        geomNode = dagpath.node ()
        dgIt = OpenMaya.MItDependencyGraph (geomNode, OpenMaya.MFn.kSkinClusterFilter,
                                            OpenMaya.MItDependencyGraph.kUpstream)
        skinCluster = dgIt.currentItem ()
        return skinCluster

    def getinfluenceObjects (self,obj):
        msel = OpenMaya.MSelectionList ()
        # OpenMaya.MGlobal.getActiveSelectionList(msel)
        msel.add (obj)
        objPath = OpenMaya.MDagPath ()
        msel.getDagPath (0, objPath)
        objPath.extendToShape ()
        mobj = self.findSkinCluster (objPath)
        skin = OpenMayaAnim.MFnSkinCluster (mobj)
        infs = OpenMaya.MDagPathArray ()
        nInfs = skin.influenceObjects (infs)
        return [infs [i].fullPathName () for i in range (nInfs)]

    def maya_copyskinweights(self,base,target):
        infs = self.getinfluenceObjects(base)
        if infs:
            cmds.select(infs,target)
            cmds.skinCluster(toSelectedBones=1,maximumInfluences=5,dropoffRate=4,name=target+"_skinCluster")

            cmds.copySkinWeights(base,target,surfaceAssociation = "closestPoint",influenceAssociation= ["oneToOne","closestJoint","closestBone"],noMirror = True)

    def show_copyblendshape_Win(self):
        try:
            self.copyblendshapeUI.close()
        except:
            pass
        self.copyblendshapeUI.show ()
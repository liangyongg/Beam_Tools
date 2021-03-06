import difflib
import json
import logging
import os
import re
import traceback

import maya.cmds as cmds
from rigging.beam.ui.Qt import QtWidgets, QtGui, QtCore
from rigging.beam import plugins
from rigging.beam.core.objects.rig import Rig
from kbackdrop import KBackdrop
import pyflowgraph.graph_view_widget
reload(pyflowgraph.graph_view_widget)
from pyflowgraph.graph_view_widget import GraphViewWidget
import kgraph_view
reload(kgraph_view)
from kgraph_view import KGraphView

class KGraphViewWidget(GraphViewWidget):

    rigNameChanged = QtCore.Signal ()

    def __init__(self, parent=None):

        # constructors of base classes
        super(KGraphViewWidget, self).__init__(parent)

        self._builder = None
        self._guideBuilder = None
        self.guideRig = None

        graphView = KGraphView (parent = self)
        self.setGraphView (graphView)
        self.newRigPreset ()

    # ============
    # Rig Methods
    # ============
    def editRigName(self):
        dialog = QtWidgets.QInputDialog(self)
        dialog.setObjectName('RigNameDialog')
        text, ok = dialog.getText(self, 'Edit Rig Name', 'New Rig Name', text=self.guideRig.getName())

        if ok is True:
            self.setGuideRigName(text)

    def setGuideRigName(self, text):
        if text.endswith('_guide') is True:
            text = text.replace('_guide', '')

        self.guideRig.setName(text)
        self.rigNameChanged.emit()

    def newRigPreset(self):
        try:
            print "KGraphViewWidget.newRigPreset"
            self.guideRig = Rig()
            graphview=self.getGraphView()
            graphview.displayGraph(self.guideRig)
            self.setGuideRigName('MyRig')

            self.openedFile = None

            self.window().setWindowTitle('Beam Editor')

            print "newRigPreset,New Rig Created"

        except:
            print "newRigPreset,Error Creating New Rig"

    def buildGuideRig(self):
        self.window ().setCursor (QtCore.Qt.WaitCursor)

        if self.guideRig.getName().endswith('_guide') is False:
            self.guideRig.setName(self.guideRig.getName() + '_guide')

        if self._guideBuilder:
            self._guideBuilder.deleteBuildElements ()
        self._guideBuilder = plugins.getBuilder ()
        self._guideBuilder.build (self.guideRig)

        self.window ().setCursor (QtCore.Qt.ArrowCursor)

    def buildRig(self):
        print "buildRig"

    # ==============
    # Other Methods
    # ==============
    def addBackdrop(self, name='Backdrop'):
        graphView = self.getGraphView()

        initName = name
        suffix = 1
        collision = True
        while collision:

            collision = graphView.hasNode(name)
            if not collision:
                break

            result = re.split(r"(\d+)$", initName, 1)
            if len(result) > 1:
                initName = result[0]
                suffix = int(result[1])

            name = initName + str(suffix).zfill(2)
            suffix += 1

        backdropNode = KBackdrop(graphView, name)
        graphView.addNode(backdropNode)

        graphView.selectNode(backdropNode, clearSelection=True)

        return backdropNode

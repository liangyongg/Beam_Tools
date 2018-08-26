import os
import sys
import inspect
from functools import partial
import pymel.core as pm

from rigging.beam.ui.Qt import QtWidgets, QtGui, QtCore,QtCompat
from rigging.beam.ui import pyqt
import rigging.beam.core
from rigging.beam.core import shifter, skin, utils

for i in [shifter, skin, utils]:
    reload(i)

class BeamUI(QtWidgets.QWidget):
    """A debugger widget hosting an inspector as well as a graph view"""

    def __init__(self, parent=None):

        # constructors of base classes
        super(BeamUI, self).__init__(parent)
        self.setObjectName('mainUI')
        self.setWindowIcon(QtGui.QIcon(''))

        self.setWindowTitle("Beam Editor")
        self.setAcceptDrops(True)

        self.mainVboxLayout = QtGui.QVBoxLayout (self)

        self.guideLayout = QtGui.QVBoxLayout ()
        self.mainVboxLayout.addLayout(self.guideLayout)

        self.build_from_selection = QtGui.QPushButton("build_from_selection")
        self.mainVboxLayout.addWidget(self.build_from_selection)

        compDir = shifter.getComponentDirectories ()

        path = self.current_path ()

        trackLoadComponent = []

        for path, comps in compDir.iteritems ():
            for comp_name in comps:

                if comp_name in trackLoadComponent:
                    pm.displayWarning(
                        "Custom component name: %s, already in default "
                        "components. Names should be unique. This component is"
                        " not loaded" % comp_name)
                    continue
                else:
                    trackLoadComponent.append (comp_name)
                if not os.path.exists(os.path.join(path,
                                                   comp_name, "__init__.py")):
                    continue
                module = shifter.importComponentGuide (comp_name)
                print "BeamUI.__init__.module",module
                reload (module)

                commandbutton = self.loadUiWidget (os.path.join (path.replace("beam_components","widgets"), "commandbutton.ui"))

                icon = QtGui.QPixmap(os.path.join (path,module.TYPE,"icon.jpg"))
                self.guideLayout.addWidget (commandbutton)
                commandbutton.pushButton.setText(module.TYPE)
                commandbutton.label.setPixmap (icon)
                QtCore.QObject.connect (commandbutton.pushButton, QtCore.SIGNAL ("clicked()"),
                                        partial (self.drawComp, module.TYPE))

        self.createConnections()

    def createConnections(self):
        QtCore.QObject.connect (self.build_from_selection, QtCore.SIGNAL ("clicked()"),
                                partial (self.buildFromSelection))

    def current_path(self):
        path = os.path.realpath(sys.path[0])
        if os.path.isfile(path):
            path = os.path.dirname(path)
            return os.path.abspath(path)
        else:
            caller_file=inspect.stack()[1][1]
            return os.path.abspath(os.path.dirname(caller_file))

    def loadUiWidget(self,uifilename,parent=None):
        ui = QtCompat.load_ui(uifilename)
        return ui

    def drawComp(self, compType, *args):

        guide = shifter.guide.Rig()

        if pm.selected():
            parent = pm.selected()[0]
        else:
            parent = None

        guide.drawNewComponent(parent, compType)

    @classmethod
    def buildFromSelection(self, *args):

        logWin = pm.window(title="Shifter Build Log", iconName='Shifter Log')
        pm.columnLayout(adjustableColumn=True)
        pm.cmdScrollFieldReporter(width=800, height=500, clr=True)
        pm.button(label='Close', command=('import pymel.core as pm\npm.deleteUI(\"' + logWin +'\", window=True)'))
        pm.setParent('..')
        pm.showWindow(logWin)
        rigging.beam.logInfos()
        rg = shifter.Rig()
        rg.buildFromSelection()

    @classmethod
    def inspectProperties(self, *args):
        oSel = pm.selected ()
        if oSel:
            root = oSel[0]
        else:
            pm.displayWarning("please select one object from the componenet guide")
            return
        pm.createNode("joint")

    @classmethod
    def inspectSettings(self, *args):

        oSel = pm.selected()
        if oSel:
            root = oSel[0]
        else:
            pm.displayWarning("please select one object from the componenet guide")
            return

        comp_type = False
        guide_root = False
        while root:
            if pm.attributeQuery("comp_type", node=root, ex=True):
                comp_type = root.attr("comp_type").get()
                break
            elif pm.attributeQuery("ismodel", node=root, ex=True):
                guide_root = root
                break
            root = root.getParent()
            pm.select(root)

        if comp_type:
            guide = shifter.importComponentGuide(comp_type)
            pyqt.showDialog(guide.componentSettings)

        elif guide_root:
            module_name = "mgear.maya.shifter.guide"
            guide = __import__(module_name, globals(), locals(), ["*"], -1)
            pyqt.showDialog(guide.guideSettings)

        else:
            pm.displayError("The selected object is not part of component guide")
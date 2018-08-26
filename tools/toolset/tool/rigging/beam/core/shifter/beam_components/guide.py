
from functools import partial

import maya.cmds as cmds
# pyMel
import pymel.core as pm
from pymel.core import datatypes

# beam
import rigging.beam

from rigging.beam.core.general import string

from rigging.beam.core import dag, vector, transform, applyop, attribute, curve, icon
for i in [dag, vector, transform, applyop, attribute, curve, icon]:
    reload(i)

from rigging.beam.core.shifter import guide
from rigging.beam.ui.beam_ui import BeamUI

import mainSettingsUI as msui

from rigging.beam.ui.Qt import QtWidgets, QtGui, QtCore


class ComponentGuide(guide.Main):

    compType = "component"  # Component type
    compName = "component"  # Component default name
    compSide = "C"
    compIndex = 0  # Component default index

    description = ""  # Description of the component

    connectors = []
    compatible = []
    ctl_grp = ""

    def __init__(self):

        self.paramNames = []
        self.paramDefs = {}
        self.values = {}

        self.valid = True

        self.root = None
        self.id = None

        self.parentComponent = None
        self.parentLocalName = None

        self.tra = {}  # dictionary of global transform
        self.atra = []  # list of global transform
        self.pos = {}  # dictionary of global postion
        self.apos = []  # list of global position
        self.prim = {}  # dictionary of primitive
        self.blades = {}
        self.size = .1

        self.save_transform = []
        self.save_primitive = []
        self.save_blade = []
        self.minmax = {}

        self.postInit()
        self.initialHierarchy()
        self.addParameters()


    def postInit(self):
        self.save_transform = ["root"]
        return

    def initialHierarchy(self):
        self.pCompType = self.addParam("comp_type", "string", self.compType)
        self.pCompName = self.addParam("comp_name", "string", self.compName)
        self.pCompSide = self.addParam("comp_side", "string", self.compSide)
        self.pCompIndex = self.addParam("comp_index", "long", self.compIndex, 0)
        self.pConnector = self.addParam("connector", "string", "standard")
        self.pUIHost = self.addParam("ui_host", "string", "")
        self.pCtlGroup = self.addParam("ctlGrp", "string", "")

        # Items -------------------------------------------
        typeItems = [self.compType, self.compType]
        for type in self.compatible:
            typeItems.append(type)
            typeItems.append(type)

        connectorItems = ["standard", "standard"]
        for item in self.connectors:
            connectorItems.append(item)
            connectorItems.append(item)

    def addObjects(self):
        self.root = self.addRoot()

    def addParameters(self):
        return

    def addDispCurve(self, name, centers=[], degree=1):
        return icon.connection_display_curve(self.getName(name),centers,degree)

    # ====================================================
    # DRAW

    def draw(self, parent):
        self.parent = parent
        self.setIndex(self.parent)
        self.addObjects()
        print "shifter.beam_component.ComponentGuide.draw"
        pm.select(self.root)

    def drawFromUI(self, parent):
        if not self.modalPositions():
            rigging.beam.log("aborded", rigging.beam.sev_warning)
            return False

        self.draw(parent)
        transform.resetTransform(self.root, r=False, s=False)

        BeamUI.inspectSettings()

        return True

    # ====================================================
    # UPDATE

    def setIndex(self, model):
        self.model = model.getParent(generations=-1)

        # Find next index available
        while True:
            obj = dag.findChild(self.model, self.getName("root"))
            if not obj or (self.root and obj == self.root):
                break
            self.setParamDefValue("comp_index", self.values["comp_index"] + 1)

    def modalPositions(self):
        """Launch a modal dialog to set position of the guide."""
        self.jNumberVal = False
        self.dirAxisVal = False
        self.jSpacVal = False

        for name in self.save_transform:

            if "#" in name:

                def _addLocMultiOptions():

                    pm.setParent(q=True)

                    pm.columnLayout(adjustableColumn=True, cal="right")
                    pm.text(label='', al="center")

                    fl = pm.formLayout()
                    jNumber = pm.intFieldGrp(v1=3, label="Joint Number")
                    pm.setParent('..')
                    pm.formLayout(fl, e=True, af=(jNumber, "left", -30))

                    dirSet = ["X", "-X", "Y", "-Y", "Z", "-Z"]
                    fl = pm.formLayout()
                    dirAxis = pm.optionMenu(label="Direction")
                    dirAxis.addMenuItems(dirSet)
                    pm.setParent('..')
                    pm.formLayout(fl, e=True, af=(dirAxis, "left", 70))

                    fl = pm.formLayout()
                    jSpac = pm.floatFieldGrp(v1=1.0, label="spacing")
                    pm.setParent('..')
                    pm.formLayout(fl, e=True, af=(jSpac, "left", -30))

                    pm.text(label='', al="center")

                    pm.button(label='Continue', c=partial(
                        _retriveOptions, jNumber, dirAxis, jSpac))
                    pm.setParent('..')

                def _retriveOptions(jNumber, dirAxis, jSpac, *args):
                    self.jNumberVal = jNumber.getValue()[0]
                    self.dirAxisVal = dirAxis.getValue()
                    self.jSpacVal = jSpac.getValue()[0]

                    pm.layoutDialog(dismiss="Continue")

                def _show():

                    pm.layoutDialog(ui=_addLocMultiOptions)

                _show()

                if self.jNumberVal:
                    if self.dirAxisVal == "X":
                        offVec = datatypes.Vector(self.jSpacVal, 0, 0)
                    elif self.dirAxisVal == "-X":
                        offVec = datatypes.Vector(self.jSpacVal * -1, 0, 0)
                    elif self.dirAxisVal == "Y":
                        offVec = datatypes.Vector(0, self.jSpacVal, 0)
                    elif self.dirAxisVal == "-Y":
                        offVec = datatypes.Vector(0, self.jSpacVal * -1, 0)
                    elif self.dirAxisVal == "Z":
                        offVec = datatypes.Vector(0, 0, self.jSpacVal)
                    elif self.dirAxisVal == "-Z":
                        offVec = datatypes.Vector(0, 0, self.jSpacVal * -1)

                    newPosition = datatypes.Vector(0, 0, 0)
                    for i in range(self.jNumberVal):
                        newPosition = offVec + newPosition
                        localName = string.replaceSharpWithPadding(name, i)
                        self.tra[localName] = transform.getTransformFromPos(newPosition)

        return True

    def addRoot(self):
        if "root" not in self.tra.keys():
            self.tra["root"] = transform.getTransformFromPos(datatypes.Vector(0, 0, 0))

        self.root = icon.guideRootIcon(self.parent, self.getName("root"), color=13, m=self.tra["root"])

        # Add Parameters from parameter definition list.
        for scriptName in self.paramNames:
            paramDef = self.paramDefs[scriptName]
            paramDef.create(self.root)

        return self.root

    def addLoc(self, name, parent, position=None):
        if name not in self.tra.keys():
            self.tra[name] = transform.getTransformFromPos(position)
        if name in self.prim.keys():
            # this functionality is not implemented. The actual design from
            # softimage Gear should be review to fit in Maya.
            loc = self.prim[name].create(parent, self.getName(name), self.tra[name], color=17)
        else:
            loc = icon.guideLocatorIcon(parent, self.getName(name), color=17, m=self.tra[name])

        return loc

        # ====================================================
        # SET / GET

    def setFromHierarchy (self, root):
        """Set the component guide from given hierarchy.

        Args:
            root (dagNode): The root of the hierarchy to parse.

        """
        self.root = root
        self.model = self.root.getParent (generations = -1)

        # ---------------------------------------------------
        # First check and set the settings
        if not self.root.hasAttr ("comp_type"):
            rigging.beam.log ("%s is not a proper guide." %self.root.longName (), rigging.beam.sev_error)
            self.valid = False
            return

        self.setParamDefValuesFromProperty (self.root)

        # ---------------------------------------------------
        # Then get the objects
        for name in self.save_transform:
            if "#" in name:
                i = 0
                while not self.minmax [name].max>0 or i< self.minmax [name].max:
                    localName = string.replaceSharpWithPadding (name, i)

                    node = dag.findChild (self.model, self.getName (localName))
                    if not node:
                        break

                    self.tra [localName] = node.getMatrix (worldSpace = True)
                    self.atra.append (node.getMatrix (worldSpace = True))
                    self.pos [localName] = node.getTranslation (space = "world")
                    self.apos.append (node.getTranslation (space = "world"))

                    i += 1

                if i<self.minmax [name].min:
                    rigging.beam.log ("Minimum of object requiered for " +name + " hasn't been reached!!",rigging.beam.sev_warning)
                    self.valid = False
                    continue

            else:
                node = dag.findChild (self.model, self.getName (name))
                if not node:
                    rigging.beam.log ("Object missing : %s" % (self.getName (name)), rigging.beam.sev_warning)
                    self.valid = False
                    continue

                self.tra [name] = node.getMatrix (worldSpace = True)
                self.atra.append (node.getMatrix (worldSpace = True))
                self.pos [name] = node.getTranslation (space = "world")
                self.apos.append (node.getTranslation (space = "world"))

        for name in self.save_blade:

            node = dag.findChild (self.model, self.getName (name))
            if not node:
                rigging.beam.log ("Object missing : %s" % (self.getName (name)), rigging.beam.sev_warning)
                self.valid = False
                continue

            self.blades [name] = vector.Blade (node.getMatrix (worldSpace = True))

        self.size = self.getSize ()

    def getName(self, name):
        return self.fullName + "_" + name

    def getType(self):
        return self.compType

    def getFullName(self):
        return self.values["comp_name"] + "_" + self.values["comp_side"] + str(self.values["comp_index"])

    def getObjectNames(self):
        names = set()
        names.update(self.save_transform)
        names.update(self.save_primitive)
        names.update(self.save_blade)

        return names

    def getSize(self):
        """Get the size of the component.

        Returns:
            float: the size

        """
        size = .01
        for pos in self.apos:
            d = vector.getDistance(self.pos["root"], pos)
            size = max(size, d)
        size = max(size, .01)

        return size

    def getVersion(self):
        return ".".join([str(i) for i in self.version])

    fullName = property(getFullName)
    type = property(getType)
    objectNames = property(getObjectNames)

class MinMax(object):

    def __init__(self, minimum=1, maximum=-1):
        self.min = minimum
        self.max = maximum



class mainSettingsTab(QtWidgets.QDialog, msui.Ui_Form):


    def __init__(self, parent=None):
        super(mainSettingsTab, self).__init__()
        self.setupUi(self)


class componentMainSettings(QtWidgets.QDialog, guide.helperSlots):
    valueChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(componentMainSettings, self).__init__()
        # the inspectSettings function set the current selection to the
        # component root before open the settings dialog
        self.root = pm.selected()[0]

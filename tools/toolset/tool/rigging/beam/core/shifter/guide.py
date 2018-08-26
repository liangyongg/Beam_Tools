# Built-in
import os
import sys
import imp
import json
import shutil
import getpass
import datetime
import traceback
import subprocess
from functools import partial

# pymel
import pymel.core as pm
from pymel.core import datatypes

# rigging.beam
import rigging.beam
from rigging.beam.core import attribute, dag, vector, skin
for i in [attribute, dag, vector, skin]:
    reload(i)
from rigging.beam.core.general import string
from rigging.beam.ui.Qt import QtWidgets, QtGui, QtCore

from . import guideUI as guui
from . import customStepUI as csui

# pyside
from maya.app.general.mayaMixin import MayaQDockWidget
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

GUIDE_UI_WINDOW_NAME = "guide_UI_window"
GUIDE_DOCK_NAME = "Guide_Components"

TYPE = "rigging.beam_guide_root"

rigging.beam_SHIFTER_CUSTOMSTEP_KEY = "rigging.beam_SHIFTER_CUSTOMSTEP_PATH"


class Main(object):
    """The main guide class"""

    def __init__(self):

        self.paramNames = []
        self.paramDefs = {}
        self.values = {}
        self.valid = True

    def addPropertyParamenters(self, parent):
        for scriptName in self.paramNames:
            paramDef = self.paramDefs[scriptName]
            paramDef.create(parent)

        return parent

    def addParam(self, scriptName, valueType, value,
                 minimum=None, maximum=None, keyable=False,
                 readable=True, storable=True, writable=True,
                 niceName=None, shortName=None):

        paramDef = attribute.ParamDef2(scriptName, valueType, value, niceName,
                                       shortName, minimum, maximum, keyable,
                                       readable, storable, writable)
        self.paramDefs[scriptName] = paramDef
        self.values[scriptName] = value
        self.paramNames.append(scriptName)

        return paramDef

    def addFCurveParam(self, scriptName, keys, interpolation=0):
        paramDef = attribute.FCurveParamDef(scriptName, keys, interpolation)
        self.paramDefs[scriptName] = paramDef
        self.values[scriptName] = None
        self.paramNames.append(scriptName)

        return paramDef

    def addEnumParam(self, scriptName, enum, value=False):
        paramDef = attribute.enumParamDef(scriptName, enum, value)
        self.paramDefs[scriptName] = paramDef
        self.values[scriptName] = value
        self.paramNames.append(scriptName)

        return paramDef

    def setParamDefValue(self, scriptName, value):
        if scriptName not in self.paramDefs.keys():
            rigging.beam.log("Can't find parameter definition for : " + scriptName,
                             rigging.beam.sev_warning)
            return False

        self.paramDefs[scriptName].value = value
        self.values[scriptName] = value

        return True
    def setParamDefValuesFromProperty(self, node):
        """Set the parameter definition values from the attributes of an object

        Arguments:
            node (dagNode): The object with the attributes.
        """

        for scriptName, paramDef in self.paramDefs.items():
            if not pm.attributeQuery(scriptName, node=node, exists=True):
                rigging.beam.log("Can't find parameter '%s' in %s" %(scriptName, node), rigging.beam.sev_warning)
                self.valid = False
            else:
                cnx = pm.listConnections(node + "." + scriptName,destination=False, source=True)
                if cnx:
                    paramDef.value = None
                    self.values[scriptName] = cnx[0]
                else:
                    paramDef.value = pm.getAttr(node + "." + scriptName)
                    self.values[scriptName] = pm.getAttr(node + "." + scriptName)

class Rig(Main):
    """Rig guide class.

    This is the class for complete rig guide definition.

        * It contains the component guide in correct hierarchy order and the
            options to generate the rig.
        * Provide the methods to add more component, import/export guide.

    Attributes:
        paramNames (list): List of parameter name cause it's actually important
            to keep them sorted.
        paramDefs (dict): Dictionary of parameter definition.
        values (dict): Dictionary of options values.
        valid (bool): We will check a few things and make sure the guide we are
            loading is up to date. If parameters or object are missing a
            warning message will be display and the guide should be updated.
        controllers (dict): Dictionary of controllers.
        components (dict): Dictionary of component. Keys are the component
            fullname (ie. 'arm_L0')
        componentsIndex (list): List of component name sorted by order
            creation (hierarchy order)
        parents (list): List of the parent of each component, in same order
            as self.components
    """

    def __init__(self):

        # Parameters names, definition and values.
        self.paramNames = []
        self.paramDefs = {}
        self.values = {}
        self.valid = True

        self.controllers = {}
        self.components = {}  # Keys are the component fullname (ie. 'arm_L0')
        self.componentsIndex = []
        self.parents = []

        self.addParameters ()

    def addParameters (self):
        # --------------------------------------------------
        # Main Tab
        self.pRigName = self.addParam ("rig_name", "string", "rig")
        self.pMode = self.addEnumParam ("mode", ["Final", "WIP"], 0)
        self.pStep = self.addEnumParam ("step",["All Steps", "Objects", "Properties","Operators", "Connect", "Joints", "Finalize"],6)
        self.pIsModel = self.addParam ("ismodel", "bool", True)
        self.pClassicChannelNames = self.addParam ("classicChannelNames","bool",True)
        self.pProxyChannels = self.addParam ("proxyChannels", "bool", False)
        self.pWorldCtl = self.addParam ("worldCtl", "bool", False)

        # --------------------------------------------------
        # skin
        self.pSkin = self.addParam ("importSkin", "bool", False)
        self.pSkinPackPath = self.addParam ("skin", "string", "")

        # --------------------------------------------------
        # Colors

        self.pLColorIndexfk = self.addParam ("L_color_fk", "long", 6, 0, 31)
        self.pLColorIndexik = self.addParam ("L_color_ik", "long", 18, 0, 31)
        self.pRColorIndexfk = self.addParam ("R_color_fk", "long", 23, 0, 31)
        self.pRColorIndexik = self.addParam ("R_color_ik", "long", 14, 0, 31)
        self.pCColorIndexfk = self.addParam ("C_color_fk", "long", 13, 0, 31)
        self.pCColorIndexik = self.addParam ("C_color_ik", "long", 17, 0, 31)

        # --------------------------------------------------
        # Settings
        self.pJointRig = self.addParam ("joint_rig", "bool", True)
        self.pSynoptic = self.addParam ("synoptic", "string", "")

        self.pDoPreCustomStep = self.addParam ("doPreCustomStep", "bool", False)
        self.pDoPostCustomStep = self.addParam ("doPostCustomStep",
                                                "bool", False)
        self.pPreCustomStep = self.addParam ("preCustomStep", "string", "")
        self.pPostCustomStep = self.addParam ("postCustomStep", "string", "")

        # --------------------------------------------------
        # Comments
        self.pComments = self.addParam ("comments", "string", "")
        self.pUser = self.addParam ("user", "string", getpass.getuser ())
        self.pDate = self.addParam ("date", "string", str (datetime.datetime.now ()))
        self.pMayaVersion = self.addParam ("maya_version", "string",str (pm.mel.eval ("getApplicationVersionAsFloat")))
        self.pGearVersion = self.addParam ("gear_version", "string", rigging.beam.getVersion ())

    def setFromSelection(self):
        """Set the guide hierarchy from selection."""
        selection = pm.ls(selection=True)
        if not selection:
            rigging.beam.log("Select one or more guide root or a guide model",rigging.beam.sev_error)
            self.valid = False
            return False

        for node in selection:
            self.setFromHierarchy(node, node.hasAttr("ismodel"))

        return True

    def setFromHierarchy(self, root, branch=True):
        """Set the guide from given hierarchy.

        Arguments:
            root (dagNode): The root of the hierarchy to parse.
            branch (bool): True to parse children components.

        """
        startTime = datetime.datetime.now()
        # Start
        rigging.beam.log("Checking guide")

        # Get the model and the root
        self.model = root.getParent(generations=-1)
        while True:
            if root.hasAttr("comp_type") or self.model == root:
                break
            root = root.getParent()
            rigging.beam.log(root)

        # ---------------------------------------------------
        # First check and set the options
        rigging.beam.log("Get options")
        self.setParamDefValuesFromProperty(self.model)

        # ---------------------------------------------------
        # Get the controllers
        rigging.beam.log("Get controllers")
        self.controllers_org = dag.findChild(self.model, "controllers_org")
        if self.controllers_org:
            for child in self.controllers_org.getChildren():
                self.controllers[child.name().split("|")[-1]] = child

        # ---------------------------------------------------
        # Components
        rigging.beam.log("Get components")
        self.findComponentRecursive(root, branch)
        endTime = datetime.datetime.now()
        finalTime = endTime - startTime
        rigging.beam.log("Find recursive in  [ " + str(finalTime) + " ]")
        # Parenting
        print "rigging.beam.core.shifter.guide.Rig.valid",self.valid
        if self.valid:
            for name in self.componentsIndex:
                rigging.beam.log("Get parenting for: " + name)
                # TODO: In the future should use connections to retrive this
                # data
                # We try the fastes aproach, will fail if is not the top node
                try:
                    # search for his parent
                    compParent = self.components[name].root.getParent()
                    print "rigging.beam.core.shifter.guide.Rig.setFromHierarchy.compParent: ",compParent
                    if compParent and compParent.hasAttr("isBeamGuide"):
                        pName = "_".join(compParent.name().split("_")[:2])
                        print "rigging.beam.core.shifter.guide.Rig.setFromHierarchy.pName: ", pName
                        pLocal = "_".join(compParent.name().split("_")[2:])
                        print "rigging.beam.core.shifter.guide.Rig.setFromHierarchy.pLocal: ", pLocal

                        pComp = self.components[pName]
                        print "rigging.beam.core.shifter.guide.Rig.components: ", self.components
                        print "rigging.beam.core.shifter.guide.Rig.setFromHierarchy.pComp: ", pComp
                        self.components[name].parentComponent = pComp
                        print "rigging.beam.core.shifter.guide.Rig.components[name].parentComponent: ", self.components[name].parentComponent
                        self.components[name].parentLocalName = pLocal
                        print "rigging.beam.core.shifter.guide.Rig.components[name].parentLocalName: ", self.components [name].parentLocalName
                # This will scan the hierachy in reverse. It is much slower
                except KeyError:
                    # search children and set him as parent
                    compParent = self.components[name]
                    # for localName, element in compParent.getObjects(
                    #         self.model, False).items():
                    # NOTE: getObjects3 is an experimental function
                    for localName, element in compParent.getObjects3(self.model).items():
                        for name in self.componentsIndex:
                            compChild = self.components[name]
                            compChild_parent = compChild.root.getParent()
                            if (element is not None and element == compChild_parent):
                                compChild.parentComponent = compParent
                                compChild.parentLocalName = localName

            # More option values
            self.addOptionsValues()

        # End
        if not self.valid:
            rigging.beam.log("The guide doesn't seem to be up to date."
                      "Check logged messages and update the guide.",
                      rigging.beam.sev_warning)

        endTime = datetime.datetime.now()
        finalTime = endTime - startTime
        rigging.beam.log("Guide loaded from hierarchy in  [ " + str(finalTime) + " ]")

    def addOptionsValues(self):
        """Gather or change some options values according to some others.

        Note:
            For the moment only gets the rig size to adapt size of object to
            the scale of the character

        """
        # Get rig size to adapt size of object to the scale of the character
        maximum = 1
        v = datatypes.Vector()
        for comp in self.components.values():
            for pos in comp.apos:
                d = vector.getDistance(v, pos)
                maximum = max(d, maximum)

        self.values["size"] = max(maximum * .05, .1)

    def drawNewComponent(self, parent, comp_type):
        comp_guide = self.getComponentGuide(comp_type)
        print "shifter.guide.Rig.drawNewComponent.comp_guide: ",comp_guide

        if not comp_guide:
            return

        if parent is None:
            self.initialHierarchy()
            parent = self.model
        else:
            parent_root = parent
            while True:
                if parent_root.hasAttr("ismodel"):
                    break

                if parent_root.hasAttr("comp_type"):
                    parent_type = parent_root.attr("comp_type").get()
                    parent_side = parent_root.attr("comp_side").get()
                    parent_uihost = parent_root.attr("ui_host").get()
                    parent_ctlGrp = parent_root.attr("ctlGrp").get()

                    if parent_type in comp_guide.connectors:
                        comp_guide.setParamDefValue("connector", parent_type)

                    comp_guide.setParamDefValue("comp_side", parent_side)
                    comp_guide.setParamDefValue("ui_host", parent_uihost)
                    comp_guide.setParamDefValue("ctlGrp", parent_ctlGrp)

                    break

                parent_root = parent_root.getParent()

        comp_guide.drawFromUI(parent)

    def findComponentRecursive(self, node, branch=True):
        """Finds components by recursive search.

        Arguments:
            node (dagNode): Object frome where start the search.
            branch (bool): If True search recursive all the children.
        """

        if node.hasAttr("comp_type"):
            comp_type = node.getAttr("comp_type")
            comp_guide = self.getComponentGuide(comp_type)

            if comp_guide:
                comp_guide.setFromHierarchy(node)
                rigging.beam.log(comp_guide.fullName + " (" + comp_type + ")")
                if not comp_guide.valid:
                    self.valid = False

                self.componentsIndex.append(comp_guide.fullName)
                self.components[comp_guide.fullName] = comp_guide

        if branch:
            for child in node.getChildren(type="transform"):
                self.findComponentRecursive(child)

    def getComponentGuide(self, comp_type):
        # Check component type
        # Import module and get class
        import rigging.beam.core.shifter as shifter
        module = shifter.importComponentGuide(comp_type)
        #print "guide.Rig.module",module
        ComponentGuide = getattr(module, "Guide")
        #print "guide.Rig.ComponentGuide()",ComponentGuide()
        return ComponentGuide()

    # =====================================================
    # DRAW
    def initialHierarchy(self):
        self.model = pm.group(n="guide", em=True, w=True)

        # Options
        self.options = self.addPropertyParamenters(self.model)

        # the basic org nulls (Maya groups)
        self.controllers_org = pm.group(n="controllers_org",em=True,p=self.model)
        self.controllers_org.attr('visibility').set(0)


class HelperSlots(object):

    def updateHostUI(self, lEdit, targetAttr):
        oType = pm.nodetypes.Transform

        oSel = pm.selected()
        if oSel:
            if isinstance(oSel[0], oType) and oSel[0].hasAttr("isGearGuide"):
                lEdit.setText(oSel[0].name())
                self.root.attr(targetAttr).set(lEdit.text())
            else:
                pm.displayWarning("The selected element is not a "
                                  "valid object or not from a guide")
        else:
            pm.displayWarning("Please select first the object.")

class GuideSettingsTab(QtWidgets.QDialog, guui.Ui_Form):

    def __init__(self, parent=None):
        super(guideSettingsTab, self).__init__(parent)
        self.setupUi(self)


class CustomStepTab(QtWidgets.QDialog, csui.Ui_Form):

    def __init__(self, parent=None):
        super(customStepTab, self).__init__(parent)
        self.setupUi(self)


class GuideSettings(MayaQWidgetDockableMixin, QtWidgets.QDialog, HelperSlots):
    # valueChanged = QtCore.Signal(int)
    greenBrush = QtGui.QBrush()
    greenBrush.setColor('#179e83')
    redBrush = QtGui.QBrush()
    redBrush.setColor('#9b2d22')
    whiteBrush = QtGui.QBrush()
    whiteBrush.setColor('#ffffff')
    whiteDownBrush = QtGui.QBrush()
    whiteDownBrush.setColor('#E2E2E2')
    orangeBrush = QtGui.QBrush()
    orangeBrush.setColor('#e67e22')

    def __init__(self, parent=None):
        pass

MainGuide = Main
RigGuide = Rig
helperSlots = HelperSlots
guideSettingsTab = GuideSettingsTab
customStepTab = CustomStepTab
guideSettings = GuideSettings
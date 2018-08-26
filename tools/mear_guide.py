import rigging.beam.ui.beam_window
reload(rigging.beam.ui.beam_window)
import pymel.core as pm
#win = rigging.beam.ui.beam_window.BeamUI()
#win.show()

from rigging.beam.core import shifter
from rigging.beam.core import transform,icon

guide = shifter.guide.Rig()
#__init__()
#guide.paramNames
#guide.paramDefs
#guide.values
#guide.valid
#guide.controllers
#guide.components
#guide.componentsIndex
#guide.parents
#guide.addParameters()
    #guide.addParam()
    #guide.addEnumParam()
com_guide = guide.getComponentGuide("arm_01")
#static#
#com_guide.compType
#com_guide.compName
#com_guide.compSide
#com_guide.compIndex
#com_guide.description
#com_guide.connectors
#com_guide.compatible
#com_guide.ctl_grp
#__init__()
#com_guide.paramNames
#com_guide.paramDefs
#com_guide.values
#com_guide.root
#com_guide.id
#com_guide.parentComponent
#com_guide.parentLocalName
#com_guide.tra
#com_guide.atra
#com_guide.pos
#com_guide.apos
#com_guide.prim
#com_guide.blades
#com_guide.size
#com_guide.save_transform
#com_guide.save_primitive
#com_guide.save_blade
#com_guide.minmax
#com_guide.postInit()
#com_guide.initialHierarchy()
    #com_guide.addParam()
#com_guide.addParameters()


model = pm.group(n="guide", em=True, w=True)
for scriptName in guide.paramNames:
	paramDef = guide.paramDefs[scriptName]
	paramDef.create(model)
controllers_org = pm.group(n="controllers_org",em=True,p=model)
controllers_org.attr('visibility').set(0)

model = model.getParent(generations=-1)

from rigging.beam.core import dag
fullname = com_guide.values["comp_name"] + "_" + com_guide.values["comp_side"] + str(com_guide.values["comp_index"]+1)
dag.findChild(model,fullname+"root")

com_guide.tra["root"] = transform.getTransformFromPos(pm.datatypes.Vector(0,0,0))
com_guide.root = icon.guideRootIcon(model,fullname+"root",color=13,m=com_guide.tra["root"])

for scriptName in com_guide.paramNames:
	paramDef = com_guide.paramDefs[scriptName]
	paramDef.create(com_guide.root)

vTemp = transform.getOffsetPosition (com_guide.root, [3, 0, -.01])
if "elbow" not in com_guide.tra.keys():
    com_guide.tra["elbow"] = transform.getTransformFromPos(vTemp)
if "elbow" in com_guide.prim.keys():
    loc = com_guide.prim["elbow"].create(model, self.getName(name), self.tra[name], color=17)
elbow=icon.guideLocatorIcon(com_guide.root,fullname+"elbow",color=17,m=com_guide.tra["elbow"])

vTemp = transform.getOffsetPosition (com_guide.root, [6, 0, 0])
if "wrist" not in com_guide.tra.keys():
    com_guide.tra["wrist"] = transform.getTransformFromPos(vTemp)
wrist=icon.guideLocatorIcon(elbow,fullname+"wrist",color=17,m=com_guide.tra["wrist"])

vTemp = transform.getOffsetPosition (com_guide.root, [7, 0, 0])
if "eff" not in com_guide.tra.keys():
    com_guide.tra["eff"] = transform.getTransformFromPos(vTemp)
eff=icon.guideLocatorIcon(wrist,fullname+"eff",color=17,m=com_guide.tra["eff"])


dispcrv = icon.connection_display_curve(fullname+"crv",[com_guide.root, elbow, wrist, eff],1)

transform.resetTransform(com_guide.root, r=False, s=False)

#buildFromSelection
rg = shifter.Rig()
#__init__()
    guide = shifter.guide.Rig()
    #__init__()
    #guide.paramNames
    #guide.paramDefs
    #guide.values
    #guide.valid    
    #guide.controllers
    #guide.components
    #guide.componentsIndex
    #guide.parents
    #guide.addParameters()
        #guide.addParam()
        #guide.addEnumParam()
#rg.groups = {}
#rg.subGroups = {}
#rg.components = {}
#rg.componentsIndex = []
#rg.customStepDic = {}

com_guide = guide.getCompo
import datetime
starttime=datetime.datetime.now()
selection=pm.ls(sl=1)[0]
selection.hasAttr("ismodel")
selection.attr("doPreCustomStep").get()
#guide.setFromSelection()
model=selection.getParent(generations=-1)
root=selection
while True:
    if root.hasAttr("comp_type") or model == root:
        break
    root=root.getParent()
for scriptName, paramDef in guide.paramDefs.items():
	if not pm.attributeQuery(scriptName, node=model, exists=True):
		rigging.beam.log("Can't find parameter '%s' in %s" %(scriptName, model), rigging.beam.sev_warning)
		self.valid = False
	else:
		cnx = pm.listConnections(model + "." + scriptName,destination=False, source=True)
		if cnx:
			paramDef.value = None
			guide.values[scriptName] = cnx[0]
		else:
			paramDef.value = pm.getAttr(model + "." + scriptName)
			guide.values[scriptName] = pm.getAttr(model + "." + scriptName)

guide.controllers_org = dag.findChild(model, "controllers_org")
if guide.controllers_org:
	for child in guide.controllers_org.getChildren():
		guide.controllers[child.name().split("|")[-1]] = child

if selection.hasAttr("comp_type"):
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
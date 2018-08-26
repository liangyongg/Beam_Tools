from rigging.beam.core import shifter
from rigging.beam.core import dag,vector,primitive,attribute,transform,icon,fcurve,node
from rigging.beam.core.general import string
from pymel.core import datatypes
import pymel.core as pm
from pymel import versions
import rigging.beam
import getpass
import datetime
rg = shifter.Rig()
#__init__()
#rg.guide=shifter.guide.Rig()
    # Parameters names, definition and values.
    #rg.guide.paramNames = []
    #rg.guide.paramDefs = {}
    #rg.guide.values = {}
    #rg.guide.valid = True
    #rg.guide.controllers = {}
    #rg.guide.components = {}  # Keys are the component fullname (ie. 'arm_L0')
    #rg.guide.componentsIndex = []
    #rg.guide.parents = []
    #rg.guide.addParameters ()
#rg.groups = {}
#rg.subGroups = {}
#rg.components = {}
#rg.componentsIndex = []
#rg.customStepDic = {}

#===buildFromSelection()===
rg.stopBuild = False
selection = pm.ls(selection=True)
ismodel = False
if selection[0].hasAttr("ismodel"):
    rg.preCustomStep(selection)
    ismodel = True
if not rg.stopBuild:
    #===rg.guide.setFromSelection()===
    selection = pm.ls(selection=True)
    for node in selection:
        #===rg.guide.setFromHierarchy(node, node.hasAttr("ismodel"))===
        rg.guide.model = node.getParent(generations=-1)
        print "rg.guide.model:",rg.guide.model
        while True:
            if node.hasAttr("comp_type") or rg.guide.model == node:
                break
            node = node.getParent()
        #===rg.guide.setParamDefValuesFromProperty(rg.guide.model)===
        for scriptName, paramDef in rg.guide.paramDefs.items():
            if not pm.attributeQuery(scriptName, node=rg.guide.model, exists=True):
                print node+"."+scriptName
                rg.guide.valid = False
            else:
                cnx = pm.listConnections(rg.guide.model + "." + scriptName,destination=False, source=True)
                if cnx:
                    paramDef.value = None
                    rg.guide.values[scriptName] = cnx[0]
                else:
                    paramDef.value = pm.getAttr(rg.guide.model + "." + scriptName)
                    rg.guide.values[scriptName] = pm.getAttr(rg.guide.model + "." + scriptName)

        rg.guide.controllers_org = shifter.dag.findChild(rg.guide.model, "controllers_org")
        if rg.guide.controllers_org:
            for child in rg.guide.controllers_org.getChildren():
                rg.guide.controllers[child.name().split("|")[-1]] = child
        
        #===rg.guide.findComponentRecursive(node, branch)===
        if node.hasAttr("comp_type"):
            comp_type = node.getAttr("comp_type")
            #===rg.guide.getComponentGuide(comp_type)===
                #shifter.importComponentGuide(comp_type)
            comp_guide = rg.guide.getComponentGuide(comp_type)
            #static
            #comp_guide.compType
            #comp_guide.compName
            #comp_guide.compSide = "C"
            #comp_guide.compIndex = 0
            #comp_guide.description = ""
            #comp_guide.connectors = []
            #comp_guide.compatible = []
            #comp_guide.ctl_grp = ""
            
            #__init__()
            	#comp_guide.paramNames = []
            #comp_guide.paramDefs = {}
            #comp_guide.values = {}
            #comp_guide.valid = True
            #comp_guide.root = None
            #comp_guide.id = None
            #comp_guide.parentComponent = None
            #comp_guide.parentLocalName = None
            #comp_guide.tra = {}  # dictionary of global transform
            #comp_guide.atra = []  # list of global transform
            #comp_guide.pos = {}  # dictionary of global postion
            #comp_guide.apos = []  # list of global position
            #comp_guide.prim = {}  # dictionary of primitive
            #comp_guide.blades = {}
            #comp_guide.size = .1
            #comp_guide.save_transform = []
            #comp_guide.save_primitive = []
            #comp_guide.save_blade = []
            #comp_guide.minmax = {}
            #comp_guide.postInit()
            #comp_guide.initialHierarchy()
            #comp_guide.addParameters()
        
            if comp_guide:
                #===comp_guide.setFromHierarchy(node)===
                comp_guide.root = node
                comp_guide.model = comp_guide.root.getParent (generations = -1)
                if not comp_guide.root.hasAttr ("comp_type"):
                    comp_guide.valid = False
                #===comp_guide.setParamDefValuesFromProperty(comp_guide.root)===
                for scriptName, paramDef in comp_guide.paramDefs.items():
                    if not pm.attributeQuery(scriptName, node=comp_guide.root, exists=True):
                        print comp_guide.root+"."+scriptName
                        comp_guide.valid = False
                    else:
                        cnx = pm.listConnections(comp_guide.root + "." + scriptName,destination=False, source=True)
                        if cnx:
                            paramDef.value = None
                            comp_guide.values[scriptName] = cnx[0]
                        else:
                            paramDef.value = pm.getAttr(comp_guide.root + "." + scriptName)
                            comp_guide.values[scriptName] = pm.getAttr(comp_guide.root + "." + scriptName)
                for name in comp_guide.save_transform:
                    if "#" in name:
                        i = 0
                        while not comp_guide.minmax [name].max>0 or i< comp_guide.minmax [name].max:
                            localName = string.replaceSharpWithPadding (name, i)
                            
                            node = dag.findChild (comp_guide.model, comp_guide.getName (localName))
                            if not node:
                                break
    
                            comp_guide.tra [localName] = node.getMatrix (worldSpace = True)
                            comp_guide.atra.append (node.getMatrix (worldSpace = True))
                            comp_guide.pos [localName] = node.getTranslation (space = "world")
                            comp_guide.apos.append (node.getTranslation (space = "world"))
                            
                            i += 1
    
                        if i<comp_guide.minmax [name].min:
                            comp_guide.valid = False
                            continue
                    else:
                        node = shifter.dag.findChild (comp_guide.model, comp_guide.getName (name))
                        if not node:
                            comp_guide.valid = False
                            continue
                        comp_guide.tra [name] = node.getMatrix (worldSpace = True)
                        comp_guide.atra.append (node.getMatrix (worldSpace = True))
                        comp_guide.pos [name] = node.getTranslation (space = "world")
                        comp_guide.apos.append (node.getTranslation (space = "world"))
    
                for name in comp_guide.save_blade:
                
                    node = dag.findChild (comp_guide.model, comp_guide.getName (name))
                    if not node:
                        comp_guide.valid = False
                        continue
                
                    comp_guide.blades [name] = vector.Blade (node.getMatrix (worldSpace = True))
                #===comp_guide.getSize ()===
                size = .01
                for pos in comp_guide.apos:
                    d = vector.getDistance(comp_guide.pos["root"], pos)
                    size = max(size, d)
                    size = max(size, .01)
    
                comp_guide.size = size
    
                if not comp_guide.valid:
                    comp_guide.valid = False
                
                rg.guide.componentsIndex.append(comp_guide.fullName)
                rg.guide.components[comp_guide.fullName] = comp_guide
        #=======================================================================
        if rg.guide.valid:
            for name in rg.guide.componentsIndex:
                try:
                    compParent = rg.guide.components[name].root.getParent()
                    if compParent and compParent.hasAttr("isBeamGuide"):
                        pName = "_".join(compParent.name().split("_")[:2])
                        pLocal = "_".join(compParent.name().split("_")[2:])
                        
                        pComp = rg.guide.components[pName]
                        rg.guide.components[name].parentComponent = pComp
                        rg.guide.components[name].parentLocalName = pLocal
                except KeyError:
                    compParent = rg.guide.components[name]
                    for localName, element in compParent.getObjects3(rg.guide.model).items():
                        for name in rg.guide.componentsIndex:
                            compChild = rg.guide.components[name]
                            compChild_parent = compChild.root.getParent()
                            if (element is not None and element == compChild_parent):
                                compChild.parentComponent = compParent
                                compChild.parentLocalName = localName
            #======rg.guide.addOptionsValues()======
            maximum = 1
            v = datatypes.Vector()
            for comp in rg.guide.components.values():
                for pos in comp.apos:
                    d = vector.getDistance(v, pos)
                    maximum = max(d, maximum)
                    
            rg.guide.values["size"] = max(maximum * .05, .1)
            
    if not rg.guide.valid:
        print "break"
    #===build()====
    rg.options = rg.guide.values
    rg.guides = rg.guide.components
    rg.customStepDic["beamRun"] = rg
        #rg.initialHierarchy()
    rg.model = primitive.addTransformFromPos(None, rg.options["rig_name"])
    attribute.lockAttribute(rg.model)
    
    # --------------------------------------------------
    # INFOS
    rg.isRig_att = attribute.addAttribute(rg.model, "is_rig", "bool", True)
    rg.rigName_att = attribute.addAttribute(rg.model, "rig_name", "string", rg.options["rig_name"])
    rg.user_att = attribute.addAttribute(rg.model, "user", "string", getpass.getuser())
    rg.isWip_att = attribute.addAttribute(rg.model, "wip", "bool", rg.options["mode"] != 0)
    rg.date_att = attribute.addAttribute(rg.model, "date", "string", str(datetime.datetime.now()))
    rg.mayaVersion_att = attribute.addAttribute(rg.model, "maya_version", "string",str(pm.mel.eval("getApplicationVersionAsFloat")))
    rg.gearVersion_att = attribute.addAttribute(rg.model, "gear_version", "string", rigging.beam.getVersion())
    rg.synoptic_att = attribute.addAttribute(rg.model, "synoptic", "string", str(rg.options["synoptic"]))
    rg.comments_att = attribute.addAttribute(rg.model, "comments", "string", str(rg.options["comments"]))
    rg.ctlVis_att = attribute.addAttribute(rg.model, "ctl_vis", "bool", True)
    if versions.current() >= 201650:
        rg.ctlVisPlayback_att = attribute.addAttribute(rg.model, "ctl_vis_on_playback", "bool", True)
    rg.jntVis_att = attribute.addAttribute(rg.model, "jnt_vis", "bool", True)
    
    rg.qsA_att = attribute.addAttribute(rg.model, "quickselA", "string", "")
    rg.qsB_att = attribute.addAttribute(rg.model, "quickselB", "string", "")
    rg.qsC_att = attribute.addAttribute(rg.model, "quickselC", "string", "")
    rg.qsD_att = attribute.addAttribute(rg.model, "quickselD", "string", "")
    rg.qsE_att = attribute.addAttribute(rg.model, "quickselE", "string", "")
    rg.qsF_att = attribute.addAttribute(rg.model, "quickselF", "string", "")
    
    rg.rigGroups = rg.model.addAttr("rigGroups", at='message', m=1)
    rg.rigPoses = rg.model.addAttr("rigPoses", at='message', m=1)
    rg.rigCtlTags = rg.model.addAttr("rigCtlTags", at='message', m=1)

    if rg.options["worldCtl"]:
        rg.global_ctl = rg.addCtl(rg.model,"world_ctl",datatypes.Matrix(),rg.options["C_color_fk"],"circle", w=10)
    else:
        rg.global_ctl = rg.addCtl(rg.model,"global_C0_ctl",datatypes.Matrix(),rg.options["C_color_fk"],"crossarrow",w=10)
    attribute.setRotOrder(rg.global_ctl, "ZXY")

    pm.connectAttr(rg.ctlVis_att, rg.global_ctl.attr("visibility"))
    if versions.current() >= 201650:
        pm.connectAttr(rg.ctlVisPlayback_att,rg.global_ctl.attr("hideOnPlayback"))
    attribute.lockAttribute(rg.global_ctl, ['v'])

    rg.setupWS = primitive.addTransformFromPos(rg.model, "setup")
    attribute.lockAttribute(rg.setupWS)

    if rg.options["joint_rig"]:
        rg.jnt_org = primitive.addTransformFromPos(rg.model, "jnt_org")
        pm.connectAttr(rg.jntVis_att, rg.jnt_org.attr("visibility"))

    #======rg.processComponents======
    rg.components_infos = {}

    for comp in rg.guide.componentsIndex:
        guide_ = rg.guides[comp]
        
        module = shifter.importComponent(guide_.type)
        Component = getattr(module, "Component")
        
        comp = Component(rg, guide_)
        #static================
        #comp.steps = ["Objects", "Properties", "Operators","Connect", "Joints", "Finalize"]
        #comp.local_params = ("tx", "ty", "tz", "rx", "ry", "rz", "ro", "sx", "sy", "sz")
        #comp.t_params = ("tx", "ty", "tz")
        #comp.r_params = ("rx", "ry", "rz", "ro")
        #comp.s_params = ("sx", "sy", "sz")
        #comp.tr_params = ("tx", "ty", "tz", "rx", "ry", "rz", "ro")
        #comp.rs_params = ("rx", "ry", "rz", "ro", "sx", "sy", "sz")
        #comp.x_axis = datatypes.Vector(1, 0, 0)
        #comp.y_axis = datatypes.Vector(0, 1, 0)
        #comp.z_axis = datatypes.Vector(0, 0, 1)
        
        #__init__()==================
        #comp.rig = rig
        #comp.guide = guide
        #comp.options = comp.rig.options
        #comp.model = comp.rig.model
        #comp.settings = comp.guide.values
        #comp.setupWS = comp.rig.setupWS
        #comp.name = comp.settings["comp_name"]
        #comp.side = comp.settings["comp_side"]
        #comp.index = comp.settings["comp_index"]
        #comp.size = comp.guide.size
        #comp.color_fk = comp.options[comp.side + "_color_fk"]
        #comp.color_ik = comp.options[comp.side + "_color_ik"]
        #comp.negate = comp.side == "R"
        #if comp.negate:
        #    comp.n_sign = "-"
        #    comp.n_factor = -1
        #else:
        #    comp.n_sign = ""
        #    comp.n_factor = 1
        #comp.groups = {}  # Dictionary of groups
        #comp.subGroups = {}  # Dictionary of subGroups
        #comp.controlers = []  # List of all the controllers of the component
        #comp.connections = {}
        #comp.connections["standard"] = comp.connect_standard
        #comp.relatives = {}
        #comp.jointRelatives = {}  # joint relatives mapping for auto connection
        #comp.controlRelatives = {}
        #comp.aliasRelatives = {}  # alias names for pretty names on combo box
        #comp.jnt_pos = []
        #comp.jointList = []
        #comp.transform2Lock = []
        #comp.stepMethods = [eval("comp.step_0%s" % i) for i in range(len(comp.steps))]

        if comp.fullName not in rg.componentsIndex:
            rg.components[comp.fullName] = comp
            rg.componentsIndex.append(comp.fullName)
            
            rg.components_infos[comp.fullName] = [guide_.compType, guide_.getVersion(), guide_.author]
            
    rg.steps = shifter.beam_components.Main.steps
    for i, name in enumerate(rg.steps):
        for compName in rg.componentsIndex:
            comp = rg.components[compName]
            #===comp.stepMethods[i]()===
                #===comp.preScript()===
                #===comp.initialHierarchy()===
            comp.root=primitive.addTransformFromPos(comp.model, comp.getName("root"), comp.guide.pos["root"])
            comp.addToGroup(comp.root, names=["componentsRoots"])
            attribute.addAttribute(comp.root, "componentType","string", comp.guide.compType)
            attribute.addAttribute(comp.root, "componentName","string", comp.guide.compName)
            attribute.addAttribute(comp.root, "componentVersion","string", str(comp.guide.version)[1:-1])
            attribute.addAttribute(comp.root, "componentAuthor","string", comp.guide.author)
            attribute.addAttribute(comp.root, "componentURL","string", comp.guide.url)
            attribute.addAttribute(comp.root, "componentEmail","string", comp.guide.email)
            if comp.options["joint_rig"]:
                comp.component_jnt_org = primitive.addTransform(comp.rig.jnt_org, comp.getName("jnt_org"))
                comp.active_jnt = comp.component_jnt_org
                comp.parent_relative_jnt = comp.component_jnt_org
            #===initControlTag()===
            comp.parentCtlTag = None
            if versions.current() >= 201650:
                parent_name = "none"
                if comp.guide.parentComponent is not None:
                    parent_name = comp.guide.parentComponent.getName(comp.guide.parentLocalName)
                    comp.parentCtlTag = comp.rig.findControlRelative(parent_name)
            #===addObjects()===
            comp.WIP = comp.options["mode"]
            comp.normal = comp.getNormalFromPos(comp.guide.apos)
            comp.binormal = comp.getBiNormalFromPos(comp.guide.apos)
            comp.length0 = vector.getDistance(comp.guide.apos[0],comp.guide.apos[1])
            comp.length1 = vector.getDistance(comp.guide.apos[1],comp.guide.apos[2])
            comp.length2 = vector.getDistance(comp.guide.apos[2],comp.guide.apos[3])

            comp.armChainUpvRef = primitive.add2DChain(comp.root,
                                                       comp.getName("armUpvRef%s_jnt"),
                                                       [comp.guide.apos[0],
                                                       comp.guide.apos[2]],
                                                       comp.normal,
                                                       False,
                                                       comp.WIP)
            negateOri = comp.armChainUpvRef[1].getAttr("jointOrientZ") * -1
            comp.armChainUpvRef[1].setAttr("jointOrientZ", negateOri)
            # FK Controlers -----------------------------------
            t = transform.getTransformLookingAt(comp.guide.apos[0],
                                                comp.guide.apos[1],
                                                comp.normal, "xz",
                                                comp.negate)
            comp.fk0_npo = primitive.addTransform(comp.root,comp.getName("fk0_npo"),t)
            vec_po = datatypes.Vector(.5 * comp.length0 * comp.n_factor, 0, 0)
            comp.fk0_ctl = comp.addCtl(comp.fk0_npo,
                                       "fk0_ctl",
                                       t,
                                       comp.color_fk,
                                       "cube",
                                       w=comp.length0,
                                       h=comp.size * .1,
                                       d=comp.size * .1,
                                       po=vec_po,
                                       tp=comp.parentCtlTag)
            attribute.setKeyableAttributes(comp.fk0_ctl,["tx", "ty", "tz", "ro", "rx", "ry", "rz", "sx"])
            t = transform.getTransformLookingAt(comp.guide.apos[1],
                                                comp.guide.apos[2],
                                                comp.normal,
                                                "xz",
                                                comp.negate)
            comp.fk1_npo = primitive.addTransform(comp.fk0_ctl,comp.getName("fk1_npo"),t)
            vec_po = datatypes.Vector(.5 * comp.length1 * comp.n_factor, 0, 0)
            comp.fk1_ctl = comp.addCtl(comp.fk1_npo,
                                       "fk1_ctl",
                                       t,
                                       comp.color_fk,
                                       "cube",
                                       w=comp.length1,
                                       h=comp.size * .1,
                                       d=comp.size * .1,
                                       po=vec_po,
                                       tp=comp.fk0_ctl)
            attribute.setKeyableAttributes(comp.fk1_ctl,["tx", "ty", "tz", "ro", "rx", "ry", "rz", "sx"])
            t = transform.getTransformLookingAt(comp.guide.apos[2],
                                                comp.guide.apos[3],
                                                comp.normal,
                                                "xz",
                                                comp.negate)

            comp.fk2_npo = primitive.addTransform(comp.fk1_ctl,comp.getName("fk2_npo"),t)
    
            vec_po = datatypes.Vector(.5 * comp.length2 * comp.n_factor, 0, 0)
            comp.fk2_ctl = comp.addCtl(comp.fk2_npo,
                                       "fk2_ctl",
                                       t,
                                       comp.color_fk,
                                       "cube",
                                       w=comp.length2,
                                       h=comp.size * .1,
                                       d=comp.size * .1,
                                       po=vec_po,
                                       tp=comp.fk1_ctl)
            attribute.setKeyableAttributes(comp.fk2_ctl)
            
            comp.fk_ctl = [comp.fk0_ctl, comp.fk1_ctl, comp.fk2_ctl]
            
            for x in comp.fk_ctl:
                attribute.setInvertMirror(x, ["tx", "ty", "tz"])
            
            # IK upv ---------------------------------
            v = comp.guide.apos[2] - comp.guide.apos[0]
            v = comp.normal ^ v
            v.normalize()
            v *= comp.size * .5
            v += comp.guide.apos[1]
            comp.upv_cns = primitive.addTransformFromPos(comp.root,comp.getName("upv_cns"),v)
            comp.upv_ctl = comp.addCtl(comp.upv_cns,
                                       "upv_ctl",
                                       transform.getTransform(comp.upv_cns),
                                       comp.color_ik,
                                       "diamond",
                                       w=comp.size * .12,
                                       tp=comp.parentCtlTag)
            if comp.settings["mirrorMid"]:
                if comp.negate:
                    comp.upv_cns.rz.set(180)
                    comp.upv_cns.sy.set(-1)
            else:
                attribute.setInvertMirror(comp.upv_ctl, ["tx"])
            attribute.setKeyableAttributes(comp.upv_ctl, comp.t_params)
            # IK Controlers -----------------------------------
            comp.ik_cns = primitive.addTransformFromPos(comp.root, comp.getName("ik_cns"), comp.guide.pos["wrist"])

            t = transform.getTransformFromPos(comp.guide.pos["wrist"])
            comp.ikcns_ctl = comp.addCtl(comp.ik_cns,
                                         "ikcns_ctl",
                                         t,
                                         comp.color_ik,
                                         "null",
                                         w=comp.size * .12,
                                         tp=comp.parentCtlTag)

            attribute.setInvertMirror(comp.ikcns_ctl, ["tx", "ty", "tz"])

            if comp.negate:
                m = transform.getTransformLookingAt(comp.guide.pos["wrist"],
                                                    comp.guide.pos["eff"],
                                                    comp.normal,
                                                    "x-y",
                                                    True)
            else:
                m = transform.getTransformLookingAt(comp.guide.pos["wrist"],
                                                    comp.guide.pos["eff"],
                                                    comp.normal,
                                                    "xy",
                                                    False)

            comp.ik_ctl = comp.addCtl(comp.ikcns_ctl,
                                      "ik_ctl",
                                      m,
                                      comp.color_ik,
                                      "cube",
                                      w=comp.size * .12,
                                      h=comp.size * .12,
                                      d=comp.size * .12,
                                      tp=comp.upv_ctl)

            if comp.settings["mirrorIK"]:
                if comp.negate:
                    comp.ik_cns.sx.set(-1)
                    comp.ik_ctl.rz.set(comp.ik_ctl.rz.get() * -1)
            else:
                attribute.setInvertMirror(comp.ik_ctl, ["tx", "ry", "rz"])
            attribute.setKeyableAttributes(comp.ik_ctl)
            comp.ik_ctl_ref = primitive.addTransform(comp.ik_ctl,
                                                     comp.getName("ikCtl_ref"),
                                                     m)
            # IK rotation controls
            if comp.settings["ikTR"]:
                comp.ikRot_npo = primitive.addTransform(comp.root,comp.getName("ikRot_npo"),m)
                comp.ikRot_cns = primitive.addTransform(comp.ikRot_npo,comp.getName("ikRot_cns"),m)
                comp.ikRot_ctl = comp.addCtl(comp.ikRot_cns,"ikRot_ctl",m,comp.color_ik,"sphere",w=comp.size * .12,tp=comp.ik_ctl)
                attribute.setKeyableAttributes(comp.ikRot_ctl, comp.r_params)
            # References --------------------------------------
            # Calculate  again the transfor for the IK ref. This way align with FK
            trnIK_ref = transform.getTransformLookingAt(comp.guide.pos["wrist"],
                                                        comp.guide.pos["eff"],
                                                        comp.normal,
                                                        "xz",
                                                        comp.negate)
            comp.ik_ref = primitive.addTransform(comp.ik_ctl_ref,
                                                 comp.getName("ik_ref"),
                                                 trnIK_ref)
            comp.fk_ref = primitive.addTransform(comp.fk_ctl[2],
                                                 comp.getName("fk_ref"),
                                                 trnIK_ref)

            # Chain --------------------------------------------
            # The outputs of the ikfk2bone solver
            comp.bone0 = primitive.addLocator(comp.root,
                                              comp.getName("0_bone"),
                                              transform.getTransform(comp.fk_ctl[0]))
            comp.bone0_shp = comp.bone0.getShape()
            comp.bone0_shp.setAttr("localPositionX", comp.n_factor * .5)
            comp.bone0_shp.setAttr("localScale", .5, 0, 0)
            comp.bone0.setAttr("sx", comp.length0)
            comp.bone0.setAttr("visibility", False)

            comp.bone1 = primitive.addLocator(comp.root,
                                              comp.getName("1_bone"),
                                              transform.getTransform(comp.fk_ctl[1]))
            comp.bone1_shp = comp.bone1.getShape()
            comp.bone1_shp.setAttr("localPositionX", comp.n_factor * .5)
            comp.bone1_shp.setAttr("localScale", .5, 0, 0)
            comp.bone1.setAttr("sx", comp.length1)
            comp.bone1.setAttr("visibility", False)
            
            comp.ctrn_loc = primitive.addTransformFromPos(comp.root,
                                                          comp.getName("ctrn_loc"),
                                                          comp.guide.apos[1])
            comp.eff_loc = primitive.addTransformFromPos(comp.root,
                                                         comp.getName("eff_loc"),
                                                         comp.guide.apos[2])
            # Mid Controler ------------------------------------
            t = transform.getTransform(comp.ctrn_loc)
            comp.mid_cns = primitive.addTransform(comp.ctrn_loc,comp.getName("mid_cns"),t)

            comp.mid_ctl = comp.addCtl(comp.mid_cns,
                                       "mid_ctl",
                                       t,
                                       comp.color_ik,
                                       "sphere",
                                       w=comp.size * .2,
                                       tp=comp.parentCtlTag)

            attribute.setKeyableAttributes(comp.mid_ctl,
                                           params=["tx", "ty", "tz",
                                                   "ro", "rx", "ry", "rz",
                                                   "sx"])
            if comp.settings["mirrorMid"]:
                if comp.negate:
                    comp.mid_cns.rz.set(180)
                    comp.mid_cns.sz.set(-1)
                comp.mid_ctl_twst_npo = primitive.addTransform(
                    comp.mid_ctl,
                    comp.getName("mid_twst_npo"),
                    t)
                comp.mid_ctl_twst_ref = primitive.addTransform(
                    comp.mid_ctl_twst_npo,
                    comp.getName("mid_twst_ref"),
                    t)
            else:
                comp.mid_ctl_twst_ref = comp.mid_ctl
                attribute.setInvertMirror(comp.mid_ctl, ["tx", "ty", "tz"])

            # Roll join ref
            comp.rollRef = primitive.add2DChain(comp.root,
                                                comp.getName("rollChain"),
                                                comp.guide.apos[:2],
                                                comp.normal,
                                                comp.negate)
            for x in comp.rollRef:
                x.setAttr("visibility", False)

            comp.tws0_loc = primitive.addTransform(comp.rollRef[0],
                                                   comp.getName("tws0_loc"),
                                                   transform.getTransform(comp.fk_ctl[0]))
            comp.tws0_rot = primitive.addTransform(comp.tws0_loc,
                                                   comp.getName("tws0_rot"),
                                                   transform.getTransform(comp.fk_ctl[0]))

            comp.tws1_npo = primitive.addTransform(comp.ctrn_loc,
                                                   comp.getName("tws1_npo"),
                                                   transform.getTransform(comp.ctrn_loc))
            comp.tws1_loc = primitive.addTransform(comp.tws1_npo,
                                                   comp.getName("tws1_loc"),
                                                   transform.getTransform(comp.ctrn_loc))
            comp.tws1_rot = primitive.addTransform(comp.tws1_loc,
                                                   comp.getName("tws1_rot"),
                                                   transform.getTransform(comp.ctrn_loc))

            comp.tws2_npo = primitive.addTransform(comp.root,
                                                   comp.getName("tws2_npo"),
                                                   transform.getTransform(comp.fk_ctl[2]))
            comp.tws2_loc = primitive.addTransform(comp.tws2_npo,
                                                   comp.getName("tws2_loc"),
                                                   transform.getTransform(comp.fk_ctl[2]))
            comp.tws2_rot = primitive.addTransform(comp.tws2_loc,
                                                   comp.getName("tws2_rot"),
                                                   transform.getTransform(comp.fk_ctl[2]))

            # Divisions ----------------------------------------
            # We have at least one division at the start, the end and one for the
            # elbow. + 2 for elbow angle control
            comp.divisions = comp.settings["div0"] + comp.settings["div1"] + 3 + 2

            comp.div_cns = []

            if comp.settings["extraTweak"]:
                tagP = comp.parentCtlTag
                comp.tweak_ctl = []

            for i in range(comp.divisions):
                div_cns = primitive.addTransform(comp.root,comp.getName("div%s_loc" % i))
                comp.div_cns.append(div_cns)
                if comp.settings["extraTweak"]:
                    t = transform.getTransform(div_cns)
                    tweak_ctl = comp.addCtl(div_cns,
                                            "tweak%s_ctl" % i,
                                            t,
                                            comp.color_fk,
                                            "square",
                                            w=comp.size * .15,
                                            d=comp.size * .15,
                                            ro=datatypes.Vector([0, 0, 1.5708]),
                                            tp=tagP)
                    attribute.setKeyableAttributes(tweak_ctl)
                    tagP = tweak_ctl
                    comp.tweak_ctl.append(tweak_ctl)
                    comp.jnt_pos.append([tweak_ctl, i, None, False])
                else:
                    comp.jnt_pos.append([div_cns, i])

            # End reference ------------------------------------
            # To help the deformation on the wrist
            comp.jnt_pos.append([comp.eff_loc, 'end'])
            # match IK FK references
            comp.match_fk0_off = primitive.addTransform(comp.root,
                                                        comp.getName("matchFk0_npo"),
                                                        transform.getTransform(comp.fk_ctl[1]))
            comp.match_fk0 = primitive.addTransform(comp.match_fk0_off,
                                                    comp.getName("fk0_mth"),
                                                    transform.getTransform(comp.fk_ctl[0]))
            comp.match_fk1_off = primitive.addTransform(comp.root,
                                                        comp.getName("matchFk1_npo"),
                                                        transform.getTransform(comp.fk_ctl[2]))
            comp.match_fk1 = primitive.addTransform(comp.match_fk1_off,
                                                    comp.getName("fk1_mth"),
                                                    transform.getTransform(comp.fk_ctl[1]))
            if comp.settings["ikTR"]:
                reference = comp.ikRot_ctl
                comp.match_ikRot = primitive.addTransform(comp.fk2_ctl,
                                                          comp.getName("ikRot_mth"),
                                                          transform.getTransform(comp.ikRot_ctl))
            else:
                reference = comp.ik_ctl
            comp.match_fk2 = primitive.addTransform(reference,
                                                    comp.getName("fk2_mth"),
                                                    transform.getTransform(comp.fk_ctl[2]))
            comp.match_ik = primitive.addTransform(comp.fk2_ctl,
                                                   comp.getName("ik_mth"),
                                                   transform.getTransform(comp.ik_ctl))
            comp.match_ikUpv = primitive.addTransform(comp.fk0_ctl,
                                                      comp.getName("upv_mth"),
                                                      transform.getTransform(comp.upv_ctl))
            # add visual reference
            comp.line_ref = icon.connection_display_curve(comp.getName("visalRef"),
                                                          [comp.upv_ctl, comp.mid_ctl])

            
            comp.relatives["root"] = comp.div_cns[0]
            comp.relatives["elbow"] = comp.div_cns[comp.settings["div0"] + 2]
            comp.relatives["wrist"] = comp.div_cns[-1]
            comp.relatives["eff"] = comp.eff_loc
            
            comp.jointRelatives["root"] = 0
            comp.jointRelatives["elbow"] = comp.settings["div0"] + 2
            comp.jointRelatives["wrist"] = len(comp.div_cns) - 1
            comp.jointRelatives["eff"] = -1
            
            comp.controlRelatives["root"] = comp.fk0_ctl
            comp.controlRelatives["elbow"] = comp.fk1_ctl
            comp.controlRelatives["wrist"] = comp.fk2_ctl
            comp.controlRelatives["eff"] = comp.fk2_ctl
            
            # here is really don't needed because the name is the same as the alias
            comp.aliasRelatives["root"] = "root"
            comp.aliasRelatives["elbow"] = "elbow"
            comp.aliasRelatives["wrist"] = "wrist"
            comp.aliasRelatives["eff"] = "hand"

            #===step_01()====
            #===getHost()===
            """Get the host for the properties"""
            comp.uihost = comp.rig.findRelative(comp.settings["ui_host"])
            #===validateProxyChannels()===
            if versions.current ()>=201650 and comp.options ["proxyChannels"]:
                comp.validProxyChannels = True
            else:
                comp.validProxyChannels = False
            #===addFullNameParam()===
            if comp.options["classicChannelNames"]:
                attr = comp.addAnimEnumParam(comp.getName(), "__________", 0, [comp.getName()])
            else:
                attr = comp.addAnimEnumParam(comp.guide.compName, "__________", 0, [comp.guide.compName])

            #===addAttributes()===
            comp.blend_att = comp.addAnimParam ("blend","Fk/Ik Blend","double",comp.settings ["blend"],0,1)
            comp.roll_att = comp.addAnimParam ("roll","Roll","double",0,-180,180)
            comp.armpit_roll_att = comp.addAnimParam ("aproll","Armpit Roll","double",0,-360,360)

            comp.scale_att = comp.addAnimParam ("ikscale","Scale","double",1,.001,99)
            comp.maxstretch_att = comp.addAnimParam ("maxstretch","Max Stretch","double",comp.settings ["maxstretch"],1,99)
            comp.slide_att = comp.addAnimParam ("slide","Slide","double",.5,0,1)
            comp.softness_att = comp.addAnimParam ("softness","Softness","double",0,0,1)
            comp.reverse_att = comp.addAnimParam ("reverse","Reverse","double",0,0,1)
            comp.roundness_att = comp.addAnimParam ("roundness","Roundness","double",0,0,comp.size)
            comp.volume_att = comp.addAnimParam ("volume","Volume","double",1,0,1)

            if comp.settings ["extraTweak"]:
                comp.tweakVis_att = comp.addAnimParam ("Tweak_vis", "Tweak Vis", "bool", False)

            # Ref
            if comp.settings ["ikrefarray"]:
                ref_names = comp.get_valid_alias_list (comp.settings ["ikrefarray"].split (","))

                if len (ref_names)>1:
                    comp.ikref_att = comp.addAnimEnumParam ("ikref", "Ik Ref", 0, ref_names)

            if comp.settings ["ikTR"]:
                ref_names = ["Auto", "ik_ctl"]
                if comp.settings ["ikrefarray"]:
                    ref_names = ref_names + comp.get_valid_alias_list (comp.settings ["ikrefarray"].split (","))

                comp.ikRotRef_att = comp.addAnimEnumParam ("ikRotRef","Ik Rot Ref",0,ref_names)

            if comp.settings ["upvrefarray"]:
                ref_names = comp.get_valid_alias_list (comp.settings ["upvrefarray"].split (","))
                ref_names = ["Auto"] + ref_names
                if len (ref_names)>1:
                    comp.upvref_att = comp.addAnimEnumParam ("upvref","UpV Ref",0, ref_names)

            if comp.settings ["pinrefarray"]:
                ref_names = comp.get_valid_alias_list (comp.settings ["pinrefarray"].split (","))
                ref_names = ["Auto"] + ref_names
                if len (ref_names)>1:
                    comp.pin_att = comp.addAnimEnumParam ("elbowref","Elbow Ref",0,ref_names)

            if comp.validProxyChannels:
                attrs_list = [comp.blend_att, comp.roundness_att]
                if comp.settings ["extraTweak"]:
                    attrs_list += [comp.tweakVis_att]
                attribute.addProxyAttribute (attrs_list,[comp.fk0_ctl,comp.fk1_ctl,comp.fk2_ctl,comp.ik_ctl,comp.upv_ctl,comp.mid_ctl])
                attribute.addProxyAttribute (comp.roll_att,[comp.ik_ctl, comp.upv_ctl])

            # Setup ------------------------------------------
            # Eval Fcurve
            comp.st_value = fcurve.getFCurveValues (comp.settings ["st_profile"],
                                                    comp.divisions)
            comp.sq_value = fcurve.getFCurveValues (comp.settings ["sq_profile"],
                                                    comp.divisions)

            comp.st_att = [comp.addSetupParam ("stretch_%s" % i,"Stretch %s" % i,"double", comp.st_value [i],-1,0)
                           for i in range (comp.divisions)]

            comp.sq_att = [comp.addSetupParam ("squash_%s" % i,"Squash %s" % i,"double",comp.sq_value [i],0,1)
                           for i in range (comp.divisions)]

            comp.resample_att = comp.addSetupParam ("resample","Resample","bool",True)
            comp.absolute_att = comp.addSetupParam ("absolute","Absolute","bool",False)

            #step_02()
            #===addOperators()===
            comp.ikHandleUpvRef = primitive.addIkHandle (comp.root,
                                                         comp.getName ("ikHandleArmChainUpvRef"),
                                                         comp.armChainUpvRef,
                                                         "ikSCsolver")
            pm.pointConstraint (comp.ik_ctl, comp.ikHandleUpvRef)
            pm.parentConstraint (comp.armChainUpvRef [0], comp.upv_cns, mo = True)

            # Visibilities -------------------------------------
            # fk
            fkvis_node = node.createReverseNode (comp.blend_att)
            for shp in comp.fk0_ctl.getShapes ():
                pm.connectAttr (fkvis_node + ".outputX", shp.attr ("visibility"))
            for shp in comp.fk1_ctl.getShapes ():
                pm.connectAttr (fkvis_node + ".outputX", shp.attr ("visibility"))
            for shp in comp.fk2_ctl.getShapes ():
                pm.connectAttr (fkvis_node + ".outputX", shp.attr ("visibility"))
            # ik
            for shp in comp.upv_ctl.getShapes ():
                pm.connectAttr (comp.blend_att, shp.attr ("visibility"))
            for shp in comp.ikcns_ctl.getShapes ():
                pm.connectAttr (comp.blend_att, shp.attr ("visibility"))
            for shp in comp.ik_ctl.getShapes ():
                pm.connectAttr (comp.blend_att, shp.attr ("visibility"))
            for shp in comp.line_ref.getShapes ():
                pm.connectAttr (comp.blend_att, shp.attr ("visibility"))
            if comp.settings ["ikTR"]:
                for shp in comp.ikRot_ctl.getShapes ():
                    pm.connectAttr (comp.blend_att, shp.attr ("visibility"))
            # Controls ROT order -----------------------------------
            attribute.setRotOrder (comp.fk0_ctl, "XZY")
            attribute.setRotOrder (comp.fk1_ctl, "XYZ")
            attribute.setRotOrder (comp.fk2_ctl, "YZX")
            attribute.setRotOrder (comp.ik_ctl, "XYZ")
            # IK Solver -----------------------------------------
            #--------------------------------------------------------------------
            # scale: this fix the scalin popping issue
            #--------------------------------------------------------------------
            # Twist references ---------------------------------
            #--------------------------------------------------------------------
            # Roll Shoulder
            #--------------------------------------------------------------------
            # Volume -------------------------------------------
            #--------------------------------------------------------------------
            # match IK/FK ref
            #--------------------------------------------------------------------
            #===step_03()===
            #===initConnector()===
            parent_name = "none"
            if comp.guide.parentComponent is not None:
                parent_name = comp.guide.parentComponent.getName(comp.guide.parentLocalName)
            comp.parent = comp.rig.findRelative(parent_name)
            comp.parent_comp = comp.rig.findComponent(parent_name)
            #===addConnection()===
            comp.connections ["shoulder_01"] = comp.connect_shoulder_01
            #===connect()===
            if comp.settings ["connector"] not in comp.connections.keys ():
                rigging.beam.log ("Unable to connect object", rigging.beam.sev_error)
            try:
                comp.connections [comp.settings ["connector"]] ()
            except AttributeError:
                pass
            #===postConnect()===
            #===step_04()===
            # get parent component joint
            if comp.settings["useIndex"]:
                try:
                    comp.active_jnt = comp.parent_comp.jointList[comp.settings["parentJointIndex"]]
                except Exception:
                    pm.displayWarning(
                        "The parent component for: %s don't have "
                        "any joint with the index: %s." %
                        (comp.fullName, str(comp.settings["parentJointIndex"])))
            else:
                parent_name = "none"
                if comp.guide.parentComponent is not None:
                    parent_name = comp.guide.parentComponent.getName(comp.guide.parentLocalName)

                relative_name = comp.rig.getRelativeName(parent_name)

                oParent_comp = comp.parent_comp
                while oParent_comp:
                    try:
                        comp.active_jnt = oParent_comp.jointList[oParent_comp.jointRelatives[relative_name]]
                        # when we search  in the parent component for a active jnt
                        # we also store it for later retrive
                        comp.parent_relative_jnt = comp.active_jnt
                        break
                    except Exception:
                        if oParent_comp.parent_comp:
                            pgpc = oParent_comp.guide.parentComponent
                            parent_name = pgpc.getName(oParent_comp.guide.parentLocalName)
                            relative_name = oParent_comp.rig.getRelativeName(parent_name)
                        else:
                            pm.displayInfo(
                                "The parent components for: %s don't have joint "
                                "List in any of them use the root off guide." %
                                comp.fullName)

                        oParent_comp = oParent_comp.parent_comp

            # Joint creation
            for jpo in comp.jnt_pos:
                if len(jpo) >= 3 and comp.options["joint_rig"]:
                    if jpo[2] == "component_jnt_org":
                        newActiveJnt = comp.component_jnt_org
                    elif jpo[2] == "parent_relative_jnt":
                        # this option force the active jnt always to the parent
                        # relative jnt.
                        # If None the active jnt will be updated to the latest in
                        # each jnt creation
                        newActiveJnt = comp.parent_relative_jnt
                    else:
                        try:
                            # here jpo[2] is also the string name of the jnt inside
                            # the component. IE: "root"
                            newActiveJnt = comp.jointList[comp.jointRelatives[jpo[2]]]

                        except Exception:
                            if jpo[2]:
                                pm.displayWarning(
                                    "Joint Structure creation: "
                                    "The object %s can't be found. Joint parent is"
                                    " NONE for %s, from %s" %
                                    (jpo[2], jpo[0], comp.fullName))
                            newActiveJnt = None
                else:
                    newActiveJnt = None
                # Handle the uniform scale
                if len(jpo) == 4 and comp.options["joint_rig"]:
                    uniScale = jpo[3]
                else:
                    uniScale = False
                # handle the matrix node connection
                if len(jpo) == 5 and comp.options["joint_rig"]:
                    gearMulMatrix = jpo[4]
                else:
                    gearMulMatrix = True

                comp.jointList.append(comp.addJoint(jpo[0], jpo[1], newActiveJnt, uniScale,gearMulMatrix=gearMulMatrix))
            #===step_05()===
            #===finalize()===
            for t in comp.transform2Lock:
                attribute.lockAttribute (t)
            #===postScript()===
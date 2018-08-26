import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import sys
import math

nodeName = ''
nodeID = OpenMaya.MTypeId(0x00000720)

class Deformer(OpenMayaMPx.MPxGeometryFilter):

    aCollideMatrix = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxGeometryFilter.__init__(self)
    
    def accessoryNodeSetup(self,dagMod):
		return result
    
    def accessoryAttribute(self):
        return self.aCollideMatrix

    def deform(self, data, itGeo, localToworldWatrix,geomIndex):
		pass

def nodeCreator():
    return OpenMayaMPx.asMPxPtr(Deformer())


def nodeInitializer():
	nAttr = OpenMaya.MFnMatrixAttribute()
	
	
def initializePlugin(mobject):
    fnPlugin = OpenMayaMPx.MFnPlugin(mobject, 'Beam', '1.0', 'Any')
    try:
        fnPlugin.registerNode(nodeName, nodeID, nodeCreator, nodeInitializer,OpenMayaMPx.MPxNode.kDeformerNode)
    except:
        sys.stderr.write('Failed to register node:' + nodeName)
        raise

def uninitializePlugin(mobject):
    fnPlugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        fnPlugin.deregisterNode(nodeID)
    except:
        sys.stderr.write('Failed to deregister node' + nodeName)
        raise
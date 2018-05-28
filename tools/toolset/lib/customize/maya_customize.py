# -*- coding: utf-8 -*-

import os
try:
    import pymel.core as pm
    import maya.cmds as cmds
    import maya.OpenMaya as OpenMaya
except:
    pass

class maya_customize(object):

    def __init__(self):
        super (maya_customize, self).__init__ ()

    def get_RefereceNodes(self):
        iter_ref_nodes = OpenMaya.MItDependencyNodes (OpenMaya.MFn.kReference)
        #ref_node_tostrings = list()
        ref_nodes = OpenMaya.MObjectArray()
        while not iter_ref_nodes.isDone ():
            mnode = iter_ref_nodes.thisNode ()
            ref_nodes.append(mnode)
            #refnode = OpenMaya.MFnDependencyNode (mnode)
            #ref_node_tostrings.append(refnode.name ())
            iter_ref_nodes.next ()
        return ref_nodes

    def openFile(self,maya_file):
        if maya_file:
            mFile = OpenMaya.MFileIO()
            mFile.open(r"%s"%os.path.abspath(maya_file).replace("\\","/"),None,True)

    def importFile(self,maya_file):
        if maya_file:
            mFile = OpenMaya.MFileIO()
            util = OpenMaya.MScriptUtil ()
            ptr = util.asCharPtr ()
            mFile.importFile (r"%s" % os.path.abspath (maya_file).replace ("\\", "/"),
                              None, False,
                              None,False)

    def referenceFile(self,maya_file):
        if maya_file:
            mFile = OpenMaya.MFileIO()
            mFile.reference(r"%s"%os.path.abspath(maya_file).replace("\\","/"),
                            False,False,os.path.basename(maya_file))
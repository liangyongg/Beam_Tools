"""Nvigate the DAG hierarchy"""


import maya.cmds as cmds
import pymel.core as pm

#############################################
# DAG
#############################################


def getTopParent(node):
    return node.getParent(generations=-1)


def getShapes(node):
    return node.listRelatives(shapes=True)


def findChild(node, name):
    # return __findChildren(node, name, True)
    return __findChild(node, name)


def findChildren(node, name):
    return __findChildren(node, name, False)


def findChildrenPartial(node, name):
    return __findChildren(node, name, False, True)


def __findChildren(node, name, firstOnly=False, partialName=False):

    if partialName:
        children = [item for item
                    in node.listRelatives(allDescendents=True,
                                          type="transform")
                    if item.name().split("|")[-1].split("_")[-1] == name]
    else:
        children = [item for item
                    in node.listRelatives(allDescendents=True,
                                          type="transform")
                    if item.name().split("|")[-1] == name]
    if not children:
        return False
    if firstOnly:
        return children[0]

    return children


def __findChild(node, name):
    try:
        for item in cmds.listRelatives(node.name(),
                                       allDescendents=True,
                                       type="transform"):
            if item.split("|")[-1] == name:
                return pm.PyNode(item)
    except pm.MayaNodeError:
        for item in node.listRelatives(allDescendents=True,
                                       type="transform"):
            if item.split("|")[-1] == name:
                return item

    return False


def __findChildren2(node, name, firstOnly=False, partialName=False):
    oName = node.name()
    if partialName:
        children = [item for item
                    in cmds.listRelatives(oName, allDescendents=True,
                                          type="transform")
                    if item.split("|")[-1].split("_")[-1] == name]
    else:
        children = [item for item
                    in cmds.listRelatives(oName, allDescendents=True,
                                          type="transform")
                    if item.split("|")[-1] == name]
    if not children:
        return False
    if firstOnly:
        return pm.PyNode(children[0])

    return [pm.PyNode(x) for x in children]


def findComponentChildren(node, name, sideIndex):
    children = []
    for item in node.listRelatives(allDescendents=True,
                                   type="transform"):
        checkName = item.name().split("|")[-1].split("_")
        if checkName[0] == name and checkName[1] == sideIndex:
            children.append(item)

    return children


def findComponentChildren2(node, name, sideIndex):
    children = []
    for item in cmds.listRelatives(node.name(), allDescendents=True,
                                   type="transform"):
        checkName = item.split("|")[-1].split("_")
        if checkName[0] == name and checkName[1] == sideIndex:
            children.append(item)

    return [pm.PyNode(x) for x in children]

# -*- coding: utf-8 -*-

import pymel.core as pm
import maya.cmds as cmds
import traceback

class Rigging_Check():

    def __init__(self):
        self.check_name = "check_same_names"
        self.description = "check the same objs in scence"
        self.auto_fix = False
        self.dataDict = {}

    def checksamename(self):
        samenames = []
        nodenames = cmds.ls(rn=0,dag=1)
        for nodename in nodenames:
            if "|" in nodename:
                samenames.append(nodename)
        refnodelist = cmds.ls(rn=1,dag=1)
        if refnodelist:
            for refnode in refnodelist:
                if refnode.split(':')[-1] in nodenames:
                    samenames.append(refnode.split(":")[-1])
                    samenames.append(refnode)
                    self.dataDict[refnode] = "more than one obj is %s name!!!"%(refnode)
        if samenames:
            cmds.select(samenames,r=1)
            num = len(samenames)
        return self.dataDict

    def do_check(self):
        try:
            res = self.checksamename()
            return res
        except:
            return traceback.format_exc()

    def do_fix(self):
        return

    def get_check_name(self):
        return self.check_name

    def get_auto_fix(self):
        return self.auto_fix
#!/usr/bin/env python
# -*- coding: utf-8 -*

import traceback
import maya.cmds as cmds

class master_check():

    def __init__(self):
        self.check_name = "check maya is save"
        self.description = "check maya is save"
        self.auto_fix = False
        return

    def check_maya_issave(self):
        if_edit=cmds.file(q=True,mf=True)
        if if_edit:
            print "The file has been modified, or the file has not been saved"
            return "The file has been modified, or the file has not been saved"
        else:
            return ""

    def do_check(self):
        try:
            res = self.check_maya_issave()
            return res
        except:
            return traceback.format_exc()

    def do_fix(self):
        return

    def get_check_name(self):
        return self.check_name

    def get_description(self):
        return self.description

    def get_auto_fix(self):
        return self.auto_fix
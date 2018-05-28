#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import re
import maya.cmds as cmds

class master_check():

    def __init__(self):
        self.check_name = "check_maya_file_plugs"
        self.description = "check_maya_file_plugs"
        self.auto_fix = False
        return

    def get_ma_file_requires(self,source_path):
        plg = re.compile(r'requires "(.*)" .*;')
        all_requires = []
        for line in open(source_path,"r"):
            res=plg.findall(line)
            if res:
                all_requires.append(res[0])
        return all_requires

    def check_maya_plgs(self):
        sn_name = cmds.file(q=True,sn=True)
        if sn_name:
            all_requires=self.get_ma_file_requires(sn_name)
            if all_requires:
                print u"file have more plugs please delete it!!!" + str(all_requires)
        else:
            print u"have not get the file name!"
        return ''

    def do_check(self):
        try:
            res = self.check_maya_plgs()
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
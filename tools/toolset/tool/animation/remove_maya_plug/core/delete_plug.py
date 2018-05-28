#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

def delete_maya_plug(sourcepath,rebuildpath):
    print sourcepath,rebuildpath

    stat_re = re.compile(r'^requires\s-nodeType\s.*')
    and_re = re.compile(r'.*-nodeType.*')
    pass_re = re.compile(r'^requires\s\"')
    mayatomr_re = re.compile(r'.*\s"Mayatomr\"\s\"2014.*')

    abc_re = re.compile(r'^requires\s-nodeType\s"AlembicNode".*')
    shave_start_re = re.compile(r'^requires\s-nodeType\s"shaveHair".*')
    shave_re = re.compile(r'.*-nodeType\s"shave.*')
    rsStart_re = re.compile(r'^requires\s-nodeType\s"Redshift".*')
    rsNodeType_re = re.compile(r'.*-nodeType\s"Redshift.*')
    rsEnd_re = re.compile(r'.*\s"redshift4maya"\s.*')
    checkState_re = re.compile(r'^currentUnit\s-l\s.*')

    shave_end_re = re.compile(r'^\s+"shaveNode"\s.*;')

    if os.path.exists(rebuildpath):
        os.remove(rebuildpath)

    with open(sourcepath,'r') as read_file:
        if os.path.exists(rebuildpath):
            new_file = open(rebuildpath,"a")
        else:
            new_file = open (rebuildpath, "w")
        check_shave_node_state = 0
        checkState = 1
        for line in read_file:
            if shave_start_re.findall(line):
                check_shave_node_state=1
            if checkState:
                if checkState_re.findall(line):
                    checkState=0
                if stat_re.findall(line) or and_re.findall(line) or pass_re.findall(line) or mayatomr_re.findall(line) or shave_end_re.findall(line):
                    if rsStart_re.findall(line) or rsNodeType_re.findall(line) or rsEnd_re.findall(line) or abc_re.findall(line) or (shave_re.findall(line) and check_shave_node_state) or (shave_end_re.findall(line) and check_shave_node_state):
                        new_file.write(line)
                        if shave_end_re.findall(line):
                            check_shave_node_state=0
                    else:
                        pass
                else:
                    new_file.write(line)
            else:
                new_file.write(line)
        new_file.close()
        print rebuildpath + "finished!!!"
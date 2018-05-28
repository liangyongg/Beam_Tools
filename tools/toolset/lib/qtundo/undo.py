#!/usr/bin/env python
# -*- coding: utf-8 -*-

import maya.cmds as cmds

def qtundo(func):
    def warpper(*args,**kwargs):
        cmds.undoInfo(openChunk=True)
        try:
            func(*args,**kwargs)
        finally:
            cmds.undoInfo(closeChunk=True)
    return warpper
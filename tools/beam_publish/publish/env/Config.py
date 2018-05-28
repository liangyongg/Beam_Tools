#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sever_tool_path = r"E:\Beam_tools\tools\toolset\tool"
sever_project_path = r"E:\Beam_tools\tools\toolset\project"

local_tool_path = r"E:\git_work\Beam_Tools\tools\toolset\tool"
local_project_path = r"E:\git_work\Beam_Tools\tools\toolset\project"

sys.path.append(sever_tool_path)
sys.path.append(sever_project_path)
sys.path.insert(0,local_tool_path)
sys.path.insert(0,local_project_path)
import playfun

class Config(object):
    TEMP_PATH = r"E:\temp"
    DEBUG = 'pub'

    if DEBUG=="ly":
        PROJECT_ASSET_PUB_PATH = r""
        PROJECT_ASSET_WORK_PATH = r""
        PROJECT_SHOT_WORK_PATH = r""
        PUBLISH_PATH_PIX = r"E:\git_work\Beam_Tools\tools\beam_publish\publish"
        PROJECT_ASSET_PATH = r""
        PROJECT_SHOT_PATH = r""
        PUBLISH_INFO_PATH = r""

    elif DEBUG=="pub":
        PROJECT_ASSET_PUB_PATH = r""
        PROJECT_ASSET_WORK_PATH = r""
        PROJECT_SHOT_WORK_PATH = r""
        PUBLISH_PATH_PIX = r"E:\git_work\Beam_Tools\tools\beam_publish\publish"
        PROJECT_ASSET_PATH = r""
        PROJECT_SHOT_PATH = r""
        PUBLISH_INFO_PATH = r""

    ASSET_STEP_TASK_INFO = playfun.Config.ASSET_STEP_TASK_INFO
    SHOT_STEP_TASK_INFO = playfun.Config.SHOT_STEP_TASK_INFO
    STEP_NAME_LIB = playfun.Config.STEP_NAME_LIB
    TYPE_LIST = playfun.Config.TYPE_LIST

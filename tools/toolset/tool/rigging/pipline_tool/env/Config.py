# -*- coding: utf-8 -*-

import os

class Config(object):

    PROJECT_ASSET_RIG_PUB_PATH = ""
    PROJECT_ASSET_RIG_WORK_PATH = r"D:\work\hszb"
    PROJECT_ASSET_SEVER_PATH = r"D:\work\hszb\Character"

    PROJECT_LOCAL_WORK_PATH = os.path.join(PROJECT_ASSET_RIG_WORK_PATH,'asset_work').replace("\\","/")
    PROJECT_ASSET_WORK_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),'asset_work').replace("\\","/")
    PROJECT_ASSET_BASE_PATH = os.path.join(os.path.dirname(os.path.realpath (__file__)),'asset_base','example').replace("\\","/")

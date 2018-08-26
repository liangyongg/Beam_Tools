#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import yaml
import glob
import inspect
from publish.ui.head import *
from publish.core import check_class
reload(check_class)

def get_check_data (data):
    data_group = dict ()
    all_check_lib = {}
    check_group_list = []
    check_groupcheck_item = {}
    if os.path.isfile (data):
        with file (data, "r") as root:
            data_group = yaml.load (root)
    if data_group:
        for data in data_group:
            all_check_lib [data] = {}
            check_groupcheck_item [data] = []
            check_group_list.append (data)
            for grp in data_group [data]:
                name = grp ['name']
                all_check_lib [data] [name] = grp
                check_groupcheck_item [data].append (name)

    return all_check_lib, check_groupcheck_item, check_group_list

def get_process_data(data):
    data_group={}
    process_info={}
    process_list=[]
    if os.path.isfile(data):
        with file(data,"r") as root:
            data_group = yaml.load(root)
    if data_group:
        for data in data_group:
            for grp in data_group[data]:
                name = grp['name']
                process_info[name]=grp
                process_list.append(name)

    return process_info,process_list

def current_path (self):
    path = os.path.realpath (sys.path [0])
    if os.path.isfile (path):
        path = os.path.dirname (path)
        return os.path.abspath (path)
    else:
        caller_file = inspect.stack () [1] [1]
        return os.path.abspath (os.path.dirname (caller_file))

def get_asset_path_info():
    sn_name=cmds.file(q=True,sn=True)
    file_name=os.path.basename(sn_name)
    asset_name=os.path.basename(sn_name).split("_")[0]+"_"+os.path.basename(sn_name).split("_")[1]

def bulid_ui(tabwidget,check_yaml,process_yaml,infowidget,cousinfo,publishwidget):
    all_check_lib, check_groupcheck_item, check_group_list = get_check_data(check_yaml)
    process_info,process_list = get_process_data(process_yaml)
    all_check_lib["process"]=process_info
    check_groupcheck_item["process"]=process_list
    check_group_list.append("process")

    for check_group_item in check_group_list:
        widget = QWidget()
        mainVboxLayout = QVBoxLayout(widget)
        widget.setContentsMargins(0,0,0,0)
        if check_group_item != "process":
            module_step = "publish_check"
        else:
            module_step = "publish_processes"
        tab_name = check_group_item
        for check_item in check_groupcheck_item[check_group_item]:
            allow_skip = all_check_lib[check_group_item][check_item].get("allow_skip","")
            if not allow_skip:
                allow_skip="false"
            check_name=all_check_lib[check_group_item][check_item]["name"]
            check_type=all_check_lib[check_group_item][check_item]["type"]
            check_item_class=check_class.check_widget(infowidget,module_step,tab_name,check_type,check_name,allow_skip,cousinfo,publishwidget)
            all_check_lib[check_group_item][check_item]["class"]=check_item_class
            mainVboxLayout.addWidget(check_item_class)
        mainVboxLayout.setSpacing(1)
        spacerItem=QSpacerItem(20,300,QSizePolicy.Minimum,QSizePolicy.Expanding)
        mainVboxLayout.addItem(spacerItem)
        tabwidget.addTab(widget,tab_name)
    return all_check_lib,check_groupcheck_item,check_group_list

def get_pass_info():
    pass_info={}
    sn_name=cmds.file(q=True,sn=True)
    file_name=os.path.basename(sn_name)
    asset_name=os.path.basename(sn_name).split("_")[0]+os.path.basename(sn_name).split("_")[1]
    no_version_publish_floder=os.path.join(sn_name.replace("\\","/").split("/srf/")[0],"srf",asset_name+".srf.surface")
    publish_folder_path=no_version_publish_floder.replace("\\","/").replace("/work/","/Reference/")
    defout_pass_file=glob.glob(os.path.join(publish_folder_path,file_name))
    if defout_pass_file:
        pass_info["default"] = defout_pass_file[0].replace("\\","/")
    else:
        pass_info["default"] = None

    pass_file_list=glob.glob(os.path.join(publish_folder_path,'pass',"*",file_name))
    if pass_file_list:
        pass_file_list=[x.replace("\\","/") for x in pass_file_list]
        for pass_path_item in pass_file_list:
            pass_name=pass_path_item.split("/")[0]
            pass_info[pass_name]=pass_path_item
    return pass_info
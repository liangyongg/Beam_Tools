import maya.cmds as cmds
import sys
import os
#from xml.etree import ElementTree
import yaml

yaml_path = r"E:/Beam_tools/tools/toolset/application/maya/Startup/menu.yaml"

def get_menu_data(yaml_path):
    menu_group = dict()
    if os.path.isfile(yaml_path):
        with open(yaml_path) as root:
            menu_group = yaml.load(root)
    return menu_group

def createmenu(configfile,parent):
    if configfile:
        options = configfile[configfile.keys()[0]]
        for option in options:
            if option['type'] == 'action':
                command = option['cmd']
                cmds.menuItem (l = option['name'], p = parent, c = str (command))
            elif option['type'] == 'menu':
                aa = cmds.menuItem (l = option['name'], bld = 1, sm = 1, to = 1, p = parent)
                createmenu (option, aa)
            elif option['type'] == 'separator':
                cmds.menuItem (divider = True, p = parent)

def main():
    configfile = get_menu_data (yaml_path)
    if configfile:
        if cmds.menu ('Beam_menu', exists = True):
            cmds.deleteUI ('Beam_menu')
        cmds.menu ('Beam_menu', label = configfile.keys () [0], to = True, p = 'MayaWindow')
        createmenu(configfile,'Beam_menu')
#a = get_menu_data(yaml_path)
#print a
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import subprocess
sys.path.append(r"E:\Beam_tools\tools\beam_publish")
try:
    import maya.cmds as cmds
    tool_in_app="maya"
except:
    pass

try:
    import nuke
    tool_in_app="nuke"
except:
    pass

from publish.ui.head import *
from publish.ui.ui_main_window import ui_main_window
import publish.env.Config as Config
import publish.core.work_response as wr
reload(wr)
reload(Config)

class publish_info():
    def __init__(self):
        pass

class Response(QtGui.QMainWindow):

    def __init__(self,parent=None,step="rigging"):
        super(Response,self).__init__(parent)

        self.STEP_NAME_LIB = Config.Config.STEP_NAME_LIB
        self.check_res_info={}
        self.check_yaml=''
        self.processe_yaml=''
        self.current_step=''
        self.current_shot_asset = ''
        self.ct_step = ''
        self.current_task = ''
        self.version_num = ''

        self.setWindowTitle ("Beam_Publish_Tool")
        self.step = step
        self.ct_step = self.STEP_NAME_LIB[step]
        self.setupUI()
        self.getElems()
        self.setDefault()
        self.connections()

    def get_pub_info(self):
        self.pub_info = publish_info()
        self.project_shot_path = Config.Config.PROJECT_SHOT_PATH
        self.project_shot_work_path = Config.Config.PROJECT_SHOT_WORK_PATH
        self.version_pub_info_path = Config.Config.PUBLISH_INFO_PATH
        self.project_asset_pub_path = Config.Config.PROJECT_ASSET_PUB_PATH
        self.project_asset_work_path = Config.Config.PROJECT_ASSET_WORK_PATH

        self.pub_info.version_pub_info_path = self.version_pub_info_path
        self.pub_info.project_shot_path = self.project_shot_path
        self.pub_info.project_shot_work_path = self.project_shot_work_path
        self.pub_info.project_asset_pub_path = self.project_asset_pub_path
        self.pub_info.project_asset_work_path = self.project_asset_work_path

        self.pub_info.shot_asset_name = self.current_shot_asset
        self.pub_info.ct_step = self.ct_step
        self.pub_info.current_task = self.current_task
        self.pub_info.version_num = self.version_num

    def setupUI(self):
        self.ui_main_window = ui_main_window()
        self.setCentralWidget(self.ui_main_window)

    def get_step_yaml(self):
        PUBLISH_PATH_PIX=Config.Config.PUBLISH_PATH_PIX
        check_yaml = os.path.join(PUBLISH_PATH_PIX,"depts",self.step,"publish_check.yaml")
        processe_yaml = os.path.join(PUBLISH_PATH_PIX,"depts",self.step,"publish_processes.yaml")
        if os.path.exists(check_yaml):
            self.check_yaml = check_yaml
        if os.path.exists(processe_yaml):
            self.processe_yaml = processe_yaml

    def getElems(self):
        self.version_label = self.ui_main_window.ui_publish_widget.main_Widget.version_label
        self.version_lineEdit = self.ui_main_window.ui_publish_widget.main_Widget.version_lineEdit
        self.Automatic_upgrade_version_pushButton = self.ui_main_window.ui_publish_widget.main_Widget.Automatic_upgrade_version_pushButton
        self.save_as_work_pushButton = self.ui_main_window.ui_publish_widget.main_Widget.save_as_work_pushButton
        self.version_spinBox = self.ui_main_window.ui_publish_widget.main_Widget.version_spinBox

        self.shot_asset_comboBox = self.ui_main_window.ui_publish_widget.main_Widget.shot_asset_comboBox
        self.publish_step_label = self.ui_main_window.ui_publish_widget.main_Widget.publish_step_label
        self.task_comboBox = self.ui_main_window.ui_publish_widget.main_Widget.task_comboBox
        self.publish_out_info_textBrowser = self.ui_main_window.ui_publish_widget.main_Widget.publish_out_info_textBrowser
        self.publish_work_tabWidget = self.ui_main_window.ui_publish_widget.main_Widget.publish_work_tabWidget
        self.Previous_page_pushButton = self.ui_main_window.ui_publish_widget.main_Widget.Previous_page_pushButton
        self.Next_page_pushButton = self.ui_main_window.ui_publish_widget.main_Widget.Next_page_pushButton
        self.Check_all_pushButton = self.ui_main_window.ui_publish_widget.main_Widget.Check_all_pushButton
        self.publish_info_plainTextEdit = self.ui_main_window.ui_publish_widget.main_Widget.publish_info_plainTextEdit

        #self.frame_widget = self.ui_main_window.ui_publish_widget.main_Widget.frame_widget


    def get_default_info(self):
        self.get_pub_info()
        self.cous_info = {"ct_step":self.ct_step,
                          "task_combobox":self.task_comboBox,
                          "shot_asset_combobox":self.shot_asset_comboBox,
                          "pubinfo":self.pub_info
                          }

    def setDefault(self):
        self.get_default_info()
        self.pub_info.version_num = self.version_spinBox.value()
        self.ASSET_STEP_TASK_INFO = Config.Config.ASSET_STEP_TASK_INFO
        self.SHOT_STEP_TASK_INFO = Config.Config.SHOT_STEP_TASK_INFO
        self.TYPE_LIST = Config.Config.TYPE_LIST
        self.debug = Config.Config.DEBUG
        if self.debug == "pub":
            self.version_label.setText(u"release version")
        else:
            self.version_label.setText(str(self.debug)+"test version")
        self.get_step_yaml()
        print self.check_yaml
        print self.processe_yaml
        self.publish_step_label.setText(self.step)
        self.shot_asset_comboBox.addItems(self.TYPE_LIST)
        self.shot_asset_comboBox.setCurrentIndex(-1)
        #self.auto_ani_rig_checkBox.hide()
        #self.pass_widget.hide()
        self.all_check_lib,self.check_groupcheck_item,self.check_group_list = wr.bulid_ui(self.publish_work_tabWidget,
                                                                                          self.check_yaml,
                                                                                          self.processe_yaml,
                                                                                          self.publish_out_info_textBrowser,
                                                                                          self.cous_info,
                                                                                          self)
        self.set_check_default_info()

    def set_pass_widget_info(self):
        self.pass_info = wr.get_pass_info()

    def set_check_default_info(self):
        for check_group in self.check_group_list:
            self.check_res_info[check_group]=False

    def connections(self):
        self.save_as_work_pushButton.clicked.connect(self.save_to_work_pushButton_clicked)
        self.Automatic_upgrade_version_pushButton.clicked.connect(self.on_publishButton_clicked)
        self.version_spinBox.valueChanged.connect(self.on_version_spinBox_currentIndex)
        self.shot_asset_comboBox.currentIndexChanged.connect(self.on_shot_asset_comBox_currentIndex)
        self.Next_page_pushButton.clicked.connect(self.on_publish_down_page_pushButton_clicked)
        self.task_comboBox.currentIndexChanged.connect(self.on_task_comBox_currentIndex)
        self.Previous_page_pushButton.clicked.connect(self.on_publish_up_page_pushButton_clicked)
        self.Check_all_pushButton.clicked.connect(self.on_publish_all_check_pushButton_clicked)
        self.publish_work_tabWidget.currentChanged.connect(self.on_publish_work_tabwidget_clicked)

    def get_version_name(self,file_floder):
        all_version = [i.split('.v')[-1] for i in glob.glob(file_floder+'.v*')]
        if all_version:
            all_version.sort()
            version_num_str='v'+str(int(all_version[-1])+1).zfill(3)
            right_publish_floder=file_floder+'.'+version_num_str
            return right_publish_floder,int(all_version[-1])+1
        else:
            right_publish_floder=file_floder+".v001"
            return right_publish_floder,1

    def on_publishButton_clicked(self):
        self.version_spinBox.setValue(0)
        self.version_lineEdit.setText('')

        self.ple_step_name=''
        self.ple_task_name=''
        self.ple_file_name_prx=''
        if self.pub_info.shot_asset_name=="asset":
            self.sn_name=cmds.file(q=True,sn=True)
            self.file_name=os.path.basename(self.sn_name)
            self.asset_name=os.path.basename(self.sn_name).split("_")[0]+"_"+os.path.basename(self.sn_name).split("_")[1]

            if self.pub_info.shot_asset_name=="asset" and self.pub_info.current_task == "HighTexture":
                self.ple_step_name="srf"
                self.ple_task_name="surface"
                self.ple_file_name_prx="_H_tex.ma"

            if self.pub_info.shot_asset_name=="asset" and self.pub_info.current_task == "AniRig":
                self.ple_step_name="rig"
                self.ple_task_name="rigging"
                self.ple_file_name_prx="_rig_ani.ma"

            if self.pub_info.shot_asset_name and self.pub_info.current_task and self.ple_step_name:
                print self.asset_name,self.ple_file_name_prx
                print self.file_name
                if self.asset_name+self.ple_file_name_prx==self.file_name:
                    publish_path_file=glob.glob(os.path.join(self.project_asset_pub_path,"*",self.asset_name))
                    if publish_path_file:
                        work_file_path = publish_path_file[0].replace("Reference","work")
                        work_full_name_floder=os.path.join(work_file_path,self.ple_step_name,self.asset_name+".%.%s"%(self.ple_step_name,self.ple_task_name))
                        up_work_file_path,new_version=self.get_version_name(work_full_name_floder)
                        self.current_version_name=os.path.basename(up_work_file_path).rsplit('.')[-1]
                        up_work_file_path_maya=os.path.join(up_work_file_path,self.asset_name+self.ple_file_name_prx)
                        self.version_spinBox.setValue(new_version)
                        self.version_lineEdit.setText(up_work_file_path_maya)
                    else:
                        print self.asset_name+u" have not asset on server.please check"

                else:
                    print u"file name and select task is difrent"
                    cmds.warning (u"file name and select task is difrent")
            else:
                print u"please select task type!"
                cmds.warning(u"please select task type!")
        elif self.pub_info.shot_asset_name=="shot":
            if self.pub_info.current_task=="Composite":
                import nuke
                self.sn_name=nuke.scriptName()
                self.file_name=os.path.basename(self.sn_name).split("_")[0]
                self.shot_name=os.path.basename(self.sn_name).split("_")[1]
                self.ple_step_name="comp"
                self.ple_task_name="composite"
                self.ple_file_name_prx="_comp.nk"

                publish_path_file = glob.glob(os.path.join(self.project_shot_path,self.sq_name,self.shot_name))
                if publish_path_file:
                    work_file_path = publish_path_file[0].replace("\\",'/').replace("/final/","/work/")
                    work_full_name_floder = os.path.join(work_file_path,self.pub_info.current_task,"%s%s.%s.%s"%(self.sq_name,self.shot_name,self.ple_step_name,self.ple_task_name))
                    up_work_file_path,new_version = self.get_version_name(work_full_name_floder)
                    up_work_file_path_maya = os.path.join(up_work_file_path,'nuke','script',self.sq_name+"_"+self.shot_name+self.ple_file_name_prx).replace("\\","/")
                    self.version_spinBox.setValue(new_version)
                    self.version_lineEdit.setText(up_work_file_path_maya)
                else:
                    print self.sn_name+"_"+self.shot_name+"shot have not on server,please check"
        else:
            print "please select task type!"
            cmds.warning("please select task type!")

    def run_update_file_name(self):
        pass

    def on_publish_work_tabwidget_clicked(self,index):
        if self.check_group_list[index]=="process":
            self.Check_all_pushButton.setText("publish")
        else:
            self.Check_all_pushButton.setText("checkAll")

    def robocopy_file(self,s_rodo,d_robo):
        import os,subprocess
        d_path = os.path.join(d_robo,os.path.basename(s_rodo).replace("\\","/"))
        cmd_str = 'robocopy '+os.path.dirname(s_rodo)+' '+d_robo+' '+os.path.basename(s_rodo)+' /s /lev:1'
        print cmd_str
        if not os.path.exists(d_path):
            subprocess.call(cmd_str,shell=True)
        else:
            print 'Path exists! '+d_robo

    def save_to_work_pushButton_clicked(self):
        work_maya_file_path=self.version_lineEdit.text()
        if tool_in_app=="nuke":
            if work_maya_file_path and not os.path.exists(os.path.dirname(work_maya_file_path)):
                os.makedirs(os.path.dirname(work_maya_file_path))
                nuke.scriptSaveAs(work_maya_file_path)
                self.version_lineEdit.setText("")
                pass
        elif tool_in_app=="maya":
            if work_maya_file_path and not os.path.exists(os.path.dirname(work_maya_file_path)):
                tmp_file_path=os.path.join(Config.Config.TEMP_PATH)
                os.makedirs(os.path.dirname(work_maya_file_path))
                tmp_folder=Config.Config.TEMP_PATH
                self.run_update_file_name()
                asset_group_type = work_maya_file_path.replace("\\","/").split("/")[-5]
                if asset_group_type in ["SceneSet","Material"]:
                    tmp_file_path = os.path.join(tmp_folder,os.path.basename(work_maya_file_path))
                    cmds.file(rename=tmp_file_path)
                    cmds.file(save=1,option="v=0",type="mayaAscii",f=1)

                    self.robocopy_file(tmp_file_path,os.path.dirname(work_maya_file_path))

                    cmds.file(work_maya_file_path,open=1,f=1)

                else:
                    cmds.file(rename=work_maya_file_path)
                    cmds.file(save=1,options="v=0;",type="MayaAscii",f=1)
                self.version_lineEdit.setText("")

    def on_version_spinBox_currentIndex(self,value_as_int):
        self.version_num=value_as_int
        self.pub_info.version_num=self.version_num

    def on_shot_asset_comBox_currentIndex(self):
        self.current_shot_asset=self.shot_asset_comboBox.currentText()
        if self.current_shot_asset=='shot' and self.ct_step:
            step_list=self.SHOT_STEP_TASK_INFO.get(self.ct_step,[])
            if step_list:
                self.task_comboBox.clear()
                self.task_comboBox.addItems(step_list)
                self.task_comboBox.setCurrentIndex(-1)
        if self.current_shot_asset=='asset' and self.ct_step:
            #self.frame_widget_hide()
            step_list=self.ASSET_STEP_TASK_INFO.get(self.ct_step,[])
            if step_list:
                self.task_comboBox.clear()
                self.task_comboBox.addItems(step_list)
                self.task_comboBox.setCurrentIndex(-1)
        self.pub_info.shot_asset_name=self.current_shot_asset

    def on_task_comBox_currentIndex(self):
        self.current_task = self.task_comboBox.currentText()
        self.pub_info.current_task = self.current_task

        #if self.pub_info.current_task == "Composite":
        #    self.frame_widget.show()
        #else:
        #    self.frame_widget.hide()

    def on_publish_down_page_pushButton_clicked(self):
        current_index=self.publish_work_tabWidget.currentIndex()
        self.publish_work_tabWidget.setCurrentIndex(current_index+1)

    def on_publish_up_page_pushButton_clicked(self):
        current_index=self.publish_work_tabWidget.currentIndex()
        self.publish_work_tabWidget.setCurrentIndex(current_index-1)

    def if_all_check(self,current_index):
        if not current_index:
            return True
        for index in range(current_index):
            if not self.check_res_info[self.check_group_list[index]]:
                return False
        return True

    def on_publish_all_check_pushButton_clicked(self):
        current_index = self.publish_work_tabWidget.currentIndex()
        if self.if_all_check(current_index):
            if tool_in_app=="nuke":
                print ""
            else:
                print ""
        else:
            if tool_in_app=="nuke":
                print ""
            else:
                print
            return
        current_tab_name=self.check_group_list[current_index]
        current_check=True
        for check_item in self.check_groupcheck_item[current_tab_name]:
            self.class_item=self.all_check_lib[current_tab_name][check_item]["class"]
            res=self.class_item.run_check()
            if not res:
                current_check=False
                self.check_res_info[current_tab_name]=current_check
                return False
            QtCore.QCoreApplication.processEvents()
        self.check_res_info[current_tab_name]=current_check
        print self.check_res_info

    def on_Treewidget_drop(self):
        pass

if __name__=="__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = Response()
    ui.show()
    sys.exit(app.exec_())
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import maya.cmds as cmds
from publish.ui.head import *
import publish.env.Config as Config
import publish.icon.check_label as check_label
reload(check_label)
reload(Config)
def import_module(name):
    module = __import__(name)
    for mod in name.split(".")[1:]:
        module = getattr(module,mod)
    return module

class qtread(QThread):

    def __init__(self,fun_class,args,parent = None):
        super(qtread,self).__init__(parent)

        self.fun_class = fun_class
        self.args = args

    def run(self):
        self.fun_class(self.args)

class check_widget(QWidget):

    def __init__(self,info_widget,module_step,tab_name,check_type,check_name,allow_skip,cous_info={},publish_widget=None):
        super (check_widget, self).__init__ ()

        self.ct_task_name=cous_info.get("ct_step","")
        self.task_combobox = cous_info.get('task_combobox','')
        self.pub_info=cous_info.get("pubinfo",'')

        self.tab_name=tab_name
        self.moudle_type = check_type
        self.moudle_name = check_name
        self.moudle_step = module_step

        #print "publish." + module_step + '.' + check_type + '.' + check_name
        check_moudle = import_module("publish."+module_step+'.'+check_type+'.'+check_name)

        reload(check_moudle)

        self.check = check_moudle.master_check()
        self.check.task_combobox=self.task_combobox
        self.check.cous_info=cous_info
        self.check.pub_info=self.pub_info
        self.check.get_version_info_fun=self.get_version_info
        self.check.get_task_info_fun=self.get_task_info

        self.check.pub_info.publish_file_path=''
        self.check.pub_info.version_num=''
        self.check.pub_info.right_publish_floder=''
        self.check.pub_info.publish_floder_nv=''
        self.check.pub_info.material_name_dict={}
        self.check.parent_win=self
        self.check.write_info=self.write_info
        self.check.qtread=qtread
        self.check.publish_widget=publish_widget

        self.info_widget = info_widget
        self.check_name = self.check.get_check_name()
        self.description = self.check.get_description()
        self.allow_skip = {'true':True,'false':False}[allow_skip]
        self.auto_fix = self.check.get_auto_fix()

        self.setupUI()
        self.setupConnections()

    def setupUI(self):
        self.mainHboxLayout = QHBoxLayout(self)
        self.skip_label = QLabel(u'check')
        self.check_label = QLabel()
        self.check_ok = QPixmap(r'%s'%(os.path.join(os.path.dirname(__file__).replace("core","icon"),"yes.png")))
        self.check_no = QPixmap(r'%s'%(os.path.join(os.path.dirname(__file__).replace("core","icon"),"no.png")))
        self.skip_checkbox = QCheckBox()
        self.skip_checkbox.setCheckState(Qt.Checked)
        if not self.allow_skip:
            self.skip_checkbox.setEnabled(False)
        self.check_button = QPushButton()
        self.check_button.setMinimumWidth(200)
        self.check_button.setText(self.check_name)

        if self.moudle_step=="publish_processes" and Config.Config.DEBUG=="pub":
            self.check_button.setEnabled(False)

        self.fix_button = QPushButton()
        self.fix_button.setText(u'repair')
        self.fix_button.setEnabled(True)

        spacerItem=QSpacerItem(100,20,QSizePolicy.Minimum,QSizePolicy.Expanding)

        self.descipt_button = QPushButton()
        self.descipt_button.setText(u'?')
        self.mainHboxLayout.addWidget(self.check_label)
        self.mainHboxLayout.addItem(spacerItem)
        self.mainHboxLayout.addWidget(self.check_button)
        self.mainHboxLayout.addWidget(self.descipt_button)
        self.mainHboxLayout.addWidget (self.fix_button)
        self.mainHboxLayout.addWidget (self.skip_label)
        self.mainHboxLayout.addWidget (self.skip_checkbox)

        self.mainHboxLayout.setContentsMargins(0,0,0,0)
        if not self.auto_fix:
            self.fix_button.setEnabled(False)
        self.setContentsMargins(0,0,0,0)

    def get_task_info(self):
        self.check.project_shot_path = self.check.pub_info.project_shot_path
        self.check.project_asset_pub_path=self.check.pub_info.project_asset_pub_path
        self.check.project_asset_work_path=self.check.pub_info.project_asset_work_path
        self.check.sn_name=cmds.file(q=True,sn=True)
        self.check.file_name=os.path.basename(self.check.sn_name)
        self.check.ct_task_name=self.check.pub_info.current_task
        self.check.asset_name=os.path.basename(self.check.sn_name).split("_")[0]+"_"+os.path.basename(self.check.sn_name).split("_")[1]
        self.check.ct_step=self.check.pub_info.ct_step
        self.check.shot_asset_name=self.check.pub_info.shot_asset_name
        #self.check.project_shot_path=self.check.pub_info.project_shot_path
        self.check.version_num=self.check.pub_info.version_num

    def get_version_info(self):
        import datetime
        import getpass
        self.check.version_pub_info_path=self.check.pub_info.version_pub_info_path
        self.check.version_folder_name=os.path.basename(os.path.dirname(self.check.sn_name))

        publish_info_tex=self.check.publish_info_plainTextEdit.publish_info.toPlainText()
        publish_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        right_publish_floder=self.check.pub_info.right_publish_floder
        user_name=getpass.getuser()
        task_name=self.check.ct_task_name
        shot_asset=self.check.shot_asset_name
        version_name=self.check.version_folder_name
        version_info={}
        version_info["user_name"]=user_name
        version_info["task_name"]=task_name
        version_info["version_name"]=version_name
        version_info["pub_folder_path"]=right_publish_floder
        version_info["shot_asset"]=shot_asset
        version_info["publish_info"]=publish_info_tex
        version_info["publist_time"]=publish_time
        version_info["material_name_dict"]=self.check.pub_info.material_name_dict
        version_st="\n"+str(version_info)

        each_version_pub_info_path=os.path.join(right_publish_floder,version_name)

        file_st=open(each_version_pub_info_path,"w")
        file_st.write(version_st)
        file_st.close()

        file_st=open(self.check.version_pub_info_path,"a")
        file_st.write(version_st)
        file_st.close()

        pub_version_list_folder=os.path.join(os.path.dirname(self.check.version_pub_info_path),"pub_version_list")
        if not os.path.exists(pub_version_list_folder):
            os.makedirs(pub_version_list_folder)
        pub_version_list_file_path=os.path.join(pub_version_list_folder,version_name)
        file_st=open(pub_version_list_file_path,"w")
        file_st.write(str(version_info))
        file_st.close()

        self.check.pub_info.version_info=version_info

    def setupConnections(self):
        self.check_button.clicked.connect(self.run_check)
        if self.auto_fix:
            self.fix_button.clicked.connect(self.run_fix)
        self.descipt_button.clicked.connect(self.show_dedcription)

    def write_info(self,info_str):
        old_text=self.info_widget.toPlainText()
        info_str=old_text+info_str
        self.info_widget.setText(info_str)

    def get_skip(self):
        if self.skip_checkbox.checkState().name == "Checked":
            self.skip_check=1
        else:
            self.skip_check=0

    def run_check(self):
        self.get_skip()
        if not self.skip_check:
            return True
        t = time.time()
        result = self.check.do_check()
        print 'result is '+result
        if result == '':
            self.valid=True
            self.check_button.setStyleSheet('QPushButton {color: rgb(10,180,100)}')
            self.check_label.setPixmap(self.check_ok)
            self.write_info(self.moudle_name+u" inspection passed\n")
            return True
        else:
            self.valid = False
            self.check_button.setStyleSheet ('QPushButton {color: rgb(255,140,140)}')
            self.check_label.setPixmap (self.check_no)
            if isinstance(result,str):
                result=result.decode('utf-8')
            else:
                pass
            if self.auto_fix:
                self.fix_button.setEnabled(True)
            self.write_info(result+"\n"+self.moudle_name+u"Check the problem,Please inform TD\n")
            return False

    def run_fix(self):
        result = self.check.do_fix ()
        if result == '':
            print "Automatic repair completed"
        else:
            print "Not possible to fix"
        self.fix_button.setEnabled(False)
        return

    def show_dedcription(self):
        QMessageBox.about(self,u'description',self.moudle_type+'.'+self.moudle_name+'.'+self.description)
        return

    def clear_result(self):
        self.label.setText("")

    def get_module_name(self):
        return self.moudle_name

    def get_valid(self):
        return self.valid

    def get_output(self):
        return self.check.get_output()

    def get_skip_check(self):
        return self.skip_checkbox.checkState()

    def enable(self):
        if self.allow_skip:
            self.skip_checkbox.setEnabled(True)

        self.check_button.setEnabled(True)
        self.check_button.setStyleSheet('QPushButton {color: rgb(200,280,200)}')

        if self.auto_fix:
            self.fix_button.setEnabled(False)

        self.descipt_button.setEnabled(True)
        return

    def disable(self):
        self.skip_checkbox.setEnabled(False)

        self.check_button.setEnabled(False)
        self.check_button.setStyleSheet('QPushButton {color: rgb(140,140,140)}')

        if self.auto_fix:
            self.fix_button.setEnabled(False)

        self.descipt_button.setEnabled(False)


if __name__ == "__main__":
    import sys

    app=QApplication(sys.argv)
    info_widget=QWidget()
    tab_name="tab_name"
    check_type="gen"
    check_name="version_name"
    allow_skip="true"
    module_step="publish_check"
    ui=check_widget(info_widget,module_step,tab_name,check_type,check_name,allow_skip)
    ui.show()
    sys.exit(app.exec_())
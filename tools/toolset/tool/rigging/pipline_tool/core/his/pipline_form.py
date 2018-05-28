# -*- coding: utf-8 -*-

import os
import sys
import functools
import glob
import re
import shutil
import logging
from customize.maya_customize import maya_customize
from rigging.pipline_tool.ui.head import *
from rigging.pipline_tool.ui.ui_main_window import ui_main_window
from rigging.pipline_tool.ui.ui_reference_window import ui_reference_window
from rigging.pipline_tool.env.Config import Config

try:
    import pymel.core as pm
    import maya.cmds as cmds
    import maya.OpenMaya as OpenMaya
except:
    pass

class asset_create_widget(QtGui.QDialog):

    def __init__(self,parent = None):
        super(asset_create_widget,self).__init__(parent)

        #self.locl_work_path = ''

        self.setObjectName("asset_create_Form")
        self.verticalLayout = QtGui.QVBoxLayout(self)

        self.horizontalLayout = QtGui.QHBoxLayout()

        self.label = QtGui.QLabel(self)
        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QtGui.QLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout_2 = QtGui.QHBoxLayout()

        self.pushButton = QtGui.QPushButton()
        self.pushButton_apply = QtGui.QPushButton ()
        self.pushButton_close = QtGui.QPushButton ()
        self.verticalLayout_2.addWidget(self.pushButton)
        self.verticalLayout_2.addWidget (self.pushButton_apply)
        self.verticalLayout_2.addWidget (self.pushButton_close)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.setWindowTitle(QtGui.QApplication.translate("asset_create", "asset_create", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("asset_create", "name:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("asset_create", "create", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_apply.setText(QtGui.QApplication.translate ("asset_create", "apply", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_close.setText(QtGui.QApplication.translate ("asset_create", "close", None, QtGui.QApplication.UnicodeUTF8))

class customize_widget(QtGui.QWidget):

    def __init__(self,listwidget,menu,parent = None):
        super(customize_widget,self).__init__(parent)

        self.project_path = Config.PROJECT_LOCAL_WORK_PATH

        self.character_prop = ''
        self.character_type = ''
        self.listwidget = listwidget
        #self.menu = menu

        self.maya_func = maya_customize()

        layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)

        self.pushbutton = QtGui.QPushButton(u"apply")
        self.pushbutton_version = QtGui.QPushButton (u"save version")

        self.label = QtGui.QLabel()

        self.combox_bf = QtGui.QComboBox()
        self.combox_bf.addItem('body')
        self.combox_bf.addItem ('facial')
        #self.combox_bf.hide()

        self.combox_step = QtGui.QComboBox()
        self.combox_step.addItem('model')
        self.combox_step.addItem ('template')
        self.combox_step.addItem ('set')
        self.combox_step.addItem ('rig')
        self.combox_step.addItem ('import')

        self.combox_type = QtGui.QComboBox()
        self.combox_type.addItem('open')
        self.combox_type.addItem ('reference')
        self.combox_type.addItem ('import')

        layout.addWidget (self.label)
        #layout.addWidget (self.combox_bf)
        layout.addWidget (self.combox_step)
        layout.addWidget (self.combox_type)
        layout.addWidget(self.pushbutton)
        layout.addWidget (self.pushbutton_version)
        self.setLayout(layout)

        self.setupconnection()

    def setupconnection(self):
        self.pushbutton.clicked.connect (lambda : self.openfile(self.project_path))
        #self.menu.triggered.connect (lambda: self.show_in_explorer(self.project_path))

    def openfile(self,path):
        folder_name = self.label.text()
        folder_combox_bf = self.combox_bf.currentText ()
        folder_step = self.combox_step.currentText ()
        folder_path = os.path.join (path, self.character_prop,self.character_type,folder_name,folder_step, folder_name + "_rig.ma")
        print folder_path
        file_type = self.combox_type.currentText ()
        if file_type == "open":
            is_edit = cmds.file(q=1,mf=1)
            if is_edit:
                reply = QtGui.QMessageBox.question (self, 'Save Changes', '',
                                                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes:
                    file_current = cmds.file(q=1,sceneName=1)
                    self.savafile(file_current)
                else:
                    pass
            self.maya_func.openFile(folder_path)
        elif file_type == "import":
            self.maya_func.importFile(folder_path)
        elif file_type == "reference":
            self.maya_func.referenceFile (folder_path)

    def savafile(self,save_path):
        if os.path.exists(save_path):
            cmds.file(rename = save_path)
            current_file = cmds.file(force=1,save=1,type = "mayaAscii",options ="v=0" )
            return current_file

    def show_in_explorer (self, path):
        '''select_delList = []
        for id in self.listwidget.selectedIndexes ():
            select_delList.append (str (self.listwidget.item (id.row ()).text ()))
        folder_step = self.combox_step.currentText ()
        print select_delList
        for floder in select_delList:
            currentpath = os.path.join (path, floder,folder_step)
            #print path,floder,folder_step
            if os.path.isdir(currentpath):
                os.startfile (os.path.dirname (currentpath))
        #print "show ...%s...%s"%(folder_step,currentpath)'''
        folder_name = self.label.text ()
        folder_step = self.combox_step.currentText ()
        currentpath = os.path.join(path,self.character_prop,self.character_type,folder_name,folder_step)
        print currentpath
        if os.path.isdir (currentpath):
            os.startfile (os.path.dirname (currentpath))

    def delete_current_asset (self, delDir):
        ''' delete_current_asset '''
        select_delList = []
        for id in self.listwidget.selectedIndexes ():
            select_delList.append (str (self.listwidget.item (id.row ()).text ()))
        print select_delList
        if select_delList:
            reply = QtGui.QMessageBox.question (self, 'delete', 'You sure to delete?',
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                for del_sel in select_delList:
                    delList = os.listdir (delDir)

                    for f in delList:
                        filePath = os.path.join (delDir, f)
                        if os.path.isfile (filePath):
                            os.remove (filePath)
                            # print filePath + " was removed!"
                        elif os.path.isdir (filePath):
                            shutil.rmtree (filePath, True)
                            # print "Directory: " + filePath + " was removed!"
                if select_delList:
                    self.update_characterprops_items ()
            else:
                pass

#from PySide import QtGui,QtCore
class From(QtGui.QMainWindow):

    def __init__(self,parent = None):
        super(From,self).__init__(parent)
        self._plugins_path = []
        self.item_list = []
        self.item_data = {}
        self.info_list = []
        self.cmd = None
        self.steps = ["model","template","set","rig","import"]

        self.ui_asset_create = asset_create_widget (self)

        self.setWindowTitle ("rigging_pipline_tool")
        self.setupUI()
        self.getElems()
        self.setDefault()
        self.connections()
        self.set_StyleSheet()

        self.update_characterprops_items()

    def setupUI (self):
        self.ui_main_window = ui_main_window ()
        self.setCentralWidget (self.ui_main_window)

        self.ui_reference_dialog = ui_reference_window(self)

    def ShowReferenceRigWin(self):
        self.ui_reference_dialog.showUI()

    def ShowCharacterWin(self):
        try:
            self.ui_asset_create.close()
        except:
            pass
        self.ui_asset_create.show()

    def getElems(self):
        self.createasset_pushButton = self.ui_main_window.ui_piplinetool_widget.main_Widget.createasset_pushButton

        self.characterprops_comboBox = self.ui_main_window.ui_piplinetool_widget.main_Widget.characterprops_comboBox
        self.charcter_type_comboBox = self.ui_main_window.ui_piplinetool_widget.main_Widget.charcter_type_comboBox
        self.characterprops_lineEdit = self.ui_main_window.ui_piplinetool_widget.main_Widget.characterprops_lineEdit
        self.characterprops_update_pushButton = self.ui_main_window.ui_piplinetool_widget.main_Widget.characterprops_update_pushButton
        self.characterprops_listWidget = self.ui_main_window.ui_piplinetool_widget.main_Widget.characterprops_listWidget
        self.characterprops_pushButton = self.ui_main_window.ui_piplinetool_widget.main_Widget.characterprops_pushButton

        self.Reference_pipline_pushButton = self.ui_main_window.ui_piplinetool_widget.main_Widget.Reference_pipline_pushButton

    def setDefault(self):
        self.project_asset_work_path = Config.PROJECT_ASSET_RIG_WORK_PATH
        self.project_local_work_path = Config.PROJECT_LOCAL_WORK_PATH

        self.characterprops_listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.characterprops_listWidget.customContextMenuRequested.connect(self.showContextMenu)

        self.contextMenu = QtGui.QMenu(self.characterprops_listWidget)
        self.deleteaction = self.contextMenu.addAction("delete")
        contextaction = self.contextMenu.addSeparator()
        self.showinexplorer = self.contextMenu.addAction ("show in explorer")

        self.deleteaction.triggered.connect(lambda :self.delete_current_asset(self.assert_path))
        self.showinexplorer.triggered.connect (lambda: self.customize_widget.show_in_explorer(self.assert_path))

    def connections(self):
        #self.gotofile_pushButton.clicked.connect(self.gotofile)
        self.createasset_pushButton.clicked.connect(self.create_asset_work)
        self.characterprops_update_pushButton.clicked.connect (self.update_characterprops_items)
        self.Reference_pipline_pushButton.clicked.connect (self.ShowReferenceRigWin)

        self.characterprops_comboBox.currentIndexChanged [unicode].connect (self.get_characterprops_combobox)
        self.characterprops_pushButton.clicked.connect(self.ShowCharacterWin)

        self.ui_asset_create.pushButton.clicked.connect (lambda :self.create_asset_character("true"))
        self.ui_asset_create.pushButton_apply.clicked.connect (lambda: self.create_asset_character ("default"))
        self.ui_asset_create.pushButton_close.clicked.connect (lambda: self.create_asset_character ("false"))

    def set_StyleSheet(self):
        self.setStyleSheet ('QMainWindow{background-color:rgb(50,50,50)}'
                            'QPushButton{background-color:rgb(70,70,70)}'
                            #'QFrame{background-color:rgb(0,0,0)}'
                            #'QTextBrowser{background-color:rgb(0,0,0)}'
                            #'QComboBox{background-color:rgb(31,31,31)'
                            )

    def get_characterprops_combobox(self):
        self.getcurrenttext()
        self.update_characterprops_items()

    def get_current_characterprops_combobox(self,current):
        self.current_characterprops_item_sel = self.characterprops_listWidget.currentItem ()
        if self.current_assettype_item_sel:
            self.current_assettype_item = self.current_assettype_item_sel.text()
        self.update_version_items()

    def create_asset_character(self,uiclose='default'):
        if uiclose == "default":
            self._create_asset_character()
        elif uiclose == "true":
            self._create_asset_character()
            try:
                self.ui_asset_create.close ()
            except:
                pass
        elif uiclose == "false":
            try:
                self.ui_asset_create.close ()
            except:
                pass

    def _create_asset_character(self):
        if os.path.exists (self.assert_path):
            character_name = self.ui_asset_create.lineEdit.text()
            sever_path_models = os.listdir(Config.PROJECT_ASSET_SEVER_PATH)
            if not character_name in sever_path_models:
                logging.error ("have not character exists!!!")
                return
            if os.path.isfile (self.assert_path+"/"+character_name):
                logging.warning("file is exists!!!")
                return
            else:
                self.copyfile(Config.PROJECT_ASSET_BASE_PATH,self.assert_path+"/"+character_name)
                self.replaceDirName(self.assert_path,"example",character_name)
                self.replaceFileName(self.assert_path,"example",character_name+"_rig")

                sever_model_file = self.get_sever_model(character_name)
                print sever_model_file
                #local_model_file = self.assert_path+"\\"+character_name+"\\"+"model"+"\\"+character_name+"_rig.ma"
                #shutil.copyfile(sever_model_file[0],local_model_file)
                if sever_model_file:
                    for step in self.steps:
                        self.update_local_rigfile(self.assert_path,character_name,sever_model_file[0],step)
                else:
                    logging.error("have not asset file %s !!!"%(sever_model_file))

                self.update_characterprops_items()
        else:
            print "local work path is not exsits!!!"
            logging.error("local work path is not exsits!!!")

    def get_work_severpath_folder(self,path,scencename,filetype):
        rig_work_path = os.path.join(path,scencename,filetype)
        if os.path.exists(rig_work_path):
            all_version = [i.split('.v') for i in glob.glob(rig_work_path+"\\his\\*rig.v*")]
            print all_version
            if all_version:
                all_version.sort()
                version_num_str = "v" +str(int(all_version[-1])+1).zfill(3)
                work_folder = scencename + '.' + filetype + '.' + 'rigging' + '.' + version_num_str
                return work_folder
            else:
                work_folder = scencename + '.' + filetype + '.' + "rigging.v001"
                return work_folder

    def get_wrok_folder(self,path,scencename,filetype):
        work_folder = self.get_work_severpath_folder(path,scencename,filetype)
        rig_work_severpath = os.path.join(path,scencename,filetype,work_folder)
        if not os.path.exists(rig_work_severpath):
            os.makedirs(rig_work_severpath)
            file(r"%s/%s"%(rig_work_severpath,work_folder),"w")
            print "%s/%s 文件已创建" % (rig_work_severpath,work_folder)
        return rig_work_severpath

    def get_sever_model(self,scencename):
        model_file=[]
        print Config.PROJECT_ASSET_SEVER_PATH+"\\"+scencename
        if os.path.exists(Config.PROJECT_ASSET_SEVER_PATH+"\\"+scencename):
            model_file = glob.glob (Config.PROJECT_ASSET_SEVER_PATH+"\\"+scencename+"\\"+"model"+"\\"+"*.ma")
        #print model_file
        return model_file

    def replaceFileName(self,rootDir, oldStr, newStr):
        for dirpath, dirNames, fileNames in os.walk(rootDir):
            for fileName in fileNames:
                if oldStr in fileName:
                    fileNameOld = os.path.join(dirpath, fileName)
                    fileNameNew = os.path.join(dirpath,fileName.replace(oldStr, newStr))
                    #print(fileNameOld + ' --> '+ fileName)
                    os.renames(fileNameOld, fileNameNew)

    def replaceDirName(self,rootDir, oldStr, newStr):
        for dirpath, dirNames, fileNames in os.walk(rootDir, topdown = False):
            for dirName in dirNames:
                if oldStr in dirName:
                    dirNameOld = os.path.join(dirpath,dirName)
                    dirNameNew = os.path.join(dirpath,dirName.replace(oldStr,newStr))
                    #print(dirNameOld + ' --> '+ dirNameNew)
                    #os.rename(dirNameOld, dirNameNew)
                    #print dirNameOld, dirNameNew

    def update_local_rigfile(self,localpath,character_name,severpath,step="model"):
        local_path = os.path.join (localpath, character_name, step, character_name + "_rig.ma")
        local_model_file = os.path.join(localpath,character_name,"model",character_name+"_rig.ma")
        local_set_file = os.path.join (localpath, character_name, "set", character_name + "_rig.ma")
        if step == "model":
            shutil.copyfile (severpath, local_model_file)
        elif step == "template":
            ref_local_path = self.get_baserig_path (local_path)
            if len(ref_local_path) != 1:
                logging.error ("path not exsits or path is wrong!!!")
                return False
            self.replace_path(local_path,ref_local_path[0],local_model_file.replace("\\","/"))
        elif step == "set":
            pass
        elif step == "rig":
            ref_local_path = self.get_baserig_path(local_path)
            if len(ref_local_path) != 2:
                logging.error ("path not exsits or path is wrong!!!")
                return False
            self.replace_path(local_path,ref_local_path[0],local_model_file.replace("\\","/"))
            self.replace_path(local_path,ref_local_path[1],local_set_file.replace("\\","/"))
        elif step == "import":
            pass

    def update_characterprops_items(self):
        self.characterprops_listWidget.clear ()
        #self.customize_widget = customize_widget (self.characterprops_listWidget, self.contextMenu)
        self.getcurrenttext()
        folder_list = list()
        self.assert_path = os.path.join(self.project_local_work_path,self.characterprops,self.charactertype)
        if os.path.exists(self.assert_path):
            #print self.assert_path
            #self.ui_asset_create.locl_work_path = self.assert_path
            folder_list = os.listdir(self.assert_path)
        #else:
        #    print "path not exsits!!!"
        if folder_list:
            folder_list.sort()
            self.connection_dict = {}
            #connectionwidgets_list = []
            #widget_dict = {}
            for foler in folder_list:
                connection_list = []
                item = QtGui.QListWidgetItem()
                self.customize_widget = customize_widget (self.characterprops_listWidget, self.contextMenu)
                widget = self.customize_widget
                #connectionwidgets_list.append(widget)
                #widget_dict[widget] = index
                widget.character_prop = self.characterprops
                widget.character_type = self.charactertype
                #widget_dict [widget.pushbutton] = widget
                widget.label.setText(foler)
                #step_text = widget.combox_step.currentText()
                #type_combox = widget.combox_type
                #widget.pushbutton.clicked.connect (lambda : self.test(widget))
                #foler_path = os.path.join(assert_path,foler,step_text,foler+"_rig")
                connection_list = [widget.label,widget.combox_step,widget.combox_type]
                self.connection_dict[widget] = connection_list
                self.characterprops_listWidget.addItem (item)
                self.characterprops_listWidget.setItemWidget(item,widget)

    def delete_current_asset(self,delDir):
        select_delList = []
        for id in self.characterprops_listWidget.selectedIndexes():
            select_delList.append(str(self.characterprops_listWidget.item(id.row()).text()))
        print select_delList
        if select_delList:
            reply = QtGui.QMessageBox.question (self, 'delete', 'You sure to delete?',
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                for del_sel in select_delList:
                    delList = os.listdir (delDir)

                    for f in delList:
                        filePath = os.path.join (delDir, f)
                        if os.path.isfile (filePath):
                            os.remove (filePath)
                            #print filePath + " was removed!"
                        elif os.path.isdir (filePath):
                            shutil.rmtree (filePath, True)
                        #print "Directory: " + filePath + " was removed!"
                if select_delList:
                    self.update_characterprops_items ()
            else:
                pass

    def getcurrenttext(self):
        self.characterprops = self.characterprops_comboBox.currentText()
        self.charactertype = self.charcter_type_comboBox.currentText()

    def importReference(self):
        ref_cls = maya_customize()
        refNodes = ref_cls.get_RefereceNodes()
        mFile = OpenMaya.MFileIO()
        for i in range (refNodes.length ()):
            ref_filename = mFile.getReferenceFileByNode(refNodes[i])
            cmds.file(ref_filename,importReference=1)

    def create_asset_work(self):
        print Config.PROJECT_ASSET_WORK_PATH,Config.PROJECT_LOCAL_WORK_PATH
        self.copyfile(Config.PROJECT_ASSET_WORK_PATH,Config.PROJECT_LOCAL_WORK_PATH)

    def get_path(self):
        re_srcpath = re.compile('file -rdi 1 -ns ".+?" -rfn (".+?RN"[\s\S]+?"P:.+?\.ma");')
        re_srcpath = re.compile('-rfn (".+?RN"[\s\S]+?"P:.+?\.ma");')


        repInfo = []
        with open(filepath,'r') as f:
            try:
                srcRefInfoList = re_srcpath.findall(f.read())
            except:
                return False
            repInfo = [[x,x.replace(refpath,filepath)] for x in srcRefInfoList]

        if not repInfo:
            return False
        else:
            srcFile = open(filepath,'r')
            try:
                srcDataTmp = srcFile.read()
            except:
                return False

    def get_baserig_path(self,filepath):
        ref = re.compile('file -rdi 1 -ns (".+?")[\s\S]+?-rfn (".+?")[\s\S]+?(".+?");')
        refpath = []
        with open(filepath,"r") as f:
            try:
                refList = ref.findall(f.read())
                #print refList[0][2]
                refpath = [i[2] for i in refList]
            except:
                return False
        return refpath

    def replace_path(self,filepath,localpath,severpath):
        srcFile = open(filepath,"r")
        try:
            srcDataTmp = srcFile.read()
            srcFile.close()
        except:
            logging.error("file read faild!!!")
            return False
        srcDataTmp = srcDataTmp.replace(localpath,'"%s"'%(severpath))

        dstFile = open(filepath,"w")
        dstFile.write(srcDataTmp)
        dstFile.close()
        return filepath

    def copyfile(self,severDir,  localDir):
        if not os.path.exists (localDir):
            shutil.copytree(severDir,localDir)
            print "copy %s file"%(localDir)
        else:
            print "copy %s file is already exsits!!!"%(localDir)

    def showContextMenu(self):
        self.contextMenu.move(QtGui.QCursor.pos())
        self.contextMenu.show()

if __name__=="__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = From()
    ui.showWinodow()
    sys.exit(app.exec_())
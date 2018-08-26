# -*- coding: utf-8 -*-

from .head import *
import os
import shutil

class Menu_ListWidget(QtWidgets.QListWidget):

    def __init__(self,parent = None):
        super(Menu_ListWidget,self).__init__(parent)

    def contextMenuEvent(self,event):
        popMenu = QtWidgets.QMenu(self)
        action = QtWidgets.QAction(QtWidgets.QIcon(""),"delete",self)

        if self.itemAt(self.mapFromGlobal(QtWidgets.QCursor.pos())):
            popMenu.addAction(action)
        popMenu.exec_(QtWidgets.QCursor.pos())

    def delete_current_asset(self,delDir):
        select_delList = []
        for id in self.selectedIndexes():
            select_delList.append(str(self.item(id.row()).text()))
        for del_sel in select_delList:
            delList = os.listdir (delDir)

            for f in delList:
                filePath = os.path.join (delDir, f)
                if os.path.isfile (filePath):
                    os.remove (filePath)
                    print filePath + " was removed!"
                elif os.path.isdir (filePath):
                    shutil.rmtree (filePath, True)
                print "Directory: " + filePath + " was removed!"
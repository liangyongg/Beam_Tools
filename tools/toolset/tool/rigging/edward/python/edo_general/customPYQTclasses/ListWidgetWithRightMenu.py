from headfile import *

class ListWidgetWithRightMenu(QtGui.QListWidget):
    def contextMenuEvent(self,QContextMenuEvent):
        #print 'aaa'
        #addQMenu
        self.rightmenu=QtGui.QMenu(self)
        #self.rightmenu.addAction('normal')
        #self.rightmenu.addAction('blocked')
        #self.rightmenu.addAction('invisible')
        #self.rightmenu.addAction('cache')
        self.rightmenu.exec_(QtGui.QCursor.pos())
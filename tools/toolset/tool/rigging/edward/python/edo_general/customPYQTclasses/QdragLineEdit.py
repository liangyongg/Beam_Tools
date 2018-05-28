from headfile import *

class QdragLineEdit(QtGui.QLabel):
    changed = QtCore.pyqtSignal(QtCore.QMimeData)
    def __init__(self, parent = None):
        super(QdragLineEdit, self).__init__(parent)
        #self.setMinimumSize(361, 240)
        #self.setAlignment(QtCore.Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.setAutoFillBackground(True)
        
    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        print 'dragEnter...........'

    def dropEvent(self, event):
        mimeData = event.mimeData()
        print 'drop..............'
        if mimeData.hasUrls():
            path = ''
            for url in mimeData.urls():
                print url.toLocalFile()
                path=path+url.toLocalFile()+'\n'
            self.setText(path)   
        else:
            self.setText("Cannot display data")


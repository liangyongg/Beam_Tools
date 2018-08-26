
from rigging.beam.ui.Qt import QtWidgets, QtGui, QtCore

class BeamUI(QtWidgets.QWidget):
    """A debugger widget hosting an inspector as well as a graph view"""

    def __init__(self, parent=None):

        # constructors of base classes
        super(BeamUI, self).__init__(parent)
        self.setObjectName('mainUI')
        self.setWindowIcon(QtGui.QIcon(''))

        self.setWindowTitle("Beam Editor")
        self.setAcceptDrops(True)
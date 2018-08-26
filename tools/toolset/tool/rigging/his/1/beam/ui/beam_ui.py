from rigging.beam.core.beam_system import BeamSystem
from rigging.beam.ui.Qt import QtWidgets, QtGui, QtCore
import rigging.beam.ui.GraphView.kgraph_view_widget
reload(rigging.beam.ui.GraphView.kgraph_view_widget)
from rigging.beam.ui.GraphView.kgraph_view_widget import KGraphViewWidget
import rigging.beam.ui.component_library
reload(rigging.beam.ui.component_library)
from rigging.beam.ui.component_library import ComponentLibrary

class BeamUI(QtWidgets.QWidget):
    """A debugger widget hosting an inspector as well as a graph view"""

    def __init__(self, parent=None):

        # constructors of base classes
        super(BeamUI, self).__init__(parent)
        self.setObjectName('mainUI')
        self.setWindowIcon(QtGui.QIcon(''))

        self.setWindowTitle("Beam Editor")
        self.setAcceptDrops(True)

        self.graphViewWidget = KGraphViewWidget (parent = self)
        self.nodeLibrary = ComponentLibrary (parent = self)

        self.horizontalSplitter = QtWidgets.QSplitter (QtCore.Qt.Horizontal, parent = self)
        self.horizontalSplitter.addWidget (self.nodeLibrary)
        self.horizontalSplitter.addWidget (self.graphViewWidget)

        self.horizontalSplitter.setStretchFactor(0, 0)
        self.horizontalSplitter.setStretchFactor(1, 1)
        self.horizontalSplitter.setSizes([0, 100])
        self.horizontalSplitter.splitterMoved.connect(self.splitterMoved)
        self.nodeLibraryExpandedSize = 175

        grid = QtWidgets.QVBoxLayout (self)
        grid.addWidget (self.horizontalSplitter)

    def showEvent(self, event):

        beamSystem = BeamSystem.getInstance()

    def splitterMoved(self, pos, index):
        self.nodeLibraryExpandedSize = pos
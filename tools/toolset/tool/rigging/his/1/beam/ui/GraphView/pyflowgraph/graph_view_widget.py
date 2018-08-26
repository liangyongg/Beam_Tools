
import sys
from rigging.beam.ui.Qt import QtWidgets, QtGui, QtCore

from graph_view import GraphView

class GraphViewWidget(QtWidgets.QWidget):

    rigNameChanged = QtCore.Signal ()

    def __init__(self, parent=None):

        # constructors of base classes
        super(GraphViewWidget, self).__init__(parent)
        self.openedFile = None
        self.setObjectName('graphViewWidget')
        self.setAttribute(QtCore.Qt.WA_WindowPropagation, True)


    def setGraphView(self, graphView):
        self.graphView = graphView

        # Setup Layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.graphView)
        self.setLayout(layout)

        #########################
        ## Setup hotkeys for the following actions.
        deleteShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Delete), self)
        deleteShortcut.activated.connect(self.graphView.deleteSelectedNodes)

        frameShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F), self)
        frameShortcut.activated.connect(self.graphView.frameSelectedNodes)

        frameShortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_A), self)
        frameShortcut.activated.connect(self.graphView.frameAllNodes)

    def getGraphView(self):
        return self.graphView

#print __name__
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = GraphViewWidget()
    graph = GraphView(parent=widget)

    widget.setGraphView (graph)

    widget.show ()
    print __file__,"GraphViewWidget"
    sys.exit (app.exec_ ())
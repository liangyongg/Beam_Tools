
from rigging.beam.ui.Qt import QtWidgets, QtGui, QtCore
from rigging.beam.core.beam_system import BeamSystem

class BeamMenu(QtWidgets.QWidget):
    """Beam Menu Widget"""

    def __init__ (self, parent = None):
        super (BeamMenu, self).__init__ (parent)

        self.setObjectName ('menuWidget')

        self.createLayout ()
        self.createConnections ()

    def createLayout (self):
        self.menuLayout = QtWidgets.QHBoxLayout ()
        self.menuLayout.setContentsMargins (0, 0, 0, 0)
        self.menuLayout.setSpacing (0)

        # Menu
        self.menuBar = QtWidgets.QMenuBar()

        # File Menu
        self.fileMenu = self.menuBar.addMenu ('&File')
        self.newAction = self.fileMenu.addAction('&New')
        self.newAction.setShortcut('Ctrl+N')
        self.newAction.setObjectName("newAction")

        # Edit Menu
        self.editMenu = self.menuBar.addMenu ('&Edit')

        # Build Menu
        self.buildMenu = self.menuBar.addMenu('&Build')
        self.buildGuideAction = self.buildMenu.addAction('Build &Guide')
        self.buildGuideAction.setShortcut('Ctrl+G')
        self.buildGuideAction.setObjectName("buildGuideAction")

        self.buildRigAction = self.buildMenu.addAction('Build &Rig')
        self.buildRigAction.setShortcut('Ctrl+B')
        self.buildRigAction.setObjectName("buildRigAction")

        # Config Widget
        self.configsParent = QtWidgets.QFrame(self)
        self.configsParent.setObjectName('configParent')
        self.configsParent.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.configsParent.setMinimumWidth(160)

        self.configsLayout = QtWidgets.QVBoxLayout()
        self.configsLayout.setContentsMargins(0, 0, 0, 0)
        self.configsLayout.setSpacing(0)

        self.configsWidget = QtWidgets.QComboBox ()
        self.configsWidget.setAutoFillBackground(True)
        self.configsWidget.setObjectName('configWidget')
        self.configsWidget.setMinimumWidth(160)
        self.configsWidget.addItem('Default Config', userData='Default Config')

        self.configsLayout.addWidget (self.configsWidget)
        self.configsParent.setLayout (self.configsLayout)

        configs = BeamSystem.getInstance ().getConfigClassNames ()
        for config in configs:
            self.configsWidget.addItem(config.split('.')[-1], userData=config)

        self.rigNameLabel = RigNameLabel ('Rig Name:')

        self.menuLayout.addWidget (self.menuBar, 3)
        self.menuLayout.addWidget (self.configsParent, 0)
        self.setLayout (self.menuLayout)

    def createConnections(self):
        beamUIWidget = self.parentWidget().getBeamUI()
        graphViewWidget = beamUIWidget.graphViewWidget

        # File Menu Connections
        self.newAction.triggered.connect(graphViewWidget.newRigPreset)
        self.newAction.triggered.connect(self.updateRigNameLabel)

        # Build Menu Connections
        self.buildGuideAction.triggered.connect(graphViewWidget.buildGuideRig)
        self.buildRigAction.triggered.connect(graphViewWidget.buildRig)

    # =======
    # Events
    # =======
    def updateRigNameLabel(self):
        krakenUIWidget = self.window().getBeamUI()

        graphViewWidget = krakenUIWidget.graphViewWidget
        newRigName = graphViewWidget.guideRig.getName()

        self.rigNameLabel.setText('Rig Name: ' + newRigName)

class RigNameLabel(QtWidgets.QLabel):

    clicked = QtCore.Signal()

    def __init__(self, parent=None):
        super(RigNameLabel, self).__init__(parent)
        self.setObjectName('rigNameLabel')
        self.setToolTip('Double Click to Edit')

    def mouseDoubleClickEvent(self, event):
        self.clicked.emit()
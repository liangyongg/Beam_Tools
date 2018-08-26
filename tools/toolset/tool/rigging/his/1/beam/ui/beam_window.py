
from rigging.beam.ui.Qt import QtWidgets, QtGui, QtCore
import rigging.beam.ui.beam_ui
reload(rigging.beam.ui.beam_ui)
from rigging.beam.ui.beam_ui import BeamUI
import rigging.beam.ui.beam_menu
reload(rigging.beam.ui.beam_menu)
from rigging.beam.ui.preferences import Preferences
from rigging.beam.ui.beam_menu import BeamMenu

class BeamWindow(QtWidgets.QMainWindow):
    """Main Beam Window that loads the UI."""

    def __init__ (self, parent = None):
        super (BeamWindow, self).__init__ (parent)
        self.setObjectName ('BeamMainWindow')
        self.setWindowTitle ('Beam Editor')
        self.setWindowIcon (QtGui.QIcon (''))
        self.setAttribute (QtCore.Qt.WA_DeleteOnClose)
        self.installEventFilter (self)

        self.preferences = Preferences ()

        self.createLayout()
        self.createConnections()

    def createLayout (self):
        mainWidget = QtWidgets.QWidget ()

        # Main Layout
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.beamUI = BeamUI(self)
        self.beamMenu = BeamMenu (self)

        self.mainLayout.addWidget (self.beamMenu)
        self.mainLayout.addWidget (self.beamUI, 1)
        mainWidget.setLayout (self.mainLayout)
        self.setCentralWidget (mainWidget)

    def createConnections(self):
        pass

    def getBeamUI(self):
        return self.beamUI
import os
import sys
from rigging.beam.ui.Qt import QtWidgets, QtGui, QtCore
#import rigging.beam.core.beam_system
#reload(rigging.beam.core.beam_system)
from rigging.beam.core.beam_system import BeamSystem

class ComponentTreeWidget(QtWidgets.QTreeWidget):
    """Component Tree Widget"""

    def __init__(self, parent):
        super(ComponentTreeWidget, self).__init__(parent)

        self.setObjectName('ComponentTree')
        self.header().close()
        self.setColumnCount(1)
        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QTreeWidget.DragOnly)

        beamUIWidget = self.parent ().parent ()
        graphViewWidget = beamUIWidget.graphViewWidget
        beamUIWidget.error_loading_startup = False

        if not self.generateData ():
            beamUIWidget.error_loading_startup = True
            # Wait until right after the window is displayed for the first time to call reportMessage

        self.buildWidgets ()

    def buildWidgets(self):
        self.clear()
        self.__iterateOnData(self._data, parentWidget=self)

    def __iterateOnData (self, data, parentWidget = None):
        print "ComponentTreeWidget.__iterateOnData"
        print "ComponentTreeWidget.__iterateOnData.%s" %data
        for item in sorted (data ['components']):
            if data ['components'] [item] not in self.bs.registeredComponents.keys ():
                print (
                "Warning: Component module " + data ['components'] [item] + " not found in registered components:")
                for component in self.bs.registeredComponents:
                    print "  " + component
                continue

            treeItem = QtWidgets.QTreeWidgetItem (parentWidget)
            treeItem.setData (0, QtCore.Qt.UserRole, data ['components'] [item])
            treeItem.setText (0, item)
            component = self.bs.registeredComponents [data ['components'] [item]]
            module = sys.modules [component.__module__]
            treeItem.setToolTip (0, module.__file__)

            if parentWidget is not None:
                parentWidget.setToolTip (0, os.path.dirname (module.__file__))

        for item in data ['subDirs'].keys ():
            treeItem = QtWidgets.QTreeWidgetItem (parentWidget)
            treeItem.setData (0, QtCore.Qt.UserRole, 'Folder')
            treeItem.setText (0, item)

            self.__iterateOnData (data ['subDirs'] [item], parentWidget = treeItem)

    def generateData (self):
        print "ComponentTreeWidget.generateData"
        self.bs = BeamSystem.getInstance ()

        isSuccessful = self.bs.loadComponentModules ()
        print self.bs.getComponentClassNames ()
        print "isSuccessful ",isSuccessful
        componentClassNames = []
        for componentClassName in sorted (self.bs.getComponentClassNames ()):
            cmpCls = self.bs.getComponentClass (componentClassName)
            if cmpCls.getComponentType () != 'Guide':
                continue

            componentClassNames.append (componentClassName)

        print "generateData", componentClassNames

        self._data = {'subDirs': {}, 'components': {}}

        for classItem in componentClassNames:
            nameSplit = classItem.rsplit('.', 1)

            className = nameSplit[-1]
            path = nameSplit[0].split('.')
            path.pop(len(path) - 1)

            parent = None
            for i, part in enumerate(path):

                if i == 0:
                    if part not in self._data['subDirs'].keys():
                        self._data['subDirs'][part] = {'subDirs': {}, 'components': {}}

                    parent = self._data['subDirs'][part]

                    continue

                if part in parent['subDirs'].keys():
                        parent = parent['subDirs'][part]
                        continue

                parent['subDirs'][part] = {'subDirs': {}, 'components': {}}
                parent = parent['subDirs'][part]

            parent['components'][className] = classItem
        print self._data
        return isSuccessful

    def mouseMoveEvent(self, event):
        self.dragObject()

    def dragObject(self):

        if not self.selectedIndexes():
            return

        item = self.selectedItems()[0]
        role = item.data(0, QtCore.Qt.UserRole)

        if role == 'Folder':
            return

        text = 'BeamComponent:' + role

        mimeData = QtCore.QMimeData()
        mimeData.setText(text)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(QtCore.QPoint(90, 23))

        ghostComponent = QtGui.QPixmap(180, 46)
        #ghostComponent.fill(QtGui.QColor(67, 143, 153, 80))
        ghostComponent.fill (QtGui.QColor (255, 255, 255, 255))

        drag.setPixmap(ghostComponent)
        drag.start(QtCore.Qt.IgnoreAction)

class ComponentLibrary(QtWidgets.QWidget):

    def __init__(self, parent):
        super(ComponentLibrary, self).__init__(parent)

        self.setMinimumWidth(175)

        self.componentTreeWidget = ComponentTreeWidget(self)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.componentTreeWidget, 0, 0)
        self.setLayout(grid)
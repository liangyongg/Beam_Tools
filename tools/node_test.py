from rigging.beam.ui.Qt import QtWidgets, QtGui, QtCore
from rigging.beam.ui.GraphView.pyflowgraph.port import InputPort, OutputPort, IOPort


class KNodeInputPort(InputPort):

    def __init__(self, parent, graph, componentInput):

        name = "input_name"
        dataType = componentInput.getDataType()
        color = getPortColor(dataType)

        super(KNodeInputPort, self).__init__(parent, graph, name, color, dataType)

        self.componentInput = componentInput

    def setCircle(self):
        self.setInCircle(KNodePortCircle(self, self.getGraph(), -2, self.getColor(), 'In'))

    def setLabel(self):
        self.setLabelItem(PortLabel(self, self.getName(), -10, self._labelColor, self._labelHighlightColor))

    def getComponentInput(self):
        return self.componentInput

class NodeTitle (QtWidgets.QGraphicsWidget):
    __color = QtGui.QColor (25, 25, 25)
    __font = QtGui.QFont ('Decorative', 14)
    __font.setLetterSpacing (QtGui.QFont.PercentageSpacing, 115)
    __labelBottomSpacing = 12

    def __init__ (self, text, parent = None):
        super (NodeTitle, self).__init__ (parent)

        self.setSizePolicy (QtWidgets.QSizePolicy (QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))

        self.__textItem = QtWidgets.QGraphicsTextItem (text, self)
        self.__textItem.setDefaultTextColor (self.__color)
        self.__textItem.setFont (self.__font)
        self.__textItem.setPos (0, -2)
        option = self.__textItem.document ().defaultTextOption ()
        option.setWrapMode (QtGui.QTextOption.NoWrap)
        self.__textItem.document ().setDefaultTextOption (option)
        self.__textItem.adjustSize ()

        self.setPreferredSize (self.textSize ())

    def setText (self, text):
        self.__textItem.setPlainText (text)
        self.__textItem.adjustSize ()
        self.setPreferredSize (self.textSize ())

    def textSize (self):
        return QtCore.QSizeF (
            self.__textItem.textWidth (),
            self.__font.pointSizeF () + self.__labelBottomSpacing
        )

class PortList(QtWidgets.QGraphicsWidget):

    def __init__(self, parent):
        super(PortList, self).__init__(parent)
        layout = QtWidgets.QGraphicsLinearLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.setOrientation(QtCore.Qt.Vertical)
        self.setLayout(layout)

    def addPort(self, port, alignment):
        layout = self.layout()
        layout.addItem(port)
        layout.setAlignment(port, alignment)
        self.adjustSize()
        return port

class NodeHeader (QtWidgets.QGraphicsWidget):
    def __init__ (self, text, parent = None):
        super (NodeHeader, self).__init__ (parent)

        self.setSizePolicy (QtWidgets.QSizePolicy (QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

        layout = QtWidgets.QGraphicsLinearLayout ()
        layout.setContentsMargins (0, 0, 0, 0)
        layout.setSpacing (3)
        layout.setOrientation (QtCore.Qt.Horizontal)
        self.setLayout (layout)

        self._titleWidget = NodeTitle (text, self)
        layout.addItem (self._titleWidget)
        layout.setAlignment (self._titleWidget, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)

    def setText (self, text):
        self._titleWidget.setText (text)

class Node (QtWidgets.QGraphicsWidget):
    nameChanged = QtCore.Signal (str, str)

    __defaultColor = QtGui.QColor (154, 205, 50, 255)
    __defaultUnselectedColor = QtGui.QColor (25, 25, 25)
    __defaultSelectedColor = QtGui.QColor (255, 255, 255, 255)

    __defaultUnselectedPen = QtGui.QPen (__defaultUnselectedColor, 1.6)
    __defaultSelectedPen = QtGui.QPen (__defaultSelectedColor, 1.6)
    __defaultLinePen = QtGui.QPen (QtGui.QColor (25, 25, 25, 255), 1.25)

    def __init__ (self):
        super (Node, self).__init__ ()

        self.__color = self.__defaultColor
        self.__unselectedColor = self.__defaultUnselectedColor
        self.__selectedColor = self.__defaultSelectedColor

        self.__unselectedPen = QtGui.QPen (self.__defaultUnselectedPen)
        self.__selectedPen = QtGui.QPen (self.__defaultSelectedPen)
        self.__linePen = QtGui.QPen (self.__defaultLinePen)

        self.setMinimumWidth (60)
        self.setMinimumHeight (20)
        self.setSizePolicy (QtWidgets.QSizePolicy (QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

        layout = QtWidgets.QGraphicsLinearLayout ()
        layout.setContentsMargins (0, 0, 0, 0)
        layout.setSpacing (0)
        layout.setOrientation (QtCore.Qt.Vertical)
        self.setLayout (layout)

        self.__headerItem = NodeHeader ("xxx", self)
        layout.addItem (self.__headerItem)
        layout.setAlignment (self.__headerItem, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)

        self.__ports = []
        self.__inputPortsHolder = PortList (self)
        self.__ioPortsHolder = PortList (self)
        self.__outputPortsHolder = PortList (self)

        layout.addItem (self.__inputPortsHolder)
        layout.addItem (self.__ioPortsHolder)
        layout.addItem (self.__outputPortsHolder)

        self.__selected = False
        self.__dragging = False

    def addPort(self, port):
        if isinstance(port, InputPort):
            self.__inputPortsHolder.addPort(port, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        elif isinstance(port, OutputPort):
            self.__outputPortsHolder.addPort(port, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        else:
            self.__ioPortsHolder.addPort(port, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.__ports.append(port)

        self.adjustSize()
        return port


class KNode (Node):
    def __init__ (self):
        super (KNode, self).__init__ ()

        self.addPort()


class GraphView (QtWidgets.QGraphicsView):
    nodeAdded = QtCore.Signal (Node)

    def __init__ (self, parent = None):
        super (GraphView, self).__init__ (parent)

        self.setObjectName ('graphView')
        self.setRenderHint (QtGui.QPainter.Antialiasing)
        self.setRenderHint (QtGui.QPainter.TextAntialiasing)

        self.setHorizontalScrollBarPolicy (QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy (QtCore.Qt.ScrollBarAlwaysOff)

        size = QtCore.QSize (600, 400)
        self.resize (size)
        self.setSceneRect (-size.width () * 0.5, -size.height () * 0.5, size.width (), size.height ())
        self.setAcceptDrops (True)
        self.reset()

    def reset(self):
        self.setScene(QtWidgets.QGraphicsScene())

    def addNode (self, node, emitSignal = True):
        self.scene ().addItem (node)

        if emitSignal:
            self.nodeAdded.emit (node)

        return node

class KGraphView (GraphView):

    def __init__(self, parent=None):
        super(KGraphView, self).__init__(parent)

        self.setAcceptDrops(True)

        node = KNode ()
        self.addNode (node)

class BeamUI(QtWidgets.QWidget):
    def __init__(self, parent=None):

        super(BeamUI, self).__init__(parent)
        self.setObjectName('mainUI')
        self.setWindowIcon(QtGui.QIcon(''))

        self.setWindowTitle("Beam Editor")
        self.setAcceptDrops(True)

        layout = QtWidgets.QVBoxLayout (self)

        self.graphViewWidget = KGraphView (parent = self)
        layout.addWidget(self.graphViewWidget)
        self.setLayout(layout)
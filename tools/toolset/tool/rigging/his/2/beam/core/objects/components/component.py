from rigging.beam.core.objects.object_3d import Object3D
from rigging.beam.core.maths import *

class Component(Object3D):
    """Kraken Component object."""

    def __init__(self, name, parent=None, location='M', metaData=None):
        super (Component, self).__init__ (name, parent, metaData = metaData)
        self._color = (154, 205, 50, 255)
        self._inputs = []
        self._outputs = []

        self._graphPos = Vec2 ()

    # ==============
    # Class Methods
    # ==============
    @classmethod
    def getComponentType(cls):
        return 'Base'

    def setGraphPos (self, graphPos):
        self._graphPos = graphPos
        return True

    def getNumInputs(self):
        return len(self._inputs)

    def getNumOutputs(self):
        return len(self._outputs)

    def getComponentColor(self):
        return self._color

    # =============
    # Graph UI
    # =============
    def getGraphPos(self):
        return self._graphPos

from rigging.beam.core.objects.object_3d import Object3D


class ComponentOutput(Object3D):
    """ComponentOutput object."""

    def __init__(self, name, parent=None, metaData=None):
        super(ComponentOutput, self).__init__(name, parent=parent, metaData=metaData)
        self.setShapeVisibility(False)
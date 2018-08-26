
from rigging.beam.core.objects.object_3d import Object3D


class ComponentInput(Object3D):
    """ComponentInput object."""

    def __init__(self, name, parent=None, metaData=None):
        super(ComponentInput, self).__init__(name, parent=parent, metaData=metaData)
        self.setShapeVisibility(False)
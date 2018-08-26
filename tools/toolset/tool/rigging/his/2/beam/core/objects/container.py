from collections import OrderedDict

from rigging.beam.core.objects.object_3d import Object3D
from rigging.beam.core.objects.components.base_example_component import BaseExampleComponent

# Note: does a container need to inherit off 'Object3D'?
# These items exist only to structure a rig as a graph.
# The never get built.
class Container(Object3D):
    """Container object."""

    def __init__(self, name, metaData=None):
        super(Container, self).__init__(name, None, metaData=metaData)
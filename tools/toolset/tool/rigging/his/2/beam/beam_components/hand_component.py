from collections import OrderedDict
from rigging.beam.core.profiler import Profiler
from rigging.beam.core.objects.components.base_example_component import BaseExampleComponent

class HandComponent(BaseExampleComponent):
    """Hand Component Base"""

    def __init__(self, name='hand', parent=None, *args, **kwargs):
        super(HandComponent, self).__init__(name, parent, *args, **kwargs)

class HandComponentGuide(HandComponent):
    """Hand Component Guide"""

    def __init__(self, name='hand', parent=None, *args, **kwargs):
        Profiler.getInstance ().push ("Construct Arm Guide Component:" + name)
        super(HandComponentGuide, self).__init__(name, parent, *args, **kwargs)

        Profiler.getInstance().pop()

    @classmethod
    def getComponentType(cls):
        return 'Guide'

    @classmethod
    def getRigComponentClass(cls):
        return HandComponentRig

class HandComponentRig(HandComponent):
    """Hand Component"""

    def __init__(self, name='Hand', parent=None):
        super(HandComponentRig, self).__init__(name, parent)

from rigging.beam.core.beam_system import BeamSystem
bs = BeamSystem.getInstance()
bs.registerComponent(HandComponentGuide)
bs.registerComponent(HandComponentRig)
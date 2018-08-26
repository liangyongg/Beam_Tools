from container import Container

class Rig(Container):
    """Rig object."""

    def __init__(self, name='rig', metaData=None):
        super(Rig, self).__init__(name, metaData=metaData)
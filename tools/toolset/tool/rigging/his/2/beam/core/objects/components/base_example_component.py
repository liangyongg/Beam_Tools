from rigging.beam.core.objects.components.component import Component

class BaseExampleComponent(Component):
    """Example Component Base"""

    def __init__(self, name='', parent=None, metaData=None, *args, **kwargs):
        super(BaseExampleComponent, self).__init__(name, parent, metaData=metaData, *args, **kwargs)
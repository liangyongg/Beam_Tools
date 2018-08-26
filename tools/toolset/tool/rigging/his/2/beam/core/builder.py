class Builder(object):

    def __init__(self, debugMode=False):
        super(Builder, self).__init__()
        self._buildElements = []

    def build (self, kSceneItem):
        print kSceneItem.getName()

    def deleteBuildElements(self):
        return None
"""
Classes:
Builder -- Base builder object to build objects in DCC.

"""
"""Builder - 基础构建器对象在DCC中构建对象。"""
import os
import logging
from rigging.beam.core.configs.config import Config
from rigging.beam.core.profiler import Profiler
from rigging.beam.core.traverser import Traverser

class Builder(object):

    def __init__(self, debugMode=False):
        super(Builder, self).__init__()

        self.config = Config.getInstance ()

    def build(self, kSceneItem):
        """Builds a rig object.

        We have to re-order component children by walking the graph to ensure
        that inputs objects are in place for the dependent components.

        Args:
            kSceneItem (sceneitem): The item to be built.

        Returns:
            object: DCC Scene Item that is created.

        """

        try:
            self._preBuild(kSceneItem)
        finally:
            self._postBuild(kSceneItem)
        return


    # ==============
    # Build Methods
    # ==============
    def _preBuild(self, kSceneItem):
        """Protected Pre-Build method.

        Args:
            kSceneItem (object): kraken kSceneItem object to build.

        Returns:
            bool: True if successful.

        """

        return True

    def _postBuild(self, kSceneItem):
        """Protected Post-Build method.

        Args:
            kSceneItem (object): kraken kSceneItem object to run post-build
                operations on.

        Returns:
            bool: True if successful.

        """
        return True

    # =====================
    # Build Object Methods
    # =====================
    def __buildSceneItem(self, kObject, phase):
        """Builds the DCC sceneitem for the supplied kObject.

        Args:
            kObject (object): kraken object to build.
            phase (type): Description.

        Returns:
            object: DCC object that was created.

        """
        # Build Object

    def __buildSceneItemList(self, kObjects, phase):
        """Builds the provided list of objects.

        Args:
            kObjects (list): Objects to be built.
            phase (int): Description.

        Returns:
            Type: True if successful.

        """
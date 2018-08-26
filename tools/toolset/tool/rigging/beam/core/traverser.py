from rigging.beam.core.objects.scence_item import SceneItem
from rigging.beam.core.objects.object_3d import Object3D

class Traverser(object):
    """base traverser for any scene item.

    The traverser iterates through all root items and determines the
    dependencies between objects, building an ordered list as it goes. This
    order is then used by the builder to ensure that objects are created and
    evaluated in the correct order. Offset's will then be reliable.

    """

    def __init__(self, name='Traverser'):
        self._rootItems = []
        self.reset()

    # =============
    # Traverse Methods
    # =============
    def reset(self):
        """Resets all internal structures of this Traverser."""

        self._visited = {}
        self._items = []

    def addRootItem(self, item):
        """Adds a new root object to this Traverser

        Args:
            item (SceneItem): The SceneItem to add as a root item.

        Returns:
            bool: True if successful.

        """

        for rootItem in self._rootItems:
            if rootItem.getId() == item.getId():
                return False

        self._rootItems.append(item)

        return True

    def traverse(self, itemCallback=None, discoverCallback=None,
                 discoveredItemsFirst=True):
        """Visits all objects within this Traverser based on the root items.

        Args:
            itemCallback (func): A callback function to be invoked for each
                item visited.
            discoverCallback (func): A callback to return an array of children
                for each item.

        """

        self.reset()

    def __visitItem (self, item, itemCallback, discoverCallback, discoveredItemsFirst):
        """Doc String.

        Args:
            item (Type): information.
            itemCallback (Type): information.
            discoverCallback (Type): information.
            discoveredItemsFirst (Type): information.

        Returns:
            Type: information.

        """

        return True
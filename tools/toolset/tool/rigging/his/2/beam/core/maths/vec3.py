
import math
from rigging.beam.core.beam_system import bs
from math_object import MathObject


class Vec3(MathObject):
    """Vector 3 object."""

    def __init__(self, x=0.0, y=0.0, z=0.0):
        """Initializes x, y, z values for Vec3 object."""
        super (Vec3, self).__init__ ()

        self.x=x
        self.y=y
        self.z=z
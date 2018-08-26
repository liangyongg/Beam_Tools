
import math
from rigging.beam.core.beam_system import bs
from math_object import MathObject


class Vec2(MathObject):
    """Vector 2 object."""

    def __init__(self, x=0.0, y=0.0):
        """Initializes x, y values for Vec2 object."""

        super(Vec2, self).__init__()
        self.x = x
        self.y = y
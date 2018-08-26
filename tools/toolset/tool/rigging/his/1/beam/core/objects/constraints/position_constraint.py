
from constraint import Constraint
from rigging.beam.core.maths.vec3 import Vec3


class PositionConstraint(Constraint):
    """Position Constraint."""

    def __init__(self, name, metaData=None):
        super(PositionConstraint, self).__init__(name, metaData=metaData)


from constraint import Constraint
from rigging.beam.core.maths.vec3 import Vec3
from rigging.beam.core.maths.quat import Quat


class OrientationConstraint(Constraint):
    """Orientation Constraint."""

    def __init__(self, name, metaData=None):
        super(OrientationConstraint, self).__init__(name, metaData=metaData)

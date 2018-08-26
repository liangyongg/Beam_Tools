
from constraint import Constraint
from rigging.beam.core.maths.xfo import Xfo
from rigging.beam.core.maths.vec3 import Vec3
from rigging.beam.core.maths.quat import Quat


class PoseConstraint(Constraint):
    """Pose Constraint."""

    def __init__(self, name, metaData=None):
        super(PoseConstraint, self).__init__(name, metaData=metaData)


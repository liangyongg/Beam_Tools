
from constraint import Constraint


class ScaleConstraint(Constraint):
    """Scale Constraint."""

    def __init__(self, name, metaData=None):
        super(ScaleConstraint, self).__init__(name, metaData=metaData)

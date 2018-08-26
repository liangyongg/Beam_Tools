import pymel.core as pm
from pymel.core import datatypes

from rigging.beam.core.shifter import beam_components

from rigging.beam.core import node, fcurve, applyop, vector, icon,attribute, transform, primitive


class Component(beam_components.Main):
    """Shifter component Class"""
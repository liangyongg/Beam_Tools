
#import rigging.beam.core.objects.components.base_example_component
#reload(rigging.beam.core.objects.components.base_example_component)
from rigging.beam.core.objects.components.base_example_component import BaseExampleComponent
from rigging.beam.core.profiler import Profiler

class ArmComponent(BaseExampleComponent):
    """Arm Component Base"""

    def __init__(self, name='arm', parent=None, *args, **kwargs):
        super(ArmComponent, self).__init__(name, parent, *args, **kwargs)

        self.globalSRTInputTgt = self.createInput('globalSRT', dataType='Xfo', parent=self.inputHrcGrp).getTarget()
        self.rootInputTgt = self.createInput('root', dataType='Xfo', parent=self.inputHrcGrp).getTarget()

        # Declare Output Xfos
        self.bicepOutputTgt = self.createOutput('bicep', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.elbowOutputTgt = self.createOutput('elbow', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.forearmOutputTgt = self.createOutput('forearm', dataType='Xfo', parent=self.outputHrcGrp).getTarget()
        self.wristOutputTgt = self.createOutput('wrist', dataType='Xfo', parent=self.outputHrcGrp).getTarget()

        # Declare Input Attrs
        self.drawDebugInputAttr = self.createInput('drawDebug', dataType='Boolean', parent=self.cmpInputAttrGrp).getTarget()
        self.rigScaleInputAttr = self.createInput('rigScale', dataType='Float', value=1.0, parent=self.cmpInputAttrGrp).getTarget()
        self.rightSideInputAttr = self.createInput('rightSide', dataType='Boolean', parent=self.cmpInputAttrGrp).getTarget()

        # Declare Output Attrs
        self.drawDebugOutputAttr = self.createOutput('drawDebug', dataType='Boolean', value=False, parent=self.cmpOutputAttrGrp).getTarget()
        self.ikBlendOutputAttr = self.createOutput('ikBlend', dataType='Float', value=0.0, parent=self.cmpOutputAttrGrp).getTarget()


class ArmComponentGuide(ArmComponent):
    """Arm Component Guide"""

    def __init__(self, name='arm', parent=None, *args, **kwargs):
        Profiler.getInstance().push("Construct Arm Guide Component:" + name)
        super(ArmComponentGuide, self).__init__(name, parent, *args, **kwargs)

    @classmethod
    def getComponentType(cls):
        return 'Guide'

    @classmethod
    def getRigComponentClass(cls):
        return ArmComponentRig

class ArmComponentRig(ArmComponent):
    """Arm Component Rig"""

    def __init__(self, name='arm', parent=None):

        Profiler.getInstance().push("Construct Arm Rig Component:" + name)
        super(ArmComponentRig, self).__init__(name, parent)

#import rigging.beam.core.beam_system
#reload(rigging.beam.core.beam_system)
from rigging.beam.core.beam_system import BeamSystem
bs = BeamSystem.getInstance()
bs.registerComponent(ArmComponentGuide)
bs.registerComponent(ArmComponentRig)
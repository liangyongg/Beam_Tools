
#import rigging.beam.core.objects.components.base_example_component
#reload(rigging.beam.core.objects.components.base_example_component)
from rigging.beam.core.objects.components.base_example_component import BaseExampleComponent
from rigging.beam.core.profiler import Profiler
from rigging.beam.core.objects.attributes.attribute_group import AttributeGroup
from rigging.beam.core.objects.attributes.bool_attribute import BoolAttribute
from rigging.beam.core.objects.attributes.scalar_attribute import ScalarAttribute

from rigging.beam.core.objects.component_group import ComponentGroup
from rigging.beam.core.objects.transform import Transform
from rigging.beam.core.objects.joint import Joint
from rigging.beam.core.objects.ctrlSpace import CtrlSpace
from rigging.beam.core.objects.control import Control

from rigging.beam.core.maths import Vec3
from rigging.beam.core.maths.xfo import Xfo
from rigging.beam.core.maths.xfo import xfoFromDirAndUpV
#from rigging.beam.core.objects.operators.kl_operator import KLOperator

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

        # ===========
        # Attributes
        # ===========
        # Add Component Params to IK control
        guideSettingsAttrGrp = AttributeGroup("GuideSettings", parent=self)

        self.bicepFKCtrlSizeInputAttr = ScalarAttribute('bicepFKCtrlSize', value=1.75, minValue=0.0, maxValue=10.0, parent=guideSettingsAttrGrp)
        self.forearmFKCtrlSizeInputAttr = ScalarAttribute('forearmFKCtrlSize', value=1.5, minValue=0.0, maxValue=10.0, parent=guideSettingsAttrGrp)

        # =========
        # Controls
        # =========
        # Guide Controls
        self.bicepCtrl = Control('bicep', parent=self.ctrlCmpGrp, shape="sphere")
        self.bicepCtrl.setColor('blue')
        self.forearmCtrl = Control('forearm', parent=self.ctrlCmpGrp, shape="sphere")
        self.forearmCtrl.setColor('blue')
        self.wristCtrl = Control('wrist', parent=self.ctrlCmpGrp, shape="sphere")
        self.wristCtrl.setColor('blue')

        armGuideSettingsAttrGrp = AttributeGroup("DisplayInfo_ArmSettings", parent=self.bicepCtrl)
        self.armGuideDebugAttr = BoolAttribute('drawDebug', value=True, parent=armGuideSettingsAttrGrp)

        self.guideOpHost = Transform('guideOpHost', self.ctrlCmpGrp)

        # Guide Operator
        #self.armGuideKLOp = KLOperator('guide', 'TwoBoneIKGuideSolver', 'Beam')
        #self.addOperator(self.armGuideKLOp)

        # Add Att Inputs
        #self.armGuideKLOp.setInput('drawDebug', self.armGuideDebugAttr)
        #self.armGuideKLOp.setInput('rigScale', self.rigScaleInputAttr)

        # Add Source Inputs
        #self.armGuideKLOp.setInput('root', self.bicepCtrl)
        #self.armGuideKLOp.setInput('mid', self.forearmCtrl)
        #self.armGuideKLOp.setInput('end', self.wristCtrl)

        # Add Target Outputs
        #self.armGuideKLOp.setOutput('guideOpHost', self.guideOpHost)

        self.default_data = {
            "name": name,
            "location": "L",
            "bicepXfo": Xfo(Vec3(2.275, 15.3, -0.75)),
            "forearmXfo": Xfo(Vec3(5.0, 13.5, -0.75)),
            "wristXfo": Xfo(Vec3(7.2, 12.25, 0.5)),
            "bicepFKCtrlSize": self.bicepFKCtrlSizeInputAttr.getValue(),
            "forearmFKCtrlSize": self.forearmFKCtrlSizeInputAttr.getValue()
        }

        self.loadData(self.default_data)

        Profiler.getInstance().pop()

        # =============
        # Data Methods
        # =============

    def saveData (self):
        """Save the data for the component to be persisted.


        Return:
        The JSON data object

        """

        data = super (ArmComponentGuide, self).saveData ()

        data ['bicepXfo'] = self.bicepCtrl.xfo
        data ['forearmXfo'] = self.forearmCtrl.xfo
        data ['wristXfo'] = self.wristCtrl.xfo

        return data

    def loadData (self, data):
        """Load a saved guide representation from persisted data.

        Arguments:
        data -- object, The JSON data object.

        Return:
        True if successful.

        """

        super (ArmComponentGuide, self).loadData (data)

        self.bicepCtrl.xfo = data ['bicepXfo']
        self.forearmCtrl.xfo = data ['forearmXfo']
        self.wristCtrl.xfo = data ['wristXfo']

        #guideOpName = ''.join ([self.getName ().split ('GuideKLOp') [0], self.getLocation (), 'GuideKLOp'])
        #self.armGuideKLOp.setName (guideOpName)

        #self.armGuideKLOp.evaluate ()

        return True

    def getRigBuildData (self):
        """Returns the Guide data used by the Rig Component to define the layout of the final rig..

        Return:
        The JSON rig data object.

        """

        data = super (ArmComponentGuide, self).getRigBuildData ()

        # values
        bicepPosition = self.bicepCtrl.xfo.tr
        forearmPosition = self.forearmCtrl.xfo.tr
        wristPosition = self.wristCtrl.xfo.tr

        # Calculate Bicep Xfo
        rootToWrist = wristPosition.subtract (bicepPosition).unit ()
        rootToElbow = forearmPosition.subtract (bicepPosition).unit ()

        bone1Normal = rootToWrist.cross (rootToElbow).unit ()
        bone1ZAxis = rootToElbow.cross (bone1Normal).unit ()

        bicepXfo = Xfo ()
        bicepXfo.setFromVectors (rootToElbow, bone1Normal, bone1ZAxis, bicepPosition)

        # Calculate Forearm Xfo
        elbowToWrist = wristPosition.subtract (forearmPosition).unit ()
        elbowToRoot = bicepPosition.subtract (forearmPosition).unit ()
        bone2Normal = elbowToRoot.cross (elbowToWrist).unit ()
        bone2ZAxis = elbowToWrist.cross (bone2Normal).unit ()
        forearmXfo = Xfo ()
        forearmXfo.setFromVectors (elbowToWrist, bone2Normal, bone2ZAxis, forearmPosition)

        # Calculate Wrist Xfo
        wristXfo = Xfo ()
        wristXfo.tr = self.wristCtrl.xfo.tr
        wristXfo.ori = forearmXfo.ori

        upVXfo = xfoFromDirAndUpV (bicepPosition, wristPosition, forearmPosition)
        upVXfo.tr = forearmPosition
        upVXfo.tr = upVXfo.transformVector (Vec3 (0, 0, 5))

        # Lengths
        bicepLen = bicepPosition.subtract (forearmPosition).length ()
        forearmLen = forearmPosition.subtract (wristPosition).length ()

        data ['bicepXfo'] = bicepXfo
        data ['forearmXfo'] = forearmXfo
        data ['wristXfo'] = wristXfo
        data ['upVXfo'] = upVXfo
        data ['bicepLen'] = bicepLen
        data ['forearmLen'] = forearmLen

        return data

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
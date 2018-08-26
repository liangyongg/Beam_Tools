import logging
import os
import sys
import json
import importlib
from rigging.beam.core.profiler import Profiler
import rigging.beam.FabricEngine.Core
from rigging.beam.plugins import getFabricClient
from collections import OrderedDict
from rigging.beam.log.utils import fabricCallback

class BeamSystem(object):

    __instance = None

    def __init__(self):

        super(BeamSystem, self).__init__()

        self.client = None
        self.typeDescs = None
        self.registeredTypes = None
        self.loadedExtensions = []

        self.registeredConfigs = OrderedDict()
        self.registeredComponents = OrderedDict()

    def loadCoreClient(self):
        if self.client is None:
            Profiler.getInstance().push("loadCoreClient")

            client = getFabricClient()
            if client is None:
                options = {
                    'reportCallback': fabricCallback,
                    'guarded': True
                }

                client = rigging.beam.FabricEngine.Core.createClient(options)

            self.client = client
            self.loadExtension('Math')
            self.loadExtension('Kraken')
            self.loadExtension('KrakenForCanvas')
            print "loadCoreClient.self.client: ",self.client
            Profiler.getInstance().pop()
        print "loadCoreClient.self.client: ",self.client

    def getCoreClient(self):
        """Returns the Fabric Engine Core Client owned by the KrakenSystem

        Returns:
            object: The Fabric Engine Core Client

        """

        if self.client is None:
            self.loadCoreClient()
        return self.client

    def loadExtension(self, extension):
        """Loads the given extension and updates the registeredTypes cache.

        Args:
            extension (str): The name of the extension to load.

        """

        if extension not in self.loadedExtensions:
            Profiler.getInstance().push("loadExtension:" + extension)
            self.client.loadExtension(extension)
            self.registeredTypes = self.client.RT.types
            self.typeDescs = self.client.RT.getRegisteredTypes()
            # Cache the loaded extension so that we aviod refreshing the typeDescs cache(costly)
            self.loadedExtensions.append(extension)
            Profiler.getInstance().pop()

    def convertFromRTVal(self, target, RTTypeName=None):
        """Generates an RTVal object based on the simple type of target
        and passes target to constructor. Converts a property of an RTVal object
        to its own pytholn RTVal object


        Args:
            target (RTVal): The RTVal object or property to cast
            RTTypeName (str): The type of RTVal to convert to

        Returns:
            RTVal: The RTVal object

        """

        self.loadCoreClient()

        if RTTypeName is None:
            RTTypeName = target.type('String').getSimpleType()
        rtValType = getattr(self.client.RT.types, RTTypeName)
        pythonRTVal = rtValType(target)

        return pythonRTVal

    def constructRTVal(self, dataType, defaultValue=None):
        """Constructs a new RTVal using the given name and optional devault value.

                Args:
                    dataType (str): The name of the data type to construct.
                    defaultValue (value): The default value to use to initialize the RTVal

                Returns:
                    object: The constructed RTval.

                """

        self.loadCoreClient ()
        klType = getattr (self.registeredTypes, dataType)
        print "kraken_system.constructRTVal.registeredTypes: ", self.registeredTypes
        print "kraken_system.constructRTVal.dataType:", dataType
        print "kraken_system.constructRTVal.klType:", klType
        if defaultValue is not None:
            if hasattr (defaultValue, '_rtval'):
                print "kraken_system.constructRTVal.defaultValue._rtval", defaultValue._rtval
                return defaultValue._rtval

            typeDesc = self.typeDescs [dataType]
            if 'members' in typeDesc:
                try:
                    value = klType.create ()
                except:
                    try:
                        return klType ()
                    except Exception as e:
                        raise Exception ("Error constructing RTVal:" + dataType)

                for i in xrange (0, len (typeDesc ['members'])):
                    memberName = typeDesc ['members'] [i] ['name']
                    memberType = typeDesc ['members'] [i] ['type']
                    if memberName in defaultValue:
                        setattr (value, memberName,
                                 self.constructRTVal (memberType, getattr (defaultValue, memberName)))

                return value

            else:
                return klType (defaultValue)
        else:
            try:
                return klType.create ()
            except:
                try:
                    print "kraken_system.constructRTVal.klType():", klType ()
                    return klType ()
                except Exception as e:
                    raise Exception ("Error constructing RTVal:" + dataType)

    def rtVal(self, dataType, defaultValue=None):
        return self.constructRTVal(dataType, defaultValue)

    def isRTVal(self, value):
        return str(type(value)) == "<type 'PyRTValObject'>"

    def getRTValTypeName(self, rtval):
        if bs.isRTVal(rtval):
            return json.loads(rtval.type("Type").jsonDesc("String").getSimpleType())['name']
        else:
            return "None"

    def registerComponent(self, componentClass):
        componentClassPath = componentClass.__module__ + "." + componentClass.__name__
        if componentClassPath in self.registeredComponents:
            # we allow reregistring of components because as a component's class is edited
            # it will be re-imported by python(in Maya), and the classes reregistered.
            pass

        self.registeredComponents[componentClassPath] = componentClass
        print "self.registeredComponents <<<>>> %s"%(self.registeredComponents)

    def getComponentClass(self, className):

        if className not in self.registeredComponents:
            raise Exception("Component with that class not registered:" + className)

        return self.registeredComponents[className]

    def getComponentClassNames(self):

        return self.registeredComponents.keys()

    def getConfigClassNames(self):

        return self.registeredConfigs.keys()

    def loadComponentModules (self):
        for componentClassPath in self.registeredComponents:
            componentModulePath = self.registeredComponents[componentClassPath].__module__
            if componentModulePath in sys.modules:
                del(sys.modules[componentModulePath])

        self.registeredComponents = {}

        def __importDirRecursive (path, parentModulePath = ''):
            isSuccessful = True

            contents = os.listdir (path)
            moduleFilefound = False
            for item in contents:
                if os.path.isfile (os.path.join (path, item)):
                    if item == "__init__.py":
                        if parentModulePath == '':
                            modulePath = os.path.basename (path)
                            moduleParentFolder = os.path.split (path) [0]
                            if moduleParentFolder not in sys.path:
                                sys.path.append (moduleParentFolder)
                        else:
                            modulePath = parentModulePath + '.' + os.path.basename (path)
                        moduleFilefound = True
            if moduleFilefound:
                for i, item in enumerate (contents):
                    if os.path.isfile (os.path.join (path, item)):
                        if item.endswith (".py") and item != "__init__.py":
                            module = modulePath + "." + item [:-3]
                            try:
                                # print module
                                md = importlib.import_module(module)
                                print md
                            except ImportError, e:
                                isSuccessful = False
                                print "__importDirRecursive,ImportError, e"
                            except Exception, e:
                                isSuccessful = False

            for item in contents:
                if os.path.isdir (os.path.join (path, item)):
                    if moduleFilefound:
                        if not __importDirRecursive (os.path.join (path, item), modulePath):
                            isSuccessful = False
                    else:
                        if not __importDirRecursive (os.path.join (path, item)):
                            isSuccessful = False

            return isSuccessful

        #default_component_path = os.path.normpath (os.path.join (os.environ.get ('Beam_PATH'),'kraken_components'))
        default_component_path=os.path.abspath(os.path.join(os.path.dirname(__file__),"..","beam_components"))
        isSuccessful = __importDirRecursive (default_component_path)
        print self.registeredComponents.keys()
        return isSuccessful

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = BeamSystem()

        return cls.__instance

bs = BeamSystem.getInstance()

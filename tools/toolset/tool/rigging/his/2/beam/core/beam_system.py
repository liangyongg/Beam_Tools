import logging
import os
import sys
import json
import importlib
from collections import OrderedDict

class BeamSystem(object):

    __instance = None

    def __init__(self):

        self.registeredConfigs = OrderedDict()
        self.registeredComponents = OrderedDict()

        super(BeamSystem, self).__init__()

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

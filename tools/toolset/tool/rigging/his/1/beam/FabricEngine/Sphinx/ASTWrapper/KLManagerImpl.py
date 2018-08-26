#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#
import os
import re
import fnmatch
import glob
import shutil
from KLExtensionImpl import KLExtension
from KLFileImpl import KLFile
from KLStructImpl import KLStruct
from KLObjectImpl import KLObject
from KLInterfaceImpl import KLInterface

class KLManager(object):

  __instance = None
  
  __header = None
  __klExtensions = None
  __klFiles = None
  __constants = None
  __aliases = None
  __types = None
  __freeFunctions = None
  __unresolvedMethods = []
  __freeFunctionLookup = None
  __typeRefRules = None

  def __init__(self, paths = None, header = None):

    KLManager.__instance = self
    self.__klExtensions = {}
    self.__klFiles = {}
    self.__constants = {}
    self.__aliases = {}
    self.__types = {}
    self.__freeFunctions = {}
    self.__freeFunctionLookup = {}
    self.__header = header
    if self.__header is None:
      self.__header = []
      self.__header += [".. image:: /images/FE_logo_345_60.*"]
      self.__header += ["   :width: 345px"]
      self.__header += ["   :height: 60px"]
      self.__header += [""]
      self.__header += ["| |FABRIC_PRODUCT_NAME| version |FABRIC_VERSION|"]
      self.__header += ["| |FABRIC_COPYRIGHT|"]
    self.__unresolvedMethods = []

    if paths is None:
      paths = [os.environ['FABRIC_EXTS_PATH'].split(os.pathsep)[0]]

    for path in paths:
      for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '*.fpm.json'):
          fullpath = os.path.join(root, filename)
          if self.__klExtensions.has_key(fullpath):
            continue
          if fullpath.find('NoRedist') > -1:
            continue
          if fullpath.find('NoInstaller') > -1:
            continue
          self.__klExtensions[fullpath] = KLExtension(fullpath, self)
          self.__klFiles.update(self.__klExtensions[fullpath]._getKLFilesDict())

    for m in self.__unresolvedMethods:

      thisType = m.getThisType()
      if thisType == None:
        continue

      T = self.getType(thisType)
      if T is None:
        T = KLStruct({'name': thisType, 'members': []})
        T.setExtension(m.getExtension())
        T.setKLFile(m.getKLFile())
        F = self.getKLFile(m.getKLFile())
        if F:
          F._registerType(T)
        self._registerType(T)
        
      elif m.getKLFile() != T.getKLFile():
        F = self.getKLFile(m.getKLFile())
        if F:
          F._registerType(T)

      T._addMethod(m)

  @staticmethod
  def getInstance():
    return KLManager.__instance

  def reportError(self, message):
    print message

  def getKLExtensions(self):
    return self.__klExtensions.values()

  def getKLExtension(self, path):
    for key in self.__klExtensions:
      ext = self.__klExtensions[key]
      if ext.getName() == path:
        return ext
    if self.__klExtensions.has_key(path):
      return self.__klExtensions[path]
    path = os.path.normpath(path)
    if self.__klExtensions.has_key(path):
      return self.__klExtensions[path]
    path = os.path.abspath(path)
    if self.__klExtensions.has_key(path):
      return self.__klExtensions[path]
    return None

  def getKLFiles(self):
    return self.__klFiles.values()

  def getKLFile(self, path):
    if self.__klFiles.has_key(path):
      return self.__klFiles[path]
    path = os.path.normpath(path)
    if self.__klFiles.has_key(path):
      return self.__klFiles[path]
    path = os.path.abspath(path)
    if self.__klFiles.has_key(path):
      return self.__klFiles[path]
    return None

  def _registerConstant(self, decl):
    if self.__constants.has_key(decl.getName()):
      self.reportError('KL Constant "%s" has been declared both two files:\n  %s\n  %s'
        % (decl.getName(), self.__constants[decl.getName()].getKLFile(), decl.getKLFile()))
    self.__constants[decl.getName()] = decl

  def _registerType(self, decl):
    if self.__types.has_key(decl.getName()):
      self.reportError('KL Type "%s" has been declared both two files:\n  %s\n  %s'
        % (decl.getName(), self.__types[decl.getName()].getKLFile(), decl.getKLFile()))
    self.__types[decl.getName()] = decl

  def _registerAlias(self, oldName, newName):
    if self.__aliases.has_key(newName):
      self.reportError('KL Alias "%s" has been declared in two files.' % newName)
    self.__aliases[newName] = oldName

  def _registerFreeFunction(self, decl):
    label = decl.getLabel()
    if self.__freeFunctionLookup.has_key(label):
      f = self.__freeFunctions[self.__freeFunctionLookup[label]]
      self.reportError('KL Function "%s" has been declared in two files.\n  %s\n  %s'
        % (label, f.getKLFile(), decl.getKLFile()))
    self.__freeFunctionLookup[label] = decl.getID()
    self.__freeFunctions[decl.getID()] = decl

  def getConstants(self):
    return self.__constants.values()

  def getConstant(self, key):
    return self.__constants.get(key, None)

  def getAliases(self):
    return self.__aliases

  def getAlias(self, key):
    return self.__aliases.get(key, None)

  def getTypes(self):
    return self.__types.values()

  def getType(self, key):
    return self.__types.get(key, None)

  def getInterfaces(self):
    result = []
    for key in self.__types:
      t = self.__types[key]
      if isinstance(t, KLInterface):
        result.append(t)
    return result

  def getInterface(self, key):
    result = self.__types.get(key, None)
    if not isinstance(result, KLInterface):
      return None
    return result

  def getStructs(self):
    result = []
    for key in self.__types:
      t = self.__types[key]
      if isinstance(t, KLStruct) and not isinstance(t, KLObject):
        result.append(t)
    return result

  def getStruct(self, key):
    result = self.__types.get(key, None)
    if not isinstance(result, KLStruct) or isinstance(result, KLObject):
      return None
    return result

  def getObjects(self):
    result = []
    for key in self.__types:
      t = self.__types[key]
      if isinstance(t, KLObject):
        result.append(t)
    return result

  def getObject(self, key):
    result = self.__types.get(key, None)
    if not isinstance(result, KLObject):
      return None
    return result

  def getFreeFunctions(self):
    return self.__freeFunctions.values()

  def getFreeFunction(self, key):
    result = self.__freeFunctions.get(key, None)
    if result is None:
      for k in self.__freeFunctions:
        if self.__freeFunctions[k].getName() == key:
          result = self.__freeFunctions[k]
          break
    return result

  def insertKLTypeRefs(self, text, useRefs = True):
    if not useRefs:
      return text

    if text.find('`') > -1 or text.find('\\[') > -1:
      return text

    oldtext = text

    if self.__typeRefRules is None:
      self.__typeRefRules = {}
      for key in self.__types:
        self.__typeRefRules[key] = re.compile('\\b%s\\b' % re.escape(key))

    for key in self.__typeRefRules:
      text = self.__typeRefRules[key].sub(':ref:`%s <%s>`' % (key, key.lower()), text)

    text = text.replace('[', '\\[')
    text = text.replace(']', '\\]')

    return text

  def registerUnresolvedMethod(self, method):
    self.__unresolvedMethods.append(method)

  def __writePageIfNeeded(self, content, targetPath):
    newContent = '\n'.join(content)
    oldContent = ''
    if os.path.exists(targetPath):
      oldContent = open(targetPath, 'r').read()
    if newContent != oldContent:
      open(targetPath, 'w').write(newContent)

  def __generateIndexPage(self, extension, targetDir, sourceDir):

    if not os.path.exists(targetDir):
      os.makedirs(targetDir)

    targetPath = os.path.join(targetDir, 'index.rst')
    sourcePath = os.path.join(sourceDir, 'index.rst.template')

    # find other rst files
    otherRstSourceFiles = glob.glob(os.path.join(sourceDir, '*.rst*'))
    otherRstTargetFiles = []
    for otherRstSourceFile in otherRstSourceFiles:
      otherRstFileName = os.path.split(otherRstSourceFile)[1].replace('.template', '')
      if otherRstFileName.lower() == 'index.rst':
        continue
      otherRstTargetFile = os.path.join(targetDir, otherRstFileName)
      if not os.path.exists(targetDir):
        os.makedirs(targetDir)
      shutil.copy(otherRstSourceFile, otherRstTargetFile)
      otherRstTargetFiles += [otherRstTargetFile]
      print 'Copied additional rst file '+otherRstTargetFile

    klFiles = extension.getKLFiles()
    klInterfaces = extension.getKLInterfaces()
    klTypes = extension.getKLTypes()
    klFunctions = extension.getKLFreeFunctions()
    klConstants = extension.getKLConstants()

    paths = []
    content = []
    if os.path.exists(sourcePath):
      content = open(sourcePath, 'r').read().split('\n')
    else:
      content = []
      content += [".. _%s_extension:" % extension.getName().lower()]
      content += [""]
      content += ["%s Extension" % extension.getName()]
      content += ["===================================================================================="]
      content += self.__header
      content += [""]
      content += ["Table of Contents"]
      content += ["-----------------"]
      content += [""]
      content += [".. toctree::"]
      content += ["  :maxdepth: 2"]
      content += ["  "]

      if len(klFiles):
        content += ["  files"]

      if len(klInterfaces):
        content += ["  interfaces"]

      if len(klTypes):
        content += ["  types"]

      if len(klFunctions):
        content += ["  functions"]

      if len(klConstants):
        content += ["  constants"]

      content += [""]
      content += ["Indices and Tables"]
      content += ["------------------"]
      content += [""]
      content += ["* :ref:`genindex`"]
      content += ["* :ref:`search`"]
      content += [""]

    if len(klFiles):
      paths += self.__generateFileListPage(extension, targetDir, sourceDir)
      for klFile in klFiles:
        paths += self.__generateFilePage(extension, klFile, targetDir, sourceDir)

    if len(klInterfaces):
      paths += self.__generateInterfaceListPage(extension, targetDir, sourceDir)
      for interface in klInterfaces:
        paths += self.__generateInterfacePage(extension, interface, targetDir, sourceDir)

    if len(klTypes):
      paths += self.__generateTypeListPage(extension, targetDir, sourceDir)
      for klType in klTypes:
        paths += self.__generateTypePage(extension, klType, targetDir, sourceDir)

    if len(klFunctions):
      paths += self.__generateFreeFunctionListPage(extension, targetDir, sourceDir)

    if len(klConstants):
      paths += self.__generateConstantListPage(extension, targetDir, sourceDir)

    self.__writePageIfNeeded(content, targetPath)
    return paths + [targetPath] + otherRstTargetFiles

  def __generateFileListPage(self, extension, targetDir, sourceDir):

    if not os.path.exists(targetDir):
      os.makedirs(targetDir)

    targetPath = os.path.join(targetDir, 'files.rst')
    sourcePath = os.path.join(sourceDir, 'files.rst')

    paths = []
    content = []
    if os.path.exists(sourcePath):
      content = open(sourcePath, 'r').read().split('\n')
    else:
      content = []
      content += [".. _%s_extension_files:" % extension.getName().lower()]
      content += [""]
      content += ["%s Extension's Files" % extension.getName()]
      content += ["==========================================================================="]
      content += [""]
      content += [".. kl-ext-filelist:: %s" % extension.getName()]
      content += [""]

    self.__writePageIfNeeded(content, targetPath)
    return paths + [targetPath]

  def __generateFilePage(self, extension, klFile, targetDir, sourceDir):

    if not os.path.exists(targetDir):
      os.makedirs(targetDir)

    targetPath = os.path.join(targetDir, '%s.rst' % klFile.getFileName())
    sourcePath = os.path.join(sourceDir, '%s.rst' % klFile.getFileName())

    paths = []
    content = []
    if os.path.exists(sourcePath):
      content = open(sourcePath, 'r').read().split('\n')
    else:
      content = []
      content += [".. _%s:" % klFile.getFileName().lower()]
      content += [".. _%s/%s:" % (extension.getName().lower(), klFile.getFileName().lower())]
      content += [""]
      content += ["%s" % klFile.getFileName()]
      content += ["==========================================================================="]
      content += [""]
      content += [".. kl-file:: %s.%s" % (extension.getName(), klFile.getFileName())]
      content += [""]

    self.__writePageIfNeeded(content, targetPath)
    return paths + [targetPath]

  def __generateInterfaceListPage(self, extension, targetDir, sourceDir):

    if not os.path.exists(targetDir):
      os.makedirs(targetDir)

    targetPath = os.path.join(targetDir, 'interfaces.rst')
    sourcePath = os.path.join(sourceDir, 'interfaces.rst')

    paths = []
    content = []
    if os.path.exists(sourcePath):
      content = open(sourcePath, 'r').read().split('\n')
    else:
      content = []
      content += [".. _%s_extension_interfaces:" % extension.getName().lower()]
      content += [""]
      content += ["%s Extension's Interfaces" % extension.getName()]
      content += ["==========================================================================="]
      content += [""]
      content += [".. kl-ext-interfacelist:: %s" % extension.getName()]
      content += [""]

    self.__writePageIfNeeded(content, targetPath)
    return paths + [targetPath]

  def __generateInterfacePage(self, extension, interface, targetDir, sourceDir):

    if not os.path.exists(targetDir):
      os.makedirs(targetDir)

    targetPath = os.path.join(targetDir, '%s.rst' % interface.getName())
    sourcePath = os.path.join(sourceDir, '%s.rst' % interface.getName())

    paths = []
    content = []
    if os.path.exists(sourcePath):
      content = open(sourcePath, 'r').read().split('\n')
    else:
      content = []
      content += [".. _%s:" % interface.getName().lower()]
      content += [""]
      content += ["%s (interface)" % interface.getName()]
      content += ["==========================================================================="]
      content += [""]
      content += [".. kl-interface:: %s" % interface.getName()]
      content += ["  createrefs=1;"]
      content += ["  methods=1;"]
      content += ["  params=1;"]
      content += [""]

    self.__writePageIfNeeded(content, targetPath)
    return paths + [targetPath]

  def __generateTypeListPage(self, extension, targetDir, sourceDir):

    if not os.path.exists(targetDir):
      os.makedirs(targetDir)

    targetPath = os.path.join(targetDir, 'types.rst')
    sourcePath = os.path.join(sourceDir, 'types.rst')

    paths = []
    content = []
    if os.path.exists(sourcePath):
      content = open(sourcePath, 'r').read().split('\n')
    else:
      content = []
      content += [".. _%s_extension_types:" % extension.getName().lower()]
      content += [""]
      content += ["%s Extension's Types" % extension.getName()]
      content += ["==========================================================================="]
      content += [""]
      content += [".. kl-ext-typelist:: %s" % extension.getName()]
      content += [""]

    self.__writePageIfNeeded(content, targetPath)
    return paths + [targetPath]

  def __generateTypePage(self, extension, klType, targetDir, sourceDir):

    if not os.path.exists(targetDir):
      os.makedirs(targetDir)

    targetPath = os.path.join(targetDir, '%s.rst' % klType.getName())
    sourcePath = os.path.join(sourceDir, '%s.rst' % klType.getName())

    captionSuffix = ''
    if isinstance(klType, KLInterface):
      captionSuffix = ' (interface)'
    elif isinstance(klType, KLObject):
      captionSuffix = ' (object)'
    elif isinstance(klType, KLStruct):
      captionSuffix = ' (struct)'

    paths = []
    content = []
    if os.path.exists(sourcePath):
      content = open(sourcePath, 'r').read().split('\n')
    else:
      content = []
      content += [".. _%s:" % klType.getName().lower()]
      content += [""]
      content += ["%s%s" % (klType.getName(), captionSuffix)]
      content += ["==========================================================================="]
      content += [""]
      content += [".. kl-type:: %s" % klType.getName()]
      content += ["  createrefs=1;"]
      content += ["  methods=1;"]
      content += ["  params=1;"]
      content += ["  members=1;"]
      content += [""]

    self.__writePageIfNeeded(content, targetPath)
    return paths + [targetPath]

  def __generateFreeFunctionListPage(self, extension, targetDir, sourceDir):

    if not os.path.exists(targetDir):
      os.makedirs(targetDir)

    targetPath = os.path.join(targetDir, 'functions.rst')
    sourcePath = os.path.join(sourceDir, 'functions.rst')

    paths = []
    content = []
    if os.path.exists(sourcePath):
      content = open(sourcePath, 'r').read().split('\n')
    else:
      content = []
      content += [".. _%s_extension_functions:" % extension.getName().lower()]
      content += [""]
      content += ["%s Extension's Free Functions" % extension.getName()]
      content += ["==========================================================================="]
      content += [""]
      content += [".. kl-ext-functionlist:: %s" % extension.getName()]
      content += ["  createrefs=1;"]
      content += ["  params=1;"]
      content += ["  plaintext=1;"]
      content += ["  brief=1;"]
      content += ["  customrst=1;"]
      content += ["  example=1;"]
      content += [""]

    self.__writePageIfNeeded(content, targetPath)
    return paths + [targetPath]

  def __generateConstantListPage(self, extension, targetDir, sourceDir):

    if not os.path.exists(targetDir):
      os.makedirs(targetDir)

    targetPath = os.path.join(targetDir, 'constants.rst')
    sourcePath = os.path.join(sourceDir, 'constants.rst')

    paths = []
    content = []
    if os.path.exists(sourcePath):
      content = open(sourcePath, 'r').read().split('\n')
    else:
      content = []
      content += [".. _%s_extension_constants:" % extension.getName().lower()]
      content += [""]
      content += ["%s Extension's Constants" % extension.getName()]
      content += ["==========================================================================="]
      content += [""]
      content += [".. kl-ext-constantlist:: %s" % extension.getName()]
      content += ["  createrefs=1;"]
      content += [""]

    self.__writePageIfNeeded(content, targetPath)
    return paths + [targetPath]

  def generateKLExtensionRST(self, extension, targetDir, sourceDir):
    paths = []

    if not os.path.exists(targetDir):
      os.makedirs(targetDir)

    paths += self.__generateIndexPage(extension, targetDir, sourceDir)

    return paths

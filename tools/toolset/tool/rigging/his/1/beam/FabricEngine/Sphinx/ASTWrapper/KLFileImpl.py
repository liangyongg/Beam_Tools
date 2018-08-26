#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

import os
import json
import FabricEngine.Core

from KLCommentImpl import KLComment
from KLConstantImpl import KLConstant
from KLTypeOpImpl import KLTypeOp
from KLStructImpl import KLStruct
from KLObjectImpl import KLObject
from KLInterfaceImpl import KLInterface
from KLFunctionImpl import KLFunction
from KLMethodImpl import KLMethod
from KLOperatorImpl import KLOperator

class KLFile(object):

  __fileName = None
  __extension = None
  __manager = None
  __client = None
  __decls = None
  __requires = None
  __aliases = None
  __types = None
  __constants = None
  __nameLine = None
  __tableLine = None

  def __init__(self, fileName, extension = None, manager = None):

    self.__fileName = fileName

    # try if this file exists as an original
    jsonFolder = os.path.split(extension.getFilePath())[0]
    relFolder = jsonFolder
    try:
      relFolder = os.path.relpath(jsonFolder, os.environ['FABRIC_EXTS_PATH'].split(os.pathsep)[0])
    except ValueError as e:
      pass

    # hmathee: FE-4549: disabling this - doesn't seem to be required anymore
    # sgDir = os.path.join(os.environ['FABRIC_SCENE_GRAPH_DIR'], 'Native', 'Exts', relFolder)
    # if os.path.exists(sgDir):
    #   relPath = os.path.relpath(self.__fileName, jsonFolder)
    #   fullPath = os.path.join(sgDir, relPath)
    #   if os.path.exists(fullPath):
    #     self.__fileName = fullPath

    self.__extension = extension
    self.__manager = manager

    if KLFile.__client is None:
      KLFile.__client = FabricEngine.Core.createClient()

    if KLFile.__tableLine is None:
      KLFile.__nameLine =  '------------------------------'
      KLFile.__tableLine = '=============================='

    content = open(self.__fileName).read()
    try:
      data = json.loads(KLFile.__client.getKLJSONAST(self.__fileName, content, False).getStringCString())
    except Exception as e:
      message = 'Failed to parse "%s"\n%s' % (self.__fileName, e)
      if manager:
        manager.reportError(message)
        return
      else:
        raise Exception(message)

    data = [data] # we are not expanding into requires, so let's make a double list

    self.__decls = []
    self.__types = {}
    self.__constants = {}
    self.__requires = []
    self.__aliases = {}

    allTypes = KLStruct.getAll()

    elementListIndex = 0
    while elementListIndex < len(data):
      elementList = data[elementListIndex]
      elementListIndex = elementListIndex + 1
      ast = elementList['ast']
      for element in ast:
        et = element['type']
        if et == 'RequireGlobal':
          self.__requires += [element['requires'][0]['name']]
        elif et == 'GlobalConstDecl':
          if not element.has_key('name'):
            continue
          decl = KLConstant(element)
          decl.setExtension(self.__extension)
          decl.setKLFile(self.__fileName)
          self.__decls += [decl]
          self.__constants[decl.getName()] = decl
          if self.__manager:
            self.__manager._registerConstant(decl)
        elif et == "ComparisonOpImpl" or et == "AssignOpImpl" or et == "BinOpImpl" or et == "ASTUniOpDecl":
          decl = KLTypeOp(element)
          decl.setExtension(self.__extension)
          decl.setKLFile(self.__fileName)
          thisType = decl.getLhs()
          if thisType and self.__types.has_key(thisType):
            self.__types[thisType]._addOperator(decl)
          self.__decls += [decl]
        elif et == "ASTStructDecl":
          if not element.has_key('members'): # filter out forward decl
            continue
          decl = KLStruct(element)
          decl.setExtension(self.__extension)
          decl.setKLFile(self.__fileName)
          self.__types[decl.getName()] = decl
          if self.__manager:
            self.__manager._registerType(decl)
        elif et == "ASTObjectDecl":
          if not element.has_key('members'): # filter out forward decl
            continue
          decl = KLObject(element)
          decl.setExtension(self.__extension)
          decl.setKLFile(self.__fileName)
          self.__types[decl.getName()] = decl
          if self.__manager:
            self.__manager._registerType(decl)
        elif et == "ASTInterfaceDecl":
          decl = KLInterface(element)
          if not element.has_key('members'): # filter out forward decl
            continue
          decl.setExtension(self.__extension)
          decl.setKLFile(self.__fileName)
          self.__types[decl.getName()] = decl
          if self.__manager:
            self.__manager._registerType(decl)
        elif et == "Function":
          decl = KLFunction(element)
          decl.setExtension(self.__extension)
          decl.setKLFile(self.__fileName)

          # check if this is a constructor
          thisType = decl.getName().strip('~')
          if allTypes.has_key(thisType):
            decl = KLMethod(element, thisType = thisType)
            decl.setExtension(self.__extension)
            decl.setKLFile(self.__fileName)
            allTypes[thisType]._addMethod(decl)
          elif self.__manager:
              self.__manager._registerFreeFunction(decl)
          self.__decls += [decl]
        elif et == "MethodOpImpl":
          decl = KLMethod(element)
          decl.setExtension(self.__extension)
          decl.setKLFile(self.__fileName)
          self.__decls += [decl]
          thisType = decl.getThisType()

          # deal with standard types
          if thisType == 'String' and not allTypes.has_key(thisType):
            stringDecl = KLStruct({'name': 'String', 'members': []})
            stringDecl.setExtension(self.__extension)
            stringDecl.setKLFile(self.__fileName)
            self.__types[thisType] = stringDecl
            self.__decls += [stringDecl]
            if self.__manager:
              self.__manager._registerType(stringDecl)
            
          if thisType and allTypes.has_key(thisType):
            allTypes[thisType]._addMethod(decl)

            if self.__fileName != allTypes[thisType].getKLFile() and self.__manager:
              self._registerType(allTypes[thisType])

          else:
            manager.registerUnresolvedMethod(decl)

        elif et == "Destructor":
          decl = KLFunction(element)
          decl.setExtension(self.__extension)
          decl.setKLFile(self.__fileName)
          thisType = decl.getName().strip('~')
          decl = KLMethod(element, thisType = thisType)
          decl.setExtension(self.__extension)
          decl.setKLFile(self.__fileName)
          self.__types[thisType]._addMethod(decl)
          self.__decls += [decl]
        elif et == "Operator":
          decl = KLOperator(element)
          decl.setExtension(self.__extension)
          decl.setKLFile(self.__fileName)
          self.__decls += [decl]
        elif et == "Alias":
          self.__aliases[element['newUserName']] = element['oldUserName']
          if self.__manager:
            self.__manager._registerAlias(element['oldUserName'], element['newUserName'])
        elif et == 'ASTFileGlobal':
          globalElements = {"ast": element['globalList']}
          data += [globalElements]
        else:
          print "Unsupported type: "+et
          pass

  def getFilePath(self):
    return self.__fileName

  def getFileName(self):
    return os.path.split(self.__fileName)[1]

  def getRequires(self):
    return self.__requires

  def getConstants(self):
    return self.__constants.values()

  def getTypes(self):
    return self.__types.values()

  def _registerType(self, T):
    self.__types[T.getName()] = T

  def getInterfaces(self):
    content = []
    for t in self.__types:
      if isinstance(self.__types[t], KLInterface):
        content += [self.__types[t]]
    return content

  def getStructs(self):
    content = []
    for t in self.__types:
      if isinstance(self.__types[t], KLStruct) and not isinstance(self.__types[t], KLObject):
        content += [self.__types[t]]
    return content

  def getObjects(self):
    content = []
    for t in self.__types:
      if isinstance(self.__types[t], KLObject):
        content += [self.__types[t]]
    return content

  def getFreeFunctions(self, includeInternal = False, category = None):
    content = []
    for decl in self.__decls:
      if isinstance(decl, KLFunction) and not isinstance(decl, KLMethod) and not isinstance(decl, KLOperator):
        if decl.isInternal() and not includeInternal:
          continue
        if decl.getComments().getSingleQualifier('category', category) != category and category:
          continue
        content += [decl]
    return content

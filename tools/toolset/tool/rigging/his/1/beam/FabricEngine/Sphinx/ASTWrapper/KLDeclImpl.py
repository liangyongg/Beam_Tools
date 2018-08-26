#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#
import uuid
  
class KLDecl(object):

  __nextID = 1
  __id = None
  __json = None
  __ext = None
  __klFile = None

  def __init__(self, data):
    self.__id = 'id'+str(KLDecl.__nextID)
    KLDecl.__nextID = KLDecl.__nextID + 1
    self.__json = data
    if type(data) == dict:
      if data.has_key('owningExtName'):
        self.__ext = data['owningExtName']

  def getID(self):
    return self.__id

  def getJson(self):
    return self.__json

  def getExtension(self):
    return self.__ext

  def setExtension(self, extension):
    if isinstance(extension, str):
      self.__ext = extension
    elif extension is None:
      self.__ext = None
    else:
      self.__ext = extension.getName()

  def isInternal(self):
    return True

  def getKLFile(self):
    return self.__klFile
    
  def setKLFile(self, path):
    self.__klFile = path

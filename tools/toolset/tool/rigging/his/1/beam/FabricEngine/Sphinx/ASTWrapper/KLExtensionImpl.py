#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

import os
import json

from KLFileImpl import KLFile

class KLExtension(object):

  __fileName = None
  __klFiles = None

  def __init__(self, fileName, manager = None):

    self.__fileName = fileName
    self.__manager = manager
    self.__klFiles = {}

    try:
      data = json.loads(open(fileName, 'r').read())
    except ValueError as e:
      print 'Extension fpm file "%s" cannot be decoded: %s' % (fileName, str(e))
      raise(e)

    folder = os.path.split(fileName)[0]

    if data.has_key('code'):
      klFiles = data['code']
      if not isinstance(klFiles, list):
        klFiles = [klFiles]
      for klFile in klFiles:
        path = os.path.join(folder, klFile)
        if self.__klFiles.has_key(path):
          continue
        self.__klFiles[str(path)] = KLFile(path, self, manager)

  def getFilePath(self):
    return self.__fileName

  def getName(self):
    fileName = os.path.split(self.__fileName)[1]
    return fileName.partition('.')[0]

  def getKLFiles(self):
    return self.__klFiles.values()

  def _getKLFilesDict(self):
    return self.__klFiles

  def getKLFile(self, path):
    if self.__klFiles.has_key(path):
      return self.__klFiles[path]
    for key in self.__klFiles:
      klFile = self.__klFiles[key]
      if klFile.getFilePath() == path:
        return klFile
      if klFile.getFileName() == path:
        return klFile
      if klFile.getFileName().rpartition('.')[0] == path:
        return klFile
    path = os.path.normpath(path)
    if self.__klFiles.has_key(path):
      return self.__klFiles[path]
    path = os.path.abspath(path)
    if self.__klFiles.has_key(path):
      return self.__klFiles[path]
    return None

  def getKLInterfaces(self):
    result = []
    for key in self.__klFiles:
      result += self.__klFiles[key].getInterfaces()
    return result

  def getKLTypes(self):
    result = []
    for key in self.__klFiles:
      result += self.__klFiles[key].getStructs()
      result += self.__klFiles[key].getObjects()
    return result

  def getKLConstants(self):
    result = []
    for key in self.__klFiles:
      result += self.__klFiles[key].getConstants()
    return result

  def getKLFreeFunctions(self):
    result = []
    for key in self.__klFiles:
      result += self.__klFiles[key].getFreeFunctions()
    return result

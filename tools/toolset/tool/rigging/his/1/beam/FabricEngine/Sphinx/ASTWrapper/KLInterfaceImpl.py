#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from KLCommentedImpl import KLCommented
from KLMethodImpl import KLMethod
from KLStructImpl import KLStruct

class KLInterface(KLCommented):

  __name = None
  __methods = None
  __methodLookup = None

  def __init__(self, data):

    # call superclass
    super(KLInterface, self).__init__(data)

    self.__name = data['name']
    KLStruct.getAll()[self.__name] = self

    self.__methods = {}
    self.__methodLookup = {}
    if data.has_key('members'):
      for member in data['members']:
        decl = KLMethod(member, thisType = self.__name)
        self.__methodLookup[decl.getLabel()] = decl.getID()
        self.__methods[decl.getID()] = decl

  def setExtension(self, extension):
    super(KLInterface, self).setExtension(extension)
    for key in self.__methods:
      self.__methods[key].setExtension(extension)

  def getName(self):
    return self.__name

  def getKLType(self):
    return 'interface'

  def getMethods(self, includeInherited = False, includeInternal = True, category = None):

    if category == 'operators':
      return []

    lookup = {}
    for key in self.__methods:
      m = self.__methods[key]
      if m.isInternal() and not includeInternal:
        continue
      if m.getComments().getSingleQualifier('category', category) != category and category:
        continue
      lookup[m.getLabel()] = m

    result = []
    for key in sorted(lookup.keys()):
      result.append(lookup[key])    

    return result

  def getMethod(self, key):
    if self.__methods.has_key(key):
      return self.__methods[key]
    if self.__methodLookup.has_key(key):
      return self.__methods[self.__methodLookup[key]]
    for id in self.__methods:
      if self.__methods[id].getName() == key:
        return self.__methods[id]
    return None

  def getParents(self):
    return []

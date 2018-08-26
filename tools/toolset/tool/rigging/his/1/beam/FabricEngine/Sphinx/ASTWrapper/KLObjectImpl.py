#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from KLStructImpl import KLStruct
from KLInterfaceImpl import KLInterface

class KLObject(KLStruct):

  __parentsAndInterfaces = None

  def __init__(self, data):

    # call superclass
    super(KLObject, self).__init__(data)

    self.__parentsAndInterfaces = []
    if data.has_key('parentsAndInterfaces'):
      self.__parentsAndInterfaces += data['parentsAndInterfaces']

  def getKLType(self):
    return 'object'

  def getInterfaces(self):
    ts = KLStruct.getAll()
    content = []
    for p in self.__parentsAndInterfaces:
      if ts.has_key(p):
        if isinstance(ts[p], KLInterface):
          content += [ts[p]]
    return content

  def getParents(self):
    ts = KLStruct.getAll()
    content = []
    for p in self.__parentsAndInterfaces:
      if ts.has_key(p):
        if isinstance(ts[p], KLObject):
          content += [ts[p]]
    return content

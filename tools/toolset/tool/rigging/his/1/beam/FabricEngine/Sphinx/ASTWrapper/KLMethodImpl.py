#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from KLFunctionImpl import KLFunction
from KLStructImpl import KLStruct
import KLInterfaceImpl
import KLObjectImpl

class KLMethod(KLFunction):

  __thisType = None
  __thisUsage = None

  def __init__(self, data, thisType = None):

    # call superclass
    super(KLMethod, self).__init__(data)

    self.__thisType = data.get('thisType', thisType)
    if not data.has_key('thisUsage'):
      self.__thisUsage = 'io'
    else:
      self.__thisUsage = data['thisUsage']

  def getThisType(self):
    return self.__thisType

  def getThisUsage(self):
    return self.__thisUsage

  def getPrefix(self):
    prefix = self.getThisType()
    # filter out constructors / destructors
    if self.getName().strip('~') == prefix:
      return ''
    return self.getThisType() + '.'

  def getSuffix(self):
    if self.__thisUsage == 'in':
      return '?'
    return '!'

  def isConstructor(self):
    return self.getLabel().startswith(self.getThisType() + ' (')

  def isVirtual(self):
    # this will have to implement the virtual keyword
    ts = KLStruct.getAll()
    if ts.has_key(self.__thisType):
      if isinstance(ts[self.__thisType], KLInterfaceImpl.KLInterface):
        return True
      if not isinstance(ts[self.__thisType], KLObjectImpl.KLObject):
        return True
    return False

  def getComments(self):
    comments = super(KLMethod, self).getComments()
    key = self.getLabel()

    # go up the inheritance hierarchy to find 
    # comments on the inherited method
    if not comments or comments.isEmpty():
      ts = KLStruct.getAll()
      if ts.has_key(self.__thisType):
        t = ts[self.__thisType]
        parents = t.getParents()
        if hasattr(t, 'getInterfaces'):
          parents += t.getInterfaces()
        for p in parents:
          methods = p.getMethods()
          for m in methods:
            if m.getLabel() == key:
              return m.getComments()

    return comments

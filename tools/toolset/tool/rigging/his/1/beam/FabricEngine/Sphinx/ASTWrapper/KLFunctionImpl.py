#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from KLCommentedImpl import KLCommented
from KLCommentImpl import KLComment
from KLParameterListImpl import KLParameterList
from KLStructImpl import KLStruct

class KLFunction(KLCommented):

  __name = None
  __returnType = None
  __params = None

  def __init__(self, data):

    # call superclass
    super(KLFunction, self).__init__(data)

    if data.has_key('returnType'):
      self.__returnType = data['returnType']

    self.__name = data['name']
    self.__params = KLParameterList(data.get('params', []))

  def getName(self):
    return self.__name

  def getPrefix(self):
    return ''

  def getSuffix(self):
    return ''

  def getKLType(self):
    return 'function'

  def getKLCode(self, includeReturnType = True, includeKeyWord = True, includePrefix = True, includeName = True):
    code = ''
    if includeKeyWord:
      code += self.getKLType()
      code += ' '
    if self.getReturnType() and includeReturnType:
      code += self.getReturnType() + ' '
    if includePrefix:
      code += self.getPrefix()
    if includeName:
      code += self.getName()

    skipSuffix = False
    if hasattr(self, 'getThisType'):
      if self.getName().strip('~') == self.getThisType():
        skipSuffix = True
    if not skipSuffix:
      code += self.getSuffix()

    code += ' ('
    if len(self.__params):
      code += ' '
      for p in self.__params:
        if not code.endswith('( ') and not code.endswith(', '):
          code += ', '
        code += p.getUsage()
        code += ' '
        code += p.getTypeNoArray()
        code += ' '
        code += p.getName()
        code += p.getTypeArraySuffix()
      code += ' '
    code += ')'
    return code

  def getLabel(self):
    return self.getKLCode(includeReturnType = False, includeKeyWord = False, includePrefix = False)

  def getReturnType(self):
    return self.__returnType

  def getParameters(self):
    return self.__params
  

#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from KLDeclImpl import KLDecl

class KLParameter(KLDecl):

  __usage = None
  __name = None
  __type = None

  def __init__(self, data):

    # call superclass
    super(KLParameter, self).__init__(data)

    self.__usage = data['usage']
    self.__type = data['typeUserName']
    self.__name = data['name']

  def getUsage(self):
    return self.__usage

  def getType(self):
    return self.__type

  def getTypeNoArray(self):
    t = self.__type.partition('[')[0]
    if t.endswith('<>'):
      return t.strip('<>')
    return t

  def getTypeArraySuffix(self):
    if self.__type.endswith('<>'):
      suffix = self.__type.partition('<')
      return suffix[1] + suffix[2]
    if self.__type.endswith(']'):
      suffix = self.__type.partition('[')
      return suffix[1] + suffix[2]
    return ''

  def getName(self):
    return self.__name
  

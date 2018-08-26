#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from KLDeclImpl import KLDecl
from KLParameterImpl import KLParameter

class KLParameterList(KLDecl):

  __params = None

  def __init__(self, data):

    # call superclass
    super(KLParameterList, self).__init__(data)

    self.__params = []
    for element in data:
      self.__params += [KLParameter(element)]

  def getParams(self):
    return self.__params

  def __len__(self):
    return len(self.__params)

  def __getitem__(self, key):
    return self.__params[key]

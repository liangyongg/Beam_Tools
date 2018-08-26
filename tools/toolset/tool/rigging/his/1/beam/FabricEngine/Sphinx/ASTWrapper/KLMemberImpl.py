#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from KLCommentedImpl import KLCommented

class KLMember(KLCommented):

  __name = None
  __type = None

  def __init__(self, data):

    # call superclass
    super(KLMember, self).__init__(data)

    self.__type = data['baseType']
    self.__name = data['memberDecls'][0]['name']
    self.__type += data['memberDecls'][0]['arrayModifier']

  def getType(self):
    return self.__type

  def getName(self):
    return self.__name

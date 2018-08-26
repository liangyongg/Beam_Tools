#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from KLCommentedImpl import KLCommented
from KLCommentImpl import KLComment

class KLConstant(KLCommented):

  __name = None
  __type = None
  __value = None

  def __init__(self, data):

    # call superclass
    super(KLConstant, self).__init__(data)

    self.__name = data['constDecl']['name']
    self.__type = data['constDecl']['type']

  def getName(self):
    return self.__name

  def getType(self):
    return self.__type
    

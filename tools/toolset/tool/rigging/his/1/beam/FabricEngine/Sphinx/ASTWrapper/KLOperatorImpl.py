#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from KLFunctionImpl import KLFunction

class KLOperator(KLFunction):

  __thisType = None
  __thisUsage = None

  def __init__(self, data, thisType = None):

    # call superclass
    super(KLOperator, self).__init__(data)

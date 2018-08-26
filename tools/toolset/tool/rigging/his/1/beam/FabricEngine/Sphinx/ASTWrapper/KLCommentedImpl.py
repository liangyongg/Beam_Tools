#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from KLDeclImpl import KLDecl
from KLCommentImpl import KLComment

class KLCommented(KLDecl):

  __comments = None

  def __init__(self, data):

    # call superclass
    super(KLCommented, self).__init__(data)

    if data.has_key('preComments'):
      self.__comments = KLComment(data['preComments'])
    else:
      self.__comments = KLComment()
    
  def getComments(self):
    return self.__comments

  def isInternal(self):
    return self.getComments().hasQualifier('internal')



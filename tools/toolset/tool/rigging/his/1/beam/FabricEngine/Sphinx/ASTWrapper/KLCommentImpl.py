#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from KLDeclImpl import KLDecl

class KLComment(KLDecl):

  __lines = None
  __qualifiers = None

  def __init__(self, data = []):

    # call superclass
    super(KLComment, self).__init__(data)
    
    self.__lines = []
    self.__lines += data
    self.__content = None
    self.__qualifiers = {}

  def isEmpty(self):
    return len(self.getDoxygenContent()) == 0

  def getDoxygenContent(self):
    if not self.__content:
      self.__content = []
      inBlock = False
      for line in self.__lines:
        lines = line.split('\n')
        for l in lines:
          l0 = l.strip(' \t\n\r')
          l1 = l.strip('/* \t\n\r')
          l2 = l.strip('/*\n\r')
          if l0.startswith('///'):
            if l2:
              self.__content += [l2]
          elif l0.startswith('/**'):
            if l2:
              self.__content += [l2]
            inBlock = True
          elif l0.endswith('*/'):
            if inBlock:
              if l2:
                self.__content += [l2]
              inBlock = False
          elif inBlock:
            # if l2:
            #   self.__content += [l2]
            self.__content += [l2]

    return self.__content

  def hasQualifier(self, qualifier):
    q = qualifier.lower().strip()
    lines = self.getDoxygenContent()
    for line in lines:
      l = line.strip()
      if l.startswith('\\'+q):
        return True
      elif not l.startswith('\\') and q == 'plaintext':
        return True
    return False

  def getQualifier(self, qualifier = None, default = None):
    q = qualifier.lower().strip()
    if self.__qualifiers.has_key(q):
      return self.__qualifiers[q]

    lines = self.getDoxygenContent()
    content = None
    insideQualifier = None
    for line in lines:
      l = line.strip()
      if l.startswith('\\'+q):
        if not content:
          content = []
        content += [l.partition(' ')[2]]
      if l.startswith('\\') and l.count(' ') == 0:
        if insideQualifier:
          if l == '\\end'+insideQualifier:
            insideQualifier = None
        else:
          insideQualifier = l[1:]
      if ((q is None or q == 'plaintext') and not l.startswith('\\')) and not insideQualifier:
        if not content:
          content = []
        content += [l]

    if content is None and default:
      if isinstance(default, list):
        content = default
      else:
        content = [default]

    self.__qualifiers[q] = content
    return content

  def getSingleQualifier(self, qualifier, default = None):
    q = self.getQualifier(qualifier, default)
    if not q:
      return ''
    if isinstance(q, list):
      return q[0]
    return q

  def getQualifierBracket(self, qualifier, default = None):
    q1 = qualifier.lower().strip()
    q2 = 'end'+q1
    if self.__qualifiers.has_key(q1):
      return self.__qualifiers[q1]

    lines = self.getDoxygenContent()
    content = None
    inBlock = False
    blockIndentation = 0
    for line in lines:
      l = line.lstrip(' \t')
      if inBlock:
        if l.startswith('\\'+q2):
          inBlock = False
        else:
          if not content:
            content = []
          if qualifier == 'rst':
            content += [line]
          else:
            if blockIndentation is None:
              blockIndentation = len(line) - len(line.lstrip())
            content += [line[blockIndentation:]]
      elif l.startswith('\\'+q1):
        inBlock = True
        blockIndentation = None

    if content is None and default:
      if isinstance(default, list):
        content = default
      else:
        content = [default]

    self.__qualifiers[q1] = content
    return content    

  def getBrief(self):
    brief = self.getQualifier('brief')
    if brief is None:
      return ''
    return str('').join(brief)

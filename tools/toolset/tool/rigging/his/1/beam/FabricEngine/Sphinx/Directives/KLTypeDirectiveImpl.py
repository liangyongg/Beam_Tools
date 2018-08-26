from KLBaseDirectiveImpl import KLBaseDirective
from ASTWrapper import KLManager, KLInterface, KLStruct, KLObject

class KLTypeDirective(KLBaseDirective):

  def getContent(self):
    options = self.getOptions()

    m = KLManager.getInstance()
    if m is None:
      return []
    key = self.arguments[0]

    decl = m.getType(key)

    captionSuffix = ''
    if isinstance(decl, KLInterface):
      captionSuffix = ' (interface)'
    elif isinstance(decl, KLObject):
      captionSuffix = ' (object)'
    elif isinstance(decl, KLStruct):
      captionSuffix = ' (struct)'

    if decl is None:
      raise self.error('KL Type "%s" not found.' % key)
    if isinstance(decl, KLInterface):
      raise self.error('KL Type "%s" is an interface.' % key)

    result = []
    result += self.generateTitle(decl.getName()+captionSuffix)
    result += self.generateBriefDesc(decl)
    result += self.generatePlainText(decl)
    result += self.generateCustomRST(decl)

    if int(self.getOptions().get('inheritancegraph', 1)):
      result += ['', '.. kl-inheritance:: %s' % decl.getName(), '']


    members = self.generateKLTypeMembers(decl)
    if len(members) > 0:
      result += ['Members', '-------------------', '']
      result += members

    result += self.generateKLExample(decl, decl.getName())

    if int(self.getOptions().get('methods', 1)):
      hasMethods = len(decl.getMethods(includeInherited = True)) > 0
      pastedSomething = False
      if hasMethods:
        result += ['Methods', '-------------------', '']
        result += ['.. kl-methodlist:: %s' % decl.getName()]
        result += ['  compact=1;']
        result += ['']
      if len(decl.getOperators()) > 0:
        result += ['Operators', '-------------------', '']
        result += ['.. kl-methodlist:: %s' % decl.getName()]
        result += ['  category=operators;']
        result += ['  compact=1;']
        result += ['']

    if int(self.getOptions().get('methods', 1)) and int(self.getOptions().get('detailedmethods', 1)):
      if hasMethods:
        result += ['Methods in detail', '-------------------', '']
        result += ['.. kl-methodlist:: %s' % decl.getName()]
        result += ['  category=;']
        result += ['  includeinherited=0;']
        result += ['  createrefs=%s;' % self.getOptions().get('createrefs', 1)]
        result += ['  title=0;']
        result += ['  params=%s;' % self.getOptions().get('params', 0)]
        result += ['  plaintext=%s;' % self.getOptions().get('plaintext', 1)]
        result += ['  brief=%s;' % self.getOptions().get('brief', 1)]
        result += ['  example=%s;' % self.getOptions().get('example', 1)]
        result += ['  customrst=%s;' % self.getOptions().get('customrst', 1)]
        result += ['']
      if len(decl.getOperators()) > 0:
        result += ['Operators in detail', '-------------------', '']
        result += ['.. kl-methodlist:: %s' % decl.getName()]
        result += ['  category=operators;']
        result += ['  createrefs=%s;' % self.getOptions().get('createrefs', 1)]
        result += ['  title=0;']
        result += ['  params=%s;' % self.getOptions().get('params', 0)]
        result += ['  plaintext=%s;' % self.getOptions().get('plaintext', 1)]
        result += ['  brief=%s;' % self.getOptions().get('brief', 1)]
        result += ['  example=%s;' % self.getOptions().get('example', 1)]
        result += ['  customrst=%s;' % self.getOptions().get('customrst', 1)]
        result += ['']

    return result

from KLBaseDirectiveImpl import KLBaseDirective
from ASTWrapper import KLManager, KLInterface, KLStruct, KLObject

class KLInterfaceDirective(KLBaseDirective):

  def getContent(self):
    options = self.getOptions()

    m = KLManager.getInstance()
    if m is None:
      return []
    key = self.arguments[0]
    decl = m.getInterface(key)
    if decl is None:
      raise self.error('KL Interface "%s" not found.' % key)

    captionSuffix = ' (interface)'

    result = []
    result += self.generateTitle(decl.getName()+captionSuffix)
    result += self.generateBriefDesc(decl)
    result += self.generatePlainText(decl)
    result += self.generateCustomRST(decl)

    if int(self.getOptions().get('inheritancegraph', 1)):
      result += ['', '.. kl-inheritance:: %s' % decl.getName(), '']

    result += self.generateKLExample(decl, decl.getName())

    if int(self.getOptions().get('methods', 1)):
      if len(decl.getMethods()) > 0:
        result += ['Functions', '-------------------', '']
        result += ['.. kl-methodlist:: %s' % decl.getName()]
        result += ['  compact=1;']
        result += ['']
        result += ['Functions in detail', '-------------------', '']
        result += ['.. kl-methodlist:: %s' % decl.getName()]
        result += ['  category=;']
        result += ['  createrefs=%s;' % self.getOptions().get('createrefs', 1)]
        result += ['  title=0;']
        result += ['  params=%s;' % self.getOptions().get('params', 0)]
        result += ['  plaintext=%s;' % self.getOptions().get('plaintext', 1)]
        result += ['  brief=%s;' % self.getOptions().get('brief', 1)]
        result += ['  example=%s;' % self.getOptions().get('example', 1)]
        result += ['  customrst=%s;' % self.getOptions().get('customrst', 1)]
        result += ['']

    return result

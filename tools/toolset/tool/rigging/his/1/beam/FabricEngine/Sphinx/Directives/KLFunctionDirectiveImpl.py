from KLBaseDirectiveImpl import KLBaseDirective
from ASTWrapper import KLManager

class KLFunctionDirective(KLBaseDirective):

  def getContent(self):
    options = self.getOptions()

    m = KLManager.getInstance()
    if m is None:
      return []
    key = self.arguments[0]
    decl = m.getFreeFunction(key)
    if decl is None:
      raise self.error('KL Function "%s" not found.' % key)

    funcCode = decl.getKLCode(includeKeyWord = False)

    result = []
    if int(self.getOptions().get('createrefs', 0)):
      result += [".. _%s:" % decl.getID()]
    result += self.generateTitle(decl.getName())
    result += ['.. kl-css:: klcode', '', '  %s' % funcCode, '']
    result += self.generateBriefDesc(decl)
    result += self.generatePlainText(decl)
    result += self.generateCustomRST(decl)
    result += self.generateKLFunctionParams(decl)
    result += self.generateKLExample(decl, decl.getName())

    return result

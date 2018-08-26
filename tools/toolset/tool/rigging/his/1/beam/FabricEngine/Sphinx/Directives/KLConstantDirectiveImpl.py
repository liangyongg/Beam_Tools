from KLBaseDirectiveImpl import KLBaseDirective
from ASTWrapper import KLManager

class KLConstantDirective(KLBaseDirective):

  def getContent(self):
    options = self.getOptions()

    m = KLManager.getInstance()
    if m is None:
      return []
    key = self.arguments[0]
    decl = m.getConstant(key)
    if decl is None:
      raise self.error('KL Constant "%s" not found.' % key)

    result = []

    if int(self.getOptions().get('createrefs', 0)):
      result += [".. _%s:" % decl.getID()]
    result += self.generateTitle(decl.getName())
    result += ['**%s** ( %s )' % (decl.getName(), decl.getType()), '']
    result += self.generateBriefDesc(decl)
    result += self.generatePlainText(decl)
    result += self.generateCustomRST(decl)
    result += self.generateKLExample(decl, decl.getName())
    result += ['']

    return result

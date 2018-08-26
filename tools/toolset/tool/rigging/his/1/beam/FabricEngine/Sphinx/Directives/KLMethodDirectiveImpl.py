from KLBaseDirectiveImpl import KLBaseDirective
from ASTWrapper import KLManager

class KLMethodDirective(KLBaseDirective):

  def getContent(self):
    options = self.getOptions()

    m = KLManager.getInstance()
    if m is None:
      return []
    key = self.arguments[0]

    (thisTypeName, id) = key.split('.')
    typeDecl = m.getType(thisTypeName)
    if typeDecl is None:
      raise self.error('KL Type "%s" not found.' % thisTypeName)

    decl = typeDecl.getMethod(id)
    if decl is None:
      if hasattr(typeDecl, 'getOperator'):
        decl = typeDecl.getOperator(id)
    if decl is None:
      raise self.error('KL Method not found on Type "%s": "%s".' % (thisTypeName, id))

    funcCode = decl.getKLCode(includeKeyWord = False)
    funcCode = m.insertKLTypeRefs(funcCode)
    if funcCode.startswith('~:ref:'):
      funcCode = funcCode.replace('~:', '~ :')

    result = []
    result += self.generateTitle(decl.getName())
    result += ['', '.. kl-css:: klcode', '', '  %s' % funcCode]

    # category = decl.getComments().getSingleQualifier('category', '')
    # if category:
    #   result += ['This method belongs to the :ref:`%s_%s_methods`.' % (thisTypeName, category), '']
    result += self.generateBriefDesc(decl)
    result += self.generatePlainText(decl)
    result += self.generateCustomRST(decl)
    result += self.generateKLFunctionParams(decl)
    result += self.generateKLExample(decl, decl.getName())

    return result

from KLBaseDirectiveImpl import KLBaseDirective
from ASTWrapper import KLManager

class KLExtensionFunctionListDirective(KLBaseDirective):

  def getContent(self):
    options = self.getOptions()

    manager = KLManager.getInstance()
    if manager is None:
      return []

    includeInternal = int(self.getOptions().get('includeinternal', 0))

    key = self.arguments[0]
    extension = manager.getKLExtension(key)
    if not extension:
      raise self.error('KL Extension "%s" not found.' % key)

    includeInternal = int(self.getOptions().get('includeinternal', 0))
    createRefs = int(self.getOptions().get('createrefs', 0))
    category = self.getOptions().get('category', None)

    allFunctions = {}
    for klFile in extension.getKLFiles():
      funcs = klFile.getFreeFunctions(includeInternal = includeInternal, category = category)
      for f in funcs:
        allFunctions[f.getLabel()] = f

    if len(allFunctions) == 0:
      return []

    result = []

    result = []
    if int(self.getOptions().get('compact', 0)):

      table = []
      for key in sorted(allFunctions.keys()):
        m = allFunctions[key]
        returnType = m.getReturnType()
        if not returnType:
          returnType = ''

        returnType = manager.insertKLTypeRefs(returnType)

        funcCode = ':ref:`%s <%s>` ' % (m.getName(), m.getID())
        funcCode += manager.insertKLTypeRefs(m.getKLCode(includeKeyWord = False, includeReturnType = False, includePrefix = False, includeName = False))

        # escape * operators
        if funcCode[0] in ['*', '+', '-']:
          funcCode = '\\'+funcCode

        row = [returnType, funcCode]
        table.append(row)

      result += self.generateTable(table, 2, 'methodtable')
    else:

      first = True
      for key in sorted(allFunctions.keys()):

        if not first:
          result += ['', '-------', '']
        first = False

        m = allFunctions[key]
        if createRefs:
          result += [".. _%s:" % m.getID()]
        result += [".. kl-function:: %s" % (m.getID())]
        result += ['  title=0;']
        result += ['  brief=%s;' % self.getOptions().get('brief', 0)]
        result += ['  plaintext=%s;' % self.getOptions().get('plaintext', 0)]
        result += ['  example=%s;' % self.getOptions().get('example', 1)]
        result += ['  params=%s;' % self.getOptions().get('params', 0)]
        result += ['  customrst=%s;' % self.getOptions().get('customrst', 1)]


    return result

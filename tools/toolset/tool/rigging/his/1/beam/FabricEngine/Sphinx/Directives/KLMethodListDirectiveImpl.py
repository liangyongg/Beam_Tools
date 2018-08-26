from KLBaseDirectiveImpl import KLBaseDirective
from ASTWrapper import KLManager

class KLMethodListDirective(KLBaseDirective):

  def getContent(self):
    options = self.getOptions()

    manager = KLManager.getInstance()
    if manager is None:
      return []
    key = self.arguments[0]
    decl = manager.getType(key)
    if decl is None:
      raise self.error('KL Type "%s" not found.' % key)

    includeInherited = int(self.getOptions().get('includeinherited', 1))
    includeInternal = int(self.getOptions().get('includeinternal', 0))
    createRefs = int(self.getOptions().get('createrefs', 0))
    category = self.getOptions().get('category', None)

    methods = decl.getMethods(includeInherited = includeInherited, includeInternal = includeInternal, category = category)

    # resort the methods
    prevCategory = ''
    if not category:
      methodsByCategory = {}
      for m in methods:
        c = m.getComments().getSingleQualifier('category', '')
        if not methodsByCategory.has_key(c):
          methodsByCategory[c] = []
        methodsByCategory[c] += [m]

      methods = []
      for c in sorted(methodsByCategory.keys()):
        methods += methodsByCategory[c]

    result = []
    if int(self.getOptions().get('compact', 0)):

      table = []
      for m in methods:

        if not category:
          c = m.getComments().getSingleQualifier('category', '')
          if c and not c == prevCategory:
            if len(table):
              result += self.generateTable(table, 2, 'methodtable')
            table = []
            result += self.generateTitle(c[0].upper()+c[1:]+' methods', 3)
            prevCategory = c

        returnType = m.getReturnType()
        if not returnType:
          returnType = ''

        returnType = manager.insertKLTypeRefs(returnType)

        if m.getName() == '!=':
          funcCode = ':ref:`\\%s <%s>` ' % (m.getName(), m.getID())
        else:
          funcCode = ':ref:`%s <%s>` ' % (m.getName(), m.getID())
        funcCode += manager.insertKLTypeRefs(m.getKLCode(includeKeyWord = False, includeReturnType = False, includePrefix = False, includeName = False))

        # escape * operators
        if funcCode[0] in ['*', '+', '-', '!', '<', '>']:
          funcCode = '\\'+funcCode

        row = [returnType, funcCode]

        table.append(row)

      if len(table):
        result += self.generateTable(table, 2, 'methodtable')
    else:

      for i in range(len(methods)):
        m = methods[i]

        if not category:
          c = m.getComments().getSingleQualifier('category', '')
          if c and not c == prevCategory:
            if createRefs:
              result += [".. _%s_%s_methods:" % (m.getThisType(), c), '']
            result += self.generateTitle(c[0].upper()+c[1:]+' methods', 2)
            prevCategory = c

        if createRefs:
          result += [".. _%s:" % m.getID()]
        result += [".. kl-method:: %s.%s" % (m.getThisType(), m.getID())]
        result += ['  title=0;']
        result += ['  brief=%s;' % self.getOptions().get('brief', 0)]
        result += ['  plaintext=%s;' % self.getOptions().get('plaintext', 0)]
        result += ['  example=%s;' % self.getOptions().get('example', 1)]
        result += ['  params=%s;' % self.getOptions().get('params', 0)]
        result += ['  customrst=%s;' % self.getOptions().get('customrst', 1)]

        if i < len(methods)-1:
          result += ['', '-------', '']

    result += ['']    

    return result

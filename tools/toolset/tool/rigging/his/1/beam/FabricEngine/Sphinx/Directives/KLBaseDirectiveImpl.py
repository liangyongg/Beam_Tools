from docutils import nodes
from docutils.parsers.rst import directives
from docutils.statemachine import ViewList
from sphinx.util.nodes import nested_parse_with_titles
from sphinx.util.compat import Directive
from ASTWrapper import KLManager

class KLBaseDirective(Directive):
  has_content = True
  required_arguments = 1
  optional_arguments = 99
  final_argument_whitespace = False
  option_spec = {
    'linenos': directives.flag,
    'no-output': directives.flag
  }

  __parsedOptions = None

  def run(self):
    stdin = u'\n'.join(self.content)
    content = self.getContent()
    if len(content) == 0:
      return []
    node = nodes.paragraph()
    # for line in content:
    #   nested_parse_with_titles(self.state, ViewList([line]), node)
    nested_parse_with_titles(self.state, ViewList(content), node)
    return [node]

  def getOptions(self):
    if self.__parsedOptions:
      return self.__parsedOptions
    self.__parsedOptions = {}
    text = ''.join(self.arguments[1:])
    lines = text.split(';')
    for line in lines:
      if not line:
        continue
      tokens = line.partition('=')
      self.__parsedOptions[tokens[0]] = tokens[2]
    return self.__parsedOptions

  def getContent(self):
    return []

  def generateTitle(self, caption, titleLevel = None):
    if titleLevel is None:
      titleLevel = int(self.getOptions().get('title', 0))

    if titleLevel == 1:
      return [''.ljust(len(caption)+2, '='), ' %s ' % caption, ''.ljust(len(caption)+2, '='), '']
    if titleLevel == 2:
      return [''.ljust(len(caption)+2, '-'), ' %s ' % caption, ''.ljust(len(caption)+2, '-'), '']
    if titleLevel == 3:
      return [caption, ''.ljust(len(caption), '='), '']
    if titleLevel == 4:
      return [caption, ''.ljust(len(caption), '-'), '']
    if titleLevel == 5:
      return [caption, ''.ljust(len(caption), '`'), '']
    if titleLevel == 6:
      return [caption, ''.ljust(len(caption), '.'), '']
    if titleLevel == 7:
      return [caption, ''.ljust(len(caption), '~'), '']
    if titleLevel == 8:
      return [caption, ''.ljust(len(caption), '*'), '']
    if titleLevel == 9:
      return [caption, ''.ljust(len(caption), '+'), '']
    if titleLevel == 10:
      return [caption, ''.ljust(len(caption), '^'), '']
    return []

  def generateBriefDesc(self, decl):
    useRefs = int(self.getOptions().get('userefs', 1))
    m = KLManager.getInstance()

    if int(self.getOptions().get('brief', 1)):
      lines = decl.getComments().getQualifier('brief')
      if not lines or len(lines) == 0:
        return []
      for i in range(len(lines)):
        if useRefs and m:
          lines[i] = m.insertKLTypeRefs(lines[i])
        lines[i] = '  ' + lines[i]
      return ['', '.. kl-css:: klbrief', ''] + lines + ['']
    return []

  def generatePlainText(self, decl):
    useRefs = int(self.getOptions().get('userefs', 1))
    m = KLManager.getInstance()

    if int(self.getOptions().get('plaintext', 1)):

      content = []
  
      if decl.getComments().hasQualifier('versionadded'):
        content += ['', '.. versionadded:: '+str(decl.getComments().getSingleQualifier('versionadded')), '']

      lines = decl.getComments().getQualifier('plaintext')
      if lines and len(lines) > 0:
        for i in range(len(lines)):
          if useRefs and m:
            lines[i] = m.insertKLTypeRefs(lines[i])
          lines[i] = '  ' + lines[i]
        content += ['', '.. kl-css:: plaintext', ''] + lines + ['']

      if decl.getComments().hasQualifier('note'):
        qualifiers = decl.getComments().getQualifier('note')
        for qualifier in qualifiers:
          content += ['', '.. note:: %s' % m.insertKLTypeRefs(qualifier), '']

      if decl.getComments().hasQualifier('seealso'):
        qualifiers = decl.getComments().getQualifier('seealso')
        for qualifier in qualifiers:
          tokens = qualifier.split(',')
          for i in range(len(tokens)):
            tokens[i] = tokens[i].strip()
            if tokens[i].find('`') == -1:
              tokens[i] = ':kl-ref:`%s`' % tokens[i]
          content += ['', '.. seealso:: %s' % ', '.join(tokens), '']

      return content

    return []

  def generateCustomRST(self, decl):
    if int(self.getOptions().get('customrst', 1)):
      lines = decl.getComments().getQualifierBracket('rst')
      if lines and len(lines) > 0:
        minIndentation = 10000
        for line in lines:
          if not line:
            continue
          l = line.lstrip()
          indentation = len(line) - len(l)
          if indentation < minIndentation:
            minIndentation = indentation
        indentation = ''.ljust(minIndentation)
        for i in range(len(lines)):
          if lines[i].startswith(indentation):
            lines[i] = lines[i][len(indentation):]
        return lines + ['']
    return []    

  def generateTable(self, table, indentation, css = 'paramtable'):

    if not isinstance(indentation, str):
      indentation = ''.ljust(indentation, ' ')

    m = KLManager.getInstance()

    borders = []
    for row in table:
      if len(borders) == 0:
        for cell in row:
          borders.append('-')
      for i in range(len(row)):
        if m:
          row[i] = m.insertKLTypeRefs(row[i])
        if len(row[i]) > len(borders[i]):
          borders[i] = ''.ljust(len(row[i]), '-')

    borderChars = indentation + '+'
    for border in borders:
      borderChars += '-' + border + '-+'
    
    content = ['', '.. kl-css:: '+css, '']
    content += [borderChars]
    for row in table:
      rowChars = indentation + '| '
      for i in range(len(row)):
        if i > 0:
          rowChars += ' | '
        rowChars += row[i].ljust(len(borders[i]), ' ')

      rowChars += ' |'
      content += [rowChars]
      content += [borderChars]
    content += ['']
    return content

  def generateKLFunctionParams(self, decl, indentation = 2):
    if int(self.getOptions().get('params', 0)):
      lines = decl.getComments().getQualifier('param')
      m = KLManager.getInstance()

      if lines and len(lines) > 0:
        table = []
        for p in lines:
          tokens = p.partition(' ')
          desc = tokens[2]
          if m:
            desc = m.insertKLTypeRefs(desc)
          table.append([tokens[0], desc])
        return self.generateTable(table, indentation, 'paramtable')

    return []    

  def generateKLTypeMembers(self, decl, indentation = 2):
    if int(self.getOptions().get('members', 0)):
      members = decl.getMembers(includeInherited = True)
      m = KLManager.getInstance()

      includeInternal = int(self.getOptions().get('includeinternal', 0))

      if len(members) > 0:
        table = []
        hasMembers = False
        for member in members:
          if member.isInternal() and not includeInternal:
            continue
          hasMembers = True
          klType = member.getType()
          desc = member.getComments().getQualifier('plaintext')
          if not desc:
            desc = ''
          else:
            desc = ' '.join(desc)
          if m:
            klType = m.insertKLTypeRefs(klType)
            desc = m.insertKLTypeRefs(desc)
          table.append([klType, member.getName(), desc])
        if not hasMembers:
          return []
        return self.generateTable(table, indentation, 'paramtable')

    return []    

  def generateKLExample(self, decl, exampleName = 'Example'):

    if int(self.getOptions().get('example', 1)):
      lines = decl.getComments().getQualifierBracket('example')

      if lines and len(lines) > 0:
        for i in range(len(lines)):
          lines[i] = '  ' + lines[i]

        if ''.join(lines).find('operator entry') == -1:
          for i in range(len(lines)):
            lines[i] = '  ' + lines[i]
          lines = ['  require '+decl.getExtension()+';', '    ', '  operator entry() {', ''] + lines + ['    ', '  }']

        return ['.. kl-example:: '+exampleName, ''] + lines + ['']
    return []        

import os
from KLBaseDirectiveImpl import KLBaseDirective
from ASTWrapper import KLManager, KLInterface

class KLFileExampleDirective(KLBaseDirective):

  def getContent(self):
    options = self.getOptions()

    filePath = self.arguments[0]

    while filePath.find('${') > -1:

      l, sep, r = filePath.partition('${')
      e, sep, r = r.partition('}')
      if os.environ.has_key(e):
        e = os.environ[e]
      filePath = l + e + r

    if not os.path.exists(filePath):
      raise Exception('KL file %s does not exist.' % filePath)

    code = open(filePath, 'r').read().split('\n')

    result = ['.. kl-example:: %s' % os.path.split(filePath)[1], '']
    for line in code:
      result += ['  %s' % line]
    result += ['']

    return result

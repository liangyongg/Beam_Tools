from KLBaseDirectiveImpl import KLBaseDirective
from ASTWrapper import KLManager

class KLExtensionConstantListDirective(KLBaseDirective):

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
    category = self.getOptions().get('category', None)

    allConstants = {}
    for klFile in extension.getKLFiles():
      constants = klFile.getConstants()
      for f in constants:
        if f.isInternal() and not includeInternal:
          continue
        allConstants[f.getName()] = f

    if len(allConstants) == 0:
      return []

    result = []

    first = True
    for key in sorted(allConstants.keys()):

      if not first:
        result += ['', '-------', '']
      first = False

      m = allConstants[key]

      result += [".. kl-constant:: %s" % (m.getName())]
      result += ['  title=0;']
      result += ['  brief=%s;' % self.getOptions().get('brief', 0)]
      result += ['  plaintext=%s;' % self.getOptions().get('plaintext', 0)]
      result += ['  createrefs=%s;' % self.getOptions().get('createrefs', 0)]
      result += ['  example=%s;' % self.getOptions().get('example', 1)]
      result += ['  params=%s;' % self.getOptions().get('params', 0)]
      result += ['  customrst=%s;' % self.getOptions().get('customrst', 1)]


    return result

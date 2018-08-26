from KLBaseDirectiveImpl import KLBaseDirective
from ASTWrapper import KLManager

class KLExtensionTypeListDirective(KLBaseDirective):

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

    allTypes = {}
    for klFile in extension.getKLFiles():
      types = klFile.getStructs()
      for t in types:
        if t.isInternal() and not includeInternal:
          continue
        allTypes[t.getName()] = t
      types = klFile.getObjects()
      for t in types:
        if t.isInternal() and not includeInternal:
          continue
        allTypes[t.getName()] = t

    if len(allTypes) == 0:
      return []

    result = []
    result += ['.. toctree::', '  :maxdepth: 1', '']
    for key in sorted(allTypes.keys()):
      result += ['  %s' % key]

    return result

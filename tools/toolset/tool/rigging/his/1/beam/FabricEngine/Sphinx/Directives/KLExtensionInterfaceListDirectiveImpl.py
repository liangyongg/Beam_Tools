from KLBaseDirectiveImpl import KLBaseDirective
from ASTWrapper import KLManager

class KLExtensionInterfaceListDirective(KLBaseDirective):

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

    allInterfaces = {}
    for klFile in extension.getKLFiles():
      interfaces = klFile.getInterfaces()
      for i in interfaces:
        if i.isInternal() and not includeInternal:
          continue
        allInterfaces[i.getName()] = i

    if len(allInterfaces) == 0:
      return []

    result = []
    result += ['.. toctree::', '  :maxdepth: 1', '']
    for key in sorted(allInterfaces.keys()):
      result += ['  %s' % key]

    return result

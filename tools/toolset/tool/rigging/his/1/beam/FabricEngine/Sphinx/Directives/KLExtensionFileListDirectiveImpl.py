from KLBaseDirectiveImpl import KLBaseDirective
from ASTWrapper import KLManager

class KLExtensionFileListDirective(KLBaseDirective):

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

    klFiles = extension.getKLFiles()

    lookup = {}
    for klFile in klFiles:
      lookup[klFile.getFileName()] = klFile

    result = ['.. toctree::', '  :maxdepth: 1', '']
    for key in sorted(lookup.keys()):
      result += ['  %s' % key]

    return result

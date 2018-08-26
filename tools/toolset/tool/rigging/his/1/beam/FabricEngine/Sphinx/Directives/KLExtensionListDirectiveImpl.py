import os

from KLBaseDirectiveImpl import KLBaseDirective
from ASTWrapper import KLManager

class KLExtensionListDirective(KLBaseDirective):

  def getContent(self):
    options = self.getOptions()

    manager = KLManager.getInstance()
    if manager is None:
      return []

    lookup = {}
    extensions = manager.getKLExtensions()
    for extension in extensions:
      lookup[extension.getName()] = extension

    result = []
    result += [".. toctree::"]
    result += ["  :maxdepth: 1"]
    result += ["  "]

    for key in sorted(lookup.keys()):
      result += ["  %s" % key+'/index']

    print result

    return result

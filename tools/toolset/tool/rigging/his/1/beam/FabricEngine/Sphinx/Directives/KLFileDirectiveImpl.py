from KLBaseDirectiveImpl import KLBaseDirective
from ASTWrapper import KLManager, KLInterface

class KLFileDirective(KLBaseDirective):

  def getContent(self):
    options = self.getOptions()

    m = KLManager.getInstance()
    if m is None:
      return []
    (extName, sep, fileName) = self.arguments[0].partition('.')

    klExtension = m.getKLExtension(extName)
    if not klExtension:
      raise self.error('KL Extension "%s" not found.' % extName)
    klFile = klExtension.getKLFile(fileName)
    if not klFile:
      raise self.error('KL File "%s" not found.' % fileName)

    result = []

    allKlConstants = klFile.getConstants()
    klConstants = []
    for klConstant in allKlConstants:
      if klConstant.isInternal():
        continue
      klConstants.append(klConstant)
    if len(klConstants):
      result += ['Constants', '----------------------', '']
      for klConstant in klConstants:
        result += ['.. kl-constant:: ' +klConstant.getName()]
        result += ['  title=3;']
        result += ['  createrefs=0;']
        result += ['  plaintext=1;']
        result += ['  brief=1;']
        result += ['  example=1;']
        result += ['  customrst=1;']
      result += ['']

    allKlInterfaces = klFile.getInterfaces()
    klInterfaces = []
    for klInterface in allKlInterfaces:
      if klInterface.isInternal():
        continue
      klInterfaces.append(klInterface)
    if len(klInterfaces):
      result += ['Interfaces', '----------------------', '']
      for klInterface in klInterfaces:
        result += ['.. kl-interface:: ' +klInterface.getName()]
        result += ['  title=3;']
        result += ['  createrefs=0;']
        result += ['  plaintext=1;']
        result += ['  brief=1;']
        result += ['  example=1;']
        result += ['  customrst=1;']
        result += ['  methods=1;']
      result += ['']

    allKlTypes = klFile.getStructs() + klFile.getObjects()
    klTypes = []
    for klType in allKlTypes:
      if klType.isInternal():
        continue
      klTypes.append(klType)
    if len(klTypes):
      result += ['Types', '----------------------', '']
      for klType in klTypes:
        result += ['.. kl-type:: ' +klType.getName()]
        result += ['  title=3;']
        result += ['  createrefs=0;']
        result += ['  inheritancegraph=0;']
        result += ['  plaintext=1;']
        result += ['  brief=1;']
        result += ['  example=1;']
        result += ['  customrst=1;']
        result += ['  members=1;']
        result += ['  methods=1;']
        result += ['  detailedmethods=0;']
      result += ['']

    allKlFreeFunctions = klFile.getFreeFunctions()
    klFreeFunctions = []
    for klFreeFunction in allKlFreeFunctions:
      if klFreeFunction.isInternal():
        continue
      klFreeFunctions.append(klFreeFunction)
    if len(klFreeFunctions):
      result += ['Functions', '----------------------', '']
      for klFreeFunction in klFreeFunctions:
        result += ['.. kl-function:: ' +klFreeFunction.getName()]
        result += ['  title=3;']
        result += ['  createrefs=0;']
        result += ['  plaintext=1;']
        result += ['  brief=1;']
        result += ['  example=1;']
        result += ['  customrst=1;']
        result += ['  params=1;']
      result += ['']

    return result

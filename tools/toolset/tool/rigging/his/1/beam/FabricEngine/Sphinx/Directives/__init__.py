import docutils.nodes
from KLExampleDirectiveImpl import KLExampleDirective
from KLFileExampleDirectiveImpl import KLFileExampleDirective
from KLCssDirectiveImpl import KLCssDirective
from KLFileDirectiveImpl import KLFileDirective
from KLConstantDirectiveImpl import KLConstantDirective
from KLFunctionDirectiveImpl import KLFunctionDirective
from KLInterfaceDirectiveImpl import KLInterfaceDirective
from KLMethodListDirectiveImpl import KLMethodListDirective
from KLMethodDirectiveImpl import KLMethodDirective
from KLInheritanceDirectiveImpl import KLInheritanceDirective
from KLTypeDirectiveImpl import KLTypeDirective
from KLExtensionListDirectiveImpl import KLExtensionListDirective
from KLExtensionFileListDirectiveImpl import KLExtensionFileListDirective
from KLExtensionConstantListDirectiveImpl import KLExtensionConstantListDirective
from KLExtensionInterfaceListDirectiveImpl import KLExtensionInterfaceListDirective
from KLExtensionTypeListDirectiveImpl import KLExtensionTypeListDirective
from KLExtensionFunctionListDirectiveImpl import KLExtensionFunctionListDirective
from CommandLineDirectiveImpl import CommandLineDirective

from KLXRefRoleImpl import KLXRefRole

def setupKLDirectives(app):
  app.add_directive('kl-example', KLExampleDirective)
  app.add_directive('kl-fileexample', KLFileExampleDirective)
  app.add_directive('kl-css', KLCssDirective)
  app.add_directive('kl-file', KLFileDirective)
  app.add_directive('kl-constant', KLConstantDirective)
  app.add_directive('kl-function', KLFunctionDirective)
  app.add_directive('kl-interface', KLInterfaceDirective)
  app.add_directive('kl-inheritance', KLInheritanceDirective)
  app.add_directive('kl-type', KLTypeDirective)
  app.add_directive('kl-methodlist', KLMethodListDirective)
  app.add_directive('kl-method', KLMethodDirective)
  app.add_directive('kl-extlist', KLExtensionListDirective)
  app.add_directive('kl-ext-filelist', KLExtensionFileListDirective)
  app.add_directive('kl-ext-constantlist', KLExtensionConstantListDirective)
  app.add_directive('kl-ext-interfacelist', KLExtensionInterfaceListDirective)
  app.add_directive('kl-ext-typelist', KLExtensionTypeListDirective)
  app.add_directive('kl-ext-functionlist', KLExtensionFunctionListDirective)
  app.add_directive('cmdline', CommandLineDirective)
  app.add_role_to_domain('std', 'kl-ref', KLXRefRole())

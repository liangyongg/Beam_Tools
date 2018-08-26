import sphinx.addnodes
import sphinx.roles
import docutils.nodes

from KLBaseDirectiveImpl import KLBaseDirective
from ASTWrapper import KLManager, KLInterface

class KLXRefRole(sphinx.roles.XRefRole):

  def process_link(self, env, refnode, has_explicit_title, title, target):

    manager = KLManager.getInstance()
    if manager:

      decl = manager.getType(title)

      if decl:

        # use the name of the type
        target = decl.getName().lower()

      else:

        decl = manager.getConstant(title)
        if decl:

          # use the id of the constant
          target = decl.getID()

        else:

          (klType, sep, klMethod) = title.partition('.')
          decl = manager.getType(klType)
          if decl:

            m = decl.getMethod(klMethod)
            if m:
              # use the id of the method

              target = m.getID()

          else:

            decl = manager.getFreeFunction(title)
            if decl:

              # use the id of the free function
              target = decl.getID()

    refnode['reftype'] = 'ref'
    refnode['refexplicit'] = True

    return super(KLXRefRole, self).process_link(env, refnode, has_explicit_title, title, target)

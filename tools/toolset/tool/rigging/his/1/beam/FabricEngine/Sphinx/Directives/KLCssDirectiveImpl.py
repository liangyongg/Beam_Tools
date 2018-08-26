from docutils import nodes
from docutils.parsers.rst import directives
from docutils.statemachine import ViewList
from sphinx.util.compat import Directive
from ASTWrapper import KLManager

class KLCssDirective(Directive):
  has_content = True
  required_arguments = 0
  optional_arguments = 1
  final_argument_whitespace = False

  def run(self):
    node = nodes.paragraph()

    m = KLManager.getInstance()
    content = ViewList(self.content)
    if m:
      for i in range(len(content)):
        content[i] = m.insertKLTypeRefs(content[i])

    self.state.nested_parse(ViewList(content), 0, node)


    children = [] + node.children
    for child in children:
      if hasattr(child, 'set_class'):
        child.set_class(self.arguments[0])

    return node.children
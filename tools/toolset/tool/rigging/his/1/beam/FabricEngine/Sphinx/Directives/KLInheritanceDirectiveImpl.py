import os, subprocess

from KLBaseDirectiveImpl import KLBaseDirective
from ASTWrapper import KLManager, KLInterface, KLObject, KLStruct

class KLInheritanceDirective(KLBaseDirective):

  def __collectInheritanceGraphParents(self, manager, node, content, firstNode = False):

    if not firstNode:
      content += [
        '   "%s" [fillcolor="#b4ced8"]' % node.getName(),
        '   "%s" [color="#3f3f3f"]' % node.getName()
      ]

      url = '../%s/%s.html' % (node.getExtension(), node.getName())
      content += ['   "%s" [URL="%s"]' % (node.getName(), url)]

    parents = node.getParents()
    if isinstance(node, KLObject):
      parents += node.getInterfaces()

    lookup = {}
    for p in parents:
      lookup[p.getName()] = p

    for key in sorted(lookup.keys()):
      p = lookup[key]
      content += ['    "%s" -> "%s";' % (node.getName(), p.getName())]
      self.__collectInheritanceGraphParents(manager, p, content)

  def __collectInheritanceGraphChildren(self, manager, node, content, firstNode = False):

    if not firstNode:
      content += [
        '   "%s" [fillcolor="#b4ced8"]' % node.getName(),
        '   "%s" [color="#3f3f3f"]' % node.getName()
      ]

      url = '../%s/%s.html' % (node.getExtension(), node.getName())
      content += ['   "%s" [URL="%s"]' % (node.getName(), url)]

    allTypes = manager.getTypes()

    lookup = {}

    for t in allTypes:
      if isinstance(t, KLInterface):
        continue
      parents = t.getParents()
      if isinstance(t, KLObject):
        parents += t.getInterfaces()
      for p in parents:
        if p == node:
          lookup[t.getName()] = t

    for key in sorted(lookup.keys()):
      t = lookup[key]
      content += ['    "%s" -> "%s";' % (t.getName(), node.getName())]
      self.__collectInheritanceGraphChildren(manager, t, content)

  def getContent(self):
    options = self.getOptions()

    m = KLManager.getInstance()
    if m is None:
      return []
    key = self.arguments[0]
    decl = m.getType(key)
    if decl is None:
      raise self.error('KL Type "%s" not found.' % key)

    result = ['digraph '+key, '{']

    result += [
      '   graph [rankdir=RL]',
      '   node [fontname=Arial,fontsize=10]',
      '   node [style=filled]',
      '   node [shape=box]',
      '   node [fillcolor="#EEEEEE"]',
      '   node [color="#EEEEEE"]',
      '   edge [color="#3f3f3f"]',
      '   "%s" [fillcolor="#3fabd3"]' % decl.getName(),
      '   "%s" [color="#3f3f3f"]' % decl.getName()
    ]

    url = '../%s/%s.html' % (decl.getExtension(), decl.getName())
    result += ['   "%s" [URL="%s"]' % (decl.getName(), url)]

    if isinstance(decl, KLObject):
      self.__collectInheritanceGraphParents(m, decl, result, firstNode = True)
    self.__collectInheritanceGraphChildren(m, decl, result, firstNode = True)

    result += ['}']
    pipe = subprocess.Popen(
        ['dot', '-Tsvg'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        )
    (stdout, stderr) = pipe.communicate('\n'.join(result))

    result = ['', '.. raw:: html', '']
    lines = stdout.replace('\r', '').split('\n')
    for line in lines:
      if len(result) == 0:
        if line.startswith('<svg'):
          result += ['  '+line]
        continue
      result += ['  '+line]
    result += ['']

    return result

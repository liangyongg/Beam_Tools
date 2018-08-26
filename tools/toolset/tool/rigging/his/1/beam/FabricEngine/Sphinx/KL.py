# -*- coding: utf-8 -*-
#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from FabricEngine.Pygments import KLLexer

import re, subprocess

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx import addnodes
from sphinx.roles import XRefRole
from sphinx.locale import l_, _
from sphinx.domains import Domain, ObjType, Index
from sphinx.directives import ObjectDescription
from sphinx.util.nodes import make_refnode, set_source_info
from sphinx.util.compat import Directive
from sphinx.util.docfields import Field, GroupedField, TypedField

from Directives import setupKLDirectives

# REs for KL signatures
kl_sig_re = re.compile(
    r'''^ (function\s|operator\s|inline\s) \s*
          (<?[a-zA-Z_][a-zA-Z_0-9]*>?\s)? \s* # optional: return type
    			([a-zA-Z_][a-zA-Z_0-9]* \s* \.)? \s* # class name(s)
          ([a-zA-Z_][a-zA-Z_0-9]* \s* [?!]?)  \s* # thing name
          (?: \((.*)\) )?          # optional: arguments
          $                   # and nothing more
          ''', re.VERBOSE)

kl_paramlist_re = re.compile(r'([,])')  # split at ','

separators = {
  'method':'#', 'attr_reader':'#', 'attr_writer':'#', 'attr_accessor':'#',
  'function':'.', 'classmethod':'.', 'class':'::', 'module':'::',
  'global':'', 'const':'::'}

kl_separator = re.compile(r"(?:\w+)?(?:\.)?")


def _iteritems(d):

    for k in d:
        yield k, d[k]


def kl_rsplit(fullname):
    items = [item for item in kl_separator.findall(fullname)]
    return ''.join(items[:-2]), items[-1]


class KLObject(ObjectDescription):
    """
    Description of a general KL object.
    """
    option_spec = {
        'noindex': directives.flag,
        'module': directives.unchanged,
		    }

    doc_field_types = [
        TypedField('parameter', label=l_('Parameters'),
                   names=('param', 'parameter', 'arg', 'argument'),
                   typerolename='obj', typenames=('paramtype', 'type')),
        TypedField('variable', label=l_('Variables'), rolename='obj',
                   names=('var', 'ivar', 'cvar'),
                   typerolename='obj', typenames=('vartype',)),
        GroupedField('exceptions', label=l_('Raises'), rolename='exc',
                     names=('raises', 'raise', 'exception', 'except'),
                     can_collapse=True),
        Field('returnvalue', label=l_('Returns'), has_arg=False,
              names=('returns', 'return')),
        Field('returntype', label=l_('Return type'), has_arg=False,
              names=('rtype',)),
		    ]

    def needs_arglist(self):
        """
        May return true if an empty argument list is to be generated even if
        the document contains none.
        """
        return False

    def handle_signature(self, sig, signode):
        """
        Transform a Ruby signature into RST nodes.
        Returns (fully qualified name of the thing, classname if any).

        If inside a class, the current class name is handled intelligently:
        * it is stripped from the displayed name if present
        * it is added to the full name (return value) if not present
        """
        m = kl_sig_re.match(sig)
        if m is None:
            raise ValueError
        functype, retann, name_prefix, name, arglist = m.groups()
        if not name_prefix:
            name_prefix = ""
        # determine module and class name (if applicable), as well as full name
        modname = self.options.get(
            'module', self.env.temp_data.get('kl:module'))
        classname = self.env.temp_data.get('kl:class')
        if self.objtype == 'global':
            add_module = False
            modname = None
            classname = None
            fullname = name
        elif classname:
            add_module = False
            if name_prefix and name_prefix.startswith(classname):
                fullname = name_prefix + name
                # class name is given again in the signature
                name_prefix = name_prefix[len(classname):].lstrip('.')
            else:
                separator = separators[self.objtype]
                fullname = classname + separator + name_prefix + name
        else:
            add_module = True
            if name_prefix:
                classname = name_prefix.rstrip('.')
                fullname = name_prefix + name
            else:
                classname = ''
                fullname = name

        signode['module'] = modname
        signode['class'] = self.class_name = classname
        signode['fullname'] = fullname

        signode += addnodes.desc_annotation(functype, functype)
        if retann:
	        signode += addnodes.desc_annotation(retann, retann)

        if name_prefix:
            signode += addnodes.desc_addname(name_prefix, name_prefix)
        # exceptions are a special case, since they are documented in the
        # 'exceptions' module.
        elif add_module and self.env.config.add_module_names:
            if self.objtype == 'global':
                nodetext = ''
                signode += addnodes.desc_addname(nodetext, nodetext)
            else:
                modname = self.options.get(
                    'module', self.env.temp_data.get('kl:module'))
                if modname and modname != 'exceptions':
                    nodetext = modname + separators[self.objtype]
                    signode += addnodes.desc_addname(nodetext, nodetext)

        signode += addnodes.desc_name(name, name)
        if not arglist:
            if self.needs_arglist():
                # for callables, add an empty parameter list
                signode += addnodes.desc_parameterlist()
            return fullname, name_prefix
        signode += addnodes.desc_parameterlist()

        stack = [signode[-1]]
        for token in kl_paramlist_re.split(arglist):
            if token == '[':
                opt = addnodes.desc_optional()
                stack[-1] += opt
                stack.append(opt)
            elif token == ']':
                try:
                    stack.pop()
                except IndexError:
                    raise ValueError
            elif not token or token == ',' or token.isspace():
                pass
            else:
                token = token.strip()
                stack[-1] += addnodes.desc_parameter(token, token)
        if len(stack) != 1:
            raise ValueError
        return fullname, name_prefix

    def get_index_text(self, modname, name):
        """
        Return the text for the index entry of the object.
        """
        raise NotImplementedError('must be implemented in subclasses')

    def _is_class_member(self):
        return self.objtype.endswith('method') or self.objtype.startswith('attr')

    def add_target_and_index(self, name_cls, sig, signode):
        if self.objtype == 'global':
            modname = ''
        else:
            modname = self.options.get(
                'module', self.env.temp_data.get('kl:module'))
        separator = separators[self.objtype]
        if self._is_class_member():
            if signode['class']:
                prefix = modname and modname + '::' or ''
            else:
                prefix = modname and modname + separator or ''
        else:
            prefix = modname and modname + separator or ''
        fullname = prefix + name_cls[0]
        # note target
        if fullname not in self.state.document.ids:
            signode['names'].append(fullname)
            signode['ids'].append(fullname)
            signode['first'] = (not self.names)
            self.state.document.note_explicit_target(signode)
            objects = self.env.domaindata['kl']['objects']
            if fullname in objects:
                self.env.warn(
                    self.env.docname,
                    'duplicate object description of %s, ' % fullname +
                    'other instance in ' +
                    self.env.doc2path(objects[fullname][0]),
                    self.lineno)
            objects[fullname] = (self.env.docname, self.objtype)

        indextext = self.get_index_text(modname, name_cls)
        if indextext:
            self.indexnode['entries'].append(('single', indextext,
                                              fullname, fullname))

    def before_content(self):
        # needed for automatic qualification of members (reset in subclasses)
        self.clsname_set = False

    def after_content(self):
        if self.clsname_set:
            self.env.temp_data['kl:class'] = None


class KLModulelevel(KLObject):
    """
    Description of an object on module level (functions, data).
    """

    def needs_arglist(self):
        return self.objtype == 'function'

    def get_index_text(self, modname, name_cls):
        if self.objtype == 'function':
            if not modname:
                return _('%s() (global function)') % name_cls[0]
            return _('%s() (module function in %s)') % (name_cls[0], modname)
        else:
            return ''


class KLXRefRole(XRefRole):
    def process_link(self, env, refnode, has_explicit_title, title, target):
        if not has_explicit_title:
            title = title.lstrip('.')   # only has a meaning for the target
            title = title.lstrip('#')
            if title.startswith("::"):
                title = title[2:]
            target = target.lstrip('~') # only has a meaning for the title
            # if the first character is a tilde, don't display the module/class
            # parts of the contents
            if title[0:1] == '~':
                m = re.search(r"(?:\.)?(?:#)?(?:::)?(.*)\Z", title)
                if m:
                    title = m.group(1)
        if not title.startswith("$"):
            refnode['kl:module'] = env.temp_data.get('kl:module')
            refnode['kl:class'] = env.temp_data.get('kl:class')
        # if the first character is a dot, search more specific namespaces first
        # else search builtins first
        if target[0:1] == '.':
            target = target[1:]
            refnode['refspecific'] = True
        return title, target


class KLModuleIndex(Index):
    """
    Index subclass to provide the Ruby module index.
    """

    name = 'modindex'
    localname = l_('Ruby Module Index')
    shortname = l_('modules')

    def generate(self, docnames=None):
        content = {}
        # list of prefixes to ignore
        ignores = self.domain.env.config['modindex_common_prefix']
        ignores = sorted(ignores, key=len, reverse=True)
        # list of all modules, sorted by module name
        modules = sorted(_iteritems(self.domain.data['modules']),
                         key=lambda x: x[0].lower())
        # sort out collapsable modules
        prev_modname = ''
        num_toplevels = 0
        for modname, (docname, synopsis, platforms, deprecated) in modules:
            if docnames and docname not in docnames:
                continue

            for ignore in ignores:
                if modname.startswith(ignore):
                    modname = modname[len(ignore):]
                    stripped = ignore
                    break
            else:
                stripped = ''

            # we stripped the whole module name?
            if not modname:
                modname, stripped = stripped, ''

            entries = content.setdefault(modname[0].lower(), [])

            package = modname.split('::')[0]
            if package != modname:
                # it's a submodule
                if prev_modname == package:
                    # first submodule - make parent a group head
                    entries[-1][1] = 1
                elif not prev_modname.startswith(package):
                    # submodule without parent in list, add dummy entry
                    entries.append([stripped + package, 1, '', '', '', '', ''])
                subtype = 2
            else:
                num_toplevels += 1
                subtype = 0

            qualifier = deprecated and _('Deprecated') or ''
            entries.append([stripped + modname, subtype, docname,
                            'module-' + stripped + modname, platforms,
                            qualifier, synopsis])
            prev_modname = modname

        # apply heuristics when to collapse modindex at page load:
        # only collapse if number of toplevel modules is larger than
        # number of submodules
        collapse = len(modules) - num_toplevels < num_toplevels

        # sort by first letter
        content = sorted(_iteritems(content))

        return content, collapse


class KLDomain(Domain):
    """KL language domain."""
    name = 'kl'
    label = 'KL'
    object_types = {
        'function': ObjType(l_('function'), 'func', 'method'),
		    }

    directives = {
        'function': KLModulelevel,
		    }

    roles = {
        'func':  KLXRefRole(fix_parens=False),
        'method':  KLXRefRole(fix_parens=False),
		    }
    initial_data = {
        'objects': {},  # fullname -> docname, objtype
        'modules': {},  # modname -> docname, synopsis, platform, deprecated
		    }
    indices = [
        KLModuleIndex,
		    ]

    def clear_doc(self, docname):
        for fullname, (fn, _) in list(self.data['objects'].items()):
            if fn == docname:
                del self.data['objects'][fullname]
        for modname, (fn, _, _, _) in list(self.data['modules'].items()):
            if fn == docname:
                del self.data['modules'][modname]

    def find_obj(self, env, modname, classname, name, type, searchorder=0):
        """
        Find a KL object for "name", perhaps using the given module and/or
        classname.
        """
        # skip parens
        if name[-2:] == '()':
            name = name[:-2]

        if not name:
            return None, None

        objects = self.data['objects']

        newname = None
        if searchorder == 1:
            if modname and classname and \
                     modname + '::' + classname + '#' + name in objects:
                newname = modname + '::' + classname + '#' + name
            elif modname and classname and \
                     modname + '::' + classname + '.' + name in objects:
                newname = modname + '::' + classname + '.' + name
            elif modname and modname + '::' + name in objects:
                newname = modname + '::' + name
            elif modname and modname + '#' + name in objects:
                newname = modname + '#' + name
            elif modname and modname + '.' + name in objects:
                newname = modname + '.' + name
            elif classname and classname + '.' + name in objects:
                newname = classname + '.' + name
            elif classname and classname + '#' + name in objects:
                newname = classname + '#' + name
            elif name in objects:
                newname = name
        else:
            if name in objects:
                newname = name
            elif classname and classname + '.' + name in objects:
                newname = classname + '.' + name
            elif classname and classname + '#' + name in objects:
                newname = classname + '#' + name
            elif modname and modname + '::' + name in objects:
                newname = modname + '::' + name
            elif modname and modname + '#' + name in objects:
                newname = modname + '#' + name
            elif modname and modname + '.' + name in objects:
                newname = modname + '.' + name
            elif modname and classname and \
                     modname + '::' + classname + '#' + name in objects:
                newname = modname + '::' + classname + '#' + name
            elif modname and classname and \
                     modname + '::' + classname + '.' + name in objects:
                newname = modname + '::' + classname + '.' + name
            # special case: object methods
            elif type in ('func', 'meth') and '.' not in name and \
                 'object.' + name in objects:
                newname = 'object.' + name
        if newname is None:
            return None, None
        return newname, objects[newname]

    def resolve_xref(self, env, fromdocname, builder,
                     typ, target, node, contnode):
        if (typ == 'mod' or
            typ == 'obj' and target in self.data['modules']):
            docname, synopsis, platform, deprecated = \
                self.data['modules'].get(target, ('','','', ''))
            if not docname:
                return None
            else:
                title = '%s%s%s' % ((platform and '(%s) ' % platform),
                                    synopsis,
                                    (deprecated and ' (deprecated)' or ''))
                return make_refnode(builder, fromdocname, docname,
                                    'module-' + target, contnode, title)
        else:
            modname = node.get('kl:module')
            clsname = node.get('kl:class')
            searchorder = node.hasattr('refspecific') and 1 or 0
            name, obj = self.find_obj(env, modname, clsname,
                                      target, typ, searchorder)
            if not obj:
                return None
            else:
                return make_refnode(builder, fromdocname, obj[0], name,
                                    contnode, name)

    def get_objects(self):
        for modname, info in _iteritems(self.data['modules']):
            yield (modname, modname, 'module', info[0], 'module-' + modname, 0)
        for refname, (docname, type) in _iteritems(self.data['objects']):
            yield (refname, refname, type, docname, refname, 1)

def setup(app):

    setupKLDirectives(app)
    app.add_domain(KLDomain)
    app.add_lexer('kl', KLLexer.KLLexer())

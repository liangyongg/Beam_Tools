# -*- coding: utf-8 -*-
#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from FabricEngine.Pygments import KLLexer

import os, re, subprocess

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


class KLExampleDirective(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 999999
    final_argument_whitespace = False
    option_spec = {
        'linenos': directives.flag,
        'no-output': directives.flag,
        }

    cache = {}

    def run(self):
        stdin = u'\n'.join(self.content)

        code = ""

        if len(self.arguments) > 0:
            code += """
/*
** Example: %s
*/

""" % ' '.join(self.arguments)
            print 'Performing KL-Example %s' % ' '.join(self.arguments)
        else:
            print 'Performing KL-Example'


        code += stdin

        if not(int(os.environ.get('FABRIC_DOCS_SKIP_EXAMPLES', 0))) and not 'no-output' in self.options and stdin.find('operator entry') > -1:

            if KLExampleDirective.cache.has_key(code):
              (stdout, stderr) = KLExampleDirective.cache[code]
            else:
              pipe = subprocess.Popen(
                  ['kl'],
                  stdin=subprocess.PIPE,
                  stdout=subprocess.PIPE,
                  stderr=subprocess.PIPE,
                  )
              (stdout, stderr) = pipe.communicate(code)

              newstderr = []
              for line in stderr.split('\n'):
                if line.startswith('[FABRIC'):
                  continue
                newstderr.append(line)
              stderr = '\n'.join(newstderr)

              KLExampleDirective.cache[code] = (stdout, stderr)

            code += """

/*
** Output:
%s
%s
*/
""" % (stderr, stdout)

        literal = nodes.literal_block(code, code)
        literal['language'] = 'kl'
        literal['linenos'] = 'linenos' in self.options
        set_source_info(self, literal)
        return [literal]

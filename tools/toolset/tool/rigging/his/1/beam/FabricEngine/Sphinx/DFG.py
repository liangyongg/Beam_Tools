# -*- coding: utf-8 -*-
#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

import subprocess
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive
from sphinx.util.nodes import set_source_info


class DFGExample(Directive):
    has_content = True
    required_arguments = 0
    optional_arguments = 99
    final_argument_whitespace = False
    option_spec = {
        'linenos': directives.flag,
        'no-output': directives.flag,
        }

    def run(self):
        stdin = u'\n'.join(self.content)

        code = ""

        if len(self.arguments) > 0:
            code += """
\"\"\"
Example: %s
\"\"\"

""" % ' '.join(self.arguments)

        code += stdin

        if not 'no-output' in self.options:
            pipe = subprocess.Popen(
                ['python'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                )
            (stdout, stderr) = pipe.communicate("""
import FabricEngine.Core, json, sys
client = FabricEngine.Core.createClient()
dfgHost = client.getDFGHost()
def notificationCallback(jsonString):
    for notif in json.loads(jsonString):
        print "[DFG NOTIFICATION: %%%%s]" %% json.dumps(notif, indent=1)
dfgHost.setNotificationCallback(notificationCallback)
%s
client.close()
""" % stdin)

            code += """

\"\"\"
*** Output:

%s
%s
\"\"\"
""" % (stderr, stdout)

        literal = nodes.literal_block(code, code)
        literal['language'] = 'python'
        literal['linenos'] = 'linenos' in self.options
        set_source_info(self, literal)
        return [literal]

def setup(app):
    app.add_directive('dfg-example', DFGExample)

import os
import subprocess
from KLBaseDirectiveImpl import KLBaseDirective

class CommandLineDirective(KLBaseDirective):

  def getContent(self):
    options = self.getOptions()

    result = []

    cmdLine = self.arguments

    result += ['.. code-block:: bash']
    result += ['    ']

    args = ''
    for arg in self.arguments:
      args += ' ' + arg
    result += ['   ' + args]
    result += []
    result += ['Result:']
    result += [' ']

    for i in range(len(cmdLine)):
      cmd = cmdLine[i]
      if cmd.startswith('$'):
        index = cmd.find('/')
        if index == -1:
          cmd = os.environ.get(cmd[1:], cmd)
        else:
          cmd = os.environ.get(cmd[1:index], cmd[:index]) + cmd[index:]
      cmdLine[i] = cmd

    pipe = subprocess.Popen(
        cmdLine,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        )
    (stdout, stderr) = pipe.communicate()

    lines = stdout.split('\n')

    result += ['.. code-block:: bash']
    result += ['    ']
    for line in lines:
      result += ['    '+line]

    return result

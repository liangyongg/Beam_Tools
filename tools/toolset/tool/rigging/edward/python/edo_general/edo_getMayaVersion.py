import maya.cmds as cmds
import maya.mel as mel
def edo_getMayaVersion():
    version=mel.eval('about -version')
    bit=''
    vs=version.split(' ')[0]
    #version='2012 x64'
    if int(vs)>=2014:
        return [version,'x64']
    else:
        if not 'x64' in version:
            return [version,'x32']
        else:
            return [version.split(' ')[0],version.split(' ')[1]]
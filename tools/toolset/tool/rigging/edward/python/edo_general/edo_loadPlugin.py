import maya.cmds as cmds
import edo_general.edo_getMayaVersion as EGMV
def edo_loadPlugin(pluginName):
    #pluginName='underworldBlendShape.mll'
    vs=EGMV.edo_getMayaVersion()
    mllpath=EGMV.__file__.replace('\\','/').split('.')[0].replace('python/edo_general/edo_getMayaVersion','mll')
    mpath=mllpath+'/maya'+vs[0]+'/'+vs[1]+'/'+pluginName
    cmds.loadPlugin(mpath,qt=1)